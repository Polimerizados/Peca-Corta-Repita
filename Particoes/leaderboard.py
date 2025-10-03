import pygame, sys, itertools
from pygame.locals import *
from Particoes.classes import bolinhas, Botao
from Particoes.loja import abrir_loja
from Particoes.opcoes import abrir_opcoes
import config

def abrir_classificacao(screen, clock):
    window_width, window_height = screen.get_size()

    # Background
    bolinhas_bg = [bolinhas() for _ in range(100)]

    background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background.fill(pygame.Color(255, 255, 255, 255))
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

    # Imagem
    leaderboard = pygame.image.load(f"Imagens/leaderboard.png")

    # Botão
    botao_voltar = Botao((210, 75), (250, 89), (50, 680), (30,673), "botao_voltar")

    # Tratamento dos dados
    def tratar_dados(lista_dados):
        dados_tratados = sorted(lista_dados, key = lambda x: x["pontuação"], reverse=True)
        dados_tratados = dados_tratados[:5]
        return dados_tratados
    
    config.lista_dados_f = tratar_dados(config.lista_dados_f)
    config.lista_dados_m = tratar_dados(config.lista_dados_m)
    config.lista_dados_d = tratar_dados(config.lista_dados_d)

    # Importar a fonte
    fonte = pygame.font.Font("Fontes/gliker-regular.ttf", 50)

    # Transformar dados em texto
    def converter_dados(lista_dados):
        textos = []
        contador = itertools.count(start=1)
        for dado in lista_dados:
            string = f"{next(contador)}. {dado["nome"]} - {dado["pontuação"]}"
            texto = fonte.render(string, True, (0, 0, 0))
            textos.append(texto)
        return textos

    textos_f = converter_dados(config.lista_dados_f)
    textos_m = converter_dados(config.lista_dados_m)
    textos_d = converter_dados(config.lista_dados_d)

    # Função desenhar textos
    def desenhar_textos(surface, lista_textos, pos_x, pos_y):
        contador = itertools.count(start=0)
        for texto in lista_textos:
            surface.blit(texto, (pos_x, pos_y + 65*(next(contador))))

    ########### WHILE ############
    ticking = 60
    classificacao_aberta = True

    while classificacao_aberta:
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

        # Desenha grounds, leaderboardo, botão e textos
        screen.blit(background, (0, 0))
        screen.blit(foreground, (0, 0))
        screen.blit(leaderboard,(0, 0))
        botao_voltar.draw(screen)
        desenhar_textos(screen, textos_f, 63, 280)
        desenhar_textos(screen, textos_m, 476, 280)
        desenhar_textos(screen, textos_d, 889, 280)

        ## EVENTOS
        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_ESCAPE: # Esc
                classificacao_aberta = False
                from Particoes.menu import abrir_menu
                abrir_menu(screen, clock)

            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Clique com botão esquerdo
                if botao_voltar.rect.collidepoint(event.pos): # Botão de jogar
                    classificacao_aberta = False
                    from Particoes.menu import abrir_menu
                    abrir_menu(screen, clock)

                    

        pygame.display.update()
        clock.tick(60)