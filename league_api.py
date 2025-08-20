import aiohttp
import os
from dotenv import load_dotenv


load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")


# OCE region endpoints
SUMMONER_URL = "https://oc1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}"
MATCHLIST_URL = "https://sea.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
MATCH_URL = "https://sea.api.riotgames.com/lol/match/v5/matches/{matchId}"

HEADERS = {"X-Riot-Token": RIOT_API_KEY}

async def get_recent_matches(summoner_name, count=1):
    """Get recent League of Legends matches for a summoner"""
    if not RIOT_API_KEY:
        return "❌ Riot API key not configured. Please check your environment variables."
    
    # Cap count at 5
    count = min(max(1, count), 5)
    
    async with aiohttp.ClientSession() as session:
        try:
            # 1. Get Summoner by name → returns PUUID
            summoner_response = await session.get(
                SUMMONER_URL.format(summonerName=summoner_name),
                headers=HEADERS
            )
            
            if summoner_response.status == 404:
                return f"❌ Summoner '{summoner_name}' not found in OCE region."
            elif summoner_response.status == 403:
                return "❌ Invalid Riot API key. Please check your configuration."
            elif summoner_response.status != 200:
                return f"❌ API Error: {summoner_response.status}"
            
            summoner_data = await summoner_response.json()
            puuid = summoner_data["puuid"]
            
            # 2. Get last n match IDs
            matchlist_response = await session.get(
                MATCHLIST_URL.format(puuid=puuid, count=count),
                headers=HEADERS
            )
            
            if matchlist_response.status != 200:
                return f"❌ Error fetching match list: {matchlist_response.status}"
            
            match_ids = await matchlist_response.json()
            
            if not match_ids:
                return f"❌ No recent matches found for '{summoner_name}'."
            
            # 3. Build response message
            response = f"**Recent {len(match_ids)} matches for {summoner_name}:**\n"
            
            for i, match_id in enumerate(match_ids, 1):
                # Get match details
                match_response = await session.get(
                    MATCH_URL.format(matchId=match_id),
                    headers=HEADERS
                )
                
                if match_response.status != 200:
                    continue
                
                match_data = await match_response.json()
                
                # Find player's stats
                participants = match_data["info"]["participants"]
                player_stats = next(
                    (p for p in participants if p["puuid"] == puuid), 
                    None
                )
                
                if not player_stats:
                    continue
                
                # Extract stats
                champ = player_stats["championName"]
                kills = player_stats["kills"]
                deaths = player_stats["deaths"]
                assists = player_stats["assists"]
                win = player_stats["win"]
                kda = (kills + assists) / (deaths if deaths != 0 else 1)
                
                # Add to response
                result_emoji = "🟢" if win else "🔴"
                response += f"\n{result_emoji} **Match {i}:** {champ} | {kills}/{deaths}/{assists} (KDA: {kda:.2f})"
            
            return response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
