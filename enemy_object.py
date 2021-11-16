from pico2d import *
from Mario import PIXEL_PER_METER

import game_framework

# Game object class here
MOVE_SPEED = 1 * PIXEL_PER_METER

class Gomba:
    image = None
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME
    def __init__(self):
        if Gomba.image == None:
            Gomba.image = load_image('image/gomba.png')
        self.frame = 0
        self.Right = False
        self.x = 400
        self.y = 20

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
            self.image.clip_composite_draw(5, 32 * (27 - int(self.frame)) + 7, 19, 20, 0, 'h', self.x, self.y, 38, 44)
        else:
            self.image.clip_draw(5, 32 * (27 - int(self.frame)) + 7, 19, 20, self.x, self.y, 38, 44)

        draw_rectangle(*self.get_bb())


class Turtle:
    image = None
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 16
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME
    def __init__(self):
        if Turtle.image == None:
            Turtle.image = load_image('image/turtle.png')
        self.frame = 0
        self.Right = False
        self.x = 500
        self.y = 25

    def get_bb(self):
        return self.x - 13, self.y - 20, self.x + 13, self.y + 20

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
            self.image.clip_composite_draw(0,  32 * (41 - int(self.frame)) + 12, 20, 35, 0, 'h', self.x, self.y, 40, 70)
        else:
            self.image.clip_draw(0, 32 * (41 - int(self.frame)) + 12, 20, 35, self.x, self.y, 40, 70)

        draw_rectangle(*self.get_bb())