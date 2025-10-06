"""
API routes for statistical analysis.
"""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/{puuid}/summary")
async def get_stats_summary(puuid: str):
    """Get summary statistics for a player"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{puuid}/champions")
async def get_champion_stats(puuid: str):
    """Get per-champion statistics"""
    raise HTTPException(status_code=501, detail="Not implemented yet")
