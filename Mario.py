from pico2d import *

import game_framework
from server import PIXEL_PER_METER


# Character Run Speed
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

Gravity = 9.8 * PIXEL_PER_METER
# Character Action Speed
# TIME_PER_ACTION = 1.0
# ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
# FRAMES_PER_ACTION = 9

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER,  SHIFT_DOWN, SHIFT_UP, SPACE_DOWN, JUMP_TO_IDLE, JUMP_TO_WALK  = range(10)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN
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
            mario.image_s_idle.clip_composite_draw(int(mario.frame_x) * 22, 199 - (int(mario.frame_y) * 22 + 23), 23, 23, 0, '', mario.x, mario.y, mario.size_x, mario.size_y)
        else:
            mario.image_s_idle.clip_composite_draw(int(mario.frame_x) * 22, 199 - (int(mario.frame_y) * 22 + 23), 23, 23, 0, 'h', mario.x, mario.y, mario.size_x, mario.size_y)

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
            mario.image_s_walk.clip_composite_draw(int(mario.frame_x) * 24, 73 - (int(mario.frame_y) * 24 + 25), 25, 25, 0, '', mario.x, mario.y, mario.size_x, mario.size_y)
        else:
            mario.image_s_walk.clip_composite_draw(int(mario.frame_x) * 24, 73 - (int(mario.frame_y) * 24 + 25), 25, 25, 0, 'h', mario.x, mario.y, mario.size_x, mario.size_y)

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
            mario.image_s_run.clip_composite_draw(int(mario.frame_x) * 24, 73 - (int(mario.frame_y) * 24 + 25), 25, 25, 0, '', mario.x, mario.y, mario.size_x, mario.size_y)
        else:
            mario.image_s_run.clip_composite_draw(int(mario.frame_x) * 24, 73 - (int(mario.frame_y) * 24 + 25), 25, 25, 0, 'h', mario.x, mario.y, mario.size_x, mario.size_y)

class DashState:
    def enter(mario, event):
        mario.dir = mario.velocity
        pass

    def exit(mario, event):
        pass

    def do(mario):
        pass

    def draw(mario):
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
        if mario.hight == 0:
            mario.jump_timer = 0
            mario.jstart_pos = mario.y
            mario.hight = 0
        pass

    def exit(mario, event):
        pass

    def do(mario):
        mario.hight = (mario.jump_timer * mario.jump_timer * (-Gravity) / 2) + (mario.jump_timer * mario.jump_power)
        mario.jump_timer += 1 * game_framework.frame_time
        mario.y = mario.jstart_pos + mario.hight
        if mario.velocity != 0:
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

        if mario.y < mario.jstart_pos:
            mario.hight = 0
            mario.y = mario.jstart_pos

            if mario.velocity == 0:
                mario.add_event(JUMP_TO_IDLE)
            else:
                mario.add_event(JUMP_TO_WALK)
        pass

    def draw(mario):
        if mario.velocity > 0:
            mario.image_s_jump.clip_composite_draw(int(mario.frame_x) * 29, 146 - (int(mario.frame_y) * 29 + 30), 30, 30, 0, 'h', mario.x, mario.y, mario.size_x + 5, mario.size_y + 5)
        else:
            mario.image_s_jump.clip_composite_draw(int(mario.frame_x) * 29, 146 - (int(mario.frame_y) * 29 + 30), 30, 30, 0, '', mario.x, mario.y, mario.size_x + 5, mario.size_y + 5)

        pass


next_state_table = {
    DashState: {SHIFT_UP: RunState_Accel,
                LEFT_UP: IdleState , LEFT_DOWN: IdleState, RIGHT_UP: IdleState, RIGHT_DOWN: IdleState},
    IdleState: {RIGHT_UP: WalkState_Accel, LEFT_UP: WalkState_Accel, RIGHT_DOWN: WalkState_Accel, LEFT_DOWN: WalkState_Accel, SLEEP_TIMER: SleepState,
                SHIFT_UP: IdleState, SHIFT_DOWN: IdleState, SPACE_DOWN: JumpState},
    WalkState_Accel: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: RunState_Accel, SHIFT_UP: WalkState_Accel, SPACE_DOWN: JumpState},
    RunState_Accel: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: WalkState_Accel, SHIFT_UP: WalkState_Accel, SPACE_DOWN: JumpState},
    SleepState: {LEFT_DOWN: WalkState_Accel, RIGHT_DOWN: WalkState_Accel, LEFT_UP: WalkState_Accel, RIGHT_UP: WalkState_Accel,
                 SHIFT_DOWN: SleepState, SHIFT_UP: SleepState},
    JumpState: {SPACE_DOWN: JumpState, JUMP_TO_WALK: WalkState_Accel, JUMP_TO_IDLE: IdleState}
}


class Character:
    image = None

    def __init__(self):
        if Character.image == None:
            Character.image = load_image('image/NSMBSmallMario_Misc_.png')
        self.image_s_idle = load_image('image/Mario_small idle 23x23.png')
        self.image_s_walk = load_image('image/Mario_small walk 25x25.png')
        self.image_s_run = load_image('image/Mario_small run 25x25.png')
        self.image_s_jump = load_image('image/Mario_small jump 30x30.png')
        self.x, self.y = 800 // 3, 50
        self.size_x, self.size_y = 50, 60
        self.dir = 1
        self.velocity = 0
        self.frame_x = 0
        self.frame_y = 0
        self.accel = 0
        self.timer = 0
        self.jump_timer = 0
        self.jump_power = 250
        self.jstart_pos = 0
        self.hight = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        pass

    def get_bb(self):
        return self.x - 13, self.y - 23, self.x + 13, self.y + 22

    def add_event(self, event):
        self.event_que.insert(0, event)
        pass

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            if event in next_state_table[self.cur_state]:
                self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        pass

    def draw(self):
        self.cur_state.draw(self)
        debug_print('Velocity :' + str(self.velocity) + ' Dir:' + str(self.dir) + ' State:' + str(self.cur_state))

        draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        pass