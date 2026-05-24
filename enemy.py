import pygame
from gameobject import GameObject
import random

from player import MOVE_FRAMES

RED = (255, 0, 0)
class Enemy(GameObject):
    def __init__(self, gridx, gridy, tile_width, tile_height, color = RED):
        x = gridx * tile_width
        y = gridy * tile_height
        super().__init__(gridx, gridy, x, y, tile_width, tile_height, color)
        self.move_speed = tile_width / MOVE_FRAMES
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.tile_width, self.tile_height))
    def update(self):
        target_x = self.gridx * self.tile_width
        target_y = self.gridy * self.tile_height

        if self.x < target_x:
            self.x = min(self.x + self.move_speed, target_x)
        elif self.x > target_x:
            self.x = max(self.x - self.move_speed, target_x)
        
        if self.y < target_y:
            self.y = min(self.y + self.move_speed, target_y)
        elif self.y > target_y:
            self.y = max(self.y - self.move_speed, target_y)
    
    def take_turn(self, game_map, tile_cols, tile_rows):
        self._move_random_adjacent(game_map, tile_cols, tile_rows)
    
    def _move_random_adjacent(self, game_map, tile_cols, tile_rows):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_gridx = self.gridx + dx
            new_gridy = self.gridy + dy

            if 0 <= new_gridx < tile_cols and 0 <= new_gridy < tile_rows:
                if game_map[new_gridx][new_gridy] == 0:
                    game_map[new_gridx][new_gridy] = game_map[self.gridx][self.gridy]
                    game_map[self.gridx][self.gridy] = 0
                    self.gridx = new_gridx
                    self.gridy = new_gridy
                    break