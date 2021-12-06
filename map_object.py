from pico2d import *

import server

# Game object class here
class Map_BackGround:

    def __init__(self):
        self.image = load_image('image/1-1_background.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def get_bb(self):
        return 0, 0, 800, 35

    def draw(self):
        self.image.clip_draw_to_origin(self.q1l, self.q1b, self.q1w, self.q1h, 0, 0)                        # quadrant 1
        self.image.clip_draw_to_origin(self.q2l, self.q2b, self.q2w, self.q2h, self.q1w, 0)                 # quadrant 2

    def update(self):
        # quadrant 1
        self.q1l = (int(server.mario.x) - self.canvas_width // 2) % self.w
        self.q1b = 0
        self.q1w = clamp(0, self.w - self.q1l, self.w)
        self.q1h = self.canvas_height
        # quadrand 2
        self.q2l = 0
        self.q2b = self.q1b
        self.q2w = self.canvas_width - self.q1w
        self.q2h = self.q1h


    def handle_event(self, event):
        pass