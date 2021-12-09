import random
import pickle

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

MapSize_Width = 100
MapSize_Height = 12

def enter():
    server.MIN_CAMERA_POS = 0
    server.MAX_CAMERA_POS = (MapSize_Width - 16) * server.tileSize
    server.cameraPos = 0

    game_world.clear()

    game_world.load()
    for o in game_world.all_objects():
        if isinstance(o, Mario.Character):
            server.mario = o
        elif isinstance(o, item_object.Item_Mushroom) or isinstance(o, item_object.Coin):
            server.items.append(o)
        elif isinstance(o, item_object.Item_Box) or isinstance(o, item_object.Crash_Block):
            server.blocks.append(o)
        elif isinstance(o, map_object.MapObjects):
            server.mapObjects.append(o)
        elif isinstance(o, enemy_object.Gomba) or isinstance(o, enemy_object.Turtle):
            server.enemys.append(o)

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