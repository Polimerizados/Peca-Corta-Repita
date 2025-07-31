import pygame, sys, random, os
from pygame.locals import *
from config import window_width, window_height, screen, clock
from Particoes.loja import abrir_loja
from Particoes.fases import rodar_fase

pygame.display.set_caption("pspspspspspspsps")

background = pygame.Surface((window_width, window_height)) 
main_menu = pygame.Surface((window_width, window_height))
screen.fill(pygame.Color(0, 0, 0))
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
                dificuldade = "f"
                rodar_fase(dificuldade, screen, clock)

            if event.key == K_s:
                selecao = abrir_loja(screen, clock)  # Passe a tela e clock para loja
                if selecao:
                    print("Escolha do usuário:")
                    print("Polimerase:", selecao["polimerase"]["nome"])
                    print("Primer:", selecao["primer"]["nome"])
                     
    pygame.display.update() 

    clock.tick(60)
