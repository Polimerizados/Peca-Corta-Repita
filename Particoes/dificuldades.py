import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas
from Particoes.fases import rodar_fase

def abrir_dificuldades(screen, clock):
    window_width, window_height = screen.get_size()

    bolinhas_bg = [bolinhas() for _ in range(100)]

    background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background.fill(pygame.Color(255, 255, 255, 255))
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

    ticking = 60
    menu_aberto = True

    facil = pygame.transform.scale(pygame.image.load(f"Imagens/botao_facil.png"), (600, 153))
    medio = pygame.transform.scale(pygame.image.load(f"Imagens/botao_medio.png"), (600, 153))
    dificil = pygame.transform.scale(pygame.image.load(f"Imagens/botao_dificil.png"), (600, 153))
    voltar = pygame.transform.scale(pygame.image.load(f"Imagens/botao_voltar.png"), (210, 75))
    titulo = pygame.transform.scale(pygame.image.load(f"Imagens/titulo_dificuldade.png"), (1000, 125))


    facil_rect = pygame.Rect((340, 225), (600, 153))
    medio_rect = pygame.Rect((340, 398), (600, 153))
    dificil_rect = pygame.Rect((340, 571), (600, 153))
    voltar_rect = pygame.Rect((50, window_height - 120), (210, 75))

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
        screen.blit(facil, (340, 225))
        screen.blit(medio, (340, 398))
        screen.blit(dificil, (340, 571))
        screen.blit(voltar, (50, window_height - 120))
        screen.blit(titulo,(140, 50))


        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                menu_aberto = False
                from Particoes.loja import abrir_loja
                abrir_loja(screen, clock)

            # Clique do mouse
            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # botão esquerdo
                if facil_rect.collidepoint(event.pos):
                    menu_aberto = False
                    rodar_fase("f", screen, clock)

                if medio_rect.collidepoint(event.pos):
                    menu_aberto = False
                    rodar_fase("m", screen, clock)

                if dificil_rect.collidepoint(event.pos):
                    menu_aberto = False
                    rodar_fase("d", screen, clock)

                if voltar_rect.collidepoint(event.pos):
                    menu_aberto = False
                    from Particoes.loja import abrir_loja
                    abrir_loja(screen, clock)

        pygame.display.update()
        clock.tick(60)