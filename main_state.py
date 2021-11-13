import random
import json
import os

from pico2d import *
import game_framework
import game_world

from Mario import Character
from enemy_object import Gomba
from enemy_object import Turtle


name = "MainState"

mario = None
gomba = None
turtle = None

def enter():
    global mario
    global gomba
    global turtle
    mario = Character()
    gomba = Gomba()
    turtle = Turtle()
    # game_world.add_object(turtle, 0)
    # game_world.add_object(gomba, 0)
    game_world.add_object(mario, 1)


def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            mario.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    # fill here
    # delay(0.1)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






