from pico2d import *
import framework
from Scene import play_scene as start_scene


def main():
    open_canvas()
    framework.run(start_scene)
    close_canvas()

if __name__ == '__main__':
    main()
