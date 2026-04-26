from abc import ABC, abstractmethod

GREEN = (0, 255, 0)

class GameObject(ABC):
    def __init__(self, gridx, gridy, x, y, tile_width, tile_height, color):
        self.gridx = gridx
        self.y = gridy
        

 