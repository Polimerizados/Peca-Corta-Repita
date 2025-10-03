import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas, PolimeraseSelect, Botao
import config
import math

def abrir_loja(screen, clock):
    window_width, window_height = screen.get_size()

    # Cores
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    DOURADO = (220, 190, 90)
    VERMELHO = (255, 0, 0)

    # Carregando recursos
    bolinhas_bg = [bolinhas() for _ in range(100)]
    titulo = pygame.image.load(f"Imagens/titulo_loja.png")
    fonte = pygame.font.Font("Fontes/gliker-regular.ttf", 32)
    moeda = pygame.image.load(f"Imagens/moeda.png")
    erro_text = fonte.render(f"Polimerase inválida", True, VERMELHO)
    dinheiro_insuficiente_text = fonte.render(f"Dinheiro Insuficiente", True, VERMELHO)

    # Botões
    botao_voltar = Botao((210, 75), (250, 89), (50, 680), (30,673), "botao_voltar")
    botao_seguinte = Botao((210, 75), (250, 89), (1010, 680), (990,673), "botao_seguinte")
    setas = {
        "esq_poli": pygame.Rect(300, 267.5, 50, 50),
        "dir_poli": pygame.Rect(930, 267.5, 50, 50),
    }

    # Polimerases
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
    polimerases = [
        PolimeraseSelect(640, 400, 200, pos_inicial=0, dicionario=componentes["polimerases"][3], img="pfu_polimerase_select"),
        PolimeraseSelect(640, 400, 200, pos_inicial=1, dicionario=componentes["polimerases"][2], img="phusion_polimerase_select"),
        PolimeraseSelect(640, 400, 200, pos_inicial=2, dicionario=componentes["polimerases"][1], img="taq_polimerase_select"), 
        PolimeraseSelect(640, 400, 200, pos_inicial=3, dicionario=componentes["polimerases"][0], img="q5_polimerase_select"), 
    ]

    def checar_giro():
        """Retorna True se todas as polimerases estiverem paradas"""
        for item in polimerases:
            if item.direcao != 0:
                return False
        return True

    ########### WHILE ############
    erro = False
    dinheiro_insuficiente = False
    loja_ativa = True
    ticking = 60

    while loja_ativa:
        # Para diferenciar passagens de tempo
        if ticking < 60:
            ticking += 1
        else:
            ticking = 0

        # Carrega pontuação
        try:
            with open("pontuacao.txt", "r") as f:
                nucleotideos = int(f.read())
        except:
            nucleotideos = 500

        # Limpa camadas
        screen.fill(BRANCO)
        
        # Desenha bolinhas
        for i in range(100):
            if ticking == bolinhas_bg[i].tick:
                bolinhas_bg[i].acelerar()
            bolinhas_bg[i].deslocar(0)
            screen.blit(bolinhas_bg[i].img, bolinhas_bg[i].pos)

        # Desenha título, pontuação e botões
        screen.blit(titulo, (window_width//2 - titulo.get_width()//2, 40))

        moeda_text = fonte.render(f"{nucleotideos}", True, DOURADO)
        screen.blit(moeda, (1210, 20))  
        screen.blit(moeda_text, (1200-moeda_text.get_width(), 25))

        botao_voltar.draw(screen)
        botao_seguinte.draw(screen)

        # Mensagem de erro
        if erro:
            screen.blit(erro_text, (window_width/2 - erro_text.get_width(), window_height/2 + 50))
        if dinheiro_insuficiente:
             screen.blit(dinheiro_insuficiente_text, (window_width/2 - erro_text.get_width(), window_height/2 + 50))

        # Desenha setas
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


        # Atualiza e desenha polimerases e nomes
        for item in polimerases:
            item.update()
        polimerases_ordenadas = sorted(polimerases, key=lambda x: x.scale)
        for item in polimerases_ordenadas:
            item.draw(screen)
        selecionada = polimerases_ordenadas[-1]

        if selecionada.desbloqueado:
            texto_polimerase = fonte.render(f"{selecionada.nome}", True, PRETO)
            screen.blit(texto_polimerase, (window_width/2 - texto_polimerase.get_width()/2, window_height/2))
        else:
            texto_bloqueada = fonte.render(f"BLOQUEADA", True, PRETO)
            screen.blit(texto_bloqueada, (window_width/2 - texto_bloqueada.get_width()/2, window_height/2))
 

        ### EVENTOS
        for event in pygame.event.get():

            if event.type == MOUSEBUTTONDOWN: # Clique com botão esquerdo

                # Reseta mensagens de erro
                erro = False
                dinheiro_insuficiente = False

                mx, my = pygame.mouse.get_pos()
                if setas["esq_poli"].collidepoint(mx, my): # Seta esquerda
                    if checar_giro():
                        for item in polimerases:
                            item.girar_esquerda()
                if setas["dir_poli"].collidepoint(mx, my): # Seta direita
                    if checar_giro():
                        for item in polimerases:
                            item.girar_direita()

                if pygame.Rect(547.5, 200, 185, 185).collidepoint(mx, my): # Polimerase central
                    if not selecionada.desbloqueado:
                        if not selecionada.comprar():
                            dinheiro_insuficiente = True


                if botao_voltar.rect.collidepoint(mx, my): # Botão voltar
                    loja_ativa = False
                    from Particoes.menu import abrir_menu
                    abrir_menu(screen, clock)
                    return None

                if botao_seguinte.rect.collidepoint(mx, my): # Botão seguinte
                    config.polimerase_selecionada = selecionada.tag
                    if selecionada.desbloqueado:
                        loja_ativa = False
                        from Particoes.dificuldades import abrir_dificuldades
                        abrir_dificuldades(screen, clock)
                    else:
                        erro = True
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Esc
                    loja_ativa = False
                    from Particoes.menu import abrir_menu
                    abrir_menu(screen, clock)
                if event.key == K_RIGHT: # Setinha direita
                    if checar_giro():
                        for item in polimerases:
                            item.girar_direita()
                elif event.key == K_LEFT: # Setinha esquerda
                    if checar_giro():
                        for item in polimerases:
                            item.girar_esquerda()

        pygame.display.update()
        clock.tick(60)

    return selecionada
