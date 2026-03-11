# --- processor.py ---

def process_war_report(planets_raw, campaigns_raw):
    # 1. Create a fast lookup for all planet data
    # This API uses 'index' or 'id' as the key
    planet_map = {p.get('index'): p for p in planets_raw}
    
    total_players = sum(p.get('statistics', {}).get('playerCount', 0) for p in planets_raw)

    # 2. Build the active fronts list
    active_fronts = []
    for camp in campaigns_raw:
        p_index = camp.get('planetIndex')
        p_info = planet_map.get(p_index, {})
        
        active_fronts.append({
            "name": p_info.get('name', f"Planet {p_index}"),
            "players": p_info.get('statistics', {}).get('playerCount', 0),
            "type": camp.get('type', 'Combat'),
            # Adding Health/Liberation for the new API
            "health": p_info.get('health', 0),
            "max_health": p_info.get('maxHealth', 1000000)
        })

    # Sort by player count
    active_fronts.sort(key=lambda x: x['players'], reverse=True)

    return {
        "total_players": total_players,
        "active_fronts": active_fronts
    }
