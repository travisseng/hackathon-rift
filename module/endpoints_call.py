import requests
from .parsing_template import * 
import pandas as pd
from datetime import datetime, timedelta
import time
import os

def get_account_riotid(type_region, type_gamename, type_gametag, api_key):
    response = requests.get(f"https://{type_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{type_gamename}/{type_gametag}?api_key={api_key}")
    riot_encrypted_puuid = response.json().get('puuid','')
    riot_gamename = response.json().get('gameName','')
    riot_gametag = response.json().get('tagLine','')
    return riot_encrypted_puuid, riot_gamename, riot_gametag

def get_league(riot_encrypted_puuid, api_key):
    url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-puuid/{riot_encrypted_puuid}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            all_rows = []
            for i in data:
                parsed = parse_league(i)[0]
                all_rows.append(parsed)
            league_df = pd.DataFrame(all_rows)
            
            league_df.to_csv("data/account_overview/league_overview.csv", index=False)
            print(f"✅ {len(league_df)} lignes enregistrées dans league_overview.csv")
            return league_df
        else:
            print("unranked")
    else:
        print(f"error {response.status_code}: {response.text}")
    

def get_summoners(riot_encrypted_puuid, api_key):
    url  = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{riot_encrypted_puuid}?api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        summoner_df = pd.DataFrame([parse_summoner(data)])
        summoner_df.to_csv("data/account_overview/summoner.csv")
    else:
        print(f"Erreur {response.status_code}: {response.text}")

def get_masteries(riot_encrypted_puuid, api_key):

    url = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{riot_encrypted_puuid}?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        parsed = [parse_mastery(champion) for champion in data]
        champions_masteries_df = pd.DataFrame(parsed)
        champions_masteries_df.to_csv("data/account_overview/champions_masteries.csv")
    else:
        print(f"Erreur {response.status_code}: {response.text}")

def get_wrapped_up_games(type_region,type_gamename,type_gametag,api_key):
    response = requests.get(f"https://{type_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{type_gamename}/{type_gametag}?api_key={api_key}")
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
            f"&type=ranked&start={start}&count={count}&api_key={api_key}"
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
        response = requests.get(f"https://europe.api.riotgames.com/lol/match/v5/matches/{i}?api_key={api_key}")
        
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
    os.makedirs(f"data/all_games/{type_gamename}#{type_gametag}", exist_ok=True)
    df.to_csv(f"data/all_games/{type_gamename}#{type_gametag}/{gamename}_{gametag}_{datetime.now().strftime('%Y%m%d')}.csv", index=False, encoding='utf-8')
