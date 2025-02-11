from PIL.Image import Image
from game_enviroment import GameAction
import logging
import requests
import io
import os

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
        import ollama
        super().__init__(debug=debug)
        self.model = model
        self.ollama = ollama

    def get_llm_action(self, screen: Image, valid_actions: list[GameAction]) -> GameAction:
        """Get next action from Ollama LLM based on current screen"""
        try:
            screen_as_bytes = screen.tobytes()
            if self.debug:
                response = self.ollama.chat(model=self.model, messages=[
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
                response = self.ollama.chat(model=self.model, messages=[
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
        import torch
        from transformers import MllamaForConditionalGeneration, AutoProcessor
        super().__init__(debug=debug)
        self.model_id = model_id
        self.model = MllamaForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.torch = torch

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

            # Clean up the action string by extracting just the action word
            action_str = action_str.split('assistant')[-1]  # Get text after 'assistant'
            action_str = action_str.replace('<|eot_id|>', '').strip()  # Remove EOT token
            action_str = action_str.replace('<|end_header_id|>', '').strip()  # Remove header end tag
            action_str = action_str.replace('.', '').strip()  # Remove any periods
            action_str = action_str.split('\n')[-1].strip()  # Get the last line which should be just the action

            if self.debug:
                self.logger.info(f"Action string: {action_str}")

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

class RemoteAgent(BasePokemonAgent):
    def __init__(self, debug: bool = False):
        """
        Initialize the Remote Pokemon Agent that connects to a server

        Args:
            debug (bool): Enable debug mode
        """
        super().__init__(debug=debug)
        self.server_url = f"http://{os.getenv('SERVER_HOST')}:{os.getenv('SERVER_PORT')}"
        self.secret_key = os.getenv("AGENT_SERVER_SECRET_KEY")

    def get_llm_action(self, screen: Image, valid_actions: list[GameAction]) -> GameAction:
        """Get next action from remote server based on current screen"""
        try:
            # Convert image to bytes
            img_byte_arr = io.BytesIO()
            screen.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Prepare the request
            files = {'image': ('screen.png', img_byte_arr, 'image/png')}
            headers = {'X-Secret-Key': self.secret_key}
            data = {'valid_actions': ','.join(action.name.lower() for action in valid_actions)}

            # Make the request
            response = requests.post(
                f"{self.server_url}/predict",
                files=files,
                data=data,
                headers=headers
            )

            if response.status_code != 200:
                self.logger.error(f"Server error: {response.text}")
                return GameAction.B

            result = response.json()
            if self.debug:
                self.logger.info(result)

            action_str = result['action'].lower()

            try:
                action = GameAction[action_str.upper()]
                if action not in valid_actions:
                    return self.handle_invalid_action(action_str)
                return action
            except KeyError:
                return self.handle_invalid_action(action_str)

        except Exception as e:
            self.logger.error(f"Error getting remote action: {e}")
            return GameAction.B
