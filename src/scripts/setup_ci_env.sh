#!/usr/bin/env bash
# 在 GitHub Actions runner 上准备 repo-miner / md2wechat 跑得起来需要的全部依赖。
# 假定 runs-on: ubuntu-latest。
#
# 关键设计：
# - tokei / claude CLI 都装到用户级目录（~/.local/bin、~/.npm-global），避免 sudo
#   也让 actions/cache 直接缓存这两个目录，命中即跳过下载/安装。
# - 版本 pin 写在脚本顶部常量；升级时改一行，cache key 自动失效。
# - REQUIRE_PUBLISH=1 时强制校验微信发布凭证（用于 auto-analyze.yml 发布场景）；
#   其它场景（analyze.yml PR 流、auto-analyze 的 skip_publish=true）保留 WARN。
set -euo pipefail

# ---- 版本 pin（升级时改这里，cache key 因 hashFiles 此脚本而自动失效）----
readonly TOKEI_VERSION="12.1.2"
readonly CLAUDE_CODE_VERSION="2.1.159"

# ---- 用户级安装路径（无 sudo，可被 actions/cache 缓存）----
readonly LOCAL_BIN="$HOME/.local/bin"
readonly NPM_PREFIX="$HOME/.npm-global"
readonly REQ_FILE_REL="requirements-ci.txt"

log() { printf '\033[1;36m[setup]\033[0m %s\n' "$*"; }

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REQ_FILE="$REPO_ROOT/$REQ_FILE_REL"

# 让后续 step 自动找到用户级 bin（GITHUB_PATH 是 actions runner 提供的）
mkdir -p "$LOCAL_BIN" "$NPM_PREFIX"
export PATH="$NPM_PREFIX/bin:$LOCAL_BIN:$PATH"
if [[ -n "${GITHUB_PATH:-}" ]]; then
    echo "$NPM_PREFIX/bin" >> "$GITHUB_PATH"
    echo "$LOCAL_BIN"     >> "$GITHUB_PATH"
fi

log "1/5 安装 apt 依赖：gh, jq, tokei"
if ! command -v gh >/dev/null 2>&1; then
    # ubuntu-latest 已自带 gh，这里只是兜底
    sudo apt-get update -qq
    sudo apt-get install -y -qq gh jq
fi
command -v jq >/dev/null || sudo apt-get install -y -qq jq

if ! command -v tokei >/dev/null 2>&1; then
    log "  下载 tokei v${TOKEI_VERSION} 到 $LOCAL_BIN (无 sudo)"
    # curl --retry 处理临时网络抖动；--max-time 防止挂死
    curl --retry 3 --retry-delay 5 --max-time 90 -fsSL \
        "https://github.com/XAMPPRocky/tokei/releases/download/v${TOKEI_VERSION}/tokei-x86_64-unknown-linux-gnu.tar.gz" \
        | tar -xz -C "$LOCAL_BIN" tokei
    chmod +x "$LOCAL_BIN/tokei"
fi
tokei --version

log "2/5 安装 Node 和 Claude Code CLI (pin v${CLAUDE_CODE_VERSION})"
# 把 npm 全局 prefix 改到用户级，避免 sudo 且让 actions/cache 能直接缓存
npm config set prefix "$NPM_PREFIX" >/dev/null
if ! claude --version >/dev/null 2>&1; then
    log "  cache miss，安装 @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}"
    # timeout 防 install 挂死；--no-fund/--no-audit 省日志
    timeout 120 npm install -g \
        "@anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}" \
        --no-fund --no-audit
fi
claude --version

log "2b/5 安装 Python 依赖（pin 在 $REQ_FILE_REL）"
python3 -m pip install --quiet --upgrade pip
python3 -m pip install --quiet -r "$REQ_FILE"
python3 -c "
import premailer, bs4, markdown, yaml
print('  premailer', premailer.__version__)
print('  beautifulsoup4', bs4.__version__)
print('  markdown', markdown.__version__)
print('  pyyaml', yaml.__version__)
"

log "3/5 注入 vendored skills 到 ~/.claude/skills/"
mkdir -p ~/.claude/skills
for skill in repo-miner md2wechat; do
    src="$REPO_ROOT/ci/skills/$skill"
    if [[ ! -d "$src" ]]; then
        echo "ERR: 缺少 vendor skill $src，请先 cp -RL .claude/skills/$skill ci/skills/" >&2
        exit 1
    fi
    rm -rf "$HOME/.claude/skills/$skill"
    cp -r "$src" "$HOME/.claude/skills/$skill"
    log "  ✓ $skill -> $HOME/.claude/skills/$skill"
done

log "4/5 校验 .env 必需变量"
# 推理后端默认走 Minimax，MINIMAX_API_KEY 必填（或 ANTHROPIC_API_KEY 应急降级）
if [[ -z "${MINIMAX_API_KEY:-}" && -z "${ANTHROPIC_API_KEY:-}" ]]; then
    echo "ERR: MINIMAX_API_KEY 未设置（且无 ANTHROPIC_API_KEY 应急降级），无法跑 skill" >&2
    exit 1
fi
if [[ -z "${MINIMAX_API_KEY:-}" ]]; then
    echo "WARN: MINIMAX_API_KEY 未设置，将走 Anthropic 应急通道" >&2
fi

# 发布凭证：REQUIRE_PUBLISH=1 时硬性要求（auto-analyze 发布场景）
# 其它场景（PR 流 analyze.yml / skip_publish=true）只 WARN 不阻断
if [[ "${REQUIRE_PUBLISH:-0}" == "1" ]]; then
    missing=()
    for var in WECHAT_APPID WECHAT_APPSECRET WECHAT_PROXY_TOKEN; do
        [[ -z "${!var:-}" ]] && missing+=("$var")
    done
    if (( ${#missing[@]} > 0 )); then
        echo "ERR: REQUIRE_PUBLISH=1 但发布凭证缺失: ${missing[*]}" >&2
        echo "ERR: 拒绝继续，避免跑完 30min 分析后才在发布阶段失败" >&2
        exit 1
    fi
else
    for var in WECHAT_APPID WECHAT_APPSECRET; do
        if [[ -z "${!var:-}" ]]; then
            echo "WARN: $var 未设置（当前 REQUIRE_PUBLISH!=1，不阻断）" >&2
        fi
    done
fi

# publish-pending label 幂等创建（供 SSH 发布失败时打到 issue 上）
# 不强依赖：gh 未认证 / 权限不足时静默跳过
if [[ -n "${GH_TOKEN:-}" ]] && command -v gh >/dev/null 2>&1; then
    gh label create publish-pending \
        --color fbca04 \
        --description "SSH 发布临时失败，需异步重试" \
        --force >/dev/null 2>&1 || true
fi

log "5/5 准备运行时目录"
# 三阶段中间产物写 tmp/（不入库），不再预建 notes/
mkdir -p "$REPO_ROOT/tmp/logs" \
         "$REPO_ROOT/tmp/publish-pending" \
         "$REPO_ROOT/src/analysis_report"

log "环境初始化完成"
