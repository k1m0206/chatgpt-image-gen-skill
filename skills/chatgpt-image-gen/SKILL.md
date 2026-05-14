---
name: chatgpt-image-gen
description: Generate images with ChatGPT through a logged-in Chromium browser, download original image files, and support Chinese/English image prompts. Use when the user asks to draw, generate, create, or refine an image prompt.
version: 1.0.0
author: k1m0206
tags:
  - image
  - image-generation
  - chatgpt
  - prompt-engineering
  - ai-art
  - hermes-skill
---

# ChatGPT Image Gen / ChatGPT 图片生成

## Use When / 触发条件
Use this skill when the user asks to generate or refine an image in Chinese or English.

当用户用中文或英文要求生成图片、优化图片提示词、创建图像描述时使用。

Examples:
- 画一张赛博朋克城市图
- 生成产品海报图片
- draw a watercolor cat
- generate image of a futuristic car
- optimize this prompt for cinematic image generation

## Capabilities / 能力
- Generate images through the logged-in ChatGPT web UI.
- Download original image files instead of low-quality screenshots.
- Support Chinese and English image prompts.
- Work with Chrome, Edge, Brave, Chromium, and other Chromium-based browsers.
- Allow custom CDP URL, output directory, timeout, and prompt prefix.
- Provide prompt guidance using bundled templates and examples.

能力：
- 通过已登录的 ChatGPT 网页生成图片。
- 下载原始图片文件，不使用低质量截图。
- 支持中文和英文提示词。
- 支持 Chrome、Edge、Brave、Chromium 等 Chromium 系浏览器。
- 支持自定义 CDP 地址、输出目录、超时时间和提示词前缀。
- 可参考内置模板和示例优化提示词。

## Requirements / 前置条件
1. A Chromium-based browser is started with debugging port `9222`.
2. ChatGPT is logged in inside that same browser.
3. Playwright is installed:
   ```bash
   pip install playwright
   ```
4. The script exists at:
   ```bash
   skills/chatgpt-image-gen/scripts/chatgpt_playwright.py
   ```

中文：
1. 浏览器已用调试端口 `9222` 启动。
2. 同一个浏览器中已登录 ChatGPT。
3. 已安装 Playwright：`pip install playwright`。
4. 脚本位于：`skills/chatgpt-image-gen/scripts/chatgpt_playwright.py`。

## Browser Setup / 启动浏览器调试端口
Chrome macOS:
```bash
killall "Google Chrome" 2>/dev/null; sleep 2
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222
```

Edge macOS:
```bash
killall "Microsoft Edge" 2>/dev/null; sleep 2
"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" --remote-debugging-port=9222
```

Chrome Windows PowerShell:
```powershell
Stop-Process -Name chrome -ErrorAction SilentlyContinue
Start-Process "chrome.exe" -ArgumentList "--remote-debugging-port=9222"
```

Edge Windows PowerShell:
```powershell
Stop-Process -Name msedge -ErrorAction SilentlyContinue
Start-Process "msedge.exe" -ArgumentList "--remote-debugging-port=9222"
```

Brave Windows PowerShell:
```powershell
Stop-Process -Name brave -ErrorAction SilentlyContinue
Start-Process "brave.exe" -ArgumentList "--remote-debugging-port=9222"
```

Verify / 验证:
```bash
curl http://127.0.0.1:9222/json/version
```

## Workflow / 执行流程
1. Confirm the browser debugging port is reachable.
2. Run the bundled script with the user's prompt:
   ```bash
   python skills/chatgpt-image-gen/scripts/chatgpt_playwright.py "user image prompt"
   ```
3. Read the saved path from script output:
   ```text
   已保存 / Saved: /path/to/file.png (2048KB)
   ```
4. Send the original image file to the user.

Hermes send example:
```
send_message(action="send", target="<current conversation target>", message="MEDIA:/path/to/file.png\nImage generated")
```

Do not hard-code user IDs. Prefer the current conversation target.

## Options / 可选参数
```bash
python skills/chatgpt-image-gen/scripts/chatgpt_playwright.py "描述 / prompt" --timeout 180 --cdp-url http://127.0.0.1:9222 --out-dir ~/.hermes/chatgpt_images
```

- `--cdp-url`: Browser CDP URL. 浏览器 CDP 地址。
- `--out-dir`: Image output directory. 图片输出目录。
- `--timeout`: Maximum wait time in seconds. 等待生成的最长秒数。
- `--prefix`: Prompt prefix sent to ChatGPT. 发送给 ChatGPT 的提示词前缀。

Environment variables:
- `HERMES_CDP_URL`: Override the default CDP URL.
- `HERMES_CHATGPT_IMAGE_DIR`: Override the default output directory.

环境变量：
- `HERMES_CDP_URL`：覆盖默认 CDP 地址。
- `HERMES_CHATGPT_IMAGE_DIR`：覆盖默认输出目录。

## Prompt Templates / 提示词模板
For richer prompt writing, read:
- `templates/cinematic.md`

Examples are in:
- `examples/example.md`

## Notes / 注意事项
### Do not use screenshots / 不要用截图
Screenshots are rendered bitmaps and are usually lower quality. Use browser-side `fetch(url, { credentials: "include" })` to download the original file.

截图是渲染后的位图，质量通常低于原图。应使用浏览器内 `fetch(url, { credentials: "include" })` 下载原始文件。

### Do not match old images / 不要匹配旧图片
The ChatGPT page may already contain images. Record the image count before generation, then wait for a new image and confirm `naturalWidth > 100` and `complete === true`.

ChatGPT 页面可能已有图片。先记录生成前图片数量，再等待新图片出现，并确认 `naturalWidth > 100` 且 `complete === true`。

### Do not curl image URLs directly / 不要直接 curl 图片 URL
The image URL requires an authenticated session. Downloading it directly from the terminal usually returns an error page, so fetch it inside the browser context.

图片 URL 需要登录态。直接在终端下载通常只会得到错误页，必须在浏览器上下文内 fetch。

### Do not launch a new browser with an active profile / 不要复用正在运行的 profile
Do not use `launch_persistent_context` with a browser profile that is already in use. Connect to the already running and logged-in browser with `chromium.connect_over_cdp(...)`.

不要用 `launch_persistent_context` 打开正在使用的浏览器 profile。应连接已运行且已登录的浏览器：`chromium.connect_over_cdp(...)`。

## Response Style / 回复风格
After generation, send the image directly with one short note. On failure, state the most likely cause and the next action.

生成完成后直接发送图片，附一句简短说明即可。失败时只说明最可能的原因和下一步操作。
