from flask import Flask, request, jsonify
from PIL import Image
import io
import argparse
from agent import OllamaAgent, HuggingFaceAgent
from game_enviroment import GameAction
import os
from dotenv import load_dotenv
import logging
import socket
import requests

load_dotenv()

SECRET_KEY = os.getenv("AGENT_SERVER_SECRET_KEY")

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except Exception:
        return 'unknown'

def get_local_ip():
    try:
        # Create a socket to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't actually create a connection, just uses the interface
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return 'unknown'

def create_app(agent_type='ollama', model=None, debug=False):
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    logging.info(f"Initializing agent server with {agent_type} agent and model: {model}")
    
    # Initialize the specified agent type
    if agent_type.lower() == 'ollama':
        model = model or "llama3.2-vision:11b"
        agent = OllamaAgent(model=model, debug=debug)
    else:  # huggingface
        model = model or "meta-llama/Llama-3.2-11B-Vision-Instruct"
        agent = HuggingFaceAgent(model_id=model, debug=debug)

    @app.route('/predict', methods=['POST'])
    def predict():
        try:
            # Validate secret key
            request_key = request.headers.get('X-Secret-Key')
            if not request_key or request_key != SECRET_KEY:
                logging.warning("Unauthorized request attempt with invalid secret key")
                return jsonify({'error': 'Unauthorized - Invalid or missing secret key'}), 401

            if 'image' not in request.files:
                logging.error("Request received without image file")
                return jsonify({'error': 'No image file provided'}), 400

            image_file = request.files['image']
            image = Image.open(io.BytesIO(image_file.read()))
            logging.info(f"Received image with size: {image.size}")
            
            valid_actions = request.form.get('valid_actions', '').split(',')
            if not valid_actions or valid_actions == ['']:
                valid_actions = [action for action in GameAction]
            else:
                valid_actions = [GameAction[action.upper()] for action in valid_actions]

            action = agent.get_llm_action(image, valid_actions)
            logging.info(f"Predicted action: {action.name}")
            
            return jsonify({
                'action': action.name,
            })

        except Exception as e:
            logging.error(f"Error processing request: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    return app

def main():
    parser = argparse.ArgumentParser(description='Start the Pokemon Agent Server')
    parser.add_argument('--agent', 
                       choices=['ollama', 'huggingface'],
                       default='ollama',
                       help='Type of agent to use (ollama or huggingface)')
    parser.add_argument('--model',
                       help='Model identifier to use. Defaults depend on agent type.')
    parser.add_argument('--debug',
                       action='store_true',
                       help='Enable debug mode')
    parser.add_argument('--port',
                       type=int,
                       default=5000,
                       help='Port to run the server on')
    parser.add_argument('--host',
                       default='0.0.0.0',
                       help='Host to run the server on')

    args = parser.parse_args()
    
    app = create_app(agent_type=args.agent, model=args.model, debug=args.debug)
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    logging.info(f"Starting server on {args.host}:{args.port}")
    logging.info(f"Local IP: {local_ip}")
    logging.info(f"Public IP: {public_ip}")
    app.run(host=args.host, port=args.port)

if __name__ == '__main__':
    main()