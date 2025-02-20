import argparse
from dotenv import load_dotenv
import logging

from agents.base import agent_factory
from environments.base import enviroment_factory

load_dotenv()

def parse_args():
    # Create main parser with common arguments
    parser = argparse.ArgumentParser(description="Game playing utility")
    
    # Add common arguments that apply to all commands
    common_args = parser.add_argument_group('common arguments')
    common_args.add_argument(
        "--agent",
        type=str,
        choices=["ollama", "remote", "manual", "lcpp"],
        default="ollama",
        help="Type of agent to use (default: ollama)",
    )
    common_args.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    # Create subparsers for different game types
    subparsers = parser.add_subparsers(dest="game_type", required=True)

    # Pokemon subcommand
    pokemon_parser = subparsers.add_parser("pokemon", help="Play Pokemon game")
    pokemon_parser.add_argument("rom_path", type=str, help="Path to the Pokemon ROM file")

    # Text adventure subcommand (simplified)
    subparsers.add_parser("text-adventure", help="Play text adventure game")

    # Server subcommand
    server_parser = subparsers.add_parser("server", help="Run an agent server")
    server_parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
    server_parser.add_argument("--host", default="0.0.0.0", help="Host to run the server on")

    return parser.parse_args()

def run_game(args):
    # Configure logging
    logging.basicConfig(
        level=logging.INFO if not args.debug else logging.DEBUG,
        format='%(name)s - %(levelname)s - %(message)s'
    )
    
    if args.game_type == "server":
        from agents.agent_server import create_app
        create_app(
            debug=args.debug,
            host=args.host,
            port=args.port
        )
        return

    # Simplified environment setup
    env_args = {
        "env_type": args.game_type,
        "env_args": {
            "debug": args.debug,
            **({"rom_path": args.rom_path} if args.game_type == "pokemon" else {})
        }
    }

    agent = agent_factory({"agent_type": args.agent, "agent_args": {"debug": args.debug}}) if args.agent != "manual" else None
    
    game_environment = enviroment_factory(env_args)
    game_environment.run(agent)

if __name__ == "__main__":
    args = parse_args()
    run_game(args)