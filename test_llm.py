import requests
import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor

def test_llm_vision():
    """Test the vision capabilities of the LLM with Hugging Face"""
    # url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/0052a70beed5bf71b92610a43a52df6d286cd5f3/diffusers/rabbit.jpg"
    # image = Image.open(requests.get(url, stream=True).raw)
    image = Image.open("test_data/test_screen.png")
    
    # Print image resolution
    print(f"Image resolution: {image.size}")
    
    try:
        model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"
        model = MllamaForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        processor = AutoProcessor.from_pretrained(model_id)
        
        # Create messages in the chat format
        messages = [
            {"role": "user", "content": [
                {"type": "image"},
                {"type": "text", "text": "If I had to write a haiku for this one, it would be: "}
            ]}
        ]
        
        # Process input using chat template
        input_text = processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = processor(
            image,
            input_text,
            add_special_tokens=False,
            return_tensors="pt"
        ).to(model.device)
        
        # Generate response
        output = model.generate(**inputs, max_new_tokens=30)
        
        # Decode and print response
        print("LLM Response:")
        print("-" * 50)
        print(processor.decode(output[0]))
        print("-" * 50)

    except Exception as e:
        print(f"Error during vision test: {e}")

if __name__ == "__main__":
    test_llm_vision()
