from PIL import Image
import os
import ollama

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

    try:
        # Make direct request to ollama
        response = ollama.chat(
            model="deepseek-r1:14b",
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [test_image.tobytes()],
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
