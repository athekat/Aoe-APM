import json
import requests
from datetime import datetime
import time

def get_player_ratings(api_url, player_name):
    try:
        response = requests.get(api_url)
    except requests.exceptions.ConnectionError as e:
        print(f"API connection error: {e}")
        return []

    if response.status_code == 200:
        data = json.loads(response.text)
        matches = data.get("matches", [])

        match_info = []
        for match in matches[:5]: #Only last 5 matches
            matchId = match.get("matchId", [])
            started = match.get("started")
            match_info.append({
                "matchId": match["matchId"],
                "started_date": datetime.strptime(started, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M"),
            })
        # print(match_info)
        return match_info
    else:
        print(f"API request failed (status code: {response.status_code})")
        return []

players = [
    {"name": "Carpincho", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=6446904&search=&page=1"},
    {"name": "Nanox", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=439001&search=&page=1"},
    {"name": "dicopatito", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=6237950&search=&page=1"},
    {"name": "Sir Monkey", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=903496&search=&page=1"}
]

# match_info = []

for player in players:
    player_ratings = get_player_ratings(player["api_url"], player["name"])
    print(f"Retrieved data for {player['name']}")
    filename = f"{player['name']}_matchesId.json"
    with open(filename, 'w') as f:
          json.dump(player_ratings, f, indent=4)
    print("Player match data saved to json file.")
