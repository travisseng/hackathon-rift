# lambda_function.py

import json
import boto3
import asyncio
from all_game_data import analyze_single_match
from module.retrieve_account import *
import os


def lambda_handler(event, context):

    if event.get("body") is not None:
        event = json.loads(event.get("body"))

    region = event.get("region")
    gameid = event.get("gameid")
    gamename = event.get("gamename")
    gametag = event.get("gametag")

    API_KEY = os.environ.get("RIOT_API_KEY")

    riot_encrypted_puuid, riot_gamename, riot_gametag = get_account_riotid(
        type_region=region,
        type_gamename=gamename,
        type_gametag=gametag,
        api_key=API_KEY,
    )

    result = analyze_single_match(
        gameid, riot_gamename, riot_gametag, riot_encrypted_puuid, region
    )

    return result
