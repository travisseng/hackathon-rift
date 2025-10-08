import requests
import pandas as pd
import json
import argparse
from module.parsing_template import *
from module.endpoints_call import * 
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from var.constants import *

load_dotenv()


API_KEY = os.getenv("API_KEY")
API_URL = "https://euw1.api.riotgames.com"

parser = argparse.ArgumentParser(description="Récupération de données League of Legends")

parser.add_argument("--region", type=str, help="server region (ex: asia, europe, americas)")
parser.add_argument("--gamename", type=str, help="player game name")
parser.add_argument("--gametag", type=str, help="player game tag (ex: euw, na, kr)")

args = parser.parse_args()

type_region = args.region
type_gamename = args.gamename
type_gametag = args.gametag


riot_encrypted_puuid, riot_gamename, riot_gametag = get_account_riotid(type_region= type_region, type_gamename= type_gamename, type_gametag = type_gametag, api_key =API_KEY)

league_account_overview_df = get_league(riot_encrypted_puuid=riot_encrypted_puuid, api_key=API_KEY)
summoners_account_overview_df = get_summoners(riot_encrypted_puuid=riot_encrypted_puuid, api_key=API_KEY)
masteries_account_overview_df =  get_masteries(riot_encrypted_puuid=riot_encrypted_puuid, api_key=API_KEY)
all_games_data = get_wrapped_up_games(type_region=type_region,type_gamename=type_gamename,type_gametag=type_gametag, api_key=API_KEY)
