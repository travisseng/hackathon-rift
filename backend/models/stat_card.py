from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class CardCategory(str, Enum):
    """Categories for stat cards with associated themes"""
    CHAMPION_MASTERY = "champion_mastery"
    FUNNY = "funny"
    SURVIVAL = "survival"
    MOVEMENT = "movement"
    GEOGRAPHY = "geography"
    MILESTONE = "milestone"
    SOCIAL = "social"
    GROWTH = "growth"


class CardRarity(str, Enum):
    """Rarity levels for cards (affects presentation)"""
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class CardTheme(BaseModel):
    """Visual theme for a stat card"""
    artwork_url: str = Field(..., description="URL to main artwork/image")
    background_color: str = Field(..., description="Hex color for background")
    accent_color: str = Field(..., description="Hex color for accents")
    icon_url: Optional[str] = Field(None, description="Optional icon URL")

    class Config:
        json_schema_extra = {
            "example": {
                "artwork_url": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ahri_0.jpg",
                "background_color": "#c77dff",
                "accent_color": "#9d4edd",
                "icon_url": "https://ddragon.leagueoflegends.com/cdn/13.1.1/img/champion/Ahri.png"
            }
        }


class StatCard(BaseModel):
    """Represents a single stat card to be displayed"""
    id: str = Field(..., description="Unique identifier for this card")
    category: CardCategory = Field(..., description="Category determining theme")
    title: str = Field(..., description="Main title of the card")
    value: str = Field(..., description="Primary stat value (formatted)")
    subtitle: Optional[str] = Field(None, description="Supporting text or context")
    theme: CardTheme = Field(..., description="Visual theme configuration")
    rarity: CardRarity = Field(CardRarity.COMMON, description="Rarity level")
    shareable: bool = Field(True, description="Whether card can be shared")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional data")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "card_most_played_champion_ahri",
                "category": "champion_mastery",
                "title": "Your Most Played Champion",
                "value": "127 games on Ahri",
                "subtitle": "That's 42 hours of charm spam!",
                "theme": {
                    "artwork_url": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ahri_0.jpg",
                    "background_color": "#c77dff",
                    "accent_color": "#9d4edd"
                },
                "rarity": "epic",
                "shareable": True,
                "metadata": {
                    "champion_id": "103",
                    "total_games": 127,
                    "win_rate": 0.548
                }
            }
        }


class CardDeck(BaseModel):
    """A collection of stat cards (primary or secondary set)"""
    player_id: str = Field(..., description="Player identifier (PUUID)")
    deck_type: str = Field(..., description="'primary' or 'secondary'")
    cards: list[StatCard] = Field(..., min_length=3, max_length=3, description="Exactly 3 cards")
    generated_at: str = Field(..., description="ISO timestamp of generation")

    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "abc123-puuid",
                "deck_type": "primary",
                "cards": [],  # Would contain 3 StatCard objects
                "generated_at": "2025-01-15T10:30:00Z"
            }
        }
