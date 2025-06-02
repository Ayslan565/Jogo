import pygame

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade, dano):
        super().__init__()
        self.image = pygame.image.load('sprites/projetil.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = velocidade
        self.dano = dano

    def atualizar(self):
        self.rect.x += self.velocidade
        if self.rect.right < 0 or self.rect.left > 1920:
            self.kill()

    def colisao(self, inimigos):
        for inimigo in inimigos:
            if self.rect.colliderect(inimigo.rect):
                inimigo.receber_dano(self.dano)
                self.kill()
