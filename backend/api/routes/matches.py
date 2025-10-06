"""
API routes for match data.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List

router = APIRouter()


@router.get("/{puuid}")
async def get_match_history(
    puuid: str,
    start: int = Query(0, ge=0),
    count: int = Query(20, ge=1, le=100)
):
    """Get match history for a player"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/match/{match_id}")
async def get_match(match_id: str):
    """Get detailed information about a specific match"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/{puuid}/sync")
async def sync_matches(puuid: str):
    """Sync latest matches from Riot API"""
    raise HTTPException(status_code=501, detail="Not implemented yet")
