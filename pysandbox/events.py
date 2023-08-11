import pygame
from pygame.locals import *
from pysandbox.utils import config


MOUSE_PRESSED = pygame.event.Event(USEREVENT + 1)
CONSTANT_EVENTS = pygame.event.Event(USEREVENT + 2)
RECURRING_EVENTS = pygame.event.Event(USEREVENT + 3)


def exit_game(**kwargs):
    pygame.quit()
    exit()


def constant_events(**kwargs):
    game = kwargs.get("game")
    game.sandbox.gravity()


def recurring_events(**kwargs):
    game = kwargs.get("game")
    game.sandbox.fill()
    game.sandbox.slide()


def change_block_by_key(**kwargs):
    game = kwargs.get("game")
    event_key = kwargs.get("event").key
    game.blocks_bar.change_block(event=event_key)


def change_block_by_mouse(x, y, **kwargs):
    game = kwargs.get("game")
    game.blocks_bar.change_block(x, y)


def change_mouse_state_to_true(**kwargs):
    game = kwargs.get("game")
    game.mouse_pressed = True


def change_mouse_state_to_false(**kwargs):
    game = kwargs.get("game")
    game.mouse_pressed = False


def place_block(x, y, **kwargs):
    game = kwargs.get("game")
    if  game.current_time - game.sandbox_press_time >= config.get("place-block-cooldown"):
        game.sandbox.place_block(game.blocks_bar.current_block, x, y)
        game.sandbox_press_time = pygame.time.get_ticks()


def keyboard_action(**kwargs):
    game = kwargs.get("game")
    event_key = kwargs.get("event").key
    if event_key == K_ESCAPE:
        exit_game()
    if event_key in game.blocks_bar.keys:
        change_block_by_key(**kwargs)


def mouse_action(**kwargs):
    game = kwargs.get("game")
    x, y = pygame.mouse.get_pos()
    if y < game.sandbox.height:
        place_block(x, y, **kwargs)
    if y > game.sandbox.height:
        y -= game.sandbox.height
        change_block_by_mouse(x, y, **kwargs)


def touch_action(**kwargs):
    game = kwargs.get("game")
    event = kwargs.get("event")
    x = round(event.x * game.width)
    y = round(event.y * game.height)
    if y < game.sandbox.height:
        place_block(x, y, **kwargs)
    if y > game.sandbox.height:
        y -= game.sandbox.height
        change_block_by_mouse(x, y, **kwargs)


events = (
    QUIT, exit_game,
    K_ESCAPE, exit_game,
    CONSTANT_EVENTS.type, constant_events,
    RECURRING_EVENTS.type, recurring_events,
    KEYDOWN, keyboard_action,
    MOUSEBUTTONDOWN, change_mouse_state_to_true,
    MOUSEBUTTONUP, change_mouse_state_to_false,
    MOUSE_PRESSED.type, mouse_action,
    FINGERDOWN, touch_action,
    FINGERMOTION, touch_action,
)
