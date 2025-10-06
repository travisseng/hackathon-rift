import requests
import pandas as pd
import json
import time
import argparse
from module.parsing_template import * 
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()


API_KEY = os.getenv("API_KEY")

encrypted_puuid = "a4u8vbWEfvvt8MhF1aEMy8C26i6GPBCkPwSZfH5BYcdsxKCjdY9qcQ7NC5CnzMiZjtQFr7loSI8nvA"
API_URL = "https://euw1.api.riotgames.com"

region = 'asia'
gamename = 'reive'
gametag='euw'

response = requests.get(f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gamename}/{gametag}?api_key={API_KEY}")
encrypted_puuid = response.json().get('puuid','')
gamename = response.json().get('gameName','')
gametag = response.json().get('tagLine','')

########### league endpoint ############### 
league_endpoint = "/lol/league/v4/entries/by-puuid/{encrypted_puuid}"
url = f"{API_URL}{league_endpoint.format(encrypted_puuid=encrypted_puuid)}?api_key={API_KEY}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if data:
        all_rows = []
        for i in data:
            parsed = parse_league(i)[0]
            all_rows.append(parsed)
        league_df = pd.DataFrame(all_rows)
        
        # sauvegarder dans un seul CSV
        league_df.to_csv("data/account_overview/league_overview.csv", index=False)
        print(f"✅ {len(league_df)} lignes enregistrées dans league_overview.csv")
    else:
        print("unranked")
else:
    print(f"Erreur {response.status_code}: {response.text}")
########### summoner endpoint ############### 

summoner_endpoint = "/lol/summoner/v4/summoners/by-puuid/{encrypted_puuid}"
url  = f"{API_URL}{summoner_endpoint.format(encrypted_puuid=encrypted_puuid)}?api_key={API_KEY}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    summoner_df = pd.DataFrame([parse_summoner(data)])
    summoner_df.to_csv("data/account_overview/summoner.csv")
    print(pd.DataFrame([parse_summoner(data)]))
else:
    print(f"Erreur {response.status_code}: {response.text}")

# # ########### champions masteries endpoint ############### 


masteries_endpoint = "/lol/champion-mastery/v4/champion-masteries/by-puuid/{encrypted_puuid}"

url = f"{API_URL}{masteries_endpoint.format(encrypted_puuid=encrypted_puuid)}?api_key={API_KEY}"

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

