from .base import BaseAgent
from typing import Optional
import ollama
import logging

class OllamaAgent(BaseAgent):
    def __init__(self, model_name="llama2", debug=False):
        """
        Initialize Ollama agent with specified model
        
        Args:
            model_name (str): Name of the Ollama model to use
            debug (bool): Enable debug mode
        """
        super().__init__(debug=debug)
        self.model_name = model_name

    def get_action_raw(self, prompt: str) -> Optional[str]:
        """
        Get next action from Ollama model based on game state
        
        Args:
            prompt (str): The prompt to send to the LLM
            
        Returns:
            str: The response from the LLM
        """
        
        try:
            prompt = self.preprocess_prompt(prompt)
            response = ollama.chat(model=self.model_name, messages=[
                {'role': 'user', 'content': prompt}
            ])
            action_str = response['message']['content'].strip().lower()
            action_str = self.postprocess_response(action_str)
            return action_str
        except Exception as e:
            self.logger.error(f"Error getting action from Ollama: {e}")
            return None