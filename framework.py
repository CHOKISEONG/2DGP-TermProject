from pico2d import *

running = True
scene = None

def run(main_scene):
    global running, scene
    open_canvas()
    scene = main_scene
    scene.enter()

    while running:
        clear_canvas()
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
