from get_account_data import main
import json


def lambda_handler(event, context):
    """
    AWS Lambda handler to process a request and trigger the main workflow.

    Expects `event` to contain:
        - region (str): game region, e.g., "euw1"
        - gamename (str): summoner's game name
        - gametag (str): summoner's tag/region suffix
        - ranked_type (str): "solo", "flex", or "solo_and_flex"
        - connectionId (str, optional)

    Extracts parameters from the event and calls `main(region, gamename, gametag, query_params, ranked_type)`.
    """
    query_params = event.get("queryStringParameters", {})
    region = event.get("region")
    gamename = event.get("gamename")
    gametag = event.get("gametag")
    ranked_type = event.get("ranked_type")
    query_params = {"connectionId": event.get("connectionId")}

    main(region, gamename, gametag, query_params, ranked_type)
