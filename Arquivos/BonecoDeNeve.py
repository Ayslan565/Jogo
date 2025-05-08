import pygame
import random
import math
from inimigos import Inimigo
import pygame

class BonecoDeNeve(Inimigo):
    def __init__(self, x, y):
        sprite_paths = [
            "Sprites\\BonecoDeNeve\\BonecoDeNeve1.png", "Sprites\\BonecoDeNeve\\BonecoDeNeve2.png",
            "Sprites\\BonecoDeNeve\\BonecoDeNeve3.png", "Sprites\\BonecoDeNeve\\BonecoDeNeve4.png"
        ]
        super().__init__(x, y, sprite_paths)
        self.hp = 100  # Pontos de vida do Boneco de Neve

    def mover_em_direcao(self, alvo_x, alvo_y):
        dx = alvo_x - self.rect.centerx
        dy = alvo_y - self.rect.centery
        distancia = pygame.math.Vector2(dx, dy).length()

        if distancia > 0:
            dx /= distancia
            dy /= distancia
            self.rect.x += dx * self.velocidade
            self.rect.y += dy * self.velocidade - 0.5  # Pequena variação para dar mais fluidez ao movimento

    def update(self, player_rect):
        self.mover_em_direcao(player_rect.centerx, player_rect.centery)
        self.atualizar_animacao()
