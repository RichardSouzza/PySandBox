import pygame
from pygame.locals import *
from pysandbox.colors import *
from pysandbox.events import *
from pysandbox.gui import BlocksBar
from pysandbox.sandbox import SandBox
from pysandbox.utils import config, get_platform


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PySandBox")
        self.screen = pygame.display.set_mode()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.bg_color = BACKGROUND_COLOR
        self.screen.fill(self.bg_color)
        
        self.clock = pygame.time.Clock()
        self.current_time = 0
        self.sandbox_press_time = 0
        self.mouse_pressed = False
        
        self.build()
    
    def build(self):
        platform = get_platform()
        if platform == "desktop":
            self.event_handler = self.desktop_events
        elif platform == "mobile":
            self.event_handler = self.mobile_events
        
        self.sandbox = SandBox(
            root=self,
            x=0,
            y=0,
            size_hint_x=1,
            size_hint_y=0.85,
            bg_color=BLACK
        )
        self.blocks_bar = BlocksBar(
            root=self,
            x=0,
            y=self.height * 0.85,
            size_hint_x=1,
            size_hint_y=0.15,
            bg_color=BACKGROUND_COLOR
        )
    
    def desktop_events(self):
        if self.mouse_pressed:
            pygame.event.post(MOUSE_PRESSED)
        for event in pygame.event.get():
            if event.type in events:
                self.run_event(event)
    
    def mobile_events(self):
        for event in pygame.event.get():
            if event.type in events:
                self.run_event(event)
    
    def run_event(self, event):
        event_type = event.type
        index = events.index(event_type)
        event_action = events[index+1]
        event_action(game=self, event=event)
    
    def draw(self):
        self.sandbox.draw()
        self.blocks_bar.draw()
    
    def run(self):
        pygame.time.set_timer(CONSTANT_EVENTS, config.get("constant-events-interval"))
        pygame.time.set_timer(RECURRING_EVENTS, config.get("recurring-events-interval"))
        while True:
            self.current_time = pygame.time.get_ticks()
            self.event_handler()
            self.draw()
            pygame.display.update()
            self.clock.tick(config.get("fps"))
