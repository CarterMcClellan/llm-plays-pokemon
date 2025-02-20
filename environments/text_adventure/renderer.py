import pygame
from .game import TextAdventureGame

class PygameRenderer:
    def __init__(self, game: TextAdventureGame):
        pygame.init()
        self.game = game
        self.tile_size = 50
        self.width = len(game.map[0]) * self.tile_size
        self.height = len(game.map) * self.tile_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Text Adventure")
        
        self.colors = {
            'w': (200, 200, 200),  # walkable - light gray
            'o': (100, 100, 100),  # wall - dark gray
            'p': (0, 255, 0),      # player - green
        }

    def render(self):
        self.screen.fill((0, 0, 0))
        self.game.map[self.game.previous_position.y][self.game.previous_position.x] = "w"
        self.game.map[self.game.current_position.y][self.game.current_position.x] = "p"
        
        for y, row in enumerate(self.game.map):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    x * self.tile_size, 
                    y * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                )
                pygame.draw.rect(self.screen, self.colors[tile], rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
        
        pygame.display.flip()