import sdl2
import math

pad_axis = [0,0] # x,y값
HEX_DIRECTIONS = [
    (math.cos(math.radians(0)),   math.sin(math.radians(0))),
    (math.cos(math.radians(60)),  math.sin(math.radians(60))),
    (math.cos(math.radians(120)), math.sin(math.radians(120))),
    (math.cos(math.radians(180)), math.sin(math.radians(180))),
    (math.cos(math.radians(240)), math.sin(math.radians(240))),
    (math.cos(math.radians(300)), math.sin(math.radians(300))),
]

def get_hex_direction(lx, ly):
    if abs(lx) < 5000 and abs(ly) < 5000:
        return None
    angle = math.atan2(-ly, lx)
    angle_deg = math.degrees(angle) % 360
    idx = int((angle_deg + 30) // 60) % 6
    return HEX_DIRECTIONS[idx]

def init_joystick():
    sdl2.SDL_InitSubSystem(sdl2.SDL_INIT_JOYSTICK | sdl2.SDL_INIT_GAMECONTROLLER)
    if sdl2.SDL_NumJoysticks() > 0:
        joystick = sdl2.SDL_JoystickOpen(0)  # 첫 번째 패드
        print('Joystick opened:', joystick)
        return joystick
    else:
        print('No joystick found')
        return None