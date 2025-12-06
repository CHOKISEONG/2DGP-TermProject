from pico2d import *
import framework
import game_world
from Character.crowd import Crowd
import Global.myEnum

victory = None

class VictoryImg:
    def __init__(self):
        self.victory_image = load_image('map/image/title.png')
        self.timer = get_time()

        self.crowd = Crowd('victory')

        self.font = load_font('ENCR10B.TTF', 110)

    def update(self):
        cur_time = get_time()
        if cur_time - self.timer > 6.0:
            quit()

    def draw(self):
        self.victory_image.clip_draw(0, 0, 800, 600, 400, 350, 800, 700)
        self.crowd.draw_victory()
        self.font.draw(0, 350, str(Global.myEnum.victory_player + 'win!!'))



def init():
    global victory
    victory = VictoryImg()

def handle_events():
    event_list = get_events()
    for event in event_list:
        pass


def update():
    global victory
    victory.update()

def draw():
    global victory
    victory.draw()

def finish():
    pass

def pause():
    pass

def resume():
    pass