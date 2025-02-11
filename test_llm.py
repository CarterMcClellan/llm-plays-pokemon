from PIL import Image
import os
from transformers import MllamaForConditionalGeneration, AutoProcessor
import torch

def test_llm_vision():
    """Test the vision capabilities of the LLM with Hugging Face"""
    # Load a test image
    test_image_path = "test_data/test_screen.png"
    if not os.path.exists(test_image_path):
        raise FileNotFoundError(f"Test image not found at {test_image_path}")
    
    test_image = Image.open(test_image_path)
    
    # Print image resolution
    print(f"Image resolution: {test_image.size}")
    
    # Update prompt format
    prompt = "<|image|><|begin_of_text|>Look at this image and describe what you see."

    try:
        model_name = "meta-llama/Llama-3.2-11B-Vision"
        # Update model class and dtype
        model = MllamaForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        processor = AutoProcessor.from_pretrained(model_name)
        
        # Simplify inputs
        inputs = processor(test_image, prompt, return_tensors="pt").to(model.device)
        
        # Generate response
        output = model.generate(**inputs, max_new_tokens=100)
        
        # Decode and print response
        print("LLM Response:")
        print("-" * 50)
        print(processor.decode(output[0]))
        print("-" * 50)

    except Exception as e:
        print(f"Error during vision test: {e}")

if __name__ == "__main__":
    test_llm_vision()
