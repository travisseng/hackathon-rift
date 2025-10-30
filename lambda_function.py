
from get_account_data import main


def lambda_handler(event, context):
    # Input Example : event = {"region": "europe", "gamename": "reive", "gametag": "euw"}
    
    region = event.get("region")
    gamename = event.get("gamename")
    gametag = event.get("gametag")
    main(region, gamename, gametag)

