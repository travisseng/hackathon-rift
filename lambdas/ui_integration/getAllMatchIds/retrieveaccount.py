import requests


def get_routing_value(type_region):
    """
    Map platform region to routing value for Riot API
    """
    routing_map = {
        "na1": "americas",
        "br1": "americas",
        "la1": "americas",
        "la2": "americas",
        "euw1": "europe",
        "eun1": "europe",
        "tr1": "europe",
        "ru": "europe",
        "kr": "asia",
        "jp1": "asia",
        "oc1": "sea",
        "ph2": "sea",
        "sg2": "sea",
        "th2": "sea",
        "tw2": "sea",
        "vn2": "sea",
    }
    return routing_map.get(type_region, "americas")


def get_account_riotid(type_region, type_gamename, type_gametag, api_key):
    response = requests.get(
        f"https://{get_routing_value(type_region)}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{type_gamename}/{type_gametag}?api_key={api_key}"
    )
    riot_encrypted_puuid = response.json().get("puuid", "")
    riot_gamename = response.json().get("gameName", "")
    riot_gametag = response.json().get("tagLine", "")
    return riot_encrypted_puuid, riot_gamename, riot_gametag
