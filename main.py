from pico2d import *
import framework
from Scene import character_selection_scene as start_scene

def main():
    open_canvas(800,600)
    framework.run(start_scene)
    close_canvas()

if __name__ == '__main__':
    main()
