---
name: withings-health
description: Fetches health data from the Withings API including weight, body composition (fat, muscle, bone, water), activity, and sleep. Use this skill when the user asks about their Withings data, weight history, body metrics, daily steps, sleep quality, or any health measurement from Withings devices.
version: 1.1.0
homepage: https://developer.withings.com/
metadata: {"clawdbot":{"emoji":"⚖️","requires":{"bins":["node"],"env":["WITHINGS_CLIENT_ID","WITHINGS_CLIENT_SECRET"]}}}
---

This skill allows you to interact with the user's Withings account to retrieve comprehensive health metrics from Withings devices (smart scales, sleep analyzers, activity trackers, etc.).

## When to Use This Skill

Use this skill when the user:
- Asks about their **weight** or weight history
- Wants to see their **body composition** (fat %, muscle mass, bone mass, hydration)
- Requests their **daily activity** (steps, distance, calories burned)
- Asks about their **sleep data** (duration, quality, deep sleep, REM)
- Mentions "Withings" or any Withings device (Body+, Sleep Analyzer, ScanWatch, etc.)
- Wants to track their health progress over time

## Setup: Creating a Withings Developer App

Before using this skill, you need to create a free Withings developer application to get your API credentials.

### Step 1: Create a Withings Developer Account

1. Go to [Withings Developer Portal](https://developer.withings.com/)
2. Click **Sign Up** or **Log In** if you already have a Withings account
3. Accept the Developer Terms of Service

### Step 2: Create Your Application

1. Navigate to **My Apps** → **Create an Application**
2. Fill in the application details:
   - **Application Name**: Choose a name (e.g., "My Clawdbot Health")
   - **Description**: Brief description of your use case
   - **Contact Email**: Your email address
   - **Callback URL**: `http://localhost:8080` (required for OAuth)
   - **Application Type**: Select "Personal Use" or appropriate type
3. Submit the application

### Step 3: Get Your Credentials

Once your application is created:
1. Go to **My Apps** and select your application
2. You'll find:
   - **Client ID** → Set as `WITHINGS_CLIENT_ID` environment variable
   - **Client Secret** → Set as `WITHINGS_CLIENT_SECRET` environment variable

### Step 4: Configure Environment Variables

Add these to your Clawdbot environment:
```bash
export WITHINGS_CLIENT_ID="your_client_id_here"
export WITHINGS_CLIENT_SECRET="your_client_secret_here"
```

Or create a `.env` file in the skill directory (this file will be ignored by git):
```
WITHINGS_CLIENT_ID=your_client_id_here
WITHINGS_CLIENT_SECRET=your_client_secret_here
```

## Configuration

The skill uses a `wrapper.js` script located in `{baseDir}`.

Before any data retrieval, check if the user is authenticated. If an error mentions "No token found", guide the user through the initial authentication process.

## Available Commands

### 1. Authentication

First-time setup - generates the OAuth URL:
```bash
node {baseDir}/wrapper.js auth
```

After the user visits the URL and gets the authorization code:
```bash
node {baseDir}/wrapper.js auth YOUR_CODE_HERE
```

### 2. Get Weight

Retrieve the latest weight measurements:
```bash
node {baseDir}/wrapper.js weight
```

Returns the 5 most recent weight entries in JSON format.

**Example output:**
```json
[
  { "date": "2026-01-17T08:30:00.000Z", "weight": "75.40 kg" },
  { "date": "2026-01-16T08:15:00.000Z", "weight": "75.65 kg" }
]
```

### 3. Get Body Composition

Retrieve comprehensive body metrics (fat, muscle, bone, water, BMI):
```bash
node {baseDir}/wrapper.js body
```

Returns the 5 most recent body composition measurements.

**Example output:**
```json
[
  {
    "date": "2026-01-17T08:30:00.000Z",
    "weight": "75.40 kg",
    "fat_percent": "18.5%",
    "fat_mass": "13.95 kg",
    "muscle_mass": "35.20 kg",
    "bone_mass": "3.10 kg",
    "hydration": "55.2%"
  }
]
```

### 4. Get Activity

Retrieve daily activity data (steps, distance, calories):
```bash
node {baseDir}/wrapper.js activity
```

Optionally specify the number of days (default: 7):
```bash
node {baseDir}/wrapper.js activity 30
```

**Example output:**
```json
[
  {
    "date": "2026-01-17",
    "steps": 8542,
    "distance": "6.23 km",
    "calories": 2150,
    "active_calories": 450,
    "soft_activity": "45 min",
    "moderate_activity": "22 min",
    "intense_activity": "8 min"
  }
]
```

### 5. Get Sleep

Retrieve sleep data and quality:
```bash
node {baseDir}/wrapper.js sleep
```

Optionally specify the number of days (default: 7):
```bash
node {baseDir}/wrapper.js sleep 14
```

**Example output:**
```json
[
  {
    "date": "2026-01-17",
    "start": "23:15",
    "end": "07:30",
    "duration": "8h 15min",
    "deep_sleep": "1h 45min",
    "light_sleep": "4h 30min",
    "rem_sleep": "1h 30min",
    "awake": "30min",
    "sleep_score": 82
  }
]
```

## Error Handling

Common errors and how to resolve them:

| Error | Cause | Solution |
|-------|-------|----------|
| "No token found" | First time use, not authenticated | Run `node wrapper.js auth` and follow the OAuth flow |
| "Failed to refresh token" | Token expired and refresh failed | Re-authenticate with `node wrapper.js auth` |
| "API Error Status: 401" | Invalid or expired credentials | Check your CLIENT_ID and CLIENT_SECRET, re-authenticate |
| "API Error Status: 503" | Withings API temporarily unavailable | Wait and retry later |
| Empty data | No measurements in the requested period | User needs to sync their Withings device |

## Notes

- Tokens are automatically refreshed when they expire
- Withings API scopes used: `user.metrics`, `user.activity`
- Data availability depends on which Withings devices the user owns
- Some metrics (like body composition) require a compatible smart scale