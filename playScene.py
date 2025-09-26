from pico2d import *

def enter():
    global bird, x
    bird = load_image('birdSheet/normalBird.png')
    x = 400

def exit():
    pass

def update():
    pass

def draw():
    clear_canvas()
    bird.draw(x, 300)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        pass