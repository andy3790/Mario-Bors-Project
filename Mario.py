from pico2d import *

import game_framework
import game_world
import item_object
import server
from server import PIXEL_PER_METER
from server import Gravity
from collision import Crash_Check
import make_world1_state


# Character Run Speed
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

MARIO_MIN_JUMP_POWER = 150
MARIO_MAX_JUMP_POWER = 800
# Character Action Speed
# TIME_PER_ACTION = 1.0
# ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
# FRAMES_PER_ACTION = 9

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER,  SHIFT_DOWN, SHIFT_UP, SPACE_DOWN, SPACE_UP, JUMP_TO_IDLE, JUMP_TO_WALK, CHECK_TO_JUMP, GAME_OVER, RESETMAP  = range(14)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
    (SDL_KEYUP, SDLK_SPACE): SPACE_UP
}


class SleepState:
    def enter(mario, event):
        pass

    def exit(mario, event):
        pass

    def do(mario):
        pass

    def draw(mario):
        pass

class IdleState:
    TIME_PER_ACTION = 10.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 77
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += 1
        elif event == LEFT_DOWN:
            mario.velocity -= 1
        elif event == RIGHT_UP:
            mario.velocity -= 1
        elif event == LEFT_UP:
            mario.velocity += 1
        mario.accel = 0
        pass

    def exit(mario, event):
        pass

    def do(mario):
        if mario.frame_x / 9 > 0:
            mario.frame_y = (mario.frame_y + IdleState.FRAMES_PER_ACTION * IdleState.ACTION_PER_TIME * game_framework.frame_time) % 9
        mario.frame_x = (mario.frame_x + IdleState.FRAMES_PER_ACTION * IdleState.ACTION_PER_TIME * game_framework.frame_time) % 9
        if mario.frame_y >= 8 and mario.frame_x >= 6:
            mario.frame_x, mario.frame_y = 0, 0;

        pass

    def draw(mario):
        if mario.dir == 1:
            mario.image_s_idle.clip_composite_draw(int(mario.frame_x) * 22, 199 - (int(mario.frame_y) * 22 + 23), 23, 23, 0, '', mario.x - server.cameraPos, mario.y, mario.size_x, mario.size_y)
        else:
            mario.image_s_idle.clip_composite_draw(int(mario.frame_x) * 22, 199 - (int(mario.frame_y) * 22 + 23), 23, 23, 0, 'h', mario.x - server.cameraPos, mario.y, mario.size_x, mario.size_y)

class WalkState_Accel:
    TIME_PER_ACTION = 0.8
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 27
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += 1
        elif event == LEFT_DOWN:
            mario.velocity -= 1
        elif event == RIGHT_UP:
            mario.velocity -= 1
        elif event == LEFT_UP:
            mario.velocity += 1
        mario.dir = mario.velocity
        if mario.frame_x >= 9 or mario.frame_y >= 3:
            mario.frame_x, mario.frame_y = 0, 0
        mario.accel = 0
        pass

    def exit(mario, event):
        pass

    def do(mario):
        mario.x += mario.velocity * RUN_SPEED_PPS * game_framework.frame_time

        mario.frame_x = (mario.frame_x + WalkState_Accel.ONE_ACTION * game_framework.frame_time)
        if mario.frame_x // 9 == 1:
            mario.frame_y = (mario.frame_y + 1)
            mario.frame_x = mario.frame_x % 9
        if mario.frame_y >= 3:
            mario.frame_x, mario.frame_y = 0, 0;
        pass

    def draw(mario):
        if mario.dir == 1:
            mario.image_s_walk.clip_composite_draw(int(mario.frame_x) * 24, 73 - (int(mario.frame_y) * 24 + 25), 25, 25, 0, '', mario.x - server.cameraPos, mario.y, mario.size_x, mario.size_y)
        else:
            mario.image_s_walk.clip_composite_draw(int(mario.frame_x) * 24, 73 - (int(mario.frame_y) * 24 + 25), 25, 25, 0, 'h', mario.x - server.cameraPos, mario.y, mario.size_x, mario.size_y)

        if server.debugMod:
            for i in range(-1,1+1):
                draw_rectangle(int(mario.x / server.tileSize + mario.velocity) * server.tileSize - server.cameraPos, int(mario.y / server.tileSize + i) * server.tileSize, int(mario.x / server.tileSize + mario.velocity + 1) * server.tileSize - server.cameraPos, int(mario.y / server.tileSize + i + 1) * server.tileSize)

class RunState_Accel:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 20
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += 1
        elif event == LEFT_DOWN:
            mario.velocity -= 1
        elif event == RIGHT_UP:
            mario.velocity -= 1
        elif event == LEFT_UP:
            mario.velocity += 1
        mario.dir = mario.velocity
        mario.frame_x = 0
        mario.frame_y = 0
        pass

    def exit(mario, event):
        pass

    def do(mario):
        mario.x += (mario.velocity + mario.accel) * 2 * RUN_SPEED_PPS * game_framework.frame_time
        mario.accel += (mario.velocity / 100) * RUN_SPEED_PPS * game_framework.frame_time
        mario.accel = clamp(-0.8, mario.accel, 0.8)

        mario.frame_x = (mario.frame_x + RunState_Accel.ONE_ACTION * game_framework.frame_time)
        if mario.frame_x // 7 == 1:
            mario.frame_y = (mario.frame_y + 1)
            mario.frame_x = mario.frame_x % 7
        if mario.frame_y >= 2 and mario.frame_x >= 5:
            mario.frame_x, mario.frame_y = 0, 0;
        pass

    def draw(mario):
        if mario.dir == 1:
            mario.image_s_run.clip_composite_draw(int(mario.frame_x) * 24, 73 - (int(mario.frame_y) * 24 + 25), 25, 25, 0, '', mario.x - server.cameraPos, mario.y, mario.size_x, mario.size_y)
        else:
            mario.image_s_run.clip_composite_draw(int(mario.frame_x) * 24, 73 - (int(mario.frame_y) * 24 + 25), 25, 25, 0, 'h', mario.x - server.cameraPos, mario.y, mario.size_x, mario.size_y)

        if server.debugMod:
            for i in range(-1,1+1):
                draw_rectangle(int(mario.x / server.tileSize + mario.velocity) * server.tileSize - server.cameraPos, int(mario.y / server.tileSize + i) * server.tileSize, int(mario.x / server.tileSize + mario.velocity + 1) * server.tileSize - server.cameraPos, int(mario.y / server.tileSize + i + 1) * server.tileSize)

class JumpPowerCheckState:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 30
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += 1
        elif event == LEFT_DOWN:
            mario.velocity -= 1
        elif event == RIGHT_UP:
            mario.velocity -= 1
        elif event == LEFT_UP:
            mario.velocity += 1
        if mario.hight == 0:
            mario.jump_power = MARIO_MAX_JUMP_POWER
            mario.jump_timer = 0
            mario.jstart_pos = 0
            mario.hight = 0
            mario.dir = mario.velocity
        else:
            mario.add_event(CHECK_TO_JUMP)
        pass

    def exit(mario, event):
        mario.jump_power = MARIO_MIN_JUMP_POWER + (MARIO_MAX_JUMP_POWER - MARIO_MIN_JUMP_POWER) * (mario.jump_timer)
        mario.gaccel *= 1.3
        pass

    def do(mario):
        mario.hight = 1
        mario.y += mario.jump_power * game_framework.frame_time
        mario.x += (mario.dir + mario.accel) * RUN_SPEED_PPS * game_framework.frame_time
        mario.accel += (mario.velocity / 100) * RUN_SPEED_PPS * game_framework.frame_time
        mario.accel = clamp(-0.8, mario.accel, 0.8)
        mario.jump_power -= (MARIO_MAX_JUMP_POWER - MARIO_MIN_JUMP_POWER) * game_framework.frame_time
        mario.jump_timer += 1 * game_framework.frame_time
        # print(mario.jump_power)

        mario.frame_x = (mario.frame_x + RunState_Accel.ONE_ACTION * game_framework.frame_time)
        if mario.frame_x // 7 == 1:
            mario.frame_y = (mario.frame_y + 1)
            mario.frame_x = mario.frame_x % 7
        if mario.frame_y >= 3 and mario.frame_x >= 2:
            mario.frame_x, mario.frame_y = 2, 3;

        if mario.jump_timer >= 0.5 or mario.jump_power < MARIO_MIN_JUMP_POWER:
            mario.add_event(CHECK_TO_JUMP)
        pass

    def draw(mario):
        if mario.velocity > 0:
            mario.image_s_jump.clip_composite_draw(int(mario.frame_x) * 29, 146 - (int(mario.frame_y) * 29 + 30), 30, 30, 0, 'h', mario.x - server.cameraPos, mario.y, mario.size_x + 5, mario.size_y + 5)
        else:
            mario.image_s_jump.clip_composite_draw(int(mario.frame_x) * 29, 146 - (int(mario.frame_y) * 29 + 30), 30, 30, 0, '', mario.x - server.cameraPos, mario.y, mario.size_x + 5, mario.size_y + 5)

        if server.debugMod:
            draw_rectangle(int(mario.x / server.tileSize) * server.tileSize - server.cameraPos, int(mario.y / server.tileSize + 1) * server.tileSize, int(mario.x / server.tileSize + 1) * server.tileSize - server.cameraPos, int(mario.y / server.tileSize + 1 + 1) * server.tileSize)
            for i in range(-1,1+1):
                draw_rectangle(int(mario.x / server.tileSize + mario.velocity) * server.tileSize - server.cameraPos, int(mario.y / server.tileSize + i) * server.tileSize, int(mario.x / server.tileSize + mario.velocity + 1) * server.tileSize - server.cameraPos, int(mario.y / server.tileSize + i + 1) * server.tileSize)

        pass

class JumpState:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 30
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += 1
        elif event == LEFT_DOWN:
            mario.velocity -= 1
        elif event == RIGHT_UP:
            mario.velocity -= 1
        elif event == LEFT_UP:
            mario.velocity += 1
        # if mario.hight == 0:
        #     mario.jump_power = 200
        #     mario.jump_timer = 0
        #     mario.jstart_pos = mario.y
        #     mario.hight = 0
        #     mario.dir = mario.velocity
        pass

    def exit(mario, event):
        pass

    def do(mario):
        mario.hight = 1
        if mario.y <= mario.jstart_pos:
            mario.hight = 0
        # mario.y = mario.jstart_pos + mario.hight
        mario.y += mario.jump_power * game_framework.frame_time
        # if mario.velocity != 0:
        mario.x += (mario.dir + mario.accel) * RUN_SPEED_PPS * game_framework.frame_time
        # print(mario.jump_timer)
        mario.accel += (mario.velocity / 100) * RUN_SPEED_PPS * game_framework.frame_time
        mario.accel = clamp(-0.8, mario.accel, 0.8)

        mario.frame_x = (mario.frame_x + RunState_Accel.ONE_ACTION * game_framework.frame_time)
        if mario.frame_x // 7 == 1:
            mario.frame_y = (mario.frame_y + 1)
            mario.frame_x = mario.frame_x % 7
        if mario.frame_y >= 3 and mario.frame_x >= 2:
            mario.frame_x, mario.frame_y = 2, 3;

        if mario.hight == 0:
            if mario.velocity == 0:
                mario.add_event(JUMP_TO_IDLE)
            else:
                mario.add_event(JUMP_TO_WALK)
        pass

    def draw(mario):
        if mario.velocity > 0:
            mario.image_s_jump.clip_composite_draw(int(mario.frame_x) * 29, 146 - (int(mario.frame_y) * 29 + 30), 30, 30, 0, 'h', mario.x - server.cameraPos, mario.y, mario.size_x + 5, mario.size_y + 5)
        else:
            mario.image_s_jump.clip_composite_draw(int(mario.frame_x) * 29, 146 - (int(mario.frame_y) * 29 + 30), 30, 30, 0, '', mario.x - server.cameraPos, mario.y, mario.size_x + 5, mario.size_y + 5)

        if server.debugMod:
            for i in range(-1,1+1):
                draw_rectangle(int(mario.x / server.tileSize + mario.velocity) * server.tileSize - server.cameraPos, int(mario.y / server.tileSize + i) * server.tileSize, int(mario.x / server.tileSize + mario.velocity + 1) * server.tileSize - server.cameraPos, int(mario.y / server.tileSize + i + 1) * server.tileSize)
        pass



class GameOverState:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 13
    ONE_ACTION = FRAMES_PER_ACTION * ACTION_PER_TIME

    def enter(mario, event):
        mario.jstart_pos = mario.y + 10
        mario.frame_x = 0
        mario.frame_y = 0
        mario.jump_timer = 0
        mario.jump_power = 200
        pass

    def exit(mario, event):
        pass

    def do(mario):
        mario.hight = (mario.jump_timer * mario.jump_timer * (-Gravity) / 2) + (mario.jump_timer * mario.jump_power)
        mario.jump_timer += 1 * game_framework.frame_time
        mario.y = mario.jstart_pos + mario.hight

        mario.frame_x = (mario.frame_x + GameOverState.ONE_ACTION * game_framework.frame_time) % 13

        if mario.y < -1000:
            print(mario.y)
            mario.life -= 1
            mario.add_event(RESETMAP)
        pass

    def draw(mario):
        mario.image_s_game_over.clip_composite_draw(int(mario.frame_x) * 29, 0, 30, 30, 0, '', mario.x - server.cameraPos, mario.y, mario.size_x + 5, mario.size_y + 5)
        pass

class ResetState:
    def enter(mario, event):
        pass

    def exit(mario, event):
        pass

    def do(mario):
        pass

    def draw(mario):
        if mario.life <= 0:
            print("GameOverCheck!")
        else:
            game_framework.change_state(make_world1_state)
        pass

next_state_table = {
    IdleState: {RIGHT_UP: WalkState_Accel, LEFT_UP: WalkState_Accel, RIGHT_DOWN: WalkState_Accel, LEFT_DOWN: WalkState_Accel, SLEEP_TIMER: SleepState,
                SHIFT_UP: IdleState, SHIFT_DOWN: IdleState, SPACE_DOWN: JumpPowerCheckState, GAME_OVER: GameOverState},
    WalkState_Accel: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: RunState_Accel, SHIFT_UP: WalkState_Accel, SPACE_DOWN: JumpPowerCheckState, GAME_OVER: GameOverState},
    RunState_Accel: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: WalkState_Accel, SHIFT_UP: WalkState_Accel, SPACE_DOWN: JumpPowerCheckState, GAME_OVER: GameOverState},
    SleepState: {LEFT_DOWN: WalkState_Accel, RIGHT_DOWN: WalkState_Accel, LEFT_UP: WalkState_Accel, RIGHT_UP: WalkState_Accel,
                 SHIFT_DOWN: SleepState, SHIFT_UP: SleepState, GAME_OVER: GameOverState},
    JumpPowerCheckState: {SPACE_DOWN: JumpState, SPACE_UP: JumpState, CHECK_TO_JUMP: JumpState, GAME_OVER: GameOverState},
    JumpState: {SPACE_DOWN: JumpState, JUMP_TO_WALK: WalkState_Accel, JUMP_TO_IDLE: IdleState, GAME_OVER: GameOverState},
    GameOverState: {RESETMAP: ResetState}
}


class Character:
    image = None

    def __init__(self, sx=0, sy=0):
        if Character.image == None:
            Character.image = load_image('image/NSMBSmallMario_Misc_.png')
        self.image_s_idle = load_image('image/Mario_small idle 23x23.png')
        self.image_s_walk = load_image('image/Mario_small walk 25x25.png')
        self.image_s_run = load_image('image/Mario_small run 25x25.png')
        self.image_s_jump = load_image('image/Mario_small jump 30x30.png')
        self.image_s_game_over = load_image('image/Mario_small GameOver 30x30.png')
        self.sound_life_lost = load_music('sound/life-lost.mp3')
        self.sound_life_lost.set_volume(server.bgm_volume)
        self.sound_power_up = load_wav('sound/power up.wav')
        self.sound_power_up.set_volume(server.effect_sound_volume)

        self.x, self.y = sx * server.tileSize + server.tileSize / 2, sy * server.tileSize + server.tileSize / 2
        self.size_x, self.size_y = server.tileSize * 1.3, server.tileSize * 1.3
        self.hp = 1
        self.dir = 1
        self.velocity = 0
        self.frame_x = 0
        self.frame_y = 0
        self.accel = 0
        self.timer = 0
        self.jump_timer = 0
        self.jump_power = MARIO_MIN_JUMP_POWER
        self.jstart_pos = 0
        self.hight = 0
        self.gaccel = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.coin = 0
        self.life = 5
        self.invincibility_timer = 0
        pass

    def get_bb(self):
        return self.x - 13, self.y - server.tileSize / 2, self.x + 13, self.y + server.tileSize / 2.5

    def add_event(self, event):
        self.event_que.insert(0, event)
        pass

    def gravity(self):
        self.gaccel += Gravity * 1.5 * game_framework.frame_time
        self.y -= self.gaccel * game_framework.frame_time

    def update(self):
        if self.invincibility_timer > 0:
            self.invincibility_timer -= game_framework.frame_time
        if self.invincibility_timer < 0:
            self.invincibility_timer = 0

        self.cur_state.do(self)
        self.x = clamp(13, self.x, server.tileSize * 200)
        if self.cur_state != GameOverState:
            for item in server.items:
                if Crash_Check(self, item):
                    if isinstance(item, item_object.Item_Mushroom):
                        if self.hp == 1:
                            self.hp += 1
                            self.sound_power_up.play(1)
                        server.items.remove(item)
                        game_world.remove_object(item)
            for i in range(-1,1+1):
                # 전방 충돌체크
                if Crash_Check(server.mario, server.TileMap[int(self.x / server.tileSize + self.velocity)][int(self.y / server.tileSize + i)]):
                    server.mario.x = server.TileMap[int(self.x / server.tileSize + self.velocity)][int(self.y / server.tileSize + i)].x + (server.tileSize / 2 + 13) * self.velocity * -1
                # 상단 충돌체크
                if Crash_Check(server.mario, server.TileMap[int(self.x / server.tileSize + i)][int(self.y / server.tileSize + 1)]):
                    server.mario.y = server.TileMap[int(self.x / server.tileSize + i)][int(self.y / server.tileSize + 1)].y - (server.tileSize)
                    server.TileMap[int(self.x / server.tileSize + i)][int(self.y / server.tileSize + 1)].hit()
                    self.add_event(CHECK_TO_JUMP)

            if self.invincibility_timer <= 0:
                for enemy in game_world.all_layer_objects(4):
                    if Crash_Check(server.mario, enemy):
                        self.hp -= 1
                        if self.hp <= 0:
                            self.sound_life_lost.play(1)
                            self.add_event(GAME_OVER)
                            # print("damage!")
                        else:
                            self.invincibility_timer = 2

            if self.x - server.cameraPos < server.tileSize * 6:
                server.cameraPos = clamp(server.MIN_CAMERA_POS, server.cameraPos - game_framework.frame_time * server.tileSize * (5 + self.accel*-5), server.MAX_CAMERA_POS)
            elif self.x - server.cameraPos > server.tileSize * 10:
                server.cameraPos = clamp(server.MIN_CAMERA_POS, server.cameraPos + game_framework.frame_time * server.tileSize * (5 + self.accel*5), server.MAX_CAMERA_POS)

        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            if event in next_state_table[self.cur_state]:
                self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        if self.cur_state != GameOverState:
            self.gravity()
            if self.y <= 0:
                self.add_event(GAME_OVER)
                self.y = server.tileSize
                # print("gameOver")

            # 하단 충돌체크
            elif Crash_Check(server.mario, server.TileMap[int(self.x / server.tileSize)][int(self.y / server.tileSize - 1)]):
                self.gaccel = 0
                server.mario.y = server.TileMap[int(self.x / server.tileSize)][int(self.y / server.tileSize - 1)].y + (server.tileSize)
                self.jstart_pos = server.mario.y
            for ob in game_world.all_layer_objects(4):
                if Crash_Check(server.mario, ob) and self.cur_state == JumpState:
                    self.gaccel = 0
                    self.jump_power = 200
                    ob.damaged()

            for item in game_world.all_layer_objects(3):
                if Crash_Check(server.mario, item):
                    pass

        pass

    def draw(self):
        if int(self.invincibility_timer*10 % 2) == 0:
            self.cur_state.draw(self)

        if server.debugMod:
            debug_print('Velocity :' + str(self.velocity) + ' Dir:' + str(self.dir) + ' State:' + str(self.cur_state))
            a1,a2,a3,a4 = self.get_bb()
            draw_rectangle(a1 - server.cameraPos,a2,a3 - server.cameraPos,a4)
        pass

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        pass

    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'coin': self.coin, 'life': self.life}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)
