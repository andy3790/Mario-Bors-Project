import random
import json
import os

from pico2d import *
import game_framework
import game_world
import title_state
import server

from Mario import Character
from server import PIXEL_PER_METER
import enemy_object
import item_object
import map_object
from collision import Crash_Check


name = "MainState"


def enter():
    # server.mario = Character()
    # server.map = map_object.Map_BackGround()
    # server.enemys.append(enemy_object.Gomba())
    # server.enemys.append(enemy_object.Turtle())
    # server.items.append(item_object.Item_Mushroom())
    # server.mapObjects.append(map_object.MapObjects(0,5,2,3))
    # server.mapObjects.append(item_object.Item_Box())
    # server.TileMap[2][3] = server.mapObjects[0]
    # server.TileMap[4][1] = server.mapObjects[1]
    #
    # game_world.add_objects(server.mapObjects, 1)
    # game_world.add_object(server.map, 0)
    # game_world.add_objects(server.items, 2)
    # game_world.add_objects(server.enemys, 3)
    # game_world.add_object(server.mario, 4)
    pass


def exit():
    game_world.clear()
    server.mario = None
    server.map = None
    server.enemys.clear()
    server.items.clear()
    server.mapObjects.clear()

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
    for game_object in game_world.all_objects():
        game_object.update()
    # fill here
    if Crash_Check(server.mario, server.map):
        server.mario.y = 29 + server.mario.size_y // 2
    for enemy in server.enemys:
        if Crash_Check(enemy, server.map):
            enemy.y = 30 + enemy.size_y // 2
        for lo in game_world.all_layer_objects(1):
            if Crash_Check(enemy, lo):
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
    # for i in range(int(a)):
    #     for j in range(int(b)):
    #         draw_rectangle(0+i*server.tileSize,0+j*server.tileSize,(1+i)*server.tileSize,(1+j)*server.tileSize)
    update_canvas()






