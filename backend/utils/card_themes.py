"""
Card theme configuration and mapping logic.
Maps stat categories to visual themes with artwork, colors, and styling.
"""

from typing import Dict, Optional
from backend.models.stat_card import CardCategory, CardTheme, CardRarity


# Theme presets for each category
CATEGORY_THEMES: Dict[CardCategory, Dict] = {
    CardCategory.CHAMPION_MASTERY: {
        "background_color": "#c77dff",
        "accent_color": "#9d4edd",
        "description": "Champion splash art with mastery stats",
    },
    CardCategory.FUNNY: {
        "background_color": "#ff6b6b",
        "accent_color": "#ee5a6f",
        "description": "Teemo demon theme for humorous/death stats",
    },
    CardCategory.SURVIVAL: {
        "background_color": "#38b000",
        "accent_color": "#2d9200",
        "description": "Warmog's Armor theme for health/survival stats",
    },
    CardCategory.MOVEMENT: {
        "background_color": "#4cc9f0",
        "accent_color": "#3a86ff",
        "description": "Ghost summoner spell theme for movement stats",
    },
    CardCategory.GEOGRAPHY: {
        "background_color": "#8d99ae",
        "accent_color": "#6c757d",
        "description": "Rift terrain/golem theme for map control stats",
    },
    CardCategory.MILESTONE: {
        "background_color": "#ffd60a",
        "accent_color": "#fca311",
        "description": "Trophy/achievement theme for milestones",
    },
    CardCategory.SOCIAL: {
        "background_color": "#7209b7",
        "accent_color": "#560bad",
        "description": "Team/friends theme for social comparisons",
    },
    CardCategory.GROWTH: {
        "background_color": "#06ffa5",
        "accent_color": "#00d084",
        "description": "Progress chart theme for improvement stats",
    },
}


# Artwork URL patterns (will be populated with actual URLs)
ARTWORK_TEMPLATES = {
    # Champion splash arts from Data Dragon
    "champion_splash": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion_name}_0.jpg",
    "champion_icon": "https://ddragon.leagueoflegends.com/cdn/14.1.1/img/champion/{champion_name}.png",

    # Item images
    "warmogs": "https://ddragon.leagueoflegends.com/cdn/14.1.1/img/item/3083.png",

    # Summoner spell images
    "ghost": "https://ddragon.leagueoflegends.com/cdn/14.1.1/img/spell/SummonerHaste.png",
    "flash": "https://ddragon.leagueoflegends.com/cdn/14.1.1/img/spell/SummonerFlash.png",

    # Generic assets (to be replaced with actual League assets)
    "teemo_demon": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Teemo_0.jpg",
    "rift_herald": "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/content/src/leagueclient/gamemodeassets/gamemodex/img/icon-herald.png",
    "achievement_trophy": "https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-profiles/global/default/icon-achievement.png",
}


def get_champion_artwork(champion_name: str, art_type: str = "splash") -> str:
    """
    Get artwork URL for a champion.

    Args:
        champion_name: Champion name (e.g., "Ahri", "LeeSin")
        art_type: "splash" or "icon"

    Returns:
        URL to the artwork
    """
    template_key = f"champion_{art_type}"
    if template_key in ARTWORK_TEMPLATES:
        return ARTWORK_TEMPLATES[template_key].format(champion_name=champion_name)
    return ARTWORK_TEMPLATES["champion_splash"].format(champion_name=champion_name)


def create_card_theme(
    category: CardCategory,
    artwork_url: Optional[str] = None,
    custom_colors: Optional[Dict[str, str]] = None
) -> CardTheme:
    """
    Create a CardTheme based on category with optional customization.

    Args:
        category: The card category
        artwork_url: Optional custom artwork URL
        custom_colors: Optional dict with 'background_color' and/or 'accent_color'

    Returns:
        CardTheme object
    """
    base_theme = CATEGORY_THEMES[category]

    # Use custom colors if provided, otherwise use defaults
    background = custom_colors.get("background_color") if custom_colors else base_theme["background_color"]
    accent = custom_colors.get("accent_color") if custom_colors else base_theme["accent_color"]

    # Default artwork based on category
    if artwork_url is None:
        artwork_url = _get_default_artwork(category)

    return CardTheme(
        artwork_url=artwork_url,
        background_color=background,
        accent_color=accent
    )


def _get_default_artwork(category: CardCategory) -> str:
    """Get default artwork URL for a category"""
    artwork_map = {
        CardCategory.CHAMPION_MASTERY: ARTWORK_TEMPLATES["champion_icon"].format(champion_name="Ahri"),
        CardCategory.FUNNY: ARTWORK_TEMPLATES["teemo_demon"],
        CardCategory.SURVIVAL: ARTWORK_TEMPLATES["warmogs"],
        CardCategory.MOVEMENT: ARTWORK_TEMPLATES["ghost"],
        CardCategory.GEOGRAPHY: ARTWORK_TEMPLATES["rift_herald"],
        CardCategory.MILESTONE: ARTWORK_TEMPLATES["achievement_trophy"],
        CardCategory.SOCIAL: ARTWORK_TEMPLATES["champion_icon"].format(champion_name="Braum"),
        CardCategory.GROWTH: ARTWORK_TEMPLATES["achievement_trophy"],
    }
    return artwork_map.get(category, "")


def determine_card_rarity(value: float, thresholds: Dict[str, float]) -> CardRarity:
    """
    Determine card rarity based on a value and thresholds.

    Args:
        value: The numeric value to evaluate
        thresholds: Dict with keys 'rare', 'epic', 'legendary' and their threshold values

    Returns:
        CardRarity enum value

    Example:
        >>> determine_card_rarity(150, {'rare': 100, 'epic': 200, 'legendary': 300})
        CardRarity.RARE
    """
    if value >= thresholds.get("legendary", float("inf")):
        return CardRarity.LEGENDARY
    elif value >= thresholds.get("epic", float("inf")):
        return CardRarity.EPIC
    elif value >= thresholds.get("rare", float("inf")):
        return CardRarity.RARE
    else:
        return CardRarity.COMMON


# Example rarity thresholds for common stats
RARITY_THRESHOLDS = {
    "games_played": {
        "rare": 100,
        "epic": 300,
        "legendary": 500,
    },
    "win_rate": {
        "rare": 0.55,
        "epic": 0.60,
        "legendary": 0.70,
    },
    "kda": {
        "rare": 3.0,
        "epic": 4.0,
        "legendary": 5.0,
    },
    "penta_kills": {
        "rare": 1,
        "epic": 3,
        "legendary": 5,
    },
    "vision_score_per_min": {
        "rare": 1.5,
        "epic": 2.0,
        "legendary": 2.5,
    },
}
