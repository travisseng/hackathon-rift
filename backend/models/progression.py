from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class ProgressionMetric(str, Enum):
    """Key metrics to track over time"""
    KDA = "kda"
    VISION_SCORE = "vision_score"
    CS_PER_MIN = "cs_per_min"
    DAMAGE_PER_MIN = "damage_per_min"
    GOLD_PER_MIN = "gold_per_min"
    KILL_PARTICIPATION = "kill_participation"
    FIRST_BLOOD_RATE = "first_blood_rate"
    EARLY_GAME_STRENGTH = "early_game_strength"
    LATE_GAME_STRENGTH = "late_game_strength"
    OBJECTIVE_CONTROL = "objective_control"
    WIN_RATE = "win_rate"


class DataPoint(BaseModel):
    """Single data point in a time series"""
    timestamp: str  # ISO format
    value: float
    match_count: int = Field(..., description="Number of matches included in this point")


class ProgressionTimeSeries(BaseModel):
    """Time series for a specific metric"""
    metric: ProgressionMetric
    data_points: List[DataPoint]
    aggregation_period: str = Field(..., description="'daily', 'weekly', 'monthly'")
    trend: str = Field(..., description="'improving', 'declining', 'stable'")
    change_percentage: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "metric": "kda",
                "data_points": [
                    {"timestamp": "2024-01-01", "value": 2.5, "match_count": 10},
                    {"timestamp": "2024-02-01", "value": 2.8, "match_count": 15}
                ],
                "aggregation_period": "monthly",
                "trend": "improving",
                "change_percentage": 12.0
            }
        }


class SkillRadar(BaseModel):
    """Radar chart data for player skills"""
    combat: float = Field(..., ge=0, le=100, description="Combat effectiveness")
    vision: float = Field(..., ge=0, le=100, description="Vision control")
    farming: float = Field(..., ge=0, le=100, description="CS and gold generation")
    objectives: float = Field(..., ge=0, le=100, description="Objective control")
    positioning: float = Field(..., ge=0, le=100, description="Positioning and survival")
    teamfight: float = Field(..., ge=0, le=100, description="Teamfight contribution")

    # Historical comparison
    previous_period: Optional[Dict[str, float]] = None
    percentile_rank: Optional[Dict[str, float]] = None  # vs similar rank players


class MilestoneAchievement(BaseModel):
    """Significant achievements or milestones"""
    id: str
    title: str
    description: str
    achieved_at: str  # ISO timestamp
    match_id: Optional[str] = None
    icon_url: Optional[str] = None
    rarity: str = Field(..., description="'common', 'rare', 'epic', 'legendary'")


class ChampionProgression(BaseModel):
    """Progression for a specific champion"""
    champion_id: int
    champion_name: str
    total_games: int
    win_rate: float
    avg_kda: float
    mastery_level: int

    # Progression metrics
    first_10_games_wr: float
    recent_10_games_wr: float
    improvement_trend: str  # 'improving', 'declining', 'stable'

    # Performance breakdown
    skill_ratings: SkillRadar
    best_matchups: List[str] = Field(default_factory=list)
    worst_matchups: List[str] = Field(default_factory=list)


class PlayerProgression(BaseModel):
    """Complete progression data for a player"""
    puuid: str
    summoner_name: str
    last_updated: str

    # Time series data
    metrics: List[ProgressionTimeSeries]

    # Current skill assessment
    current_skill_radar: SkillRadar

    # Champion-specific progression
    champion_progression: List[ChampionProgression]

    # Achievements
    milestones: List[MilestoneAchievement] = Field(default_factory=list)

    # Improvement insights
    biggest_improvements: List[str] = Field(default_factory=list)
    areas_for_growth: List[str] = Field(default_factory=list)

    # Rank tracking
    rank_history: List[Dict[str, str]] = Field(default_factory=list)
    # Format: [{"timestamp": "2024-01-01", "rank": "GOLD_II", "lp": 45}]
