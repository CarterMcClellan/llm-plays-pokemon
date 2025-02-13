import logging
from abc import ABC, abstractmethod
from typing import Optional

class BaseAgent(ABC):
    def __init__(self, debug=False):
        """
        Initialize the base Agent that can work with any game environment

        Args:
            debug (bool): Enable debug mode
        """
        self.debug = debug

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize metrics
        self.reset_metrics()

    def reset_metrics(self):
        """Reset agent metrics"""
        self.total_steps = 0
        self.action_history = []
        self.invalid_actions = 0

    @abstractmethod
    def get_action_raw(self, prompt: str) -> Optional[str]:
        """
        Get the next action from the LLM based on the current game state

        Args:
            game_state (GameState): The current state of the game

        Returns:
            GameAction: The chosen action
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def preprocess_prompt(self, prompt: str) -> str:
        """
        Preprocess the prompt for the LLM
        """
        return prompt
    
    def postprocess_response(self, action: str) -> str:
        """
        Postprocess the response from the LLM
        """
        return action
