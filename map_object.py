from pico2d import *

# Game object class here
class Map_BackGround:
    def __init__(self):
        self.image = load_image('image/1-1_background.png')
        self.x = 400
        self.y = 300

    def get_bb(self):
        return 0, 0, 800, 35

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 792, 792, self.x , self.y,800,600)
        draw_rectangle(*self.get_bb())


class Item_Box:
    def __init__(self, sx = 400, sy = 400):
        self.image = load_image('image/qblock_strips.png')
        self.framex = 0
        self.framey = 8
        self.x = sx
        self.y = sy
    def update(self):
        self.framex += 1
        if self.framex > 6:
            self.framex = 0
            self.framey -= 1
        if self.framey == 6:
            self.framey = 8

    def draw(self):
        self.image.clip_draw(self.framex * 24, self.framey * 24, 24, 24, self.x , self.y,30,30)