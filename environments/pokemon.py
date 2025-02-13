from agents.base import BaseAgent
from pyboy import PyBoy
from pyboy import WindowEvent
from typing import List, Any, NamedTuple

from consts.maps import MAP_CONST
from consts.moves import MOVE_MAP
from consts.species import SPECIES_MAP
from consts.status_effect import STATUS_EFFECT_MAP
from consts.types import TYPE_MAP
from base import GameAction, GameState, GameEnvironment

class PokemonGameAction(GameAction):
    A = (WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A)
    B = (WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B)
    UP = (WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP)
    DOWN = (WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN)
    LEFT = (WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT)
    RIGHT = (WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT)
    START = (WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START)

    @classmethod
    def get_all_actions(cls) -> List["PokemonGameAction"]:
        return [cls.A, cls.B, cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT, cls.START]

    def __repr__(self):
        return self.name.lower()

class PokemonGameState(GameState):
    @classmethod
    def create(cls, available_actions: List[PokemonGameAction], screen: Any) -> "PokemonGameState":
        return cls(available_actions=available_actions, screen=screen)
    
class PokemonGameEnviromentArgs(NamedTuple):
    headless: bool
    debug: bool
    rom_path: str

    @classmethod
    def create(cls, args: dict) -> "PokemonGameEnviromentArgs":
        if any([req not in args for req in ["headless", "debug", "rom_path"]]):
            raise ValueError("Missing required arguments")

        return cls(
            headless=args["headless"],
            debug=args["debug"],
            rom_path=args["rom_path"]
        )

class PokemonGameEnviroment(GameEnvironment):
    """
    Utility class for reading and displaying Pokemon Red game state information.
    Provides methods to access memory locations and interpret game data.
    """

    def __init__(self, args: PokemonGameEnviromentArgs):
        headless = args.headless
        debug = args.debug
        head = "null" if headless else "SDL2"
        rom_path = args.rom_path
        if debug:
            self.pyboy = PyBoy(rom_path, window=head, log_level="DEBUG")
        else:
            self.pyboy = PyBoy(rom_path, window=head)

        # All of these random addresses come from the symbol file
        # https://github.com/pret/pokered/blob/symbols/pokered.sym
        self.PARTY_SIZE_ADDR = 0xD163
        self.PARTY_SPECIES_START = 0xD164

        # Add Pokemon structure base addresses
        # plus 0x08 for first pokemon,
        # second = 44 bytes + first pokemon
        # third = 44 bytes + second pokemon
        # etc...
        self.PARTY_POKEMON_STRUCTURES = {
            0: self.PARTY_SIZE_ADDR + 0x08,
            1: self.PARTY_SIZE_ADDR + 0x34,
            2: self.PARTY_SIZE_ADDR + 0x60,
            3: self.PARTY_SIZE_ADDR + 0x8C,
            4: self.PARTY_SIZE_ADDR + 0xB8,
            5: self.PARTY_SIZE_ADDR + 0xE4,
        }

        self.BADGE_ADDR = 0xD356
        self.POSITION_ADDRS = {"x": 0xD362, "y": 0xD361, "map": 0xD35E}

        # Add new memory addresses for game state detection
        self.BATTLE_STATE_ADDR = 0xD057  # Battle state indicator
        self.MENU_STATE_ADDR = 0xD35E  # Current map/menu state

        # Action frequency - How many ticks to wait between actions
        self.ACTION_FREQ = 10

    def read_memory(self, addr: int) -> int:
        """Read a single byte from memory at the given address."""
        return self.pyboy.memory[addr]

    def get_position(self) -> tuple:
        """Returns current (x, y, map) position."""
        return (
            self.read_memory(self.POSITION_ADDRS["x"]),
            self.read_memory(self.POSITION_ADDRS["y"]),
            self.read_memory(self.POSITION_ADDRS["map"]),
        )

    def get_party_size(self) -> int:
        """Returns number of Pokemon in party."""
        return self.read_memory(self.PARTY_SIZE_ADDR)

    def get_badge_count(self) -> int:
        """Returns number of badges obtained."""
        return bin(self.read_memory(self.BADGE_ADDR)).count("1")

    def is_in_battle(self) -> bool:
        """Returns True if currently in a battle, False otherwise."""
        return self.read_memory(self.BATTLE_STATE_ADDR) != 0

    def get_game_state(self) -> GameState:
        """ 
        Returns the current game state.
        """
        screen = self.pyboy.screen.image

        return GameState(
            available_actions=[
                GameAction.A,
                GameAction.B,
                GameAction.UP,
                GameAction.DOWN,
                GameAction.LEFT,
                GameAction.RIGHT,
                GameAction.START,
            ],
            screen=screen,
        )

    def _read_two_bytes(self, addr: int) -> int:
        """Helper method to read a 2-byte value from memory."""
        low_byte = self.read_memory(addr)
        high_byte = self.read_memory(addr + 1)
        result = high_byte + (low_byte << 8)
        return result

    def _read_three_bytes(self, addr: int) -> int:
        """Helper method to read a 3-byte value from memory."""
        low_byte = self.read_memory(addr)
        mid_byte = self.read_memory(addr + 1)
        high_byte = self.read_memory(addr + 2)
        result = high_byte + (low_byte << 16) + (mid_byte << 8)
        return result

    def get_party_data(self, slot: int) -> dict:
        """
        Returns complete data structure for a Pokemon in the given party slot (0-5).

        The information for all these offsets can be found here:
        https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_(Generation_I)
        """
        if slot >= 6 or slot < 0:
            raise ValueError(f"Invalid party slot: {slot}")

        base_addr = self.PARTY_POKEMON_STRUCTURES[slot]

        return {
            "species": self.read_memory(base_addr + 0x00),
            "current_hp": self._read_two_bytes(base_addr + 0x01),
            "level": self.read_memory(base_addr + 0x03),
            "status": self.read_memory(base_addr + 0x04),
            "type1": TYPE_MAP[self.read_memory(base_addr + 0x05)],
            "type2": TYPE_MAP[self.read_memory(base_addr + 0x06)],
            "catch_rate": self.read_memory(base_addr + 0x07),
            "moves": [
                MOVE_MAP[self.read_memory(base_addr + 0x08)],
                MOVE_MAP[self.read_memory(base_addr + 0x09)],
                MOVE_MAP[self.read_memory(base_addr + 0x0A)],
                MOVE_MAP[self.read_memory(base_addr + 0x0B)],
            ],
            "trainer_id": self._read_two_bytes(base_addr + 0x0C),
            "experience": self._read_three_bytes(base_addr + 0x0E),
            "stat_exp": {
                "hp": self._read_two_bytes(base_addr + 0x11),
                "attack": self._read_two_bytes(base_addr + 0x13),
                "defense": self._read_two_bytes(base_addr + 0x15),
                "speed": self._read_two_bytes(base_addr + 0x17),
                "special": self._read_two_bytes(base_addr + 0x19),
            },
            "iv_data": self._read_two_bytes(base_addr + 0x1B),
            "pp": [
                self.read_memory(base_addr + 0x1D),
                self.read_memory(base_addr + 0x1E),
                self.read_memory(base_addr + 0x1F),
                self.read_memory(base_addr + 0x20),
            ],
            "stats": {
                "level": self.read_memory(base_addr + 0x21),
                "max_hp": self._read_two_bytes(base_addr + 0x22),
                "attack": self._read_two_bytes(base_addr + 0x24),
                "defense": self._read_two_bytes(base_addr + 0x26),
                "speed": self._read_two_bytes(base_addr + 0x28),
                "special": self._read_two_bytes(base_addr + 0x2A),
            },
        }

    def get_battle_data(self) -> dict:
        return {
            "opponent_species": self.read_memory(0xD058),
            "opponent_level": self.read_memory(0xD059),
            "opponent_hp": self._read_two_bytes(0xD05A),
            "opponent_max_hp": self._read_two_bytes(0xD05C),
        }

    def print_game_state(self):
        """Prints current game state information."""
        x, y, map_n = self.get_position()
        print("\n=== Pokemon Red Game State ===")
        print(f"Position: Map {MAP_CONST[map_n]} at ({x}, {y})")
        print(f"Badges: {self.get_badge_count()}")

        if self.is_in_battle():
            battle_data = self.get_battle_data()
            print("Opponent Pokemon:")
            print(f"  Species: {SPECIES_MAP[battle_data['opponent_species']]}")
            print(f"  Level: {battle_data['opponent_level']}")
            print(
                f"  HP: {battle_data['opponent_hp']}/{battle_data['opponent_max_hp']}"
            )

        print("\nDetailed Party Pokemon Information:")
        print(f"Party Size: {self.get_party_size()}")
        for i in range(self.get_party_size()):
            pokemon = self.get_party_data(i)
            print(f"\nParty Slot {i+1}")
            print(f"  Pokemon: {SPECIES_MAP[pokemon['species']]}")
            print(f"  Types:   {pokemon['type1']}/{pokemon['type2']}")
            print(f"  Level:   {pokemon['stats']['level']}")
            print(f"  HP:      {pokemon['current_hp']}/{pokemon['stats']['max_hp']}")
            print(f"  Status:  {STATUS_EFFECT_MAP[pokemon['status']]}")
            print(f"  Stats:")
            print(f"    Attack:    {pokemon['stats']['attack']}")
            print(f"    Defense:   {pokemon['stats']['defense']}")
            print(f"    Speed:     {pokemon['stats']['speed']}")
            print(f"    Special:   {pokemon['stats']['special']}")
            print(f"  Moves: {pokemon['moves']}")
            print(f"  PP: {pokemon['pp']}")


    def take_action(self, action: GameAction):
        (press, release) = action.value
        self.pyboy.send_input(press)
        press_step = 8
        # render = self.save_video or not self.headless
        render = not self.headless
        self.pyboy.tick(press_step)
        self.pyboy.send_input(release)
        self.pyboy.tick(self.ACTION_FREQ - press_step - 1, render)
        self.pyboy.tick(1, True)

    def get_system_prompt(self):
        return """
        You are a pokemon trainer.
        """

    def run(self, agent: BaseAgent):
        while True:
            game_state = self.get_game_state()
            action = agent.get_action(game_state)
            self.take_action(action)
