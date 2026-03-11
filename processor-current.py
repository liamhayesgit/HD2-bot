# --- processor.py ---
#constants
MIN_HGH_ACTIVITY = 50000
DAILY_PEAK = 0

def format_steam_report(player_count):
    """Formats the data for the !status embed."""
    global DAILY_PEAK
    count = int(player_count) if player_count is not None else 0
    if player_count > DAILY_PEAK:
        DAILY_PEAK = player_count
        is_new_peak = True
    else:
        is_new_peak = False

    try:
        player_count = int(player_count)
    except (ValueError, TypeError):
        player_count = 0  # Default to 0 if conversion fails
        if player_count >= MIN_HGH_ACTIVITY:
            status_msg = "🔥 High Activity" 
            colour = 0xFFE800
        else:
            status_msg = "🛡️ Standard Ops"
            colour = 0x1b2838  # Steam Dark Blue

    if player_count == 0:
        return {
            "count": "N/A",
            "status": "⚠️ Connection Lost",
            "colour": 0xFF0000,  # Red for error
            "platform": "Steam"
        }
    if player_count > 50000:
       status_msg = "🔥 High Activity" if player_count > 50000 else "🛡️ Standard Ops"
       colour = 0xFFE800
    else:
        status_msg = "🛡️ Standard Ops"
        colour = 0x1b2838  # Steam Dark Blue

    return {
        "count": f"{player_count:,}",
        "peak": f"{DAILY_PEAK:,}" if is_new_peak else "No new peak",
        "status": status_msg,
        "colour": colour,
        "platform": "Steam (PC)"
    }

def format_presence_text(player_count):
    """Formats the 'Playing...' text for the bot's sidebar status."""
    if player_count <= 0:
        return "Waiting for Orders..."
    
    return f"{player_count:,} Helldivers on Steam"
