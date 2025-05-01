import pygame
import random


class Vendedor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("vendedor.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)