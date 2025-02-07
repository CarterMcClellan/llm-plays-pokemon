from pyboy import PyBoy
from pokemon_game_state import PokemonGameState
from pokemon_action_handler import PokemonActionHandler

if __name__ == "__main__":
    headless = False
    gb_path = "red.gbc"
    head = "null" if headless else "SDL2"
    pyboy = PyBoy(gb_path, window=head)

    game_state = PokemonGameState(pyboy)
    action_handler = PokemonActionHandler(pyboy)

    while pyboy.tick():
        game_state.print_game_state()

    pyboy.stop()

    # while True:
    #     game_state.print_game_state()
    #     time.sleep(1)
