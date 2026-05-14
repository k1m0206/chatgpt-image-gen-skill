# chatgpt-image-gen

Hermes agent 使用的 ChatGPT 图片生成 skill。它通过已登录并开启 CDP 调试端口的 Chromium 系浏览器访问 ChatGPT，生成图片后下载原始图片文件。

ChatGPT image generation skill for Hermes agent. It uses a logged-in Chromium-based browser with a CDP debugging port enabled, asks ChatGPT to generate an image, then downloads the original image file.

支持 Chrome、Edge、Brave、Chromium 等 Chromium 系浏览器。不支持 Safari；Firefox 不能直接复用当前 CDP 流程。

Supports Chromium-based browsers such as Chrome, Edge, Brave, and Chromium. Safari is not supported; Firefox cannot reuse this CDP flow directly.

## 文件 / Files
- `SKILL.md`：给 Hermes agent 读取的 skill 指令。Skill instructions for Hermes agent.
- `chatgpt_playwright.py`：实际执行图片生成和原图下载的脚本。Script that generates the image and downloads the original file.

## 前置条件 / Requirements
1. Python 已安装。Python is installed.
2. 已安装 Playwright。Playwright is installed:
   ```bash
   pip install playwright
   ```
3. Chromium 系浏览器已登录 ChatGPT。A Chromium-based browser is logged in to ChatGPT.
4. 浏览器用 `--remote-debugging-port=9222` 启动。The browser is started with `--remote-debugging-port=9222`.

## 安装到 Hermes / Install for Hermes
将脚本复制到 Hermes 脚本目录：

Copy the script to the Hermes scripts directory:

```bash
mkdir -p ~/.hermes/scripts
cp chatgpt_playwright.py ~/.hermes/scripts/chatgpt_playwright.py
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

验证调试端口：

Verify the debugging port:

```bash
curl http://127.0.0.1:9222/json/version
```

## 使用 / Usage
直接运行：

Run directly:

```bash
python ~/.hermes/scripts/chatgpt_playwright.py "一只穿宇航服的猫，电影感，高清"
python ~/.hermes/scripts/chatgpt_playwright.py "a cat in an astronaut suit, cinematic, high detail"
```

成功后输出类似：

Successful output looks like:

```text
已保存 / Saved: /Users/name/.hermes/chatgpt_images/img_20260514_100000.png (2048KB)
```

Hermes agent 读取这个路径后，将原始图片文件发送给用户。

Hermes agent reads this path and sends the original image file to the user.

## 参数 / Options
```bash
python ~/.hermes/scripts/chatgpt_playwright.py "描述 / prompt" --timeout 180 --cdp-url http://127.0.0.1:9222 --out-dir ~/.hermes/chatgpt_images
```

- `--cdp-url`：浏览器 CDP 地址，默认 `http://127.0.0.1:9222`。Browser CDP URL. Default: `http://127.0.0.1:9222`.
- `--out-dir`：图片输出目录，默认 `~/.hermes/chatgpt_images`。Image output directory. Default: `~/.hermes/chatgpt_images`.
- `--timeout`：等待生成的最长秒数，默认 `150`。Maximum wait time in seconds. Default: `150`.
- `--prefix`：发送给 ChatGPT 的提示词前缀，默认 `请生成一张图片：`。Prompt prefix sent to ChatGPT. Default: `请生成一张图片：`.

也可以用环境变量覆盖默认值：

Defaults can also be overridden with environment variables:

- `HERMES_CDP_URL`
- `HERMES_CHATGPT_IMAGE_DIR`

## 常见问题 / FAQ
### 无法连接浏览器调试端口 / Cannot connect to browser debugging port
确认浏览器是用 `--remote-debugging-port=9222` 启动的，并且 `curl http://127.0.0.1:9222/json/version` 能返回内容。

Make sure the browser was started with `--remote-debugging-port=9222`, and `curl http://127.0.0.1:9222/json/version` returns a response.

### 已连接浏览器但没有登录上下文 / Connected, but no logged-in context
确认打开的是同一个浏览器实例，并且该浏览器里已经登录 ChatGPT。

Make sure this is the same browser instance and ChatGPT is logged in there.

### 生成超时 / Generation timed out
可能是 ChatGPT 页面未响应、模型没有开始生成、网络慢，或者页面结构变化。先手动打开 ChatGPT 确认能正常生成图片。

ChatGPT may be unresponsive, image generation may not have started, the network may be slow, or the page structure may have changed. Open ChatGPT manually and confirm image generation works.

### 下载到错误页或小文件 / Downloaded an error page or tiny file
不要用终端直接下载图片 URL。图片需要登录态，脚本必须在浏览器上下文里 `fetch` 才能拿到原图。

Do not download the image URL directly from the terminal. The image requires a logged-in session, so the script must fetch it inside the browser context.
