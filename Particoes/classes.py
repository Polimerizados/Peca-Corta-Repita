import pygame, sys, random, os, math
from pygame.locals import *
from config import window_width, window_height
from Particoes.musica import tocar_som, som_hover
from typing import Callable


class dNTP:
    def __init__(self, level, up_down, base="random", pos="random"):
        self.level = level

        self.up_down = up_down

        if base == "random":
            if level == "f" or level == "m" or level == "d":
                bases = ["A", "T", "C", "G"]
            self.base = random.choice(bases)
        else:
            self.base = base

        if self.base == "A":
            self.base_par = "T"
            self.tipo = "purica"
        elif self.base == "T":
            self.base_par = "A"
            self.tipo = "pirimidica"
        elif self.base == "C":
            self.base_par = "G"
            self.tipo = "pirimidica"
        else:
            self.base_par = "C"
            self.tipo = "purica"
    
        self.img = pygame.image.load(f"Imagens/f{level}_d{self.base}TP_{self.up_down}.png") 

        if pos == "random":
            self.pos = (random.randint(0, window_width-80), random.randint(0, window_height-100))
        else:
            self.pos = pos

        self.tick = random.randint(0, 59)

        self.vel = (random.randint(-5, 5), random.randint(-5, 5))

    def acelerar(self):
        if self.pos[0] < 0:
            self.vel = (random.randint(1, 5), random.randint(-5, 5))                
        elif self.pos[0] > window_width:
            self.vel = (random.randint(-5, -1), random.randint(-5, 5))
        if self.pos[1] < 0:
            self.vel = (random.randint(-5, 5), random.randint(1, 5))
        elif self.pos[1] > window_height:
            self.vel = (random.randint(-5, 5), random.randint(-5, -1))
        else:
            self.vel = (random.randint(-5, 5), random.randint(-5, 5))

    def deslocar(self, scrolling=0):
        if scrolling == 0:
            self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        else:
            self.pos = (self.pos[0] + 2*scrolling, self.pos[1] + self.vel[1])



class ligH:
    def __init__(self, base, base_par):
        self.base = base
        self.base_par = base_par
        if self.base == "A" and self.base_par == "T":
            self.img = pygame.image.load(f"Imagens/ligH_AT.png")
        elif self.base == "T" and self.base_par == "A":
            self.img = pygame.image.load(f"Imagens/ligH_TA.png")
        elif self.base == "C" and self.base_par == "G":
            self.img = pygame.image.load(f"Imagens/ligH_CG.png")
        elif self.base == "G" and self.base_par == "C":
            self.img = pygame.image.load(f"Imagens/ligH_GC.png")
        
class dP:
    def __init__(self, level, tipo="purica", up_down="up"):
        self.level = level
        self.tipo = tipo
        if level == "m" or level == "d":
            self.img = pygame.image.load(f"Imagens/f{level}_dP_{tipo}_{up_down}.png")



class bolinhas:
    def __init__(self, pos="random"):
        if pos == "random":
            self.pos = (random.randint(0, window_width-80), random.randint(0, window_height-100))
        else:
            self.pos = pos
        self.tick = random.randint(0, 59)
        self.vel = (random.randint(-3, 3), random.randint(-3, 3))
        self.img = pygame.transform.scale(pygame.image.load(f"Imagens/bolinha.png"), (10, 10)) 

    def acelerar(self):
        if self.pos[0] < 0:
            self.vel = (random.randint(0, 1), random.randint(-1, 1))                
        elif self.pos[0] > window_width:
            self.vel = (random.randint(-1, 0), random.randint(-1, 1))
        elif self.pos[1] < 0:
            self.vel = (random.randint(-1, 1), random.randint(0, 1))
        elif self.pos[1] > window_height:
            self.vel = (random.randint(-1, 1), random.randint(-1, 0))
        else:
            self.vel = (random.randint(-1, 1), random.randint(-1, 1))

    def deslocar(self, scrolling):
        self.pos = (self.pos[0] + self.vel[0] + scrolling / 2, self.pos[1] + self.vel[1])
        


class polimerase:
    def __init__(self, polimerase_selecionada, dificuldade, pos):
        self.img = pygame.image.load(f"Imagens/{polimerase_selecionada}_polimerase.png")
        self.pos_original = pos
        self.pos = [self.pos_original[0], self.pos_original[1]] # Lista, para poder manipular

        if polimerase_selecionada == "taq":
            self.scrolling_ticks = 200 # Imagem 100X100, mas o dobro de ticks
            self.scrolling = -1 # 1 pixel por tick confirmado
            self.se_multiplo = True # pulando 1 tick sim, 1 não, 3,333 sec para cada pareamento
        elif polimerase_selecionada ==  "phusion":
            self.scrolling_ticks = 100
            self.scrolling = -1 # 1,666 sec para cada pareamento
            self.se_multiplo = False
        elif polimerase_selecionada == "PFU":
            self.scrolling_ticks = 50
            self.scrolling = -2 # 0,888 sec para cada pareamento
            self.se_multiplo = False
        else: # Polimerase Q5            
            self.scrolling_ticks = 25
            self.scrolling = -4
            self.se_multiplo = False

        self.decimo_de_ciclo = self.scrolling_ticks / 10 
        self.key_cima = 0
         
    def car_tremble(self, scroll_ticks):

        if self.pos[1] == self.pos_original[1]:
            self.key_cima = self.decimo_de_ciclo

        if self.key_cima > 0:
            s_pos = 10 * (scroll_ticks % self.decimo_de_ciclo) ** 3 / self.decimo_de_ciclo ** 3
            self.key_cima -= 1

        else:
            s_pos = (self.decimo_de_ciclo ** 3 * scroll_ticks / 10) ** (1/3)

        self.pos = [self.pos_original[0], self.pos_original[1] + int(s_pos)]



class PolimeraseSelect:
    def __init__(self, cx, cy, raio, dicionario, scale=185, img="taq_polimerase_select", vel_ang=2, pos_inicial=0):
        self.cx = cx
        self.cy = cy
        self.raio = raio
        self.scale = scale
        self.nome = dicionario["nome"]
        self.tag = dicionario["tag"]
        self.custo = dicionario["custo"]
        self.desbloqueado = dicionario["desbloqueado"]
        self.img = pygame.image.load(f"Imagens/{img}.png")
        try:
            self.img_bloqueado = pygame.image.load(f"Imagens/bloqueado_{self.custo}.png")
        except:
            self.img_bloqueado = pygame.image.load(f"Imagens/bloqueado_1000.png")
        self.velocidade_angular = vel_ang
        

        # Ângulos dos 4 pontos principais
        self.angulos = [90, 0, 270, 180] # Atrás, direita, frente, esquerda
        self.posicao_atual = pos_inicial
        self.posicao_alvo = pos_inicial

        self.angulo = self.angulos[self.posicao_atual]
        self.alvo = self.angulo
        self.direcao = 0  # +1 anti-horário, -1 horário, 0 parado

    def girar_direita(self):
        if self.direcao == 0:
            self.posicao_alvo = (self.posicao_alvo + 1) % 4
            self.alvo = self.angulos[self.posicao_alvo]
            self.direcao = -1  # horário

    def girar_esquerda(self):
        if self.direcao == 0:
            self.posicao_alvo = (self.posicao_alvo - 1) % 4
            self.alvo = self.angulos[self.posicao_alvo]
            self.direcao = +1  # anti-horário

    def update(self):
        if self.direcao != 0:
            if self.angulo == self.alvo:
                self.posicao_atual = self.posicao_alvo
                self.direcao = 0
            else:
                self.angulo += self.velocidade_angular * self.direcao
                self.angulo %= 360


    def draw(self, surface):
        if self.posicao_atual == 0 and self.direcao == 0:
            pass
        else:
            rad = math.radians(self.angulo)
            x = self.cx + self.raio * math.cos(rad)
            y = self.cy - self.raio * math.sin(rad)
            self.scale = y*0.2 + 65
            imagem = pygame.transform.scale(self.img, (self.scale, self.scale))
            imagem_bloqueado = pygame.transform.scale(self.img_bloqueado, (self.scale, self.scale))

            # posição
            img_x = x - (self.scale / 2)
            img_y = 292.5 - (self.scale / 2)
            self.rect = pygame.Rect(img_x, img_y, self.scale, self.scale)

            if self.posicao_atual == 0:
                self.rect = pygame.Rect(img_x, img_y, self.scale, self.scale)
            else:
                self.rect = None

            fog = max(0, min(255, int(-y * 0.5 + 300)))

            # desenhar a imagem 
            surface.blit(imagem, (img_x, img_y))

            if not self.desbloqueado:
                surface.blit(imagem_bloqueado, (img_x, img_y))

            # camada de fog
            fog_surface = pygame.Surface((self.scale, self.scale), pygame.SRCALPHA)
            fog_surface.fill((20, 20, 20, fog))  

            # aplicar por cima
            surface.blit(fog_surface, (img_x, img_y))
    
    def comprar(self):
        try:
            with open("pontuacao.txt", "r") as f:
                nucleotideos = int(f.read())
        except:
            nucleotideos = 500
        if not self.desbloqueado and nucleotideos >= self.custo:
            self.desbloqueado = True
            nucleotideos -= self.custo
            with open("pontuacao.txt", "w") as f:
                f.write(str(nucleotideos))
            return True
        else:
            return False
        

class Botao:
    """Cria um botão com efeito de hover, forma e texto customizáveis."""

    def __init__(
        self,
        tamanho: tuple[int, int],
        pos: tuple[int, int],
        img: str | None = None,
        cor: tuple[int, int, int] = (255, 255, 255),
        fator_hover: float = 1.0,
        cor_hover: tuple[int, int, int] | None = None,
        cor_clique: tuple[int, int, int] | None = None,
        raio_borda: int = 0,
        fn_desenho: Callable[[pygame.Surface, pygame.Rect, tuple], None] | None = None,
        texto: str | None = None,
        nome_fonte: str | None = None,
        tamanho_fonte: int = 16,
        cor_texto: tuple[int, int, int] = (0, 0, 0),
        cor_texto_hover: tuple[int, int, int] | None = None,
        cor_texto_clique: tuple[int, int, int] | None = None,
        ancora_texto: tuple[float, float] = (0.5, 0.5),
        borda: float = 0,
        cor_borda: tuple[int, int, int] | None = None,
        cor_borda_hover: tuple[int, int, int] | None = None,
        cor_borda_clique: tuple[int, int, int] | None = None,
    ):
        self.cor = cor
        self.cor_hover = cor_hover or cor
        self.cor_clique = cor_clique or self.cor_hover
        self.raio_borda = raio_borda
        self.raio_borda_hover = round(raio_borda * fator_hover)
        self.fn_desenho = fn_desenho

        self.borda = borda
        self.borda_hover = round(borda * fator_hover)
        self.cor_borda = cor_borda or cor_texto
        self.cor_borda_hover = cor_borda_hover or self.cor_borda
        self.cor_borda_clique = cor_borda_clique or self.cor_borda_hover

        self.texto = texto
        self.cor_texto = cor_texto
        self.cor_texto_hover = cor_texto_hover or cor_texto
        self.cor_texto_clique = cor_texto_clique or self.cor_texto_hover
        self.ancora_texto = ancora_texto
        self.estava_hover = False

        self.rect = pygame.Rect(pos, tamanho)
        self.rect_ativo = self.rect

        lh = tamanho[0] * fator_hover
        ah = tamanho[1] * fator_hover
        px = pos[0] - (lh - tamanho[0]) / 2
        py = pos[1] - (ah - tamanho[1]) / 2
        self.rect_hover = pygame.Rect(px, py, lh, ah)

        bruto = self._carregar_imagem(img)
        self._imagem = pygame.transform.scale(bruto, tamanho) if bruto else None
        self._imagem_hover = pygame.transform.scale(self._carregar_imagem_hover(img), (int(lh), int(ah))) if bruto else None

        if texto is not None:
            self._fonte = pygame.font.Font(nome_fonte, tamanho_fonte)
            self._fonte_hover = pygame.font.Font(nome_fonte, int(tamanho_fonte * fator_hover))
        else:
            self._fonte = None
            self._fonte_hover = None

        self._clicado = False

    # ------------------------------------------------------------------

    @staticmethod
    def _carregar_imagem(nome: str | None) -> pygame.Surface | None:
        if nome is None:
            return None
        try:
            return pygame.image.load(f"Imagens/{nome}.png")
        except Exception:
            return None
    
    @staticmethod 
    def _carregar_imagem_hover(nome: str | None) -> pygame.Surface | None:
        if nome is None:
            return None
        try:
            try:
                return pygame.image.load(f"Imagens/{nome}_hover.png")
            except Exception:
                return pygame.image.load(f"Imagens/{nome}.png")
        except Exception:
            return None

    @property
    def com_hover(self) -> bool:
        return self.rect_ativo.collidepoint(pygame.mouse.get_pos())

    # ------------------------------------------------------------------

    def processar_evento(self, evento: pygame.event.Event) -> bool:
        """Processa eventos do botão. Retorna True no momento do clique."""
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_ativo.collidepoint(evento.pos):
                self._clicado = True

        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if self._clicado and self.rect_ativo.collidepoint(evento.pos):
                self._clicado = False
                return True
            self._clicado = False

        return False

    # ------------------------------------------------------------------

    def _desenhar_texto(self, superficie: pygame.Surface, rect: pygame.Rect, hover: bool) -> None:
        if not self.texto or not self._fonte:
            return

        if self._clicado:
            fonte = self._fonte_hover
            cor = self.cor_texto_clique
        elif hover:
            fonte = self._fonte_hover
            cor = self.cor_texto_hover
        else:
            fonte = self._fonte
            cor = self.cor_texto

        surf_texto = fonte.render(self.texto, True, cor)
        lt, at = surf_texto.get_size()

        ax, ay = self.ancora_texto
        x = rect.x + ax * (rect.width - lt)
        y = rect.y + ay * (rect.height - at)

        superficie.blit(surf_texto, (x, y))

    def desenhar(self, superficie: pygame.Surface) -> None:
        hover = self.com_hover

        if hover and not self.estava_hover:
            tocar_som(som_hover)
        self.estava_hover = hover

        if self._clicado:
            self.rect_ativo = self.rect_hover
            cor = self.cor_clique
            imagem = self._imagem_hover
            cor_borda = self.cor_borda_clique
            borda = self.borda_hover
            raio_borda = self.raio_borda_hover
        elif hover:
            self.rect_ativo = self.rect_hover
            cor = self.cor_hover
            imagem = self._imagem_hover
            cor_borda = self.cor_borda_hover
            borda = self.borda_hover
            raio_borda = self.raio_borda_hover
        else:
            self.rect_ativo = self.rect
            cor = self.cor
            imagem = self._imagem
            cor_borda = self.cor_borda
            borda = self.borda
            raio_borda = self.raio_borda

        if imagem:
            superficie.blit(imagem, self.rect_ativo)
        elif self.fn_desenho:
            self.fn_desenho(superficie, self.rect_ativo, cor)
        else:
            pygame.draw.rect(superficie, cor, self.rect_ativo, border_radius=raio_borda)
            if self.borda:
                pygame.draw.rect(superficie, cor_borda, self.rect_ativo, borda, border_radius=raio_borda)

        self._desenhar_texto(superficie, self.rect_ativo, hover)

    def colide(self, pos: tuple[int, int]) -> bool:
        return self.rect_ativo.collidepoint(pos)

# Caixas de texto (para o menu)    
class CaixaTexto:
    def __init__(self, x, y):
        self.posx = x
        self.posy = y
        self.texto = ""
        self.ativo = True
        self.cursor_visivel = True
        self.cursor_ativo = True
        self.tempo_cursor = 0
        
    def manipular_evento(self, evento):
        if evento.type == pygame.KEYDOWN and self.ativo:
            if evento.key == pygame.K_BACKSPACE: # Apertou a tecla de apagar
                self.texto = self.texto[:-1] # Apagar último caractere
            else:
                # Adicionar caractere (limitar a 3 caracteres)
                if len(self.texto) < 3:
                    self.texto += evento.unicode

        return False  # Retorna False por padrão
    
    def atualizar(self):
        if len(self.texto) < 3:
            self.cursor_ativo = True
        else:
            self.cursor_ativo = False

        if self.cursor_ativo:
            # Piscar o cursor
            self.tempo_cursor += 1
            if self.tempo_cursor > 24:  # A cada 60 frames
                self.cursor_visivel = not self.cursor_visivel
                self.tempo_cursor = 0
    
    def desenhar(self, superficie, fonte):
        # Desenhar o texto
        texto_surface = fonte.render(self.texto, True, (0, 0, 0))
        superficie.blit(texto_surface, (self.posx + 20, self.posy + 3))
        
        # Desenhar cursor se estiver ativo
        if self.cursor_ativo and self.cursor_visivel:
            pygame.draw.line(superficie, (0, 0, 0), (20 + self.posx + 30*len(self.texto), self.posy + 40), (40 + self.posx + 30*len(self.texto), self.posy + 40), 3)
    
    def salvar(self, pontuacao, dificuldade):
        self.ativo = False
        return {"nome": self.texto, "pontuação": pontuacao, "dificuldade":dificuldade}