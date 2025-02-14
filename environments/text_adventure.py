from enum import Enum
from typing import NamedTuple, Optional, List
from agents.base import BaseAgent
from utils.keystroke_listener import ModernKeyboardListener, echo_disabled
from environments.base import GameAction, GameEnvironment
from dataclasses import dataclass
import pygame
import re

class Position(NamedTuple):
    x: int
    y: int

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

class TextAdventureGameEnvironmentArgs:
    def __init__(self, map_size: int = 8, debug: bool = False):
        self.map_size = map_size
        self.debug = debug

class TextAdventureGameEnvironment(GameEnvironment):
    def __init__(self, args: TextAdventureGameEnvironmentArgs):
        super().__init__()
        self.logger.info(f"Initializing Text Adventure Environment with debug: {args.debug}")
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
        self.debug = args.debug

        # Initialize Pygame
        pygame.init()
        self.tile_size = 50  # pixels per tile
        self.width = len(self.map[0]) * self.tile_size
        self.height = len(self.map) * self.tile_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Text Adventure")
        
        # Define colors
        self.colors = {
            'w': (200, 200, 200),  # walkable - light gray
            'o': (100, 100, 100),  # wall - dark gray
            'p': (0, 255, 0),      # player - green
        }

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Update map with player position
        self.map[self.previous_position.y][self.previous_position.x] = "w"
        self.map[self.current_position.y][self.current_position.x] = "p"
        
        # Draw tiles
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    x * self.tile_size, 
                    y * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                )
                pygame.draw.rect(self.screen, self.colors[tile], rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # border
        
        # Update display
        pygame.display.flip()
        
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

    def get_map_string(self) -> str:
        return '\n'.join([''.join(row) for row in self.map])

    def is_valid_move(self, x, y):
        # Check if the position is within bounds and is walkable
        if (0 <= y < len(self.map) and 
            0 <= x < len(self.map[0]) and 
            self.map[y][x] == 'w'):
            return True
        return False
    
    def update(self, action: TextAdventureGameAction):
        if self.debug:
            self.logger.info(f"Updating position from {self.current_position} to {action}")

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
            self.render()
    
    def get_prompt(self) -> str:
        return f"""You are in a text adventure. 

```
{self.get_map_string()}        
```
        
The world contains:
{TextAdventureTiles.get_tiles_description()}
You can choose to take any of the following actions: {TextAdventureGameAction.get_all_actions()}
Return the answer using the answer tag, for example if the answer is "up", return:
```
<answer>up</answer>
```
"""

    def _brute_parse(self, answer: str) -> Optional[str]:
        # strip everything within the <think></think> tags
        answer = re.sub(r'<think>(.*?)</think>', '', answer)
        answer = answer.strip().lower()

        # count all the occurrences of each action
        action_counts = {
            "up": answer.count("up"),
            "down": answer.count("down"),
            "left": answer.count("left"),
            "right": answer.count("right")
        }

        # if no actions found, return None
        if sum(action_counts.values()) == 0:
            return None

        # return the action with the highest count
        most_common_action = max(action_counts, key=action_counts.get)
        return most_common_action
                
    def parse_answer(self, answer: Optional[str]) -> TextAdventureGameAction:
        if answer:
            tag_match = re.search(r'<answer>(.*?)</answer>', answer)
            box_match = re.search(r'\\boxed{\\text{(.*?)}}', answer)
            brute_match = self._brute_parse(answer)
            
            action = None
            if tag_match:
                action = tag_match.group(1).strip().lower()
            elif box_match:
                action = box_match.group(1).strip().lower()
            elif brute_match:
                action = brute_match
            
            if action:
                if action == "up":
                    return TextAdventureGameAction.UP
                elif action == "down":
                    return TextAdventureGameAction.DOWN
                elif action == "left":
                    return TextAdventureGameAction.LEFT
                elif action == "right":
                    return TextAdventureGameAction.RIGHT

        if self.debug:
            self.logger.warning(f"No valid action found in answer: {answer}, returning default action: {TextAdventureGameAction.UP}")

        return TextAdventureGameAction.UP
        
    def run(self, agent: Optional[BaseAgent] = None):
        try:
            if agent:
                while True:
                    self.render()
                    prompt = self.get_prompt()
                    if self.debug:
                        self.logger.info(f"\nPrompt: {prompt}")  

                    raw_action = agent.get_action_raw(prompt)
                    action = self.parse_answer(raw_action)

                    if self.debug:
                        self.logger.info(f"\nRaw Action: {raw_action}\nAction Parsed: {action}")    

                    self.update(action)
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return
                    
            else:
                with echo_disabled():
                    self.listener = ModernKeyboardListener(self.handle_key_event)
                    self.render()
                    self.listener.run()
        finally:
            pygame.quit()

    def handle_key_event(self, event):
        if event['type'] == 'down':
            if event['name'] == 'escape':
                self.listener.stop()
                pygame.quit()
            elif event['name'] in ['up', 'down', 'left', 'right']:
                if event['name'] == 'up':
                    self.update(TextAdventureGameAction.UP)
                elif event['name'] == 'down':
                    self.update(TextAdventureGameAction.DOWN)
                elif event['name'] == 'left':
                    self.update(TextAdventureGameAction.LEFT)
                elif event['name'] == 'right':
                    self.update(TextAdventureGameAction.RIGHT)
