from pygame import mixer
import config


def tocar_musica(musica):
    if config.musica_on:
        mixer.music.load(musica) # Carrega a música

        mixer.music.set_volume(config.volume_m/100) # Configura a música

        mixer.music.play() # Toca a música

som_hover = mixer.Sound("musicas/som.mp3") # Carrega o efeito sonoro

def tocar_som(somzeira):
    if config.som_on:
        somzeira.set_volume((config.volume_s)/100) # Configura o efeito sonoro

        somzeira.play() # Toca a música # Configura o efeito sonoro