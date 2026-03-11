print(f"--- I AM RUNNING THIS EXACT FILE: {__file__} ---")
import discord
from discord.ext import commands
import aiohttp
import asyncio
import time

# --- CONFIGURATION ---
# Replace with your actual bot token
TOKEN = 'token_here'  # <-- REPLACE THIS WITH YOUR BOT TOKEN
# Stable API endpoint for global war summary
# The most stable "All-in-one" endpoint
API_URL = "https://helldiverstrainingmanual.com/api/v1/war/status"


# --- BOT SETUP ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# --- THE "DEMOCRACY" FUNCTION ---
async def fetch_war_data():
    base_url = "https://helldiverstrainingmanual.com/api/v1/war"
    headers = {"User-Agent": "DemocracyBot/1.0", "Accept": "application/json"}

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            # We fetch all 3 sources in parallel for speed
            tasks = [
                session.get(f"{base_url}/info"),
                session.get(f"{base_url}/status"),
                session.get(f"{base_url}/campaign")
            ]
            responses = await asyncio.gather(*tasks)
            
            # Convert all to JSON
            info_data = await responses[0].json(content_type=None)
            status_data = await responses[1].json(content_type=None)
            camp_data = await responses[2].json(content_type=None)
            
            return info_data, status_data, camp_data
        except Exception as e:
            print(f"LOG: API Connection Error: {e}")
            return None, None, None

# --- BOT COMMANDS ---
@bot.command()
async def status(ctx):
    # Ensure fetch_war_data returns (info, status_raw, campaigns) in that order
    info_raw, status_raw, campaigns = await fetch_war_data()
    
    if not all([info_raw, status_raw, campaigns]):
        return await ctx.send("❌ Connection to High Command lost.")

    # 1. MAP PLAYER COUNTS (The "status" dive)
    player_map = {}
    total_players = 0
    # The API returns status as: {"planetStatus": [...]}
    planet_status_list = status_raw.get('planetStatus', [])
    
    for p in planet_status_list:
        idx = p.get('planetIndex')
        # Deep dive into statistics -> playerCount
        stats = p.get('statistics', {})
        count = stats.get('playerCount', 0)
        player_map[idx] = count
        total_players += count

    # 2. MAP NAMES (The "info" dive)
    # The 'info' endpoint returns a dict: {"planets": { "0": {...}, "1": {...} }}
    names_map = {}
    planets_info = info_raw.get('planets', {}) # Focus on the 'planets' sub-folder
    
    for k, v in planets_info.items():
        if str(k).isdigit():
            names_map[int(k)] = v.get('name', f"Planet {k}")

    # 3. BUILD EMBED
    embed = discord.Embed(
        title="🛡️ Galactic War Status Report", 
        color=0xFFE800,
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="👥 Total Helldivers", value=f"{total_players:,}", inline=False)

    # 4. CHUNK THE FRONTS (Handle 1024 char limit)
    fronts_text = ""
    for camp in campaigns:
        p_idx = camp.get('planetIndex')
        
        # Use our new maps to get the data
        p_name = names_map.get(p_idx, f"Planet {p_idx}")
        p_count = player_map.get(p_idx, 0)
        p_type = camp.get('type', 'Combat')

        line = f"📍 **{p_name}**: {p_count:,} Divers ({p_type})\n"
        
        # If the text is getting too long for Discord, start a new field
        if len(fronts_text) + len(line) > 1000:
            embed.add_field(name="🔥 Active Fronts", value=fronts_text, inline=False)
            fronts_text = line
        else:
            fronts_text += line

    if fronts_text:
        embed.add_field(name="🔥 Active Fronts", value=fronts_text, inline=False)
    
    embed.set_footer(text="Verified by Helldivers Training Manual")
    await ctx.send(embed=embed)

# --- RUN ---
bot.run("token")
