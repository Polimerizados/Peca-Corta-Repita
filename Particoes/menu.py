import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas
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

    # Jogar
    botao_jogar = pygame.image.load(f"Imagens/botao_jogar.png")
    botao_jogar_pos = (440, 356)
    botao_jogar_rect = pygame.Rect(botao_jogar_pos, tamanho_botoes) 
    botao_j_rect = botao_jogar_rect # Inicialmente pequeno
    
    # Opções
    botao_opcoes = pygame.image.load(f"Imagens/botao_opcoes.png")
    botao_opcoes_pos = (440, 493)
    botao_opcoes_rect = pygame.Rect(botao_opcoes_pos, tamanho_botoes)  
    botao_o_rect = botao_opcoes_rect # Inicialmente pequeno

    # Leaderboard
    botao_leaderboard = pygame.image.load(f"Imagens/botao_leaderboard.png")
    botao_leaderboard_pos = (440, 630)
    botao_leaderboard_rect = pygame.Rect(botao_leaderboard_pos, tamanho_botoes)  
    botao_l_rect = botao_leaderboard_rect # Inicialmente pequeno 

    # Jogar (Hover)
    botao_jogar_h = pygame.image.load(f"Imagens/botao_jogar_hover.png")
    botao_jogar_pos_h = (400, 341)
    botao_jogar_rect_h = pygame.Rect(botao_jogar_pos_h, tamanho_hover)  

    # Opções (Hover)
    botao_opcoes_h = pygame.image.load(f"Imagens/botao_opcoes_hover.png")
    botao_opcoes_pos_h = (400, 478)
    botao_opcoes_rect_h = pygame.Rect(botao_opcoes_pos_h, tamanho_hover)  

    # Leaderboard (Hover)
    botao_leaderboard_h = pygame.image.load(f"Imagens/botao_leaderboard_hover.png")
    botao_leaderboard_pos_h = (400, 614)
    botao_leaderboard_rect_h = pygame.Rect(botao_leaderboard_pos_h, tamanho_hover)

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


        # --- LÓGICA DE HOVER ---
        mouse_pos = pygame.mouse.get_pos()

        # Jogar
        hovering_j = botao_j_rect.collidepoint(mouse_pos)
        if hovering_j:
            botao_j  = botao_jogar_h 
            botao_j_pos = botao_jogar_pos_h 
            botao_j_rect = botao_jogar_rect_h
        else:
            botao_j  = botao_jogar 
            botao_j_pos = botao_jogar_pos
            botao_j_rect = botao_jogar_rect

        # Opções
        hovering_o = botao_o_rect.collidepoint(mouse_pos)
        if hovering_o:
            botao_o  = botao_opcoes_h 
            botao_o_pos = botao_opcoes_pos_h 
            botao_o_rect = botao_opcoes_rect_h
        else:
            botao_o  = botao_opcoes
            botao_o_pos = botao_opcoes_pos
            botao_o_rect = botao_opcoes_rect

        # Leaderboard
        hovering_l = botao_l_rect.collidepoint(mouse_pos)
        if hovering_l:
            botao_l  = botao_leaderboard_h 
            botao_l_pos = botao_leaderboard_pos_h 
            botao_l_rect = botao_leaderboard_rect_h
        else:
            botao_l  = botao_leaderboard
            botao_l_pos = botao_leaderboard_pos
            botao_l_rect = botao_leaderboard_rect
            ###### TEMPORÁRIO ######
            erro = False

        # Desenha grounds, título e botões
        screen.blit(background, (0, 0))
        screen.blit(foreground, (0, 0))
        screen.blit(botao_j, botao_j_pos)
        screen.blit(botao_o, botao_o_pos)
        screen.blit(botao_l, botao_l_pos)
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
                if botao_j_rect.collidepoint(event.pos): # Botão de jogar
                    menu_aberto = False
                    abrir_loja(screen, clock)
                if botao_o_rect.collidepoint(event.pos): # Botão de opções
                    menu_aberto = False
                    abrir_opcoes(screen, clock)
                if botao_l_rect.collidepoint(event.pos): # Botão de leaderboard
                    ###### TEMPORÁRIO ######
                    erro = True
                    

        pygame.display.update()
        clock.tick(60)