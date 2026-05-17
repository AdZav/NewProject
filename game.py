import pygame
import random
from player import *
from wall import Wall
from enemy import Enemy
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

INITIAL_PLAYER_X = 2
INITIAL_PLAYER_Y = 5

class Game:
    def __init__(self, _width, _height, _caption):
        self.width = _width
        self.height = _height
        self.caption = _caption
        self.tile_cols = 10
        self.tile_rows = 10
        self.tile_width = self.width / self.tile_cols
        self.tile_height = self.height / self.tile_rows

        self.clock = pygame.time.Clock()
        self.running = True

        # GAME SETUP    
        self._setup_pygame()
        self._init_game_objects()

    def run_game_loop(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self._update()
            self._draw()
    
    def _init_game_objects(self):
        self.map = []
        for _ in range(self.tile_cols):
            new_col = []
            for _ in range(self.tile_rows):
                new_col.append(0)
            self.map.append(new_col)
            self.map = [[0] * self.tile_rows for _ in range(self.tile_cols)]
        self.player = Player(INITIAL_PLAYER_X, INITIAL_PLAYER_Y, self.tile_width, self.tile_height)
        self.map[INITIAL_PLAYER_X][INITIAL_PLAYER_Y] = self.player
        self.enemies = []
        self._generate_level()

    def _generate_level(self, num_internal_walls = 10, num_enemies = 3):

        for col in range(self.tile_cols):
            # first col
            self.map[col][0] = Wall(col, 0, self.tile_width, self.tile_height)

            # last col
            self.map[col][self.tile_cols - 1] = Wall(col, self.tile_cols - 1, self.tile_width, self.tile_height)

        for row in range(self.tile_rows):
            # first row
            self.map[0][row] = Wall(0, row, self.tile_width, self.tile_height)

            # last row
            self.map[self.tile_rows - 1][row] = Wall(self.tile_cols - 1, row, self.tile_width, self.tile_height)
        
        for _ in range(num_internal_walls):
            x = random.randint(1, self.tile_cols - 2)
            y = random.randint(1, self.tile_rows - 2)
            
            while self.map[x][y] != 0:
                x = random.randint(1, self.tile_cols - 2)
                y = random.randint(1, self.tile_rows - 2)

        for _ in range(num_enemies):
            minx_tile_spawn_range = 3
            maxx_tile_spawn_range = self.tile_rows - 1
            miny_tile_spawn_range = 1
            maxy_tile_spawn_range = self.tile_cols - 1

            enemy_x, enemy_y = self.find_free_tile(minx_tile_spawn_range, maxx_tile_spawn_range, miny_tile_spawn_range, maxy_tile_spawn_range)
            enemy = Enemy(enemy_x, enemy_y, self.tile_width, self.tile_height)
            self.map[enemy_x][enemy_y] = enemy
            self.enemies.append(enemy)

            self.map[x][y] = Wall(x, y, self.tile_width, self.tile_height)
    def find_free_tile(self, minx, maxx, miny, maxy):
        while True:
            check_x = random.randint(minx, maxx)
            check_y = random.randint(miny, maxy)
            if self.map[check_x][check_y] == 0:
                return check_x, check_y

            
       
    def _setup_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.player:
                moved = self.player.handle_input(event, self.map, self.tile_cols, self.tile_rows)
                if moved:
                    for enemy in self.enemies:
                        enemy.take_turn(self.map, self.tile_cols, self.tile_rows)
    
    def _draw(self):
        self.screen.fill(WHITE)
        
        for col in range(self.tile_cols):
            for row in range(self.tile_rows):
                if isinstance(self.map[col][row], Wall):
                    self.map[col][row].draw(self.screen)
                rect = (col * self.tile_width, row * self.tile_height, self.tile_width, self.tile_height)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)

        pygame.display.update()

    def _update(self):
        pass
        self.player.update()
        for enemy in self.enemies:
            enemy.update()