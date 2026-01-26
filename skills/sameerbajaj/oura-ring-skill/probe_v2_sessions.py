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
        # Check 'sleep' (not daily_sleep)
        r = await client.get(f"{base_url}/sleep", headers=headers)
        print("Sleep Session Sample:")
        print(r.json()['data'][-1] if r.status_code == 200 and 'data' in r.json() else f"Error {r.status_code}")
        
        # Check 'readiness' (not daily_readiness)
        r = await client.get(f"{base_url}/readiness", headers=headers)
        print("\nReadiness Session Sample:")
        print(r.json()['data'][-1] if r.status_code == 200 and 'data' in r.json() else f"Error {r.status_code}")

import asyncio
asyncio.run(probe())
