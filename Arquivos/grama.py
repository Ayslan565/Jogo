import pygame
import random

class Grama(pygame.sprite.Sprite):
    # Lista de caminhos dos sprites
    imagens_grama = [
        pygame.transform.scale(pygame.image.load('Sprites\\mato\\Mato_1.png'), (50, 50)),
        pygame.transform.scale(pygame.image.load('Sprites\\mato\\Mato_2.png'), (50, 50)),
    ]

    def __init__(self, x, y, largura=50, altura=50):
        super().__init__()

        # Escolhe aleatoriamente uma imagem de grama e redimensiona
        imagem_original = random.choice(self.imagens_grama)
        self.image = pygame.transform.scale(imagem_original, (largura, altura))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.colisao_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height)

    def desenhar(self, tela, camera_x=0, camera_y=0):
        pos_x = self.rect.x - camera_x
        pos_y = self.rect.y - camera_y
        tela.blit(self.image, (pos_x, pos_y))

    def verificar_colisao(self, jogador):
        return self.colisao_rect.colliderect(jogador.rect)
