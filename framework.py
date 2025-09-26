from pico2d import *
from Bpm import *

running = True
bpm = Bpm()
scene = None

def run(main_scene):
    global running, bpm, scene
    open_canvas()
    scene = main_scene
    scene.enter()
    while running:
        bpm.update()
        scene.handle_events()
        scene.update()
        scene.draw()
        update_canvas()
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
