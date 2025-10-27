import time
from pico2d import *

running = True
scene = None

FPS = 60
frame_time = 1.0 / FPS

def run(main_scene):
    global running, scene
    open_canvas(800,600)
    scene = main_scene
    scene.enter()

    while running:
        start_time = get_time()

        clear_canvas()
        scene.handle_events()
        scene.update()
        scene.draw()
        update_canvas()

        elapsed = get_time() - start_time
        if elapsed < frame_time:
            delay(frame_time - elapsed)

    scene.exit()
    close_canvas()

def change_scene(new_scene):
    global scene
    if scene is not None:
        scene.exit()
    scene = new_scene
    scene.enter()

def quit():
    global running
    running = False
