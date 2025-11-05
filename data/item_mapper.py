"""
Item ID to Name Mapper
Uses Riot's Data Dragon API to map item IDs to readable names
"""

import requests
import json
from typing import Dict, Optional
from functools import lru_cache


class ItemMapper:
    """Maps item IDs to item names using Riot's Data Dragon"""
    
    def __init__(self, version: str = "latest", language: str = "en_US"):
        """
        Initialize item mapper
        
        Args:
            version: Patch version (e.g., "13.24.1" or "latest")
            language: Language code (e.g., "en_US", "ko_KR", "fr_FR")
        """
        self.version = version
        self.language = language
        self.items_cache = None
        self._load_items()
    
    def _load_items(self):
        """Load item data from Data Dragon"""
        try:
            # Get latest version if needed
            if self.version == "latest":
                versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
                versions = requests.get(versions_url).json()
                self.version = versions[0]
            
            # Fetch item data
            items_url = f"https://ddragon.leagueoflegends.com/cdn/{self.version}/data/{self.language}/item.json"
            response = requests.get(items_url)
            response.raise_for_status()
            
            data = response.json()
            self.items_cache = data['data']
            print(f"✓ Loaded {len(self.items_cache)} items from patch {self.version}")
            
        except Exception as e:
            print(f"Warning: Could not load item data: {e}")
            self.items_cache = {}
    
    def get_item_name(self, item_id: int) -> str:
        """
        Get item name from ID
        
        Args:
            item_id: Item ID
        
        Returns:
            Item name or "Unknown Item (ID)" if not found
        """
        if self.items_cache is None:
            return f"Unknown Item ({item_id})"
        
        item_data = self.items_cache.get(str(item_id))
        if item_data:
            return item_data['name']
        
        return f"Unknown Item ({item_id})"
    
    def get_build_names(self, item_ids: list) -> list:
        """
        Convert list of item IDs to names
        
        Args:
            item_ids: List of item IDs
        
        Returns:
            List of item names
        """
        return [self.get_item_name(item_id) for item_id in item_ids]
    
    def format_build(self, item_ids: list) -> str:
        """
        Format build as readable string
        
        Args:
            item_ids: List of item IDs
        
        Returns:
            Formatted string like "Item1, Item2, Item3"
        """
        names = self.get_build_names(item_ids)
        return ", ".join(names)


# Singleton instance for convenience
_mapper_instance = None

def get_item_mapper(version: str = "latest", language: str = "en_US") -> ItemMapper:
    """Get or create singleton ItemMapper instance"""
    global _mapper_instance
    if _mapper_instance is None:
        _mapper_instance = ItemMapper(version, language)
    return _mapper_instance


def map_item_id(item_id: int) -> str:
    """Quick helper to map single item ID"""
    mapper = get_item_mapper()
    return mapper.get_item_name(item_id)


def map_build(item_ids: list) -> list:
    """Quick helper to map build"""
    mapper = get_item_mapper()
    return mapper.get_build_names(item_ids)


# Example usage
if __name__ == "__main__":
    print("Item Mapper Test\n")
    
    # Initialize mapper
    mapper = ItemMapper()
    
    # Test some common items
    test_items = [
        3031,  # Infinity Edge
        3006,  # Berserker's Greaves
        3094,  # Rapid Firecannon
        3087,  # Statikk Shiv
        3036,  # Lord Dominik's Regards
        3139,  # Mercurial Scimitar
    ]
    
    print("Item ID → Name Mapping:")
    for item_id in test_items:
        print(f"  {item_id}: {mapper.get_item_name(item_id)}")
    
    print(f"\nFull Build: {mapper.format_build(test_items)}")