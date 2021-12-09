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

MapSize_Width = 210
MapSize_Height = 20

def enter():
    server.MIN_CAMERA_POS = 0
    server.MAX_CAMERA_POS = (MapSize_Width - 16) * server.tileSize
    server.cameraPos = 0

    for i in range(MapSize_Height):
        for j in range(MapSize_Width):
            server.TileMap[j][i] = 0
    game_world.clear()
    del server.mario
    del server.map
    server.enemys.clear()
    server.blocks.clear()
    server.items.clear()
    server.mapObjects.clear()

    server.mario = Mario.Character(0, 2)
    server.map = map_object.Map_BackGround()

    for i in range(53):
        for j in range(2):
            server.mapObjects.append(map_object.MapObjects(3 - (i % 4),6 - j,i,j))

    server.blocks.append(item_object.Item_Box(17, 4))
    server.blocks[-1].putin_item(item_object.Coin())

    server.blocks.append(item_object.Crash_Block(21, 4))
    server.blocks.append(item_object.Item_Box(22, 4))
    server.blocks[-1].putin_item(item_object.Item_Mushroom())
    server.blocks.append(item_object.Crash_Block(23, 4))
    server.blocks.append(item_object.Item_Box(23, 7))
    server.blocks[-1].putin_item(item_object.Coin())
    server.blocks.append(item_object.Item_Box(24, 4))
    server.blocks[-1].putin_item(item_object.Coin())
    server.blocks.append(item_object.Crash_Block(25, 4))

    server.enemys.append(enemy_object.Gomba(25, 2))

    append_pipe(30,2,2)
    append_pipe(37,2,3)
    append_pipe(44,2,4)

    server.enemys.append(enemy_object.Gomba(43, 2))
    server.enemys.append(enemy_object.Gomba(42, 2))

    server.blocks.append(item_object.Item_Box(50, 4))
    server.blocks[-1].putin_item(item_object.Item_Mushroom())

    for i in range(56,67+1):
        for j in range(2):
            server.mapObjects.append(map_object.MapObjects(3 - (i % 4),6 - j,i,j))

    server.blocks.append(item_object.Crash_Block(60, 4))
    server.blocks.append(item_object.Item_Box(61, 4))
    server.blocks[-1].putin_item(item_object.Item_Mushroom())
    server.blocks.append(item_object.Crash_Block(62, 4))

    server.blocks.append(item_object.Crash_Block(63, 7))
    server.blocks.append(item_object.Crash_Block(64, 7))
    server.blocks.append(item_object.Crash_Block(65, 7))
    server.blocks.append(item_object.Crash_Block(66, 7))
    server.blocks.append(item_object.Crash_Block(67, 7))
    server.blocks.append(item_object.Crash_Block(68, 7))
    server.blocks.append(item_object.Crash_Block(69, 7))

    server.enemys.append(enemy_object.Gomba(64, 8))
    server.enemys.append(enemy_object.Gomba(68, 8))

    for i in range(71,138+1):
        for j in range(2):
            server.mapObjects.append(map_object.MapObjects(3 - (i % 4),6 - j,i,j))

    server.blocks.append(item_object.Crash_Block(72, 7))
    server.blocks.append(item_object.Crash_Block(73, 7))
    server.blocks.append(item_object.Crash_Block(74, 7))
    server.blocks.append(item_object.Item_Box(75, 4))
    server.blocks[-1].putin_item(item_object.Item_Mushroom())
    server.blocks.append(item_object.Crash_Block(75, 4))

    server.enemys.append(enemy_object.Gomba(80, 2))
    server.enemys.append(enemy_object.Gomba(78, 2))

    server.blocks.append(item_object.Crash_Block(79, 4))
    server.blocks.append(item_object.Item_Box(80, 4))
    server.blocks[-1].putin_item(item_object.Coin())

    server.blocks.append(item_object.Item_Box(84, 4))
    server.blocks[-1].putin_item(item_object.Coin())

    server.enemys.append(enemy_object.Turtle(86, 2))

    server.blocks.append(item_object.Item_Box(90, 4))
    server.blocks[-1].putin_item(item_object.Coin())
    server.blocks.append(item_object.Item_Box(93, 4))
    server.blocks[-1].putin_item(item_object.Coin())
    server.blocks.append(item_object.Item_Box(93, 7))
    server.blocks[-1].putin_item(item_object.Item_Mushroom())
    server.blocks.append(item_object.Item_Box(96, 4))
    server.blocks[-1].putin_item(item_object.Coin())

    server.blocks.append(item_object.Crash_Block(100, 4))

    server.blocks.append(item_object.Crash_Block(102, 7))
    server.blocks.append(item_object.Crash_Block(103, 7))
    server.blocks.append(item_object.Crash_Block(104, 7))
    server.blocks.append(item_object.Crash_Block(105, 7))

    server.blocks.append(item_object.Crash_Block(110, 7))
    server.blocks.append(item_object.Crash_Block(111, 4))
    server.blocks.append(item_object.Crash_Block(112, 4))
    server.blocks.append(item_object.Crash_Block(113, 7))
    server.blocks.append(item_object.Item_Box(111, 7))
    server.blocks[-1].putin_item(item_object.Coin())
    server.blocks.append(item_object.Item_Box(112, 7))
    server.blocks[-1].putin_item(item_object.Coin())

    for i in range(4+1):
        for j in range(i):
            server.blocks.append(item_object.Crash_Block(119-j, 6-i))
    for i in range(4+1):
        for j in range(i):
            server.blocks.append(item_object.Crash_Block(122+j, 6-i))

    for i in range(4+1):
        for j in range(i):
            server.blocks.append(item_object.Crash_Block(137-j, 6-i))
    server.blocks.append(item_object.Crash_Block(138, 5))
    server.blocks.append(item_object.Crash_Block(138, 4))
    server.blocks.append(item_object.Crash_Block(138, 3))
    server.blocks.append(item_object.Crash_Block(138, 2))

    for i in range(142,200):
        for j in range(2):
            server.mapObjects.append(map_object.MapObjects(3 - (i % 4),6 - j,i,j))

    for i in range(4+1):
        for j in range(i):
            server.blocks.append(item_object.Crash_Block(142+j, 6-i))

    append_pipe(152,2,2)

    server.blocks.append(item_object.Crash_Block(156, 4))
    server.blocks.append(item_object.Crash_Block(157, 4))
    server.blocks.append(item_object.Crash_Block(159, 4))
    server.blocks.append(item_object.Item_Box(158, 4))
    server.blocks[-1].putin_item(item_object.Coin())

    append_pipe(164,2,2)

    for i in range(8+1):
        for j in range(i):
            server.blocks.append(item_object.Crash_Block(173-j, 10-i))
    server.blocks.append(item_object.Crash_Block(174, 2))
    server.blocks.append(item_object.Crash_Block(174, 3))
    server.blocks.append(item_object.Crash_Block(174, 4))
    server.blocks.append(item_object.Crash_Block(174, 5))
    server.blocks.append(item_object.Crash_Block(174, 6))
    server.blocks.append(item_object.Crash_Block(174, 7))
    server.blocks.append(item_object.Crash_Block(174, 8))
    server.blocks.append(item_object.Crash_Block(174, 9))

    server.blocks.append(map_object.End_castle_flag(0,0,180  ,2))
    server.blocks.append(map_object.End_castle_flag(1,0,181,2))
    server.blocks.append(map_object.End_castle_flag(1,1,181,3))
    server.blocks.append(map_object.End_castle_flag(1,1,181,4))
    server.blocks.append(map_object.End_castle_flag(1,1,181,5))
    server.blocks.append(map_object.End_castle_flag(1,1,181,6))
    server.blocks.append(map_object.End_castle_flag(1,1,181,7))
    server.blocks.append(map_object.End_castle_flag(1,1,181,8))
    server.blocks.append(map_object.End_castle_flag(1,1,181,9))
    server.blocks.append(map_object.End_castle_flag(1,2,181,10))
    server.blocks.append(map_object.End_castle_flag(2,0,182,2))

    game_world.add_object(server.map, 0)
    game_world.add_objects(server.mapObjects, 1)
    game_world.add_objects(server.blocks, 2)
    game_world.add_objects(server.items, 3)
    game_world.add_objects(server.enemys, 4)
    game_world.add_object(server.mario, 5)

    game_framework.change_state(main_state)

def append_pipe(x, y, height):
    server.blocks.append(map_object.Pipe(0,4,x,y+height-1))
    server.blocks.append(map_object.Pipe(1,4,x+1,y+height-1))

    for i in range(height-1):
        server.blocks.append(map_object.Pipe(0,3,x,y+i))
        server.blocks.append(map_object.Pipe(1,3,x+1,y+i))

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