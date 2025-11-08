import requests
from .parsing_template import * 
import pandas as pd
from datetime import datetime, timedelta
import time
import boto3
from io import StringIO
from io import BytesIO
import json

def get_routing_value(type_region):
    """
    Map platform region to routing value for Riot API
    """
    routing_map = {
        'na1': 'americas',
        'br1': 'americas',
        'la1': 'americas',
        'la2': 'americas',
        'euw1': 'europe',
        'eun1': 'europe',
        'tr1': 'europe',
        'ru': 'europe',
        'kr': 'asia',
        'jp1': 'asia',
        'oc1': 'sea',
        'ph2': 'sea',
        'sg2': 'sea',
        'th2': 'sea',
        'tw2': 'sea',
        'vn2': 'sea'
    }
    return routing_map.get(type_region, 'americas')

def get_account_riotid(type_region, type_gamename, type_gametag, api_key):
    response = requests.get(f"https://{get_routing_value(type_region)}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{type_gamename}/{type_gametag}?api_key={api_key}")
    riot_encrypted_puuid = response.json().get('puuid','')
    riot_gamename = response.json().get('gameName','')
    riot_gametag = response.json().get('tagLine','')
    return riot_encrypted_puuid, riot_gamename, riot_gametag

def get_league(type_region,type_gamename, type_gametag,riot_encrypted_puuid, api_key, bucket_name):
    s3 = boto3.client('s3')
    prefix = f"{type_gamename}_{type_gametag}"
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

def get_item_name(item_id, items_data):
    if not item_id:
        return None
    return items_data.get("data", None).get(str(item_id), {}).get("name", None)

def get_item_name(item_id, items_data):
    if not item_id:
        return None
    return items_data.get("data", None).get(str(item_id), {}).get("name", None)

def get_summoners(type_region,type_gamename, type_gametag,riot_encrypted_puuid, api_key,bucket_name):
    s3 = boto3.client('s3')
    prefix = f"{type_gamename}_{type_gametag}"
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
        print(f"error {response.status_code}: {response.text}")

def get_masteries(type_region, type_gamename, type_gametag,riot_encrypted_puuid, api_key, bucket_name):
    s3 = boto3.client('s3')
    prefix = f"{type_gamename}_{type_gametag}"
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
        print(f"error {response.status_code}: {response.text}")

def get_nested_value(data, key_path):
    keys = key_path.split(".")
    val = data
    for k in keys:
        val = val.get(k, 0) if isinstance(val, dict) else 0
    return val

def get_runes(p):
    styles = p.get("perks", {}).get("styles", [])
    primary = styles[0].get("style") if len(styles) > 0 else None
    sub = styles[1].get("style") if len(styles) > 1 else None
    return primary, sub

stats_keys = {
    "championName": "Champion",
    "teamPosition": "Team Position",
    "individualPosition": "Individual Position",
    "totalTimeSpentDead": "Total Time Dead",
    "kills": "Kills",
    "deaths": "Deaths",
    "assists": "Assists",
    "totalMinionsKilled": "Total Minions Killed",
    "neutralMinionsKilled": "Neutral Minions Killed",
    "totalDamageDealt": "Total Damage Dealt",
    "totalDamageDealtToChampions": "Damage to Champions",
    "goldEarned": "Gold Earned",
    "totalDamageTaken": "Damage Taken",
    "visionScore": "Vision Score",
    "wardsPlaced": "Wards Placed",
    "wardsKilled": "Wards Killed",
    "challenges.kda": "KDA",
    "pentaKills": "Penta Kills",
    "quadraKills": "Quadra Kills",
    "tripleKills": "Triple Kills",
    "skillshotsHit": "Skillshots Hit",
    "firstBloodKill": "First Blood Kill",
    "challenges.dragonTakedowns": "Dragon Takedowns",
    "challenges.teamBaronKills": "Team Baron Kills",
    "challenges.epicMonsterSteals": "Epic Monster Steals",
}

def get_wrapped_up_games(type_region, type_gamename,type_gametag,riot_encrypted_puuid, api_key,bucket_name):
    s3 = boto3.client('s3')
    prefix = f"{type_gamename}_{type_gametag}"
    file_key = f"{prefix}/{type_gamename}_{type_gametag}_games_summary.csv"

    now = datetime.now()
    one_year_ago = now - timedelta(days=365)
    epoch_now = int(time.mktime(now.timetuple()))
    epoch_one_year_ago = int(time.mktime(one_year_ago.timetuple()))

    all_match_ids = []
    start = 0
    count = 100

    while True:
        url = (
            f"https://{get_routing_value(type_region)}.api.riotgames.com/lol/match/v5/matches/by-puuid/{riot_encrypted_puuid}/ids"
            f"?startTime={epoch_one_year_ago}&endTime={epoch_now}"
            f"&type=ranked&start={start}&count={count}&api_key={api_key}"
        )

        response = requests.get(url)

    
        if response.status_code != 200:
            print(f"error {response.status_code} on start={start}")
            break

        match_ids = response.json()


        if not match_ids:
            break

        all_match_ids.extend(match_ids)


        print(f"Gathered {len(match_ids)} matchs (total: {len(all_match_ids)})")


        start += count

    
        time.sleep(1.2)  

    print(f"amount of matchs collected : {len(all_match_ids)}")

    matches_data = []

    for match_id in all_match_ids:
        response = requests.get(f"https://{get_routing_value(type_region)}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}")
        
        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 120))
            print(f"Rate limit reached — awating {wait} secondes...")
            time.sleep(wait)
            continue

        if response.status_code == 200:
            matches_data.append(response.json())


    items_bucket = s3.get_object(Bucket="ddragon-resources", Key="15.19.1/data/en_US/item.json")
    items_data = json.loads(items_bucket['Body'].read())
    data_player = []
    runes = {"style": {8100: 'Domination',
    8300: 'Inspiration',
    8000: 'Precision',
    8400: 'Resolve',
    8200: 'Sorcery'},
    "perk":{8112: 'Electrocute',
    8128: 'Dark Harvest',
    9923: 'Hail of Blades',
    8126: 'Cheap Shot',
    8139: 'Taste of Blood',
    8143: 'Sudden Impact',
    8137: 'Sixth Sense',
    8140: 'Grisly Mementos',
    8141: 'Deep Ward',
    8135: 'Treasure Hunter',
    8105: 'Relentless Hunter',
    8106: 'Ultimate Hunter',
    8351: 'Glacial Augment',
    8360: 'Unsealed Spellbook',
    8369: 'First Strike',
    8306: 'Hextech Flashtraption',
    8304: 'Magical Footwear',
    8321: 'Cash Back',
    8313: 'Triple Tonic',
    8352: 'Time Warp Tonic',
    8345: 'Biscuit Delivery',
    8347: 'Cosmic Insight',
    8410: 'Approach Velocity',
    8316: 'Jack Of All Trades',
    8005: 'Press the Attack',
    8008: 'Lethal Tempo',
    8021: 'Fleet Footwork',
    8010: 'Conqueror',
    9101: 'Absorb Life',
    9111: 'Triumph',
    8009: 'Presence of Mind',
    9104: 'Legend: Alacrity',
    9105: 'Legend: Haste',
    9103: 'Legend: Bloodline',
    8014: 'Coup de Grace',
    8017: 'Cut Down',
    8299: 'Last Stand',
    8437: 'Grasp of the Undying',
    8439: 'Aftershock',
    8465: 'Guardian',
    8446: 'Demolish',
    8463: 'Font of Life',
    8401: 'Shield Bash',
    8429: 'Conditioning',
    8444: 'Second Wind',
    8473: 'Bone Plating',
    8451: 'Overgrowth',
    8453: 'Revitalize',
    8242: 'Unflinching',
    8214: 'Summon Aery',
    8229: 'Arcane Comet',
    8230: 'Phase Rush',
    8224: 'Axiom Arcanist',
    8226: 'Manaflow Band',
    8275: 'Nimbus Cloak',
    8210: 'Transcendence',
    8234: 'Celerity',
    8233: 'Absolute Focus',
    8237: 'Scorch',
    8232: 'Waterwalking',
    8236: 'Gathering Storm'}
    }

    for match_data in matches_data:
        participants = match_data.get("info", {}).get("participants", [])
        for player in participants:
            if player.get("puuid") == riot_encrypted_puuid:
                data_player.append({
                    'matchId': match_data.get('metadata', {}).get('matchId'),
                    'gameCreation': match_data.get('info', {}).get('gameCreation'),
                    'gameDuration': match_data.get('info', {}).get('gameDuration'),
                    'gameMode': match_data.get('info', {}).get('gameMode'),
                    'queueId': match_data.get('info', {}).get('queueId'),
                    'queueType': {
                        420: "5v5 Ranked Solo games",
                        440: "5v5 Ranked Flex games"
                    }.get(match_data.get('info', {}).get('queueId'), "Other"),
                    "champion_name": player.get("championName"),
                    "champion_id": player.get("championId"),
                    "teamPosition": player.get("teamPosition"),
                    "individualPosition": player.get("individualPosition"),
                    "player": player.get("riotIdGameName"),
                    "death_time": player.get("totalTimeSpentDead"),
                    "kills_amount": player.get("kills"),
                    "deaths_amount": player.get("deaths"),
                    "assists_amount": player.get("assists"),
                    "total_minions_killed": player.get("totalMinionsKilled"),
                    "neutralMinionsKilled": player.get("neutralMinionsKilled"),
                    "cs_score": player.get("totalMinionsKilled") + player.get("neutralMinionsKilled"),
                    "total_damage_dealt": player.get("totalDamageDealt"),
                    "total_damage_to_champions": player.get("totalDamageDealtToChampions"),
                    "goldEarned": player.get("goldEarned"),
                    "totalDamageTaken": player.get("totalDamageTaken"),
                    'win': player.get('win'),
                    'items_0': get_item_name(player.get('item0'), items_data),
                    'items_1': get_item_name(player.get('item1'), items_data),
                    'items_2': get_item_name(player.get('item2'), items_data),
                    'items_3': get_item_name(player.get('item3'), items_data),
                    'items_4': get_item_name(player.get('item4'), items_data),
                    'items_5': get_item_name(player.get('item5'), items_data),
                    'items_6': get_item_name(player.get('item6'), items_data),
                    'summoner1Id': player.get('summoner1Id'),
                    'summoner2Id': player.get('summoner2Id'),
                    'primaryStyle': player.get('perks', {}).get('styles', [{}])[0].get('style'),
                    'primaryStyle_name': runes.get("style").get(player.get('perks', {}).get('styles', [{}])[0].get('style')),
                    'subStyle': player.get('perks', {}).get('styles', [{}])[1].get('style') if len(player.get('perks', {}).get('styles', [])) > 1 else None,
                    'subStyle_name': runes.get("style").get(player.get('perks', {}).get('styles', [{}])[1].get('style') if len(player.get('perks', {}).get('styles', [])) > 1 else None),
                    'primaryPerk': player.get('perks', {}).get('styles', [{}])[0].get('selections', [{}])[0].get('perk'),
                    'primaryPerk_name': runes.get("perk").get(player.get('perks', {}).get('styles', [{}])[0].get('selections', [{}])[0].get('perk')),
                    "pentakills": player.get("pentaKills"),
                    "quadra_kills": player.get("quadraKills"),
                    "triple_kills": player.get("tripleKills"),
                    "skillshots_hit": player.get("skillshotsHit"),
                    "first_blood_kill": player.get("firstBloodKill"),
                    "dragon_takedowns": player.get("challenges", {}).get("dragonTakedowns"),
                    "team_baron_kills": player.get("challenges", {}).get("teamBaronKills"),
                    "visionScore": player.get("visionScore"),
                    "wards_placed": player.get("wardsPlaced"),
                    "wards_killed": player.get("wardsKilled"),
                    "individual_position": player.get("individualPosition"),
                    "kda": player.get("challenges", {}).get("kda"),
                    "epic_monster_steals": player.get("challenges", {}).get("epicMonsterSteals"),
                })

    champions_masteries_df = pd.DataFrame(data_player)
    csv_buffer = StringIO()
    champions_masteries_df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=f"{prefix}/")

    s3.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=csv_buffer.getvalue(),
        ContentType='text/csv'
    )
    
    all_matches = []

    for match_data in matches_data:  # ici, all_match_ids = liste de dictionnaires JSON déjà chargés
        match_id = match_data.get("metadata", {}).get("matchId")
        participants = match_data.get("info", {}).get("participants", [])

        # Trouver le joueur principal
        player = next((p for p in participants if p.get("puuid") == riot_encrypted_puuid), None)
        if not player:
            print(f"⚠️ Joueur {type_gamename} non trouvé dans {match_id}")
            continue

        # Trouver l'adversaire sur la même lane mais dans l'équipe adverse
        opponent = next(
            (p for p in participants
             if p.get("individualPosition") == player.get("individualPosition")
             and p.get("teamId") != player.get("teamId")),
            None
        )
        if not opponent:
            print(f"⚠️ Aucun opposant trouvé pour {type_gamename} dans {match_id}")
            continue

        # --- Dictionnaire des stats à extraire ---
        stats_keys = {
            "kills": "Kills",
            "deaths": "Deaths",
            "assists": "Assists",
            "totalDamageDealtToChampions": "Damage to Champions",
            "goldEarned": "Gold",
            "totalMinionsKilled": "CS",
            "visionScore": "Vision Score"
        }

        # --- Contexte complet de la partie ---
        context = []
        for p in participants:
            context.append({
                "name": p.get("riotIdGameName"),
                "champion": p.get("championName"),
                "teamId": p.get("teamId"),
                "lane": p.get("individualPosition"),
                "win": p.get("win"),
                "stats": {label: get_nested_value(p, key) for key, label in stats_keys.items()},
                "items": [get_item_name(p.get(f"item{i}"),items_data) for i in range(7)],
                "summonerSpells": [p.get("summoner1Id"), p.get("summoner2Id")],
                "runes": list(get_runes(p)),
            })

        # --- Données principales du match ---
        match_summary = {
            "matchId": match_id,
            "gameMode": match_data.get("info", {}).get("gameMode"),
            "duration_min": int(match_data.get("info", {}).get("gameDuration", 0) // 60),
            "player": {
                "name": player.get("riotIdGameName"),
                "champion": player.get("championName"),
                "teamId": player.get("teamId"),
                "win": player.get("win"),
                "stats": {label: get_nested_value(player, key) for key, label in stats_keys.items()},
                "items": [player.get(f"item{i}") for i in range(7)],
                "summonerSpells": [player.get("summoner1Id"), player.get("summoner2Id")],
                "runes": list(get_runes(player)),
            },
            "opponent": {
                "name": opponent.get("riotIdGameName"),
                "champion": opponent.get("championName"),
                "teamId": opponent.get("teamId"),
                "win": opponent.get("win"),
                "stats": {label: get_nested_value(opponent, key) for key, label in stats_keys.items()},
                "items": [opponent.get(f"item{i}") for i in range(7)],
                "summonerSpells": [opponent.get("summoner1Id"), opponent.get("summoner2Id")],
                "runes": list(get_runes(opponent)),
            },
            "context": context
        }

        all_matches.append(match_summary)

        json_bytes = BytesIO(json.dumps(match_summary, indent=4, ensure_ascii=False).encode("utf-8"))
        s3.put_object(
            Bucket=bucket_name,
            Key=f"{prefix}/game_context/{match_id}.json",
            Body=json_bytes.getvalue(),
            ContentType="application/json"
        )


def get_timeline_games(type_region, type_gamename,type_gametag,riot_encrypted_puuid, api_key,bucket_name):
    s3 = boto3.client('s3')
    prefix = f"{type_gamename}_{type_gametag}"

    now = datetime.now()
    one_year_ago = now - timedelta(days=365)
    epoch_now = int(time.mktime(now.timetuple()))
    epoch_one_year_ago = int(time.mktime(one_year_ago.timetuple()))

    all_match_ids = []
    start = 0
    count = 100

    while True:
        url = (
            f"https://{get_routing_value(type_region)}.api.riotgames.com/lol/match/v5/matches/by-puuid/{riot_encrypted_puuid}/ids"
            f"?startTime={epoch_one_year_ago}&endTime={epoch_now}"
            f"&type=ranked&start={start}&count={count}&api_key={api_key}"
        )

        response = requests.get(url)

    
        if response.status_code != 200:
            print(f"Error {response.status_code} on {start}")
            break

        match_ids = response.json()


        if not match_ids:
            break

        all_match_ids.extend(match_ids)


        print(f"Collected : {len(match_ids)} matchs (total: {len(all_match_ids)})")


        start += count

    
        time.sleep(1.2)  

    print(f"Sum all match collected : {len(all_match_ids)}")

    for match_id in all_match_ids:
        url = f"https://{get_routing_value(type_region)}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={api_key}"
        response = requests.get(url)

        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 120))
            print(f"Rate limit reached — awating {wait} secondes...")
            time.sleep(wait)
            continue


        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                print(f"⚠️ not a JSON for {match_id}: {response.text[:200]}")
                continue

            json_bytes = BytesIO(json.dumps(data, indent=4, ensure_ascii=False).encode("utf-8"))
            s3.put_object(
                Bucket=bucket_name,
                Key=f"{prefix}/game_history/{match_id}.json",
                Body=json_bytes.getvalue(),
                ContentType="application/json"
            )

        else:
            print(f"{response.status_code} error for {match_id}: {response.text[:200]}")


    for match_id in all_match_ids:
        url = f"https://{get_routing_value(type_region)}.api.riotgames.com/lol/match/v5/matches/{match_id}/?api_key={api_key}"
        response = requests.get(url)

        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 120))
            print(f"Rate limit reached — awating {wait} secondes...")
            time.sleep(wait)
            continue


        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                print(f"⚠️ not a JSON for {match_id}: {response.text[:200]}")
                continue

            json_bytes = BytesIO(json.dumps(data, indent=4, ensure_ascii=False).encode("utf-8"))
            s3.put_object(
                Bucket=bucket_name,
                Key=f"{prefix}/game_summary/{match_id}.json",
                Body=json_bytes.getvalue(),
                ContentType="application/json"
            )

        else:
            print(f"{response.status_code} error for {match_id}: {response.text[:200]}")