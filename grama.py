import pygame
import random

class Grama(pygame.sprite.Sprite):
    # Lista de caminhos dos sprites
    imagens_grama = [
        pygame.image.load('Sprites\mato\Mato_1.png'),
        pygame.image.load('Sprites\mato\Mato_2.png'),
    ]

    def __init__(self, x, y, largura=50, altura=50):
        super().__init__()

        # Escolhe aleatoriamente uma imagem de grama e redimensiona
        imagem_original = random.choice(self.imagens_grama)
        self.image = pygame.transform.scale(imagem_original, (largura, altura))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.colisao_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height)

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

    def verificar_colisao(self, jogador):
        return self.colisao_rect.colliderect(jogador.rect)
