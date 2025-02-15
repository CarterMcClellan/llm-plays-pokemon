from dataclasses import dataclass
from typing import List, NamedTuple, Optional
from .actions import TextAdventureGameAction
from .tiles import TextAdventureTile, TextAdventureTiles

class Position(NamedTuple):
    x: int
    y: int

class TextAdventureGame:
    def __init__(self, map_size: int = 8):
        self.map = [
            ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
            ['o', 'w', 'w', 'w', 'w', 'w', 'w', 'o'],
            ['o', 'w', 'w', 'w', 'w', 'w', 'w', 'o'],
            ['o', 'w', 'w', 'w', 'w', 'w', 'w', 'o'],
            ['o', 'w', 'w', 'w', 'w', 'w', 'w', 'o'],
            ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o']
        ]
        self.current_position = Position(1, 1)
        self.previous_position = Position(1, 1)

    def is_valid_move(self, x: int, y: int) -> bool:
        if (0 <= y < len(self.map) and 
            0 <= x < len(self.map[0]) and 
            self.map[y][x] == 'w'):
            return True
        return False

    def update(self, action: TextAdventureGameAction) -> bool:
        new_x, new_y = self.current_position.x, self.current_position.y
        
        if action == TextAdventureGameAction.UP:
            new_y -= 1
        elif action == TextAdventureGameAction.DOWN:
            new_y += 1
        elif action == TextAdventureGameAction.LEFT:
            new_x -= 1
        elif action == TextAdventureGameAction.RIGHT:
            new_x += 1

        valid = self.is_valid_move(new_x, new_y)
        if valid:
            self.previous_position = self.current_position
            self.current_position = Position(new_x, new_y)
        return valid

    def get_map_string(self) -> str:
        # Update map with player position
        self.map[self.previous_position.y][self.previous_position.x] = "w"
        self.map[self.current_position.y][self.current_position.x] = "p"
        return '\n'.join([''.join(row) for row in self.map])