import pygame

class Vida:
    def __init__(self, vida_maxima=100, vida_atual=None):
        """Inicializa a vida do jogador."""
        self.vida_maxima = vida_maxima
        self.vida_atual = vida_atual if vida_atual is not None else vida_maxima

        # Sprites para cada parte da vida
        self.sprites = [
            pygame.transform.scale(pygame.image.load("Sprites/vida/Vida 6-6.png"), (250, 250)),
            pygame.transform.scale(pygame.image.load("Sprites/vida/Vida 5-6.png"), (250, 250)),
            pygame.transform.scale(pygame.image.load("Sprites/vida/Vida 4-6.png"), (250, 250)),
            pygame.transform.scale(pygame.image.load("Sprites/vida/Vida 3-6.png"), (250, 250)),
            pygame.transform.scale(pygame.image.load("Sprites/vida/Vida 2-6.png"), (250, 250)),
            pygame.transform.scale(pygame.image.load("Sprites/vida/Vida 1-6.png"), (250, 250)),
            pygame.transform.scale(pygame.image.load("Sprites/vida/Vida 0-6.png"), (250, 250)),
        ]

    def receber_dano(self, dano):
        """Diminui a vida do jogador quando recebe dano."""
        self.vida_atual -= dano
        if self.vida_atual < 0:
            self.vida_atual = 0  # A vida não pode ser negativa

    def curar(self, quantidade):
        """Recupera vida do jogador."""
        self.vida_atual += quantidade
        if self.vida_atual > self.vida_maxima:
            self.vida_atual = self.vida_maxima  # A vida não pode ultrapassar o máximo

    def esta_vivo(self):
        """Verifica se o jogador está vivo."""
        return self.vida_atual > 0

    def desenhar(self, tela, x, y):
        """Desenha a vida dividida em sprites."""
        # Determina qual sprite usar com base na vida
        if self.vida_atual >= self.vida_maxima:
            sprite = self.sprites[0]  # Vida cheia
        elif self.vida_atual >= self.vida_maxima * 5 / 6:
            sprite = self.sprites[1]  # Vida 1.0
        elif self.vida_atual >= self.vida_maxima * 2 / 3:
            sprite = self.sprites[2]  # Vida 0.5
        elif self.vida_atual >= self.vida_maxima / 2:
            sprite = self.sprites[3]  # Vida 1.0
        elif self.vida_atual >= self.vida_maxima / 3:
            sprite = self.sprites[4]  # Vida 0.5
        elif self.vida_atual >= self.vida_maxima / 6:
            sprite = self.sprites[5]  # Vida 0.25
        else:
            sprite = self.sprites[6]  # Vida 0.0

        # Desenha o sprite correspondente
        tela.blit(sprite, (x, y))  # Desenha o sprite da vida

    def __str__(self):
        return f"Vida: {self.vida_atual}/{self.vida_maxima}"

