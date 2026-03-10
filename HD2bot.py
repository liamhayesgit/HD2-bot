import api_manager
from discord.ext import commands
import discord
from api_manager import HelldiversAPI 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

hd_api = HelldiversAPI()

@bot.command()
async def status(ctx):
    data = await hd_api.get_war_status()
    
    if data and 'statistics' in data:
        # Pull the player count directly from the statistics object
        players = data['statistics'].get('playerCount', 0)
        await ctx.send(f"🎖️ **Galactic War Update**: {players:,} Helldivers are active!")
    else:
        await ctx.send("📡 Connection to High Command lost.")









bot.run("Discord token here")
