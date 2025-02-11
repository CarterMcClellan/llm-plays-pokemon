from PIL import Image
import os
import ollama
import base64
from io import BytesIO

def test_llm_vision():
    """Test the vision capabilities of the LLM with a direct ollama call"""
    # Load a test image
    test_image_path = "test_data/test_screen.png"
    if not os.path.exists(test_image_path):
        raise FileNotFoundError(f"Test image not found at {test_image_path}")
    
    test_image = Image.open(test_image_path)
    
    # Print image resolution
    print(f"Image resolution: {test_image.size}")
    
    # Create a simple prompt
    prompt = """Look at this image and describe what you see."""

    # Convert image to base64
    buffered = BytesIO()
    test_image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    try:
        # Make direct request to ollama
        response = ollama.chat(
            model="llama3.2-vision:11b",
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [img_base64],
            }],
            stream=True
        )

        # Print response in real-time
        print("LLM Response:")
        print("-" * 50)
        for part in response:
            chunk = part['message']['content']
            print(chunk, end='', flush=True)
        print("\n" + "-" * 50)

    except Exception as e:
        print(f"Error during vision test: {e}")

if __name__ == "__main__":
    test_llm_vision()
