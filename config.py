import pygame

pygame.init()
window_width = int(pygame.display.Info().current_w)
window_height = int(pygame.display.Info().current_h)
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()