import pygame

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game:
    def __init__(self, _width, _height, _caption):
        self.width = _width
        self.height = _height
        self.caption = _caption

        self.clock = pygame.time.Clock()
        self.running = True
        self._setup_pygame()

    def run_game_loop(self):
        while self.running:
            self.clock.tick(FPS)