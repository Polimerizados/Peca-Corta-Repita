import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas

def abrir_loja(screen, clock):
    window_width, window_height = screen.get_size()

    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    CINZA = (200, 200, 200)
    LARANJA = (255, 140, 0)
    VERDE = (50, 200, 50)
    VERMELHO = (200, 50, 50)
    fonte = pygame.font.SysFont("Segoe UI", 32)

    try:
        with open("pontuacao.txt", "r") as f:
            nucleotideos = int(f.read())
    except:
        nucleotideos = 500

    def salvar_pontuacao(pontos):
        with open("pontuacao.txt", "w") as f:
            f.write(str(pontos))

    componentes = {
        "polimerases": [
            {"nome": "Q5 High-Fidelity", "custo": 1000, "desbloqueado": False},
            {"nome": "Taq DNA Polimerase", "custo": 0, "desbloqueado": True},
            {"nome": "Phusion", "custo": 0, "desbloqueado": True},
        ],
        "primers": [
            {"nome": "PrimerBank", "custo": 1500, "desbloqueado": False},
            {"nome": "Taq Primer", "custo": 0, "desbloqueado": True},
            {"nome": "SYBR Mix", "custo": 0, "desbloqueado": True},
        ]
    }

    selecionado = {"polimerase": 1, "primer": 1}

    bolinhas_bg = [bolinhas() for _ in range(100)]
    titulo = pygame.transform.scale(pygame.image.load(f"Imagens/titulo_loja.png"), (1000, 125))
    botao_voltar = pygame.transform.scale(pygame.image.load(f"Imagens/botao_voltar.png"), (210, 75))
    voltar_rect = pygame.Rect((50, window_height - 120), (210, 75))
    botao_seguinte = pygame.transform.scale(pygame.image.load(f"Imagens/botao_seguinte.png"), (210, 75))
    seguinte_rect = pygame.Rect((window_width - 270, window_height - 120), (210, 75))
    setas = {
        "esq_poli": pygame.Rect(100, 200, 50, 50),
        "dir_poli": pygame.Rect(500, 200, 50, 50),
        "esq_primer": pygame.Rect(100, 400, 50, 50),
        "dir_primer": pygame.Rect(500, 400, 50, 50),
    }

    def desenhar_item(item, pos):
        cor = VERDE if item["desbloqueado"] else CINZA
        ret = pygame.Rect(pos[0], pos[1], 200, 100)
        pygame.draw.rect(screen, cor, ret, border_radius=10)
        nome = fonte.render(item["nome"], True, PRETO)
        screen.blit(nome, (pos[0] + (200 - nome.get_width()) // 2, pos[1] + 30))
        if not item["desbloqueado"]:
            cadeado = fonte.render(f"{item['custo']} nt", True, VERMELHO)
            screen.blit(cadeado, (pos[0]+10, pos[1]+60))
        return ret

    loja_ativa = True
    ticking = 60
    selecao_final = {}

    while loja_ativa:
        screen.fill(BRANCO)

        if ticking < 60:
            ticking += 1
        else:
            ticking = 0

        for i in range(100):
            if ticking == bolinhas_bg[i].tick:
                bolinhas_bg[i].acelerar()
            bolinhas_bg[i].deslocar(0)
            screen.blit(bolinhas_bg[i].img, bolinhas_bg[i].pos)

        screen.blit(titulo, (window_width//2 - titulo.get_width()//2, 40))

        moeda = fonte.render(f"{nucleotideos} Nucleotídeos", True, LARANJA)
        screen.blit(moeda, (window_width - moeda.get_width() - 30, 20))

        pol = componentes["polimerases"][selecionado["polimerase"]]
        screen.blit(fonte.render("DNA Polimerase", True, PRETO), (200, 160))
        desenhar_item(pol, (200, 200))

        primer = componentes["primers"][selecionado["primer"]]
        screen.blit(fonte.render("Primer", True, PRETO), (200, 360))
        desenhar_item(primer, (200, 400))

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


        screen.blit(botao_voltar, (50, window_height - 120))
        screen.blit(botao_seguinte, (window_width - 270, window_height - 120))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if setas["esq_poli"].collidepoint(mx, my):
                    selecionado["polimerase"] = max(0, selecionado["polimerase"] - 1)
                if setas["dir_poli"].collidepoint(mx, my):
                    selecionado["polimerase"] = min(len(componentes["polimerases"]) - 1, selecionado["polimerase"] + 1)
                if setas["esq_primer"].collidepoint(mx, my):
                    selecionado["primer"] = max(0, selecionado["primer"] - 1)
                if setas["dir_primer"].collidepoint(mx, my):
                    selecionado["primer"] = min(len(componentes["primers"]) - 1, selecionado["primer"] + 1)

                if pygame.Rect(200, 200, 200, 100).collidepoint(mx, my):
                    item = componentes["polimerases"][selecionado["polimerase"]]
                    if not item["desbloqueado"] and nucleotideos >= item["custo"]:
                        item["desbloqueado"] = True
                        nucleotideos -= item["custo"]
                        salvar_pontuacao(nucleotideos)

                if pygame.Rect(200, 400, 200, 100).collidepoint(mx, my):
                    item = componentes["primers"][selecionado["primer"]]
                    if not item["desbloqueado"] and nucleotideos >= item["custo"]:
                        item["desbloqueado"] = True
                        nucleotideos -= item["custo"]
                        salvar_pontuacao(nucleotideos)

                if voltar_rect.collidepoint(mx, my):
                    loja_ativa = False
                    from Particoes.menu import abrir_menu
                    abrir_menu(screen, clock)
                    return None

                if seguinte_rect.collidepoint(mx, my):
                    selecao_final = {
                        "polimerase": componentes["polimerases"][selecionado["polimerase"]],
                        "primer": componentes["primers"][selecionado["primer"]],
                    }
                    loja_ativa = False
                    from Particoes.dificuldades import abrir_dificuldades
                    abrir_dificuldades(screen, clock)
            
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                loja_ativa = False
                from Particoes.menu import abrir_menu
                abrir_menu(screen, clock)

        pygame.display.update()
        clock.tick(60)

    return selecao_final
