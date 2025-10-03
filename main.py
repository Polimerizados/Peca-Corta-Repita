import pygame, sys, random, os
from pygame.locals import *
from pygame import mixer
from config import window_width, window_height, screen, clock
from Particoes.menu import abrir_menu
from musica import tocar_musica

pygame.display.set_caption("pspspspspspspsps")

background = pygame.Surface((window_width, window_height)) 
main_menu = pygame.Surface((window_width, window_height))
background.fill(pygame.Color(255, 255, 255))
main_menu.fill(pygame.Color(0, 255, 0))
main_menu.set_alpha(50)

########### Pontos Globais ############

def salvar_pontuacao(pontos):
    with open("pontuacao.txt", "w") as f:
        f.write(str(pontos))

def carregar_pontuacao():
    if os.path.exists("pontuacao.txt"):
        with open("pontuacao.txt", "r") as f:
            return int(f.read())
    return 0


########### MÚSICA ############

tocar_musica("Particoes/macacos_me_mordam.wav")

########### WHILE ############
while True: 
    
    screen.blit(background, (0, 0))
    screen.blit(main_menu, (0, 0))

    for event in pygame.event.get():
        if event.type == KEYDOWN: # Teclado 

            if event.key == K_ESCAPE: # Esc
                pygame.quit()
                sys.exit()

            if event.key == K_SPACE: # Espaço
                abrir_menu(screen, clock)
                            
    pygame.display.update()
    clock.tick(60)
