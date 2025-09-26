from pico2d import *
from Bird import Bird

def enter():
    global bird, x, y
    x = 400
    y = 300
    bird = Bird(x,y)


def exit():
    pass

def update():
    pass

def draw():
    clear_canvas()
    bird.draw()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        pass