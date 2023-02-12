import pygame
from pygame.locals import *
from assets.colors import colors
from blocks import Earth, Eraser, Sand, Stone, Water


class BlocksBar:
    def __init__(self, root, x, y, size_hint_x, size_hint_y):
        self.root = root
        self.width = root.width * size_hint_x
        self.height = root.height * size_hint_y
        self.screen = root.screen.subsurface(x, y, self.width, self.height)
        self.bg_color = colors["bg_color"]
        self.border_width = round(self.height * 0.15)
        self.current_block = Sand
        self.make_columns()
        self.build()
    
    def build(self):
        self.keys = {K_1: 1, K_2: 2, K_3: 3, K_4: 4}
        
        self.sand_button = Button(
            Sand,
            colors["sand"],
            colors["dark_sand"],
            self.cols[0], round(self.border_width / 2),
            self.cols_width,
            self.height - self.border_width
        )
        self.earth_button = Button(
            Earth,
            colors["earth"],
            colors["dark_earth"],
            self.cols[1], round(self.border_width / 2),
            self.cols_width,
            self.height - self.border_width
        )
        self.stone_button = Button(
            Stone,
            colors["stone"],
            colors["dark_stone"],
            self.cols[2], round(self.border_width / 2),
            self.cols_width,
            self.height - self.border_width
        )
        self.water_button = Button(
            Water,
            colors["water"],
            colors["dark_water"],
            self.cols[3], round(self.border_width / 2),
            self.cols_width,
            self.height - self.border_width
        )
        self.eraser_button = Button(
            Eraser,
            colors["white"],
            colors["dark_white"],
            self.cols[4], round(self.border_width / 2),
            self.cols_width,
            self.height - self.border_width
        )
        self.buttons = {}
        self.buttons["sand"] = self.sand_button
        self.buttons["earth"] = self.earth_button
        self.buttons["stone"] = self.stone_button
        self.buttons["water"] = self.water_button
        self.buttons["eraser"] = self.eraser_button
    
    def event(self, x=0, y=0, event=None):
        if event in self.keys.keys():
            index = self.keys[event] - 1
            
            for button in self.buttons.values():
                button.press = False
            
            button = list(self.buttons.values())[index]
            button.press = True
            self.current_block = button.block
        
        else:
            for button in self.buttons.values():
                button.press = False
                if button.rect.collidepoint(x, y):
                    self.current_block = button.block
    
    def draw(self):
        # Background:
        self.screen.fill(self.bg_color)
        # Border:
        pygame.draw.lines(
            self.screen,
            self.bg_color,
            False,
            ((0, 0),
            (self.width, 0),
            (self.width, self.height),
            (0, self.height),
            (0, 0)),
            self.border_width
        )
        # Buttons:
        for button in self.buttons.values():
            if button.block == self.current_block:
                button.press = True
            button.draw(self.screen)
    
    def make_columns(self):
        self.cols_number = 5
        self.cols_width = round((self.width - self.border_width) / self.cols_number)
        self.cols = []
        for col in range(self.cols_number):
            self.cols.append(round(col * self.cols_width + self.border_width / 2))


class Button:
    def __init__(self, block, color, on_press_color, x, y, width, height):
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.block = block
        self.color = color
        self.press = False
        self.on_press_color = on_press_color
    
    def draw(self, screen):
        if self.press:
            color = self.on_press_color
        else:
            color = self.color
        pygame.draw.rect(screen, color, self.rect)
