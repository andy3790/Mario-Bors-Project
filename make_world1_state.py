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

MapSize_Width = 100
MapSize_Height = 12

def enter():
    server.MIN_CAMERA_POS = 0
    server.MAX_CAMERA_POS = (MapSize_Width - 16) * server.tileSize
    server.cameraPos = 0

    for i in range(MapSize_Height):
        for j in range(MapSize_Width):
            server.TileMap[j][i] = 0
    game_world.clear()
    server.mario = Mario.Character()
    server.map = map_object.Map_BackGround()
    server.enemys.append(enemy_object.Gomba())
    server.enemys.append(enemy_object.Turtle())
    server.items.append(item_object.Item_Mushroom())
    server.itemBox = item_object.Item_Box(4, 3)
    server.TileMap[4][3] = server.itemBox
    server.blocks.append(item_object.Crash_Block(8, 3))
    server.TileMap[8][3] = server.blocks[-1]
    for i in range(20):
        server.mapObjects.append(map_object.MapObjects(3 - (i % 4),5,i,0))
        server.TileMap[i][0] = server.mapObjects[-1]
    server.mapObjects.append(map_object.MapObjects(0, 5, 6, 4))
    server.TileMap[6][4] = server.mapObjects[-1]
    game_world.add_objects(server.mapObjects, 1)
    game_world.add_object(server.map, 0)
    game_world.add_object(server.itemBox, 2)
    game_world.add_objects(server.blocks, 2)
    game_world.add_objects(server.items, 3)
    game_world.add_objects(server.enemys, 4)
    game_world.add_object(server.mario, 5)

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