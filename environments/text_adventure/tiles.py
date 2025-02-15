from dataclasses import dataclass
from typing import List

@dataclass
class TextAdventureTile:
    symbol: str
    description: str
    
class TextAdventureTiles:
    WALKABLE = TextAdventureTile("w", "empty space you can walk on")
    PLAYER = TextAdventureTile("p", "your current position")
    WALL = TextAdventureTile("o", "walls that block your path")
    
    @classmethod
    def get_all_tiles(cls) -> List[TextAdventureTile]:
        return [value for value in vars(cls).values() if isinstance(value, TextAdventureTile)]
    
    @classmethod
    def get_tiles_description(cls) -> str:
        return "\n".join([f"- {tile.description} ('{tile.symbol}')" for tile in cls.get_all_tiles()])