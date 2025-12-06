from pico2d import *
import framework
from Scene import title_scene as start_scene

def main():
    open_canvas(800,700, full=True)
    framework.run(start_scene)
    close_canvas()

if __name__ == '__main__':
    main()
