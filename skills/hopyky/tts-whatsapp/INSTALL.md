# 📦 Installation Guide

Complete installation guide for the tts-whatsapp skill.

## Prerequisites

Before installing this skill, ensure you have:

1. ✅ **Clawdbot** installed and configured
2. ✅ **WhatsApp** connected to Clawdbot
3. ✅ **Node.js** v14 or higher
4. ✅ **Python 3.9+** (for Piper TTS)

## Step 1: Install Dependencies

### Install Piper TTS

```bash
# macOS / Linux
pip3 install --user piper-tts

# Verify installation
piper --version
```

### Install FFmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Fedora/RHEL
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg

# Verify installation
ffmpeg -version
```

## Step 2: Install the Skill

### Option A: Via ClawdHub (Recommended)

```bash
# Coming soon - ClawdHub automatic installation
clawdbot skills install tts-whatsapp
```

### Option B: Manual Installation

```bash
# Clone or download this repository
cd ~/.clawdbot/skills/
git clone https://github.com/clawdbot/clawdhub.git temp
cp -r temp/skills/tts-whatsapp tts-whatsapp
rm -rf temp

# Or download and extract manually
mkdir -p ~/.clawdbot/skills/tts-whatsapp
cd ~/.clawdbot/skills/tts-whatsapp
# Extract downloaded files here
```

## Step 3: Download Voice Models

### Choose Your Language

Visit [Piper Voice Samples](https://rhasspy.github.io/piper-samples/) to listen to available voices.

### Download Models

```bash
# Create models directory
mkdir -p ~/.clawdbot/skills/piper-tts/models/

# Example: Download French model (siwis, medium quality)
cd ~/.clawdbot/skills/piper-tts/models/

# Download .onnx file
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx

# Download .onnx.json file (required)
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json
```

### Popular Models to Download

```bash
# English US (lessac - female, high quality)
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

# Spanish ES (carlfm - male)
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/carlfm/medium/es_ES-carlfm-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/carlfm/medium/es_ES-carlfm-medium.onnx.json

# German (thorsten - male, high quality)
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json
```

**Note:** Always download BOTH the `.onnx` and `.onnx.json` files for each model.

## Step 4: Configure the Skill

Edit your Clawdbot configuration:

```bash
nano ~/.clawdbot/clawdbot.json
```

Add the skill configuration:

```json
{
  "skills": {
    "entries": {
      "tts_whatsapp": {
        "enabled": true,
        "env": {
          "PIPER_BIN_PATH": "/Users/YOUR_USERNAME/Library/Python/3.9/bin/piper",
          "WHATSAPP_DEFAULT_TARGET": "+15555550123",
          "PIPER_DEFAULT_LANG": "en_US",
          "PIPER_DEFAULT_VOICE": "lessac",
          "PIPER_DEFAULT_QUALITY": "medium"
        }
      }
    }
  }
}
```

### Configuration Values

Replace these values:

- `PIPER_BIN_PATH`: Run `which piper` to find your path
- `WHATSAPP_DEFAULT_TARGET`: Your WhatsApp number in E.164 format (+1234567890)
- `PIPER_DEFAULT_LANG`: Your preferred language code
- `PIPER_DEFAULT_VOICE`: Your preferred voice name
- `PIPER_DEFAULT_QUALITY`: `x_low`, `low`, `medium`, or `high`

### Find WhatsApp Group IDs

To send to a WhatsApp group, you need the group ID:

```bash
# List recent messages to see group IDs
clawdbot message read --channel whatsapp

# Group IDs look like: 120363257357161211@g.us
```

## Step 5: Test the Installation

### Test TTS generation (without sending)

```bash
tts-whatsapp "This is a test" --no-send
```

You should see:
- ✅ TTS generation successful
- ✅ Conversion to OGG successful
- ✅ File path displayed

### Test sending to yourself

```bash
tts-whatsapp "Test message to myself"
```

You should receive the voice message on WhatsApp.

### Test different language

```bash
tts-whatsapp "Hola mundo" --lang es_ES --voice carlfm
```

## Troubleshooting

### Piper not found

```bash
# Find piper location
which piper

# If not found, reinstall
pip3 install --user piper-tts

# Check Python bin directory
ls ~/Library/Python/3.9/bin/  # macOS
ls ~/.local/bin/               # Linux
```

### FFmpeg not found

```bash
# Verify FFmpeg installation
which ffmpeg
ffmpeg -version

# Reinstall if needed (see Step 1)
```

### Model not found

```
ERROR: Modèle introuvable: ~/.clawdbot/skills/piper-tts/models/en_US-lessac-medium.onnx
```

**Solution:** Make sure you downloaded BOTH files:
- `en_US-lessac-medium.onnx`
- `en_US-lessac-medium.onnx.json`

### Permission denied

```bash
# Make the script executable
chmod +x ~/.clawdbot/skills/tts-whatsapp/bin/tts-whatsapp
```

### No default target error

Either:
1. Set `WHATSAPP_DEFAULT_TARGET` in your config, OR
2. Always use `--target` when calling the command

## Upgrade

To upgrade to a newer version:

```bash
# Via ClawdHub (when available)
clawdbot skills update tts-whatsapp

# Manual upgrade
cd ~/.clawdbot/skills/tts-whatsapp
git pull  # or re-download and extract
```

## Uninstall

```bash
# Remove the skill
rm -rf ~/.clawdbot/skills/tts-whatsapp

# Optionally remove voice models
rm -rf ~/.clawdbot/skills/piper-tts

# Optionally uninstall Piper
pip3 uninstall piper-tts
```

## Next Steps

- 📖 Read [README.md](README.md) for usage examples
- 🌍 Check [LANGUAGES.md](LANGUAGES.md) for all available voices
- 🎤 Test different voices and qualities
- 👥 Try sending to WhatsApp groups

## Need Help?

- 📚 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/clawdbot/clawdhub/issues)
- 💬 [Clawdbot Discussions](https://github.com/clawdbot/clawdbot/discussions)
