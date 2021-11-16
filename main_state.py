import random
import json
import os

from pico2d import *
import game_framework
import game_world

from Mario import Character
from enemy_object import Gomba
from enemy_object import Turtle
from item_object import Item_Box
from item_object import Item_Mushroom


name = "MainState"

mario = None
gomba = None
turtle = None

def Crash_Check(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def enter():
    global mario
    global gomba
    global turtle
    mario = Character()
    gomba = Gomba()
    turtle = Turtle()
    itembox = Item_Box()
    itemmush = Item_Mushroom()
    game_world.add_object(itembox, 1)
    game_world.add_object(itemmush, 2)
    game_world.add_object(turtle, 3)
    game_world.add_object(gomba, 3)
    game_world.add_object(mario, 4)


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






