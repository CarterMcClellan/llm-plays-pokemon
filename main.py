import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Pokemon Red/Blue utility")
    parser.add_argument("--rom", type=str, help="Path to the GameBoy ROM file to run")
    parser.add_argument(
        "--headless", action="store_true", help="Run in headless mode without GUI"
    )
    parser.add_argument(
        "--ram-file", type=str, help="Path to RAM dump file (*.gbc.ram) to analyze"
    )
    return parser.parse_args()


def analyze_ram(ram_file):
    """
    long term I would like this function to be able to edit sram and create interesting save states to test the
    agent... see the notebook which I have started working on.
    """
    pass

def run_game(rom_path, headless):
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
    
    # while pyboy.tick():
    while True:
        state = game_enviroment.get_game_state()
        action = agent.get_llm_action(state.screen, state.available_actions)
        game_enviroment.take_action(action)

    pyboy.stop()


if __name__ == "__main__":
    args = parse_args()

    if args.ram_file:
        analyze_ram(args.ram_file)
    elif args.rom:
        run_game(args.rom, args.headless)
    else:
        print(
            "Please specify either --rom to run the game or --ram-file to analyze RAM"
        )
