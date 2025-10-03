import requests
import pandas as pd
from datetime import datetime
import json
from module.parsing_template import * 

API_URL = "https://euw1.api.riotgames.com"

########### league endpoint ############### 
league_endpoint = "/lol/league/v4/entries/by-puuid/{encryptedPUUID}"
url  = f"{API_URL}{league_endpoint.format(encryptedPUUID=encryptedPUUID)}?api_key={API_KEY}"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    if data:
        league_df = pd.DataFrame(data)
        league_df.to_csv("data/account_overview/league.csv")
        print("league", pd.DataFrame(parse_league(data)))
    else:
        print("unranked")
else:
    print(f"Erreur {response.status_code}: {response.text}")

########### summoner endpoint ############### 


summoner_endpoint = "/lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}"
url  = f"{API_URL}{summoner_endpoint.format(encryptedPUUID=encryptedPUUID)}?api_key={API_KEY}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    summoner_df = pd.DataFrame([parse_summoner(data)])
    summoner_df.to_csv("data/account_overview/summoner.csv")
    print(pd.DataFrame([parse_summoner(data)]))
else:
    print(f"Erreur {response.status_code}: {response.text}")

########### champions masteries endpoint ############### 


masteries_endpoint = "/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}"

url = f"{API_URL}{masteries_endpoint.format(encryptedPUUID=encryptedPUUID)}?api_key={API_KEY}"

headers = {
    "X-Riot-Token": API_KEY
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    parsed = [parse_mastery(champion) for champion in data]
    champions_masteries_df = pd.DataFrame(parsed)
    champions_masteries_df.to_csv("data/account_overview/champions_masteries.csv")
    print(champions_masteries_df)
else:
    print(f"Erreur {response.status_code}: {response.text}")

