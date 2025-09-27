import pygame
from pico2d import *
from bird import Bird
from map import Map
from musicManager import Music

def enter():
    global bg, bird, birdPos, music
    music = Music('sound/90bpm_mainScene.mp3')
    music.play(repeat=True)
    bg = Map()
    bird = Bird(bg)
    birdPos = bird.getPos()

def exit():
    pass

def update():
    bird.handle_event(get_events())

def draw():
    bg.draw()
    bird.draw()

def handle_events():
    pass