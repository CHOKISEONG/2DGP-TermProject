from pico2d import *
from Bpm import *

running = True
bpm = Bpm()
scene = None

def run(mainscene):
    global running, bpm, scene
    open_canvas()
    scene = mainscene
    scene.enter()
    while running:
        bpm.update()
        scene.handle_events()
        scene.update()
        scene.draw()
        update_canvas()
    scene.exit()
    close_canvas()

def changeScene(newScene):
    global scene
    if scene is not None:
        scene.exit()
    scene = newScene
    scene.enter()

def quit():
    global running
    running = False
