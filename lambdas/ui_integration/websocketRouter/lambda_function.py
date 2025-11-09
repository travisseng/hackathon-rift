import boto3
import json
import os

lambda_client = boto3.client("lambda")


def lambda_handler(event, context):

    body = json.loads(event.get("body", "{}"))

    
    connection_id = event["requestContext"]["connectionId"]
    region = body.get("region")
    gamename = body.get("gamename")
    gametag = body.get("gametag")
    action = body.get("action", "process")

    
    lambda_client.invoke(
        FunctionName="league_api_call", 
        InvocationType="Event",
        Payload=json.dumps(
            {
                "connectionId": connection_id,
                "region": region,
                "gamename": gamename,
                "gametag": gametag,
                "action": action,
            }
        ),
    )

    return {"statusCode": 200, "body": f"Started processing {str(event)}"}
