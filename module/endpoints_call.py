import requests
from .parsing_template import * 
import pandas as pd
from datetime import datetime, timedelta
import time
import os
import boto3
from io import StringIO
from io import BytesIO
import json

def get_account_riotid(type_region, type_gamename, type_gametag, api_key):
    response = requests.get(f"https://{type_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{type_gamename}/{type_gametag}?api_key={api_key}")
    riot_encrypted_puuid = response.json().get('puuid','')
    riot_gamename = response.json().get('gameName','')
    riot_gametag = response.json().get('tagLine','')
    return riot_encrypted_puuid, riot_gamename, riot_gametag

def get_league(type_region,type_gamename, type_gametag,riot_encrypted_puuid, api_key, bucket_name):
    s3 = boto3.client('s3')
    prefix = f"{type_gamename}#{type_gametag}"
    file_key = f"{prefix}/league_overview.csv"

    url = f"https://{type_region}.api.riotgames.com/lol/league/v4/entries/by-puuid/{riot_encrypted_puuid}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            all_rows = []
            for i in data:
                parsed = parse_league(i)[0]
                all_rows.append(parsed)
            league_df = pd.DataFrame(all_rows)
            csv_buffer = StringIO()
            league_df.to_csv(csv_buffer, index=False)

            s3.put_object(Bucket=bucket_name, Key=f"{prefix}/")

            # Upload du CSV dans S3
            s3.put_object(
                Bucket=bucket_name,
                Key=file_key,
                Body=csv_buffer.getvalue(),
                ContentType='text/csv'
            )
        else:
            print("unranked")
    else:
        print(f"error {response.status_code}: {response.text}")
    

def get_summoners(type_region,type_gamename, type_gametag,riot_encrypted_puuid, api_key,bucket_name):
    s3 = boto3.client('s3')
    prefix = f"{type_gamename}#{type_gametag}"
    file_key = f"{prefix}/summoners.csv"

    url  = f"https://{type_region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{riot_encrypted_puuid}?api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        summoner_df = pd.DataFrame([parse_summoner(data)])
            
        csv_buffer = StringIO()
        summoner_df.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=bucket_name, Key=f"{prefix}/")

        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )
    else:
        print(f"Erreur {response.status_code}: {response.text}")

def get_masteries(type_region, type_gamename, type_gametag,riot_encrypted_puuid, api_key, bucket_name):
    s3 = boto3.client('s3')
    prefix = f"{type_gamename}#{type_gametag}"
    file_key = f"{prefix}/champions_masteries.csv"

    url = f"https://{type_region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{riot_encrypted_puuid}?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        parsed = [parse_mastery(champion) for champion in data]
        champions_masteries_df = pd.DataFrame(parsed)

        csv_buffer = StringIO()
        champions_masteries_df.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=bucket_name, Key=f"{prefix}/")
        
        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )
    else:
        print(f"Erreur {response.status_code}: {response.text}")

def get_wrapped_up_games(type_region, type_gamename,type_gametag,riot_encrypted_puuid, api_key,bucket_name):
    s3 = boto3.client('s3')
    prefix = f"{type_gamename}#{type_gametag}"
    file_key = f"{prefix}/{type_gamename}_{type_gametag}_{datetime.now().strftime('%Y%m%d')}.csv"

    now = datetime.now()
    one_year_ago = now - timedelta(days=365)
    epoch_now = int(time.mktime(now.timetuple()))
    epoch_one_year_ago = int(time.mktime(one_year_ago.timetuple()))

    all_match_ids = []
    start = 0
    count = 100

    while True:
        url = (
            f"https://{type_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{riot_encrypted_puuid}/ids"
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
                if (p.get("puuid") == riot_encrypted_puuid)
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

    champions_masteries_df = pd.DataFrame(data_rows)
    csv_buffer = StringIO()
    champions_masteries_df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=f"{prefix}/")

    s3.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=csv_buffer.getvalue(),
        ContentType='text/csv'
    )

    matches_data = []

def get_timeline_games(type_region, type_gamename,type_gametag,riot_encrypted_puuid, api_key,bucket_name):
    s3 = boto3.client('s3')
    prefix = f"{type_gamename}#{type_gametag}"

    now = datetime.now()
    one_year_ago = now - timedelta(days=365)
    epoch_now = int(time.mktime(now.timetuple()))
    epoch_one_year_ago = int(time.mktime(one_year_ago.timetuple()))

    all_match_ids = []
    start = 0
    count = 100

    while True:
        url = (
            f"https://{type_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{riot_encrypted_puuid}/ids"
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


        print(f"Collected : {len(match_ids)} matchs (total: {len(all_match_ids)})")


        start += count

    
        time.sleep(1.2)  

    print(f"Sum all match collected : {len(all_match_ids)}")

    print("entré dans la boucle all match id")

    for match_id in all_match_ids:
        url = f"https://{type_region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
        response = requests.get(url)

        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 120))
            print(f"Rate limit atteint — pause de {wait} secondes...")
            time.sleep(wait)
            continue


        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                print(f"⚠️ Réponse non JSON pour {match_id}: {response.text[:200]}")
                continue

            json_bytes = BytesIO(json.dumps(data, indent=4, ensure_ascii=False).encode("utf-8"))
            s3.put_object(
                Bucket=bucket_name,
                Key=f"{prefix}/game_history/{match_id}_timeline_{type_gamename}.json",
                Body=json_bytes.getvalue(),
                ContentType="application/json"
            )


        else:
            print(f"❌ Erreur {response.status_code} pour {match_id}: {response.text[:200]}")