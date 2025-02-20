from typing import Optional
import pygame
from environments.base import GameEnvironment
from agents.base import BaseAgent
from .game import TextAdventureGame
from .renderer import PygameRenderer
from .parser import ResponseParser
from .actions import TextAdventureGameAction
from .tiles import TextAdventureTiles
from .args import TextAdventureGameEnvironmentArgs

class TextAdventureGameEnvironment(GameEnvironment):
    def __init__(self, args: TextAdventureGameEnvironmentArgs):
        super().__init__()
        self.debug = args.debug
        self.game = TextAdventureGame(args.map_size)
        self.renderer = PygameRenderer(self.game)
        self.parser = ResponseParser()
        self.action_map = {
            pygame.K_w: TextAdventureGameAction.UP,
            pygame.K_s: TextAdventureGameAction.DOWN,
            pygame.K_a: TextAdventureGameAction.LEFT,
            pygame.K_d: TextAdventureGameAction.RIGHT,
            pygame.K_q: None  
        }

    def render(self):
        """Render the current game state"""
        self.renderer.render()

    def update(self, action: TextAdventureGameAction):
        """Update game state with the given action"""
        return self.game.update(action)

    def parse_answer(self, answer: Optional[str]) -> TextAdventureGameAction:
        """Parse the LLM response into a game action"""
        return self.parser.parse_answer(answer)

    def handle_pygame_events(self) -> bool:
        """
        Handle pygame events and return whether the game should continue running
        
        Returns:
            bool: False if the game should quit, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key in self.action_map:
                    action = self.action_map[event.key]
                    if self.debug:
                        self.logger.info(f"Key pressed: {pygame.key.name(event.key)}")
                        self.logger.info(f"Action: {action}")
                    if action is not None:
                        self.update(action)
                    else:
                        return False  
        return True

    def get_prompt(self) -> str:
        return f"""You are in a text adventure. 

```
{self.game.get_map_string()}        
```
        
The world contains:
{TextAdventureTiles.get_tiles_description()}
You can choose to take any of the following actions: {TextAdventureGameAction.get_all_actions()}
Return the answer using the answer tag, for example if the answer is "up", return:
```
<answer>up</answer>
```
"""

    def run(self, agent: Optional[BaseAgent] = None):
        try:
            running = True
            
            if agent:
                while running:
                    running = self.handle_pygame_events()
                    if not running:
                        break

                    self.render()
                    prompt = self.get_prompt()
                    raw_action = agent.get_action_raw(prompt)
                    action = self.parse_answer(raw_action)

                    if self.debug:
                        self.logger.info(f"\nRaw Action: {raw_action}\nAction Parsed: {action}")    

                    self.update(action)
            else:
                self.logger.info("Running in manual mode")
                self.logger.info("Game Controls: WASD to move, Q to quit")
                
                while running:
                    running = self.handle_pygame_events()
                    if not running:
                        break
                        
                    self.render()
        finally:
            pygame.quit()