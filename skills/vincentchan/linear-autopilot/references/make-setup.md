# Make.com Setup Guide

Step-by-step guide to connect Linear → Discord via Make.com (formerly Integromat).

> ✅ **Recommended for free tier** - Make.com offers 1,000 operations/month free vs Pipedream's 100 credits. Better value for light usage.

## Create Scenario

1. Go to [make.com](https://make.com) and sign up (free)
2. Click **Create a new scenario**

## Step 1: Add Linear Trigger

1. Click the **+** button in the center
2. Search for **Linear** → Select **Watch Issues**
3. Click **Create a connection**:
   - Go to Linear → Settings → API → Personal API keys
   - Create new key, copy it
   - Paste into Make, name the connection
4. Configure the trigger:
   - **Team**: Select your team
   - **Limit**: 10 (how many to fetch per run)
   - Click **OK**

## Step 2: Add Filter (Important!)

Click the dotted line after Linear module:

1. Click **Set up a filter**
2. Label: "Only Todo tasks"
3. Condition:
   - Field: `state` → `name`
   - Operator: **Text operators: Equal to**
   - Value: `Todo`

This ensures only tasks in "Todo" status trigger the workflow.

## Step 3: Add Discord Webhook

1. Click **+** after the filter
2. Search for **Discord** → Select **Send a Message to a Channel via Webhook**
3. Create Discord webhook:
   - In Discord: Go to your #linear-tasks channel
   - Edit Channel → Integrations → Webhooks → **New Webhook**
   - Name it "Linear Tasks" or similar
   - Copy the webhook URL
4. Back in Make:
   - **Webhook URL**: Paste the Discord webhook URL
   - **Content**:
   ```
   <@YOUR_BOT_ID>
   📋 New task: {{1.title}}
     Status: {{1.state.name}}
     ID: {{1.identifier}}
   ```
   Replace `YOUR_BOT_ID` with your Clawdbot Discord bot's user ID.

## Step 4: Test

1. Click **Run once** (bottom left)
2. Go to Linear, create a test task with status "Todo"
3. Check Discord for the message
4. Verify Clawdbot responds

## Step 5: Activate

1. Toggle the scenario **ON** (bottom left switch)
2. Set schedule: **Immediately** for real-time, or choose interval
3. Click **Save**

## Flow Diagram

```
Linear (new/updated issue)
    ↓
Filter (state.name = "Todo")
    ↓
Discord Webhook → #linear-tasks
    ↓
Clawdbot processes task
```

## Free Tier Limits

| Feature | Make.com Free |
|---------|---------------|
| Operations | 1,000/month |
| Scenarios | 2 active |
| Interval | 15 minutes minimum |
| Data transfer | 100MB |

For typical task automation (a few tasks per day), 1,000 ops/month is plenty.

## Troubleshooting

### Tasks not triggering
- Check scenario is turned ON (green toggle)
- Verify Linear connection is valid
- Check filter condition (state.name = "Todo")
- Run manually with **Run once** to debug

### Discord message not appearing
- Verify webhook URL is correct
- Test webhook directly with curl:
  ```bash
  curl -X POST -H "Content-Type: application/json" \
    -d '{"content":"Test message"}' \
    YOUR_WEBHOOK_URL
  ```

### Filter not working
- Check spelling: "Todo" is case-sensitive
- Use **state** → **name** (not state.id)

## Comparison: Make vs Pipedream

| Feature | Make.com | Pipedream |
|---------|----------|-----------|
| Free operations | 1,000/month | 100 total (unclear reset) |
| Minimum interval | 15 min (free) | Instant |
| UI complexity | Moderate | Simpler |
| Linear integration | Native | Native |

**Verdict**: Make.com is better value for free tier. Pipedream is simpler if you're paying.
