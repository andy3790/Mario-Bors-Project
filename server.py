from collections import defaultdict

TileMap = defaultdict(dict)
PIXEL_PER_METER = (10.0 / 0.2) # 10 pixel 20 cm
tileSize = PIXEL_PER_METER # 1 m

mario = None
map = None
enemys = []
items = []
mapObjects = []