import pygame
import math

class ProjetilNeve(pygame.sprite.Sprite):
    """
    Representa um projétil de bola de neve que segue o jogador (teleguiado)
    e é compatível com a nova arquitetura do GerenciadorDeInimigos.
    """
    def __init__(self, x_origem, y_origem, alvo_obj, dano, velocidade=200, tamanho=10, cor=(200, 200, 255), cor_contorno=(0,0,0), largura_contorno=1):
        """
        Inicializa um novo projétil de neve teleguiado.

        Args:
            x_origem (int): A posição x inicial do projétil.
            y_origem (int): A posição y inicial do projétil.
            alvo_obj (pygame.sprite.Sprite): O objeto do jogador a ser seguido.
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
        self.alvo = alvo_obj # Armazena a referência do jogador
        self.dano = dano
        self.velocidade_magnitude = velocidade
        
        # Lógica de vida útil (o projétil se destrói sozinho após este tempo)
        self.duracao_maxima_ms = 7000 # Duração de 7 segundos para ter tempo de perseguir
        self.tempo_criacao = pygame.time.get_ticks()

    def update(self, dt_ms):
        """
        Atualiza a posição do projétil, recalculando a direção ao alvo a cada frame.
        O método agora só precisa de 'dt_ms' para funcionar.
        """
        agora = pygame.time.get_ticks()
        
        # Condições para o projétil ser destruído: alvo inválido ou tempo de vida expirado
        if not self.alvo or not self.alvo.esta_vivo() or (agora - self.tempo_criacao > self.duracao_maxima_ms):
            self.kill() # Remove o sprite de todos os grupos
            return

        # --- LÓGICA DE PERSEGUIÇÃO (HOMING) ---
        # 1. Calcula a direção para o alvo NESTE FRAME
        dx = self.alvo.rect.centerx - self.x
        dy = self.alvo.rect.centery - self.y
        distancia = math.hypot(dx, dy)

        # 2. Normaliza o vetor de direção para manter a velocidade constante
        if distancia > 0:
            direcao_x = dx / distancia
            direcao_y = dy / distancia
        else:
            # Se o projétil já alcançou o centro do alvo, ele não se move mais
            direcao_x, direcao_y = 0, 0

        # 3. Calcula o movimento com base no tempo (independente de FPS)
        fator_tempo_seg = dt_ms / 1000.0
        movimento_x = direcao_x * self.velocidade_magnitude * fator_tempo_seg
        movimento_y = direcao_y * self.velocidade_magnitude * fator_tempo_seg

        # 4. Aplica o movimento às coordenadas de ponto flutuante
        self.x += movimento_x
        self.y += movimento_y
        self.rect.center = (int(self.x), int(self.y))
        
    def desenhar(self, surface, camera_x, camera_y):
        """
        Desenha o projétil na tela, ajustado pela posição da câmera.
        """
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

