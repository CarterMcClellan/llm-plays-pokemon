import matplotlib.pyplot as plt
from PIL.Image import Image
from game_enviroment import GameAction
import logging
import ollama

class PokemonLLMAgent:
    def __init__(self, model="deepseek-r1:14b", debug=False):
        """
        Initialize the Pokemon LLM Agent

        Args:
            model (str): Ollama model to use
        """
        self.model = model
        self.debug = debug

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize metrics
        self.reset_metrics()

    def get_prompt(self, valid_actions):
        """Create the base prompt for the LLM"""
        return f"""You are playing Pokemon Red. You can see the game screen and must choose the next action.
Valid actions are: {valid_actions}
Based on what you see in the game screen, what single action should be taken next?
Respond with just one word - the action to take."""

    def reset_metrics(self):
        """Reset agent metrics"""
        self.total_steps = 0
        self.action_history = []
        self.invalid_actions = 0

    def get_llm_action(
        self, screen: Image, valid_actions: list[GameAction]
    ) -> GameAction:
        """Get next action from LLM based on current screen"""
        try:
            screen_as_bytes = screen.tobytes()
            if self.debug:
                response = ollama.chat(model=self.model, messages=[
                    {
                        'role': 'user',
                        'content': self.get_prompt(valid_actions),
                        'images': [screen_as_bytes],
                    },
                ], stream=True)

                curr = ""
                for part in response:
                    part_val = part['message']['content']
                    curr += part_val
                    print(part_val, end='', flush=True)

                action_str: str = curr.strip().lower()
            else:
                response = ollama.chat(model=self.model, messages=[
                    {
                        'role': 'user',
                        'content': self.get_prompt(valid_actions),
                        'images': [screen_as_bytes],
                    },
                ])

                action_str: str = response['response'].strip().lower()

            # Convert string to GameAction enum
            try:
                action = GameAction[action_str.upper()]
                if action not in valid_actions:
                    self.logger.warning(f"Invalid action from LLM: {action}")
                    self.invalid_actions += 1
                    action = GameAction.B
            except KeyError:
                self.logger.warning(f"Invalid action string from LLM: {action_str}")
                self.invalid_actions += 1
                action = GameAction.B

            return action

        except Exception as e:
            self.logger.error(f"Error getting LLM action: {e}")
            return GameAction.B  # Default to B on error

    def get_metrics(self):
        """Get current episode metrics"""
        return {
            "total_steps": self.total_steps,
            "invalid_actions": self.invalid_actions,
            "action_frequencies": {
                action: self.action_history.count(action)
                for action in self.valid_actions
            },
        }
