import pygame
import random
from vida import Vida
from arvores import Arvore
from grama import Grama
from armas import Arma
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, velocidade=11, vida_maxima=100):
        super().__init__()

        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)

        self.velocidade = velocidade
        self.vida = Vida(vida_maxima)

        # Sprites de animação de movimento
        self.sprites = [
            pygame.transform.scale(pygame.image.load("Sprites/Asrahel/Asrahel1.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("Sprites/Asrahel/Asrahel2.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("Sprites/Asrahel/Asrahel3.png"), (50, 50)),
        ]

        # Sprites de animação de idle
        self.sprites_idle = [
            pygame.transform.scale(pygame.image.load("Sprites/Asrahel/Idle/Asrahel_idle1.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("Sprites/Asrahel/Idle/Asrahel_idle2.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("Sprites/Asrahel/Idle/Asrahel_idle5.png"), (50, 50)),
        ]

        self.atual = 0
        self.frame_idle = 0
        self.image = self.sprites_idle[self.frame_idle]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.rect.inflate_ip(-30, -20)

        self.parado = True

        # Controle de tempo de animação
        self.tempo_animacao = 120  # milissegundos entre frames
        self.ultimo_update = pygame.time.get_ticks()

        # Armas
        self.armas_ativas = [
            Arma("Espada", "Sprites/Armas/espada.png", 10),
            Arma("Arco", "Sprites/Armas/arco.png", 8),
            Arma("Besta", "Sprites/Armas/besta.png", 12)
        ]
        self.arma_atual = self.armas_ativas[0]

    def receber_dano(self, dano):
        self.vida.receber_dano(dano)
        if not self.vida.esta_vivo():
            print("Você morreu!")

    def update(self):
        agora = pygame.time.get_ticks()

        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            if self.parado:
                self.frame_idle = (self.frame_idle + 1) % len(self.sprites_idle)
                self.image = self.sprites_idle[self.frame_idle]
            else:
                self.atual = (self.atual + 1) % len(self.sprites)
                self.image = self.sprites[self.atual]

        self.rect.center = (self.x, self.y)

    def mover(self, teclas, arvores):
        dx = dy = 0

        if teclas[pygame.K_LEFT]:
            dx = -self.velocidade
        if teclas[pygame.K_RIGHT]:
            dx = self.velocidade
        if teclas[pygame.K_UP]:
            dy = -self.velocidade
        if teclas[pygame.K_DOWN]:
            dy = self.velocidade

        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)

        self.parado = (dx == 0 and dy == 0)

    def trocar_arma(self):
        if len(self.armas_ativas) > 1:
            current_index = self.armas_ativas.index(self.arma_atual)
            self.arma_atual = self.armas_ativas[(current_index + 1) % len(self.armas_ativas)]

    def usar_arma(self, inimigo):
        if self.arma_atual.tipo == "melee":
            if self.rect.colliderect(inimigo.rect):
                inimigo.receber_dano(self.arma_atual.dano)
                print(f"Usou {self.arma_atual.nome} e causou {self.arma_atual.dano} de dano!")
        elif self.arma_atual.tipo == "ranged":
            print(f"Usou {self.arma_atual.nome} para ataque à distância!")

    def atacar(self, teclas, inimigos):
        if teclas[pygame.K_SPACE]:
            for inimigo in inimigos:
                self.usar_arma(inimigo)
                self.empurrar_jogador(inimigo)

    def empurrar_jogador(self, inimigo):
        if self.rect.colliderect(inimigo.rect):
            dx = self.rect.centerx - inimigo.rect.centerx
            dy = self.rect.centery - inimigo.rect.centery
            distancia = math.hypot(dx, dy)
            if distancia > 0:
                dx /= distancia
                dy /= distancia
                empurrar_forca = 15
                self.rect.x += dx * empurrar_forca
                self.rect.y += dy * empurrar_forca

    def desenhar_vida(self, tela, x, y):
        self.vida.desenhar(tela, x, y)
