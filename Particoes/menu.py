import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas, Botao
from Particoes.loja import abrir_loja
from Particoes.opcoes import abrir_opcoes

def abrir_menu(screen, clock):
    window_width, window_height = screen.get_size()

    # Background
    bolinhas_bg = [bolinhas() for _ in range(100)]

    background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background.fill(pygame.Color(255, 255, 255, 255))
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

    # Título
    titulo = pygame.image.load(f"Imagens/titulo.png")

    ## BOTÕES
    tamanho_botoes = (400, 110)
    tamanho_hover = (477, 143)

    botao_jogar = Botao(tamanho_botoes, tamanho_hover, (440, 356), (400, 341), "botao_jogar")
    botao_opcoes = Botao(tamanho_botoes, tamanho_hover, (440, 493), (400, 478), "botao_opcoes")
    botao_leaderboard = Botao(tamanho_botoes, tamanho_hover, (440, 630), (400, 614), "botao_leaderboard") 

    ###### TEMPORÁRIO ######
    mini_font = pygame.font.Font("Fontes/gliker-regular.ttf", 25)
    opção_indispoivel = mini_font.render(f"Opção indisponível", True, (255, 0, 0))

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
        botao_jogar.draw(screen)
        botao_opcoes.draw(screen)
        botao_leaderboard.draw(screen)
        screen.blit(titulo,(0, 0))
        
        ###### TEMPORÁRIO ######
        try:
            if erro:
                screen.blit(opção_indispoivel, (890, 673))
        except:
            erro = False

        ## EVENTOS
        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_ESCAPE: # Esc
                menu_aberto = False

            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Clique com botão esquerdo
                if botao_jogar.rect.collidepoint(event.pos): # Botão de jogar
                    menu_aberto = False
                    abrir_loja(screen, clock)
                if botao_opcoes.rect.collidepoint(event.pos): # Botão de opções
                    menu_aberto = False
                    abrir_opcoes(screen, clock)
                if botao_leaderboard.rect.collidepoint(event.pos): # Botão de leaderboard
                    ###### TEMPORÁRIO ######
                    erro = True
                    

        pygame.display.update()
        clock.tick(60)