import requests
import time
import json

def trigger_analysis(match_ids_file):
    """Triggers analysis for match IDs from a JSON file."""

    try:
        with open(match_ids_file, 'r') as f:
            match_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{match_ids_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{match_ids_file}'.")
        return

    base_url = "https://www.aoe2insights.com/match/{}/analyze/"

    for match in match_data:
        match_id = match.get("matchId")
        if not match_id:
            print("Error: 'matchId' key missing in one of the JSON objects.")
            continue  # Skip to the next match

        url = base_url.format(match_id)
        print(f"Requesting: {url}")

        try:
            response = requests.get(url)

            if response.status_code == 200:
                print(f"{playername}'s Match ID {match_id}: Analysis triggered successfully.")
                # Process response if needed:
                # print(response.text)
                # data = response.json()
                # print(data)

            elif response.status_code == 404:
                print(f"Match ID {match_id}: Not Found (404).")
            else:
                print(f"Match ID {match_id}: Request failed with status code {response.status_code}")
                print(response.text) # Print the response content to see the error

        except requests.exceptions.RequestException as e:
            print(f"Match ID {match_id}: An error occurred: {e}")

        time.sleep(5)

if __name__ == "__main__":
    players = [
    {"name": "Carpincho", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=6446904&search=&page=1"},
    {"name": "Nanox", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=439001&search=&page=1"},
    {"name": "dicopatito", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=6237950&search=&page=1"},
    {"name": "Sir Monkey", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=903496&search=&page=1"}
]
   
    for player in players:
        playername = player["name"]
        match_ids_file = f"{playername}_matchesId.json" # Replace with your json file name
        trigger_analysis(match_ids_file)