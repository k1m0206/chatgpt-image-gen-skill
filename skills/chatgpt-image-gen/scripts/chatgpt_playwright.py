#!/usr/bin/env python3
"""ChatGPT image generator v5: download original images through a logged-in browser."""

import argparse
import asyncio
import base64
import os
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_CDP_URL = os.environ.get("HERMES_CDP_URL", "http://127.0.0.1:9222")
DEFAULT_SAVE_DIR = Path(
    os.environ.get(
        "HERMES_CHATGPT_IMAGE_DIR",
        str(Path.home() / ".hermes" / "chatgpt_images"),
    )
).expanduser()


class ImageGenerationError(RuntimeError):
    """Raised when ChatGPT image generation cannot complete."""


def build_output_path(save_dir: Path) -> Path:
    return save_dir / f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"


async def download_image_from_page(page, src: str) -> bytes:
    b64 = await page.evaluate(
        """async (src) => {
            const r = await fetch(src, {credentials: 'include'});
            if (!r.ok) {
                throw new Error(`download failed: ${r.status} ${r.statusText}`);
            }
            const b = await r.blob();
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result.split(',')[1]);
                reader.onerror = () => reject(reader.error);
                reader.readAsDataURL(b);
            });
        }""",
        src,
    )
    return base64.b64decode(b64)


async def wait_for_generated_image(page, before_count: int, timeout_seconds: int) -> dict:
    attempts = max(1, timeout_seconds // 3)
    for i in range(attempts):
        await page.wait_for_timeout(3000)
        info = await page.evaluate(
            """(before) => {
                const imgs = document.querySelectorAll('img[src*="estuary"]');
                if (imgs.length <= before) return {newImage: false};
                const last = imgs[imgs.length - 1];
                return {
                    newImage: true,
                    width: last.naturalWidth,
                    height: last.naturalHeight,
                    complete: last.complete,
                    src: last.src
                };
            }""",
            before_count,
        )

        if info.get("newImage") and info.get("width", 0) > 100 and info.get("complete"):
            print(f"图片已加载 / Image loaded: {info['width']}x{info['height']} ({(i + 1) * 3}s)")
            return info

        if i % 5 == 4:
            print(f"等待中 / Waiting... ({(i + 1) * 3}s)")

    raise ImageGenerationError(f"生成超时 / Generation timed out after {timeout_seconds}s")


async def submit_prompt(page, prompt: str, prefix: str) -> None:
    textarea = page.locator("#prompt-textarea")
    await textarea.click(timeout=10000)
    await textarea.fill(f"{prefix}{prompt}")
    await page.wait_for_timeout(500)

    try:
        await page.locator('button[data-testid="send-button"]').click(timeout=3000)
    except Exception:
        await page.keyboard.press("Enter")


async def main(
    prompt: str,
    cdp_url: str = DEFAULT_CDP_URL,
    save_dir: Path = DEFAULT_SAVE_DIR,
    timeout_seconds: int = 150,
    prefix: str = "请生成一张图片：",
) -> str:
    try:
        from playwright.async_api import async_playwright
    except ModuleNotFoundError as exc:
        raise ImageGenerationError("缺少 Playwright / Missing Playwright. Run: pip install playwright") from exc

    save_dir.mkdir(parents=True, exist_ok=True)
    out = build_output_path(save_dir)
    page = None

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp(cdp_url)
        except Exception as exc:
            raise ImageGenerationError(
                f"无法连接浏览器调试端口 / Cannot connect to browser debugging port: {cdp_url}. "
                "请先用 --remote-debugging-port=9222 启动 Chrome、Edge、Brave 或 Chromium / "
                "Start Chrome, Edge, Brave, or Chromium with --remote-debugging-port=9222 first."
            ) from exc

        if not browser.contexts:
            raise ImageGenerationError(
                "已连接浏览器，但没有可用的登录上下文 / Connected to browser, but no usable logged-in context. "
                "请确认该浏览器中已登录 ChatGPT / Make sure ChatGPT is logged in inside that browser."
            )

        page = await browser.contexts[0].new_page()
        try:
            print("打开 ChatGPT / Opening ChatGPT...")
            await page.goto("https://chatgpt.com", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            before_count = await page.evaluate(
                """() => document.querySelectorAll('img[src*="estuary"]').length"""
            )

            print(f"输入 / Prompt: {prompt[:60]}...")
            await submit_prompt(page, prompt, prefix)

            print("等待生成 / Waiting for generation...")
            info = await wait_for_generated_image(page, before_count, timeout_seconds)

            print("下载原始图片 / Downloading original image...")
            out.write_bytes(await download_image_from_page(page, info["src"]))
            size_kb = out.stat().st_size // 1024
            print(f"已保存 / Saved: {out} ({size_kb}KB)")
            return str(out)
        finally:
            if page is not None:
                await page.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="通过 ChatGPT 网页生成图片并下载原始文件 / Generate images through ChatGPT web and download the original file."
    )
    parser.add_argument("prompt", help="图片描述 / image prompt")
    parser.add_argument("--cdp-url", default=DEFAULT_CDP_URL, help="浏览器 CDP 地址 / browser CDP URL")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_SAVE_DIR, help="图片输出目录 / image output directory")
    parser.add_argument("--timeout", type=int, default=150, help="等待生成的最长秒数 / max wait time in seconds")
    parser.add_argument(
        "--prefix",
        default="请生成一张图片：",
        help="发送给 ChatGPT 的提示词前缀 / prompt prefix sent to ChatGPT",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(
            main(
                args.prompt,
                cdp_url=args.cdp_url,
                save_dir=args.out_dir.expanduser(),
                timeout_seconds=args.timeout,
                prefix=args.prefix,
            )
        )
    except ImageGenerationError as exc:
        print(f"失败 / Failed: {exc}", file=sys.stderr)
        sys.exit(2)
