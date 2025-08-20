import asyncio
import os
from dotenv import load_dotenv
from league_api import get_recent_matches

# Load environment variables
load_dotenv()

async def test_league_api():
    print("Testing League API...")
    
    # Check if API key is loaded
    api_key = os.getenv("RIOT_API_KEY")
    if not api_key:
        print("❌ RIOT_API_KEY not found in .env file")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Test with a summoner name
    summoner_name = "Doublelift"
    print(f"Testing with summoner: {summoner_name}")
    
    try:
        result = await get_recent_matches(summoner_name, 1)
        print(f"Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_league_api())
