import requests

def get_enriched_war_data():
    base_url = "https://helldiverstrainingmanual.com/api/v1/war"
    
    try:
        info_resp = requests.get(f"{base_url}/info")
        camp_resp = requests.get(f"{base_url}/campaign")
        
        all_planets = info_resp.json()
        active_campaigns = camp_resp.json()

        # DEBUG: This will show you exactly what words the API is using
        if isinstance(all_planets, list) and len(all_planets) > 0:
            print(f"--- API Keys detected: {list(all_planets[0].keys())} ---")

        print(f"\n--- LIVE CAMPAIGN REPORT ---")
        for camp in active_campaigns:
            p_id = camp.get('planetIndex')
            
            # Use 'id' if 'planetIndex' isn't there
            if p_id is None: p_id = camp.get('id')

            planet_name = "Unknown Planet"
            if isinstance(all_planets, list) and p_id < len(all_planets):
                # Try common name keys
                p_data = all_planets[p_id]
                planet_name = p_data.get('name') or p_data.get('planetName') or f"Planet {p_id}"

            # Try common status keys
            status = camp.get('type') or camp.get('status') or "Active Combat"

            print(f"📍 {planet_name} | Status: {status}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_enriched_war_data()
print("\n--- END OF REPORT ---")
