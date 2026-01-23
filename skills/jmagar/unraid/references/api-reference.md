# Unraid API - Complete Reference Guide

**Tested on:** Unraid 7.2 x86_64  
**Date:** 2026-01-21  
**API Type:** GraphQL  
**Base URL:** `https://YOUR-UNRAID-SERVER/graphql`  

---

## 📊 Summary

Out of 46 total GraphQL query endpoints:
- **✅ 27 fully working read-only endpoints**
- **⚠️ 1 works but returns empty** (`plugins`)
- **❌ 3 return null** (`flash`, `parityHistory`, `services`)
- **❓ 15 untested** (mostly write/mutation operations)

---

## Authentication

All requests require the `x-api-key` header:

```bash
-H "x-api-key: YOUR_API_KEY_HERE"
```

### How to Generate API Key:
1. Log in to Unraid WebGUI
2. Settings → Management Access → API Keys
3. Create API Key with **Viewer** role (read-only)
4. Copy the generated key

---

## 🎯 All 27 Working Read-Only Endpoints

### 1. System Info & Metrics

#### **info** - Hardware Specifications
Get CPU, OS, motherboard, and hardware details.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ info { time cpu { model cores threads } os { platform distro release arch } system { manufacturer model version uuid } } }"
  }' | jq '.'
```

**Response:**
```json
{
  "data": {
    "info": {
      "time": "2026-01-21T12:57:22.539Z",
      "cpu": {
        "model": "183",
        "cores": 16,
        "threads": 24
      },
      "os": {
        "platform": "linux",
        "distro": "Unraid OS",
        "release": "7.2 x86_64",
        "arch": "x64"
      },
      "system": {
        "manufacturer": "Micro-Star International Co., Ltd.",
        "model": "MS-7E07",
        "version": "1.0",
        "uuid": "fec05753-077c-8e18-a089-047c1644678a"
      }
    }
  }
}
```

---

#### **metrics** - Real-Time Usage Stats
Get current CPU and memory usage percentages.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ metrics { cpu { percentTotal } memory { total used free percentTotal swapTotal swapUsed swapFree } } }"
  }' | jq '.'
```

**Response:**
```json
{
  "data": {
    "metrics": {
      "cpu": {
        "percentTotal": 20.99
      },
      "memory": {
        "total": 134773903360,
        "used": 129472622592,
        "free": 5301280768,
        "percentTotal": 59.97,
        "swapTotal": 0,
        "swapUsed": 0,
        "swapFree": 0
      }
    }
  }
}
```

**Note:** Memory values are in bytes.

---

#### **online** - Server Online Status
Simple boolean check if server is online.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{ "query": "{ online }" }' | jq '.'
```

**Response:**
```json
{
  "data": {
    "online": true
  }
}
```

---

#### **isInitialSetup** - Initial Setup Status
Check if server has completed initial setup.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{ "query": "{ isInitialSetup }" }' | jq '.'
```

**Response:**
```json
{
  "data": {
    "isInitialSetup": false
  }
}
```

---

### 2. Storage & Disks

#### **array** - Array Status & Disks
Get array state, disk details, temperatures, and capacity.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ array { state disks { id name device size status temp fsSize fsFree fsUsed fsType rotational isSpinning } parityCheckStatus { status progress errors speed } } }"
  }' | jq '.'
```

**Response (sample):**
```json
{
  "data": {
    "array": {
      "state": "STARTED",
      "disks": [
        {
          "id": "3cb1026338736ed07b8afec2c484e429710b0f6550dc65d0c5c410ea9d0fa6b2:WDC_WD120EDBZ-11B1HA0_5QGWN5DF",
          "name": "disk1",
          "device": "sdb",
          "size": 11718885324,
          "status": "DISK_OK",
          "temp": 38,
          "fsSize": 11998001574,
          "fsFree": 1692508541,
          "fsUsed": 10305493033,
          "fsType": "xfs",
          "rotational": true,
          "isSpinning": true
        }
      ],
      "parityCheckStatus": {
        "status": "NEVER_RUN",
        "progress": 0,
        "errors": null,
        "speed": "0"
      }
    }
  }
}
```

**Note:** Sizes are in kilobytes. Temperature in Celsius.

---

#### **disks** - All Physical Disks
Get ALL disks including array disks, cache SSDs, and boot USB.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ disks { id name } }"
  }' | jq '.'
```

**Response (sample):**
```json
{
  "data": {
    "disks": [
      {
        "id": "3cb1026338736ed07b8afec2c484e429710b0f6550dc65d0c5c410ea9d0fa6b2:04009732070823130633",
        "name": "Cruzer Glide"
      },
      {
        "id": "3cb1026338736ed07b8afec2c484e429710b0f6550dc65d0c5c410ea9d0fa6b2:5QGWN5DF",
        "name": "WDC WD120EDBZ-11B1HA0"
      },
      {
        "id": "3cb1026338736ed07b8afec2c484e429710b0f6550dc65d0c5c410ea9d0fa6b2:S6S2NS0TB18572X",
        "name": "Samsung SSD 970 EVO Plus 2TB"
      }
    ]
  }
}
```

**Returns:** Array disks + Cache SSDs + Boot USB (17 disks in tested system).

---

#### **shares** - Network Shares
List all user shares with comments.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ shares { id name comment } }"
  }' | jq '.'
```

**Response:**
```json
{
  "data": {
    "shares": [
      {
        "id": "3cb1026338736ed07b8afec2c484e429710b0f6550dc65d0c5c410ea9d0fa6b2:appdata",
        "name": "appdata",
        "comment": "application data"
      },
      {
        "id": "3cb1026338736ed07b8afec2c484e429710b0f6550dc65d0c5c410ea9d0fa6b2:backups",
        "name": "backups",
        "comment": "primary homelab backup target"
      }
    ]
  }
}
```

---

### 3. Virtualization

#### **docker** - Docker Containers
List all Docker containers with status and metadata.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ docker { containers { id names image state status created autoStart } } }"
  }' | jq '.'
```

**Response (when no containers):**
```json
{
  "data": {
    "docker": {
      "containers": []
    }
  }
}
```

**Note:** Container logs are NOT accessible via this API. Use `docker logs` via SSH.

---

#### **vms** - Virtual Machines
List all VMs with status and resource allocation.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ vms { id name state cpus memory autostart } }"
  }' | jq '.'
```

**Response (when no VMs):**
```json
{
  "data": {
    "vms": []
  }
}
```

---

### 4. Logs & Monitoring

#### **logFiles** - List All Log Files
Get list of all available system log files.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ logFiles { name size modifiedAt } }"
  }' | jq '.'
```

**Response (sample, 32 logs found):**
```json
{
  "data": {
    "logFiles": [
      {
        "name": "syslog",
        "size": 142567,
        "modifiedAt": "2026-01-21T13:00:00.000Z"
      },
      {
        "name": "docker.log",
        "size": 66321,
        "modifiedAt": "2026-01-05T19:14:53.934Z"
      },
      {
        "name": "dmesg",
        "size": 93128,
        "modifiedAt": "2025-12-19T11:09:30.200Z"
      }
    ]
  }
}
```

---

#### **logFile** - Read Log Content
Read the actual contents of a log file.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "query { logFile(path: \"syslog\", lines: 10) { path totalLines startLine content } }"
  }' | jq '.'
```

**Response:**
```json
{
  "data": {
    "logFile": {
      "path": "/var/log/syslog",
      "totalLines": 1395,
      "startLine": 1386,
      "content": "Jan 21 07:49:49 tootie sshd-session[2992319]: Accepted keyboard-interactive/pam for root from 100.80.181.18 port 49724 ssh2\n..."
    }
  }
}
```

**Parameters:**
- `path` - Log file name (required)
- `lines` - Number of lines to return (optional, defaults to last 100)
- `startLine` - Line number to start from (optional)

**Available logs include:**
- `syslog` - System log
- `docker.log` - Docker daemon log
- `dmesg` - Kernel messages
- `wtmp` - Login records
- And 28 more...

---

#### **notifications** - System Alerts
Get system notifications and alerts.

**Get notification counts:**
```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ notifications { overview { unread { info warning alert total } archive { info warning alert total } } } }"
  }' | jq '.'
```

**Response:**
```json
{
  "data": {
    "notifications": {
      "overview": {
        "unread": {
          "info": 66,
          "warning": 0,
          "alert": 0,
          "total": 66
        },
        "archive": {
          "info": 581,
          "warning": 4,
          "alert": 1,
          "total": 586
        }
      }
    }
  }
}
```

**List unread notifications:**
```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ notifications { list(filter: { type: UNREAD, offset: 0, limit: 10 }) { id subject description timestamp } } }"
  }' | jq '.'
```

**Response (sample):**
```json
{
  "data": {
    "notifications": {
      "list": [
        {
          "id": "...",
          "subject": "Backup Notification",
          "description": "ZFS replication was successful...",
          "timestamp": "2026-01-21T09:10:40.000Z"
        }
      ]
    }
  }
}
```

**Parameters for list query:**
- `type` - `UNREAD` or `ARCHIVE` (required)
- `offset` - Starting index (required, use 0 for first page)
- `limit` - Number of results (required, max typically 100)
- `importance` - Filter by `INFO`, `WARNING`, or `ALERT` (optional)

---

### 5. UPS & Power

#### **upsDevices** - UPS Status
Get UPS battery backup status (if configured).

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ upsDevices { id name status charge load runtime } }"
  }' | jq '.'
```

**Response (when no UPS):**
```json
{
  "data": {
    "upsDevices": []
  }
}
```

---

### 6. User & Authentication

#### **me** - Current User Info
Get information about the current authenticated user.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ me { id } }"
  }' | jq '.'
```

---

#### **owner** - Server Owner
Get server owner information.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ owner { username url avatar } }"
  }' | jq '.'
```

**Response:**
```json
{
  "data": {
    "owner": {
      "username": "root",
      "url": "",
      "avatar": ""
    }
  }
}
```

---

#### **isSSOEnabled** - SSO Status
Check if Single Sign-On is enabled.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{ "query": "{ isSSOEnabled }" }' | jq '.'
```

**Response:**
```json
{
  "data": {
    "isSSOEnabled": true
  }
}
```

---

#### **oidcProviders** - OIDC Providers
List configured OpenID Connect providers.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ oidcProviders { id } }"
  }' | jq '.'
```

---

### 7. API Keys & Access

#### **apiKeys** - List API Keys
Get list of all API keys (requires appropriate permissions).

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ apiKeys { id name createdAt } }"
  }' | jq '.'
```

**Response (sample, 4 keys found):**
```json
{
  "data": {
    "apiKeys": [
      {
        "id": "key1",
        "name": "monitoring",
        "createdAt": "2026-01-01T00:00:00.000Z"
      }
    ]
  }
}
```

---

### 8. Configuration & Settings

#### **config** - System Configuration
Get system configuration details.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ config { id } }"
  }' | jq '.'
```

---

#### **settings** - System Settings
Get system settings.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ settings { id } }"
  }' | jq '.'
```

---

#### **vars** - System Variables
Get system variables.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ vars { id } }"
  }' | jq '.'
```

---

### 9. Customization & Theming

#### **customization** - UI Customization
Get UI theme and customization settings.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ customization { theme { name headerBackgroundColor headerPrimaryTextColor showBannerImage showBannerGradient } } }"
  }' | jq '.'
```

**Response:**
```json
{
  "data": {
    "customization": {
      "theme": {
        "name": "white",
        "headerBackgroundColor": "#2e3440",
        "headerPrimaryTextColor": "#FFF",
        "showBannerImage": false,
        "showBannerGradient": false
      }
    }
  }
}
```

---

#### **publicTheme** - Public Theme Settings
Get public-facing theme settings.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ publicTheme { name showBannerImage showBannerGradient headerBackgroundColor headerPrimaryTextColor headerSecondaryTextColor } }"
  }' | jq '.'
```

**Response:**
```json
{
  "data": {
    "publicTheme": {
      "name": "white",
      "showBannerImage": false,
      "showBannerGradient": false,
      "headerBackgroundColor": "#2e3440",
      "headerPrimaryTextColor": "#FFF",
      "headerSecondaryTextColor": "#fff"
    }
  }
}
```

---

#### **publicPartnerInfo** - Partner/OEM Branding
Get partner or OEM branding information.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ publicPartnerInfo { partnerName partnerUrl partnerLogoUrl hasPartnerLogo } }"
  }' | jq '.'
```

**Response:**
```json
{
  "data": {
    "publicPartnerInfo": {
      "partnerName": null,
      "partnerUrl": null,
      "partnerLogoUrl": "/webGui/images/UN-logotype-gradient.svg",
      "hasPartnerLogo": false
    }
  }
}
```

---

### 10. Server Management

#### **registration** - License Info
Get Unraid license/registration information.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ registration { id } }"
  }' | jq '.'
```

---

#### **server** - Server Metadata
Get server metadata.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ server { id } }"
  }' | jq '.'
```

---

#### **servers** - Multi-Server Management
Get list of servers (for multi-server setups).

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ servers { id } }"
  }' | jq '.'
```

---

### 11. Plugins

#### **plugins** - Installed Plugins
List installed plugins.

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ plugins { name version author description } }"
  }' | jq '.'
```

**Response (when no plugins):**
```json
{
  "data": {
    "plugins": []
  }
}
```

---

## 🎯 Complete Dashboard Query

Get everything useful in a single query:

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "query Dashboard { 
      info { 
        time 
        cpu { model cores threads } 
        os { distro release } 
        system { manufacturer model }
      } 
      metrics { 
        cpu { percentTotal } 
        memory { total used free percentTotal } 
      } 
      array { 
        state 
        disks { name device temp status fsSize fsFree fsUsed isSpinning }
        parityCheckStatus { status progress errors }
      }
      shares { name comment }
      online
      isSSOEnabled
    }"
  }' | jq '.'
```

---

## ❌ Endpoints That Return Null

These queries exist but return `null` in Unraid 7.2:

1. **`flash`** - Boot USB drive info (returns `null`)
2. **`parityHistory`** - Historical parity checks (returns `null` - use `array.parityCheckStatus` instead)
3. **`services`** - System services (returns `null`)

---

## 🔍 Schema Discovery

### Discover Available Fields for a Type

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ __type(name: \"Info\") { fields { name type { name } } } }"
  }' | jq -r '.data.__type.fields[] | "\(.name): \(.type.name)"'
```

### List All Available Queries

```bash
curl -s -X POST "https://YOUR-UNRAID/graphql" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "{ __type(name: \"Query\") { fields { name } } }"
  }' | jq -r '.data.__type.fields[].name' | sort
```

---

## 📝 Field Name Reference

Common differences from online documentation:

| Online Docs | Actual Unraid 7.2 Field |
|------------|------------------------|
| `uptime` | `time` |
| `cpu.usage` | `metrics.cpu.percentTotal` |
| `memory.usage` | `metrics.memory.percentTotal` |
| `array.status` | `array.state` |
| `disk.temperature` | `disk.temp` |
| `percentUsed` | `percentTotal` |

---

## ⚡ Best Practices

1. **Use `metrics` for real-time stats** - CPU/memory usage is in `metrics`, not `info`
2. **Use `array.disks` for array disks** - The top-level `disks` query includes ALL disks (USB, SSDs, etc.)
3. **Always check errors** - GraphQL returns errors in `errors` array
4. **Use introspection** - Field names can vary between versions
5. **Sizes are in kilobytes** - Disk sizes and capacities are in KB, not bytes
6. **Temperature is Celsius** - All temperature values are in Celsius
7. **Handle empty arrays** - Many queries return `[]` when no data exists
8. **Use viewer role** - Create API keys with "Viewer" role for read-only access

---

## 🚫 Known Limitations

1. **No Docker container logs** - Container output logs are NOT accessible via API
2. **No real-time streaming** - All queries are request/response, no WebSocket subscriptions
3. **Some queries require higher permissions** - Read-only "Viewer" role may not access all queries
4. **No mutation examples included** - This guide covers read-only queries only

---

## 📚 Additional Resources

- **Unraid Docs:** https://docs.unraid.net/
- **GraphQL Spec:** https://graphql.org/
- **GraphQL Introspection:** Use `__schema` and `__type` queries to explore the API

---

**Last Updated:** 2026-01-21  
**API Version:** Unraid 7.2 GraphQL API  
**Total Working Endpoints:** 27 of 46
