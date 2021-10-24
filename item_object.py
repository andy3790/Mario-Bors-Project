from pico2d import *

# Game object class here
class Item_Mushroom:
    def __init__(self):
        self.image = load_image('mushroom.png')
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