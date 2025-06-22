# Arquivo: Jogo/Arquivos/XP_Orb.py

import pygame
import math
import random

class XPOrb(pygame.sprite.Sprite):
    """
    Classe base para uma orbe de XP que pode ser coletada pelo jogador.
    Define a animação de pulsação e o tempo de vida.
    """
    def __init__(self, x, y, xp_value, cor_nucleo, cor_brilho, raio):
        super().__init__()

        self.xp_value = xp_value
        self.raio = raio
        self.tamanho_sprite = (raio * 2.5, raio * 2.5) # Área total para o brilho
        
        # Atributos para o efeito de pulsação
        self.cor_nucleo = cor_nucleo
        self.cor_brilho = cor_brilho
        self.tempo_animacao = pygame.time.get_ticks() + random.randint(0, 500) # Desfasa as animações
        self.frequencia_pulso = 0.003

        # Cria a superfície inicial e o rect
        self.image = pygame.Surface(self.tamanho_sprite, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

        # Atributos de controle
        self.duracao_maxima_ms = 20000 # Orbe dura 20 segundos antes de desaparecer
        self.tempo_criacao = pygame.time.get_ticks()

    def _desenhar_brilho(self):
        """
        Desenha a orbe com um efeito de brilho pulsante.
        """
        self.image.fill((0, 0, 0, 0)) # Limpa a superfície
        
        # Fator de pulsação (0 a 1)
        fator_pulso = (math.sin(self.tempo_animacao * self.frequencia_pulso) + 1) / 2
        
        raio_brilho_atual = self.raio + (self.raio * 0.5 * fator_pulso)
        alpha_brilho = 70 + (80 * fator_pulso)
        
        centro_surf = (self.tamanho_sprite[0] // 2, self.tamanho_sprite[1] // 2)

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
            self.raio
        )

    def update(self, dt_ms):
        """
        Atualiza a animação da orbe e verifica seu tempo de vida.
        """
        # Verifica se o tempo de vida expirou
        if pygame.time.get_ticks() - self.tempo_criacao > self.duracao_maxima_ms:
            self.kill()
            return
        
        # Atualiza a animação de pulsação
        self.tempo_animacao += dt_ms
        self._desenhar_brilho()

    def desenhar(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))


# --- Classes Específicas para cada tipo de Orbe ---

class XPOrbPequeno(XPOrb):
    """Orbe de 10 XP (Comum). Cor: Amarela."""
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y, 
            xp_value=10, 
            cor_nucleo=(255, 255, 150), 
            cor_brilho=(200, 180, 50), 
            raio=6
        )

class XPOrbMedio(XPOrb):
    """Orbe de 25 XP (Incomum). Cor: Azul."""
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y, 
            xp_value=25, 
            cor_nucleo=(180, 220, 255), 
            cor_brilho=(50, 120, 200), 
            raio=8
        )

class XPOrbGrande(XPOrb):
    """Orbe de 35 XP (Rara). Cor: Roxa."""
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y, 
            xp_value=35, 
            cor_nucleo=(240, 200, 255), 
            cor_brilho=(160, 80, 200), 
            raio=10
        )
