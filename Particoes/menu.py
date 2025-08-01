import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas
from Particoes.loja import abrir_loja

def abrir_menu(screen, clock):
    window_width, window_height = screen.get_size()

    bolinhas_bg = [bolinhas() for _ in range(100)]

    background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background.fill(pygame.Color(255, 255, 255, 255))
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

    ticking = 60
    menu_aberto = True

    botao = pygame.transform.scale(pygame.image.load(f"Imagens/botao_jogar.png"), (600, 153))
    titulo = pygame.transform.scale(pygame.image.load(f"Imagens/titulo.png"), (1000, 500))

    # Define posição do botão
    botao_pos = (340, 400)
    botao_rect = pygame.Rect(botao_pos, (600, 153))  # (pos, tamanho)


    while menu_aberto:
        screen.blit(background, (0, 0))
        foreground.fill((0, 0, 0, 0))  # limpa a camada das bolinhas

        if ticking < 60:
            ticking += 1
        else:
            ticking = 0

        for i in range(100):
            if ticking == bolinhas_bg[i].tick:
                bolinhas_bg[i].acelerar()
            bolinhas_bg[i].deslocar(0)
            foreground.blit(bolinhas_bg[i].img, bolinhas_bg[i].pos)

        screen.blit(foreground, (0, 0))
        screen.blit(botao, botao_pos)
        screen.blit(titulo,(140, 0))


        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                menu_aberto = False

            # Clique do mouse
            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # botão esquerdo
                if botao_rect.collidepoint(event.pos):
                    menu_aberto = False
                    abrir_loja(screen, clock)

        pygame.display.update()
        clock.tick(60)