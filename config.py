import socket, threading, json, time, os
import config
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

_LEADERBOARD_FILE = "leaderboard.json"
_leaderboard_lock = threading.Lock()

def _atomic_write(path, data_str):
    dirn = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmpname = tempfile.mkstemp(dir=dirn)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(data_str)
        os.replace(tmpname, path)
    except Exception:
        if os.path.exists(tmpname):
            os.remove(tmpname)
        raise

def save_leaderboard():
    with _leaderboard_lock:
        data = {
            "f": lista_dados_f,
            "m": lista_dados_m,
            "d": lista_dados_d,
            "ts": time.time()
        }
        s = json.dumps(data, ensure_ascii=False, indent=2)
        _atomic_write(_LEADERBOARD_FILE, s)

def load_leaderboard():
    global lista_dados_f, lista_dados_m, lista_dados_d
    if not os.path.exists(_LEADERBOARD_FILE):
        return
    with _leaderboard_lock:
        try:
            with open(_LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            lista_dados_f = data.get("f", [])
            lista_dados_m = data.get("m", [])
            lista_dados_d = data.get("d", [])
        except Exception as e:
            print("Erro ao carregar leaderboard:", e)

load_leaderboard()