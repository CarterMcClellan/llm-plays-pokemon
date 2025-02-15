from .base import BaseAgent
from typing import Optional
import llama_cpp

class LlamaCppAgent(BaseAgent):
    def __init__(self, agent_args: dict):
        """
        Initialize llama.cpp agent with specified model
        
        Args:
            agent_args (dict): Configuration arguments
        """
        super().__init__(agent_args)

        # make sure the model has been properly downloaded from hf hub
        self.model = llama_cpp.Llama.from_pretrained(
            # "unsloth/DeepSeek-R1-Distill-Qwen-32B-Q4_K_M",
            "unsloth/DeepSeek-R1-Distill-Qwen-32B-GGUF",
            n_gpu_layers=100,
            n_threads=16,
            type_k=llama_cpp.GGML_TYPE_Q8_0,
        )
        
        # self.model = llama_cpp.Llama(
        #     model_path="models/DeepSeek-R1-Distill-Qwen-32B-Q4_K_M.gguf",
        #     n_gpu_layers=100,  # cheap way to fully offload to GPU
        #     n_threads=16,
        #     type_k=llama_cpp.GGML_TYPE_Q8_0,
        # )

    def get_action_raw(self, prompt: str) -> Optional[str]:
        """
        Get next action from llama.cpp model based on game state
        
        Args:
            prompt (str): The prompt to send to the LLM
            
        Returns:
            str: The response from the LLM
        """
        try:
            prompt = self.preprocess_prompt(prompt)
            
            if self.debug:
                response = self.model.create_completion(
                    prompt=f"<｜User｜>{prompt}<｜Assistant｜>",
                    stream=True
                )
                action_str = ""
                for chunk in response:
                    val = chunk['choices'][0]['text']
                    if val:
                        action_str += val
                        if self.debug:
                            print(val, end='', flush=True)
            else:
                response = self.model.create_completion(
                    prompt=f"<｜User｜>{prompt}<｜Assistant｜>",
                    stream=False
                )
                action_str = response['choices'][0]['text'].strip().lower()

            action_str = self.postprocess_response(action_str)
            return action_str
            
        except Exception as e:
            self.logger.error(f"Error getting action from llama.cpp: {e}")
            return None