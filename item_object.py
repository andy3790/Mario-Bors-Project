from pico2d import *

import server
import game_framework

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

    def get_bb(self):
        return self.x - self.size_x / 2, self.y - self.size_y / 2, self.x + self.size_x / 2, self.y + self.size_y / 2

    def update(self):
        if self.Right:
            self.x += MOVE_SPEED * game_framework.frame_time
            if self.x > 800:
                self.Right = False
        else:
            self.x -= MOVE_SPEED * game_framework.frame_time
            if self.x < 0:
                self.Right = True

    def draw(self):
        self.image.draw(self.x,self.y, self.size_x, self.size_y)

        draw_rectangle(*self.get_bb())


class Item_Box:
    image = None
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 16
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME
    def __init__(self, sx = 4, sy = 1):
        if Item_Box.image == None:
            Item_Box.image = load_image('image/qblock_strips.png')
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

    def draw(self):
            self.image.clip_draw(int(self.framex) * 24, int(self.framey) * 24, 24, 24, self.x , self.y,self.size_x, self.size_y)
            draw_rectangle(*self.get_bb())