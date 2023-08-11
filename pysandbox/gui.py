import pygame
from pygame.locals import *
from pysandbox.blocks import *


class Widget:
    def __init__(self, root, x, y, size_hint_x, size_hint_y, bg_color):
        self.root = root
        self.width = root.width * size_hint_x
        self.height = root.height * size_hint_y
        self.screen = root.screen.subsurface(x, y, self.width, self.height)
        self.bg_color = bg_color


class BlocksBar(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.border_width = round(self.height * 0.15)
        self.current_block = Sand
        self.make_columns()
        self.build()
    
    def build(self):
        self.sand_button = BlockButton(
            block=Sand,
            x=self.cols[0],
            y=round(self.border_width / 2),
            width=self.cols_width,
            height=self.height - self.border_width,
            color=SAND_COLOR,
            on_press_color=SAND_COLOR_DARK
        )
        self.earth_button = BlockButton(
            block=Earth,
            x=self.cols[1],
            y=round(self.border_width / 2),
            width=self.cols_width,
            height=self.height - self.border_width,
            color=EARTH_COLOR,
            on_press_color=EARTH_COLOR_DARK
        )
        self.stone_button = BlockButton(
            block=Stone,
            x=self.cols[2],
            y=round(self.border_width / 2),
            width=self.cols_width,
            height=self.height - self.border_width,
            color=STONE_COLOR,
            on_press_color=STONE_COLOR_DARK
        )
        self.water_button = BlockButton(
            block=Water,
            x=self.cols[3],
            y=round(self.border_width / 2),
            width=self.cols_width,
            height=self.height - self.border_width,
            color=WATER_COLOR,
            on_press_color=WATER_COLOR_DARK
        )
        self.eraser_button = BlockButton(
            block=Eraser,
            x=self.cols[4],
            y=round(self.border_width / 2),
            width=self.cols_width,
            height=self.height - self.border_width,
            color=WHITE,
            on_press_color=GRAY
        )
        self.keys = {
            K_1: "sand", K_2: "earth",
            K_3: "stone", K_4: "water",
            K_5: "eraser"
        }
        self.buttons = {}
        self.buttons["sand"] = self.sand_button
        self.buttons["earth"] = self.earth_button
        self.buttons["stone"] = self.stone_button
        self.buttons["water"] = self.water_button
        self.buttons["eraser"] = self.eraser_button
    
    def change_block(self, x=0, y=0, event=None):
        if event in self.keys.keys():
            for button in self.buttons.values():
                button.press = False
            button = self.buttons[self.keys[event]]
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
            surface=self.screen,
            color=self.bg_color,
            closed=False,
            points=(
                (0, 0),
                (self.width, 0),
                (self.width, self.height),
                (0, self.height),
                (0, 0)),
            width=self.border_width
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
    def __init__(self, x, y, width, height, color, on_press_color):
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.color = color
        self.on_press_color = on_press_color
        self.press = False
    
    def draw(self, screen):
        color = self.on_press_color if self.press else self.color
        pygame.draw.rect(screen, color, self.rect)


class BlockButton(Button):
    def __init__(self, block, **kwargs):
        super().__init__(**kwargs)
        self.block = block
