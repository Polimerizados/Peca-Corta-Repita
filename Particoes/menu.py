import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas, Botao
from Particoes.dificuldades import abrir_dificuldades
from Particoes.opcoes import abrir_opcoes
from Particoes.musica import tocar_musica, som_hover
from config import resource_path

def abrir_menu(screen, clock):
    window_width, window_height = screen.get_size()

    # Background
    bolinhas_bg = [bolinhas() for _ in range(100)]

    background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background.fill(pygame.Color(255, 255, 255, 255))
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

    # Título
    titulo = pygame.image.load(resource_path(f"Imagens/titulo.png"))
    fonte = pygame.font.Font(resource_path("Fontes/gliker-regular.ttf"), 95)
    texto_titulo = fonte.render("Pesque, Conecte e Repita", True, (0, 0, 0))
    texto_pos = ((window_width-texto_titulo.get_width())/2, 200-texto_titulo.get_height())

    ## BOTÕES
    tamanho_botoes = (400, 110)
    tamanho_hover = (477, 143)

    CINZA = (244, 244, 244)
    botao_jogar = Botao(tamanho_botoes, (440, 356), cor=CINZA, fator_hover=1.185, texto="Jogar", nome_fonte=resource_path("Fontes/gliker-regular.ttf"), tamanho_fonte=58, borda=6)
    botao_opcoes = Botao(tamanho_botoes, (440, 493), cor=CINZA, fator_hover=1.185, texto="Opções", nome_fonte=resource_path("Fontes/gliker-regular.ttf"), tamanho_fonte=58, borda=6)
    botao_leaderboard = Botao(tamanho_botoes, (440, 630), cor=CINZA, fator_hover=1.185, texto="Leaderboard", nome_fonte=resource_path("Fontes/gliker-regular.ttf"), tamanho_fonte=58, borda=6)

    # Música
    if not pygame.mixer.music.get_busy():
        tocar_musica(resource_path("musicas/macacos_me_mordam.wav"))

    ########### WHILE ############
    ticking = 60
    menu_aberto = True

    while menu_aberto:
        # Para diferenciar a passagem do tempo
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

        # Desenha grounds, título e botões
        screen.blit(background, (0, 0))
        screen.blit(foreground, (0, 0))
        botao_jogar.desenhar(screen)
        botao_opcoes.desenhar(screen)
        botao_leaderboard.desenhar(screen)
        screen.blit(titulo,(0, 0))
        screen.blit(texto_titulo, texto_pos)

        ## EVENTOS
        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_ESCAPE: # Esc
                menu_aberto = False

            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Clique com botão esquerdo
                if botao_jogar.rect.collidepoint(event.pos): # Botão de jogar
                    menu_aberto = False
                    abrir_dificuldades(screen, clock)
                if botao_opcoes.rect.collidepoint(event.pos): # Botão de opções
                    menu_aberto = False
                    abrir_opcoes(screen, clock)
                if botao_leaderboard.rect.collidepoint(event.pos): # Botão de leaderboard
                    menu_aberto = False
                    from Particoes.leaderboard import abrir_classificacao
                    abrir_classificacao(screen, clock)

        pygame.display.update()
        clock.tick(60)

    screen.fill((255, 255, 255, 255))