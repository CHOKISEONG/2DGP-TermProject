from pico2d import *
import framework
from Scene import play_scene
from Character.crowd import Crowd

image = None
image_white = None
sound = None
crowd = None

def init():
    global image, image_white, image_white_frame, sound, crowd, img_timer, df
    image = load_image('map/image/title.png')
    image_white = load_image('map/image/title_white.png')
    image_white_frame = 0
    img_timer = get_time()
    sound = load_wav('Sound/music/titleMusic.wav')
    sound.repeat_play()
    crowd = Crowd('title')
    df = 1


def finish():
    global image, image_white, sound, crowd
    del image, image_white, sound, crowd

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            framework.change_mode(play_scene)

def draw():

    clear_canvas()

    image_white.clip_draw((image_white_frame % 6) * 128,600 - 96 * (image_white_frame // 6 + 1),128,96,400,300,800,600)
    image.draw(400,300)
    crowd.draw_title()

    update_canvas()

def update():
    global img_timer, image_white_frame, df
    cur_time = get_time()
    if cur_time - img_timer > 0.1:
        img_timer = cur_time
        image_white_frame += df
        if image_white_frame > 16 or image_white_frame < 1:
            df = -df
        print(image_white_frame)

def pause(): pass
def resume(): pass