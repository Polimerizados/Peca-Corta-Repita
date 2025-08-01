import pygame, sys, random, os
from pygame.locals import *
sys.path.append(os.path.abspath(".."))
from Particoes.utils import salvar_pontuacao, carregar_pontuacao
sys.path.append(os.path.abspath("Particoes"))
from classes import dNTP, ligH, dP, bolinhas
from config import window_width, window_height, screen, clock

def rodar_fase(dificuldade, screen, clock):
    ####### ESCOPO DA FASE #######
    background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background.fill(pygame.Color(240, 240, 240, 255))
    midground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)


    # Spawn temporário de 12 bases:
    dNTPs_livres = [dNTP(dificuldade, "down") for _ in range(12)]
    diff_x = 0
    diff_y = 0

    #Bolinhas background
    bolinhas_bg = [bolinhas() for _ in range(100)]

    ### Fita
    """ Meta """
    polimerase_sel = (pygame.image.load("Imagens/polimerase_teste.png"), 0, 0, 0)
    primer_sel = (pygame.image.load("Imagens/primer_pareado_teste.png"), 0, 0, 0)
    """ Meta """
    polimerase_sel_img = pygame.transform.scale(polimerase_sel[0], (200, 280)) 
    primer_sel_img = pygame.transform.scale(primer_sel[0], (500, 200))
    nucleotideos_fita = [dNTP(dificuldade, "up", "random", (160+100*i, window_height-190)) for i in range(12)]
    dP_fita = [dP(dificuldade, nucleotideos_fita[i].tipo, "up") for i in range(12)]
    dP_contra_fita = [0] * 12
    contra_fita = [0] * 12
    lista_ligH = [0] * 12
    if dificuldade == "m" or "d":
        primeiro_par = pygame.transform.scale(pygame.image.load(f"Imagens/primeiro_par_f{dificuldade}.png"), (100, 270))


    ########### WHILE ############
    clicado_index = ""
    ticking = 60
    running = True

    # REMOVER DEPOIS - APENAS PARA TESTES #
    pygame.font.init()
    pontuacao_global = carregar_pontuacao()
    fonte = pygame.font.SysFont("Segoe UI", 48)
    # REMOVER DEPOIS - APENAS PARA TESTES #

    while running:
        # Para diferenciar passagens de tempo
        if ticking < 60:
            ticking += 1
        else:
            ticking = 0

        # Redesenha o background puro
        screen.blit(background, (0, 0))
        midground.fill((0, 0, 0, 0))

        for i in range(100):
            if ticking == bolinhas_bg[i].tick:
                bolinhas_bg[i].acelerar()
            bolinhas_bg[i].deslocar()
            midground.blit(bolinhas_bg[i].img, bolinhas_bg[i].pos)

        # REMOVER DEPOIS - APENAS PARA TESTES
        texto_amino = fonte.render(f"pnts: {pontuacao_global}", True, (0, 0, 0))
        screen.blit(texto_amino, (20, 20))
        # REMOVER DEPOIS - APENAS PARA TESTES #

        ### FOREGROUND
        if dificuldade == "f":
            pygame.draw.rect(foreground, "aqua", ((0, window_height-120), (window_width, 40)))
            pygame.draw.rect(foreground, "aqua", ((0, window_height-230), (160, 40)))

        for i in range(12):
            if dificuldade == "f":
                foreground.blit(nucleotideos_fita[i].img, (160+100*i, window_height-160))
            if dificuldade == "m" or "d":
                foreground.blit(nucleotideos_fita[i].img, (160+100*i, window_height-190))
                foreground.blit(dP_fita[i].img, (160+100*i, window_height-110))
                
            if contra_fita[i] == 0:
                continue
            if dificuldade == "f":
                pygame.draw.rect(foreground, "aqua", ((160+100*i, window_height-230), (120, 40)))
            foreground.blit(contra_fita[i].img, (160+100*i, window_height-240))
            if dificuldade == "m" or "d":
                foreground.blit(dP_contra_fita[i].img, (160+100*i, window_height-300))
                if nucleotideos_fita[i].base_par == contra_fita[i].base:
                    foreground.blit(lista_ligH[i].img, (160+100*i, window_height-240))

        ### MIDGROUND
        # Atualiza as posições de tempo em tempo, sob o mouse ou aleatoriamente
        for i in range(12):
            if i == clicado_index:
                dNTPs_livres[clicado_index].pos = tuple(a - b for a, b in zip(pygame.mouse.get_pos(), (diff_x, diff_y)))
            else:
                # Força a volta das bases que saírem da tela
                if ticking == dNTPs_livres[i].tick:
                    dNTPs_livres[i].acelerar()
                dNTPs_livres[i].deslocar()
            midground.blit(dNTPs_livres[i].img, dNTPs_livres[i].pos)

        screen.blit(midground, (0, 0))

        if dificuldade == "m" or "d":
            foreground.blit(primeiro_par, (60, window_height-300))
        foreground.blit(polimerase_sel_img, (-60, window_height-320))

        screen.blit(foreground, (0, 0))

        ### EVENTOS
        for event in pygame.event.get():

            # Identifica se se clicou em uma dNTP livre
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in range(12):
                    dNTP_x, dNTP_y = dNTPs_livres[i].pos
                    (diff_x, diff_y) = (mouse_x - dNTP_x, mouse_y - dNTP_y)
                    if 80 >= diff_x >= 0 and 100 >= diff_y >= 0:  
                        clicado_index = i
                        break

            # Identifica quando se solta a dNTP, se a liberta, se em cima da fita
            if event.type == MOUSEBUTTONUP:
                diff_x = -1
                diff_y = -1
                if isinstance(clicado_index, int):   
                    pareante = nucleotideos_fita[contra_fita.index(0)] 
                    if pygame.mouse.get_pos()[0] in range(pareante.pos[0], pareante.pos[0]+80):
                        if pygame.mouse.get_pos()[1] in range(pareante.pos[1]-80, pareante.pos[1]+100):
                            contra_fita[contra_fita.index(0)] = dNTP(
                                dificuldade,
                                "down",
                                dNTPs_livres[clicado_index].base,
                                (dNTPs_livres[clicado_index].pos[0],window_height-240)
                            )
                            lista_ligH[lista_ligH.index(0)] = ligH(
                                nucleotideos_fita[lista_ligH.index(0)].base,
                                contra_fita[lista_ligH.index(0)].base
                            )
                            if dificuldade == "m" or "d":
                                dP_contra_fita[dP_contra_fita.index(0)] = dP(
                                    dificuldade, 
                                    dNTPs_livres[clicado_index].tipo,
                                    "down"
                                )
                            dNTPs_livres.pop(clicado_index)
                            dNTPs_livres.append(dNTP(dificuldade, "down"))
                            pontuacao_global += 1
                            salvar_pontuacao(pontuacao_global)
                clicado_index = ""

            # Se o usuário quiser sair, só, só
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    from Particoes.dificuldades import abrir_dificuldades
                    abrir_dificuldades(screen, clock)

        pygame.display.update()
        clock.tick(60)