import pygame, sys, random, os
from pygame.locals import *
from dez_e_dez import window_width, window_height, clock, screen

class dNTP:
    def __init__(self, level, up_down, base="random", pos="random"):
        self.level = level

        self.up_down = up_down

        if base == "random":
            if level == "f":
                bases = ["A", "T", "C", "G"]
            self.base = random.choice(bases)
        else:
            self.base = base

        if self.base == "A":
            self.base_par = "T"
        if self.base == "T":
            self.base_par = "A"
        if self.base == "C":
            self.base_par = "G"
        if self.base == "G":
            self.base_par = "C"
    
        self.img = pygame.transform.scale(pygame.image.load(f"Imagens/f{level}_d{self.base}TP_{self.up_down}.png"), (80, 100)) 

        if pos == "random":
            self.pos = (random.randint(0, window_width-80), random.randint(0, window_height-100))
        else:
            self.pos = pos

        self.tick = random.randint(0, 59)

        self.vel = (random.randint(-5, 5), random.randint(-5, 5))

    def acelerar(self):
        if self.pos[0] < 0:
            self.vel = (random.randint(1, 5), random.randint(-5, 5))                
        elif self.pos[0] > window_width:
            self.vel = (random.randint(-5, -1), random.randint(-5, 5))
        elif self.pos[1] < 0:
            self.vel = (random.randint(-5, 5), random.randint(1, 5))
        elif self.pos[1] > window_height:
            self.vel = (random.randint(-5, 5), random.randint(-5, -1))
        else:
            self.vel = (random.randint(-5, 5), random.randint(-5, 5))

    def deslocar(self):
        self.pos = tuple(a + b for a, b in zip(self.pos, self.vel))

# class polimerase:
# (0img, 1vel_arrasto_mouse, 2vel_poliemrizacao/scroll_da_fita, 3proofreading)