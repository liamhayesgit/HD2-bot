print(f"--- I AM RUNNING THIS EXACT FILE: {__file__} ---")
import discord
from discord.ext import commands
import aiohttp
import asyncio
import time

# --- CONFIGURATION ---
# Replace with your actual bot token
TOKEN = 'Discord token here' 
# Stable API endpoint for global war summary
# The most stable "All-in-one" endpoint
API_URL = "https://helldiverstrainingmanual.com/api/v1/war/status"


# --- BOT SETUP ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- THE "DEMOCRACY" FUNCTION ---
async def fetch_war_data():
    # NOTICE: We changed 'status' to 'summary' at the end of the URL
    url = "https://helldiverstrainingmanual.com"
    
    headers = {
        "User-Agent": "DemocracyBot/1.0",
        "Accept": "application/json"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            print(f"LOG: Requesting Summary from: {url}")
            async with session.get(url) as response:
                if response.status == 200:
                    # content_type=None is still needed to bypass the HTML error
                    return await response.json(content_type=None)
                return None
        except Exception as e:
            print(f"LOG: API Connection Error: {e}")
            return None

              
# --- BOT COMMANDS ---
@bot.command()
async def status(ctx):
    data = await fetch_war_data()
    
    # 1. The Training Manual API uses 'planetStatus' as the main list
    if data and 'planetStatus' in data:
        total_players = 0
        
        # 2. We must loop through every planet and look inside its 'statistics'
        for planet in data['planetStatus']:
            stats = planet.get('statistics', {})
            # The key is 'playerCount' (case-sensitive!)
            count = stats.get('playerCount', 0)
            total_players += count
            
        # 3. Create the Pro Embed
        embed = discord.Embed(
            title="🛡️ Galactic War Status Report", 
            description="Real-time data from Super Earth High Command.",
            color=0xFFE800
        )
        # Use {total_players:,} to add commas (e.g., 45,231)
        embed.add_field(name="👥 Active Helldivers", value=f"{total_players:,}", inline=True)
        embed.set_footer(text="Status: Operational • Managed Democracy")
        embed.timestamp = discord.utils.utcnow()
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ High Command sent a scrambled signal (No planet data).")



# --- RUN ---
bot.run(TOKEN)
