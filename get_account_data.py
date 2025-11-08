# get_account_data.py
import requests
import pandas as pd
import json
from module.parsing_template import *
from module.endpoints_call import *
from datetime import datetime, timedelta
import os 



def main(type_region, type_gamename, type_gametag, bucket_name="s3-api-lol"):
    ssm = boto3.client('ssm')
    try:
        parameter = ssm.get_parameter(
            Name='/rift-rewind-challenge2/riot-api-key',
            WithDecryption=True
        )
        API_KEY = parameter['Parameter']['Value']
    except Exception as e:
        print(f"Failed to get API key: {str(e)}")
        return {
            'statusCode': 500,
            'error': 'Failed to retrieve API key'
        }

    riot_encrypted_puuid, riot_gamename, riot_gametag = get_account_riotid(
        type_region=type_region,
        type_gamename=type_gamename,
        type_gametag=type_gametag,
        api_key=API_KEY,
    )

    get_league(type_region, riot_gamename, riot_gametag, riot_encrypted_puuid, API_KEY, bucket_name)
    get_summoners(type_region, riot_gamename, riot_gametag, riot_encrypted_puuid, API_KEY, bucket_name)
    get_masteries(type_region, riot_gamename, riot_gametag, riot_encrypted_puuid, API_KEY, bucket_name)
    get_wrapped_up_games(type_region, riot_gamename, riot_gametag,riot_encrypted_puuid, API_KEY, bucket_name)
    get_timeline_games(type_region, riot_gamename, riot_gametag,riot_encrypted_puuid, API_KEY, bucket_name)

    
    return
