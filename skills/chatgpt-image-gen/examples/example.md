# Examples / 示例

## Chinese Prompt / 中文提示词
User:
```text
画一张赛博朋克猫侦探，电影感，雨夜
```

Run:
```bash
python skills/chatgpt-image-gen/scripts/chatgpt_playwright.py "赛博朋克猫侦探站在雨夜巷口，霓虹灯反射在湿润地面，电影感构图，戏剧化光影，高细节，真实质感"
```

Expected script output:
```text
已保存 / Saved: ~/.hermes/chatgpt_images/img_20260514_100000.png (2048KB)
```

## English Prompt / 英文提示词
User:
```text
Generate a cinematic samurai scene
```

Run:
```bash
python skills/chatgpt-image-gen/scripts/chatgpt_playwright.py "A lone samurai standing in heavy rain on an empty Kyoto street at night, cinematic composition, neon reflections on wet stone, dramatic backlight, misty atmosphere, high detail, realistic textures"
```

Expected script output:
```text
已保存 / Saved: ~/.hermes/chatgpt_images/img_20260514_100000.png (2048KB)
```

## Hermes Send / Hermes 发送
```text
send_message(action="send", target="<current conversation target>", message="MEDIA:/path/to/file.png\nImage generated")
```
