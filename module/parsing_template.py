
from datetime import datetime

def parse_mastery(mastery_json, champion_mapping=None):
    """
    """
    parsed = {
        "puuid": mastery_json.get("puuid"),
        "champion": mastery_json.get("championId"),
        "championLevel": mastery_json.get("championLevel"),
        "championPoints": mastery_json.get("championPoints"),
        "lastPlayTime": datetime.utcfromtimestamp(mastery_json.get("lastPlayTime")/1000).strftime("%Y-%m-%d %H:%M:%S"),
        "pointsSinceLastLevel": mastery_json.get("championPointsSinceLastLevel"),
        "pointsUntilNextLevel": mastery_json.get("championPointsUntilNextLevel"),
        "tokensEarned": mastery_json.get("tokensEarned"),
        "markRequiredForNextLevel": mastery_json.get("markRequiredForNextLevel"),
        "seasonMilestone": mastery_json.get("championSeasonMilestone"),
    }
    return parsed


def parse_summoner(summoner_json):
    """
    """
    parsed_summoner = {
        "puuid": summoner_json.get("puuid"),
        "profileIconId": summoner_json.get("profileIconId"),
        "revisionDate": summoner_json.get("revisionDate"),
        "summonerLevel": summoner_json.get("summonerLevel"),

    }
    return parsed_summoner

def parse_league(league_json):
    """
    """
    parsed_league = []
    for queueType in league_json:

        parsed_league.append({
            "puuid": league_json.get("puuid"),
            "leagueId": league_json.get("leagueId"),
            "queueType": league_json.get("queueType"),
            "tier": league_json.get("tier"),
            "rank": league_json.get("rank"),
            "leaguePoints": league_json.get("leaguePoints"),
            "wins": league_json.get("wins"),
            "losses": league_json.get("losses"),
            "veteran": league_json.get("veteran"),
            "inactive": league_json.get("inactive"),
            "freshBlood": league_json.get("freshBlood"),
            "hotStreak": league_json.get("hotStreak")
        })
        
    return parsed_league