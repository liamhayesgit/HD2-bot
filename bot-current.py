import discord
from discord.ext import commands, tasks # Added 'tasks'
from api_client import fetch_steam_players
from processor import format_steam_report
from processor import format_steam_report, format_presence_text # Importing the new function for presence text formatting

# --- BOT SETUP ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 1. THE AUTO-SYNC LOOP ---

@tasks.loop(minutes=5.0)
async def update_presence():
    # 1. Fetch raw data
    raw_count = await fetch_steam_players()
    
    # 2. Process the text using our new processor function
    status_text = format_presence_text(raw_count)
    
    # 3. Update the Discord sidebar
    await bot.change_presence(activity=discord.Game(name=status_text))
    print(f"LOG: Status updated to: {status_text}")

# --- 2. START THE LOOP ON BOOT ---
@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} is Online.')
    # This starts the background task as soon as the bot connects
    if not update_presence.is_running():
        update_presence.start()

# --- 3. THE !STATUS COMMAND (Existing) ---
@bot.command()
async def status(ctx):
    raw_count = await fetch_steam_players()
    # This dictionary from processor.py must be used below
    data = format_steam_report(raw_count) 
    
    # --- THIS REBUILDS THE IMAGING ---
    embed = discord.Embed(
        title="🖥️ Steam Front-Line Report", 
        description="Real-time combat data from Super Earth High Command.",
        color=data["colour"]    
    )
    
    # We "plug in" the formatted strings from your processor
    embed.add_field(name="👥 Active Helldivers", value=data["count"], inline=True)
    embed.add_field(name="📊 Status", value=data["status"], inline=True)

    peak_label = "🔥 Daily Peak" if data["peak"] != "No new peak" else "📈 Daily Peak"
    embed.add_field(name=peak_label, value=data["peak"], inline=True)

    embed.add_field(name="📅 Status", value=data["status"], inline=False)
    embed.set_footer(text="Verified by Super Earth High Command")
                        
    # Add a thumbnail or footer for extra "imaging"
    embed.set_thumbnail(url="https://cdn.akamai.steamstatic.com/steam/apps/553850/header.jpg")  # Helldivers image
    embed.set_footer(text=f"Platform: {data['platform']} • Managed Democracy")
    embed.timestamp = discord.utils.utcnow()

    # CRITICAL: You must include 'embed=embed' here
    await ctx.send(embed=embed)

bot.run("token")

