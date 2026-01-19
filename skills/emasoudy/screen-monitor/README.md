# Screen-Monitor Skill

Browser-based screen sharing with vision analysis. Works with any multimodal LLM.

## Installation

```bash
clawdhub install screen-monitor
```

Or manual:
```bash
git clone https://github.com/emasoudy/clawdbot-skills.git
cp -r clawdbot-skills/screen-monitor ~/.clawdbot/skills/
```

## Usage

1. Get share link: `screen_share_link`
2. Open link in browser (e.g., `http://192.168.1.100:18795/screen-share`)
3. Click "Start Sharing"
4. Ask questions about your screen

## Requirements

- Multimodal LLM (Gemini, Claude, Qwen3-VL, etc.)
- Modern browser with WebRTC
- Optional: ImageMagick for OS fallback

## License

MIT - See LICENSE file
