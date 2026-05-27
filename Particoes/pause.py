import pygame, sys
from pygame.locals import *
from Particoes.classes import Slider
import config


def pausar(screen, clock):
    window_width, window_height = screen.get_size()

    # Cores
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    RED = (255, 0, 0)

    # Background cinza e transparente
    background_p = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background_p.fill(pygame.Color(120, 120, 120, 100))
    screen.blit(background_p, (0, 0))

    menu_pause = pygame.image.load(f"Imagens/pause_menu.png")

    # Rect para a identificação dos botões
    rect_sair = pygame.Rect((288, 555), (284, 119))
    rect_continuar = pygame.Rect((700, 555), (284, 119))

    # Slider da musica
    slider_musica = Slider((530, 291), 350, 15, 15, initial_val=config.volume_m, color=GRAY, fill_color=BLACK, show_value=True, font_name="Fontes/gliker-regular.ttf", font_size=36)

    # Slider do som
    slider_som = Slider((530, 359), 350, 15, 15, initial_val=config.volume_s, color=GRAY, fill_color=BLACK, show_value=True, font_name="Fontes/gliker-regular.ttf", font_size=36)

    # Valor do slider
    dragging_s = False

    ## CHECK BOX
    check_box = pygame.image.load(f"Imagens/check.png")

    # Rect botão de música e som
    rect_musica = pygame.Rect((463, 276), (45, 45))
    rect_som = pygame.Rect((463, 341), (45, 45))

    # Pause da música
    musica_pausou = False

    # Fonte
    try:
        font = pygame.font.Font("Fontes/gliker-regular.ttf", 36)
        mini_font = pygame.font.Font("Fontes/gliker-regular.ttf", 25)
    except:
        font = pygame.font.SysFont("arial", 36, bold=True)
        mini_font = pygame.font.SysFont("arial", 25, bold=True)

    # Idioma
    menu_idioma = pygame.image.load(f"Imagens/pause_menu_idioma.png")
    rect_idioma = pygame.Rect((463, 403), (247, 52))
    rect_portugues = pygame.Rect((463, 454), (247, 45))
    rect_ingles = pygame.Rect((463, 498), (247, 45))
    rect_espanhol = pygame.Rect((463, 543), (247, 45))
    idioma_indispoivel = mini_font.render(f"Idioma indisponível", True, RED)
    selecionando_idioma = False
    

    ########### WHILE ############
    
    ticking = 60
    p_running = True
    pausado = True

    while pausado:
        # Para diferenciar a passagem do tempo
        if ticking < 60:
            ticking += 1
        else:
            ticking = 0

        # Desenha menu
        if selecionando_idioma:
            screen.blit(menu_idioma, (265, 84))
        else:
            screen.blit(menu_pause, (265, 84))

        # Idioma
        texto_idioma = font.render(config.idioma, True, BLACK)
        screen.blit(texto_idioma, (470, 405)) 
        if config.idioma != "Português":
            screen.blit(idioma_indispoivel, (725, 410)) 

        # Check box
        if config.musica_on:
            screen.blit(check_box, (463, 276))
            if musica_pausou:
                pygame.mixer.music.unpause()
                musica_pausou = False
        else:
            pygame.mixer.music.pause()
            musica_pausou = True

        if config.som_on:
            screen.blit(check_box, (463, 341))

        slider_musica.desenhar(screen)
        slider_som.desenhar(screen)

        
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
                pausado = False

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
                elif rect_sair.collidepoint(event.pos):
                    pausado = False
                    p_running = False
                
                # Botão de continuar
                elif rect_continuar.collidepoint(event.pos): 
                    pausado = False

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
                
            elif event.type == MOUSEBUTTONUP and event.button == 1: # Soltou o botão esquerdo
                dragging_m = False
                dragging_s = False


        pygame.display.update()
        clock.tick(60)

    return(p_running)