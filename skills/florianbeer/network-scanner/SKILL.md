---
name: network-scanner
description: Scan networks to discover devices, gather MAC addresses, vendors, and hostnames. Supports known networks (from config) or custom CIDRs.
homepage: https://github.com/clawdbot/skills
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      bins: ["nmap", "dig"]
    tags:
      - network
      - discovery
      - devices
      - nmap
---

# Network Scanner

Discover and identify devices on local or remote networks using nmap. Gathers IP addresses, hostnames (via reverse DNS), MAC addresses, and vendor identification.

## Requirements

- `nmap` - Network scanning (`apt install nmap` or `brew install nmap`)
- `dig` - DNS lookups (usually pre-installed)
- `sudo` access recommended for MAC address discovery

## Quick Start

```bash
# Auto-detect and scan current network
python3 scripts/scan.py

# Scan a specific CIDR
python3 scripts/scan.py 192.168.1.0/24

# Scan with custom DNS server for reverse lookups
python3 scripts/scan.py 192.168.1.0/24 --dns 192.168.1.1

# Output as JSON
python3 scripts/scan.py --json
```

## Configuration

Configure named networks in `~/.config/network-scanner/networks.json`:

```json
{
  "networks": {
    "home": {
      "cidr": "192.168.1.0/24",
      "dns": "192.168.1.1",
      "description": "Home Network"
    },
    "office": {
      "cidr": "10.0.0.0/24",
      "dns": "10.0.0.1",
      "description": "Office Network"
    }
  }
}
```

Then scan by name:

```bash
python3 scripts/scan.py home
python3 scripts/scan.py office --json
```

### Commands

```bash
# Create example config
python3 scripts/scan.py --init-config

# List configured networks
python3 scripts/scan.py --list

# Scan without sudo (may miss MAC addresses)
python3 scripts/scan.py home --no-sudo
```

## Output Formats

**Markdown (default):**
```
### Home Network
*Last scan: 2026-01-28 00:10*

| IP | Name | MAC | Vendor |
|----|------|-----|--------|
| 192.168.1.1 | router.local | AA:BB:CC:DD:EE:FF | Ubiquiti |
| 192.168.1.100 | nas.local | 11:22:33:44:55:66 | Synology |

*2 devices found*
```

**JSON (--json):**
```json
{
  "network": "Home Network",
  "cidr": "192.168.1.0/24",
  "devices": [
    {
      "ip": "192.168.1.1",
      "hostname": "router.local",
      "mac": "AA:BB:CC:DD:EE:FF",
      "vendor": "Ubiquiti"
    }
  ],
  "scanned_at": "2026-01-28T00:10:00",
  "device_count": 2
}
```

## Use Cases

- **Device inventory**: Keep track of all devices on your network
- **Security audits**: Identify unknown devices
- **Documentation**: Generate network maps for documentation
- **Automation**: Integrate with home automation to detect device presence

## Tips

- Use `sudo` for accurate MAC address detection (nmap needs privileges for ARP)
- Configure your local DNS server for better hostname resolution
- Add to cron or heartbeat for daily inventory updates
- Extend `MAC_VENDORS` in the script for better device identification
