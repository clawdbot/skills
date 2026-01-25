---
name: bambu-local
description: Control Bambu Lab 3D printers locally via MQTT (no cloud). Supports A1, A1 Mini, P1P, P1S, X1C.
homepage: https://github.com/Doridian/OpenBambuAPI
metadata: {"clawdbot":{"emoji":"🖨️","requires":{"bins":["python3"]}}}
---
# Bambu Local - 3D Printer Control

Control Bambu Lab printers locally via MQTT without cloud dependency.

## Setup

1. Create virtual environment:
```bash
python3 -m venv ~/bambu-env
source ~/bambu-env/bin/activate
pip install paho-mqtt
```

2. Create `config.json` in skill folder:
```json
{
  "printer_ip": "192.168.x.x",
  "access_code": "xxxxxxxx",
  "serial": "xxxxxxxxxxxx",
  "printer_name": "MyPrinter"
}
```

Get these from your printer: Settings → LAN Only Mode (access code) and Settings → Device (serial).

## Commands

### Status
```bash
run ~/clawd/skills/bambu-local/bambu status
```

### Light
```bash
run ~/clawd/skills/bambu-local/bambu light on
run ~/clawd/skills/bambu-local/bambu light off
```

### Print Control
```bash
run ~/clawd/skills/bambu-local/bambu print pause
run ~/clawd/skills/bambu-local/bambu print resume
run ~/clawd/skills/bambu-local/bambu print stop
```

### Speed (1=Silent, 2=Standard, 3=Sport, 4=Ludicrous)
```bash
run ~/clawd/skills/bambu-local/bambu speed 2
```

### Temperature
```bash
run ~/clawd/skills/bambu-local/bambu temp --bed 60
run ~/clawd/skills/bambu-local/bambu temp --nozzle 200
```

### G-code
```bash
run ~/clawd/skills/bambu-local/bambu gcode "G28"
```

## Supported Printers
- Bambu Lab A1 / A1 Mini
- Bambu Lab P1P / P1S  
- Bambu Lab X1 / X1C
