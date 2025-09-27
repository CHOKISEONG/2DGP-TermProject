from pico2d import *
from bird import Bird

def enter():
    global bg, bird, x, y
    x = 400
    y = 300
    bird = Bird(x,y)


def exit():
    pass

def update():
    bird.update()
    pass

def draw():
    bird.draw()

def handle_events():
    events = get_events()
    for event in events:
        pass