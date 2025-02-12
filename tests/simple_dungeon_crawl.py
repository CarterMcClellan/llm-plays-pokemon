from typing import NamedTuple
from keystroke_listener import ModernKeyboardListener, echo_disabled

class Position(NamedTuple):
    x: int
    y: int

class DungeonGame:
    def __init__(self):
        # Initialize the map with walls (o), walkable paths (w), and player (p)
        self.map = [
            ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
            ['o', 'w', 'w', 'w', 'w', 'w', 'w', 'o'],
            ['o', 'w', 'w', 'w', 'w', 'w', 'w', 'o'],
            ['o', 'w', 'w', 'w', 'w', 'w', 'w', 'o'],
            ['o', 'w', 'w', 'w', 'w', 'w', 'w', 'o'],
            ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o']
        ]
        # Starting player position
        self.current_position = Position(1, 1)
        self.previous_position = Position(1, 1)
        
    def render(self):
        # Update the map with player position
        temp_map = [list(row) for row in self.map]
        temp_map[self.previous_position.y][self.previous_position.x] = "w"
        temp_map[self.current_position.y][self.current_position.x] = "p"
        
        # Convert the map to a string and print
        map_str = '\n'.join([''.join(row) for row in temp_map])
        print(f"\033[H\033[J{map_str}", flush=True)  # ANSI escape codes to clear screen and move cursor home

    def is_valid_move(self, x, y):
        # Check if the position is within bounds and is walkable
        if (0 <= y < len(self.map) and 
            0 <= x < len(self.map[0]) and 
            self.map[y][x] == 'w'):
            return True
        return False
    
    def update(self, key):
        new_x, new_y = self.current_position.x, self.current_position.y
        
        if key == 'up':
            new_y -= 1
        elif key == 'down':
            new_y += 1
        elif key == 'left':
            new_x -= 1
        elif key == 'right':
            new_x += 1

        valid = self.is_valid_move(new_x, new_y)
        if valid:
            self.previous_position = self.current_position
            self.current_position = Position(new_x, new_y)
            self.render()

    def run(self):
        def handle_key_event(event):
            # print(f"Key {event['type']}: {event['name']} (keycode: {event['keycode']})")
            if event['type'] == 'down':
                if event['name'] == 'escape':
                    self.listener.stop()
                elif event['name'] in ['up', 'down', 'left', 'right']:
                    self.update(event['name'])

        with echo_disabled():
            self.listener = ModernKeyboardListener(handle_key_event)
            self.render()
            self.listener.run()

if __name__ == "__main__":
    game = DungeonGame()
    game.run()