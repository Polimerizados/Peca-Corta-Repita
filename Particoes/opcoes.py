import pygame, sys
from pygame.locals import *
from Particoes.classes import bolinhas
import config


def abrir_opcoes(screen, clock):
    window_width, window_height = screen.get_size()

    # Cores
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    RED = (255, 0, 0)

    bolinhas_bg = [bolinhas() for _ in range(100)]

    screen.fill(pygame.Color(255, 255, 255, 0))
    background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background.fill(pygame.Color(255, 255, 255, 0))

    botao_voltar = pygame.image.load(f"Imagens/botao_voltar.png")
    voltar_rect = pygame.Rect((50, window_height - 120), (210, 75))

    #####################################################

    menu_opcoes = pygame.image.load(f"Imagens/menu_opcoes.png")

    ## SLIDER MÚSICA
    # Configurações do slider
    slider_x_m = 453
    slider_y_m = 268
    slider_width_m = 534
    slider_height_m = 20
    slider_rect_m = pygame.Rect((slider_x_m, slider_y_m), (slider_width_m, slider_height_m))

    # Controle deslizante CIRCULAR
    handle_radius_m = 20
    handle_center_m = [((config.volume_m/100)*slider_width_m) + slider_x_m , slider_y_m + slider_height_m//2]

    # Sombreamento do slider
    hover_slider_rect_m = pygame.Rect((slider_x_m, slider_y_m), (handle_center_m[0]-slider_x_m, slider_height_m))

    # Valor do slider
    dragging_m = False

    ## SLIDER SOM
    # Configurações do slider
    slider_x_s = 453
    slider_y_s = 363
    slider_width_s = 534
    slider_height_s = 20
    slider_rect_s = pygame.Rect((slider_x_s, slider_y_s), (slider_width_s, slider_height_s))

    # Controle deslizante CIRCULAR
    handle_radius_s = 20
    handle_center_s = [((config.volume_s/100)*slider_width_s) + slider_x_s, slider_y_s + slider_height_s//2]

    # Sombreamento do slider
    hover_slider_rect_s = pygame.Rect((slider_x_s, slider_y_s), (handle_center_s[0]-slider_x_s, slider_height_s))

    # Valor do slider
    dragging_s = False

    ## CHECK BOX
    check_box = pygame.image.load(f"Imagens/check_opcoes.png")

    # Rect botão de música e som
    rect_musica = pygame.Rect((365, 243), (66, 66))
    rect_som = pygame.Rect((365, 339), (66, 66))

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
        screen.blit(value_text, (slider_x_m + slider_width_m + 20, slider_y_m-25))

        # Slider som
        draw_rounded_rect(screen, GRAY, slider_rect_s, 7.5)

        draw_rounded_rect(screen, BLACK, hover_slider_rect_s, 7.5)

        pygame.draw.circle(screen, BLACK, handle_center_s, handle_radius_s)

        value_text = font.render(f"{config.volume_s}", True, BLACK)
        screen.blit(value_text, (slider_x_s + slider_width_s + 20, slider_y_s-25))

    def update_m_slider_value():
        """Atualiza o valor da música"""
        config.volume_m = int(((handle_center_m[0] - slider_x_m) / slider_width_m) * 100)
        config.volume_m = max(0, min(100, config.volume_m))
        
    def update_s_slider_value():
        """Atualiza o valor do som"""
        config.volume_s = int(((handle_center_s[0] - slider_x_s) / slider_width_s) * 100)
        config.volume_s = max(0, min(100, config.volume_s))


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

        # Desenha as bolinhas
        for i in range(100):
            if ticking == bolinhas_bg[i].tick:
                bolinhas_bg[i].acelerar()
            bolinhas_bg[i].deslocar(0)
            background.blit(bolinhas_bg[i].img, bolinhas_bg[i].pos)

        # Desenha grounds
        screen.blit(background, (0, 0))

        # Desenha menu
        if selecionando_idioma:
            screen.blit(menu_opcoes_idioma, (0, 0))
        else:
            screen.blit(menu_opcoes, (0, 0))

        # Idioma
        texto_idioma = font.render(config.idioma, True, BLACK)
        screen.blit(texto_idioma, (375, 427)) 
        if config.idioma != "Português":
            screen.blit(idioma_indispoivel, (750, 445)) 

        # Check box
        if config.musica_on:
            screen.blit(check_box, (365, 243))
        if config.som_on:
            screen.blit(check_box, (365, 339))
        
        ## EVENTOS
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE: # Apertou Esc
                opcoes_aberto = False
                from Particoes.menu import abrir_menu
                abrir_menu(screen, clock)

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
                elif voltar_rect.collidepoint(event.pos):
                    opcoes_aberto = False
                    from Particoes.menu import abrir_menu
                    abrir_menu(screen, clock)

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
