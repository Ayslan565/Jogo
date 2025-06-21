import pygame
import math
import os

class ProjetilMaga(pygame.sprite.Sprite):
    """
    Representa um projétil de energia roxa que segue o jogador (teleguiado)
    e pulsa com um brilho.
    """
    tamanho_sprite_definido = (40, 40) 

    def __init__(self, x_origem, y_origem, alvo_obj, dano, velocidade):
        """
        Inicializa um novo projétil de energia teleguiado.

        Args:
            x_origem (int): A posição x inicial do projétil.
            y_origem (int): A posição y inicial do projétil.
            alvo_obj (pygame.sprite.Sprite): O objeto do jogador a ser seguido.
            dano (int): O dano que o projétil causará.
            velocidade (float): A velocidade de movimento em pixels por segundo.
        """
        super().__init__()

        self.x = float(x_origem)
        self.y = float(y_origem)
        
        # --- Atributos para o Efeito Visual de Brilho ---
        self.raio_nucleo = 7
        self.raio_brilho_max = 18
        self.cor_nucleo = (230, 200, 255) # Roxo bem claro, quase branco
        self.cor_brilho = (150, 80, 220)  # Roxo para o brilho
        
        self.tempo_animacao = pygame.time.get_ticks()
        self.frequencia_pulso = 0.005 # Controla a velocidade da pulsação

        # Cria a superfície para desenhar o efeito
        self.image = pygame.Surface(self.tamanho_sprite_definido, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        
        # --- Atributos de Combate e de Vida ---
        self.alvo = alvo_obj # Armazena a referência do jogador
        self.dano = dano
        self.velocidade_magnitude = velocidade
        
        # Lógica de vida útil: projétil dura 5 segundos
        self.duracao_maxima_ms = 5000 
        self.tempo_criacao = pygame.time.get_ticks()

    def _desenhar_brilho(self):
        """
        Desenha a bola de energia com um efeito de brilho que pulsa.
        """
        self.image.fill((0, 0, 0, 0)) # Limpa a superfície para redesenhar
        
        fator_pulso = (math.sin(self.tempo_animacao * self.frequencia_pulso) + 1) / 2
        
        raio_brilho_atual = self.raio_nucleo + (self.raio_brilho_max - self.raio_nucleo) * fator_pulso
        alpha_brilho = 50 + (100 * fator_pulso)
        
        centro_surf = (self.tamanho_sprite_definido[0] // 2, self.tamanho_sprite_definido[1] // 2)

        # Desenha o brilho externo
        pygame.draw.circle(
            self.image,
            (*self.cor_brilho, int(alpha_brilho)),
            centro_surf,
            int(raio_brilho_atual)
        )
        # Desenha o núcleo interno
        pygame.draw.circle(
            self.image,
            self.cor_nucleo,
            centro_surf,
            self.raio_nucleo
        )

    def update(self, dt_ms):
        """
        Atualiza a posição (seguindo o alvo) e a animação de pulsação do projétil.
        """
        agora = pygame.time.get_ticks()
        # Se o alvo não existe, morreu, ou se o tempo de vida acabou, o projétil se destrói.
        if not self.alvo or not self.alvo.esta_vivo() or (agora - self.tempo_criacao > self.duracao_maxima_ms):
            self.kill()
            return

        # --- LÓGICA DE PERSEGUIÇÃO (HOMING) ---
        dx = self.alvo.rect.centerx - self.x
        dy = self.alvo.rect.centery - self.y
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            direcao_x = dx / distancia
            direcao_y = dy / distancia
        else:
            direcao_x, direcao_y = 0, 0

        # Calcula e aplica o movimento
        fator_tempo_seg = dt_ms / 1000.0
        movimento_x = direcao_x * self.velocidade_magnitude * fator_tempo_seg
        movimento_y = direcao_y * self.velocidade_magnitude * fator_tempo_seg

        self.x += movimento_x
        self.y += movimento_y
        self.rect.center = (int(self.x), int(self.y))

        # Atualiza o efeito visual
        self.tempo_animacao += dt_ms
        self._desenhar_brilho()

    def desenhar(self, janela, camera_x, camera_y):
        janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
