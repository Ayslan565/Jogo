import pygame
import random
import math
from inimigos import Inimigo

class fantasma(Inimigo):
    def __init__(self, velocidade=1.5):
        sprite_paths = [
            "Sprites\\Fantasma\\Fantasma1.png", "Sprites\\Fantasma\\Fantasma2.png", 
            "Sprites\\Fantasma\\Fantasma3.png", "Sprites\\Fantasma\\Fantasma4.png", 
            "Sprites\\Fantasma\\Fantasma5.png", "Sprites\\Fantasma\\Fantasma6.png", 
            "Sprites\\Fantasma\\Fantasma8.png", "Sprites\\Fantasma\\Fantasma9.png"
        ]
        super().__init__(velocidade, sprite_paths)
        self.hp = 100  # Pontos de vida do Fantasma

    def mover_em_direcao(self, alvo_x, alvo_y):
        dx = alvo_x - self.rect.centerx
        dy = alvo_y - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia
            self.rect.x += dx * self.velocidade
            self.rect.y += dy * self.velocidade - 0.5  # Pequena variação para dar mais fluidez ao movimento

    def verificar_colisao(self, player):
        """Verifica colisão com o jogador."""
        return self.rect.colliderect(player.rect)

    def update(self, player_rect):
        """Atualiza o inimigo com base no movimento do jogador."""
        self.mover_em_direcao(player_rect.centerx, player_rect.centery)
        self.atualizar_animacao()

    def atacar(self, player):
        """Quando o fantasma colide com o jogador, ele causa dano e empurra o jogador."""
        if self.rect.colliderect(player.rect):
            dano = 10  # Definindo um valor de dano
            print("Fantasma atacou o jogador!")

            # Causando dano no jogador
            player.receber_dano(dano)

            # Empurrando o jogador para longe do fantasma
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distancia = math.hypot(dx, dy)

            if distancia > 0:
                dx /= distancia
                dy /= distancia
                empurrar_forca = 15  # Intensidade do empurrão
                player.rect.x += dx * empurrar_forca
                player.rect.y += dy * empurrar_forca

    