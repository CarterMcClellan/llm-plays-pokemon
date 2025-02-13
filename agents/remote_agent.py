from .base import BaseAgent
from typing import Optional
import requests

class RemoteAgent(BaseAgent):
    def __init__(self, api_url, api_key=None, debug=False):
        """
        Initialize Remote agent that calls an external API
        
        Args:
            api_url (str): URL of the remote API
            api_key (str, optional): API key for authentication
            debug (bool): Enable debug mode
        """
        super().__init__(debug=debug)
        self.api_url = api_url
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

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