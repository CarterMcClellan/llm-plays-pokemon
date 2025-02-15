from typing import Optional
from .base import BaseAgent
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

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

        self.model_name = "unsloth/DeepSeek-R1-Distill-Qwen-32B-bnb-4bit"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name).to(self.device)

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
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            if self.debug:
                action_str = ""
                # Stream the output token by token when in debug mode
                for output in self.model.generate(
                    **inputs,
                    max_length=512,
                    pad_token_id=self.tokenizer.eos_token_id,
                    streaming=True
                ):
                    new_tokens = output[len(inputs['input_ids'][0]):]
                    decoded = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
                    if decoded:
                        action_str += decoded
                        print(decoded, end='', flush=True)
            else:
                outputs = self.model.generate(**inputs)
                action_str = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip().lower()
            
            action_str = self.postprocess_response(action_str)
            return action_str
        except Exception as e:
            self.logger.error(f"Something went wrong with the HuggingFace model: {e}")
            return None