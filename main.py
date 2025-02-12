import argparse
import os
import time
from dotenv import load_dotenv
import numpy as np
# import keyboard

load_dotenv()

def parse_args():
    parser = argparse.ArgumentParser(description="Pokemon Red/Blue utility")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ROM command
    rom_parser = subparsers.add_parser("rom", help="Run a GameBoy ROM file")
    rom_parser.add_argument("path", type=str, help="Path to the GameBoy ROM file")
    rom_parser.add_argument(
        "--headless", action="store_true", help="Run in headless mode without GUI"
    )
    rom_parser.add_argument(
        "--manual",
        action="store_true",
        help="Enable manual control instead of AI agent",
    )
    rom_parser.add_argument(
        "--agent",
        type=str,
        choices=["ollama", "huggingface", "remote"],
        default="ollama",
        help="Type of agent to use (default: ollama)",
    )

    # RAM analysis command
    ram_parser = subparsers.add_parser("ram", help="Analyze a RAM dump file")
    ram_parser.add_argument("path", type=str, help="Path to RAM dump file (*.gbc.ram)")

    return parser.parse_args()


def analyze_ram(ram_file):
    """
    long term I would like this function to be able to edit sram and create interesting save states to test the
    agent... see the notebook which I have started working on.
    """
    pass


def run_game(rom_path, headless, manual, agent_type="ollama"):
    from pyboy import PyBoy
    from game_enviroment import GameEnviroment
    from agent import OllamaAgent, HuggingFaceAgent, RemoteAgent
    import logging

    head = "null" if headless else "SDL2"
    debug = True
    logging.info(f"Running game with debug: {debug}")
    if debug:
        pyboy = PyBoy(rom_path, window=head, log_level="DEBUG")
    else:
        pyboy = PyBoy(rom_path, window=head)

    game_enviroment = GameEnviroment(pyboy=pyboy, debug=debug)
    
    if agent_type == "remote":
        agent = RemoteAgent(debug=debug)
    elif agent_type == "ollama":
        agent = OllamaAgent(debug=debug)
    else:
        agent = HuggingFaceAgent(debug=debug)

    if not manual:
        while True:
            state = game_enviroment.get_game_state()
            action = agent.get_llm_action(state.screen, state.available_actions)
            game_enviroment.take_action(action)
            if not pyboy.tick():
                break
    else:
        while pyboy.tick():
            pass
            # if keyboard.is_pressed("q"):
            #     game_enviroment.take_screen_shot(as_np=True)

    pyboy.stop()


if __name__ == "__main__":
    args = parse_args()

    if args.command == "ram":
        analyze_ram(args.path)
    elif args.command == "rom":
        run_game(
            args.path, 
            args.headless, 
            args.manual,
            args.agent
        )
    else:
        print("Please specify a command. Use --help for more information.")
