import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas, Botao, Slider
import config


def abrir_opcoes(screen, clock):
    window_width, window_height = screen.get_size()

    # Cores
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    RED = (255, 0, 0)

    # Background
    bolinhas_bg = [bolinhas() for _ in range(100)]

    screen.fill(pygame.Color(255, 255, 255, 0))
    background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background.fill(pygame.Color(255, 255, 255, 0))
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    foreground.fill(pygame.Color(255, 255, 255, 0))

    menu_opcoes = pygame.image.load(f"Imagens/menu_opcoes.png")

    # Botão de voltar
    botao_voltar = Botao((210, 75), (50, 680), cor=(244,244,244), fator_hover=1.185, texto="Voltar", nome_fonte="Fontes/gliker-regular.ttf", tamanho_fonte=33, borda=5)

    # Slider da musica
    slider_musica = Slider((460, 268), 520, 20, value_offset=30, initial_val=config.volume_m, color=GRAY, fill_color=BLACK, show_value=True, font_name="Fontes/gliker-regular.ttf", font_size=55)

    # Slider do som
    slider_som = Slider((460, 363), 520, 20, value_offset=30, initial_val=config.volume_s, color=GRAY, fill_color=BLACK, show_value=True, font_name="Fontes/gliker-regular.ttf", font_size=55)

    ## CHECK BOX
    check_box = pygame.image.load(f"Imagens/check_opcoes.png")

    # Rect botão de música e som
    rect_musica = pygame.Rect((365, 243), (66, 66))
    rect_som = pygame.Rect((365, 339), (66, 66))

    # Pause da música
    musica_pausou = False

    # Fonte
    try:
        font = pygame.font.Font("Fontes/gliker-regular.ttf", 55)
        mini_font = pygame.font.Font("Fontes/gliker-regular.ttf", 35)
    except:
        font = pygame.font.SysFont("arial", 55, bold=True)
        mini_font = pygame.font.SysFont("arial", 35, bold=True)

    # Idioma
    menu_opcoes_idioma = pygame.image.load(f"Imagens/menu_opcoes_idioma.png")
    rect_idioma = pygame.Rect((365, 428), (363, 76))
    rect_portugues = pygame.Rect((365, 504), (363, 65))
    rect_ingles = pygame.Rect((365, 568), (363, 65))
    rect_espanhol = pygame.Rect((365, 634), (363, 65))
    idioma_indispoivel = mini_font.render(f"Idioma indisponível", True, RED)
    selecionando_idioma = False

    ########### WHILE ############

    ticking = 60
    opcoes_aberto = True

    while opcoes_aberto:
        # Para diferenciar a passagem do tempo
        if ticking < 60:
            ticking += 1
        else:
            ticking = 0
        

        # Limpa as camadas
        background.fill((255, 255, 255, 255))  
        foreground.fill((255, 255, 255, 0))  

        # Desenha as bolinhas
        for i in range(100):
            if ticking == bolinhas_bg[i].tick:
                bolinhas_bg[i].acelerar()
            bolinhas_bg[i].deslocar(0)
            background.blit(bolinhas_bg[i].img, bolinhas_bg[i].pos)

        # Desenha menu
        if selecionando_idioma:
            foreground.blit(menu_opcoes_idioma, (0, 0))
        else:
            foreground.blit(menu_opcoes, (0, 0))

        # Idioma
        texto_idioma = font.render(config.idioma, True, BLACK)
        foreground.blit(texto_idioma, (375, 427)) 
        if config.idioma != "Português":
            foreground.blit(idioma_indispoivel, (750, 445)) 

        # Check box
        if config.musica_on:
            foreground.blit(check_box, (365, 243))
            if musica_pausou:
                pygame.mixer.music.unpause()
                musica_pausou = False
        else:
            pygame.mixer.music.pause()
            musica_pausou = True

        if config.som_on:
            foreground.blit(check_box, (365, 339))

        # Sliders de som & música 
        slider_musica.desenhar(foreground)
        slider_som.desenhar(foreground)
        botao_voltar.desenhar(foreground)

        # Desenha grounds
        screen.blit(background, (0, 0))
        screen.blit(foreground, (0, 0))
            
        ## EVENTOS
        for event in pygame.event.get():
            if slider_musica.manipular_evento(event):
                config.musica_on = True
                config.volume_m = int(slider_musica.value)
                pygame.mixer.music.set_volume(slider_musica.value / 100)

            if slider_som.manipular_evento(event):
                config.som_on = True
                config.volume_s = int(slider_som.value)     

            if event.type == KEYDOWN and event.key == K_ESCAPE: # Apertou Esc
                opcoes_aberto = False
                from Particoes.menu import abrir_menu
                abrir_menu(screen, clock)

            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Clique com botão esquerdo        
                # Colisão circular com os sliders
                mouse_x, mouse_y = event.pos

                # Seleção de idioma
                if rect_portugues.collidepoint(event.pos) and selecionando_idioma:
                    config.idioma = "Português"
                elif rect_ingles.collidepoint(event.pos) and selecionando_idioma:
                    config.idioma = "English"
                elif rect_espanhol.collidepoint(event.pos) and selecionando_idioma: 
                    config.idioma = "Español"   

                # Botão de sair
                elif botao_voltar.rect.collidepoint(mouse_x, mouse_y): # Botão voltar
                    opcoes_aberto = False
                    from Particoes.menu import abrir_menu
                    abrir_menu(screen, clock)

                # Check box de música
                elif rect_musica.collidepoint(event.pos):
                    config.musica_on = False if config.musica_on else True
                # Check box de som
                elif rect_som.collidepoint(event.pos):
                    config.som_on = False if config.som_on else True

                # Botão de idioma
                if rect_idioma.collidepoint(event.pos) and not selecionando_idioma:
                    selecionando_idioma = True
                else:
                    selecionando_idioma = False


        pygame.display.update()
        clock.tick(60)
