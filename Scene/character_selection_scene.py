from pico2d import *
import framework
import game_world
from Scene import play_scene
from Character.bird import AnimationController

player1_character = None
player2_character = None
start_selected_music = None

# i가 0~3 까지 4개의 캐릭터가 마우스랑 겹치는지 확인해서 사이즈 증가
def is_selected(mouse_x, mouse_y, x, y, i):
    half_w = size[0] * ds[i] / 3.0
    half_h = size[1] * ds[i] / 3.0
    bx, by = x, y
    if (bx - half_w) <= mouse_x <= (bx + half_w) and (by - half_h) <= mouse_y <= (by + half_h):
        ds[i] = 1.2
        return True
    else:
        ds[i] = 1.0
        return False

def init():
    print('character_selection_scene init')
    global start_selected_music, select_sound, select_sound2, select_font, bird1, bird1_pos, bird2, bird2_pos, bird3, bird3_pos, bird4, bird4_pos, choice_font, choice_font_pos, rotate, rotate_idx, delay, time, delay_growth, max_delay, size, ds
    start_selected_music = load_music('Sound/sample/character_select_start.mp3')
    start_selected_music.set_volume(100)
    start_selected_music.play()

    bird1 = AnimationController('Character/image/shovelBird.png')
    bird1_pos = [400, 0]
    bird2 = AnimationController('Character/image/blackBird.png')
    bird2_pos = [400, 0]
    bird3 = AnimationController('Character/image/kingBird.png')
    bird3_pos = [400, 0]
    bird4 = AnimationController('Character/image/hatBird.png')
    bird4_pos = [400, 0]
    size = [50, 50]
    ds = [1.0, 1.0, 1.0, 1.0]

    choice_font = load_font('ENCR10B.TTF', 16)
    choice_font_pos = [0, -10, 0, -10]

    rotate = ['down', 'left', 'up', 'right']
    rotate_idx = 0
    delay = 0.1
    time = 0.0
    delay_growth = 0.02
    max_delay = 0.9

    select_sound = load_music('Sound/sample/select_sound.mp3')
    select_sound2 = load_music('Sound/sample/select_sound2.mp3')

def handle_events():
    global player1_character, player2_character, select_font, choice_font_pos

    # 캐릭터 이동 애니메이션 완료 후에 입력 받게 설정
    if bird1_pos[1] < 350:
        return

    # 둘 다 캐릭터 고르기 완료하면 플레이 씬으로 이동
    if player1_character is not None and player2_character is not None:
        framework.change_mode(play_scene)
        return

    event_list = get_events()
    for event in event_list:
        mouse_x, mouse_y = event.x, get_canvas_height() - event.y
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            if is_selected(mouse_x, mouse_y, *bird1_pos, 0):
                if player1_character is None:
                    choice_font_pos[0], choice_font_pos[1] = bird1_pos[0] - 50, bird1_pos[1] - 100
                elif choice_font_pos[0] != bird1_pos[0] - 50:
                        choice_font_pos[2], choice_font_pos[3] = bird1_pos[0] - 50, bird1_pos[1] - 100
            elif is_selected(mouse_x, mouse_y, *bird2_pos, 1):
                if player1_character is None:
                    choice_font_pos[0], choice_font_pos[1] = bird2_pos[0] - 50, bird2_pos[1] - 100
                elif choice_font_pos[0] != bird2_pos[0] - 50:
                    choice_font_pos[2], choice_font_pos[3] = bird2_pos[0] - 50, bird2_pos[1] - 100
            elif is_selected(mouse_x, mouse_y, *bird3_pos, 2):
                if player1_character is None:
                    choice_font_pos[0], choice_font_pos[1] = bird3_pos[0] - 50, bird3_pos[1] - 100
                elif choice_font_pos[0] != bird3_pos[0] - 50:
                    choice_font_pos[2], choice_font_pos[3] = bird3_pos[0] - 50, bird3_pos[1] - 100
            elif is_selected(mouse_x, mouse_y, *bird4_pos, 3):
                if player1_character is None:
                    choice_font_pos[0], choice_font_pos[1] = bird4_pos[0] - 50, bird4_pos[1] - 100
                elif choice_font_pos[0] != bird4_pos[0] - 50:
                    choice_font_pos[2], choice_font_pos[3] = bird4_pos[0] - 50, bird4_pos[1] - 100
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if is_selected(mouse_x, mouse_y, *bird1_pos, 0):
                if player1_character is None:
                    player1_character = 'shovelBird'
                    select_sound.play()
                elif player1_character == 'shovelBird':
                    return
                else:
                    player2_character = 'shovelBird'
                    select_sound2.play()
            elif is_selected(mouse_x, mouse_y, *bird2_pos, 1):
                if player1_character is None:
                    player1_character = 'blackBird'
                    select_sound.play()
                elif player1_character == 'blackBird':
                    return
                else:
                    player2_character = 'blackBird'
                    select_sound2.play()
            elif is_selected(mouse_x, mouse_y, *bird3_pos, 2):
                if player1_character is None:
                    player1_character = 'kingBird'
                    select_sound.play()
                elif player1_character == 'kingBird':
                    return
                else:
                    player2_character = 'kingBird'
                    select_sound2.play(1)
            elif is_selected(mouse_x, mouse_y, *bird4_pos, 3):
                if player1_character is None:
                    player1_character = 'hatBird'
                    select_sound.play(1)
                elif player1_character == 'hatBird':
                    return
                else:
                    player2_character = 'hatBird'
                    select_sound2.play(1)



def update():
    global time, delay, rotate_idx
    game_world.update(0)
    if bird1_pos[1] < 350:
        bird1_pos[1] += 1
        bird1_pos[0] -= 0.5
    if bird2_pos[1] < 350:
        bird2_pos[1] += 1
        bird2_pos[0] -= 0.15
    if bird3_pos[1] < 350:
        bird3_pos[1] += 1
        bird3_pos[0] += 0.15
    if bird4_pos[1] < 350:
        bird4_pos[1] += 1
        bird4_pos[0] += 0.5
        size[0] += 0.3
        size[1] += 0.3

    time += 0.01
    if time < delay:
        return

    if bird4_pos[1] < 350:
        rotate_idx = (rotate_idx + 1) % len(rotate)
        new_direction = rotate[rotate_idx]
        bird1.change_type(new_direction)
        bird2.change_type(new_direction)
        bird3.change_type(new_direction) # kingBird 스프라이트 고치기
        bird4.change_type(new_direction)
    else:
        bird1.change_type('down')
        bird2.change_type('down')
        bird3.change_type('down')
        bird4.change_type('down')

    time = 0.0
    delay = min(max_delay, delay + delay_growth)

def draw():
    clear_canvas()

    game_world.render()
    bird1.draw(*bird1_pos, size[0] * ds[0], size[1] * ds[0])
    bird2.draw(*bird2_pos, size[0] * ds[1], size[1] * ds[1])
    bird3.draw(*bird3_pos, size[0] * ds[2], size[1] * ds[2])
    bird4.draw(*bird4_pos, size[0] * ds[3], size[1] * ds[3])
    choice_font.draw(choice_font_pos[0], choice_font_pos[1], 'Player 1', (255,0,0))
    choice_font.draw(choice_font_pos[2], choice_font_pos[3], 'Player 2', (0,255,0))

    update_canvas()

def finish():
    pass

def pause():
    pass
def resume():
    pass