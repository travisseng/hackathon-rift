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



#######################################

response = requests.get(f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gamename}/{gametag}?api_key=RGAPI-2861802e-6a8d-4e49-ba06-8ebc7ff7ea8c")
encrypted_puuid = response.json().get('puuid','')
gamename = response.json().get('gameName','')
gametag = response.json().get('tagLine','')

one_year_ago = datetime.now() - timedelta(days=365)
epoch_one_year_ago = int(time.mktime(one_year_ago.timetuple()))

now = datetime.now()
one_year_ago = now - timedelta(days=365)
epoch_now = int(time.mktime(now.timetuple()))
epoch_one_year_ago = int(time.mktime(one_year_ago.timetuple()))

all_match_ids = []
start = 0
count = 100  

while True:
    url = (
        f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{encrypted_puuid}/ids"
        f"?startTime={epoch_one_year_ago}&endTime={epoch_now}"
        f"&type=ranked&start={start}&count={count}&api_key={API_KEY}"
    )

    response = requests.get(url)

 
    if response.status_code != 200:
        print(f"Erreur {response.status_code} sur start={start}")
        break

    match_ids = response.json()


    if not match_ids:
        break

    all_match_ids.extend(match_ids)


    print(f"Récupéré {len(match_ids)} matchs (total: {len(all_match_ids)})")


    start += count

  
    time.sleep(1.2)  

print(f"Total de matchs collectés : {len(all_match_ids)}")

matches_data = []

for i in all_match_ids:
    response = requests.get(f"https://europe.api.riotgames.com/lol/match/v5/matches/{i}?api_key={API_KEY}")
    
    if response.status_code == 429:
        wait = int(response.headers.get("Retry-After", 120))
        print(f"Rate limit atteint — pause de {wait} secondes...")
        time.sleep(wait)
        continue

    if response.status_code == 200:
        matches_data.append(response.json())

mydata = []

for data in matches_data:
    game_played = next(
        (
            p
            for p in data.get("info", {}).get("participants", [])
            if (p.get("puuid") == encrypted_puuid)
        ),
        None
    )
    
    mydata.append(game_played)

data_rows = []

for prout in mydata:
    if prout is None:
        print(prout)

    data_rows.append({
        "player" : prout.get("riotIdGameName"),
        "death_time": prout.get("totalTimeSpentDead"),
        "deaths_amount": prout.get("deaths"),
        "kills_amount": prout.get("kills"),
        "total_damage_dealt": prout.get("totalDamageDealt"),
        "total_damage_to_champions": prout.get("totalDamageDealtToChampions"),
        "pentakills": prout.get("pentaKills"),
        "quadra_kills": prout.get("quadraKills"),
        "triple_kills": prout.get("tripleKills"),
        "skillshots_hit": prout.get("skillshotsHit"),
        "first_blood_kill": prout.get("firstBloodKill"),
        "dragon_takedowns": prout.get("challenges").get("dragonTakedowns"),
        "team_baron_kills": prout.get("challenges").get("teamBaronKills"),
        "total_minions_killed": prout.get("totalMinionsKilled"),
        "wards_placed": prout.get("wardsPlaced"),
        "wards_killed": prout.get("wardsKilled"),
        "individual_position": prout.get("individualPosition"),
        "champion_name": prout.get("championName"),
        "kda": prout.get("challenges").get("kda"),
        "epic_monster_steals": prout.get("challenges").get("epicMonsterSteals"),
    })

df = pd.DataFrame(data_rows)
df.to_csv(f"data/all_games/{gamename}_{gametag}_{datetime.now().strftime('%Y%m%d')}.csv", index=False, encoding='utf-8')
