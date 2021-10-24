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


class Item_Box:
    def __init__(self):
        self.image = load_image('qblock_strips.png')
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


def handle_events():
    global running
    global mario
    global marioMove
    global marioRight
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            marioMove = True
            marioRight = False
            mario.framey = 4
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            marioMove = True
            marioRight = True
            mario.framey = 4
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            marioMove = False
            mario.framey = 8
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            marioMove = False
            mario.framey = 8
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            mario.Jump = True

# initialization code
WIN_HIGHT = 600
WIN_WIDTH = 800
open_canvas(WIN_WIDTH, WIN_HIGHT)
running = True
marioMove = False
marioRight = False
map = load_image('background.png')
mario = Character()
gomba = Gomba()
turtle = Turtle()
mushroom = Item_Mushroom()
itembox = Item_Box()

# game main loop code

while running:
    handle_events()
    clear_canvas()
    mario.update()
    gomba.update()
    turtle.update()

    mushroom.update()
    itembox.update()

    if marioMove:
        mario.move(marioRight)


    delay(0.05)
    map.clip_draw(520,500,500,480,400,300, 800, 600)
    gomba.Draw()
    turtle.Draw()

    mushroom.Draw()
    itembox.Draw()

    mario.Draw()
    update_canvas()

# finalization code
close_canvas()