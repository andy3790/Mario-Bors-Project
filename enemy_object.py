from pico2d import *
import server

import game_framework

# Game object class here
MOVE_SPEED = 1 * server.PIXEL_PER_METER

class Gomba:
    image = None
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME
    def __init__(self, sx = 5, sy = 1):
        if Gomba.image == None:
            Gomba.image = load_image('image/gomba.png')
        self.frame = 0
        self.Right = False
        self.x = sx * server.tileSize + server.tileSize / 2
        self.y = sy * server.tileSize + server.tileSize / 2.3
        self.size_x = server.tileSize
        self.size_y = server.tileSize

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def update(self):
        self.frame = (self.frame + Gomba.ONE_ACTION * game_framework.frame_time) % 8
        if self.Right:
            self.x += MOVE_SPEED * game_framework.frame_time
            if self.x > 800:
                self.Right = False
        else:
            self.x -= MOVE_SPEED * game_framework.frame_time
            if self.x < 0:
                self.Right = True

    def draw(self):
        if self.Right:
            self.image.clip_composite_draw(5, 32 * (27 - int(self.frame)) + 7, 19, 20, 0, 'h', self.x - server.cameraPos, self.y, self.size_x, self.size_y)
        else:
            self.image.clip_draw(5, 32 * (27 - int(self.frame)) + 7, 19, 20, self.x - server.cameraPos, self.y, self.size_x, self.size_y)

        if server.debugMod:
            a1, a2, a3, a4 = self.get_bb()
            draw_rectangle(a1 - server.cameraPos, a2, a3 - server.cameraPos, a4)


class Turtle:
    image = None
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 16
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME
    def __init__(self, sx = 6, sy = 1):
        if Turtle.image == None:
            Turtle.image = load_image('image/turtle.png')
        self.frame = 0
        self.Right = False
        self.x = sx * server.tileSize + server.tileSize / 2
        self.y = sy * server.tileSize + server.tileSize / 1.5
        self.size_x = server.tileSize
        self.size_y = server.tileSize / 5 * 7

    def get_bb(self):
        return self.x - 13, self.y - 25, self.x + 13, self.y + 25

    def update(self):
        self.frame = (self.frame + Turtle.ONE_ACTION * game_framework.frame_time) % 16
        if self.Right:
            self.x += MOVE_SPEED * game_framework.frame_time
            if self.x > 800:
                self.Right = False
        else:
            self.x -= MOVE_SPEED * game_framework.frame_time
            if self.x < 0:
                self.Right = True

    def draw(self):
        if self.Right:
            self.image.clip_composite_draw(0,  32 * (41 - int(self.frame)) + 17, 20, 30, 0, 'h', self.x - server.cameraPos, self.y, self.size_x, self.size_y)
        else:
            self.image.clip_draw(0, 32 * (41 - int(self.frame)) + 17, 20, 30, self.x - server.cameraPos, self.y, self.size_x, self.size_y)

        if server.debugMod:
            a1, a2, a3, a4 = self.get_bb()
            draw_rectangle(a1 - server.cameraPos, a2, a3 - server.cameraPos, a4)