#!/usr/bin/env python3
"""
Test script to verify the gold price API and MCP function work correctly
"""

import asyncio
import json
import httpx

async def test_gold_api():
    """Test fetching gold prices from API"""
    api_url = "https://api.chnwt.dev/thai-gold-api/latest"
    
    print("Testing Gold Price API...")
    print(f"URL: {api_url}\n")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "success" and "response" in data:
                result = data["response"]
                
                print("✅ API Response Success!")
                print("\n" + "="*50)
                print(json.dumps(result, ensure_ascii=False, indent=2))
                print("="*50)
                
                # Display formatted output
                print("\n📊 ราคาทองคำวันนี้:")
                print(f"  วันที่: {result['date']}")
                print(f"  อัพเดท: {result['update_time']}")
                print(f"\n  ทองรูปพรรณ:")
                print(f"    ซื้อ: {result['price']['gold']['buy']} บาท")
                print(f"    ขาย: {result['price']['gold']['sell']} บาท")
                print(f"\n  ทองแท่ง:")
                print(f"    ซื้อ: {result['price']['gold_bar']['buy']} บาท")
                print(f"    ขาย: {result['price']['gold_bar']['sell']} บาท")
                print(f"\n  การเปลี่ยนแปลง:")
                print(f"    เทียบครั้งก่อน: {result['price']['change']['compare_previous']}")
                print(f"    เทียบเมื่อวาน: {result['price']['change']['compare_yesterday']}")
                
            else:
                print("❌ Invalid response format from API")
                print(json.dumps(data, ensure_ascii=False, indent=2))
                
    except httpx.HTTPError as e:
        print(f"❌ HTTP error occurred: {str(e)}")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_gold_api())
