# 微信公众号 API 发布指南

## 环境变量

从项目根目录 `.env` 文件或系统环境变量读取：

```
WECHAT_APPID=your_appid
WECHAT_APPSECRET=your_appsecret
```

## API 流程

### 1. 获取 access_token

```bash
curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${WECHAT_APPID}&secret=${WECHAT_APPSECRET}"
```

响应：

```json
{
  "access_token": "ACCESS_TOKEN",
  "expires_in": 7200
}
```

注意：access_token 有效期 2 小时，每次发布前重新获取。

### 2. 获取封面图

从 Unsplash 获取暗色调随机图片，主题词随机轮换：

| 主题词 | 说明 |
|--------|------|
| stars | 星空 |
| universe | 宇宙 |
| ocean,dark | 深色海洋 |
| desert,night | 沙漠夜景 |
| forest,dark | 幽暗森林 |
| green-trees,nature | 绿树自然 |

```bash
# 随机选取一个主题词
THEME="stars,universe,dark"
curl -sL "https://source.unsplash.com/featured/900x383/?${THEME}" -o /tmp/wechat_cover.jpg
```

建议尺寸：900x383 px（微信推荐 2.35:1 比例）。

### 3. 上传封面图到素材库

```bash
curl -s -F "media=@/tmp/wechat_cover.jpg" \
  "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${ACCESS_TOKEN}&type=image"
```

响应：

```json
{
  "media_id": "MEDIA_ID",
  "url": "http://mmbiz.qpic.cn/..."
}
```

### 4. 发布到草稿箱

```bash
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [{
      "title": "文章标题",
      "author": "阳志平",
      "digest": "文章摘要（不超过120字）",
      "content": "<p>HTML正文内容</p>",
      "thumb_media_id": "MEDIA_ID",
      "need_open_comment": 0,
      "only_fans_can_comment": 0
    }]
  }'
```

响应：

```json
{
  "media_id": "DRAFT_MEDIA_ID"
}
```

### 5. 验证

发布成功后，在微信公众平台后台「草稿箱」中查看。

## 注意事项

- HTML 内容需使用 `<style>` 内嵌样式，微信会保留 `<style>` 标签内的样式
- 微信会清除 HTML 中的 class 属性，因此 CSS 须使用标签选择器
- 封面图建议 900x383 px，过大会被微信压缩
- digest（摘要）不超过 120 个字符
- content 字段中的 HTML 需转义 JSON 特殊字符
- 已认证的服务号或订阅号可使用草稿箱 API
