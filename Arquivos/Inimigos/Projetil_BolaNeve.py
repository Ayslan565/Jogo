import pygame
import math

class ProjetilNeve(pygame.sprite.Sprite):
    """
    Representa um projétil de bola de neve que viaja em linha reta.
    """
    def __init__(self, x_origem, y_origem, x_alvo, y_alvo, dano, velocidade=200, tamanho=10, cor=(200, 200, 255), cor_contorno=(0,0,0), largura_contorno=1):
        """
        Inicializa um novo projétil de neve de tiro reto.

        Args:
            x_origem (int): A posição x inicial do projétil.
            y_origem (int): A posição y inicial do projétil.
            x_alvo (int): A coordenada x do alvo no momento do disparo.
            y_alvo (int): A coordenada y do alvo no momento do disparo.
            dano (int): O dano que o projétil causará.
            velocidade (float): A velocidade de movimento em pixels por segundo.
            tamanho (int): O raio do círculo que representa o projétil.
        """
        super().__init__()

        self.tamanho = tamanho
        
        # Cria a imagem do projétil
        diametro_total = self.tamanho * 2
        self.image = pygame.Surface((diametro_total, diametro_total), pygame.SRCALPHA)
        pygame.draw.circle(self.image, cor, (self.tamanho, self.tamanho), self.tamanho)
        if largura_contorno > 0:
            pygame.draw.circle(self.image, cor_contorno, (self.tamanho, self.tamanho), self.tamanho, largura_contorno)

        # Atributos de posição e movimento
        self.x = float(x_origem)
        self.y = float(y_origem)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # Atributos de combate e de vida
        self.dano = dano
        self.velocidade_magnitude = velocidade
        
        # --- CÁLCULO DE DIREÇÃO FIXA ---
        # A direção é calculada uma vez e não muda mais.
        dx = x_alvo - self.x
        dy = y_alvo - self.y
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            self.direcao_x = dx / distancia
            self.direcao_y = dy / distancia
        else:
            self.direcao_x = 0
            self.direcao_y = -1 # Padrão para atirar para cima se o alvo estiver na mesma posição
        
        # Lógica de vida útil (o projétil se destrói sozinho após este tempo)
        self.duracao_maxima_ms = 7000 
        self.tempo_criacao = pygame.time.get_ticks()

    def update(self, dt_ms):
        """
        Atualiza a posição do projétil em sua trajetória linear.
        """
        agora = pygame.time.get_ticks()
        
        # O projétil é destruído apenas se seu tempo de vida expirar.
        if (agora - self.tempo_criacao > self.duracao_maxima_ms):
            self.kill() 
            return

        # --- LÓGICA DE MOVIMENTO EM LINHA RETA ---
        fator_tempo_seg = dt_ms / 1000.0
        movimento_x = self.direcao_x * self.velocidade_magnitude * fator_tempo_seg
        movimento_y = self.direcao_y * self.velocidade_magnitude * fator_tempo_seg

        self.x += movimento_x
        self.y += movimento_y
        self.rect.center = (int(self.x), int(self.y))
        
    def desenhar(self, surface, camera_x, camera_y):
        """
        Desenha o projétil na tela, ajustado pela posição da câmera.
        """
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

