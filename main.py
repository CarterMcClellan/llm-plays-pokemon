import argparse
from dotenv import load_dotenv

from agents.base import agent_factory
from environments.base import enviroment_factory

load_dotenv()

def parse_args():
    parser = argparse.ArgumentParser(description="Game playing utility")
    
    parser.add_argument(
        "--agent",
        type=str,
        choices=["ollama", "huggingface", "remote", "manual"],
        default="ollama",
        help="Type of agent to use (default: ollama)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    # Create subparsers for different game types
    subparsers = parser.add_subparsers(dest="game_type", required=True)

    # Pokemon subcommand
    pokemon_parser = subparsers.add_parser("pokemon", help="Play Pokemon game")
    pokemon_parser.add_argument(
        "rom_path",
        type=str,
        help="Path to the Pokemon ROM file"
    )

    # Text adventure subcommand
    text_adventure_parser = subparsers.add_parser("text-adventure", help="Play text adventure game")

    return parser.parse_args()

def run_game(args):
    env_args = {
        "env_type": args.game_type,
        "env_args": {
            "debug": args.debug,
        }
    }

    if args.game_type == "pokemon":
        env_args["env_args"]["rom_path"] = args.rom_path


    if args.agent != "manual":
        agent_args = {
            "agent_type": args.agent,
            "agent_args": {
                "debug": args.debug
            }
        }
        agent = agent_factory(agent_args)
    else:
        agent = None

    game_environment = enviroment_factory(env_args)
    game_environment.run(agent)

if __name__ == "__main__":
    args = parse_args()
    run_game(args)