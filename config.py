import pygame

pygame.init()
window_width = int(pygame.display.Info().current_w)
window_height = int(pygame.display.Info().current_h)
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
idioma = "Português"
musica_on = True
som_on = True
volume_m = 50
volume_s = 50
polimerase_selecionada = "taq"
dados_player = {}

######### TEMPORÁRIO #########
lista_dados_f = []
lista_dados_m = []
lista_dados_d = []