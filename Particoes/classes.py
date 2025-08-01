import pygame, sys, random, os
from pygame.locals import *
from config import window_width, window_height

class dNTP:
    def __init__(self, level, up_down, base="random", pos="random"):
        self.level = level

        self.up_down = up_down

        if base == "random":
            if level == "f" or level == "m" or level == "d":
                bases = ["A", "T", "C", "G"]
            self.base = random.choice(bases)
        else:
            self.base = base

        if self.base == "A":
            self.base_par = "T"
            self.tipo = "purica"
        if self.base == "T":
            self.base_par = "A"
            self.tipo = "pirimidica"
        if self.base == "C":
            self.base_par = "G"
            self.tipo = "pirimidica"
        if self.base == "G":
            self.base_par = "C"
            self.tipo = "purica"
    
        if level == "m" or level == "d":
            self.img = pygame.transform.scale(pygame.image.load(f"Imagens/f{level}_d{self.base}TP_{self.up_down}.png"), (100, 100)) 
        elif level == "f":
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

class ligH:
    def __init__(self, base, base_par):
        self.base = base
        self.base_par = base_par
        if self.base == "A" and self.base_par == "T":
            self.img = pygame.transform.scale(pygame.image.load(f"Imagens/ligH_AT.png"), (100, 150)) 
        elif self.base == "T" and self.base_par == "A":
            self.img = pygame.transform.scale(pygame.image.load(f"Imagens/ligH_TA.png"), (100, 150)) 
        elif self.base == "C" and self.base_par == "G":
            self.img = pygame.transform.scale(pygame.image.load(f"Imagens/ligH_CG.png"), (100, 150)) 
        elif self.base == "G" and self.base_par == "C":
            self.img = pygame.transform.scale(pygame.image.load(f"Imagens/ligH_GC.png"), (100, 150))
        
class dP:
    def __init__(self, level, tipo="purica", up_down="up"):
        self.level = level
        self.tipo = tipo
        if level == "m" or level == "d":
            self.img = pygame.transform.scale(pygame.image.load(f"Imagens/f{level}_dP_{tipo}_{up_down}.png"), (100, 80)) 

class bolinhas:
    def __init__(self):

        self.pos = (random.randint(0, window_width-80), random.randint(0, window_height-100))
        self.tick = random.randint(0, 59)
        self.vel = (random.randint(-5, 5), random.randint(-5, 5))
        self.img = pygame.transform.scale(pygame.image.load(f"Imagens/bolinha.png"), (10, 10)) 

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