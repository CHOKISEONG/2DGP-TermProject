from pico2d import *
import game_world
import framework

settingPanel = None

def init():
    global panel
    settingPanel = SettingPannel()
    game_world.add_object(settingPanel, 2)

def finish():
    game_world.remove_object(panel)

def update(): pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_0:
                play_mode.boy.item = None
            elif event.key == SDLK_1:
                play_mode.boy.item = 'Ball'
            elif event.key == SDLK_2:
                play_mode.boy.item = 'BigBall'
            game_framework.pop_mode()

def pause(): pass
def resume(): pass