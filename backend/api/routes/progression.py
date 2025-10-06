"""
API routes for player progression tracking and visualization.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from backend.models.progression import (
    PlayerProgression,
    ProgressionTimeSeries,
    ProgressionMetric,
    SkillRadar,
    ChampionProgression
)

router = APIRouter()


@router.get("/{puuid}", response_model=PlayerProgression)
async def get_player_progression(
    puuid: str,
    time_period: str = Query("all", regex="^(week|month|season|year|all)$")
):
    """
    Get complete progression data for a player.

    Args:
        puuid: Player UUID
        time_period: Time window for progression data
    """
    # TODO: Implement progression data retrieval
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{puuid}/metrics/{metric}", response_model=ProgressionTimeSeries)
async def get_metric_timeseries(
    puuid: str,
    metric: ProgressionMetric,
    aggregation: str = Query("weekly", regex="^(daily|weekly|monthly)$")
):
    """
    Get time series data for a specific metric.

    Args:
        puuid: Player UUID
        metric: The metric to retrieve
        aggregation: How to aggregate the data points
    """
    # TODO: Implement metric time series generation
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{puuid}/skill-radar", response_model=SkillRadar)
async def get_skill_radar(puuid: str, include_comparison: bool = False):
    """
    Get current skill radar chart data.

    Args:
        puuid: Player UUID
        include_comparison: Include percentile rank vs similar players
    """
    # TODO: Implement skill radar calculation
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{puuid}/champions", response_model=List[ChampionProgression])
async def get_champion_progression(
    puuid: str,
    min_games: int = Query(5, ge=1),
    sort_by: str = Query("games", regex="^(games|winrate|improvement)$")
):
    """
    Get progression data for all champions played.

    Args:
        puuid: Player UUID
        min_games: Minimum games required to include a champion
        sort_by: How to sort the results
    """
    # TODO: Implement champion-specific progression
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/{puuid}/analyze")
async def analyze_progression(puuid: str):
    """
    Trigger AI analysis of player progression.

    This will:
    1. Calculate all time series metrics
    2. Identify trends and patterns
    3. Generate insights about improvements/declines
    4. Update skill radar
    """
    # TODO: Implement progression analysis pipeline
    raise HTTPException(status_code=501, detail="Not implemented yet")
