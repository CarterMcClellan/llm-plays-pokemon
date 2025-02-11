import matplotlib.pyplot as plt
from PIL.Image import Image
from game_enviroment import GameAction
import logging
import ollama
import torch
from transformers import MllamaForConditionalGeneration, AutoProcessor

class BasePokemonAgent:
    def __init__(self, debug=False):
        """
        Initialize the base Pokemon Agent

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

    def handle_invalid_action(self, action_str: str) -> GameAction:
        """Handle invalid actions by logging and returning default action"""
        self.logger.warning(f"Invalid action string from LLM: {action_str}")
        self.invalid_actions += 1
        return GameAction.B

    def get_prompt(self, valid_actions):
        """Get standardized prompt for both agent types"""
        return f"""You are playing Pokemon Red. You can see the game screen and must choose the next action.
Valid actions are: {valid_actions}
Based on what you see in the game screen, what single action should be taken next?
Respond with just one word - the action to take."""

class OllamaAgent(BasePokemonAgent):
    def __init__(self, model="llama3.2-vision:11b", debug=False):
        super().__init__(debug=debug)
        self.model = model

    def get_llm_action(self, screen: Image, valid_actions: list[GameAction]) -> GameAction:
        """Get next action from Ollama LLM based on current screen"""
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
                action_str = curr.strip().lower()
            else:
                response = ollama.chat(model=self.model, messages=[
                    {
                        'role': 'user',
                        'content': self.get_prompt(valid_actions),
                        'images': [screen_as_bytes],
                    },
                ])
                action_str = response['response'].strip().lower()

            try:
                action = GameAction[action_str.upper()]
                if action not in valid_actions:
                    return self.handle_invalid_action(action_str)
                return action
            except KeyError:
                return self.handle_invalid_action(action_str)

        except Exception as e:
            self.logger.error(f"Error getting LLM action: {e}")
            return GameAction.B

class HuggingFaceAgent(BasePokemonAgent):
    def __init__(self, model_id="meta-llama/Llama-3.2-11B-Vision-Instruct", debug=False):
        super().__init__(debug=debug)
        self.model_id = model_id
        self.model = MllamaForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        self.processor = AutoProcessor.from_pretrained(model_id)

    def get_llm_action(self, screen: Image, valid_actions: list[GameAction]) -> GameAction:
        """Get next action from Hugging Face LLM based on current screen"""
        try:
            messages = [
                {"role": "user", "content": [
                    {"type": "image"},
                    {"type": "text", "text": self.get_prompt(valid_actions)}
                ]}
            ]

            input_text = self.processor.apply_chat_template(messages, add_generation_prompt=True)
            inputs = self.processor(
                screen,
                input_text,
                add_special_tokens=False,
                return_tensors="pt"
            ).to(self.model.device)

            output = self.model.generate(**inputs, max_new_tokens=30)
            action_str = self.processor.decode(output[0]).strip().lower()

            try:
                action = GameAction[action_str.upper()]
                if action not in valid_actions:
                    return self.handle_invalid_action(action_str)
                return action
            except KeyError:
                return self.handle_invalid_action(action_str)

        except Exception as e:
            self.logger.error(f"Error getting LLM action: {e}")
            return GameAction.B
