import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas, Botao
from Particoes.fases import rodar_fase

def abrir_dificuldades(screen, clock):
    window_width, window_height = screen.get_size()

    background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background.fill(pygame.Color(255, 255, 255, 255))
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

    # Carregando Assets
    bolinhas_bg = [bolinhas() for _ in range(100)]
    titulo = pygame.image.load(f"Imagens/titulo_dificuldade.png")

    # Botões
    facil = Botao((360, 371), (400, 412), (65, 235), (45, 215), "botao_facil")
    medio = Botao((360, 371), (400, 412), (462, 235), (442, 215), "botao_medio")
    dificil = Botao((360, 371), (400, 412), (856, 235), (836, 215), "botao_dificil")
    voltar = Botao((210, 75), (250, 89), (50, 680), (30,673), "botao_voltar")


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
        facil.draw(screen)
        medio.draw(screen)
        dificil.draw(screen)
        voltar.draw(screen)
        screen.blit(titulo,(140, 50))

        ## EVENTOS
        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_ESCAPE: # Esc
                menu_aberto = False
                from Particoes.menu import abrir_menu
                abrir_menu(screen, clock)

            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Clique com botão esquerdo
                if facil.rect.collidepoint(event.pos): # Fácil
                    menu_aberto = False
                    rodar_fase("f", screen, clock)

                if medio.rect.collidepoint(event.pos): # Médio
                    menu_aberto = False
                    rodar_fase("m", screen, clock)

                if dificil.rect.collidepoint(event.pos): # Difícil
                    menu_aberto = False
                    rodar_fase("d", screen, clock)

                if voltar.rect.collidepoint(event.pos): # Voltar
                    menu_aberto = False
                    from Particoes.menu import abrir_menu
                    abrir_menu(screen, clock)

        pygame.display.update()
        clock.tick(60)