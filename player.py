import pygame
import random
from vida import Vida  # Importando a classe Vida
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

        # Vida do jogador
        self.vida = Vida(vida_maxima)

        # Sprites do jogador
        self.sprites = [
            pygame.transform.scale(pygame.image.load("Sprites/Asrahel/Asrahel1.png"), (70, 70)),
            pygame.transform.scale(pygame.image.load("Sprites/Asrahel/Asrahel2.png"), (70, 70)),
            pygame.transform.scale(pygame.image.load("Sprites/Asrahel/Asrahel3.png"), (70, 70))
        ]

        self.atual = 0
        self.image = self.sprites[self.atual]

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.rect.inflate_ip(-30, -20)  # Reduz a área de colisão

        # Armas
        self.armas_ativas = [
            Arma("Espada", "Sprites/Armas/espada.png", 10),  # Arma inicial (Espada)
            Arma("Arco", "Sprites/Armas/arco.png", 8),  # Outra arma (Arco)
            Arma("Besta", "Sprites/Armas/besta.png", 12)  # Outra arma (Besta)
        ]

        self.arma_atual = self.armas_ativas[0]  # Começa com a primeira arma (Espada)

    def receber_dano(self, dano):
        """Método para reduzir a vida do jogador quando ele recebe dano."""
        self.vida.receber_dano(dano)
        if not self.vida.esta_vivo():
            print("Você morreu!")  # Aqui você pode adicionar a lógica de morte do jogador, reiniciar o jogo, etc.

    def update(self):
        """Atualiza a animação do jogador."""
        self.atual = (self.atual + 1) % len(self.sprites)
        self.image = self.sprites[self.atual]
        self.rect.center = (self.x, self.y)

    def mover(self, teclas, arvores):
        """Move o jogador com base nas teclas pressionadas."""
        dx = dy = 0

        if teclas[pygame.K_LEFT]:
            dx = -self.velocidade
        if teclas[pygame.K_RIGHT]:
            dx = self.velocidade
        if teclas[pygame.K_UP]:
            dy = -self.velocidade
        if teclas[pygame.K_DOWN]:
            dy = self.velocidade

        # Atualiza a posição do player
        self.x += dx
        self.y += dy

        self.rect.center = (self.x, self.y)

    def trocar_arma(self):
        """Alterna entre as armas da lista."""
        if len(self.armas_ativas) > 1:
            current_index = self.armas_ativas.index(self.arma_atual)
            self.arma_atual = self.armas_ativas[(current_index + 1) % len(self.armas_ativas)]

    def usar_arma(self, inimigo):
        """Usa a arma atual contra um inimigo."""
        if self.arma_atual.tipo == "melee":
            # Aplica o dano corpo a corpo
            if self.rect.colliderect(inimigo.rect):
                inimigo.receber_dano(self.arma_atual.dano)
                print(f"Usou {self.arma_atual.nome} e causou {self.arma_atual.dano} de dano!")
        elif self.arma_atual.tipo == "ranged":
            # Caso a arma seja de longo alcance, você pode lançar um projétil
            print(f"Usou {self.arma_atual.nome} para ataque à distância! ")

    def atacar(self, teclas, inimigos):
        """Verifica se a tecla de ataque foi pressionada e realiza o ataque."""
        if teclas[pygame.K_SPACE]:  # Quando pressionar a tecla espaço, atacar
            for inimigo in inimigos:  # Verifica todos os inimigos
                self.usar_arma(inimigo)
                self.empurrar_jogador(inimigo)

    def empurrar_jogador(self, inimigo):
        """Empurra o jogador para longe do inimigo ao colidir com ele."""
        if self.rect.colliderect(inimigo.rect):
            # Calcular direção oposta do inimigo para empurrar o jogador
            dx = self.rect.centerx - inimigo.rect.centerx
            dy = self.rect.centery - inimigo.rect.centery
            distancia = math.hypot(dx, dy)

            if distancia > 0:
                dx /= distancia
                dy /= distancia
                empurrar_forca = 15  # Intensidade do empurrão
                self.rect.x += dx * empurrar_forca
                self.rect.y += dy * empurrar_forca

    def desenhar_vida(self, tela, x, y):
        """Desenha a barra de vida do jogador."""
        self.vida.desenhar(tela, x, y)
