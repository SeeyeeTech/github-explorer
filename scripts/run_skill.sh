#!/usr/bin/env bash
# 调用 Claude Code skill，走 Minimax 的 Anthropic 兼容端点。
#
# 默认行为：
#   - ANTHROPIC_BASE_URL 写死指向 Minimax（公开常量，非 secret）
#   - 用 MINIMAX_API_KEY 作为 ANTHROPIC_AUTH_TOKEN（Minimax 官方要求的变量名）
#   - 主动清空 ANTHROPIC_API_KEY，避免 Claude CLI 错误地走官方接口
#   - 失败时同后端指数退避重试（BACKOFFS 控制；处理临时网络抖动 / 限流）
#
# 应急降级（不建议常用，需手动设 FORCE_BACKEND）：
#   FORCE_BACKEND=anthropic + ANTHROPIC_API_KEY=sk-ant-...
#   → 强制走 Anthropic 官方接口，跳过 Minimax
#
# Usage:
#   run_skill.sh <prompt> [--timeout <sec>] [--log <path>] [--retries <N>]
#
# 退出码：
#   0    成功
#   非0  失败（透传 claude 退出码）
#   124  超时（不重试）
#   2    配置错（不重试）

set -uo pipefail

# Minimax Anthropic 兼容端点（公开常量）
# 国内版默认；国际版用 https://api.minimax.io/anthropic
MINIMAX_ENDPOINT="${MINIMAX_BASE_URL_OVERRIDE:-https://api.minimaxi.com/anthropic}"

PROMPT="${1:?用法: run_skill.sh <prompt> [--timeout N] [--log path]}"
shift

TIMEOUT_SEC=1500
LOG_FILE=""
MAX_RETRIES=2                # 同后端重试次数（共 3 次尝试）
BACKOFFS=(10 30)             # len 必须 == MAX_RETRIES；指数退避秒数

while [[ $# -gt 0 ]]; do
    case "$1" in
        --timeout) TIMEOUT_SEC="$2"; shift 2 ;;
        --log)     LOG_FILE="$2";    shift 2 ;;
        --retries) MAX_RETRIES="$2"; shift 2 ;;
        *) echo "未知参数: $1" >&2; exit 2 ;;
    esac
done

if [[ -z "$LOG_FILE" ]]; then
    mkdir -p tmp/logs
    LOG_FILE="tmp/logs/run-$(date +%Y%m%d-%H%M%S)-$$.log"
fi

# 兼容 macOS：优先 gtimeout，其次 timeout，都没有就不加超时
if command -v timeout >/dev/null 2>&1; then
    TIMEOUT_CMD=(timeout)
elif command -v gtimeout >/dev/null 2>&1; then
    TIMEOUT_CMD=(gtimeout)
else
    TIMEOUT_CMD=()
fi

log() { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*" | tee -a "$LOG_FILE" >&2; }

run_once() {
    local backend="$1"
    local -a env_args=()

    case "$backend" in
        minimax)
            if [[ -z "${MINIMAX_API_KEY:-}" ]]; then
                log "MINIMAX_API_KEY 未设置"
                return 2
            fi
            env_args=(
                "ANTHROPIC_BASE_URL=$MINIMAX_ENDPOINT"
                "ANTHROPIC_AUTH_TOKEN=$MINIMAX_API_KEY"
                # 显式清空官方 key 防止冲突（Minimax 文档建议）
                "ANTHROPIC_API_KEY="
            )
            log "后端: minimax ($MINIMAX_ENDPOINT)"
            ;;
        anthropic)
            if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
                log "ANTHROPIC_API_KEY 未设置，无法应急降级"
                return 2
            fi
            env_args=(
                "ANTHROPIC_BASE_URL="
                "ANTHROPIC_AUTH_TOKEN="
                "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY"
            )
            log "后端: anthropic (应急降级)"
            ;;
        *) log "未知后端 $backend"; return 1 ;;
    esac

    local cmd=()
    if [[ ${#TIMEOUT_CMD[@]} -gt 0 ]]; then
        # --kill-after：SIGTERM 后 30s 内若进程仍在则发 SIGKILL，
        # 避免 Claude CLI 忽略 SIGTERM 时卡满 job timeout-minutes
        cmd=("${TIMEOUT_CMD[@]}" --kill-after=30s "$TIMEOUT_SEC")
    fi
    cmd+=(env "${env_args[@]}" claude -p "$PROMPT" --dangerously-skip-permissions)

    set +e
    "${cmd[@]}" 2>&1 | tee -a "$LOG_FILE"
    local rc=$?
    set -e
    return "$rc"
}

# 默认只跑 Minimax；FORCE_BACKEND=anthropic 时切应急通道
BACKEND="${FORCE_BACKEND:-minimax}"
case "$BACKEND" in
    minimax|anthropic) ;;
    *) log "FORCE_BACKEND 取值非法: $BACKEND"; exit 2 ;;
esac

for attempt in $(seq 0 "$MAX_RETRIES"); do
    if [[ $attempt -gt 0 ]]; then
        # BACKOFFS 长度 == MAX_RETRIES；index = attempt-1
        delay="${BACKOFFS[$((attempt-1))]:-30}"
        log "重试 $attempt/$MAX_RETRIES，退避 ${delay}s"
        sleep "$delay"
        if [[ $attempt -eq $MAX_RETRIES ]]; then
            # GH Actions 日志高亮，便于事后追因
            echo "::warning::$BACKEND 已重试到最后一次（${MAX_RETRIES} 次重试用尽）" >&2
        fi
    fi
    rc=0
    run_once "$BACKEND" || rc=$?
    if [[ $rc -eq 0 ]]; then
        log "成功 ($BACKEND)"
        exit 0
    fi
    if [[ $rc -eq 124 ]]; then
        log "$BACKEND 超时 (${TIMEOUT_SEC}s)，不重试"
        exit 124
    fi
    if [[ $rc -eq 2 ]]; then
        log "$BACKEND 配置缺失"
        exit 2
    fi
    log "$BACKEND 失败 rc=$rc"
done

log "重试用尽，最终失败 rc=$rc"
exit "$rc"
