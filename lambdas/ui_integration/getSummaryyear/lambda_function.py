import json
import boto3

s3 = boto3.client("s3")


def lambda_handler(event, context):
    bucket_name = "s3-process-lol"

    query_params = event.get("queryStringParameters", {}) or {}
    gamename = query_params.get("gamename")
    gametag = query_params.get("gametag")

    if not gamename or not gametag:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing gamename or gametag parameter"}),
        }

    prefix = f"{gamename}_{gametag}"
    object_key = f"{prefix}/{prefix}_stats_monthly_json.json"

    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response["Body"].read().decode("utf-8")
        data = json.loads(file_content)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(data),
        }

    except Exception as e:
        print(f"Erreur : {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
