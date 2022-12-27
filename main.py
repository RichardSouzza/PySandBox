import pygame
from pygame.locals import *
from assets.colors import colors
from gui import BlocksBar
from sandbox import SandBox
from kivy.utils import platform


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.bg_color = colors["bg_color"]
        self.screen.fill(self.bg_color)
        
        self.clock = pygame.time.Clock()
        self.current_time = 0
        self.button_press_time = 0
        self.sandbox_press_time = 0
        self.blocks_event_time = 0
        
        self.build()
    
    def build(self):
        if platform in ("linux", "macosx", "win"):
            self.events = self.desktop_events
        
        elif platform in ("android", "ios"):
            self.events = self.mobile_events
        
        self.sandbox = SandBox(
            self,
            0, 0,
            1, 0.85
        )
        self.blocks_bar = BlocksBar(
            self,
            0, self.height * 0.85,
            1, 0.15
        )
    
    def desktop_events(self):
        self.sandbox.gravity()
        
        if self.current_time - self.blocks_event_time > 200:
            self.sandbox.slide()
            self.sandbox.fill()
            self.blocks_event_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type in (KEYDOWN, KEYUP):
                # Event on the blocks bar.
                if  self.current_time - self.button_press_time >= 100:
                    self.blocks_bar.event(event=event.key)
                    self.button_press_time = pygame.time.get_ticks()
            
            if event.type in (MOUSEBUTTONDOWN, MOUSEMOTION):
                x = event.pos[0]
                y = event.pos[1]
                
                if y < self.sandbox.height:
                    # Event in the sandbox.
                    if  self.current_time - self.sandbox_press_time >= 100:
                        self.sandbox.make_block(self.blocks_bar.current_block, x, y)
                        self.sandbox_press_time = pygame.time.get_ticks()
            
            if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION):
                x = event.pos[0]
                y = round((event.pos[1] - self.height) * -1)
                
                if y * self.height > self.sandbox.height:
                    # Event on the blocks bar.
                    if  self.current_time - self.button_press_time >= 100:
                        self.blocks_bar.event(x, y)
                        self.button_press_time = pygame.time.get_ticks()
    
    def draw(self):
        self.sandbox.draw()
        self.blocks_bar.draw()
    
    def mobile_events(self):
        self.sandbox.gravity()
        
        if self.current_time - self.blocks_event_time > 200:
            self.sandbox.slide()
            self.sandbox.fill()
            self.blocks_event_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type in (FINGERDOWN, FINGERMOTION):
                x = round(event.x * self.width)
                y = round(event.y * self.height)
                
                if y < self.sandbox.height:
                    # Event in the sandbox.
                    if  self.current_time - self.sandbox_press_time >= 100:
                        self.sandbox.make_block(self.blocks_bar.current_block, x, y)
                        self.sandbox_press_time = pygame.time.get_ticks()
            
            if event.type in (FINGERDOWN, FINGERMOTION, FINGERUP):
                x = round(event.x * self.width)
                y = event.y
                
                if y * self.height > self.sandbox.height:
                    # Event on the blocks bar.
                    if  self.current_time - self.button_press_time >= 100:
                        y = round(event.y * (self.blocks_bar.height - self.blocks_bar.border_width))
                        self.blocks_bar.event(x, y)
                        self.button_press_time = pygame.time.get_ticks()
    
    def run(self):
        while True:
            self.current_time = pygame.time.get_ticks()
            self.events()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode()
    pygame.display.set_caption("PySandBox")
    
    game = Game(screen)
    game.run()