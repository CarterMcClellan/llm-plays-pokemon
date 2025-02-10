import argparse


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


def run_game(rom_path, headless, manual):
    from pyboy import PyBoy
    from game_enviroment import GameEnviroment
    from agent import PokemonLLMAgent

    head = "null" if headless else "SDL2"
    debug = False
    if debug:
        pyboy = PyBoy(rom_path, window=head, log_level="DEBUG")
    else:
        pyboy = PyBoy(rom_path, window=head)

    game_enviroment = GameEnviroment(pyboy)
    agent = PokemonLLMAgent()

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

    pyboy.stop()


if __name__ == "__main__":
    args = parse_args()

    if args.command == "ram":
        analyze_ram(args.path)
    elif args.command == "rom":
        run_game(args.path, args.headless, args.manual)
    else:
        print("Please specify a command. Use --help for more information.")
