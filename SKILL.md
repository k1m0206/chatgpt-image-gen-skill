---
name: chatgpt-image-gen
description: Hermes agent 用于通过已登录且开启 CDP 调试端口的 Chromium 系浏览器调用 ChatGPT 网页生成图片，并下载原始图片文件。Use when the user asks to draw, generate, or create an image in Chinese or English.
---

# ChatGPT 图片生成 / ChatGPT Image Generation

## 触发条件 / Triggers
用户要求生成图片时使用。Use this skill when the user asks to generate an image, for example:

- 画一张赛博朋克城市图
- 生成产品海报图片
- draw a watercolor cat
- generate image of a futuristic car

中文或英文提示词都可以直接传给脚本。Chinese and English prompts can both be passed directly to the script.

## 原理 / How It Works
通过 Playwright CDP 连接已运行的 Chromium 系浏览器，在 ChatGPT 页面输入提示词。图片生成完成后，在浏览器上下文里 `fetch` 图片 URL，自动带上登录 cookie，下载原始图片文件。

Connect to a running Chromium-based browser through Playwright CDP, enter the prompt on ChatGPT, then fetch the generated image URL inside the browser context so the logged-in cookies are included.

支持 Chrome、Edge、Brave、Chromium 等 Chromium 系浏览器。不支持 Safari；Firefox 不能直接复用这套 CDP 流程。

Supports Chrome, Edge, Brave, Chromium, and other Chromium-based browsers. Safari is not supported; Firefox cannot reuse this CDP flow directly.

## 前置条件 / Requirements
1. 浏览器已用调试端口启动，默认端口为 `9222`。The browser is started with debugging port `9222`.
2. 同一个浏览器中已登录 ChatGPT。ChatGPT is logged in inside that same browser.
3. Python 环境已安装 Playwright：`pip install playwright`。Playwright is installed.
4. 脚本已安装到 Hermes 脚本目录：`~/.hermes/scripts/chatgpt_playwright.py`。The script is installed in the Hermes scripts directory.

## 安装 / Install
将仓库中的 `chatgpt_playwright.py` 复制到：

Copy `chatgpt_playwright.py` to:

```bash
~/.hermes/scripts/chatgpt_playwright.py
```

输出图片默认保存到：

Generated images are saved by default to:

```bash
~/.hermes/chatgpt_images/
```

## 启动浏览器调试端口 / Start Browser Debugging Port
Chrome macOS：

```bash
killall "Google Chrome" 2>/dev/null; sleep 2
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222
```

Edge macOS：

```bash
killall "Microsoft Edge" 2>/dev/null; sleep 2
"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" --remote-debugging-port=9222
```

Chrome Windows PowerShell：

```powershell
Stop-Process -Name chrome -ErrorAction SilentlyContinue
Start-Process "chrome.exe" -ArgumentList "--remote-debugging-port=9222"
```

Edge Windows PowerShell：

```powershell
Stop-Process -Name msedge -ErrorAction SilentlyContinue
Start-Process "msedge.exe" -ArgumentList "--remote-debugging-port=9222"
```

Brave Windows PowerShell：

```powershell
Stop-Process -Name brave -ErrorAction SilentlyContinue
Start-Process "brave.exe" -ArgumentList "--remote-debugging-port=9222"
```

验证 / Verify:

```bash
curl http://127.0.0.1:9222/json/version
```

## 执行流程 / Workflow
1. 确认浏览器调试端口可访问。Confirm that the browser debugging port is reachable.
2. 运行脚本。Run the script:
   ```bash
   python ~/.hermes/scripts/chatgpt_playwright.py "用户的图片描述 / user image prompt"
   ```
3. 从脚本输出中读取保存路径。Read the saved path from script output:
   ```text
   已保存 / Saved: /path/to/file.png (2048KB)
   ```
4. 将生成的原始图片文件发给用户。Send the generated original image file to the user.

Hermes 发送示例 / Hermes send example:

```
send_message(action="send", target="<当前会话目标 / current conversation target>", message="MEDIA:/path/to/file.png\n已生成图片 / Image generated")
```

不要写死用户 ID，优先使用当前会话目标。Do not hard-code user IDs; prefer the current conversation target.

## 可选参数 / Options
```bash
python ~/.hermes/scripts/chatgpt_playwright.py "描述 / prompt" --timeout 180 --cdp-url http://127.0.0.1:9222 --out-dir ~/.hermes/chatgpt_images
```

- `--cdp-url`：浏览器 CDP 地址。Browser CDP URL.
- `--out-dir`：图片输出目录。Image output directory.
- `--timeout`：等待生成的最长秒数。Maximum wait time in seconds.
- `--prefix`：发送给 ChatGPT 的提示词前缀。Prompt prefix sent to ChatGPT.

也可以用环境变量。Environment variables:

- `HERMES_CDP_URL`：覆盖默认 CDP 地址。Override the default CDP URL.
- `HERMES_CHATGPT_IMAGE_DIR`：覆盖默认输出目录。Override the default output directory.

## 注意事项 / Notes
### 不要用 screenshot 截图 / Do not use screenshots
截图是渲染后的位图，质量通常低于原图。应使用浏览器内 `fetch(url, { credentials: "include" })` 下载原始文件。

Screenshots are rendered bitmaps and are usually lower quality. Use browser-side `fetch(url, { credentials: "include" })` to download the original file.

### 不要匹配旧图片 / Do not match old images
ChatGPT 页面可能已有图片。先记录生成前图片数量，再等待新图片出现，并确认 `naturalWidth > 100` 且 `complete === true`。

The ChatGPT page may already contain images. Record the image count before generation, then wait for a new image and confirm `naturalWidth > 100` and `complete === true`.

### 不要直接 curl 图片 URL / Do not curl the image URL directly
图片 URL 需要登录态。直接在终端下载通常只会得到错误页，必须在浏览器上下文内 fetch。

The image URL requires an authenticated session. Downloading it directly from the terminal usually returns an error page, so fetch it inside the browser context.

### 不要复用正在运行的浏览器 profile 启动新浏览器 / Do not launch a new browser with an active profile
不要用 `launch_persistent_context` 打开正在使用的浏览器 profile。应连接已运行且已登录的浏览器：`chromium.connect_over_cdp(...)`。

Do not use `launch_persistent_context` with a browser profile that is already in use. Connect to the already running and logged-in browser with `chromium.connect_over_cdp(...)`.

## 工作风格 / Response Style
生成完成后直接发送图片，附一句简短说明即可。失败时只说明最可能的原因和下一步操作。

After generation, send the image directly with one short note. On failure, state the most likely cause and the next action.
