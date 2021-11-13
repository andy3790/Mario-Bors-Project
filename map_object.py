from pico2d import *

# Game object class here
class Item_Box:
    def __init__(self):
        self.image = load_image('image/qblock_strips.png')
        self.framex = 0
        self.framey = 8
        self.x = 400
        self.y = 80
    def update(self):
        self.framex += 1
        if self.framex > 6:
            self.framex = 0
            self.framey -= 1
        if self.framey == 6:
            self.framey = 8

    def Draw(self):
            self.image.clip_draw(self.framex * 24, self.framey * 24, 24, 24, self.x , self.y,30,30)