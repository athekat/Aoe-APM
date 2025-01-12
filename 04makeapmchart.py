import requests
from io import BytesIO
import json
import plotly.graph_objects as go


players = [
    {"name": "Carpincho", "url": "https://raw.githubusercontent.com/athekat/Aoe-APM/refs/heads/main/Carpincho_matches_with_apm.json"},
    {"name": "Nanox", "url": "https://raw.githubusercontent.com/athekat/Aoe-APM/refs/heads/main/Nanox_matches_with_apm.json"},
    {"name": "dicopatito", "url": "https://raw.githubusercontent.com/athekat/Aoe-APM/refs/heads/main/dicopatito_matches_with_apm.json"},
    {"name": "Sir Monkey", "url": "https://raw.githubusercontent.com/athekat/Aoe-APM/refs/heads/main/Sir%20Monkey_matches_with_apm.json"}
]

# Define the URL of the JSON data

url = "https://raw.githubusercontent.com/athekat/Aoe-APM/refs/heads/main/dicopatito_matches_with_apm.json"
for player in players:
    playername = player["name"]
    url = player["url"]

    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = json.load(BytesIO(response.content))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        exit() 
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit()

    dates = []
    apm_values = []
    for match in data[:50]:
        if "mean_apm" in match:  
            dates.append(match["started_date"])
            apm_values.append(match["mean_apm"])
        else:
            print(f"Warning: Match {match['matchId']} does not have 'mean_apm' data.")

    player_name = match["player_name"]
    filename = f"{playername}_apm_by_date.png"

    fig = go.Figure(
        data=[
            go.Scatter(
                x=dates,
                y=apm_values,
                mode="lines+markers",
                line=dict(color="#ADFF2F"),
                marker=dict(color="#ADFF2F"),
                text=apm_values,
                textposition='top center'
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="#2C3034",
        paper_bgcolor="#2C3034",
        font=dict(family="Arial", size=10, color="lightgray"),
        xaxis=dict(tickangle=-45, tickfont=dict(size=9)),
    )

    fig.update_xaxes(type="category", autorange="reversed")

    try:
        fig.write_image(filename, width=800, height=400, scale=2)
        print(f"Chart saved as {filename}")
    except Exception as e:
        print(f"Error writing image: {e}")