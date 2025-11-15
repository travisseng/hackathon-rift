# lambda_function.py

import json
import boto3
from retrieveaccount import *


def lambda_handler(event, context):

    if event.get("body") is not None:
        event = json.loads(event.get("body"))

    region = event.get("region")
    gamename = event.get("gamename")
    gametag = event.get("gametag")

    ssm = boto3.client("ssm")
    try:
        parameter = ssm.get_parameter(
            Name="/rift-rewind-challenge2/riot-api-key", WithDecryption=True
        )
        API_KEY = parameter["Parameter"]["Value"]
    except Exception as e:
        print(f"Failed to get API key: {str(e)}")
        return {"statusCode": 500, "error": "Failed to retrieve API key"}

    riot_encrypted_puuid, riot_gamename, riot_gametag = get_account_riotid(
        type_region=region,
        type_gamename=gamename,
        type_gametag=gametag,
        api_key=API_KEY,
    )
    bucket_name = "s3-api-lol"
    folder = f"{riot_gamename}_{riot_gametag}/game_context"
    s3 = boto3.client("s3")

    paginator = s3.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=folder)

    file_keys = []
    for page in page_iterator:
        if "Contents" in page:
            file_keys.extend([obj["Key"] for obj in page["Contents"]])

    if not file_keys:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "file_count": 0,
                    "files": [],
                    "message": f"No files found in folder '{folder}'",
                }
            ),
        }

    files_content = []
    for key in file_keys:
        try:
            obj = s3.get_object(Bucket=bucket_name, Key=key)
            content = obj["Body"].read().decode("utf-8")
            files_content.append(json.loads(content))
        except Exception as e:
            print(f"Failed to load {key}: {str(e)}")
            files_content.append({"key": key, "error": str(e)})

    return {
        "statusCode": 200,
        "body": json.dumps({"file_count": len(files_content), "files": files_content}),
    }
