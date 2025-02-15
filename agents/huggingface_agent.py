from typing import Optional
from .base import BaseAgent
from transformers import AutoModelForCausalLM, AutoTokenizer

class HuggingFaceAgent(BaseAgent):
    def __init__(self, agent_args: dict):
        """
        Initialize HuggingFace agent with specified model
        
        Args:
            model_name (str): Name of the HuggingFace model to use
            debug (bool): Enable debug mode
        """
        super().__init__(agent_args)
        self.debug = agent_args.get("debug", False)

        self.model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

    def get_action_raw(self, prompt: str) -> Optional[str]:
        """
        Get next action from HuggingFace model based on game state
        
        Args:
            game_state (GameState): Current game state including screen and available actions
            
        Returns:
            GameAction: The chosen action
        """
        prompt = self.preprocess_prompt(prompt)

        try:
            # Generate response from model
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(**inputs, max_length=50)
            action_str = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip().lower()
            action_str = self.postprocess_response(action_str)

            return action_str
        except Exception as e:
            self.logger.error(f"Something went wrong with the HuggingFace model: {e}")
            return None