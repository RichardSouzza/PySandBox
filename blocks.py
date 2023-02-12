import pygame
from assets.colors import colors


class Block:
    def __init__(self, type, color, fall):
        self.type = type
        self.color = color
        self.fall = fall
    
    def collision_y(self, blocks_list, align=False):
        for block in blocks_list:
            if self.rect.bottom >= block.rect.top:
                if align:
                    self.rect.bottom = block.rect.top
                    if type(block) == Water and type(self) != Water:
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
        super().__init__("solid", colors["earth"], True)


class Eraser(Block):
    def __init__(self):
        super().__init__("eraser", colors["white"], False)


class Sand(Block):
    def __init__(self):
        super().__init__("solid", colors["sand"], True)


class Stone(Block):
    def __init__(self):
        super().__init__("solid", colors["stone"], False)


class Water(Block):
    def __init__(self):
        super().__init__("liquid", colors["water"], True)
