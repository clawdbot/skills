# Auto-Hunt Setup

Run hunters continuously with automatic respawning.

## 1. Create Cron Job

Add a cron job that checks hunter count every 10 minutes:

```javascript
cron({
  action: "add",
  job: {
    text: "🔄 HUNTER CHECK: Use sessions_list to count active crypto-hunter subagents. If fewer than 3 running, IMMEDIATELY spawn 3 new hunters using sessions_spawn with different VC portfolio sources. Reply NO_REPLY after checking/spawning.",
    schedule: "*/10 * * * *",
    enabled: true
  }
})
```

## 2. Update HEARTBEAT.md

Add to your workspace HEARTBEAT.md:

```markdown
## Crypto Hunter Auto-Respawn
Check if crypto hunters are running:
1. Use sessions_list to see active subagents
2. If fewer than 3 hunters are active (labels containing "crypto-hunter"), spawn new ones
3. Use fresh VC portfolio sources each time
4. Keep the search running until told to stop
```

## 3. Initialize CSVs

Create the CSV files if they don't exist:

**crypto-master.csv:**
```
Name,Chain,Category,Website,X Link,Funding,Contacts
```

**crypto-no-contacts.csv:**
```
Name,Chain,Category,Website,X Link,Funding,Notes
```

## Stopping Auto-Hunt

To stop:
1. Remove or disable the cron job
2. Remove the hunter section from HEARTBEAT.md
3. Any running hunters will complete but won't respawn

## Monitoring

Check hunter status:
```
sessions_list({ activeMinutes: 10, kinds: ["sub-agent"] })
```

Check CSV counts:
```
wc -l crypto-master.csv crypto-no-contacts.csv
```
