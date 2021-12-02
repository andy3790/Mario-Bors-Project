import game_framework
import pico2d

import main_state as start_state

pico2d.open_canvas(800, 600)
game_framework.run(start_state)
pico2d.close_canvas()