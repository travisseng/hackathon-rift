import json
import boto3
import os

s3 = boto3.client("s3")


def lambda_handler(event, context):
    params = event.get("body")
    if params:
        params = json.loads(params)
        name = params.get("name")
        gametag = params.get("gametag")
    else:
        name = event.get("name")
        gametag = event.get("gametag")

    if not name or not gametag:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(
                {"error": f"{event} Missing 'name' or 'gametag' parameter"}
            ),
        }

    bucket_name = os.environ.get("BUCKET_NAME", "s3-process-lol")
    key_prefix = f"{name}_{gametag}"
    file_key = f"{key_prefix}/{key_prefix}_wrapped_up_stats.json"

    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response["Body"].read().decode("utf-8")
        json_content = json.loads(file_content)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(
                {
                    "exists": True,
                    "bucket": bucket_name,
                    "path": file_key,
                    "content": json_content,
                }
            ),
        }

    except s3.exceptions.ClientError as e:
        if (
            e.response["Error"]["Code"] == "NoSuchKey"
            or e.response["Error"]["Code"] == "404"
        ):
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps(
                    {"exists": False, "bucket": bucket_name, "path": file_key}
                ),
            }
        else:
            # Unexpected error
            raise e
