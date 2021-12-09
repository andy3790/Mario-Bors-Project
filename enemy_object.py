from pico2d import *
import server

import game_framework
import game_world
from collision import Crash_Check

# Game object class here
MOVE_SPEED = 1 * server.PIXEL_PER_METER

class Gomba:
    image = None
    damage_sound = None
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME

    def __init__(self, sx = 5, sy = 1):
        if Gomba.image == None:
            Gomba.image = load_image('image/gomba.png')
        if Gomba.damage_sound == None:
            Gomba.damage_sound = load_wav('sound/stomp.wav')
            Gomba.damage_sound.set_volume(server.effect_sound_volume)
        self.frame = 0
        self.Right = False
        self.x = sx * server.tileSize + server.tileSize / 2
        self.y = sy * server.tileSize + server.tileSize / 2.3
        self.size_x = server.tileSize
        self.size_y = server.tileSize
        self.dmg = False
        self.gaccel = 0

    def get_bb(self):
        if self.dmg:
            return 0, 0, 0, 0
        else:
            return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def update(self):
        if self.dmg:
            self.frame += (Gomba.ONE_ACTION / 4 * game_framework.frame_time)
            if self.frame > 9:
                game_world.remove_object(self)
                for e in server.enemys:
                    if e == self:
                        server.enemys.remove(e)
            pass
        else:
            self.frame = (self.frame + Gomba.ONE_ACTION * game_framework.frame_time) % 8
            if self.Right:
                self.x += MOVE_SPEED * game_framework.frame_time
            else:
                self.x -= MOVE_SPEED * game_framework.frame_time

            for o in game_world.all_layer_objects(1):
                if Crash_Check(self, o):
                    self.Right = not self.Right
            for o in game_world.all_layer_objects(2):
                if Crash_Check(self, o):
                    self.Right = not self.Right
            self.gravity()
            if server.TileMap[int(self.x / server.tileSize)][int(self.y / server.tileSize - 1)] != 0:
                self.gaccel = 0
                self.y = server.TileMap[int(self.x / server.tileSize)][int(self.y / server.tileSize - 1)].y + (server.tileSize)
            else:
                self.Right = not self.Right

    def damaged(self):
        self.dmg = True
        self.frame = 8
        self.damage_sound.play(1)

    def gravity(self):
        self.gaccel += server.Gravity * 1.5 * game_framework.frame_time
        self.y -= self.gaccel * game_framework.frame_time

    def draw(self):
        if self.Right:
            self.image.clip_composite_draw(5, 32 * (27 - int(self.frame)) + 7, 19, 20, 0, 'h', self.x - server.cameraPos, self.y, self.size_x, self.size_y)
        else:
            self.image.clip_draw(5, 32 * (27 - int(self.frame)) + 7, 19, 20, self.x - server.cameraPos, self.y, self.size_x, self.size_y)

        if server.debugMod:
            a1, a2, a3, a4 = self.get_bb()
            draw_rectangle(a1 - server.cameraPos, a2, a3 - server.cameraPos, a4)

    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'Right': self.Right, 'dmg': self.dmg}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)


class Turtle:
    image = None
    damage_sound = None
    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 16
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME

    def __init__(self, sx = 6, sy = 1):
        if Turtle.image == None:
            Turtle.image = load_image('image/turtle.png')
        if Turtle.damage_sound == None:
            Turtle.damage_sound = load_wav('sound/stomp.wav')
            Turtle.damage_sound.set_volume(server.effect_sound_volume)
        self.frame = 0
        self.Right = False
        self.x = sx * server.tileSize + server.tileSize / 2
        self.y = sy * server.tileSize + server.tileSize / 1.5
        self.size_x = server.tileSize
        self.size_y = server.tileSize / 5 * 7
        self.dmg = False
        self.gaccel = 0


    def get_bb(self):
        if self.dmg:
            return 0, 0, 0, 0
        else:
            return self.x - 13, self.y - 25, self.x + 13, self.y + 25

    def update(self):
        if self.dmg:
            self.frame = (self.frame + Turtle.ONE_ACTION / 16 * game_framework.frame_time) % 1 + 16
        else:
            self.frame = (self.frame + Turtle.ONE_ACTION * game_framework.frame_time) % 16
            if self.Right:
                self.x += MOVE_SPEED * game_framework.frame_time
            else:
                self.x -= MOVE_SPEED * game_framework.frame_time

            for o in game_world.all_layer_objects(1):
                if Crash_Check(self, o):
                    self.Right = not self.Right
            for o in game_world.all_layer_objects(2):
                if Crash_Check(self, o):
                    self.Right = not self.Right

            self.gravity()
            if server.TileMap[int(self.x / server.tileSize)][int(self.y / server.tileSize - 1)] != 0:
                self.gaccel = 0
                self.y = server.TileMap[int(self.x / server.tileSize)][int(self.y / server.tileSize - 1)].y + (server.tileSize)
            else:
                self.Right = not self.Right

    def damaged(self):
        self.dmg = True
        self.damage_sound.play(1)

    def gravity(self):
        self.gaccel += server.Gravity * 1.5 * game_framework.frame_time
        self.y -= self.gaccel * game_framework.frame_time

    def draw(self):
        if self.dmg:
            self.image.clip_draw(0, 32 * (41 - int(self.frame)) + 17, 20, 15, self.x - server.cameraPos, self.y - self.size_y / 5, self.size_x, self.size_y / 2)
        else:
            if self.Right:
                self.image.clip_composite_draw(0,  32 * (41 - int(self.frame)) + 17, 20, 30, 0, 'h', self.x - server.cameraPos, self.y, self.size_x, self.size_y)
            else:
                self.image.clip_draw(0, 32 * (41 - int(self.frame)) + 17, 20, 30, self.x - server.cameraPos, self.y, self.size_x, self.size_y)

        if server.debugMod:
            a1, a2, a3, a4 = self.get_bb()
            draw_rectangle(a1 - server.cameraPos, a2, a3 - server.cameraPos, a4)


    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'Right': self.Right, 'dmg': self.dmg}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)