# Projetil_BolaNeve.py
import time
import pygame
import math # Importa math para cálculo de direção e distância

class ProjetilNeve(pygame.sprite.Sprite):
    """
    Representa um projétil de bola de neve atirado pelo Boneco de Neve.
    """
    def __init__(self, x_origem, y_origem, x_alvo, y_alvo, velocidade=5, tamanho=10, cor=(200, 200, 255)):
        """
        Inicializa um novo projétil de neve.

        Args:
            x_origem (int): A posição x inicial do projétil (geralmente a posição do inimigo).
            y_origem (int): A posição y inicial do projétil (geralmente a posição do inimigo).
            x_alvo (int): A posição x do alvo (geralmente a posição do jogador) no momento do disparo.
            y_alvo (int): A posição y do alvo (geralmente a posição do jogador) no momento do disparo.
            velocidade (float): A velocidade de movimento do projétil.
            tamanho (int): O raio do círculo que representa o projétil.
            cor (tuple): A cor do projétil (R, G, B).
        """
        super().__init__()

        self.tamanho = tamanho
        self.cor = cor
        self.image = pygame.Surface((self.tamanho * 2, self.tamanho * 2), pygame.SRCALPHA) # Cria uma superfície transparente
        pygame.draw.circle(self.image, self.cor, (self.tamanho, self.tamanho), self.tamanho) # Desenha um círculo na superfície

        self.rect = self.image.get_rect(center=(x_origem, y_origem)) # Posição inicial centrada na origem
        self.velocidade = velocidade

        # Calcula a direção para o alvo
        dx = x_alvo - x_origem
        dy = y_alvo - y_origem
        distancia = math.hypot(dx, dy)

        # Normaliza o vetor de direção e multiplica pela velocidade
        if distancia > 0:
            self.velocidade_x = (dx / distancia) * self.velocidade
            self.velocidade_y = (dy / distancia) * self.velocidade
        else:
            # Se a origem e o alvo forem os mesmos, o projétil não se move
            self.velocidade_x = 0
            self.velocidade_y = 0

        self.dano = 10 # Dano causado pelo projétil (ajuste conforme necessário)
        self.atingiu = False # Flag para saber se o projétil atingiu algo (jogador)
        self.tempo_criacao = time.time() # Tempo de criação para possível remoção por tempo
        self.vida_util = 5 # Tempo em segundos antes de o projétil desaparecer (ajuste)


    def update(self, player, tela_largura, tela_altura):
        """
        Atualiza a posição do projétil e verifica colisões.

        Args:
            player (Player): O objeto jogador para verificar colisão.
            tela_largura (int): Largura da tela para verificar limites.
            tela_altura (int): Altura da tela para verificar limites.
        """
        # Move o projétil
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y

        # Verifica colisão com o jogador (se o jogador estiver vivo e o projétil não tiver atingido nada ainda)
        # Adiciona verificação para garantir que o objeto player tem os atributos necessários
        if not self.atingiu and hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo():
            if self.rect.colliderect(player.rect):
                # Aplica dano ao jogador
                if hasattr(player, 'receber_dano'):
                    player.receber_dano(self.dano)
                    self.atingiu = True # Marca o projétil como tendo atingido
                    # print(f"DEBUG(ProjetilNeve): Projétil atingiu o jogador! Causou {self.dano} de dano.") # Debug
                else:
                     # print("DEBUG(ProjetilNeve): Objeto player não tem método 'receber_dano'.") # Debug
                     pass # Não faz nada se o player não puder receber dano


        # Remove o projétil se sair da tela ou se a vida útil acabar
        if self.rect.right < 0 or self.rect.left > tela_largura or \
           self.rect.bottom < 0 or self.rect.top > tela_altura or \
           self.atingiu or (time.time() - self.tempo_criacao > self.vida_util):
            self.kill() # Remove o sprite do grupo (se estiver usando grupos)
            # print("DEBUG(ProjetilNeve): Projétil removido (fora da tela, atingiu alvo ou vida útil expirou).") # Debug


    def desenhar(self, surface, camera_x, camera_y):
        """
        Desenha o projétil na superfície, aplicando o offset da câmera.

        Args:
            surface (pygame.Surface): A superfície onde desenhar.
            camera_x (int): O offset x da câmera.
            camera_y (int): O offset y da câmera.
        """
        # Desenha o projétil com o offset da câmera
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
