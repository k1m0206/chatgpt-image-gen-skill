---
name: chatgpt-image-gen
description: 通过 Playwright 控制 Edge 浏览器，调用 ChatGPT 网页生成图片并下载原始图片发给用户
---

# ChatGPT 图片生成 Skill

## 触发条件
用户说：画XXX、生成XXX图片、帮我画、draw XXX、generate image of XXX

## 原理
Playwright CDP 连接已运行的 Edge（--remote-debugging-port=9222），在 ChatGPT 网页输入提示词，浏览器内 fetch 下载原始图片（自动带 cookie 认证）。

## 前置条件
1. Edge 用调试端口启动（见下文）
2. ChatGPT 已在 Edge 中登录
3. `pip3 install playwright`（只需 playwright，不需要 install chromium）

## 执行流程

### Step 1: 检查 Edge 调试端口
```bash
curl -s http://127.0.0.1:9222/json/version 2>/dev/null | head -1
```
如果失败，重启 Edge（用 terminal background=true）：
```bash
killall "Microsoft Edge" 2>/dev/null; sleep 2
"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" --remote-debugging-port=9222
```
等 5 秒后验证：`curl -s http://127.0.0.1:9222/json/version`

### Step 2: 运行脚本
```bash
python3 ~/.hermes/scripts/chatgpt_playwright.py "用户的图片描述"
```
脚本输出会包含 `✅ 已保存: /path/to/file.png (XXXkB)`

### Step 3: 发送图片
用 send_message 发送原始文件：
```
send_message(action="send", target="telegram:5656131857", message="MEDIA:/path/to/file.png\n描述文字")
```

## 脚本位置
~/.hermes/scripts/chatgpt_playwright.py

## 输出目录
~/.hermes/chatgpt_images/

## Pitfalls（已踩过的坑）

### ❌ 用 screenshot() 截图 → 图片质量差
- **错误**: `img_el.screenshot(path=...)` 只截到 1.1MB
- **正确**: 浏览器内 `fetch(url, {credentials:'include'})` → blob → base64 → 2MB 原图
- 原因：截图是渲染后的位图，fetch 下的是服务端原始文件

### ❌ 页面已有图片导致误匹配
- **错误**: 只检查 `img[src*="estuary"].length > 0` → 3秒就"成功"，截到的是旧图或头像
- **正确**: 先记录 `before = img count`，等待 `after > before`，且检查 `naturalWidth > 100 && complete === true`
- 原因：ChatGPT 页面预先加载了多张 estuary 图片（侧边栏 GPT 图标等）

### ❌ 截到空白占位符
- **错误**: 新 estuary 图片出现就截图 → 可能是未加载完的白色卡片
- **正确**: 等待 `naturalWidth > 100` + `complete === true`，确保图片真正渲染完成
- 原因：ChatGPT 先插入占位符 DOM，再异步加载图片内容

### ❌ Playwright launch_persistent_context 复用 Edge profile
- **错误**: `launch_persistent_context(user_data_dir=edge_data, channel="msedge")` → 显示未登录
- **正确**: 用 CDP 连接已运行的 Edge：`chromium.connect_over_cdp("http://127.0.0.1:9222")`
- 原因：Edge 的 profile 有锁机制，正在运行时 Playwright 无法独占访问

### ❌ curl 直接下载图片 URL
- **错误**: `curl -o img.png "https://chatgpt.com/backend-api/estuary/..."` → 39字节错误页
- **正确**: 必须在浏览器内 fetch（自动带 session cookie）
- 原因：estuary URL 需要登录态认证

## 工作风格
用户偏好简洁直接，不要冗长解释。生成完直接发图，附一句话说明即可。
