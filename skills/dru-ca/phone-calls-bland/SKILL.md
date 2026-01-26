---
name: phone-calls
description: Make AI-powered phone calls via Bland AI - book restaurants, make appointments, inquire about services. The AI calls on your behalf and reports back with transcripts.
metadata: {"clawdbot":{"emoji":"📞","requires":{"env":["BLAND_API_KEY"]}}}
---

# Phone Calls Skill

Make AI-powered phone calls on behalf of the user — book restaurants, make appointments, inquire about services, etc.

## Provider: Bland AI

**Why Bland AI?**
- Simplest API of all options (Vapi, Retell are more complex)
- Just need `phone_number` + `task` to make a call
- Low latency, natural-sounding voices
- Pay-per-minute, no platform fees
- Self-hosted (data stays secure)

## Setup Required

### 1. Create Bland AI Account
1. Go to https://app.bland.ai
2. Sign up with email
3. Add payment method (or use free trial credits)

### 2. Get API Key
1. Go to https://app.bland.ai/dashboard
2. Click your profile → API Keys
3. Copy your API key

### 3. Configure Clawdbot
Add to your environment or `.env`:
```bash
BLAND_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

Or store in `~/.clawd/secrets.json`:
```json
{
  "bland_api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
}
```

## Usage

### Basic Call
```bash
./phone-call.sh "+447123456789" "Call the restaurant and book a table for 2 at 7pm tonight under the name John"
```

### With Custom Voice
```bash
./phone-call.sh "+447123456789" "Ask about their opening hours" --voice maya
```

### Check Call Status
```bash
./check-call.sh <call_id>
```

## How It Works

1. You provide a phone number and a task/objective
2. Bland AI calls the number with an AI agent
3. The AI follows your instructions naturally
4. You get a transcript and summary after the call

## Example Tasks

**Restaurant Booking:**
```
Call this restaurant and book a table for 4 people on Saturday at 8pm. 
The booking should be under the name "Smith". If they ask for a phone 
number, give them +447123456789.
```

**Appointment Inquiry:**
```
Call this dental office and ask what appointments are available next 
week for a routine checkup. Get at least 3 options if possible.
```

**Service Inquiry:**
```
Call this plumber and ask if they can come out tomorrow to fix a 
leaking tap. Get a quote for the callout fee.
```

## Pricing (Bland AI)

- **Outbound calls:** ~$0.09/minute (US) 
- **Varies by country** — check https://app.bland.ai for current rates
- First calls may have free credits

## Voice Options

Built-in voices:
- `josh` - Male, professional
- `maya` - Female, friendly (default)
- `florian` - Male, European accent
- `derek` - Male, casual
- `june` - Female, professional
- `nat` - Male, natural
- `paige` - Female, upbeat

## Advanced Features

### Voicemail Handling
The AI can detect voicemails and either hang up, leave a message, or ignore.

### Call Recording
Set `record: true` to get a recording URL after the call.

### Webhooks
Get notified when calls complete by setting a webhook URL.

### Conversation Pathways
For complex flows (IVR menus, multi-step processes), create pathways in the Bland dashboard.

## Limitations

- Cannot call emergency services (999, 911, etc.)
- Some numbers may be blocked (DNC lists)
- Rate limited: 1 call per 10 seconds to the same number
- Max call duration: 30 minutes default (configurable)

## Troubleshooting

**"Invalid phone number"**
- Include country code: `+44` for UK, `+1` for US
- Remove spaces and parentheses

**"Insufficient balance"**
- Add credits at https://app.bland.ai/dashboard/billing

**"Rate limit exceeded"**
- Wait a few seconds between calls to the same number

## Files

- `phone-call.sh` — Make a phone call
- `check-call.sh` — Check call status/transcript
- `bland.sh` — Low-level API wrapper
