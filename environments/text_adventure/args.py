class TextAdventureGameEnvironmentArgs:
    def __init__(self, map_size: int = 8, debug: bool = False):
        self.map_size = map_size
        self.debug = debug