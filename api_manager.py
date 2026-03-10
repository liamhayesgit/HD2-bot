import aiohttp
import time
import asyncio

class HelldiversAPI:
    def __init__(self):
        # The base website
        self.domain = "https://helldiverstrainingmanual.com"
        # The specific data path
        self.endpoint = "/api/v1/war/summary"
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            "Accept": "application/json"
        }

    async def get_war_status(self):
        # Join them together for the request
        target_url = f"{self.domain}{self.endpoint}"
        
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                print(f"LOG: Requesting from {target_url}")
                async with session.get(target_url) as response:
                    if response.status == 200:
                        # We use content_type=None to ignore the 'text/html' error
                        return await response.json(content_type=None)
                    return None
            except Exception as e:
                print(f"LOG: Error: {e}")
                return None
