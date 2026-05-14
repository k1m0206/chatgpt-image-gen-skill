# ChatGPT Image Gen Skill

Professional ChatGPT image generation skill for Hermes Agent.

Hermes Agent 的 ChatGPT 图片生成 skill，支持通过已登录的 Chromium 系浏览器调用 ChatGPT 网页生成图片，并下载原始图片文件。

## Features / 功能
- Generate images through ChatGPT web UI.
- Download original images instead of screenshots.
- Support Chinese and English prompts.
- Support Chrome, Edge, Brave, Chromium, and other Chromium-based browsers.
- Provide cinematic prompt template and examples.
- Configurable CDP URL, output directory, timeout, and prompt prefix.

中文：
- 通过 ChatGPT 网页生成图片。
- 下载原始图片，不使用低质量截图。
- 支持中文和英文提示词。
- 支持 Chrome、Edge、Brave、Chromium 等 Chromium 系浏览器。
- 内置电影感提示词模板和示例。
- 支持自定义 CDP 地址、输出目录、超时时间和提示词前缀。

## Install / 安装
Add this repository as a Hermes skill tap:

添加这个仓库作为 Hermes skill tap：

```bash
hermes skills tap add k1m0206/chatgpt-image-gen-skill
```

Search:

搜索：

```bash
hermes skills search image
```

Install:

安装：

```bash
hermes skills install chatgpt-image-gen
```

Or install by full path:

也可以使用完整路径安装：

```bash
hermes skills install k1m0206/chatgpt-image-gen-skill/chatgpt-image-gen
```

## Repository Structure / 仓库结构
```text
chatgpt-image-gen-skill/
├── README.md
├── LICENSE
└── skills/
    └── chatgpt-image-gen/
        ├── SKILL.md
        ├── scripts/
        │   └── chatgpt_playwright.py
        ├── templates/
        │   └── cinematic.md
        └── examples/
            └── example.md
```

Hermes scans:

Hermes 会扫描：

```text
skills/*/SKILL.md
```

## Requirements / 前置条件
1. Python is installed. 已安装 Python。
2. Playwright is installed. 已安装 Playwright：
   ```bash
   pip install playwright
   ```
3. A Chromium-based browser is logged in to ChatGPT. Chromium 系浏览器已登录 ChatGPT。
4. The browser is started with `--remote-debugging-port=9222`. 浏览器用调试端口启动。

## Start Browser Debugging Port / 启动浏览器调试端口
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

Verify:

验证：

```bash
curl http://127.0.0.1:9222/json/version
```

## Usage / 使用
Ask Hermes:

向 Hermes 发送：

```text
Generate a cinematic samurai scene
```

or:

或者：

```text
画一张赛博朋克猫侦探，电影感，雨夜
```

Direct script usage:

直接运行脚本：

```bash
python skills/chatgpt-image-gen/scripts/chatgpt_playwright.py "a cat in an astronaut suit, cinematic, high detail"
```

Successful output:

成功输出：

```text
已保存 / Saved: ~/.hermes/chatgpt_images/img_20260514_100000.png (2048KB)
```

## Options / 参数
```bash
python skills/chatgpt-image-gen/scripts/chatgpt_playwright.py "prompt" --timeout 180 --cdp-url http://127.0.0.1:9222 --out-dir ~/.hermes/chatgpt_images
```

- `--cdp-url`: Browser CDP URL. 浏览器 CDP 地址。
- `--out-dir`: Image output directory. 图片输出目录。
- `--timeout`: Maximum wait time in seconds. 最长等待秒数。
- `--prefix`: Prompt prefix sent to ChatGPT. 发送给 ChatGPT 的提示词前缀。

Environment variables:

环境变量：

- `HERMES_CDP_URL`
- `HERMES_CHATGPT_IMAGE_DIR`

## Examples / 示例
See:

查看：

- `skills/chatgpt-image-gen/examples/example.md`
- `skills/chatgpt-image-gen/templates/cinematic.md`

## GitHub Topics / 推荐 Topics
Recommended GitHub repository topics:

推荐设置这些 GitHub Topics：

```text
hermes-skill
ai-agent
prompt-engineering
image-generation
chatgpt
ai-art
chromium
playwright
```

## License / 许可证
MIT
