=====================================
 gcal-pro - Google Calendar for Clawdbot
 Installation Guide
=====================================

Thank you for purchasing gcal-pro!

REQUIREMENTS
------------
- Clawdbot installed (https://clawd.bot)
- Python 3.11+
- Google account

QUICK INSTALL (5 minutes)
-------------------------

1. Extract this zip to your Clawdbot skills folder or any location

2. Install Python dependencies:
   pip install -r requirements.txt

3. Set up Google Calendar API (one-time):
   - Go to https://console.cloud.google.com
   - Create a new project called "gcal-pro"
   - Enable "Google Calendar API"
   - Go to APIs & Services > OAuth consent screen
   - Select "External", fill in app name and email
   - Add scopes: calendar.readonly and calendar.events
   - Add yourself as a test user
   - Go to Credentials > Create Credentials > OAuth client ID
   - Select "Desktop app", download the JSON
   - Save it as: ~/.config/gcal-pro/client_secret.json

4. Authenticate:
   python scripts/gcal_auth.py auth
   (Browser will open - sign in with Google)

5. Activate your Pro license:
   python scripts/gcal_license.py activate --key YOUR-LICENSE-KEY

6. Test it:
   python scripts/gcal_core.py today
   python scripts/gcal_core.py brief

USAGE WITH CLAWDBOT
-------------------
Just talk naturally:
- "What's on my calendar today?"
- "Schedule lunch with Alex Friday at noon"
- "Delete my 3pm meeting"
- "When am I free this week?"

SUPPORT
-------
Issues? Email: [your-email]
Docs: See SKILL.md for full documentation

=====================================
