import os

def salvar_pontuacao(pontos):
    with open("pontuacao.txt", "w") as f:
        f.write(str(pontos))

def carregar_pontuacao():
    if os.path.exists("pontuacao.txt"):
        with open("pontuacao.txt", "r") as f:
            return int(f.read())
    return 0