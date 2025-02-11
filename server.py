from flask import Flask, request, jsonify
from PIL import Image
import io
import argparse
from agent import OllamaAgent, HuggingFaceAgent
from game_enviroment import GameAction
import os

SECRET_KEY = os.getenv("AGENT_SERVER_SECRET_KEY")

def create_app(agent_type='ollama', model=None, debug=False):
    app = Flask(__name__)
    
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
                return jsonify({'error': 'Unauthorized - Invalid or missing secret key'}), 401

            if 'image' not in request.files:
                return jsonify({'error': 'No image file provided'}), 400

            image_file = request.files['image']
            image = Image.open(io.BytesIO(image_file.read()))
            
            valid_actions = request.form.get('valid_actions', '').split(',')
            if not valid_actions or valid_actions == ['']:
                valid_actions = [action for action in GameAction]
            else:
                valid_actions = [GameAction[action.upper()] for action in valid_actions]

            action = agent.get_llm_action(image, valid_actions)
            
            return jsonify({
                'action': action.name,
                'metrics': agent.get_metrics()
            })

        except Exception as e:
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
    app.run(host=args.host, port=args.port)

if __name__ == '__main__':
    main()
