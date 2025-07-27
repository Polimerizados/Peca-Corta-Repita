import pygame, sys, random, os
from pygame.locals import *
from dez_e_dez import window_width, window_height, clock, screen

class dNTP:
    def __init__(self, level, base="random", pos="random"):
        self.level = level

        if base == "random":
            if level == "f":
                bases = ["A", "T", "C", "G"]
            self.base = random.choice(bases)
        else:
            self.base = base
    
        self.img = pygame.transform.scale(pygame.image.load(f"Imagens/f{level}_d{self.base}TP.png"), (80, 100)) 

        if pos == "random":
            self.pos = (random.randint(0, window_width-80), random.randint(0, window_height-100))
        else:
            self.pos = pos

# class polimerase:
# (0img, 1vel_arrasto_mouse, 2vel_poliemrizacao/scroll_da_fita, 3proofreading)