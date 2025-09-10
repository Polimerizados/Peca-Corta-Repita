import pygame, sys
from pygame.locals import *
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

    menu_pause = pygame.transform.scale(pygame.image.load(f"Imagens/pause_menu.png"), (750, 636))

    # Rect para a identificação dos botões
    rect_sair = pygame.Rect((288, 555), (284, 119))
    rect_continuar = pygame.Rect((700, 555), (284, 119))

    ## SLIDER MÚSICA
    # Configurações do slider
    slider_x_m = 520
    slider_y_m = 291
    slider_width_m = 360
    slider_height_m = 15
    slider_rect_m = pygame.Rect((slider_x_m, slider_y_m), (slider_width_m, slider_height_m))

    # Controle deslizante CIRCULAR
    handle_radius_m = 15
    handle_center_m = [((config.volume_m/100)*slider_width_m) + slider_x_m , slider_y_m + slider_height_m//2]

    # Sombreamento do slider
    hover_slider_rect_m = pygame.Rect((slider_x_m, slider_y_m), (handle_center_m[0]-slider_x_m, slider_height_m))

    # Valor do slider
    dragging_m = False

    ## SLIDER SOM
    # Configurações do slider
    slider_x_s = 520
    slider_y_s = 359
    slider_width_s = 360
    slider_height_s = 15
    slider_rect_s = pygame.Rect((slider_x_s, slider_y_s), (slider_width_s, slider_height_s))

    # Controle deslizante CIRCULAR
    handle_radius_s = 15
    handle_center_s = [((config.volume_s/100)*slider_width_s) + slider_x_s, slider_y_s + slider_height_s//2]

    # Sombreamento do slider
    hover_slider_rect_s = pygame.Rect((slider_x_s, slider_y_s), (handle_center_s[0]-slider_x_s, slider_height_s))

    # Valor do slider
    dragging_s = False

    ## CHECK BOX
    check_box = pygame.transform.scale(pygame.image.load(f"Imagens/check.png"), (45, 45))

    # Rect botão de música e som
    rect_musica = pygame.Rect((463, 276), (45, 45))
    rect_som = pygame.Rect((463, 341), (45, 45))

    # Fonte
    try:
        font = pygame.font.Font("Fontes/gliker-regular.ttf", 36)
        mini_font = pygame.font.Font("Fontes/gliker-regular.ttf", 25)
    except:
        font = pygame.font.SysFont("arial", 36, bold=True)
        mini_font = pygame.font.SysFont("arial", 25, bold=True)

    # Idioma
    menu_idioma = pygame.transform.scale(pygame.image.load(f"Imagens/pause_menu_idioma.png"), (750, 636))
    rect_idioma = pygame.Rect((463, 403), (247, 52))
    rect_portugues = pygame.Rect((463, 454), (247, 45))
    rect_ingles = pygame.Rect((463, 498), (247, 45))
    rect_espanhol = pygame.Rect((463, 543), (247, 45))
    idioma_indispoivel = mini_font.render(f"Idioma indisponível", True, RED)
    selecionando_idioma = False

    
    ## FUNÇÕES
    def draw_rounded_rect(surface, color, rect, radius=5):
        """Desenha retângulo com cantos arredondados"""
        x, y, w, h = rect
        pygame.draw.rect(surface, color, (x + radius, y, w - 2*radius, h))
        pygame.draw.rect(surface, color, (x, y + radius, w, h - 2*radius))
        pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
        pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
        pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
        pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)

    def draw_slider():
        """Desenha slider de música e de som"""
        # Slider musica
        draw_rounded_rect(screen, GRAY, slider_rect_m, 7.5)

        draw_rounded_rect(screen, BLACK, hover_slider_rect_m, 7.5)

        pygame.draw.circle(screen, BLACK, handle_center_m, handle_radius_m)

        value_text = font.render(f"{config.volume_m}", True, BLACK)
        screen.blit(value_text, (slider_x_m + slider_width_m + 20, slider_y_m-15))

        # Slider som
        draw_rounded_rect(screen, GRAY, slider_rect_s, 7.5)

        draw_rounded_rect(screen, BLACK, hover_slider_rect_s, 7.5)

        pygame.draw.circle(screen, BLACK, handle_center_s, handle_radius_s)

        value_text = font.render(f"{config.volume_s}", True, BLACK)
        screen.blit(value_text, (slider_x_s + slider_width_s + 20, slider_y_s-15))

    def update_m_slider_value():
        """Atualiza o valor da música"""
        config.volume_m = int(((handle_center_m[0] - slider_x_m) / slider_width_m) * 100)
        config.volume_m = max(0, min(100, config.volume_m))
        
    def update_s_slider_value():
        """Atualiza o valor do som"""
        config.volume_s = int(((handle_center_s[0] - slider_x_s) / slider_width_s) * 100)
        config.volume_s = max(0, min(100, config.volume_s))

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
        if config.som_on:
            screen.blit(check_box, (463, 341))
        
        ## EVENTOS
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE: # Apertou Esc
                pausado = False

            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Clique com botão esquerdo        
                # Colisão circular com os sliders
                mouse_x, mouse_y = event.pos
                distance_m = ((mouse_x - handle_center_m[0])**2 + (mouse_y - handle_center_m[1])**2)**0.5
                distance_s = ((mouse_x - handle_center_s[0])**2 + (mouse_y - handle_center_s[1])**2)**0.5

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

                # Slider de música
                elif distance_m <= handle_radius_m:
                    dragging_m = True

                # Slider de som
                elif distance_s <= handle_radius_s:
                    dragging_s = True

                # Botão de idioma
                if rect_idioma.collidepoint(event.pos) and not selecionando_idioma:
                    selecionando_idioma = True
                else:
                    selecionando_idioma = False
                
            elif event.type == MOUSEBUTTONUP and event.button == 1: # Soltou o botão esquerdo
                dragging_m = False
                dragging_s = False

            elif event.type == MOUSEMOTION: # Movimentou o mouse
                # Segurando o slider de música
                if dragging_m:
                    config.musica_on = True
                    mouse_x = event.pos[0]
                    new_x = max(slider_x_m, min(slider_x_m + slider_width_m, mouse_x))
                    handle_center_m[0] = new_x
                    hover_slider_rect_m = pygame.Rect((slider_x_m, slider_y_m), (handle_center_m[0]-slider_x_m, slider_height_m))
                    update_m_slider_value()

                # Segurando o slider de som
                if dragging_s:
                    config.som_on = True
                    mouse_x = event.pos[0]
                    new_x = max(slider_x_s, min(slider_x_s + slider_width_s, mouse_x))
                    handle_center_s[0] = new_x
                    hover_slider_rect_s = pygame.Rect((slider_x_s, slider_y_s), (handle_center_s[0]-slider_x_s, slider_height_s))
                    update_s_slider_value()

        draw_slider()
        pygame.display.update()
        clock.tick(60)

    return(p_running)