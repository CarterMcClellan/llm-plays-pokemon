import numpy as np
from pyboy import PyBoy
from consts.moves import MOVE_MAP
from consts.types import TYPE_MAP

class PokemonGameState:
    """
    Utility class for reading and displaying Pokemon Red game state information.
    Provides methods to access memory locations and interpret game data.
    """

    def __init__(self, pyboy: PyBoy):
        self.pyboy = pyboy
        
        # Memory address constants
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
            5: self.PARTY_SIZE_ADDR + 0xE4
        }
        
        self.BADGE_ADDR = 0xD356
        self.POSITION_ADDRS = {
            'x': 0xD362,
            'y': 0xD361,
            'map': 0xD35E
        }

        # Add new memory addresses for game state detection
        self.BATTLE_STATE_ADDR = 0xD057  # Battle state indicator
        self.MENU_STATE_ADDR = 0xD35E    # Current map/menu state
        
    def read_memory(self, addr: int) -> int:
        """Read a single byte from memory at the given address."""
        return self.pyboy.memory[addr]
    
    def get_position(self) -> tuple:
        """Returns current (x, y, map) position."""
        return (
            self.read_memory(self.POSITION_ADDRS['x']),
            self.read_memory(self.POSITION_ADDRS['y']),
            self.read_memory(self.POSITION_ADDRS['map'])
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
    
    def get_game_state(self) -> str:
        """
        Returns the current game state/context.
        Possible states include: battle, menu, overworld, etc.
        """
        if self.is_in_battle():
            return "battle"
            
        # Map value can indicate menus and special states
        map_value = self.read_memory(self.MENU_STATE_ADDR)
        
        # You can add more specific menu detection based on map values
        # These would need to be verified with testing
        if map_value == 0:
            return "menu"
        else:
            return "overworld"
    
    def _read_two_bytes(self, addr: int) -> int:
        """Helper method to read a 2-byte value from memory."""
        low_byte = self.read_memory(addr)
        high_byte = self.read_memory(addr + 1)
        # result = low_byte + (high_byte << 8)
        result = high_byte + (low_byte << 8)
        return result
    
    def _read_three_bytes(self, addr: int) -> int:
        """Helper method to read a 3-byte value from memory."""
        low_byte = self.read_memory(addr)
        mid_byte = self.read_memory(addr + 1)
        high_byte = self.read_memory(addr + 2)
        result = high_byte + (low_byte << 16) + (mid_byte << 8)
        return result

    def get_pokemon_data(self, slot: int) -> dict:
        """
        Returns complete data structure for a Pokemon in the given party slot (0-5).

        The information for all these offsets can be found here:
        https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_(Generation_I)
        """
        if slot >= 6 or slot < 0:
            raise ValueError(f"Invalid party slot: {slot}")
            
        base_addr = self.PARTY_POKEMON_STRUCTURES[slot]
        
        return {
            'species': self.read_memory(base_addr + 0x00),
            'current_hp': self._read_two_bytes(base_addr + 0x01),
            'level': self.read_memory(base_addr + 0x03),
            'status': self.read_memory(base_addr + 0x04),
            'type1': TYPE_MAP[self.read_memory(base_addr + 0x05)],
            'type2': TYPE_MAP[self.read_memory(base_addr + 0x06)],
            'catch_rate': self.read_memory(base_addr + 0x07),
            'moves': [
                MOVE_MAP[self.read_memory(base_addr + 0x08)],
                MOVE_MAP[self.read_memory(base_addr + 0x09)],
                MOVE_MAP[self.read_memory(base_addr + 0x0A)],
                MOVE_MAP[self.read_memory(base_addr + 0x0B)]
            ],
            'trainer_id': self._read_two_bytes(base_addr + 0x0C),
            'experience': self._read_three_bytes(base_addr + 0x0E),
            'stat_exp': {
                'hp': self._read_two_bytes(base_addr + 0x11),
                'attack': self._read_two_bytes(base_addr + 0x13),
                'defense': self._read_two_bytes(base_addr + 0x15),
                'speed': self._read_two_bytes(base_addr + 0x17),
                'special': self._read_two_bytes(base_addr + 0x19)
            },
            'iv_data': self._read_two_bytes(base_addr + 0x1B),
            'pp': [
                self.read_memory(base_addr + 0x1D),
                self.read_memory(base_addr + 0x1E),
                self.read_memory(base_addr + 0x1F),
                self.read_memory(base_addr + 0x20)
            ],
            'stats': {
                'level': self.read_memory(base_addr + 0x21),
                'max_hp': self._read_two_bytes(base_addr + 0x22),
                'attack': self._read_two_bytes(base_addr + 0x24),
                'defense': self._read_two_bytes(base_addr + 0x26),
                'speed': self._read_two_bytes(base_addr + 0x28),
                'special': self._read_two_bytes(base_addr + 0x2A)
            }
        }

    def print_game_state(self):
        """Prints current game state information."""
        x, y, map_n = self.get_position()
        print("\n=== Pokemon Red Game State ===")
        print(f"Position: Map {map_n} at ({x}, {y})")
        print(f"Party Size: {self.get_party_size()}")
        print(f"Badges: {self.get_badge_count()}")
        
        # Add game state context
        print(f"Game State: {self.get_game_state()}")
        print(f"In Battle: {self.is_in_battle()}")
        
        print("\nDetailed Party Pokemon Information:")
        for i in range(self.get_party_size()):
            pokemon = self.get_pokemon_data(i)
            print(f"\nPokemon {i+1} (Species #{pokemon['species']}):")
            print(f"  Level: {pokemon['level']}")
            print(f"  HP: {pokemon['current_hp']}/{pokemon['stats']['max_hp']}")
            print(f"  Types: {pokemon['type1']}/{pokemon['type2']}")
            print(f"  Stats:")
            print(f"    Attack:  {pokemon['stats']['attack']}")
            print(f"    Defense: {pokemon['stats']['defense']}")
            print(f"    Speed:   {pokemon['stats']['speed']}")
            print(f"    Special: {pokemon['stats']['special']}")
            print(f"  Moves: {pokemon['moves']}")
            print(f"  PP: {pokemon['pp']}") 