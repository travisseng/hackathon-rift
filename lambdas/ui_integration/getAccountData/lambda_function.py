import json
import boto3

s3 = boto3.client("s3")
BUCKET_NAME = "s3-api-lol"

FILES_TO_FETCH = ["summoners.json", "league_overview.json"]


def lambda_handler(event, context):
    query_params = event.get("queryStringParameters", {}) or {}
    gamename = query_params.get("gamename")
    gametag = query_params.get("gametag")
    prefix = f"{gamename}_{gametag}"

    if not gamename or not gametag:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing gamename or gametag parameter"}),
        }

    combined_data = {}

    for file_name in FILES_TO_FETCH:
        s3_key = f"{prefix}/{file_name}"
        try:
            response = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
            file_content = response["Body"].read().decode("utf-8")
            data = json.loads(file_content)
            key_name = file_name.replace(".json", "")
            combined_data[key_name] = data

        except Exception as e:
            print(f"Error fetching {s3_key}: {e}")
            combined_data[file_name] = {"error": str(e)}

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(combined_data),
    }
