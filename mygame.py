import game_framework
import pico2d

import start_state as start_state
import server

pico2d.open_canvas(int(server.tileSize * 16), int(server.tileSize * 12))
game_framework.run(start_state)
pico2d.close_canvas()