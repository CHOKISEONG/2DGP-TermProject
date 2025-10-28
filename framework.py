from pico2d import *

running = None
stack = []

FPS = 60
frame_time = 1.0 / FPS

def change_mode(mode):
    global stack

    # 현재 씬을 종료
    if stack:
        stack[-1].finish()
        stack.pop()

    # 새로운 씬을 시작
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if stack:
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if stack:
        # 현재 씬을 종료
        stack[-1].finish()
        stack.pop()

    # 이전 씬을 다시 시작
    if stack:
        stack[-1].resume()


def quit():
    global running
    running = False

def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    # 게임 로직
    while running:
        start_time = get_time()

        clear_canvas()
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        update_canvas()

        elapsed = get_time() - start_time
        if elapsed < frame_time:
            delay(frame_time - elapsed)

    # 스택의 모든 씬들 제거
    while stack:
        stack[-1].finish()
        stack.pop()