```mermaid
erDiagram
    RIOT_API {
        string summoner_endpoint "/lol/summoner/v4/summoners/by-puuid/{riot_encrypted_puuid}"
        string league_endpoint "/lol/league/v4/entries/by-puuid/{riot_encrypted_puuid}"
        string champions_masteries_endpoint "/lol/champion-mastery/v4/champion-masteries/by-puuid/{riot_encrypted_puuid}"
        string games_history_endpoint "riot/account/v1/accounts/by-riot-id/{type_gamename}/{type_gametag}"
    }

    LEAGUE {
        string puuid "primary key"
        int profileIconId
        int revisionDate
        int summonerLevel
    }
    SUMMONER {
        int puuid "primary key"
        int leagueId
        int queueType
        int tier
        int rank
        int leaguePoints
        int wins
        int losses
        int veteran
        int inactive
        string freshBlood
        string hotStreak
    }
    CHAMPIONS_MASTERIES {
        string puuid "primary key"
        int champion
        int championLevel
        int championPoints
        string lastPlayTime
        string pointsSinceLastLevel
        int pointsUntilNextLevel
        int tokensEarned
        int markRequiredForNextLevel
        int markRequiredForNextLevel

    }

LEAGUE_OVERVIEW{
    int tobedefined
}

GAMES_HISTORY{
    int player
    int death_time
    int deaths_amount
    int kills_amount
    int total_damage_dealt
    int total_damage_to_champions
    int pentakills
    int quadra_kills
    int triple_kills
    int skillshots_hit
    int first_blood_kill
    int dragon_takedowns
    int team_baron_kills
    int total_minions_killed
    int wards_placed
    int wards_killed
    int individual_position
    int champion_name
    int kda
    int epic_monster_steals
}

    RIOT_API ||--|{ CHAMPIONS_MASTERIES : champions_masteries_endpoint
    RIOT_API ||--|{ LEAGUE : league_endpoint
    RIOT_API ||--|{ SUMMONER : summoner_endpoint
    RIOT_API ||--|{ GAMES_HISTORY : games_history_endpoint

    CHAMPIONS_MASTERIES ||--|{ LEAGUE_OVERVIEW : merge
    LEAGUE||--|{ LEAGUE_OVERVIEW : merge
    SUMMONER||--|{ LEAGUE_OVERVIEW : merge
    GAMES_HISTORY ||--|{ LEAGUE_OVERVIEW : merge
```