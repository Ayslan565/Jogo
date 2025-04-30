import pygame
import random

class Arvore(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()

        # Lista com os caminhos das imagens
        imagens = ['sprites/Arvore/arvore.png', 'sprites/Arvore/Arvore1.png']

        # Escolhe aleatoriamente uma das imagens
        imagem_escolhida = random.choice(imagens)

        # Carrega a imagem escolhida
        self.image = pygame.image.load(imagem_escolhida)

        # Redimensiona a imagem
        self.image = pygame.transform.scale(self.image, (180, 180))  # Aumentando a árvore
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def desenhar(self, tela):
        # Desenha a imagem na tela
        tela.blit(self.image, self.rect)

    def verificar_colisao(self, player):
        from player import Player  # Importação movida para dentro do método
        self.atualizar_colisao()  # Atualiza a colisão com o jogador
        return self.colisao_rect.colliderect(player.rect)  # Verifica colisão com o rect do jogador
