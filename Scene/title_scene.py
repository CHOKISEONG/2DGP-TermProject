from pico2d import *
import framework
import game_world
from Scene import play_scene
from Scene import character_selection_scene
from Character.crowd import Crowd

title = None
title_sound = None
mouse_x = 400.0
mouse_y = 300.0

class TitleImg:
    def __init__(self):
        self.title_image = load_image('map/image/title.png')

        self.image_white = load_image('map/image/title_white.png')
        self.image_white_frame = 0
        self.df = 1

        self.start_button = load_image('UI/image/start_button.png')
        self.button_ds = 1.0
        self.timer = get_time()

        self.crowd = Crowd('title')

        self.my_name = load_font('ENCR10B.TTF', 32)

        self.is_paused = False

    def update(self, beat_idx):
        cur_time = get_time()
        if cur_time - self.timer > 0.142:
            self.timer = cur_time
            self.image_white_frame += self.df
            if self.image_white_frame > 16 or self.image_white_frame < 1:
                self.df = -self.df

    def draw(self):
        if self.is_paused:
            self.image_white.clip_draw((self.image_white_frame % 6) * 128, 600 - 96 * (self.image_white_frame // 6 + 1),
                                       128, 96, 400, 300,
                                       800, 600)
            self.title_image.draw(400, 300)
            self.crowd.draw_title(mouse_x, mouse_y)
        else:
            self.image_white.clip_draw((self.image_white_frame % 6) * 128, 600 - 96 * (self.image_white_frame // 6 + 1), 128, 96, 400, 300,
                                  800, 600)
            if self.timer >= 6.0:
                self.title_image.draw(400, 300)
                self.crowd.draw_title(mouse_x, mouse_y)
                self.start_button.clip_draw(0, 30, 100, 50, 400, 200, 220 * self.button_ds, 100 * self.button_ds)
            else:
                self.my_name.draw(300, 400, '2023182034')
                self.my_name.draw(300, 350, 'Cho Kiseong')



def init():
    global title, timer, title_sound, my_name
    title = TitleImg()
    game_world.add_object(title)

    title_sound = load_wav('Sound/music/titleMusic.wav')
    title_sound.repeat_play()


def finish():
    print('title_scene finished')
    global image, image_white, image_white_frame, title_sound, crowd, img_timer, df, start_button, font, button_ds
    del image, image_white, image_white_frame, title_sound, crowd, img_timer, df, start_button, font, button_ds


def handle_events():
    global title, mouse_x, mouse_y, button_ds

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, get_canvas_height() - event.y
            if 310 < mouse_x < 510 and 150 < mouse_y < 230:
                title.button_ds = 1.1
            else:
                title.button_ds = 1.0

            if mouse_x < 100: mouse_x = 100
            elif mouse_x > 500: mouse_x = 500
            if mouse_y < 200: mouse_y = 200

        elif event.type == SDL_MOUSEBUTTONDOWN and title.timer >= 6.0:
            if 310 < mouse_x < 510 and 150 < mouse_y < 230:
                framework.push_mode(character_selection_scene)


def update():
    game_world.update(0)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()



def pause():
    print('title_scene paused')
    title.is_paused = True
    title_sound.set_volume(20)

def resume():
    print('title_scene resumed')
    title.is_paused = False