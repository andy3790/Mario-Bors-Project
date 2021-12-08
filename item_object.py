import random

from pico2d import *

import server
import game_framework
import game_world
from server import Gravity
from collision import Crash_Check

MOVE_SPEED = 2 * server.PIXEL_PER_METER
# Game object class here
class Item_Mushroom:
    image = None
    def __init__(self, sx = 4, sy = 1):
        if Item_Mushroom.image == None:
            Item_Mushroom.image = load_image('image/mushroom.png')
        self.Right = False
        self.x = sx * server.tileSize + server.tileSize / 2
        self.y = sy * server.tileSize + server.tileSize / 2.5
        self.size_x = server.tileSize / 5 * 4
        self.size_y = server.tileSize / 5 * 4
        self.gaccel = 0

    def get_bb(self):
        return self.x - self.size_x / 2, self.y - self.size_y / 2, self.x + self.size_x / 2, self.y + self.size_y / 2

    def update(self):
        if self.Right:
            self.x += MOVE_SPEED * game_framework.frame_time
            if self.x > 800:
                pass
                # self.Right = False
        else:
            self.x -= MOVE_SPEED * game_framework.frame_time
            if self.x < 0:
                self.Right = True

        self.gravity()
        if self.y <= 0:
            game_world.remove_object(self)
            for o in server.items:
                if o == self:
                    server.items.remove(o)
        # 하단 충돌체크
        elif Crash_Check(self, server.TileMap[int(self.x / server.tileSize)][int(self.y / server.tileSize - 1)]):
            self.gaccel = 0
            self.y = server.TileMap[int(self.x / server.tileSize)][int(self.y / server.tileSize - 1)].y + (server.tileSize / 5 * 4.5)

    def pop_out(self, x, y):
        self.x = x
        self.y = y + server.tileSize

    def gravity(self):
        self.gaccel += Gravity * 1.5 * game_framework.frame_time
        self.y -= self.gaccel * game_framework.frame_time

    def draw(self):
        self.image.draw(self.x - server.cameraPos,self.y, self.size_x, self.size_y)

        if server.debugMod:
            a1, a2, a3, a4 = self.get_bb()
            draw_rectangle(a1 - server.cameraPos, a2, a3 - server.cameraPos, a4)


class Item_Box:
    image = None
    image_popout = None
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 16
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME
    def __init__(self, sx = 4, sy = 1):
        if Item_Box.image == None:
            Item_Box.image = load_image('image/qblock_strips.png')
        if Item_Box.image_popout == None:
            Item_Box.image_popout = load_image('image/brown big block.png')
        self.framex = 0
        self.framey = 8
        self.x = sx * server.tileSize + server.tileSize / 2
        self.y = sy * server.tileSize + server.tileSize / 2
        self.size_x = server.tileSize
        self.size_y = server.tileSize
        self.initem = []
        self.putin_item(Item_Mushroom())

    def putin_item(self, item):
        self.initem.append(item)

    def get_bb(self):
        return self.x - self.size_x / 2, self.y - self.size_y / 2, self.x + self.size_x / 2, self.y + self.size_y / 2

    def update(self):
        if len(self.initem) > 0:
            self.framex += Item_Box.ONE_ACTION * game_framework.frame_time
            if self.framex > 6:
                self.framex = 0
                self.framey -= 1
            if self.framey == 6:
                self.framey = 8

    def hit(self):
        if len(self.initem) > 0:
            ob = self.initem.pop()
            ob.pop_out(self.x, self.y)
            server.items.append(ob)
            game_world.add_object(ob, 3)


    def draw(self):
        if len(self.initem) > 0:
            self.image.clip_draw(int(self.framex) * 24, int(self.framey) * 24, 24, 24, self.x - server.cameraPos , self.y,self.size_x, self.size_y)
        else:
            self.image_popout.clip_draw(0,0,64,64,self.x - server.cameraPos, self.y, self.size_x, self.size_y)

        if server.debugMod:
            a1, a2, a3, a4 = self.get_bb()
            draw_rectangle(a1 - server.cameraPos, a2, a3 - server.cameraPos, a4)

class Coin:
    image = None
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 16
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME
    def __init__(self, sx, sy):
        if Coin.image == None:
            Coin.image = load_image('image/qblock_strips.png')
        self.framex = 0
        self.framey = 8
        self.x = sx * server.tileSize + server.tileSize / 2
        self.y = sy * server.tileSize + server.tileSize / 2
        self.size_x = server.tileSize
        self.size_y = server.tileSize
    def get_bb(self):
        return self.x - self.size_x / 2, self.y - self.size_y / 2, self.x + self.size_x / 2, self.y + self.size_y / 2
    def update(self):
        self.framex += Item_Box.ONE_ACTION * game_framework.frame_time
        if self.framex > 6:
            self.framex = 0
            self.framey -= 1
        if self.framey == 6:
            self.framey = 8

    def hit(self):
        print("hitbox")

    def draw(self):
            self.image.clip_draw(int(self.framex) * 24, int(self.framey) * 24, 24, 24, self.x - server.cameraPos , self.y,self.size_x, self.size_y)

            if server.debugMod:
                a1, a2, a3, a4 = self.get_bb()
                draw_rectangle(a1 - server.cameraPos, a2, a3 - server.cameraPos, a4)


class Crash_Block:
    image = None
    TIME_PER_ACTION = 0.25
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME
    def __init__(self, sx = 4, sy = 1):
        if Crash_Block.image == None:
            Crash_Block.image = load_image('image/qblock_strips.png')
        self.framex = 0
        self.framey = 6
        self.frameTimer = 0
        self.x = sx * server.tileSize + server.tileSize / 2
        self.y = sy * server.tileSize + server.tileSize / 2
        self.size_x = server.tileSize
        self.size_y = server.tileSize
    def get_bb(self):
        return self.x - self.size_x / 2, self.y - self.size_y / 2, self.x + self.size_x / 2, self.y + self.size_y / 2

    def update(self):
        self.framex += Crash_Block.ONE_ACTION * game_framework.frame_time
        if self.framex >= 4:
            self.frameTimer += game_framework.frame_time
        if self.frameTimer > 0:
            self.frameTimer += game_framework.frame_time
            self.framex = 0
            if self.frameTimer > random.randint(3,10):
                self.frameTimer = 0


    def hit(self):
        game_world.remove_object(self)
        for o in server.blocks:
            if o == self:
                server.blocks.remove(o)
        server.TileMap[int(self.x / server.tileSize)][int(self.y / server.tileSize)] = 0



    def draw(self):
            self.image.clip_draw(int(self.framex) * 24, int(self.framey) * 24, 24, 24, self.x - server.cameraPos , self.y,self.size_x, self.size_y)

            if server.debugMod:
                a1, a2, a3, a4 = self.get_bb()
                draw_rectangle(a1 - server.cameraPos, a2, a3 - server.cameraPos, a4)