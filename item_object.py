from pico2d import *

# Game object class here
class Item_Mushroom:
    image = None
    def __init__(self):
        if Item_Mushroom.image == None:
            Item_Mushroom.image = load_image('image/mushroom.png')
        self.Right = False
        self.x = 100
        self.y = 15
    def update(self):
        if self.Right:
            self.x += 5
            if self.x > 800:
                self.Right = False
        else:
            self.x -= 5
            if self.x < 0:
                self.Right = True

    def Draw(self):
            self.image.draw(self.x,self.y, 30, 30)


class Item_Box:
    image = None
    def __init__(self):
        if Item_Box.image == None:
            Item_Box.image = load_image('image/qblock_strips.png')
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