import pygame, sys
from pygame.locals import *
from Particoes.classes import CaixaTexto
import config
from musica import tocar_musica

# Tenta importar o módulo de rede (opcional)
try:
    import leaderboard_net
    _NETWORK_AVAILABLE = True
except Exception:
    leaderboard_net = None
    _NETWORK_AVAILABLE = False


def gameover(screen, clock, dificuldade, pontuacao):
    window_width, window_height = screen.get_size()

    # Background cinza e transparente
    background_p = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    background_p.fill(pygame.Color(120, 120, 120, 100))
    screen.blit(background_p, (0, 0))

    fim_de_jogo = pygame.image.load(f"Imagens/fim_de_jogo.png")
    fim_de_jogo_s = pygame.image.load(f"Imagens/fim_de_jogo_s.png")
    fim_de_jogo_nhs = pygame.image.load(f"Imagens/fim_de_jogo_nhs.png")
    fim_de_jogo_nhs_s = pygame.image.load(f"Imagens/fim_de_jogo_nhs_s.png")

    # Rect para a identificação dos botões
    rect_sair = pygame.Rect((813, 555), (159, 119))
    rect_classificacao = pygame.Rect((308, 555), (484, 119))
    rect_salvar = pygame.Rect((570, 475), (398, 59))

    # Caixa de texto
    caixa_texto = CaixaTexto(440, 475)

    # Importar fonte
    mini_fonte = pygame.font.Font("Fontes/gliker-regular.ttf", 20)
    fonte = pygame.font.Font("Fontes/gliker-regular.ttf", 40)
    mega_fonte = pygame.font.Font("Fontes/gliker-regular.ttf", 70)

    # Carregar pontuacao
    texto_pontuacao = mega_fonte.render(str(pontuacao), True, (0, 0, 0))
    pos_pontuacao = (640 - (texto_pontuacao.get_width() / 2), 285)

    # Checa novo record
    if dificuldade == "f":
        if len(config.lista_dados_f) > 0 and pontuacao <= config.lista_dados_f[0]["pontuação"]:
            recorde = False
        else:
            recorde = True
  
    if dificuldade == "m":
        if len(config.lista_dados_m) > 0 and pontuacao <= config.lista_dados_m[0]["pontuação"]:
            recorde = False
        else:
            recorde = True
    
    if dificuldade == "d":
        if len(config.lista_dados_d) > 0 and pontuacao <= config.lista_dados_d[0]["pontuação"]:
            recorde = False
        else:
            recorde = True


    # Textos de erro
    texto_erro = mini_fonte.render("Seu nome precisa conter 3 caracteres", True, (255, 0, 0))
    erro = False

    texto_strike = mini_fonte.render("Atenção! Se sair sua pontuação não será salva!", True, (255, 0, 0))
    strike = False

    texto_nome = mini_fonte.render("Esse nome já está no placar", True, (255, 0, 0))
    erro_nome = False

    # Música
    tocar_musica("musicas/macacos_me_mordam.wav")

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
        if recorde:
            if salvo:    
                screen.blit(fim_de_jogo_nhs_s, (265, 84))
            else:
                screen.blit(fim_de_jogo_nhs, (265, 84))
        else:
            if salvo:    
                screen.blit(fim_de_jogo_s, (265, 84))
            else:
                screen.blit(fim_de_jogo, (265, 84))

        # Desenha pontuação
        screen.blit(texto_pontuacao, pos_pontuacao)

        # Desenha textos de erro
        if erro:
            screen.blit(texto_erro, (570, 440))
        if erro_nome:
            screen.blit(texto_nome, (570, 440))
        if strike:
            screen.blit(texto_strike, (308, 678))

        ## EVENTOS
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:  # Apertou Esc
                tela_gameover = False
                from Particoes.menu import abrir_menu
                abrir_menu(screen, clock)

            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Clique com botão esquerdo
                # Botão de sair
                if rect_sair.collidepoint(event.pos):
                    if salvo == True or strike == True:
                        tela_gameover = False
                        from Particoes.menu import abrir_menu
                        abrir_menu(screen, clock)
                    else:
                        strike = True

                # Botão de classificacao
                elif rect_classificacao.collidepoint(event.pos):
                    if salvo == True or strike == True:
                        tela_gameover = False
                        from Particoes.leaderboard import abrir_classificacao
                        abrir_classificacao(screen, clock)
                    else:
                        strike = True

                # Botao de salvar
                elif rect_salvar.collidepoint(event.pos):
                    if len(caixa_texto.texto) == 3:
                        # tenta obter o registro do CaixaTexto.salvar
                        novo_registro = caixa_texto.salvar(pontuacao, dificuldade)

                        # se salvar retornou só a string do nome, normaliza para dict
                        if isinstance(novo_registro, str):
                            novo_registro = {"nome": novo_registro, "pontuação": pontuacao}
                        # garanta chaves mínimas
                        novo_registro.setdefault("nome", "")
                        novo_registro.setdefault("pontuação", pontuacao)

                        # função auxiliar local para checar existência e inserir
                        def inserir_se_vazio(lista, novo):
                            nomes = [dado.get("nome") for dado in lista]
                            lista.append(novo)
                            return True
                            

                        inseriu = False
                        if dificuldade == "f":
                            inseriu = inserir_se_vazio(config.lista_dados_f, novo_registro)
                        elif dificuldade == "m":
                            inseriu = inserir_se_vazio(config.lista_dados_m, novo_registro)
                        elif dificuldade == "d":
                            inseriu = inserir_se_vazio(config.lista_dados_d, novo_registro)

                        if inseriu:
                            # marca salvo para UI
                            salvo = True
                            erro_nome = False
                            strike = False
                            erro = False

                            # garante que os serviços de rede estão rodando (se disponíveis)
                            if _NETWORK_AVAILABLE:
                                try:
                                    leaderboard_net.start_network_services()
                                except Exception:
                                    # ignora se falhar (já rodando ou erro)
                                    pass

                            # salva o leaderboard em disco (persistência imediata)
                            try:
                                config.save_leaderboard()
                            except Exception as e:
                                print("Erro ao salvar leaderboard:", e)

                            # notifica o Pygame / UI que houve atualização (opcional)
                            try:
                                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'leaderboard_updated': True}))
                            except Exception:
                                pass

                        else:
                            # nome já existe
                            erro_nome = True
                            erro = False

                    else:
                        erro = True
                        erro_nome = False

            caixa_texto.manipular_evento(event)

        caixa_texto.atualizar()

        caixa_texto.desenhar(screen, fonte)

        pygame.display.update()
        clock.tick(60)
