import random
import json
import os

from pico2d import *
import game_framework
import game_world
import title_state
import server

from Mario import Character
from Mario import PIXEL_PER_METER
import enemy_object
import item_object
import map_object


name = "MainState"

Gravity = 9.8 * PIXEL_PER_METER
gAccel = 0



def Crash_Check(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def enter():
    server.mario = Character()
    server.map = map_object.Map_BackGround()
    server.enemys.append(enemy_object.Gomba())
    server.enemys.append(enemy_object.Turtle())
    server.items.append(item_object.Item_Mushroom())
    server.itemBox = item_object.Item_Box()
    game_world.add_object(server.map, 0)
    game_world.add_object(server.itemBox, 1)
    game_world.add_objects(server.items, 2)
    game_world.add_objects(server.enemys, 3)
    game_world.add_object(server.mario, 4)


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
                # game_framework.quit()
                game_framework.change_state(title_state)
        else:
            server.mario.handle_event(event)


def update():
    global gAccel
    for game_object in game_world.all_objects():
        game_object.update()
    # fill here
    # mario.y -= gAccel * game_framework.frame_time
    # if gAccel < 18:
    #     gAccel += Gravity * game_framework.frame_time
    if Crash_Check(server.mario, server.map):
        server.mario.y = 29 + server.mario.size_y // 2
        gAccel = 0
    for enemy in server.enemys:
        if Crash_Check(enemy, server.map):
            enemy.y = 30 + enemy.size_y // 2
        if Crash_Check(enemy, server.itemBox):
            enemy.Right = not enemy.Right
            enemy.update()
    for item in server.items:
        if Crash_Check(item, server.map):
            item.y = 30 + item.size_y // 2


    # delay(0.1)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    a = 800 / server.tileSize
    b = 600 / server.tileSize
    for i in range(int(a)):
        for j in range(int(b)):
            draw_rectangle(0+i*server.tileSize,0+j*server.tileSize,(1+i)*server.tileSize,(1+j)*server.tileSize)
    update_canvas()






