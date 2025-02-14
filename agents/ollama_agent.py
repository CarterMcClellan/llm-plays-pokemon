from .base import BaseAgent
from typing import Optional
import ollama
import os

class OllamaAgent(BaseAgent):
    def __init__(self, agent_args: dict):
        """
        Initialize Ollama agent with specified model
        
        Args:
            model_name (str): Name of the Ollama model to use
            debug (bool): Enable debug mode
        """
        super().__init__(agent_args)

        model_name = os.getenv("OLLAMA_MODEL_NAME")
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
            if self.debug:
                stream = ollama.chat(model=self.model_name, messages=[
                    {'role': 'user', 'content': prompt}
                ], stream=True)

                response = ""
                for chunk in stream:
                    val = chunk['message']['content']
                    if val:
                        response += val
                        if self.debug:
                            print(val, end='', flush=True)
            else:
                response = ollama.chat(model=self.model_name, messages=[
                    {'role': 'user', 'content': prompt}
                ])

            action_str = response['message']['content'].strip().lower()
            action_str = self.postprocess_response(action_str)
            return action_str
        except Exception as e:
            self.logger.error(f"Error getting action from Ollama: {e}")
            return None