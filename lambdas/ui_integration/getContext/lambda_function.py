import json
import boto3


def lambda_handler(event, context):
    query_params = event.get("queryStringParameters")
    bucket_name = "s3-api-lol"
    prefix = query_params.get("prefix")

    if not prefix:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'prefix' parameter"}),
        }

    s3 = boto3.client("s3")

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{prefix}/game_context/")
    files = response.get("Contents", [])

    all_data = []

    for obj in files:
        key = obj["Key"]

        if key.endswith("/"):
            continue

        file_obj = s3.get_object(Bucket=bucket_name, Key=key)
        file_content = file_obj["Body"].read().decode("utf-8")

        try:
            data = json.loads(file_content)
            all_data.append(data)
        except json.JSONDecodeError:
            print(f"⚠️ Fichier non JSON valide: {key}")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"data": data}),
    }
