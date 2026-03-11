# --- api_client.py ---
import aiohttp

# Official Steam API endpoint for player counts
STEAM_API_URL = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
APP_ID = "553850"

async def fetch_steam_players():
    params = {"appid": APP_ID}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(STEAM_API_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    # Returns only the number of players
                    return data.get("response", {}).get("player_count", 0)
                return 0
        except Exception as e:
            print(f"Steam API Error: {e}")
            return 0
