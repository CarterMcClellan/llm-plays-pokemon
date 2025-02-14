from .base import BaseAgent
from typing import Optional
import requests
import os

class RemoteAgent(BaseAgent):
    def __init__(self, agent_args: dict):
        """
        Initialize Remote agent that calls an external API
        
        Args:
            api_url (str): URL of the remote API
            api_key (str, optional): API key for authentication
            debug (bool): Enable debug mode
        """
        super().__init__(agent_args)
        host = os.environ["AGENT_SERVER_HOST"]
        port = os.environ["AGENT_SERVER_PORT"]
        key = os.environ["AGENT_SERVER_SECRET_KEY"]
        self.api_url = f"{host}:{port}"
        self.headers = {"Authorization": f"Bearer {key}"}

    def get_action_raw(self, prompt: str) -> Optional[str]:
        """
        Get next action from remote API based on game state
        
        Args:
            game_state (GameState): Current game state including screen and available actions
            
        Returns:
            str: The response from the remote API
        """
        prompt = self.preprocess_prompt(prompt)
        
        try:
            response = requests.post(self.api_url, json={"prompt": prompt}, headers=self.headers)
            response.raise_for_status()
            action_str = response.json().get("action", "").strip().lower()
            action_str = self.postprocess_response(action_str)
            return action_str
        except Exception as e:
            self.logger.error(f"Error getting action from remote API: {e}")
            return None