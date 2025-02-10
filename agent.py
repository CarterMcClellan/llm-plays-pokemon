import matplotlib.pyplot as plt
from anthropic import Anthropic
import logging

class PokemonLLMAgent:
    def __init__(self, model="claude-3-haiku-20240307"):
        """
        Initialize the Pokemon LLM Agent
        
        Args:
            gb_path (str): Path to the Pokemon ROM file
            state_path (str): Path to the save state file
            api_key (str): Anthropic API key
            model (str): Anthropic model to use
            headless (bool): Whether to run without display
        """
        self.client = Anthropic()
        self.model = model
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize metrics
        self.reset_metrics()
        
    def get_prompt(self, valid_actions):
        """Create the base prompt for the LLM"""
        return f"""You are playing Pokemon Red. You can see the game screen and must choose the next action.
Valid actions are: {valid_actions}
Based on what you see in the game screen, what single action should be taken next?
Respond with just one word - the action to take."""

    def reset_metrics(self):
        """Reset agent metrics"""
        self.total_steps = 0
        self.action_history = []
        self.invalid_actions = 0
    
    def get_llm_action(self, screen_path, valid_actions):
        """Get next action from LLM based on current screen"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1,
                temperature=0.0,
                messages=[
                    {"role": "user", "content": [
                        {"type": "text", "text": self.get_prompt(valid_actions)},
                        {"type": "image", "source": {"type": "path", "path": screen_path}}
                    ]}
                ]
            )
            
            action = message.content[0].text.strip().lower()
            
            if action not in valid_actions:
                self.logger.warning(f"Invalid action from LLM: {action}")
                self.invalid_actions += 1
                action = 'b'  # Default to B if invalid
                
            return action
            
        except Exception as e:
            self.logger.error(f"Error getting LLM action: {e}")
            return 'b'  # Default to B on error
    
    def get_metrics(self):
        """Get current episode metrics"""
        return {
            'total_steps': self.total_steps,
            'invalid_actions': self.invalid_actions,
            'action_frequencies': {
                action: self.action_history.count(action) 
                for action in self.valid_actions
            }
        }