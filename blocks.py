import pygame
from assets.colors import colors


class Block:
    def __init__(self, color, fall):
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


class Air(Block):
    def __init__(self):
        super().__init__(colors["white"], False)


class Earth(Block):
    def __init__(self):
        super().__init__(colors["earth"], True)


class Sand(Block):
    def __init__(self):
        super().__init__(colors["sand"], True)


class Stone(Block):
    def __init__(self):
        super().__init__(colors["stone"], False)


class Water(Block):
    def __init__(self):
        super().__init__(colors["water"], True)
