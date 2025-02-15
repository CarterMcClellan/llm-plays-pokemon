from typing import Optional
import pygame
from environments.base import GameEnvironment
from agents.base import BaseAgent
from utils.keystroke_listener import ModernKeyboardListener, echo_disabled
from .game import TextAdventureGame
from .renderer import PygameRenderer
from .parser import ResponseParser
from .actions import TextAdventureGameAction
from .tiles import TextAdventureTiles
from .args import TextAdventureGameEnvironmentArgs

class TextAdventureGameEnvironment(GameEnvironment):
    # def __init__(self, map_size: int = 8, debug: bool = False):
    def __init__(self, args: TextAdventureGameEnvironmentArgs):
        super().__init__()
        self.debug = args.debug
        self.game = TextAdventureGame(args.map_size)
        self.renderer = PygameRenderer(self.game)
        self.parser = ResponseParser()

    def render(self):
        """Render the current game state"""
        self.renderer.render()

    def update(self, action: TextAdventureGameAction):
        """Update game state with the given action"""
        return self.game.update(action)

    def parse_answer(self, answer: Optional[str]) -> TextAdventureGameAction:
        """Parse the LLM response into a game action"""
        return self.parser.parse_answer(answer)

    def handle_key_event(self, key: str) -> bool:
        """Handle keyboard input for manual play"""
        action_map = {
            'w': TextAdventureGameAction.UP,
            's': TextAdventureGameAction.DOWN,
            'a': TextAdventureGameAction.LEFT,
            'd': TextAdventureGameAction.RIGHT,
            'q': None  # Quit
        }
        
        if key in action_map:
            action = action_map[key]
            if action is None:
                return False  # Quit game
            self.update(action)
            self.render()
        return True

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

    def run(self, agent: Optional[BaseAgent] = None):
        try:
            if agent:
                while True:
                    self.render()
                    prompt = self.get_prompt()

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