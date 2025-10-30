# get_account_data.py
import requests
import pandas as pd
import json
from module.parsing_template import *
from module.endpoints_call import *
from datetime import datetime, timedelta
import os
from var.constants import *
import boto3
import glob

API_URL = "https://euw1.api.riotgames.com"
API_KEY = os.getenv("API_KEY")


def main(type_region, type_gamename, type_gametag):
    riot_encrypted_puuid, riot_gamename, riot_gametag = get_account_riotid(
        type_region=type_region,
        type_gamename=type_gamename,
        type_gametag=type_gametag,
        api_key=API_KEY,
    )

    league_account_overview_df = get_league(type_region, riot_gamename, riot_gametag, riot_encrypted_puuid, API_KEY, "csv-holder-buckets")
    summoners_account_overview_df = get_summoners(type_region, riot_gamename, riot_gametag, riot_encrypted_puuid, API_KEY, "csv-holder-buckets")
    masteries_account_overview_df = get_masteries(type_region, riot_gamename, riot_gametag, riot_encrypted_puuid, API_KEY, "csv-holder-buckets")
    all_games_data = get_wrapped_up_games(type_region, riot_gamename, riot_gametag,riot_encrypted_puuid, API_KEY, "csv-holder-buckets")
    all_games_timeline = get_timeline_games(type_region, riot_gamename, riot_gametag,riot_encrypted_puuid, API_KEY, "csv-holder-buckets")
    
    return
