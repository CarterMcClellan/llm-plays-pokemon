from pyboy import PyBoy
from pyboy.utils import WindowEvent
import numpy as np
from skimage.transform import downscale_local_mean

class SimplePokemonEnv:
    def __init__(self, gb_path, headless=False):
        # Initialize valid actions
        self.valid_actions = {
            'up': WindowEvent.PRESS_ARROW_UP,
            'down': WindowEvent.PRESS_ARROW_DOWN,
            'left': WindowEvent.PRESS_ARROW_LEFT,
            'right': WindowEvent.PRESS_ARROW_RIGHT,
            'a': WindowEvent.PRESS_BUTTON_A,
            'b': WindowEvent.PRESS_BUTTON_B,
            'start': WindowEvent.PRESS_BUTTON_START
        }
        
        # Initialize release actions
        self.release_actions = {
            'up': WindowEvent.RELEASE_ARROW_UP,
            'down': WindowEvent.RELEASE_ARROW_DOWN,
            'left': WindowEvent.RELEASE_ARROW_LEFT,
            'right': WindowEvent.RELEASE_ARROW_RIGHT,
            'a': WindowEvent.RELEASE_BUTTON_A,
            'b': WindowEvent.RELEASE_BUTTON_B,
            'start': WindowEvent.RELEASE_BUTTON_START
        }

        # Initialize PyBoy
        window_type = "null" if headless else "SDL2"
        self.pyboy = PyBoy(gb_path, window=window_type)
        
        if not headless:
            self.pyboy.set_emulation_speed(6)

    def get_screen(self, reduce_res=True):
        """Get the current game screen as a numpy array"""
        game_pixels = self.pyboy.screen.ndarray[:,:,0:1]  # Get grayscale image
        if reduce_res:
            # Reduce resolution by factor of 2
            game_pixels = downscale_local_mean(game_pixels, (2,2,1)).astype(np.uint8)
        return game_pixels

    def step(self, action):
        """Execute an action in the environment
        
        Args:
            action (str): One of 'up', 'down', 'left', 'right', 'a', 'b', 'start'
        """
        if action not in self.valid_actions:
            raise ValueError(f"Invalid action: {action}. Must be one of {list(self.valid_actions.keys())}")
        
        # Press button
        self.pyboy.send_input(self.valid_actions[action])
        
        # Hold for 8 frames
        self.pyboy.tick(8, True)
        
        # Release button
        self.pyboy.send_input(self.release_actions[action])
        
        # Wait for remainder of action duration (total 16 frames)
        self.pyboy.tick(8, True)
        
        # Return the new screen
        return self.get_screen()

    def reset(self, state_path):
        """Reset the environment using a saved state"""
        with open(state_path, "rb") as f:
            self.pyboy.load_state(f)
        return self.get_screen()

    def close(self):
        """Close the environment"""
        self.pyboy.stop()

    def get_valid_actions(self):
        """Return list of valid actions"""
        return list(self.valid_actions.keys())