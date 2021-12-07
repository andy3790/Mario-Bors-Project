import random

from pico2d import *
import game_framework
import game_world
import server
import main_state

import Mario
from server import PIXEL_PER_METER
import enemy_object
import item_object
import map_object

def enter():
    game_world.clear()
    server.mario = Mario.Character()
    server.map = map_object.Map_BackGround()
    server.enemys.append(enemy_object.Gomba())
    server.enemys.append(enemy_object.Turtle())
    server.items.append(item_object.Item_Mushroom())
    server.itemBox = item_object.Item_Box()
    server.mapObjects.append(map_object.MapObjects(0,5,2,3))
    server.TileMap[2][3] = server.mapObjects[0]
    game_world.add_objects(server.mapObjects, 1)
    game_world.add_object(server.map, 0)
    game_world.add_object(server.itemBox, 1)
    game_world.add_objects(server.items, 2)
    game_world.add_objects(server.enemys, 3)
    game_world.add_object(server.mario, 4)
    server.TileMap[4][1] = server.itemBox

    game_framework.change_state(main_state)


def exit():
    pass

def pause():
    pass


def resume():
    pass


def handle_events():
    pass


def update():
    pass

def draw():
    pass