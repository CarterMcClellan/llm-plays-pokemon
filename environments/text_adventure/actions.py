from typing import List
from environments.base import GameAction

class TextAdventureGameAction(GameAction):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def get_all_actions(cls) -> List["TextAdventureGameAction"]:
        return [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT]
    
    def __repr__(self):
        return self.name.lower()