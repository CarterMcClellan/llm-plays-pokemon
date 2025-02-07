from pyboy import PyBoy
from enum import Enum
import time

class GameActions(Enum):
    """Enum for available game actions"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    A = "a"
    B = "b"
    START = "start"
    SELECT = "select"

class PokemonActionHandler:
    """
    Handles all game interactions and button inputs for Pokemon Red.
    Provides methods for common actions and sequences.
    """
    
    def __init__(self, pyboy: PyBoy):
        self.pyboy = pyboy
        self._button_mapping = {
            GameActions.UP: "up",
            GameActions.DOWN: "down",
            GameActions.LEFT: "left",
            GameActions.RIGHT: "right",
            GameActions.A: "button_a",
            GameActions.B: "button_b",
            GameActions.START: "button_start",
            GameActions.SELECT: "button_select"
        }
    
    def press_button(self, action: GameActions, frames_held: int = 1):
        """Press and hold a button for specified number of frames"""
        button = self._button_mapping[action]
        self.pyboy.button(button, True)
        self.tick(frames_held)
        self.pyboy.button(button, False)
        self.tick(1)  # Buffer frame
    
    def tick(self, frames: int = 1):
        """Advance the game by specified number of frames"""
        for _ in range(frames):
            self.pyboy.tick()
    
    # Common action sequences
    def walk_steps(self, direction: GameActions, steps: int):
        """Walk in specified direction for given number of steps"""
        if direction not in [GameActions.UP, GameActions.DOWN, GameActions.LEFT, GameActions.RIGHT]:
            raise ValueError("Direction must be UP, DOWN, LEFT, or RIGHT")
        
        for _ in range(steps):
            self.press_button(direction, frames_held=16)  # One step is typically 16 frames
    
    def select_menu_item(self, moves: int = 1, confirm: bool = True):
        """Move down in a menu and optionally confirm selection"""
        for _ in range(moves):
            self.press_button(GameActions.DOWN)
            self.tick(2)
        
        if confirm:
            self.press_button(GameActions.A)
    
    def open_menu(self):
        """Open the main menu"""
        self.press_button(GameActions.START)
    
    def close_menu(self):
        """Close current menu"""
        self.press_button(GameActions.B) 