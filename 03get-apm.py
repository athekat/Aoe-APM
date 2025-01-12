import requests
import json
import time
import os

players = [
    {"name": "Carpincho", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=6446904&search=&page=1"},
    {"name": "Nanox", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=439001&search=&page=1"},
    {"name": "dicopatito", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=6237950&search=&page=1"},
    {"name": "Sir Monkey", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=903496&search=&page=1"}
]



def get_player_mean_apm(data_url, player_name):

  try:
    response = requests.get(data_url)
    response.raise_for_status()

    data = response.json()
    return get_player_mean_apm_from_data(data, player_name)

  except requests.exceptions.RequestException as e:
    print(f"Error retrieving data from {data_url}: {e}")
    return None

def get_player_mean_apm_from_data(data, player_name):
  players = data["player"]
  for player_id, player_info in players.items():
    if player_info["name"] == player_name:
      apm_data = data["apm"]["mean"]
      return apm_data.get(player_id)  
  return None

output_file = "Carpincho_matches_with_apm.json"
output_data = []

# Load list of matches from JSON file
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        try:
            existing_data = json.load(f)
            # Create a set of existing match IDs for efficient lookup
            existing_match_ids = {item["matchId"] for item in existing_data}
            output_data.extend(existing_data)  # Start with existing data
        except json.JSONDecodeError:
            print(f"Warning: Could not decode existing JSON in {output_file}. Starting with empty data.")
            existing_match_ids = set() # Start with empty set if the file is empty or corrupted
else:
    existing_match_ids = set()

# Load list of matches from JSON file

for player in players:
  playername = player["name"]
  with open(f"{playername}_matchesId.json", "r") as f:
    matches = json.load(f)

  for match in matches:
    match_id = match["matchId"]
    
    # Check if the match ID already exists in the output data
    if match_id in existing_match_ids:
        print(f"Match {match_id} already processed. Skipping.")
        continue  # Skip to the next match
    
    data_url = f"https://aoe2insights.s3.amazonaws.com/media/public/matches/analysis/analysis-{match_id}.json"
    player_name = playername  # Update with your desired player


    mean_apm = get_player_mean_apm(data_url, player_name)

    # Add data to output structure
    match_data = {
        "matchId": match_id,
        "started_date": match["started_date"],
        "player_name": player_name
    }
    if mean_apm is not None:
      print("Processing...")
      match_data["mean_apm"] = mean_apm
    else:
      print(f"Player '{player_name}' not found or error retrieving data for match {match_id}")
    output_data.append(match_data)
    existing_match_ids.add(match_id)  
    time.sleep(5)

  # Save output to a new JSON file
  filename = f"{playername}_matches_with_apm.json"
  with open(filename, "w") as f:
    json.dump(output_data, f, indent=4)  

  print(f"{playername}'s APM data saved to json file.")