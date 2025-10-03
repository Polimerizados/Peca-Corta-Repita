import pygame, sys, random, os, math
from pygame.locals import *
from config import window_width, window_height
from musica import tocar_som
from math import sin, atan

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
        self.sentido = 1 # 1 cima, -1 baixo
        self_aceleracao_vertical = 2/5

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
            
            """MANUTENÇÃO --- CHECAR COMO SERÁ"""
            
            self.scrolling_ticks = 100
            self.scrolling = -1 
            self.se_multiplo = False



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
    def __init__(self, tamanho, tamanho_hover, pos, pos_hover, imagem):
        
        # Define imagens e rects (normal e hover)
        img = pygame.image.load(f"Imagens/{imagem}.png")
        img_hover = pygame.image.load(f"Imagens/{imagem}_hover.png")

        rect = pygame.Rect(pos, tamanho)
        rect_hover =  pygame.Rect(pos_hover, tamanho_hover)
        self.rect = rect # Rect inicial

        # Armazena parâmetros
        self.imgs = (img, img_hover)
        self.rects = (rect, rect_hover)
        self.tamanhos = (tamanho, tamanho_hover)
        self.posicoes = (pos, pos_hover)
            
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        hovering = self.rect.collidepoint(mouse_pos)

        if hovering and self.rect == self.rects[0]:
            tocar_som()

        # Checa se o mouse está sobre o botão e define os parâmetros utilizados (normal ou hover)
        if hovering: 
            self.img = self.imgs[1] 
            self.pos = self.posicoes[1] 
            self.rect = self.rects[1]  
        else:
            self.img = self.imgs[0] 
            self.pos = self.posicoes[0] 
            self.rect = self.rects[0]

        # Desenha botão
        surface.blit(self.img, self.pos)

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
