# Projetil_BolaNeve.py
import time
import pygame
import math # Importa math para cálculo de direção e distância

class ProjetilNeve(pygame.sprite.Sprite):
    """
    Representa um projétil de bola de neve atirado pelo Boneco de Neve.
    """
    def __init__(self, x_origem, y_origem, x_alvo, y_alvo, dano, velocidade=5, tamanho=10, cor=(200, 200, 255), cor_contorno=(0,0,0), largura_contorno=1):
        """
        Inicializa um novo projétil de neve.

        Args:
            x_origem (int): A posição x inicial do projétil.
            y_origem (int): A posição y inicial do projétil.
            x_alvo (int): A posição x do alvo.
            y_alvo (int): A posição y do alvo.
            dano (int): O dano que o projétil causará.
            velocidade (float): A velocidade de movimento do projétil.
            tamanho (int): O raio do círculo que representa o projétil.
            cor (tuple): A cor do projétil (R, G, B).
            cor_contorno (tuple): A cor do contorno do projétil (R, G, B).
            largura_contorno (int): A largura da linha do contorno.
        """
        super().__init__()

        self.tamanho = tamanho
        self.cor = cor
        self.cor_contorno = cor_contorno
        self.largura_contorno = largura_contorno

        diametro_total = self.tamanho * 2
        self.image = pygame.Surface((diametro_total, diametro_total), pygame.SRCALPHA) 
        
        pygame.draw.circle(self.image, self.cor, (self.tamanho, self.tamanho), self.tamanho) 
        
        if self.largura_contorno > 0:
            pygame.draw.circle(self.image, self.cor_contorno, (self.tamanho, self.tamanho), self.tamanho, self.largura_contorno)

        self.rect = self.image.get_rect(center=(x_origem, y_origem)) 
        self.velocidade_magnitude = velocidade 
        self.dano = dano 

        dx = x_alvo - x_origem
        dy = y_alvo - y_origem
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            self.velocidade_x = (dx / distancia) * self.velocidade_magnitude
            self.velocidade_y = (dy / distancia) * self.velocidade_magnitude
        else:
            self.velocidade_x = 0
            self.velocidade_y = -self.velocidade_magnitude 

        self.atingiu = False 
        self.tempo_criacao = time.time() 
        self.vida_util = 5 
        self.alive = True 


    def update(self, player, tela_largura, tela_altura, dt_ms=None): 
        """
        Atualiza a posição do projétil e verifica colisões.
        """
        if not self.alive:
            return

        fator_tempo = 1.0
        if dt_ms is not None and dt_ms > 0:
            fator_tempo = (dt_ms / (1000.0 / 60.0)) 


        self.rect.x += self.velocidade_x * fator_tempo
        self.rect.y += self.velocidade_y * fator_tempo

        if not self.atingiu and hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo():
            if self.rect.colliderect(player.rect):
                if hasattr(player, 'receber_dano'):
                    player.receber_dano(self.dano)
                    self.atingiu = True 
                else:
                    print("DEBUG(ProjetilNeve): Objeto player não tem método 'receber_dano'.")
        
        if self.rect.right < 0 or self.rect.left > tela_largura or \
           self.rect.bottom < 0 or self.rect.top > tela_altura or \
           self.atingiu or (time.time() - self.tempo_criacao > self.vida_util):
            self.kill() 
            self.alive = False 


    def desenhar(self, surface, camera_x, camera_y):
        """
        Desenha o projétil na superfície, aplicando o offset da câmera.
        """
        if self.alive:
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
