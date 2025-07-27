import pygame, sys, random, os
from pygame.locals import *
sys.path.append(os.path.abspath(".."))
from dez_e_dez import window_width, window_height, clock, screen
sys.path.append(os.path.abspath("Particoes"))
from classes import dNTP

####### ESCOPO DA FASE #######
background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
background.fill(pygame.Color(240, 240, 240, 255))
midground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

# Spawn temporário de 11 bases:
dNTPs_livres = [dNTP("f") for _ in range(12)]
dNTPs_livres_desl = [0] * 12

### Fita
""" Meta """
polimerase_sel = (pygame.image.load("Imagens/polimerase_teste.png"), 0, 0, 0)
primer_sel = (pygame.image.load("Imagens/primer_pareado_teste.png"), 0, 0, 0)
""" Meta """
polimerase_sel_img = pygame.transform.scale(polimerase_sel[0], (200, 280)) 
primer_sel_img = pygame.transform.scale(primer_sel[0], (500, 200))
dNTPs_fita = [dNTP("f", "random", (160+100*i, window_height-150)) for i in range(12)]

########### WHILE ############
clicado_index = ""
ticking = 60
running = True

while running:
    # Para diferenciar passagens de tempo
    if ticking < 60:
        ticking += 1
    else:
        ticking = 0

    # Redesenha o background puro
    screen.blit(background, (0, 0))
    midground.fill((0, 0, 0, 0))

    ### MIDGROUND
    # Atualiza as posições de tempo em tempo, sob o mouse ou aleatoriamente
    for i in range(12):
        if i == clicado_index:
            dNTPs_livres[clicado_index].pos = tuple(a - b for a, b in zip(pygame.mouse.get_pos(), (diff_x, diff_y)))
        else:
            # Força a volta das bases que saírem da tela
            if ticking == 0:
                if dNTPs_livres[i].pos[0] < 0:
                       dNTPs_livres_desl[i] = (random.randint(1, 5), random.randint(-5, 5))                 
                elif dNTPs_livres[i].pos[0] > window_width:
                    dNTPs_livres_desl[i] = (random.randint(-5, -1), random.randint(-5, 5))
                elif dNTPs_livres[i].pos[1] < 0:
                    dNTPs_livres_desl[i] = (random.randint(-5, 5), random.randint(1, 5))
                elif dNTPs_livres[i].pos[1] > window_height:
                    dNTPs_livres_desl[i] = (random.randint(-5, 5), random.randint(-5, -1))
                else:
                    dNTPs_livres_desl[i] = (random.randint(-5, 5), random.randint(-5, 5))
            dNTPs_livres[i].pos = tuple(a + b for a, b in zip(dNTPs_livres[i].pos, dNTPs_livres_desl[i]))
        midground.blit(dNTPs_livres[i].img, dNTPs_livres[i].pos)

    ### FOREGROUND
    pygame.draw.rect(foreground, "aqua", ((0, window_height-100), (window_width, 40)))

    for i in range(12):
        foreground.blit(dNTPs_fita[i].img, (160+100*i, window_height-150))

    foreground.blit(polimerase_sel_img, (-60, window_height-320))

    screen.blit(midground, (0, 0))
    screen.blit(foreground, (0, 0))

    for event in pygame.event.get():

        # Identifica se se clicou em uma dNTP livre
        if event.type == MOUSEBUTTONDOWN or clicado_index is int:
            mouse_x, mouse_y = pygame.mouse.get_pos() 
            for i in range(12):
                dNTP_x, dNTP_y = dNTPs_livres[i].pos
                (diff_x, diff_y) = (mouse_x - dNTP_x, mouse_y - dNTP_y)
                if 80 >= diff_x >= 0 and 100 >= diff_y >= 0:  
                    clicado_index = i
                    break
        if event.type == MOUSEBUTTONUP:
            clicado_index = ""

        # Se o usuário quiser sair, só, só
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    pygame.display.update()
    clock.tick(60)