import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas, PolimeraseSelect
import config
import math

def abrir_loja(screen, clock):
    window_width, window_height = screen.get_size()

    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    DOURADO = (220, 190, 90)
    VERMELHO = (255, 0, 0)
    fonte = pygame.font.Font("Fontes/gliker-regular.ttf", 32)
    moeda = pygame.transform.scale(pygame.image.load(f"Imagens/moeda.png"), (40, 50))
    erro_text = fonte.render(f"Polimerase inválida", True, VERMELHO)
    sem_dinheiro_text = fonte.render(f"Dinheiro Insuficiente", True, VERMELHO)
    erro = False
    sem_dinheiro = False

    componentes = {
        "polimerases": [
            {"nome": "Q5 High Fidelity", "tag": "q5", "custo": 1000, "desbloqueado": False},
            {"nome": "Taq Polimerase", "tag": "taq", "custo": 0, "desbloqueado": True},
            {"nome": "Phusion", "tag": "phusion", "custo": 0, "desbloqueado": True},
            {"nome": "Pfu Polimerase", "tag": "pfu", "custo": 500, "desbloqueado": False},
        ],
        "primers": [
            {"nome": "PrimerBank", "custo": 1500, "desbloqueado": False},
            {"nome": "Taq Primer", "custo": 0, "desbloqueado": True},
            {"nome": "SYBR Mix", "custo": 0, "desbloqueado": True},
        ]
    }

    bolinhas_bg = [bolinhas() for _ in range(100)]
    titulo = pygame.transform.scale(pygame.image.load(f"Imagens/titulo_loja.png"), (1000, 125))
    botao_voltar = pygame.transform.scale(pygame.image.load(f"Imagens/botao_voltar.png"), (210, 75))
    voltar_rect = pygame.Rect((50, window_height - 120), (210, 75))
    botao_seguinte = pygame.transform.scale(pygame.image.load(f"Imagens/botao_seguinte.png"), (210, 75))
    seguinte_rect = pygame.Rect((window_width - 270, window_height - 120), (210, 75))
    setas = {
        "esq_poli": pygame.Rect(300, 267.5, 50, 50),
        "dir_poli": pygame.Rect(930, 267.5, 50, 50),
    }
    polimerases = [
        PolimeraseSelect(640, 400, 200, pos_inicial=0, dicionario=componentes["polimerases"][3], img="pfu_polimerase_select"),
        PolimeraseSelect(640, 400, 200, pos_inicial=1, dicionario=componentes["polimerases"][2], img="phusion_polimerase_select"),
        PolimeraseSelect(640, 400, 200, pos_inicial=2, dicionario=componentes["polimerases"][1], img="taq_polimerase_select"), 
        PolimeraseSelect(640, 400, 200, pos_inicial=3, dicionario=componentes["polimerases"][0], img="q5_polimerase_select"), 


    ]

    def checar_giro():
        for item in polimerases:
            if item.direcao != 0:
                return False
        return True

    loja_ativa = True
    ticking = 60
    selecao_final = {}

    while loja_ativa:
        screen.fill(BRANCO)

        if ticking < 60:
            ticking += 1
        else:
            ticking = 0

        try:
            with open("pontuacao.txt", "r") as f:
                nucleotideos = int(f.read())
        except:
            nucleotideos = 500

        for i in range(100):
            if ticking == bolinhas_bg[i].tick:
                bolinhas_bg[i].acelerar()
            bolinhas_bg[i].deslocar(0)
            screen.blit(bolinhas_bg[i].img, bolinhas_bg[i].pos)

        screen.blit(titulo, (window_width//2 - titulo.get_width()//2, 40))

        moeda_text = fonte.render(f"{nucleotideos}", True, DOURADO)
        screen.blit(moeda, (1210, 20))  
        screen.blit(moeda_text, (1200-moeda_text.get_width(), 25))

        if erro:
            screen.blit(erro_text, (window_width/2 - erro_text.get_width(), window_height/2 + 50))
        if sem_dinheiro:
             screen.blit(sem_dinheiro_text, (window_width/2 - erro_text.get_width(), window_height/2 + 50))

        for nome, seta in setas.items():
            if "esq" in nome:
                pygame.draw.polygon(screen, PRETO, [
                    (seta.x + 40, seta.y + 5),
                    (seta.x + 10, seta.y + 25),
                    (seta.x + 40, seta.y + 45)
                ])
            else:
                pygame.draw.polygon(screen, PRETO, [
                    (seta.x + 10, seta.y + 5),
                    (seta.x + 40, seta.y + 25),
                    (seta.x + 10, seta.y + 45)
                ])


        # Atualizar polimerases
        for item in polimerases:
            item.update()

        polimerases_ordenadas = sorted(polimerases, key=lambda x: x.scale)
        for item in polimerases_ordenadas:
            item.draw(screen)
        
        selecionada = polimerases_ordenadas[-1]

        screen.blit(botao_voltar, (50, window_height - 120))
        screen.blit(botao_seguinte, (window_width - 270, window_height - 120))
        if selecionada.desbloqueado:
            texto_polimerase = fonte.render(f"{selecionada.nome}", True, PRETO)
            screen.blit(texto_polimerase, (window_width/2 - texto_polimerase.get_width()/2, window_height/2))
        else:
            texto_bloqueada = fonte.render(f"BLOQUEADA", True, PRETO)
            screen.blit(texto_bloqueada, (window_width/2 - texto_bloqueada.get_width()/2, window_height/2))
 

        for event in pygame.event.get():

            if event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                erro = False
                sem_dinheiro = False

                if setas["esq_poli"].collidepoint(mx, my):
                    for item in polimerases:
                        item.girar_esquerda()
                if setas["dir_poli"].collidepoint(mx, my):
                    for item in polimerases:
                        item.girar_direita()

                if pygame.Rect(547.5, 200, 185, 185).collidepoint(mx, my):
                    if not selecionada.desbloqueado:
                        if not selecionada.comprar():
                            sem_dinheiro = True


                if voltar_rect.collidepoint(mx, my):
                    loja_ativa = False
                    from Particoes.menu import abrir_menu
                    abrir_menu(screen, clock)
                    return None

                if seguinte_rect.collidepoint(mx, my):
                    config.polimerase_selecionada = selecionada.tag
                    if selecionada.desbloqueado:
                        loja_ativa = False
                        from Particoes.dificuldades import abrir_dificuldades
                        abrir_dificuldades(screen, clock)
                    else:
                        erro = True
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    loja_ativa = False
                    from Particoes.menu import abrir_menu
                    abrir_menu(screen, clock)
                if event.key == K_RIGHT:
                    if checar_giro():
                        for item in polimerases:
                            item.girar_direita()
                elif event.key == K_LEFT:
                    if checar_giro():
                        for item in polimerases:
                            item.girar_esquerda()

            if event.type == QUIT:  # usuário clicou no X
                loja_ativa = False
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

    return selecao_final
