# leaderboard_net.py
import socket, threading, json, time
import config
import pygame

BROADCAST_PORT = 50000
BROADCAST_ADDR = '<broadcast>'
BUFFER_SIZE = 65536
SEND_INTERVAL = 1.0  # segundos

def _current_payload():
    return {
        "ts": time.time(),
        "payload": {
            "f": config.lista_dados_f,
            "m": config.lista_dados_m,
            "d": config.lista_dados_d
        }
    }

def _merge_list(local_list, incoming_list, key_name="nome", score_name="pontuação"):
    lookup = { item[key_name]: item for item in local_list if key_name in item }
    for item in incoming_list:
        name = item.get(key_name)
        if not name:
            continue
        local = lookup.get(name)
        if local is None or item.get(score_name, 0) > local.get(score_name, 0):
            lookup[name] = item
    merged = list(lookup.values())
    merged.sort(key=lambda x: x.get(score_name, 0), reverse=True)
    return merged

class Broadcaster(threading.Thread):
    def __init__(self, interval=SEND_INTERVAL, port=BROADCAST_PORT):
        super().__init__(daemon=True)
        self.interval = interval
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.running = True
        self._last_send = 0

    def run(self):
        while self.running:
            now = time.time()
            if now - self._last_send >= self.interval:
                payload = _current_payload()
                try:
                    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
                    self.sock.sendto(data, (BROADCAST_ADDR, self.port))
                    self._last_send = now
                except Exception as e:
                    print("Erro broadcast:", e)
            time.sleep(0.1)

    def stop(self):
        self.running = False
        try:
            self.sock.close()
        except:
            pass

class Listener(threading.Thread):
    def __init__(self, port=BROADCAST_PORT):
        super().__init__(daemon=True)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind(('', self.port))
        except Exception as e:
            print("Erro bind Listener:", e)
            raise
        self.running = True

    def run(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(BUFFER_SIZE)
                try:
                    msg = json.loads(data.decode("utf-8"))
                    incoming = msg.get("payload", {})
                    changed = False
                    with config._leaderboard_lock:
                        f_merged = _merge_list(config.lista_dados_f, incoming.get("f", []))
                        m_merged = _merge_list(config.lista_dados_m, incoming.get("m", []))
                        d_merged = _merge_list(config.lista_dados_d, incoming.get("d", []))
                        if f_merged != config.lista_dados_f or m_merged != config.lista_dados_m or d_merged != config.lista_dados_d:
                            config.lista_dados_f = f_merged
                            config.lista_dados_m = m_merged
                            config.lista_dados_d = d_merged
                            changed = True
                    if changed:
                        config.save_leaderboard()
                        # posta um evento para o Pygame reagir (opcional)
                        try:
                            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'leaderboard_updated': True}))
                        except Exception:
                            pass
                except Exception as e:
                    print("Erro parse msg leaderboard:", e)
            except Exception as e:
                break

    def stop(self):
        self.running = False
        try:
            self.sock.close()
        except:
            pass

_broadcaster = None
_listener = None

def start_network_services(broadcast_interval=1.0):
    global _broadcaster, _listener
    if _listener is None:
        _listener = Listener()
        _listener.start()
    if _broadcaster is None:
        _broadcaster = Broadcaster(interval=broadcast_interval)
        _broadcaster.start()

def stop_network_services():
    global _broadcaster, _listener
    if _broadcaster:
        _broadcaster.stop()
        _broadcaster = None
    if _listener:
        _listener.stop()
        _listener = None
