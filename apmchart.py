import requests
import json

def get_player_mean_apm(data_url, player_name):

  try:
    response = requests.get(data_url)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    data = response.json()
    return get_player_mean_apm_from_data(data, player_name)  # Reuse function

  except requests.exceptions.RequestException as e:
    print(f"Error retrieving data from {data_url}: {e}")
    return None

def get_player_mean_apm_from_data(data, player_name):
  # This part remains the same as before, extracting APM from the data
  # ... (refer to the previous code snippet for details)
  players = data["player"]
  for player_id, player_info in players.items():
    if player_info["name"] == player_name:
      apm_data = data["apm"]["mean"]
      return apm_data.get(player_id)  # Use .get() for safer access
  return None
# Example usage
data_url = "https://aoe2insights.s3.amazonaws.com/media/public/matches/analysis/analysis-361919995.json"
player_name = "Nanox"

mean_apm = get_player_mean_apm(data_url, player_name)

if mean_apm is not None:
  print(f"Mean APM for {player_name}: {mean_apm}")
else:
  print(f"Player '{player_name}' not found in the data or error retrieving data.")