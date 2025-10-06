from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ParticipantStats(BaseModel):
    """Stats for a single participant in a match"""
    puuid: str
    champion_id: int
    champion_name: str

    # Core stats
    kills: int
    deaths: int
    assists: int

    # Combat stats
    total_damage_dealt_to_champions: int
    total_damage_taken: int
    total_heal: int
    gold_earned: int

    # Map presence
    total_minions_killed: int
    neutral_minions_killed: int
    vision_score: int
    wards_placed: int
    wards_killed: int

    # Movement & positioning
    total_time_cc_dealt: int
    time_ccing_others: int
    total_distance_traveled: Optional[int] = None

    # Game impact
    damage_self_mitigated: int
    turret_kills: int
    inhibitor_kills: int

    # Position data
    position: Optional[str] = None  # TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY
    team_position: Optional[str] = None

    # Items
    items: List[int] = Field(default_factory=list)

    # Outcome
    win: bool
    game_ended_in_early_surrender: bool = False

    # Timing
    longest_time_spent_living: int = 0
    total_time_spent_dead: int = 0

    # Additional metadata
    summoner_spells: List[int] = Field(default_factory=list)
    perks: Dict[str, Any] = Field(default_factory=dict)


class MatchInfo(BaseModel):
    """General match information"""
    match_id: str
    game_creation: int  # Unix timestamp
    game_duration: int  # Seconds
    game_mode: str
    game_type: str
    queue_id: int
    map_id: int
    platform_id: str

    # Parsed datetime
    @property
    def game_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.game_creation / 1000)


class Match(BaseModel):
    """Complete match data"""
    metadata: Dict[str, Any]
    info: MatchInfo
    participants: List[ParticipantStats]

    def get_participant_by_puuid(self, puuid: str) -> Optional[ParticipantStats]:
        """Get a specific participant's stats"""
        for participant in self.participants:
            if participant.puuid == puuid:
                return participant
        return None


class PlayerMatchHistory(BaseModel):
    """Aggregated match history for a player"""
    puuid: str
    summoner_name: str
    matches: List[Match] = Field(default_factory=list)
    total_matches: int = 0
    time_period: Dict[str, str] = Field(default_factory=dict)  # start_date, end_date

    def add_match(self, match: Match):
        """Add a match to the history"""
        self.matches.append(match)
        self.total_matches += 1
