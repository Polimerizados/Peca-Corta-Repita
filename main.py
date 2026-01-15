from pygame.time import Clock
from pygame.display import set_caption, Info, set_mode
from Particoes.menu import abrir_menu


set_caption("pspspspspspspsps")

window_width = int(Info().current_w)
window_height = int(Info().current_h)

screen = set_mode((window_width, window_height))
clock = Clock()

abrir_menu(screen, clock)