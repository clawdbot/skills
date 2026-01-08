# Oura Ring CLI Skill

## Description
This tool allows retrieving health and biometric data from the Oura Ring API (V2) via a command-line interface. Use this to answer questions about the user's sleep, activity, readiness, and physiological stats.

Repository: [https://github.com/ruhrpotter/oura-cli](https://github.com/ruhrpotter/oura-cli)

## Installation

### 1. Build the CLI
```bash
cd ~
git clone https://github.com/ruhrpotter/oura-cli.git
cd oura-cli
go build -o oura ./cmd/oura
```

### 2. Create Oura OAuth App
1. Go to [Oura Developer Portal](https://cloud.ouraring.com/oauth/developer)
2. Create a new application
3. Set Redirect URI to: `http://localhost:8080/callback`
4. Note down your **Client ID** and **Client Secret**

### 3. Authenticate
```bash
export OURA_CLIENT_ID="your_client_id"
export OURA_CLIENT_SECRET="your_client_secret"
./oura auth login
```

A browser will open for OAuth authorization. Tokens are stored in `~/.config/oura-cli/config.json`.

## Prerequisite
The CLI must be authenticated. If a command fails with an auth error, notify the user to run `./oura auth login`.

## Syntax
`./oura get <category> [flags]`

## Categories
- `personal`: User profile (age, weight, height, email).
- `sleep`: Daily sleep scores and efficiency.
- `activity`: Daily activity scores, steps, and movement.
- `readiness`: Daily readiness scores indicating recovery.
- `heartrate`: Time-series heart rate data.
- `workout`: Detailed workout sessions.
- `spo2`: Blood oxygen saturation levels.
- `sleep-details`: Detailed sleep sessions including hypnograms.
- `sessions`: Activity sessions (e.g. naps, rest).
- `sleep-times`: Optimal bedtime guidance.
- `stress`: Daily stress levels.
- `resilience`: Daily resilience scores and recovery.
- `cv-age`: Cardiovascular age estimates.
- `vo2-max`: VO2 Max measurements.
- `ring-config`: Ring hardware configuration (color, size, etc.).
- `rest-mode`: Rest mode periods.
- `tags`: Enhanced tags (notes, lifestyle choices).

## Arguments
- `--start <YYYY-MM-DD>`: REQUIRED for most time-series data. The start date of the range.
- `--end <YYYY-MM-DD>`: OPTIONAL. The end date of the range. If omitted, it may default to the start date or return a single day depending on context.

## Agent Instructions
1.  **Date Resolution**: You **MUST** resolve all relative date terms (e.g., "today", "yesterday", "last week", "this month") into absolute `YYYY-MM-DD` string format based on the current operational date.
2.  **Date ranges**:
    - For "today": Set `--start` to today's date.
    - For "yesterday": Set `--start` to yesterday's date.
    - For "last 7 days": Set `--start` to 7 days ago and `--end` to today.
3.  **Path**: Assume the binary is `./oura` in the current working directory unless the user specifies otherwise.
4.  **Output**: The CLI returns JSON. Parse the JSON `data` array to formulate a natural language response.

## Examples

**User Request**: "How was my sleep last night?"
**Context**: Today is 2024-03-15. "Last night" usually implies the sleep session ending on the morning of today, or the previous day's data depending on how Oura dates it (Oura dates sleep by the morning it ends).
**Reasoning**: Sleep for the night of the 14th to 15th is logged as `2024-03-15`.
**Command**:
```bash
./oura get sleep --start 2024-03-15
```

**User Request**: "What is my readiness score today?"
**Context**: Today is 2024-03-15.
**Command**:
```bash
./oura get readiness --start 2024-03-15
```

**User Request**: "Show my heart rate for the first week of January 2024."
**Command**:
```bash
./oura get heartrate --start 2024-01-01 --end 2024-01-07
```

**User Request**: "Who am I?"
**Command**:
```bash
./oura get personal
```
