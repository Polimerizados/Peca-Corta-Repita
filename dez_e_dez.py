
# 
#
#
#
#
# APERTE ESPAÇO DUAS VEZES PARA INICIAR DENTRO DA EXECUÇÃO
#
#
#
#
#


import pygame, sys, random
from pygame.locals import *

######## ESCOPO GERAL ########
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("pspspspspspspsps")

window_width = int(pygame.display.Info().current_w) # 1280
window_height = int(pygame.display.Info().current_h) # 800
screen = pygame.display.set_mode((window_width, window_height))
background = pygame.Surface((window_width, window_height)) 
main_menu = pygame.Surface((window_width, window_height))
screen.fill(pygame.Color(0, 0, 0))
background.fill(pygame.Color(255, 255, 255))
main_menu.fill(pygame.Color(0, 255, 0)) 
main_menu.set_alpha(50)

########### WHILE ############
while True:

    screen.blit(background, (0, 0))
    screen.blit(main_menu, (0, 0))

    for event in pygame.event.get():
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == K_SPACE:  
                with open("Particoes/fases.py") as fases:
                    exec(fases.read())

            if event.key == K_l:
                with open("Particoes/loja.py") as loja:
                    exec(loja.read())
                     
    pygame.display.update() 

    clock.tick(60)