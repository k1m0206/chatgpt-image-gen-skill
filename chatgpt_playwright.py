#!/usr/bin/env python3
"""ChatGPT 图片生成器 v4 — 直接下载原始图片"""

import asyncio, sys, base64
from pathlib import Path
from datetime import datetime

CDP = "http://127.0.0.1:9222"
SAVE_DIR = Path.home() / ".hermes" / "chatgpt_images"

async def main(prompt: str):
    from playwright.async_api import async_playwright
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    out = SAVE_DIR / f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        page = await browser.contexts[0].new_page()

        print("🌐 打开 ChatGPT...")
        await page.goto("https://chatgpt.com", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        before = await page.evaluate("() => document.querySelectorAll('img[src*=\"estuary\"]').length")

        print(f"✏️  输入: {prompt[:40]}...")
        ta = page.locator("#prompt-textarea")
        await ta.click()
        await ta.fill(f"请生成一张图片：{prompt}")
        await page.wait_for_timeout(500)

        print("📤 发送...")
        try:
            await page.locator('button[data-testid="send-button"]').click(timeout=3000)
        except:
            await page.keyboard.press("Enter")

        print("⏳ 等待生成...")
        for i in range(50):
            await page.wait_for_timeout(3000)

            info = await page.evaluate("""(before) => {
                const imgs = document.querySelectorAll('img[src*="estuary"]');
                if (imgs.length <= before) return {new: false};
                const last = imgs[imgs.length - 1];
                return {
                    new: true,
                    w: last.naturalWidth,
                    h: last.naturalHeight,
                    complete: last.complete,
                    src: last.src
                };
            }""", before)

            if info.get("new") and info.get("w", 0) > 100 and info.get("complete"):
                print(f"📸 图片已加载! {info['w']}x{info['h']} ({(i+1)*3}s)")

                # 直接 fetch 下载原始图片
                print("💾 下载原始图片...")
                b64 = await page.evaluate("""async (src) => {
                    const r = await fetch(src, {credentials: 'include'});
                    const b = await r.blob();
                    return new Promise(res => {
                        const reader = new FileReader();
                        reader.onload = () => res(reader.result.split(',')[1]);
                        reader.readAsDataURL(b);
                    });
                }""", info["src"])

                out.write_bytes(base64.b64decode(b64))
                sz = out.stat().st_size
                print(f"✅ 已保存: {out} ({sz//1024}KB)")
                await page.close()
                return str(out)

            if i % 5 == 4:
                print(f"   等待中... ({(i+1)*3}s)")

        print("❌ 超时")
        await page.close()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 chatgpt_playwright.py \"描述\"")
        sys.exit(1)
    asyncio.run(main(sys.argv[1]))
