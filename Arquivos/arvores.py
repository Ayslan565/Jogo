import pygame
import random

class Arvore(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, estacao_inicial=0):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.rect = pygame.Rect(x, y, largura, altura)
        self.image = None
        self.estacao = estacao_inicial
        self.atualizar_sprite(self.estacao)

    def atualizar_sprite(self, nova_estacao):
        self.estacao = nova_estacao
        if self.estacao == 3:  # Inverno
            imagem_escolhida = random.choice([
                './Sprites/Arvore/Arvore_Inverno.png',
                'Sprites/Arvore/Carvalho_Inverno-.png'
            ])
        elif self.estacao == 1:  # Outono
            imagem_escolhida = random.choice([
                './Sprites/Arvore/Arvore_Outono.png',
                './Sprites/Arvore/Carvalho_Outono.png'
            ])
        elif self.estacao == 2:  # Primavera
            imagem_escolhida = random.choice([
                './Sprites/Arvore/Arvore.png',
                './Sprites/Arvore/Carvalho_Primavera.png'
            ])
        else:  # Verão
            imagem_escolhida = random.choice([
                './Sprites/Arvore/Arvore.png',
                './Sprites/Arvore/Carvalho_Verao-.png'
            ])
        try:
            self.image = pygame.image.load(imagem_escolhida).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.largura, self.altura))
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {imagem_escolhida}")
            self.image = pygame.Surface((self.largura, self.altura))
            self.image.fill((0, 255, 0))  # Cor fallback

    def desenhar(self, tela, camera_x=0, camera_y=0):
        pos_x = self.rect.x - camera_x
        pos_y = self.rect.y - camera_y
        tela.blit(self.image, (pos_x, pos_y))
