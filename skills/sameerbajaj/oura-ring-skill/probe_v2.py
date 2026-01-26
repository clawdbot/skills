# /// script
# dependencies = [
#   "httpx",
#   "python-dotenv",
# ]
# ///
import os
import httpx
from dotenv import load_dotenv

load_dotenv("/Users/sameerbajaj/clawd/skills/oura-ring/.env")
token = os.getenv("OURA_PERSONAL_ACCESS_TOKEN")
base_url = "https://api.ouraring.com/v2/usercollection"
headers = {"Authorization": f"Bearer {token}"}

async def probe():
    async with httpx.AsyncClient() as client:
        # Check daily_sleep details
        r = await client.get(f"{base_url}/daily_sleep", headers=headers)
        print("Daily Sleep Sample:")
        print(r.json()['data'][-1] if 'data' in r.json() else "No data")
        
        # Check daily_readiness details
        r = await client.get(f"{base_url}/daily_readiness", headers=headers)
        print("\nDaily Readiness Sample:")
        print(r.json()['data'][-1] if 'data' in r.json() else "No data")

import asyncio
asyncio.run(probe())
