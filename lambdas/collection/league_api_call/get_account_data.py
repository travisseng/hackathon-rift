# get_account_data.py
import requests
import pandas as pd
import json
from module.parsing_template import *
from module.endpoints_call import *
from datetime import datetime, timedelta
import os
import boto3
import time
import os


def get_api_key():
    return os.environ.get("RIOT_API_KEY")


def send_progress(endpoint, connection_id, data):
    """
    Send a JSON-encoded progress message to a client via API Gateway WebSocket.

    Args:
        endpoint (str): The API Gateway endpoint URL.
        connection_id (str): The connection ID of the client. If None, the function does nothing.
        data (dict): The data to send to the client.

    Behavior:
        - Creates an API Gateway Management API client for the given endpoint.
        - Sends the JSON-encoded `data` to the specified `connection_id`.
    """
    if connection_id is None:
        return
    client = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint)
    client.post_to_connection(
        ConnectionId=connection_id, Data=json.dumps(data).encode("utf-8")
    )


def main(
    type_region,
    type_gamename,
    type_gametag,
    query_params,
    ranked_type="solo",
    bucket_name="s3-api-lol",
    bucket_process_data="s3-process-lol",
):

    connection_id = query_params.get("connectionId", None)
    endpoint = "https://v19yst44bk.execute-api.eu-west-3.amazonaws.com/production"
    API_KEY = get_api_key()

    try:
        send_progress(endpoint, connection_id, {"type": "progress", "progress": 0})
        riot_encrypted_puuid, riot_gamename, riot_gametag = get_account_riotid(
            type_region=type_region,
            type_gamename=type_gamename,
            type_gametag=type_gametag,
            api_key=API_KEY,
        )

        get_league(
            type_region,
            riot_gamename,
            riot_gametag,
            riot_encrypted_puuid,
            API_KEY,
            bucket_name,
        )
        get_summoners(
            type_region,
            riot_gamename,
            riot_gametag,
            riot_encrypted_puuid,
            API_KEY,
            bucket_name,
        )
        end_time = time.time()
        get_masteries(
            type_region,
            riot_gamename,
            riot_gametag,
            riot_encrypted_puuid,
            API_KEY,
            bucket_name,
        )
        end_time = time.time()
        all_miss_ids, all_match_ids = get_all_match_id(
            riot_gamename,
            riot_gametag,
            riot_encrypted_puuid,
            type_region,
            API_KEY,
            bucket_name,
            ranked_type,
        )
        end_time = time.time()
        if len(all_miss_ids) > 0:
            get_wrapped_up_games(
                type_region,
                riot_gamename,
                riot_gametag,
                riot_encrypted_puuid,
                API_KEY,
                bucket_name,
                all_miss_ids,
                endpoint,
                connection_id,
            )
            set_wrapped_data(
                riot_gamename, riot_gametag, bucket_name, bucket_process_data
            )
            set_summary_period_analysis(
                riot_gamename, riot_gametag, bucket_name, bucket_process_data
            )
            send_progress(endpoint, connection_id, {"type": "progress", "progress": 90})
            get_timeline_games(
                type_region,
                riot_gamename,
                riot_gametag,
                API_KEY,
                bucket_name,
                all_match_ids,
            )
        else:
            print("No match ids found")
        send_progress(endpoint, connection_id, {"type": "complete"})
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Full execution completed successfully"}),
        }

    except Exception as e:
        print(f"Error in main: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
