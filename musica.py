from pygame import mixer
import config


def tocar_musica(musica):
    
    mixer.music.load(musica) # Carrega a música

    mixer.music.set_volume((config.volume_m)/200) # Configura o volume

    mixer.music.play() # Toca a música

def tocar_som():
    if config.som_on:
        som_hover = mixer.Sound("Particoes/som.mp3") # Carrega a música

        som_hover.set_volume((config.volume_s)/100)

        som_hover.play() # Toca a música