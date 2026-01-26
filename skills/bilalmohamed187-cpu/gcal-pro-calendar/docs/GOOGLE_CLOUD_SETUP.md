# Google Cloud Project Setup Guide

## Overview
This guide walks you through creating a Google Cloud project, enabling the Calendar API, and configuring OAuth 2.0 to get your `client_secret.json` file.

**Time required:** ~15 minutes  
**Prerequisites:** Google account

---

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)

2. Click the project dropdown (top-left, next to "Google Cloud")

3. Click **"New Project"**

4. Enter project details:
   - **Project name:** `gcal-pro`
   - **Organization:** Leave as default (or "No organization")
   
5. Click **"Create"**

6. Wait ~30 seconds for project creation

7. Make sure `gcal-pro` is selected in the project dropdown

---

## Step 2: Enable Google Calendar API

1. In the left sidebar, go to **APIs & Services → Library**
   - Or direct link: https://console.cloud.google.com/apis/library

2. Search for **"Google Calendar API"**

3. Click on **Google Calendar API**

4. Click **"Enable"**

5. Wait for it to enable (~10 seconds)

---

## Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services → OAuth consent screen**
   - Or direct link: https://console.cloud.google.com/apis/credentials/consent

2. Select **User Type:**
   - Choose **"External"** (unless you have Google Workspace)
   - Click **"Create"**

3. Fill in **App Information:**
   ```
   App name: gcal-pro
   User support email: [your email]
   ```

4. Skip the **App logo** (optional, add later)

5. Fill in **App domain** (all optional for now, skip)

6. Fill in **Developer contact information:**
   ```
   Email addresses: [your email]
   ```

7. Click **"Save and Continue"**

---

## Step 4: Configure Scopes

1. Click **"Add or Remove Scopes"**

2. In the filter, search for and select these scopes:
   ```
   ✓ .../auth/calendar.readonly     (Free tier - read only)
   ✓ .../auth/calendar.events       (Pro tier - read/write events)
   ```

3. Click **"Update"**

4. Click **"Save and Continue"**

---

## Step 5: Add Test Users

1. Click **"Add Users"**

2. Enter your Gmail address (the one you'll test with)

3. Click **"Add"**

4. Click **"Save and Continue"**

5. Review summary and click **"Back to Dashboard"**

---

## Step 6: Create OAuth 2.0 Credentials

1. Go to **APIs & Services → Credentials**
   - Or direct link: https://console.cloud.google.com/apis/credentials

2. Click **"+ Create Credentials"** (top of page)

3. Select **"OAuth client ID"**

4. Configure the OAuth client:
   ```
   Application type: Desktop app
   Name: gcal-pro-desktop
   ```

5. Click **"Create"**

6. A popup appears with your credentials. Click **"Download JSON"**

7. **IMPORTANT:** Save the file as `client_secret.json`

---

## Step 7: Store Credentials Securely

Move the downloaded file to the gcal-pro config directory:

**Windows (PowerShell):**
```powershell
# Create config directory
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\gcal-pro"

# Move the downloaded file (adjust source path as needed)
Move-Item "$env:USERPROFILE\Downloads\client_secret*.json" "$env:USERPROFILE\.config\gcal-pro\client_secret.json"

# Verify
Get-Content "$env:USERPROFILE\.config\gcal-pro\client_secret.json" | Select-Object -First 3
```

**macOS/Linux:**
```bash
# Create config directory
mkdir -p ~/.config/gcal-pro

# Move the downloaded file
mv ~/Downloads/client_secret*.json ~/.config/gcal-pro/client_secret.json

# Verify
head -3 ~/.config/gcal-pro/client_secret.json
```

---

## Step 8: Verify Setup

Your config directory should now contain:
```
~/.config/gcal-pro/
└── client_secret.json    ← OAuth credentials (DO NOT SHARE)
```

After running the auth flow (next step), it will also contain:
```
~/.config/gcal-pro/
├── client_secret.json    ← OAuth credentials
└── token.json            ← User's access/refresh tokens (auto-generated)
```

---

## Security Notes

⚠️ **NEVER commit these files to git:**
- `client_secret.json` — Your app's credentials
- `token.json` — User's access tokens

Add to `.gitignore`:
```
client_secret.json
token.json
*.json
```

---

## Troubleshooting

**"Access blocked: This app's request is invalid"**
- Make sure you added your email as a test user (Step 5)

**"Error 403: access_denied"**
- App is in testing mode — only test users can authorize
- Add the user's email to test users list

**"This app isn't verified"**
- Expected during development
- Click "Advanced" → "Go to gcal-pro (unsafe)" to continue
- We'll submit for verification before public launch

---

## Next Step

Once you have `client_secret.json` saved, let me know and I'll build the OAuth authentication flow script.
