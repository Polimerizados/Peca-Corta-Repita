import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas, Botao
from Particoes.fases import rodar_fase
from Particoes.musica import tocar_musica
from config import resource_path


def abrir_dificuldades(screen, clock):
    window_width, window_height = screen.get_size()

    background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background.fill(pygame.Color(255, 255, 255, 255))
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

    # Carregando Assets
    bolinhas_bg = [bolinhas() for _ in range(100)]
    fonte = pygame.font.Font(resource_path("Fontes/gliker-regular.ttf"), 93)
    titulo = fonte.render("Selecione a dificuldade", True, (0, 0, 0))
    titulo_pos = ((window_width-titulo.get_width())/2, 170-titulo.get_height())

    # Botões
    facil = Botao((360, 371), (65, 235), "botao_facil", fator_hover=1.111, texto="Fácil", nome_fonte=resource_path("Fontes/gliker-regular.ttf"), tamanho_fonte=58, ancora_texto=(0.5, 0.94))
    medio = Botao((360, 371), (462, 235), "botao_medio", fator_hover=1.111, texto="Médio", nome_fonte=resource_path("Fontes/gliker-regular.ttf"), tamanho_fonte=58, ancora_texto=(0.5, 0.94))
    dificil = Botao((360, 371), (856, 235), "botao_dificil", fator_hover=1.111, texto="Difícil", nome_fonte=resource_path("Fontes/gliker-regular.ttf"), tamanho_fonte=58, ancora_texto=(0.5, 0.94))
    voltar = Botao((210, 75), (50, 680), cor=(244, 244, 244), fator_hover=1.185, texto="Voltar", nome_fonte=resource_path("Fontes/gliker-regular.ttf"), tamanho_fonte=33, borda=5)

    # Música
    if not pygame.mixer.music.get_busy():
        tocar_musica(resource_path("musicas/macacos_me_mordam.wav"))

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
        facil.desenhar(screen)
        medio.desenhar(screen)
        dificil.desenhar(screen)
        voltar.desenhar(screen)
        screen.blit(titulo, titulo_pos)

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
