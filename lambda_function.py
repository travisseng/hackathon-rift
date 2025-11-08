from get_account_data import main


def lambda_handler(event, context):
    # Exemple d'input : {
#   "region": "na1",
#   "gamename": "na dogbilel",
#   "gametag": "na1"
# }

    region = event.get("region")
    gamename = event.get("gamename")
    gametag = event.get("gametag")
    main(region, gamename, gametag)

