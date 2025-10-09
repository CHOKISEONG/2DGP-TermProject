import pygame
from pico2d import *
from black_bird import BlackBird
from hat_bird import HatBird
from map import Map
from musicManager import Music

def enter():
    global bg, player1, player2, music
    music = Music('sound/120bpm_mainScene.mp3', 120)
    music.play(repeat=True)
    bg = Map()
    player1 = BlackBird(bg)
    player2 = HatBird(bg)
    player2.move(13)

def exit():
    pass

def update():
    events = pico2d.get_events()
    player1.handle_event(events)
    player2.handle_event(events)

def draw():
    bg.draw()
    player1.draw()
    player2.draw()

def handle_events():

    pass