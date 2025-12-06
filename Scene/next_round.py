from pico2d import *
import framework
import game_world
import Global.myEnum
from Scene import victory_scene

def init():
    from Scene.play_scene import sfx
    global timer

    sfx.play('win')
    timer = get_time()

def handle_events():
    pass

def update():
    global timer
    from Scene.play_scene import player1, player2

    if player1.hp.final_hp <= 0:
        print('player2 최종 우승')
        Global.myEnum.victory_player = 'player2 '
        framework.push_mode(victory_scene)
    elif player2.hp.final_hp <= 0:
        print('player1 최종 우승')
        Global.myEnum.victory_player = 'player1 '
        framework.push_mode(victory_scene)

    if get_time() - timer > 3.0:
        if player1.hp.hp <= 0:
            player1.hp.hp = 9
        elif player2.hp.hp <= 0:
            player2.hp.hp = 9
        framework.pop_mode()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    print('ending_scene finished')

def pause():
    print('ending_scene paused')

def resume():
    print('ending_scene resumed')