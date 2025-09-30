import pygame, sys, random, os
from pygame.locals import *
sys.path.append(os.path.abspath(".."))
from Particoes.utils import salvar_pontuacao, carregar_pontuacao
sys.path.append(os.path.abspath("Particoes"))
from classes import dNTP, ligH, dP, bolinhas, polimerase
from config import window_width, window_height, screen, clock
import config

def rodar_fase(dificuldade, screen, clock):
    ####### ESCOPO DA FASE #######
    background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background.fill(pygame.Color(240, 240, 240, 255))
    midground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    cleaner = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    cleaner.fill(pygame.Color(255, 255, 255, 255))

    # Spawn temporário de 12 bases:
    dNTPs_livres = [dNTP(dificuldade, "down") for _ in range(24)]
    diff_x = 0
    diff_y = 0

    #Bolinhas background
    bolinhas_bg = [bolinhas() for _ in range(100)]

    ### Fita
    inicio_x_fita = 0
    polimerase_selecionada = config.polimerase_selecionada
    pol = polimerase(polimerase_selecionada, dificuldade)
    nucleotideos_fita = [dNTP(dificuldade, "up", "random", (100*i, window_height-190)) for i in range(14)]
    dP_contra_fita = [0] * 14
    contra_fita = [0] * 14
    lista_ligH = [0] * 14
    for i in range(14):
        if 100 * i < 550:
            contra_fita[i] = dNTP(dificuldade, "down", nucleotideos_fita[i].base_par, (inicio_x_fita+100*i, window_height-240))
            if dificuldade == "m" or dificuldade == "d":
                dP_contra_fita[i] = dP(dificuldade, contra_fita[i].tipo, "down")
                lista_ligH[i] = ligH(nucleotideos_fita[i].base, nucleotideos_fita[i].base_par)
    if dificuldade == "m" or dificuldade == "d":
        dP_fita = [dP(dificuldade, nucleotideos_fita[i].tipo, "up") for i in range(14)]

    # Botão de Pause
    botao_pause = pygame.image.load(f"Imagens/pause_botao.png")
    pause_rect = pygame.Rect((1197, 35), (40, 50))

    # Pontuação
    pygame.font.init()
    pontuacao_global = carregar_pontuacao()
    fonte = pygame.font.Font("Fontes/gliker-regular.ttf", 48)
    moeda = pygame.image.load(f"Imagens/moeda.png")

    ########### WHILE ############
    clicado_index = ""
    ticking = 60
    pula_tick = pol.se_multiplo # Com a polimerase teste, será 1 pixel por 2 ticks
    scroll_vel = 0
    scroll_ticks = 1
    scroll_ticks_max = 0
    qnt_ticks_max = 0
    qnt_scrolls = 0
    running = True


    while running:
        # Para diferenciar passagens de tempo
        if ticking < 60:
            ticking += 1
        else:
            ticking = 0

        # "Animação" paralela do scrolling
        if scroll_vel != 0:
            if qnt_ticks_max > 0:
                if scroll_ticks == scroll_ticks_max:
                    qnt_scrolls += 1
                    scroll_ticks = 1
                    qnt_ticks_max += -1
                    nucleotideos_fita.pop(0)
                    nucleotideos_fita.append(dNTP(dificuldade, "up", "random", (100*13, window_height-190)))
                    contra_fita.pop(0)
                    contra_fita.append(0)
                    if dificuldade == "m" or dificuldade == "d":
                        dP_fita.pop(0)
                        dP_fita.append(dP(dificuldade, nucleotideos_fita[13].tipo, "up"))
                        dP_contra_fita.pop(0)
                        dP_contra_fita.append(0)
                        lista_ligH.pop(0)
                        lista_ligH.append(0)
            else:
                scroll_vel = 0
                scroll_ticks = 1
                scroll_ticks_max = 0
            scroll_ticks += 1
            if pula_tick == True:
                inicio_x_fita += scroll_vel
            pula_tick = not pula_tick

        # Limpa os grounds
        background.blit(cleaner, (0, 0))
        background.fill((240, 240, 240))
        midground.fill((0, 0, 0, 0))
        foreground.fill((0, 0, 0, 0))

        ### BACKGROUND
        for i in range(100):
            if bolinhas_bg[i].pos[0] < -11:
                bolinhas_bg[i] = bolinhas()
            if ticking == bolinhas_bg[i].tick:
                bolinhas_bg[i].acelerar()
            bolinhas_bg[i].deslocar(scroll_vel)
            background.blit(bolinhas_bg[i].img, bolinhas_bg[i].pos)

        ### MIDGROUND
        # Atualiza as posições de tempo em tempo, sob o mouse ou aleatoriamente
        for i in range(24):
            if i == clicado_index:
                dNTPs_livres[clicado_index].pos = tuple(a - b for a, b in zip(pygame.mouse.get_pos(), (diff_x, diff_y)))
            else:
                # Força a volta das bases que saírem da tela
                if ticking == dNTPs_livres[i].tick:
                    dNTPs_livres[i].acelerar()
                dNTPs_livres[i].deslocar(scroll_vel)
            midground.blit(dNTPs_livres[i].img, dNTPs_livres[i].pos)

        ### FOREGROUND
        if dificuldade == "f":
            pygame.draw.rect(foreground, "aqua", ((0, window_height-120), (window_width, 40)))

        for i in range(14):
            if dificuldade == "f":
                nucleotideos_fita[i].pos = (inicio_x_fita+100*(i+qnt_scrolls), window_height-170)
                foreground.blit(nucleotideos_fita[i].img, nucleotideos_fita[i].pos)
            if dificuldade == "m" or dificuldade == "d":
                nucleotideos_fita[i].pos = (inicio_x_fita+100*(i+qnt_scrolls), window_height-190)
                foreground.blit(nucleotideos_fita[i].img, nucleotideos_fita[i].pos)
                foreground.blit(dP_fita[i].img, (inicio_x_fita+100*(i+qnt_scrolls), window_height-110))
            if contra_fita[i] == 0:
                continue
            if dificuldade == "f":
                pygame.draw.rect(foreground, "aqua", ((inicio_x_fita+100*(i+qnt_scrolls), window_height-235), (120, 40)))
                foreground.blit(contra_fita[i].img, (inicio_x_fita+100*(i+qnt_scrolls), window_height-245))
            if dificuldade == "m" or dificuldade == "d":
                foreground.blit(contra_fita[i].img, (inicio_x_fita+100*(i+qnt_scrolls), window_height-240))
                foreground.blit(dP_contra_fita[i].img, (inicio_x_fita+100*(i+qnt_scrolls), window_height-300))
                if nucleotideos_fita[i].base_par == contra_fita[i].base:
                    foreground.blit(lista_ligH[i].img, (inicio_x_fita+100*(i+qnt_scrolls), window_height-240))

        # Desenha os grounds, polimerase, botões e pontuação
        screen.blit(background, (0, 0))
        screen.blit(midground, (0, 0))
        screen.blit(foreground, (0, 0))
        pygame.Surface.set_alpha(pol.img, 100)
        screen.blit(pol.img, (550, window_height-320))
        screen.blit(botao_pause, (1197, 35))
        texto_amino = fonte.render(f"{pontuacao_global}", True, (220, 190, 90))
        screen.blit(moeda, (40 + texto_amino.get_width(), 25))
        screen.blit(texto_amino, (30, 20))

        ### EVENTOS
        for event in pygame.event.get():
            
            if event.type == MOUSEBUTTONDOWN: # Clique
                # Identifica se clicou em uma dNTP livre
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in range(24):
                    dNTP_x, dNTP_y = dNTPs_livres[i].pos
                    (diff_x, diff_y) = (mouse_x - dNTP_x, mouse_y - dNTP_y)
                    if 80 >= diff_x >= 0 and 100 >= diff_y >= 0:  
                        clicado_index = i
                        break
                # Identifica se clicou no botão de pause
                if pause_rect.collidepoint(event.pos):
                    from Particoes.pause import pausar
                    running = pausar(screen, clock)
                    if not running:
                        from Particoes.menu import abrir_menu
                        abrir_menu(screen, clock)

            # Identifica quando se solta a dNTP, se a liberta, se em cima da fita
            if event.type == MOUSEBUTTONUP:
                diff_x = -1
                diff_y = -1
                if isinstance(clicado_index, int):   
                    pareante = nucleotideos_fita[contra_fita.index(0)]
                    if pareante.base_par == dNTPs_livres[clicado_index].base:
                        if pygame.mouse.get_pos()[0] in range(550, 750) and pareante.pos[0] in range(550, 715): # Se está dentro da polimerase
                            if pygame.mouse.get_pos()[1] in range(window_height-320, window_height-20):
                                contra_fita[contra_fita.index(0)] = dNTP(
                                    dificuldade,
                                    "down",
                                    dNTPs_livres[clicado_index].base,
                                    (pareante.pos[0], window_height-240)
                                )
                                if dificuldade == "m" or dificuldade == "d":
                                    lista_ligH[lista_ligH.index(0)] = ligH(
                                        pareante.base,
                                        pareante.base_par
                                    )
                                    dP_contra_fita[dP_contra_fita.index(0)] = dP(
                                        dificuldade, 
                                        dNTPs_livres[clicado_index].tipo,
                                        "down"
                                    )
                                dNTPs_livres.pop(clicado_index)
                                dNTPs_livres.append(dNTP(dificuldade, "down"))
                                scroll_ticks_max = pol.scrolling_ticks
                                scroll_vel = pol.scrolling
                                qnt_ticks_max += 1
                                pareante = 0
                                pontuacao_global += 1
                                salvar_pontuacao(pontuacao_global)
                clicado_index = ""


            if event.type == KEYDOWN: # Teclado
                if event.key == K_ESCAPE: # Esc
                    running = False
                    from Particoes.dificuldades import abrir_dificuldades
                    abrir_dificuldades(screen, clock)
                if event.key == K_p: # P (pause)
                    from Particoes.pause import pausar
                    running = pausar(screen, clock)
                    if not running:
                        from Particoes.menu import abrir_menu
                        abrir_menu(screen, clock)


        pygame.display.update()
        clock.tick(60)