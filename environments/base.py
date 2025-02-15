from abc import ABC, abstractmethod
from enum import Enum
from typing import NamedTuple, List, Any, Optional
import logging

from agents.base import BaseAgent

class GameAction(Enum):
    """Base class for game actions"""
    @classmethod
    @abstractmethod
    def get_all_actions(cls) -> List["GameAction"]:
        """Returns all possible actions for the game"""
        raise NotImplementedError

    def __repr__(self):
        return self.name.lower()
    
    @classmethod
    @abstractmethod
    def default_action(cls) -> "GameAction":
        """Returns the default action for the game"""
        raise NotImplementedError

class GameEnvironment(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def get_prompt(self) -> str:
        """
        Get the system prompt for the game
        """
        raise NotImplementedError
    
    @abstractmethod
    def run(self, agent: Optional[BaseAgent] = None):
        """
        Run the game environment with the given agent

        If no agent is provided, the environment will run in manual mode
        """
        raise NotImplementedError


def enviroment_factory(args: dict) -> GameEnvironment:
    """
    Factory function to create a GameEnvironment instance based on the provided arguments
    """
    env_type = args.get("env_type")
    env_args = args.get("env_args")
    if not env_type or not env_args:
        raise ValueError("Missing environment type or arguments")
    
    if type(env_args) != dict:
        raise ValueError("Environment arguments must be a dictionary")
    
    if type(env_type) != str:
        raise ValueError("Environment type must be a string")

    if env_type == "pokemon":
        from environments.pokemon import PokemonGameEnviroment, PokemonGameEnviromentArgs
        poke_args = PokemonGameEnviromentArgs(**env_args)
        return PokemonGameEnviroment(poke_args)
    elif env_type == "text-adventure":
        # from environments.text_adventure import TextAdventureGameEnvironment, TextAdventureGameEnvironmentArgs
        from environments.text_adventure.environment import TextAdventureGameEnvironment
        from environments.text_adventure.args import TextAdventureGameEnvironmentArgs
        text_args = TextAdventureGameEnvironmentArgs(**env_args)
        return TextAdventureGameEnvironment(text_args)
    else:
        raise ValueError(f"Invalid environment type: {env_type}")