import random
import json
import os

from pico2d import *
import game_framework
import game_world

from Mario import Character
from Mario import PIXEL_PER_METER
import enemy_object
import item_object
import map_object


name = "MainState"

Gravity = 9.8 * PIXEL_PER_METER
gAccel = 0

mario = None
enemys = []
items = []
gomba = None
turtle = None
map = None
itemBox = None


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
    global enemys
    global items
    global map
    global itemBox
    mario = Character()
    map = map_object.Map_BackGround()
    enemys.append(enemy_object.Gomba())
    enemys.append(enemy_object.Turtle())
    items.append(item_object.Item_Mushroom())
    itemBox = item_object.Item_Box()
    game_world.add_object(map, 0)
    game_world.add_object(itemBox, 1)
    game_world.add_objects(items, 2)
    game_world.add_objects(enemys, 3)
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
    global gAccel
    for game_object in game_world.all_objects():
        game_object.update()
    # fill here
    # mario.y -= gAccel * game_framework.frame_time
    # if gAccel < 18:
    #     gAccel += Gravity * game_framework.frame_time
    if Crash_Check(mario, map):
        mario.y = 29 + mario.size_y // 2
        gAccel = 0
    for enemy in enemys:
        if Crash_Check(enemy, map):
            enemy.y = 30 + enemy.size_y // 2
        if Crash_Check(enemy, itemBox):
            enemy.Right = not enemy.Right
            enemy.update()
    for item in items:
        if Crash_Check(item, map):
            item.y = 30 + item.size_y // 2


    # delay(0.1)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






