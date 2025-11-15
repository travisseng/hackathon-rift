import json
import boto3

s3 = boto3.client("s3")


def lambda_handler(event, context):
    bucket_name = "s3-api-lol"

    query_params = event.get("queryStringParameters", {}) or {}
    gamename = query_params.get("gamename")
    gametag = query_params.get("gametag")
    match_id = query_params.get("match_id")
    if not gamename or not gametag:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing gamename or gametag parameter"}),
        }

    prefix = f"{gamename}_{gametag}"
    object_key = f"{prefix}/llm_output/{match_id}_analysis.json"

    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response["Body"].read().decode("utf-8")
        data = json.loads(file_content)
        data = {
            "match_id": match_id,
            "score": data.get("player", {}).get("score"),
            "summary": data.get("final_verdict", {}).get("summary"),
        }

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
