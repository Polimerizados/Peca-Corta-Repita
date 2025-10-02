import pygame, sys
from pygame.locals import *
from Particoes.classes import CaixaTexto
import config


def gameover(screen, clock, dificuldade):
    window_width, window_height = screen.get_size()

    # Background cinza e transparente
    background_p = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background_p.fill(pygame.Color(120, 120, 120, 100))
    screen.blit(background_p, (0, 0))

    fim_de_jogo = pygame.image.load(f"Imagens/fim_de_jogo.png")
    fim_de_jogo_s = pygame.image.load(f"Imagens/fim_de_jogo_s.png")

    # Rect para a identificação dos botões
    rect_sair = pygame.Rect((813, 555), (159, 119))
    rect_classificacao = pygame.Rect((308, 555), (484, 119))
    rect_salvar = pygame.Rect((570, 475), (398, 59))

    # Caixa de texto
    caixa_texto = CaixaTexto(440, 475)

    ###### TEMPORÁRIO ######
    fonte = pygame.font.Font("Fontes/gliker-regular.ttf", 40)
    mini_fonte = pygame.font.Font("Fontes/gliker-regular.ttf", 30)
    opção_indispoivel = mini_fonte.render(f"Opção indisponível", True, (255, 0, 0))


    ########### WHILE ############
    ticking = 60
    tela_gameover = True
    salvo = False

    while tela_gameover:
        # Para diferenciar a passagem do tempo
        if ticking < 60:
            ticking += 1
        else:
            ticking = 0

        # Desenha tela de fim de jogo
        if salvo:
            screen.blit(fim_de_jogo_s, (265, 84))
        else:
            screen.blit(fim_de_jogo, (265, 84))

        ###### TEMPORÁRIO ######
        try:
            if erro:
                screen.blit(opção_indispoivel, (410, 673))
        except:
            erro = False

        ## EVENTOS
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE: # Apertou Esc
                tela_gameover = False
                from Particoes.menu import abrir_menu
                abrir_menu(screen, clock)

            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Clique com botão esquerdo        
                # Botão de sair
                if rect_sair.collidepoint(event.pos):
                    tela_gameover = False
                    from Particoes.menu import abrir_menu
                    abrir_menu(screen, clock)
                
                # Botão de classificacao
                elif rect_classificacao.collidepoint(event.pos): 
                    ###### TEMPORÁRIO ######
                    erro = True

                # Botao de salvar
                elif rect_salvar.collidepoint(event.pos): 
                    config.dados_player = caixa_texto.salvar(100, dificuldade)
                    print(config.dados_player)
                    salvo = True
            
            caixa_texto.manipular_evento(event)

        caixa_texto.atualizar()

        caixa_texto.desenhar(screen, fonte)


        pygame.display.update()
        clock.tick(60)