import logging
from abc import ABC, abstractmethod
from typing import Optional

class BaseAgent(ABC):
    def __init__(self, agent_args: dict):
        """
        Initialize the base Agent that can work with any game environment

        Args:
            agent_args (dict): Arguments for the agent
        """
        self.agent_args = agent_args

        self.debug = agent_args.get("debug", False)

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

def agent_factory(args: dict) -> BaseAgent:
    """
    Factory function to create a BaseAgent instance based on the provided arguments
    """
    agent_type = args.get("agent_type")
    agent_args = args.get("agent_args")
    if not agent_type or not agent_args:
        raise ValueError("Missing agent type or arguments")
    
    if type(agent_args) != dict:
        raise ValueError("Agent arguments must be a dictionary")
    
    if agent_type == "remote":
        from agents.remote_agent import RemoteAgent
        return RemoteAgent(agent_args)
    elif agent_type == "ollama":
        from agents.ollama_agent import OllamaAgent
        return OllamaAgent(agent_args)
    elif agent_type == "huggingface":
        from agents.huggingface_agent import HuggingFaceAgent
        return HuggingFaceAgent(agent_args)
    else:
        raise ValueError(f"Invalid agent type: {agent_type}")