import requests
from .parsing_template import *
import pandas as pd
from datetime import datetime, timedelta
import time
import boto3
from io import StringIO
from io import BytesIO
import json
import numpy as np


def send_progress(endpoint, connection_id, data):
    '''
    Send a JSON-encoded message to a client via API Gateway WebSocket.

    Args:
        endpoint (str): The API Gateway endpoint URL.
        connection_id (str): The client connection ID. If None, nothing is sent.
        data (dict): The data to send to the client.

    Behavior:
        Creates a boto3 API Gateway Management API client and sends the JSON-encoded `data` to the given connection.
    '''
    if connection_id is None:
        return
    client = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint)
    client.post_to_connection(
        ConnectionId=connection_id, Data=json.dumps(data).encode("utf-8")
    )


def convert_numpy(obj):
    '''
    Convert numpy data types to native Python types.

    Args:
        obj: A numpy object (integer, floating, ndarray) or other.

    Returns:
        int, float, list, or str: Converted Python type suitable for JSON serialization.
    '''
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return str(obj)


def get_account_riotid(type_region, type_gamename, type_gametag, api_key):
    '''
    Retrieve the Riot account information by summoner name and tag.

    Args:
        type_region (str): Riot region code (e.g., "euw1").
        type_gamename (str): Summoner's in-game name.
        type_gametag (str): Summoner's tag/region suffix.
        api_key (str): Riot API key.

    Returns:
        tuple: (riot_encrypted_puuid, riot_gamename, riot_gametag)
    '''
    response = requests.get(
        f"https://{get_routing_value(type_region)}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{type_gamename}/{type_gametag}?api_key={api_key}"
    )
    riot_encrypted_puuid = response.json().get("puuid", "")
    riot_gamename = response.json().get("gameName", "")
    riot_gametag = response.json().get("tagLine", "")
    return riot_encrypted_puuid, riot_gamename, riot_gametag


def get_league(
    type_region, type_gamename, type_gametag, riot_encrypted_puuid, api_key, bucket_name
):
    '''
    Fetch the league entries for a player and upload the summary to S3.

    Args:
        type_region (str): Riot region code.
        type_gamename (str): Summoner's in-game name.
        type_gametag (str): Summoner's tag.
        riot_encrypted_puuid (str): Player's encrypted PUUID.
        api_key (str): Riot API key.
        bucket_name (str): S3 bucket where the league JSON will be stored.

    Behavior:
        - Retrieves league data via Riot API.
        - Parses the data using `parse_league`.
        - Uploads a JSON summary to the specified S3 bucket.
        - Prints "unranked" if the player has no ranked data.
    '''
    s3 = boto3.client("s3")
    prefix = f"{type_gamename}_{type_gametag}"
    file_key = f"{prefix}/league_overview.json"

    url = f"https://{type_region}.api.riotgames.com/lol/league/v4/entries/by-puuid/{riot_encrypted_puuid}?api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if not data:
            print("unranked")
            return json.dumps({"status": "unranked"})

        all_rows = []
        for i in data:
            parsed = parse_league(i)[0]
            all_rows.append(parsed)

        # Création du JSON
        league_json = {
            "status": "success",
            "data": {f"queue_{idx+1}": row for idx, row in enumerate(all_rows)},
        }

        # Upload vers S3 en JSON
        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(league_json, indent=4),
            ContentType="application/json",  # <- corrige le type MIME
        )


def get_summoners(
    type_region, type_gamename, type_gametag, riot_encrypted_puuid, api_key, bucket_name
):
    '''
    Fetch summoner information by PUUID and upload the data to S3.

    Args:
        type_region (str): Riot region code.
        type_gamename (str): Summoner's in-game name.
        type_gametag (str): Summoner's tag.
        riot_encrypted_puuid (str): Player's encrypted PUUID.
        api_key (str): Riot API key.
        bucket_name (str): S3 bucket to store the summoner JSON.

    Returns:
        dict: JSON containing summoner data with status "success", or error message with status "error".

    Behavior:
        - Retrieves summoner data via Riot API.
        - Parses the data using `parse_summoner`.
        - Uploads the JSON to the S3 bucket.
    '''
    s3 = boto3.client("s3")
    prefix = f"{type_gamename}_{type_gametag}"
    file_key = f"{prefix}/summoners.json"

    url = f"https://{type_region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{riot_encrypted_puuid}?api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        summoner_parsed = parse_summoner(data)

        summoner_json = {"status": "success", "data": summoner_parsed}

        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(summoner_json, indent=4),
            ContentType="application/json",
        )

        return summoner_json

    else:
        print(f"Error {response.status_code}: {response.text}")
        error_json = {"status": "error", "message": response.text}
        return error_json


def get_masteries(
    type_region, type_gamename, type_gametag, riot_encrypted_puuid, api_key, bucket_name
):
    '''
    Fetch champion mastery data for a player and upload to S3.

    Args:
        type_region (str): Riot region code.
        type_gamename (str): Summoner's in-game name.
        type_gametag (str): Summoner's tag.
        riot_encrypted_puuid (str): Player's encrypted PUUID.
        api_key (str): Riot API key.
        bucket_name (str): S3 bucket to store champion mastery JSON.

    Returns:
        dict: JSON containing mastery data with status "success", or error message with status "error".

    Behavior:
        - Retrieves champion mastery data via Riot API.
        - Parses each champion using `parse_mastery`.
        - Uploads the JSON to the S3 bucket.
    '''
    s3 = boto3.client("s3")
    prefix = f"{type_gamename}_{type_gametag}"
    file_key = f"{prefix}/champions_masteries.json"  # 

    url = f"https://{type_region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{riot_encrypted_puuid}?api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        parsed_data = [parse_mastery(champion) for champion in data]

        masteries_json = {"status": "success", "data": parsed_data}

        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(masteries_json, indent=4),
            ContentType="application/json",
        )

        return masteries_json

    else:
        print(f"Error {response.status_code}: {response.text}")
        error_json = {"status": "error", "message": response.text}
        return error_json


def get_all_match_id(
    gamename,
    gametag,
    riot_encrypted_puuid,
    type_region,
    api_key,
    bucket_name,
    ranked_type,
):
    s3 = boto3.client("s3")

    # 🔹 Liste les fichiers déjà présents
    response = s3.list_objects_v2(
        Bucket=bucket_name, Prefix=f"{gamename}_{gametag}/game_summary/"
    )

    if "Contents" in response:
        existing_files = {
            obj["Key"].split("/")[-1].replace(".json", "")
            for obj in response["Contents"]
        }
    else:
        print(
            "⚠️ Aucun fichier trouvé dans le bucket, on considère tout comme manquant."
        )
        existing_files = set()

    # 🔹 Calcul des timestamps
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    epoch_now = int(time.mktime(now.timetuple()))
    epoch_start_of_year = int(time.mktime(start_of_year.timetuple()))

    all_match_ids = []
    start = 0
    count = 100

    while True:
        queue_map = {"solo": 420, "flex": 440}

        base_url = (
            f"https://{get_routing_value(type_region)}.api.riotgames.com/"
            f"lol/match/v5/matches/by-puuid/{riot_encrypted_puuid}/ids"
        )

        if ranked_type in queue_map:
            param = f"queue={queue_map[ranked_type]}"
        elif ranked_type == "solo_and_flex":
            param = "type=ranked"
        else:
            raise ValueError(
                f" Unknown ranked_type, please select 'solo', 'flex' or 'solo_and_flex'"
            )

        url = (
            f"{base_url}?startTime={epoch_start_of_year}&endTime={epoch_now}"
            f"&{param}&start={start}&count={count}&api_key={api_key}"
        )
        response = requests.get(url)

        if response.status_code != 200:
            print(f"❌ Error {response.status_code} on {start}")
            break

        match_ids = response.json()

        if not match_ids:
            break

        all_match_ids.extend(match_ids)
        print(f"✅ Collected: {len(match_ids)} matches (total: {len(all_match_ids)})")
        start += count

    # 🔹 Limite à 200 matchs max
    if len(all_match_ids) > 100:
        step = len(all_match_ids) / 100
        all_match_ids = [all_match_ids[int(i * step)] for i in range(100)]

    # 🔹 Si aucun fichier n'existe, tous les matchs sont manquants
    if not existing_files:
        all_miss_ids = all_match_ids
    else:
        all_miss_ids = [
            match_id for match_id in all_match_ids if match_id not in existing_files
        ]
    print(ranked_type, len(all_miss_ids), len(all_match_ids))

    return all_miss_ids, all_match_ids


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


def get_item_name(item_id, items_data):
    if not item_id:
        return None
    return items_data.get("data", None).get(str(item_id), {}).get("name", None)


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


def get_wrapped_up_games(
    type_region,
    type_gamename,
    type_gametag,
    riot_encrypted_puuid,
    api_key,
    bucket_name,
    all_match_ids,
    endpoint,
    connection_id,
):
    '''
    Fetch match data for a list of match IDs, process it, and store summaries in S3.

    Args:
        type_region (str): Riot region code (e.g., "euw1").
        type_gamename (str): Summoner's in-game name.
        type_gametag (str): Summoner's tag/region suffix.
        riot_encrypted_puuid (str): Player's encrypted PUUID.
        api_key (str): Riot API key.
        bucket_name (str): Name of the S3 bucket to store match JSON and CSV.
        all_match_ids (list): List of match IDs to retrieve and process.
        endpoint (str): API Gateway endpoint URL for sending progress updates.
        connection_id (str): WebSocket connection ID to send progress updates.

    Behavior:
        - Iterates over `all_match_ids` and retrieves match details via Riot API.
        - Handles rate limiting by waiting when HTTP 429 is returned.
        - Stores each match's raw JSON in S3 under "{gamename}_{gametag}/game_summary/".
        - Identifies the player and their lane opponent in each match.
        - Extracts stats, items, summoner spells, and runes for the player and opponent.
        - Builds a full match summary including all participants' context.
        - Stores detailed match context JSON in S3 under "{gamename}_{gametag}/game_context/".
        - Aggregates all player data into a DataFrame and stores it as a CSV in S3.
        - Sends progress updates via API Gateway WebSocket as processing proceeds.
    '''
    s3 = boto3.client("s3")
    prefix = f"{type_gamename}_{type_gametag}"
    file_key = f"{prefix}/{prefix}_games_summary.csv"

    matches_data = []

    for i, match_id in enumerate(all_match_ids):
        response = requests.get(
            f"https://{get_routing_value(type_region)}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
        )

        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 30))
            print(f"Rate limit reached — awating {wait} secondes...")
            time.sleep(wait)
            continue

        if response.status_code == 200:
            matches_data.append(response.json())

        json_bytes = BytesIO(
            json.dumps(response.json(), indent=4, ensure_ascii=False).encode("utf-8")
        )
        s3.put_object(
            Bucket=bucket_name,
            Key=f"{prefix}/game_summary/{match_id}.json",
            Body=json_bytes.getvalue(),
            ContentType="application/json",
        )
        send_progress(
            endpoint,
            connection_id,
            {"type": "progress", "progress": round(i / len(all_match_ids) * 90, 1)},
        )

    all_matches = []

    items_bucket = s3.get_object(
        Bucket="ddragon-resources", Key="15.19.1/data/en_US/item.json"
    )
    items_data = json.loads(items_bucket["Body"].read())
    data_player = []
    runes = {
        "style": {
            8100: "Domination",
            8300: "Inspiration",
            8000: "Precision",
            8400: "Resolve",
            8200: "Sorcery",
        },
        "perk": {
            8112: "Electrocute",
            8128: "Dark Harvest",
            9923: "Hail of Blades",
            8126: "Cheap Shot",
            8139: "Taste of Blood",
            8143: "Sudden Impact",
            8137: "Sixth Sense",
            8140: "Grisly Mementos",
            8141: "Deep Ward",
            8135: "Treasure Hunter",
            8105: "Relentless Hunter",
            8106: "Ultimate Hunter",
            8351: "Glacial Augment",
            8360: "Unsealed Spellbook",
            8369: "First Strike",
            8306: "Hextech Flashtraption",
            8304: "Magical Footwear",
            8321: "Cash Back",
            8313: "Triple Tonic",
            8352: "Time Warp Tonic",
            8345: "Biscuit Delivery",
            8347: "Cosmic Insight",
            8410: "Approach Velocity",
            8316: "Jack Of All Trades",
            8005: "Press the Attack",
            8008: "Lethal Tempo",
            8021: "Fleet Footwork",
            8010: "Conqueror",
            9101: "Absorb Life",
            9111: "Triumph",
            8009: "Presence of Mind",
            9104: "Legend: Alacrity",
            9105: "Legend: Haste",
            9103: "Legend: Bloodline",
            8014: "Coup de Grace",
            8017: "Cut Down",
            8299: "Last Stand",
            8437: "Grasp of the Undying",
            8439: "Aftershock",
            8465: "Guardian",
            8446: "Demolish",
            8463: "Font of Life",
            8401: "Shield Bash",
            8429: "Conditioning",
            8444: "Second Wind",
            8473: "Bone Plating",
            8451: "Overgrowth",
            8453: "Revitalize",
            8242: "Unflinching",
            8214: "Summon Aery",
            8229: "Arcane Comet",
            8230: "Phase Rush",
            8224: "Axiom Arcanist",
            8226: "Manaflow Band",
            8275: "Nimbus Cloak",
            8210: "Transcendence",
            8234: "Celerity",
            8233: "Absolute Focus",
            8237: "Scorch",
            8232: "Waterwalking",
            8236: "Gathering Storm",
        },
    }

    for (
        match_data
    ) in matches_data:  # ici, all_match_ids = liste de dictionnaires JSON déjà chargés
        match_id = match_data.get("metadata", {}).get("matchId")
        participants = match_data.get("info", {}).get("participants", [])

        # Trouver le joueur principal
        player = next(
            (p for p in participants if p.get("puuid") == riot_encrypted_puuid), None
        )
        if not player:
            print(f"⚠️ Joueur {type_gamename} non trouvé dans {match_id}")
            continue

        # Trouver l'adversaire sur la même lane mais dans l'équipe adverse
        opponent = next(
            (
                p
                for p in participants
                if p.get("individualPosition") == player.get("individualPosition")
                and p.get("teamId") != player.get("teamId")
            ),
            None,
        )
        if not opponent:
            print(f"⚠️ Aucun opposant trouvé pour {type_gamename} dans {match_id}")
            continue

        # --- Dictionnaire des stats à extraire ---
        stats_keys = {
            "kills": "kills",
            "deaths": "deaths",
            "assists": "assists",
            "totalDamageDealtToChampions": "totalDamageDealtToChampions",
            "goldEarned": "goldEarned",
            "totalMinionsKilled": "totalMinionsKilled",
            "neutralMinionsKilled": "neutralMinionsKilled",
            "visionScore": "visionScore",
        }

        # --- Contexte complet de la partie ---
        context = []
        for p in participants:
            context.append(
                {
                    "name": p.get("riotIdGameName"),
                    "champion": p.get("championName"),
                    "teamId": p.get("teamId"),
                    "lane": p.get("individualPosition"),
                    "win": p.get("win"),
                    "stats": {
                        label: get_nested_value(p, key)
                        for key, label in stats_keys.items()
                    },
                    "items": [
                        get_item_name(p.get(f"item{i}"), items_data) for i in range(7)
                    ],
                    "summonerSpells": [p.get("summoner1Id"), p.get("summoner2Id")],
                    "runes": list(get_runes(p)),
                }
            )

        # --- Données principales du match ---
        match_summary = {
            "matchId": match_id,
            "gameCreation": match_data.get("info", {}).get("gameCreation"),
            "duration": int(match_data.get("info", {}).get("gameDuration", 0)),
            "player": {
                "name": player.get("riotIdGameName"),
                "lane": player.get("individualPosition"),
                "champion": player.get("championName"),
                "teamId": player.get("teamId"),
                "win": player.get("win"),
                "stats": {
                    label: get_nested_value(player, key)
                    for key, label in stats_keys.items()
                },
                "items": [player.get(f"item{i}") for i in range(7)],
                "summonerSpells": [
                    player.get("summoner1Id"),
                    player.get("summoner2Id"),
                ],
                "runes": list(get_runes(player)),
            },
            "opponent": {
                "name": opponent.get("riotIdGameName"),
                "lane": opponent.get("individualPosition"),
                "champion": opponent.get("championName"),
                "teamId": opponent.get("teamId"),
                "win": opponent.get("win"),
                "stats": {
                    label: get_nested_value(opponent, key)
                    for key, label in stats_keys.items()
                },
                "items": [opponent.get(f"item{i}") for i in range(7)],
                "summonerSpells": [
                    opponent.get("summoner1Id"),
                    opponent.get("summoner2Id"),
                ],
                "runes": list(get_runes(opponent)),
            },
            "context": context,
        }

        all_matches.append(match_summary)

        json_bytes = BytesIO(
            json.dumps(match_summary, indent=4, ensure_ascii=False).encode("utf-8")
        )
        s3.put_object(
            Bucket=bucket_name,
            Key=f"{prefix}/game_context/{match_id}.json",
            Body=json_bytes.getvalue(),
            ContentType="application/json",
        )

    items_bucket = s3.get_object(
        Bucket="ddragon-resources", Key="15.19.1/data/en_US/item.json"
    )
    items_data = json.loads(items_bucket["Body"].read())
    matches_full_data = []

    data_player = []
    runes = get_runes_from_id()
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{prefix}/game_summary/")
    for obj in response["Contents"]:
        key = obj["Key"]
        if key.endswith(".json"):
            file_obj = s3.get_object(Bucket=bucket_name, Key=key)
            file_content = file_obj["Body"].read().decode("utf-8")
            try:
                data = json.loads(file_content)
                matches_full_data.append(data)
            except json.JSONDecodeError:
                print(f" json not usable: {key}")

    for match_data in matches_full_data:
        participants = match_data.get("info", {}).get("participants", [])
        for player in participants:
            if player.get("puuid") == riot_encrypted_puuid:
                data_player.append(
                    get_data_player_infos(match_data, player, items_data, runes)
                )

    champions_masteries_df = pd.DataFrame(data_player)
    csv_buffer = StringIO()
    champions_masteries_df.to_csv(csv_buffer, index=False)

    s3.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=csv_buffer.getvalue(),
        ContentType="text/csv",
    )


def get_timeline_games(
    type_region,
    type_gamename,
    type_gametag,
    api_key,
    bucket_name,
    all_match_ids,
    offset=0,
    limit=5,
):
    '''
    Fetch match timeline data for a subset of match IDs and store in S3.

    Args:
        type_region (str): Riot region code (e.g., "euw1").
        type_gamename (str): Summoner's in-game name.
        type_gametag (str): Summoner's tag/region suffix.
        api_key (str): Riot API key.
        bucket_name (str): S3 bucket to store match timeline JSON.
        all_match_ids (list): List of match IDs to process.
        offset (int, optional): Starting index in all_match_ids. Defaults to 0.
        limit (int, optional): Maximum number of matches to process in this call. Defaults to 5.

    Returns:
        dict: Information about processed matches including count, offset, total, and remaining.
    '''
    s3 = boto3.client("s3")
    prefix = f"{type_gamename}_{type_gametag}"
    offset = len(
        s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{prefix}/game_history/").get(
            "Contents", []
        )
    )
    match_ids_slice = all_match_ids[offset : offset + limit]
    print("prout", match_ids_slice)

    for match_id in match_ids_slice:
        url = f"https://{get_routing_value(type_region)}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={api_key}"
        response = requests.get(url)

        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 5))
            print(f"Rate limit reached — awaiting {wait} secondes...")
            time.sleep(wait)
            continue

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                print(f"⚠️ not a JSON for {match_id}: {response.text[:200]}")
                continue

            json_bytes = BytesIO(
                json.dumps(data, indent=4, ensure_ascii=False).encode("utf-8")
            )
            s3.put_object(
                Bucket=bucket_name,
                Key=f"{prefix}/game_history/{match_id}.json",
                Body=json_bytes.getvalue(),
                ContentType="application/json",
            )
        else:
            print(f"{response.status_code} error for {match_id}: {response.text[:200]}")

    return {
        "processed": len(match_ids_slice),
        "offset": offset,
        "total": len(all_match_ids),
        "remaining": max(0, len(all_match_ids) - offset - limit),
    }


def set_wrapped_data(type_gamename, type_gametag, bucket_name, bucket_process_data):
    '''
    Aggregate processed game summary CSV into a wrapped JSON format and upload to S3.

    Args:
        type_gamename (str): Summoner's in-game name.
        type_gametag (str): Summoner's tag/region suffix.
        bucket_name (str): S3 bucket containing the raw game summary CSV.
        bucket_process_data (str): S3 bucket to store the wrapped-up JSON.
    '''
    s3 = boto3.client("s3")
    prefix = f"{type_gamename}_{type_gametag}"
    file_key = f"{prefix}/{prefix}_games_summary.csv"

    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    data = obj["Body"].read().decode("utf-8")
    df = pd.read_csv(StringIO(data))

    wrapped_up_json = parse_summary_to_wrapped_up(df)

    json_bytes = BytesIO(
        json.dumps(
            wrapped_up_json, indent=4, default=convert_numpy, ensure_ascii=False
        ).encode("utf-8")
    )
    s3.put_object(
        Bucket=bucket_process_data,
        Key=f"{prefix}/{prefix}_wrapped_up_stats.json",
        Body=json_bytes.getvalue(),
        ContentType="application/json",
    )


def set_summary_period_analysis(
    type_gamename, type_gametag, bucket_name, bucket_process_data
):
    '''
    Compute aggregated statistics for games per champion, position, trimester, and month; store results as JSON in S3.

    Args:
        type_gamename (str): Summoner's in-game name.
        type_gametag (str): Summoner's tag/region suffix.
        bucket_name (str): S3 bucket containing the raw game summary CSV.
        bucket_process_data (str): S3 bucket to store the aggregated statistics JSON files.

    Behavior:
        - Calculates global stats per champion/position.
        - Calculates trimester-based stats.
        - Calculates monthly stats.
        - Computes derived metrics such as CS per minute and winrate.
        - Stores results in S3 as JSON files for global, trimester, and monthly statistics.
    '''
    s3 = boto3.client("s3")
    prefix = f"{type_gamename}_{type_gametag}"
    file_key = f"{prefix}/{prefix}_games_summary.csv"

    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    data = obj["Body"].read().decode("utf-8")
    df = pd.read_csv(StringIO(data))

    df["date"] = pd.to_datetime(df["gameCreation"], unit="ms")
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%B")

    def get_trimester(row):
        if row["month"] >= 1 and row["month"] <= 3:
            return f"Q1 {row['year']}"
        elif row["month"] >= 4 and row["month"] <= 6:
            return f"Q2 {row['year']}"
        elif row["month"] >= 7 and row["month"] <= 9:
            return f"Q3 {row['year']}"
        else:
            return f"Q4 {row['year']}"

    df["trimester"] = df.apply(get_trimester, axis=1)

    top_champions = df["champion_name"].value_counts().head(10).index.tolist()
    df = df[df["champion_name"].isin(top_champions)]

    for i, champ in enumerate(top_champions, 1):
        count = (df["champion_name"] == champ).sum()

    df["cs_total"] = df["total_minions_killed"] + df["neutralMinionsKilled"]
    df["cs_per_min"] = (df["cs_total"] / df["gameDuration"]) * 60

    stats_global = (
        df.groupby(["champion_name", "teamPosition"])
        .agg(
            {
                "matchId": "count",
                "win": "sum",
                "kda": "mean",
                "kills_amount": "mean",
                "deaths_amount": "mean",
                "assists_amount": "mean",
                "cs_total": "mean",
                "cs_per_min": "mean",
                "total_damage_to_champions": "mean",
                "goldEarned": "mean",
                "totalDamageTaken": "mean",
                "visionScore": "mean",
                "wards_placed": "mean",
                "wards_killed": "mean",
            }
        )
        .reset_index()
    )

    stats_global.columns = [
        "champion",
        "position",
        "games",
        "wins",
        "avg_kda",
        "avg_kills",
        "avg_deaths",
        "avg_assists",
        "avg_cs",
        "avg_cs_per_min",
        "avg_dmg_to_champs",
        "avg_gold",
        "avg_dmg_taken",
        "avg_vision_score",
        "avg_wards_placed",
        "avg_wards_killed",
    ]

    stats_global["winrate"] = (
        stats_global["wins"] / stats_global["games"] * 100
    ).round(1)
    stats_global = stats_global.sort_values("games", ascending=False)

    stats_trimester = (
        df.groupby(["champion_name", "teamPosition", "trimester"])
        .agg(
            {
                "matchId": "count",
                "win": "sum",
                "kda": "mean",
                "kills_amount": "mean",
                "deaths_amount": "mean",
                "assists_amount": "mean",
                "cs_total": "mean",
                "cs_per_min": "mean",
                "total_damage_to_champions": "mean",
                "goldEarned": "mean",
                "totalDamageTaken": "mean",
                "visionScore": "mean",
                "wards_placed": "mean",
                "wards_killed": "mean",
            }
        )
        .reset_index()
    )

    stats_trimester.columns = [
        "champion",
        "position",
        "trimester",
        "games",
        "wins",
        "avg_kda",
        "avg_kills",
        "avg_deaths",
        "avg_assists",
        "avg_cs",
        "avg_cs_per_min",
        "avg_dmg_to_champs",
        "avg_gold",
        "avg_dmg_taken",
        "avg_vision_score",
        "avg_wards_placed",
        "avg_wards_killed",
    ]

    stats_trimester["winrate"] = (
        stats_trimester["wins"] / stats_trimester["games"] * 100
    ).round(1)
    stats_trimester = stats_trimester.sort_values(["champion", "trimester"])

    stats_monthly = (
        df.groupby(
            [
                "champion_name",
                "teamPosition",
                "trimester",
                "year",
                "month",
                "month_name",
            ]
        )
        .agg(
            {
                "matchId": "count",
                "win": "sum",
                "kda": "mean",
                "kills_amount": "mean",
                "deaths_amount": "mean",
                "assists_amount": "mean",
                "cs_total": "mean",
                "cs_per_min": "mean",
                "total_damage_to_champions": "mean",
                "goldEarned": "mean",
                "totalDamageTaken": "mean",
                "visionScore": "mean",
                "wards_placed": "mean",
                "wards_killed": "mean",
            }
        )
        .reset_index()
    )

    stats_monthly.columns = [
        "champion",
        "position",
        "trimester",
        "year",
        "month_number",
        "month_name",
        "games",
        "wins",
        "avg_kda",
        "avg_kills",
        "avg_deaths",
        "avg_assists",
        "avg_cs",
        "avg_cs_per_min",
        "avg_dmg_to_champs",
        "avg_gold",
        "avg_dmg_taken",
        "avg_vision_score",
        "avg_wards_placed",
        "avg_wards_killed",
    ]

    stats_monthly["winrate"] = (
        stats_monthly["wins"] / stats_monthly["games"] * 100
    ).round(1)
    stats_monthly = stats_monthly.sort_values(["champion", "year", "month_number"])

    champion_exemple = stats_global.iloc[0]["champion"]
    stats_champion = stats_global[stats_global["champion"] == champion_exemple].iloc[0]

    stats_global_json = stats_global.to_dict(orient="records")
    stats_trimester_json = stats_trimester.to_dict(orient="records")
    stats_monthly_json = stats_monthly.to_dict(orient="records")

    json_bytes = BytesIO(
        json.dumps(
            stats_global_json, indent=4, default=convert_numpy, ensure_ascii=False
        ).encode("utf-8")
    )
    s3.put_object(
        Bucket=bucket_process_data,
        Key=f"{prefix}/{prefix}_stats_global_json.json",
        Body=json_bytes.getvalue(),
        ContentType="application/json",
    )

    json_bytes = BytesIO(
        json.dumps(
            stats_trimester_json, indent=4, default=convert_numpy, ensure_ascii=False
        ).encode("utf-8")
    )
    s3.put_object(
        Bucket=bucket_process_data,
        Key=f"{prefix}/{prefix}_stats_trimester_json.json",
        Body=json_bytes.getvalue(),
        ContentType="application/json",
    )

    json_bytes = BytesIO(
        json.dumps(
            stats_monthly_json, indent=4, default=convert_numpy, ensure_ascii=False
        ).encode("utf-8")
    )
    s3.put_object(
        Bucket=bucket_process_data,
        Key=f"{prefix}/{prefix}_stats_monthly_json.json",
        Body=json_bytes.getvalue(),
        ContentType="application/json",
    )
