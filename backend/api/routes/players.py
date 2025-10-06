"""
API routes for player data.
"""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/{puuid}")
async def get_player(puuid: str):
    """Get player profile information"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/by-name/{region}/{summoner_name}")
async def get_player_by_name(region: str, summoner_name: str):
    """Get player by summoner name"""
    raise HTTPException(status_code=501, detail="Not implemented yet")
