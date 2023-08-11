import pygame
from pysandbox.colors import *


class Block:
    def __init__(self, type, color, fall):
        self.type = type
        self.color = color
        self.fall = fall
    
    def collision_y(self, blocks_list, align=False):
        for block in blocks_list:
            if self.col == block.col:
                if self.rect.bottom >= block.rect.top:
                    if align:
                        self.rect.bottom = block.rect.top
                        if block.type == "liquid" and self.type != "liquid":
                            initial_y = self.rect.y
                            self.rect.y = block.rect.y
                            block.rect.y = initial_y 
                    return True
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def move_y(self, distance, blocks_list):
        collision = self.collision_y(blocks_list, align=True)
        if not collision:
            self.rect.y += distance
    
    def set_rect(self, col, row, x, y, size):
        self.rect = pygame.rect.Rect((x, y, size, size))
        self.col = col
        self.row = row


class Earth(Block):
    def __init__(self):
        super().__init__("solid", EARTH_COLOR, True)


class Eraser(Block):
    def __init__(self):
        super().__init__("eraser", WHITE, False)


class Sand(Block):
    def __init__(self):
        super().__init__("solid", SAND_COLOR, True)


class Stone(Block):
    def __init__(self):
        super().__init__("solid", STONE_COLOR, False)


class Water(Block):
    def __init__(self):
        super().__init__("liquid", WATER_COLOR, True)
