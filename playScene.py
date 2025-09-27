import pygame
from pico2d import *
from bird import Bird
from map import Map

def enter():
    global bg, bird, birdPos
    bg = Map()
    bird = Bird(bg)
    birdPos = bird.getPos()

def exit():
    pass

def update():
    bird.handle_event(get_events())
    pass

def draw():
    bg.draw()
    bird.draw()

def handle_events():
    pass