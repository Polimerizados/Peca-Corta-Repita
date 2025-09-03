import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas

def pausar(screen, clock):
    window_width, window_height = screen.get_size()

    # Cores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    BLUE = (0, 0, 255)

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
    handle_center_m = [slider_x_m + 180, slider_y_m + slider_height_m//2]

    # Sombreamento do slider
    hover_slider_rect_m = pygame.Rect((slider_x_m, slider_y_m), (handle_center_m[0]-slider_x_m, slider_height_m))

    # Valor do slider
    slider_value_m = 50
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
    handle_center_s = [slider_x_s + 180, slider_y_s + slider_height_s//2]

    # Sombreamento do slider
    hover_slider_rect_s = pygame.Rect((slider_x_s, slider_y_s), (handle_center_s[0]-slider_x_s, slider_height_s))

    # Valor do slider
    slider_value_s = 50
    dragging_s = False

    # Fonte
    try:
        font = pygame.font.Font("Fontes/gliker-regular.ttf", 36)
    except:
        font = pygame.font.SysFont("arial", 36, bold=True)

    
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

        value_text = font.render(f"{slider_value_m}", True, BLACK)
        screen.blit(value_text, (slider_x_m + slider_width_m + 20, slider_y_m-15))

        # Slider som
        draw_rounded_rect(screen, GRAY, slider_rect_s, 7.5)

        draw_rounded_rect(screen, BLACK, hover_slider_rect_s, 7.5)

        pygame.draw.circle(screen, BLACK, handle_center_s, handle_radius_s)

        value_text = font.render(f"{slider_value_s}", True, BLACK)
        screen.blit(value_text, (slider_x_s + slider_width_s + 20, slider_y_s-15))

    def update_m_slider_value():
        """Atualiza o valor da música"""
        nonlocal slider_value_m
        slider_value_m = int(((handle_center_m[0] - slider_x_m) / slider_width_m) * 100)
        slider_value_m = max(0, min(100, slider_value_m))
        
    def update_s_slider_value():
        """Atualiza o valor do som"""
        nonlocal slider_value_s
        slider_value_s = int(((handle_center_s[0] - slider_x_s) / slider_width_s) * 100)
        slider_value_s = max(0, min(100, slider_value_s))

    ticking = 60
    p_running = True
    pausado = True

    while pausado:
        
        if ticking < 60:
            ticking += 1
        else:
            ticking = 0

        screen.blit(menu_pause, (265, 84))

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE: # Apertou Esc
                pausado = False

            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Clique com botão esquerdo
                # Botão de sair
                if rect_sair.collidepoint(event.pos):
                    pausado = False
                    p_running = False
                
                #   Botão de continuar
                if rect_continuar.collidepoint(event.pos): 
                    pausado = False

                # Colisão circular com os sliders
                mouse_x, mouse_y = event.pos
                distance_m = ((mouse_x - handle_center_m[0])**2 + (mouse_y - handle_center_m[1])**2)**0.5
                distance_s = ((mouse_x - handle_center_s[0])**2 + (mouse_y - handle_center_s[1])**2)**0.5

                # Slider de música
                if distance_m <= handle_radius_m:
                    dragging_m = True

                # Slider de som
                if distance_s <= handle_radius_s:
                    dragging_s = True    

            elif event.type == MOUSEBUTTONUP and event.button == 1: # Soltou o botão esquerdo
                dragging_m = False
                dragging_s = False

            elif event.type == MOUSEMOTION: # Movimentou o mouse
                # Segurando o slider de música
                if dragging_m:
                    mouse_x = event.pos[0]
                    new_x = max(slider_x_m, min(slider_x_m + slider_width_m, mouse_x))
                    handle_center_m[0] = new_x
                    hover_slider_rect_m = pygame.Rect((slider_x_m, slider_y_m), (handle_center_m[0]-slider_x_m, slider_height_m))
                    update_m_slider_value()

                # Segurando o slider de som
                if dragging_s:
                    mouse_x = event.pos[0]
                    new_x = max(slider_x_s, min(slider_x_s + slider_width_s, mouse_x))
                    handle_center_s[0] = new_x
                    hover_slider_rect_s = pygame.Rect((slider_x_s, slider_y_s), (handle_center_s[0]-slider_x_s, slider_height_s))
                    update_s_slider_value()

        draw_slider()
        pygame.display.update()
        clock.tick(60)

    return(p_running)