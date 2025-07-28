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
dificuldade = "f"

# Spawn temporário de 12 bases:
dNTPs_livres = [dNTP(dificuldade, "down") for _ in range(12)]
diff_x = 0
diff_y = 0

### Fita
""" Meta """
polimerase_sel = (pygame.image.load("Imagens/polimerase_teste.png"), 0, 0, 0)
primer_sel = (pygame.image.load("Imagens/primer_pareado_teste.png"), 0, 0, 0)
""" Meta """
polimerase_sel_img = pygame.transform.scale(polimerase_sel[0], (200, 280)) 
primer_sel_img = pygame.transform.scale(primer_sel[0], (500, 200))
nucleotideos_fita = [dNTP(dificuldade, "up", "random", (160+100*i, window_height-150)) for i in range(12)]
contra_fita = [0] * 12
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
            if ticking == dNTPs_livres[i].tick:
                dNTPs_livres[i].acelerar()
            dNTPs_livres[i].deslocar()
        midground.blit(dNTPs_livres[i].img, dNTPs_livres[i].pos)

    screen.blit(midground, (0, 0))

    ### FOREGROUND
    pygame.draw.rect(foreground, "aqua", ((0, window_height-110), (window_width, 40)))
    pygame.draw.rect(foreground, "aqua", ((0, window_height-230), (160, 40)))
    for i in range(12):
        foreground.blit(nucleotideos_fita[i].img, (160+100*i, window_height-160))
        if contra_fita[i] == 0:
            continue
        pygame.draw.rect(foreground, "aqua", ((160+100*i, window_height-230), (100, 40)))
        foreground.blit(contra_fita[i].img, (160+100*i, window_height-240))

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
                if pygame.mouse.get_pos()[0] in range(pareante.pos[0]-80, pareante.pos[0]+100):
                    if pygame.mouse.get_pos()[1] in range(pareante.pos[1], pareante.pos[1]+80):
                        contra_fita[contra_fita.index(0)] = dNTP(
                            dificuldade,
                            "down",
                            dNTPs_livres[clicado_index].base,
                            (dNTPs_livres[clicado_index].pos[0],window_height-240)
                        )
                        dNTPs_livres.pop(clicado_index)
                        dNTPs_livres.append(dNTP(dificuldade, "down"))
            clicado_index = ""

        # Se o usuário quiser sair, só, só
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    pygame.display.update()
    clock.tick(60)