from pico2d import *

import game_framework

# Character Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Character Action Speed
# TIME_PER_ACTION = 1.0
# ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
# FRAMES_PER_ACTION = 9

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER,  SHIFT_DOWN, SHIFT_UP = range(7)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
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
        elif mario.dir == -1:
            mario.image_s_idle.clip_composite_draw(int(mario.frame_x) * 22, 199 - (int(mario.frame_y) * 22 + 23), 23, 23, 0, 'h', mario.x, mario.y, mario.size_x, mario.size_y)

class WalkState:
    TIME_PER_ACTION = 1.0
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
        pass

    def exit(mario, event):
        pass

    def do(mario):
        mario.x += mario.velocity * RUN_SPEED_PPS * game_framework.frame_time

        mario.frame_x = (mario.frame_x + WalkState.ONE_ACTION * game_framework.frame_time)
        if mario.frame_x // 9 == 1:
            mario.frame_y = (mario.frame_y + 1)
            mario.frame_x = mario.frame_x % 9
        if mario.frame_y >= 3:
            mario.frame_x, mario.frame_y = 0, 0;
        pass

    def draw(mario):
        if mario.dir == 1:
            mario.image_s_walk.clip_composite_draw(int(mario.frame_x) * 24, 73 - (int(mario.frame_y) * 24 + 25), 25, 25, 0, '', mario.x, mario.y, mario.size_x, mario.size_y)
        elif mario.dir == -1:
            mario.image_s_walk.clip_composite_draw(int(mario.frame_x) * 24, 73 - (int(mario.frame_y) * 24 + 25), 25, 25, 0, 'h', mario.x, mario.y, mario.size_x, mario.size_y)

class RunState:
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
        pass

    def exit(mario, event):
        pass

    def do(mario):
        mario.x += mario.velocity * 2 * RUN_SPEED_PPS * game_framework.frame_time

        mario.frame_x = (mario.frame_x + RunState.ONE_ACTION * game_framework.frame_time)
        if mario.frame_x // 7 == 1:
            mario.frame_y = (mario.frame_y + 1)
            mario.frame_x = mario.frame_x % 7
        if mario.frame_y >= 2 and mario.frame_x >= 5:
            mario.frame_x, mario.frame_y = 0, 0;
        pass

    def draw(mario):
        if mario.dir == 1:
            mario.image_s_run.clip_composite_draw(int(mario.frame_x) * 24, 73 - (int(mario.frame_y) * 24 + 25), 25, 25, 0, '', mario.x, mario.y, mario.size_x, mario.size_y)
        elif mario.dir == -1:
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


next_state_table = {
    DashState: {SHIFT_UP: RunState,
                LEFT_UP: IdleState , LEFT_DOWN: IdleState, RIGHT_UP: IdleState, RIGHT_DOWN: IdleState},
    IdleState: {RIGHT_UP: WalkState, LEFT_UP: WalkState, RIGHT_DOWN: WalkState, LEFT_DOWN: WalkState, SLEEP_TIMER: SleepState,
                SHIFT_UP: IdleState, SHIFT_DOWN: IdleState},
    WalkState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: RunState, SHIFT_UP: WalkState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: RunState, SHIFT_UP: WalkState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState, LEFT_UP: RunState, RIGHT_UP: RunState,
                 SHIFT_DOWN: SleepState, SHIFT_UP: SleepState}
}


class Character:
    image = None

    def __init__(self):
        if Character.image == None:
            Character.image = load_image('image/NSMBSmallMario_Misc_.png')
        self.image_s_idle = load_image('image/Mario_small idle 23x23.png')
        self.image_s_walk = load_image('image/Mario_small walk 25x25.png')
        self.image_s_run = load_image('image/Mario_small run 25x25.png')
        self.x, self.y = 800 // 2, 90
        self.size_x, self.size_y = 40, 50
        self.dir = 1
        self.velocity = 0
        self.frame_x = 0
        self.frame_y = 0
        self.timer = 0
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