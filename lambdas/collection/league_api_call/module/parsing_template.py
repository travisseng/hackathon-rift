from datetime import datetime
import pandas as pd


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


def parse_mastery(mastery_json, champion_mapping=None):
    """ """
    parsed = {
        "puuid": mastery_json.get("puuid"),
        "champion": mastery_json.get("championId"),
        "championLevel": mastery_json.get("championLevel"),
        "championPoints": mastery_json.get("championPoints"),
        "lastPlayTime": datetime.utcfromtimestamp(
            mastery_json.get("lastPlayTime") / 1000
        ).strftime("%Y-%m-%d %H:%M:%S"),
        "pointsSinceLastLevel": mastery_json.get("championPointsSinceLastLevel"),
        "pointsUntilNextLevel": mastery_json.get("championPointsUntilNextLevel"),
        "tokensEarned": mastery_json.get("tokensEarned"),
        "markRequiredForNextLevel": mastery_json.get("markRequiredForNextLevel"),
        "seasonMilestone": mastery_json.get("championSeasonMilestone"),
    }
    return parsed


def get_stats_key():
    stats_keys = {
        "championName": "Champion",
        "teamPosition": "Team Position",
        "individualPosition": "Individual Position",
        "totalTimeSpentDead": "Total Time Dead",
        "kills": "Kills",
        "deaths": "Deaths",
        "assists": "Assists",
        "totalMinionsKilled": "Total Minions Killed",
        "neutralMinionsKilled": "Neutral Minions Killed",
        "totalDamageDealt": "Total Damage Dealt",
        "totalDamageDealtToChampions": "Damage to Champions",
        "goldEarned": "Gold Earned",
        "totalDamageTaken": "Damage Taken",
        "visionScore": "Vision Score",
        "wardsPlaced": "Wards Placed",
        "wardsKilled": "Wards Killed",
        "challenges.kda": "KDA",
        "pentaKills": "Penta Kills",
        "quadraKills": "Quadra Kills",
        "tripleKills": "Triple Kills",
        "skillshotsHit": "Skillshots Hit",
        "firstBloodKill": "First Blood Kill",
        "challenges.dragonTakedowns": "Dragon Takedowns",
        "challenges.teamBaronKills": "Team Baron Kills",
        "challenges.epicMonsterSteals": "Epic Monster Steals",
    }
    return stats_keys


def parse_summoner(summoner_json):
    """ """
    parsed_summoner = {
        "puuid": summoner_json.get("puuid"),
        "profileIconId": summoner_json.get("profileIconId"),
        "revisionDate": summoner_json.get("revisionDate"),
        "summonerLevel": summoner_json.get("summonerLevel"),
    }
    return parsed_summoner


def parse_league(league_json):
    """ """
    parsed_league = []
    parsed_league.append(
        {
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
            "hotStreak": league_json.get("hotStreak"),
        }
    )

    return parsed_league


def get_runes_from_id():
    runes_dict = {
        "style": {
            8100: "Domination",
            8300: "Inspiration",
            8000: "Precision",
            8400: "Resolve",
            8200: "Sorcery",
        },
        "perk": {
            8112: "Electrocute",
            8128: "Dark Harvest",
            9923: "Hail of Blades",
            8126: "Cheap Shot",
            8139: "Taste of Blood",
            8143: "Sudden Impact",
            8137: "Sixth Sense",
            8140: "Grisly Mementos",
            8141: "Deep Ward",
            8135: "Treasure Hunter",
            8105: "Relentless Hunter",
            8106: "Ultimate Hunter",
            8351: "Glacial Augment",
            8360: "Unsealed Spellbook",
            8369: "First Strike",
            8306: "Hextech Flashtraption",
            8304: "Magical Footwear",
            8321: "Cash Back",
            8313: "Triple Tonic",
            8352: "Time Warp Tonic",
            8345: "Biscuit Delivery",
            8347: "Cosmic Insight",
            8410: "Approach Velocity",
            8316: "Jack Of All Trades",
            8005: "Press the Attack",
            8008: "Lethal Tempo",
            8021: "Fleet Footwork",
            8010: "Conqueror",
            9101: "Absorb Life",
            9111: "Triumph",
            8009: "Presence of Mind",
            9104: "Legend: Alacrity",
            9105: "Legend: Haste",
            9103: "Legend: Bloodline",
            8014: "Coup de Grace",
            8017: "Cut Down",
            8299: "Last Stand",
            8437: "Grasp of the Undying",
            8439: "Aftershock",
            8465: "Guardian",
            8446: "Demolish",
            8463: "Font of Life",
            8401: "Shield Bash",
            8429: "Conditioning",
            8444: "Second Wind",
            8473: "Bone Plating",
            8451: "Overgrowth",
            8453: "Revitalize",
            8242: "Unflinching",
            8214: "Summon Aery",
            8229: "Arcane Comet",
            8230: "Phase Rush",
            8224: "Axiom Arcanist",
            8226: "Manaflow Band",
            8275: "Nimbus Cloak",
            8210: "Transcendence",
            8234: "Celerity",
            8233: "Absolute Focus",
            8237: "Scorch",
            8232: "Waterwalking",
            8236: "Gathering Storm",
        },
    }
    return runes_dict


def get_data_player_infos(match_data, player, items_data, runes):
    def get_item_name(item_id, items_data):
        if not item_id:
            return None
        return items_data.get("data", None).get(str(item_id), {}).get("name", None)

    data_player_json = {
        "matchId": match_data.get("metadata", {}).get("matchId"),
        "gameCreation": match_data.get("info", {}).get("gameCreation"),
        "gameDuration": match_data.get("info", {}).get("gameDuration"),
        "gameMode": match_data.get("info", {}).get("gameMode"),
        "queueId": match_data.get("info", {}).get("queueId"),
        "queueType": {420: "5v5 Ranked Solo games", 440: "5v5 Ranked Flex games"}.get(
            match_data.get("info", {}).get("queueId"), "Other"
        ),
        "champion_name": player.get("championName"),
        "champion_id": player.get("championId"),
        "teamPosition": player.get("teamPosition"),
        "individualPosition": player.get("individualPosition"),
        "player": player.get("riotIdGameName"),
        "death_time": player.get("totalTimeSpentDead"),
        "kills_amount": player.get("kills"),
        "deaths_amount": player.get("deaths"),
        "assists_amount": player.get("assists"),
        "total_minions_killed": player.get("totalMinionsKilled"),
        "neutralMinionsKilled": player.get("neutralMinionsKilled"),
        "cs_score": player.get("totalMinionsKilled")
        + player.get("neutralMinionsKilled"),
        "total_damage_dealt": player.get("totalDamageDealt"),
        "total_damage_to_champions": player.get("totalDamageDealtToChampions"),
        "goldEarned": player.get("goldEarned"),
        "totalDamageTaken": player.get("totalDamageTaken"),
        "win": player.get("win"),
        "items_0": get_item_name(player.get("item0"), items_data),
        "items_1": get_item_name(player.get("item1"), items_data),
        "items_2": get_item_name(player.get("item2"), items_data),
        "items_3": get_item_name(player.get("item3"), items_data),
        "items_4": get_item_name(player.get("item4"), items_data),
        "items_5": get_item_name(player.get("item5"), items_data),
        "items_6": get_item_name(player.get("item6"), items_data),
        "summoner1Id": player.get("summoner1Id"),
        "summoner2Id": player.get("summoner2Id"),
        "primaryStyle": player.get("perks", {}).get("styles", [{}])[0].get("style"),
        "primaryStyle_name": runes.get("style").get(
            player.get("perks", {}).get("styles", [{}])[0].get("style")
        ),
        "subStyle": player.get("perks", {}).get("styles", [{}])[1].get("style")
        if len(player.get("perks", {}).get("styles", [])) > 1
        else None,
        "subStyle_name": runes.get("style").get(
            player.get("perks", {}).get("styles", [{}])[1].get("style")
            if len(player.get("perks", {}).get("styles", [])) > 1
            else None
        ),
        "primaryPerk": player.get("perks", {})
        .get("styles", [{}])[0]
        .get("selections", [{}])[0]
        .get("perk"),
        "primaryPerk_name": runes.get("perk").get(
            player.get("perks", {})
            .get("styles", [{}])[0]
            .get("selections", [{}])[0]
            .get("perk")
        ),
        "pentakills": player.get("pentaKills"),
        "quadra_kills": player.get("quadraKills"),
        "triple_kills": player.get("tripleKills"),
        "skillshots_hit": player.get("skillshotsHit"),
        "first_blood_kill": player.get("firstBloodKill"),
        "dragon_takedowns": player.get("challenges", {}).get("dragonTakedowns"),
        "team_baron_kills": player.get("challenges", {}).get("teamBaronKills"),
        "visionScore": player.get("visionScore"),
        "wards_placed": player.get("wardsPlaced"),
        "wards_killed": player.get("wardsKilled"),
        "individual_position": player.get("individualPosition"),
        "kda": player.get("challenges", {}).get("kda"),
        "epic_monster_steals": player.get("challenges", {}).get("epicMonsterSteals"),
    }
    return data_player_json


def parse_summary_to_wrapped_up(df):
    """ """

    def format_time(seconds: int) -> str:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        return f"{days:02d} day(s) {hours:02d} hour(s) {minutes:02d} minute(s)"

    wrapped_up_json = {
        "game_duration": {
            "timespend": sum(df["gameDuration"]),
            "longest_game": format_time(max(df["gameDuration"])),
            "gameplayed": df.shape[0],
            "victory": {
                k: int(v) for k, v in df["win"].value_counts().to_dict().items()
            },
            "winrate": round(sum(df["win"]) / df.shape[0], 2),
            "timespend_hh_mm_ss": format_time(sum(df["gameDuration"])),
            "amount_played_year": pd.to_datetime(df["gameCreation"], unit="ms")
            .dt.strftime("%m/%y")
            .value_counts()
            .to_dict(),
            "tag_comment0": "Passionate",
            "comment0": f"You spent {format_time(sum(df['gameDuration']))} seconds through {(df.shape[0])} ranked games in the summoner's rift",
            "tag_comment2": "Rookie Explorer",
            "comment2": f"You’ve played {df.shape[0]} games for a total of {format_time(sum(df['gameDuration']))}. Still warming up, but hey — every minion slain counts!",
            "tag_comment3": "Ranked Grinder",
            "comment3": f"{df.shape[0]} games, {format_time(sum(df['gameDuration']))} on the Rift... You’re not just playing anymore — you’re on the grind. Respect the hustle!",
            "tag_comment1": "League Addict",
            "comment1": f"{df.shape[0]} games and {format_time(sum(df['gameDuration']))} spent in the Rift. Touch some grass? Nah — you’re too busy climbing ELO!",
        },
        "role_champs_played": {
            "most_played_champ": {
                k: int(v) for k, v in df["champion_name"].value_counts().head(3).items()
            },
            "most_played_role": {
                k: int(v) for k, v in df["teamPosition"].value_counts().head(3).items()
            },
        },
        "deaths_stats": {
            "count_dead": sum(df["deaths_amount"]),
            "count_dead_age": sum(df["deaths_amount"]) / df.shape[0],
            "time_dead": sum(df["death_time"]),
            "longest_death": int(max(df["death_time"])),
            "timespend_hh_mm_ss": format_time(sum(df["death_time"])),
            "tag_comment1": "Daltonian",
            "comment1": f"You saw in black and white {sum(df['deaths_amount'])} times",
            "tag_comment2": "Cinephile",
            "comment2": f"You saw the equivalent of {round(sum(df['death_time'])/5220,2)} Charlie Chaplin's movie in black and white",
        },
        "kills_assists_stats": {
            "kills": sum(df["kills_amount"]),
            "assists": sum(df["assists_amount"]),
            "firstbloodkills": sum(df["first_blood_kill"]),
            "triple_kills": sum(df["triple_kills"]),
            "quadra_kills": sum(df["quadra_kills"]),
            "penta_kills": sum(df["pentakills"]),
            "tag_comment1": "The Opportunist",
            "comment1": f"You’ve stacked {sum(df['assists_amount'])} assists — always there for your teammates... or just for the free KP?",
            "tag_comment2": "The Finisher",
            "comment2": f"{sum(df['kills_amount'])} kills and {sum(df['first_blood_kill'])} first bloods — you don’t wait for opportunities, you create them.",
            "tag_comment3": "The Showstopper",
            "comment3": f"{sum(df['triple_kills'])} triples, {sum(df['quadra_kills'])} quadras, and {sum(df['pentakills'])} pentas — you’re basically the highlight reel of your team.",
            "tag_comment4": "The Menace",
            "comment4": f"With {sum(df['kills_amount']) + sum(df['assists_amount'])} total contributions, you’ve been in nearly every fight. Enemy team probably reports you for 'trying too hard'.",
        },
        "metrics": {
            "kda_avg": round(sum(df["kda"]) / df.shape[0], 2),
            "sum_cs": sum(df["cs_score"]) / df.shape[0],
            "avg_cs_min": sum(df[df["teamPosition"] != "UTILITY"]["cs_score"])
            * 60
            / sum(df[df["teamPosition"] != "UTILITY"]["gameDuration"]),
            "goldEarned": sum(df["goldEarned"]),
            "goldEarned_avg": int(sum(df["goldEarned"]) / df.shape[0]),
            "total_damage_to_champions_avg": int(
                sum(df[df["teamPosition"] != "UTILITY"]["total_damage_to_champions"])
                / df.shape[0]
            ),
            "totalDamageTaken_avg": int(sum(df["totalDamageTaken"]) / df.shape[0]),
            "firstbloodkills": sum(df["first_blood_kill"]),
            "penta_kills": sum(df["pentakills"]),
            "tag_comment1": "The Economist",
            "comment1": f"An average of {int(sum(df['goldEarned'])/df.shape[0])} gold per game — that’s some serious coin. You could buy a full build… or at least one control ward.",
            "tag_comment2": "The Stat Machine",
            "comment2": f"Your average KDA is {round(sum(df['kda'])/df.shape[0],2)}. Clean plays, clutch survivals — you’re basically a walking League spreadsheet.",
            "tag_comment3": "The Damage Dealer",
            "comment3": f"With {int(sum(df['total_damage_to_champions'])/df.shape[0])} average damage per game, you’re clearly allergic to auto-attacking minions.",
            "tag_comment4": "The Farmer",
            "comment4": f"A steady {round(sum(df[df['teamPosition'] != 'UTILITY']['cs_score']) * 60 / sum(df[df['teamPosition'] != 'UTILITY']['gameDuration']),2)} CS/min — wave control on point. Lane kingdom secured.",
            "tag_comment5": "The Frontliner",
            "comment5": f"Taking {int(sum(df['totalDamageTaken'])/df.shape[0])} damage per game and still standing? That’s tank behavior. Respect the shield.",
        },
        "objectives": {
            "visionScore": sum(df["visionScore"]),
            "wards_placed": sum(df["wards_placed"]),
            "wards_killed": sum(df["wards_killed"]),
            "visionScore_avg": sum(df["visionScore"]) / df.shape[0],
            "wards_placed_avg": sum(df["wards_placed"]) / df.shape[0],
            "wards_killed_avg": sum(df["wards_killed"]) / df.shape[0],
            "dragon_takedowns": sum(df["dragon_takedowns"]),
            "team_baron_kills": sum(df["team_baron_kills"]),
            "epic_monster_steals": sum(df["wards_placed"]),
        },
        "synthese": {
            "gameplayed": df.shape[0],
            "victory": df["win"].value_counts().to_dict(),
            "winrate": round(sum(df["win"]) / df.shape[0], 2),
            "kda_avg": round(sum(df["kda"]) / df.shape[0], 2),
            "role_champs_played": {
                "most_played_champ": dict(df["champion_name"].value_counts()[0:3]),
                "most_played_role": dict(df["teamPosition"].value_counts()[0:3]),
            },
            "champion_pool": df["champion_name"].unique(),
            "champion_pool": len(df["champion_name"].unique()),
            "visionScore_avg": sum(df["visionScore"]) / df.shape[0],
            "timespend_hh_mm_ss": format_time(sum(df["death_time"])),
            "total_damage_to_champions_avg": int(
                sum(df["total_damage_to_champions"]) / df.shape[0]
            ),
            "amount_played_year": pd.to_datetime(df["gameCreation"], unit="ms")
            .dt.strftime("%B %Y")
            .value_counts()
            .to_dict(),
        },
    }
    return wrapped_up_json


def get_stats_mean():
    dict_stats_mean = {
        "matchId": "count",
        "win": "sum",
        "kda": "mean",
        "kills_amount": "mean",
        "deaths_amount": "mean",
        "assists_amount": "mean",
        "cs_total": "mean",
        "cs_per_min": "mean",
        "total_damage_to_champions": "mean",
        "goldEarned": "mean",
        "totalDamageTaken": "mean",
        "visionScore": "mean",
        "wards_placed": "mean",
        "wards_killed": "mean",
    }
    return dict_stats_mean
