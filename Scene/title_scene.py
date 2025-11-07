from pico2d import *
import framework
from Scene import play_scene
from Scene import character_selection_scene
from Character.crowd import Crowd

image = None
image_white = None
start_button = None
sound = None
crowd = None
mouse_x = 400.0
mouse_y = 300.0

def init():
    global image, image_white, image_white_frame, sound, crowd, img_timer, df, start_button, font, button_ds
    image = load_image('map/image/title.png')

    image_white = load_image('map/image/title_white.png')
    image_white_frame = 0
    df = 1

    start_button = load_image('UI/image/start_button.png')
    button_ds = 1.0

    img_timer = get_time()
    sound = load_wav('Sound/music/titleMusic.wav')
    sound.repeat_play()
    crowd = Crowd('title')

    font = load_font('ENCR10B.TTF', 32)


def finish():
    global image, image_white, image_white_frame, sound, crowd, img_timer, df, start_button, font, button_ds
    del image, image_white, image_white_frame, sound, crowd, img_timer, df, start_button, font, button_ds


def handle_events():
    global mouse_x, mouse_y, button_ds

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, get_canvas_height() - event.y
            if 310 < mouse_x < 510 and 150 < mouse_y < 230:
                button_ds = 1.1
            else:
                button_ds = 1.0

            if mouse_x < 100: mouse_x = 100
            elif mouse_x > 500: mouse_x = 500
            if mouse_y < 200: mouse_y = 200

        elif event.type == SDL_MOUSEBUTTONDOWN and img_timer >= 6.0:
            if 310 < mouse_x < 510 and 150 < mouse_y < 230:
                framework.push_mode(character_selection_scene)


def update():
    global img_timer, image_white_frame, df

    cur_time = get_time()
    if cur_time - img_timer > 0.142:
        img_timer = cur_time
        image_white_frame += df
        if image_white_frame > 16 or image_white_frame < 1:
            df = -df


def draw():
    global cur_time, mouse_x, mouse_y, button_ds
    clear_canvas()

    image_white.clip_draw((image_white_frame % 6) * 128,600 - 96 * (image_white_frame // 6 + 1),128,96,400,300,800,600)
    if img_timer >= 6.0:
        image.draw(400,300)
        crowd.draw_title(mouse_x, mouse_y)
        start_button.clip_draw(0,30,100,50,400,200, 220 * button_ds,100 * button_ds)
    else:
        font.draw(300,400, '2023182034')
        font.draw(300,350, 'Cho Kiseong')

    update_canvas()



def pause():
    print('hi')
def resume(): pass