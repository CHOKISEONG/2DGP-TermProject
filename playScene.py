from pico2d import *
from dualsense import *
from crowd import Crowd
from black_bird import BlackBird
from shovel_bird import ShovelBird
from map import Map
from musicManager import Music

key_state = set()
joystick = init_joystick()

def enter():
    global bg, player1, music, crowd
    music = Music('sound/120bpm_mainScene.mp3', 120)
    music.play(repeat=True)
    bg = Map()
    player1 = ShovelBird(bg)
    crowd = Crowd()

def exit():
    pass

def update():
    pass
    #DEADZONE = 5000
    #lx, ly = pad_axis
    #dir_vec = get_hex_direction(lx, ly)
    #if abs(lx) > DEADZONE or abs(ly) > DEADZONE:
        #angle = math.atan2(-ly, lx)
        #print(f"스틱 각도(라디안): {angle}, X: {lx}, Y: {ly}")
    #player1.handle_event(events)

def draw():
    bg.draw()
    player1.draw()
    crowd.draw()

def handle_events():
    for event in get_events():
        print("이벤트 발생:", event)
        if event.type == SDL_JOYAXISMOTION:
            print(f"JOY_AXIS {event.axis} = {event.value}")
        elif event.type == SDL_JOYBUTTONDOWN:
            print(f"JOY_BUTTON_DOWN {event.button}")
        elif event.type == SDL_JOYBUTTONUP:
            print(f"JOY_BUTTON_UP {event.button}")
        elif event.type == SDL_KEYDOWN:
            print(f"KEY_DOWN {event.key}")