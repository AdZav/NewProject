import os
import pygame
import random
from gameobject import GameObject
from spritesheet import load_spritesheet, Animation

RED = (255, 0, 0)
MOVE_FRAMES = 10  # how many frames to cross one tile
# Path to enemy sprite assets (relative to this file)
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets", "3 Dude_Monster")

class Enemy(GameObject):
    def __init__(self, gridx, gridy, tile_width, tile_height, color=RED):
        # Calculate the initial position manually using grid system tiles
        x = gridx * tile_width
        y = gridy * tile_height
        super().__init__(gridx, gridy, x, y, tile_width, tile_height, color)

        # Movement animation
        self.move_speed = tile_width / MOVE_FRAMES # how much distance to cover each frame

        ### Sprite animations
        scale = (tile_width, tile_height)
        self.animations = {
            "idle": Animation(load_spritesheet(os.path.join(ASSET_DIR, "Dude_Monster_Idle_4.png"), 32, 32, scale), speed=8),
            "walk": Animation(load_spritesheet(os.path.join(ASSET_DIR, "Dude_Monster_Walk_6.png"), 32, 32, scale), speed=max(1, MOVE_FRAMES // 6)),
        }
        self.current_animation = "idle"
        self.direction = "right"
        self.is_moving = False

    def draw(self, surface):
        frame = self.animations[self.current_animation].get_frame()
        # Flip horizontally when facing left
        if self.direction == "left":
            frame = pygame.transform.flip(frame, True, False)
        surface.blit(frame, (self.x, self.y))
    
    def update(self):
        ## Set target x and y
        target_x = self.gridx * self.tile_width
        target_y = self.gridy * self.tile_height

        # check if we are before or after target x
        if self.x < target_x:
            self.x = min(self.x + self.move_speed, target_x)

        elif self.x > target_x:  
            self.x = max(self.x - self.move_speed, target_x)

        # check if we are before or after target y
        if self.y < target_y:
            self.y = min(self.y + self.move_speed, target_y)
        elif self.y > target_y:
            self.y = max(self.y - self.move_speed, target_y)

        # Determine if still moving and pick the right animation
        self.is_moving = (self.x != target_x or self.y != target_y)
        if self.is_moving:
            if self.current_animation != "walk":
                self.current_animation = "walk"
                self.animations["walk"].reset()
            self.animations["walk"].tick()
        else:
            if self.current_animation != "idle":
                self.current_animation = "idle"
                self.animations["idle"].reset()
            self.animations["idle"].tick()

            
    def take_turn(self, game_map, tile_cols, tile_rows):
        # Enemy takes a turn
        self._move_random_adjacent(game_map, tile_cols, tile_rows)

    def _move_random_adjacent(self, game_map, tile_cols, tile_rows):
        # Create list of direction options for the enemy
        directions = [(0, -1), # move down
                      (0, 1), # move up
                      (-1, 0), # move left
                      (1, 0)] # move right


        # shuffle the direction list
        random.shuffle(directions)

        # iterate through the direction tuple list, move on the first one that is free
        for dx, dy in directions:
            new_gridx = self.gridx + dx
            new_gridy = self.gridy + dy

            # check within boundaries
            if 0 <= new_gridx < tile_rows and 0 <= new_gridy < tile_cols:

                if game_map[new_gridx][new_gridy] == 0:
                    # Update the new position and clear the previous one on the map for the player
                    game_map[new_gridx][new_gridy] = game_map[self.gridx][self.gridy]
                    game_map[self.gridx][self.gridy] = 0

                    ## Track facing direction for sprite flipping
                    if dx < 0:
                        self.direction = "left"
                    elif dx > 0:
                        self.direction = "right"

                    self.gridx = new_gridx
                    self.gridy = new_gridy
                    break            