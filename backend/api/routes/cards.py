"""
API routes for stat cards generation and retrieval.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from backend.models.stat_card import CardDeck, StatCard

router = APIRouter()


@router.get("/{puuid}/primary", response_model=CardDeck)
async def get_primary_cards(puuid: str):
    """
    Get the primary set of 3 stat cards for a player.

    This set contains the most impressive or notable stats.
    """
    # TODO: Implement card generation logic
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{puuid}/secondary", response_model=CardDeck)
async def get_secondary_cards(puuid: str):
    """
    Get the secondary set of 3 stat cards for a player (reroll set).

    This set contains alternative interesting stats.
    """
    # TODO: Implement card generation logic
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/{puuid}/generate")
async def generate_all_cards(puuid: str, force_refresh: bool = False):
    """
    Generate all stat cards for a player.

    Args:
        puuid: Player UUID
        force_refresh: Force regeneration even if cards exist

    Returns:
        Status of card generation
    """
    # TODO: Implement full card generation pipeline
    # 1. Fetch match history
    # 2. Calculate all stats
    # 3. Generate cards with themes
    # 4. Use AI to enhance narratives
    # 5. Store cards
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{puuid}/all", response_model=List[StatCard])
async def get_all_cards(puuid: str):
    """
    Get all generated cards for a player (not just the 3+3 shown).

    Useful for debugging or advanced views.
    """
    # TODO: Implement
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/{card_id}/share")
async def create_shareable_card(card_id: str):
    """
    Generate a shareable image for a specific card.

    Returns:
        URL to the generated image
    """
    # TODO: Implement card-to-image generation
    # Could use PIL/Pillow or a service like Cloudinary
    raise HTTPException(status_code=501, detail="Not implemented yet")
