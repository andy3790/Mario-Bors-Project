from pico2d import *

# Game object class here
class Character:
    def __init__(self):
        self.image = load_image('mario.png')
        self.framex = 0
        self.framey = 8
        self.Right = False
        self.Jump = False
        self.jumphight = 0
        self.x = 400
        self.y = 20
        self.speed = 0
        self.counter = 0
    def update(self):
        self.y -= 5
        if self.y < 20:
            self.y = 20
        if self.counter > 1:
            self.framex = (self.framex + 1) % 6
            self.counter = 0
        self.counter += 1
        if self.framey == 8:
            self.framex = 0
        if self.Jump and self.jumphight < 30:
            self.y += 10
            self.jumphight += 5
            if self.jumphight >= 30:
                self.Jump = False
                self.jumphight = 0
        pass
    def move(self, right):
        self.Right = right
        if self.Right:
            self.x += 5
        else:
            self.x -= 5

    def Draw(self):
        if self.Right:
            self.image.clip_composite_draw(130 - (19 * self.framex), (24 * self.framey) - 1, 20, 23,0,'h', self.x, self.y, 40, 46)
        else:
            self.image.clip_draw(130 - (19 * self.framex),(24 * self.framey) - 1,20,23,self.x,self.y, 40, 46)
        pass