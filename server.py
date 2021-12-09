from collections import defaultdict

TileMap = defaultdict(dict)
PIXEL_PER_METER = (10.0 / 0.2) # 10 pixel 20 cm
Gravity = 9.8 * PIXEL_PER_METER
tileSize = PIXEL_PER_METER # 1 m
MAX_CAMERA_POS = 0
MIN_CAMERA_POS = 0
cameraPos = 0
bgm_volume = 16
effect_sound_volume = 32


debugMod = False
mario = None
map = None
enemys = []
items = []
blocks = []
mapObjects = []