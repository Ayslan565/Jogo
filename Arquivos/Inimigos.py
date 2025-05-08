import pygame

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path):
        super().__init__()
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))  # Ajuste o tamanho conforme necessário
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = 2

    def mover_em_direcao(self, alvo_x, alvo_y):
        dx = alvo_x - self.rect.centerx
        dy = alvo_y - self.rect.centery
        distancia = pygame.math.Vector2(dx, dy).length()

        if distancia > 0:
            dx /= distancia
            dy /= distancia
            self.rect.x += dx * self.velocidade
            self.rect.y += dy * self.velocidade

    def atualizar(self, jogador_rect):
        self.mover_em_direcao(jogador_rect.centerx, jogador_rect.centery)

    def desenhar(self, janela, camera_x, camera_y):
        janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
