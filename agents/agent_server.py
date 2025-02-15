from agents.lcpp_agent import LlamaCppAgent
from flask import Flask, request, jsonify
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

def create_app(
    debug: bool,
    host: str,
    port: int
):
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Initialize the HuggingFaceAgent
    agent = LlamaCppAgent(agent_args={"debug": debug})

    @app.route('/predict', methods=['POST'])
    def predict():
        try:
            # Validate secret key
            request_key = request.headers.get('X-Secret-Key')
            if not request_key or request_key != SECRET_KEY:
                logging.warning("Unauthorized request attempt with invalid secret key")
                return jsonify({'error': 'Unauthorized - Invalid or missing secret key'}), 401
            
            if not request.json:
                logging.error("Request received without JSON data")
                return jsonify({'error': 'No JSON data provided'}), 400

            as_json = request.json 

            if 'prompt' not in request.json:
                logging.error("Request received without prompt")
                return jsonify({'error': 'No prompt provided'}), 400

            prompt = as_json.get('prompt')
            action = agent.get_action_raw(prompt)
            
            return jsonify({
                'action': action,
            })

        except Exception as e:
            logging.error(f"Error processing request: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    local_ip = get_local_ip()
    public_ip = get_public_ip()
    logging.info(f"Starting server on {host}:{port}")
    logging.info(f"Local IP: {local_ip}")
    logging.info(f"Public IP: {public_ip}")
    app.run(host=host, port=port)