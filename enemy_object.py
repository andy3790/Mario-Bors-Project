from pico2d import *

# Game object class here

class Gomba:
    def __init__(self):
        self.image = load_image('gomba.png')
        self.frame = 0
        self.Right = False
        self.x = 400
        self.y = 20
    def update(self):
        self.frame = (self.frame + 1) % 8
        if self.Right:
            self.x += 5
            if self.x > 800:
                self.Right = False
        else:
            self.x -= 5
            if self.x < 0:
                self.Right = True

    def Draw(self):
        if self.Right:
            self.image.clip_composite_draw(5, 32 * (27 - self.frame) + 7, 19, 20, 0, 'h', self.x, self.y, 38, 44)
        else:
            self.image.clip_draw(5, 32 * (27 - self.frame) + 7, 19, 20, self.x, self.y, 38, 44)


class Turtle:
    def __init__(self):
        self.image = load_image('turtle.png')
        self.frame = 0
        self.Right = False
        self.x = 500
        self.y = 25
    def update(self):
        self.frame = (self.frame + 1) % 16
        if self.Right:
            self.x += 5
            if self.x > 800:
                self.Right = False
        else:
            self.x -= 5
            if self.x < 0:
                self.Right = True

    def Draw(self):
        if self.Right:
            self.image.clip_composite_draw(0,  32 * (41 - self.frame) + 12, 20, 35, 0, 'h', self.x, self.y, 40, 70)
        else:
            self.image.clip_draw(0, 32 * (41 - self.frame) + 12, 20, 35, self.x, self.y, 40, 70)