# Unraid API Quick Reference

Quick reference for the most common Unraid GraphQL API queries.

## Setup

```bash
# Set environment variables
export UNRAID_URL="https://your-unraid-server/graphql"
export UNRAID_API_KEY="your-api-key-here"

# Or use the helper script directly
./scripts/unraid-query.sh -u "$UNRAID_URL" -k "$API_KEY" -q "{ online }"
```

## Common Queries

### System Status
```graphql
{ 
  online 
  metrics { 
    cpu { percentTotal } 
    memory { total used free percentTotal } 
  } 
}
```

### Array Status
```graphql
{ 
  array { 
    state 
    parityCheckStatus { status progress errors } 
  } 
}
```

### Disk List with Temperatures
```graphql
{ 
  array { 
    disks { 
      name 
      device 
      temp 
      status 
      fsSize 
      fsFree 
      isSpinning 
    } 
  } 
}
```

### All Physical Disks (including USB/SSDs)
```graphql
{ 
  disks { 
    id 
    name 
  } 
}
```

### Network Shares
```graphql
{ 
  shares { 
    name 
    comment 
  } 
}
```

### Docker Containers
```graphql
{ 
  docker { 
    containers { 
      id 
      names 
      image 
      state 
      status 
    } 
  } 
}
```

### Virtual Machines
```graphql
{ 
  vms { 
    id 
    name 
    state 
    cpus 
    memory 
  } 
}
```

### List Log Files
```graphql
{ 
  logFiles { 
    name 
    size 
    modifiedAt 
  } 
}
```

### Read Log Content
```graphql
{ 
  logFile(path: "syslog", lines: 20) { 
    content 
    totalLines 
  } 
}
```

### System Info
```graphql
{ 
  info { 
    time 
    cpu { model cores threads } 
    os { distro release } 
    system { manufacturer model } 
  } 
}
```

### UPS Devices
```graphql
{ 
  upsDevices { 
    id 
    name 
    status 
    charge 
    load 
  } 
}
```

### Notifications

**Counts:**
```graphql
{ 
  notifications { 
    overview { 
      unread { info warning alert total } 
      archive { info warning alert total } 
    } 
  } 
}
```

**List Unread:**
```graphql
{ 
  notifications { 
    list(filter: { type: UNREAD, offset: 0, limit: 10 }) { 
      id 
      subject 
      description 
      timestamp 
    } 
  } 
}
```

**List Archived:**
```graphql
{ 
  notifications { 
    list(filter: { type: ARCHIVE, offset: 0, limit: 10 }) { 
      id 
      subject 
      description 
      timestamp 
    } 
  } 
}
```

## Field Name Notes

- Use `metrics` for real-time usage (CPU/memory percentages)
- Use `info` for hardware specs (cores, model, etc.)
- Temperature field is `temp` (not `temperature`)
- Status field is `state` for array (not `status`)
- Sizes are in kilobytes
- Temperatures are in Celsius

## Response Structure

All responses follow this pattern:
```json
{
  "data": {
    "queryName": { ... }
  }
}
```

Errors appear in:
```json
{
  "errors": [
    { "message": "..." }
  ]
}
```
