from pygame import mixer
import config
from config import resource_path

def tocar_musica(musica):
    if config.musica_on:
        mixer.music.load(musica) # Carrega a música

        mixer.music.set_volume(config.volume_m/100) # Configura a música

        mixer.music.play() # Toca a música

som_hover = mixer.Sound(resource_path("musicas/som.mp3")) # Carrega o efeito sonoro

def tocar_som(som):
    if config.som_on:
        som.set_volume((config.volume_s)/100) # Configura o efeito sonoro

        som.play() # Toca a música # Configura o efeito sonoro