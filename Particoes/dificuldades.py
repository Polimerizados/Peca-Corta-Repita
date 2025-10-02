import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas
from Particoes.fases import rodar_fase

def abrir_dificuldades(screen, clock):
    window_width, window_height = screen.get_size()

    background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background.fill(pygame.Color(255, 255, 255, 255))
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

    # Carregando Assets
    bolinhas_bg = [bolinhas() for _ in range(100)]

    facil = pygame.image.load(f"Imagens/botao_facil.png")
    medio = pygame.image.load(f"Imagens/botao_medio.png")
    dificil = pygame.image.load(f"Imagens/botao_dificil.png")
    voltar = pygame.image.load(f"Imagens/botao_voltar.png")
    titulo = pygame.image.load(f"Imagens/titulo_dificuldade.png")

    # Rects dos botões
    facil_rect = pygame.Rect((65, 235), (360, 371))
    medio_rect = pygame.Rect((462, 235), (360, 371))
    dificil_rect = pygame.Rect((856, 235), (360, 371))
    voltar_rect = pygame.Rect((50, window_height - 120), (210, 75))

    ########### WHILE ############
    ticking = 60
    menu_aberto = True

    while menu_aberto:
        # Para diferenciar passagens de tempo
        if ticking < 60:
            ticking += 1
        else:
            ticking = 0

        # Limpa as camadas
        foreground.fill((0, 0, 0, 0))  

        # Desenha as bolinhas
        for i in range(100):
            if ticking == bolinhas_bg[i].tick:
                bolinhas_bg[i].acelerar()
            bolinhas_bg[i].deslocar(0)
            foreground.blit(bolinhas_bg[i].img, bolinhas_bg[i].pos)

        # Desenha os grounds, botões e título
        screen.blit(background, (0, 0))
        screen.blit(foreground, (0, 0))
        screen.blit(facil, (65, 235))
        screen.blit(medio, (462, 235))
        screen.blit(dificil, (856, 235))
        screen.blit(voltar, (50, window_height - 120))
        screen.blit(titulo,(140, 50))

        ## EVENTOS
        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_ESCAPE: # Esc
                menu_aberto = False
                from Particoes.loja import abrir_loja
                abrir_loja(screen, clock)

            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Clique com botão esquerdo
                if facil_rect.collidepoint(event.pos): # Fácil
                    menu_aberto = False
                    rodar_fase("f", screen, clock)

                if medio_rect.collidepoint(event.pos): # Médio
                    menu_aberto = False
                    rodar_fase("m", screen, clock)

                if dificil_rect.collidepoint(event.pos): # Difícil
                    menu_aberto = False
                    rodar_fase("d", screen, clock)

                if voltar_rect.collidepoint(event.pos): # Voltar
                    menu_aberto = False
                    from Particoes.loja import abrir_loja
                    abrir_loja(screen, clock)

        pygame.display.update()
        clock.tick(60)