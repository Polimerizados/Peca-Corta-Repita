import pygame, sys, random, os
from pygame.locals import *
sys.path.append(os.path.abspath(".."))
from dez_e_dez import window_width, window_height, clock, screen

####### ESCOPO DA FASE #######
background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
background.fill(pygame.Color(240, 240, 240, 255))
midground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

ATP = (pygame.image.load("Imagens/ff_dATP.png"), "A")
CTP = (pygame.image.load("Imagens/ff_dCTP.png"), "C")
GTP = (pygame.image.load("Imagens/ff_dGTP.png"), "G")
TTP = (pygame.image.load("Imagens/ff_dTTP.png"), "T")
Ntps_possiveis = [ATP, CTP, GTP, TTP]
Ntp_x_size, Ntp_y_size = (80, 100) # resizing NTP(x, y) -> (80, 100)
Ntps = [pygame.transform.scale(Ntps_possiveis[random.randint(0, 3)][0], (80, 100)) for i in range(11)]

# Posições iniciais aleatórias = []
Ntps_x = []
Ntps_y = []
for NTP in Ntps:
    Ntp_x = random.randint(0, window_width)
    Ntp_y = random.randint(0, window_height-Ntp_y_size)
    Ntps_x.append(Ntp_x)
    Ntps_y.append(Ntp_y)
    midground.blit(NTP, (Ntp_x, Ntp_y))
Ntps_movs_x = [0] * 10 # Taxa de deslocamento inicialmente 0
Ntps_movs_y = [0] * 10 #  //  //      //          //      //

# Variáveis para o click
Ntp_clicado = 100 # número grande fora de qualquer index
diff_x = 0
diff_y = 0

# Fita
""" Meta """
# (0img, 1vel_arrasto_mouse, 2vel_poliemrizacao/scroll_da_fita, 3proofreading)
polimerase_sel = (pygame.image.load("Imagens/polimerase_teste.png"), 0, 10, 0) # Props. da pol. e do primer
# (0img, N/A, N/A, N/A)
primer_sel = (pygame.image.load("Imagens/primer_pareado_teste.png"), 0, 0, 0) # Óóóóóóóó, está pareado!!!
""" Meta """
polimerase_sel_img = pygame.transform.scale(polimerase_sel[0], (200, 280)) 
primer_sel_img = pygame.transform.scale(primer_sel[0], (500, 200))
Ntps_fita = [0] * 11
for i in range(11):
    r = random.randint(0, 3)
    Ntps_fita[i] = (pygame.transform.scale(Ntps_possiveis[r][0], (80, 100)), Ntps_possiveis[r][1])

########### WHILE ############
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
    # Atualiza as posições de tempo em tempo com velocidades aleatórias
    for i in range(10):
        if i != Ntp_clicado:
            if ticking == 0:
                Ntps_movs_x[i] = random.randint(-5, 5)
                Ntps_movs_y[i] = random.randint(-5, 5)
            Ntps_x[i] += Ntps_movs_x[i]
            Ntps_y [i] += Ntps_movs_y[i]
            midground.blit(Ntps[i], (Ntps_x[i], Ntps_y[i]))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Submete a posição da imagem à do mouse
    if Ntp_clicado != 100:
        Ntps_movs_x[Ntp_clicado] = 0
        Ntps_movs_y[Ntp_clicado] = 0
        Ntps_x[Ntp_clicado] = mouse_x + diff_x
        Ntps_y[Ntp_clicado] = mouse_y + diff_y
        midground.blit(Ntps[Ntp_clicado],
        (Ntps_x[Ntp_clicado], Ntps_y[Ntp_clicado]))

    ### FOREGROUND
    pygame.draw.rect(foreground, "aqua", ((0, window_height-100), (window_width, 40)))

    for i in range(11):
        foreground.blit(Ntps_fita[i][0], (160+100*i, window_height-150))

    foreground.blit(polimerase_sel_img, (-60, window_height-320))

    screen.blit(midground, (0, 0))
    screen.blit(foreground, (0, 0))
    
    # Muda Ntps_fita para o scrolamento
    # """if adsfsadf"""
    # """CONTABILIZOU O PONTO"""
    # """..."""
    # Ntps_fita.pop(0)
    # r = random.randint(0,3)
    # Ntps_fita.append(pygame.transform.scale(Ntps_possiveis[r][0], (80, 100)), Ntps_possiveis[r][1])

    for event in pygame.event.get():

        # Verifica se o mouse clicou numa hitbox das imagens
        if Ntp_clicado == 100:
            for Ntp_x, Ntp_y in zip(Ntps_x, Ntps_y):
                if event.type == MOUSEBUTTONDOWN:
                    if mouse_x in range(Ntp_x, Ntp_x+Ntp_x_size):
                        if mouse_y in range(Ntp_y, Ntp_y+Ntp_y_size):
                            diff_x = Ntp_x - mouse_x
                            diff_y = Ntp_y - mouse_y 
                            Ntp_clicado = Ntps_x.index(Ntp_x)
                            break

        # Retorna a movimentação da imagem
        else:
            if event.type == MOUSEBUTTONUP:
                    Ntps_movs_x[Ntp_clicado] = random.randint(-5, 5)
                    Ntps_movs_y[Ntp_clicado] = random.randint(-5, 5)
                    Ntp_clicado = 100
                    diff_x = 0
                    diff_y = 0

        # Se o usuário quiser sair, só, só
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    pygame.display.update()
    clock.tick(60)