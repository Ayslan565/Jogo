import pygame

class Arma(pygame.sprite.Sprite):
    def __init__(self, nome, imagem_path, dano, tipo='melee'):
        super().__init__()
        self.nome = nome
        self.image = pygame.image.load(imagem_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.dano = dano
        self.tipo = tipo
