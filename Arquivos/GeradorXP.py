# Arquivo: Jogo/Arquivos/GeradorXP.py
import pygame
import random
import math

# Tenta importar as classes de Orbe de XP.
try:
    from XPs_Orb import XPOrbPequeno, XPOrbMedio, XPOrbGrande
except ImportError:
    print("ERRO CRÍTICO (GeradorXP.py): Não foi possível encontrar 'XP_Orb.py'.")
    # Define classes placeholder para evitar que o jogo trave.
    class XPOrbPequeno(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.rect = pygame.Rect(x,y,12,12)
            self.xp_value = 10
        def update(self, dt_ms): self.kill()
        def desenhar(self, s, cx, cy): pass
            
    class XPOrbMedio(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.rect = pygame.Rect(x,y,16,16)
            self.xp_value = 25
        def update(self, dt_ms): self.kill()
        def desenhar(self, s, cx, cy): pass

    class XPOrbGrande(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.rect = pygame.Rect(x,y,20,20)
            self.xp_value = 35
        def update(self, dt_ms): self.kill()
        def desenhar(self, s, cx, cy): pass


class GeradorXP:
    """
    Responsável por criar e gerir as orbes de XP que aparecem no mapa.
    """
    def __init__(self, limite_orbes=1005, intervalo_spawn_ms=4000):
        """
        Inicializa o gerador de orbes de XP.

        Args:
            limite_orbes (int): O número máximo de orbes que podem existir no mapa ao mesmo tempo.
            intervalo_spawn_ms (int): O tempo em milissegundos entre as tentativas de criar uma nova orbe.
        """
        self.orbes = pygame.sprite.Group()
        self.limite_orbes = limite_orbes
        self.intervalo_spawn_ms = intervalo_spawn_ms
        self.ultimo_spawn = pygame.time.get_ticks()

        # Define as chances de cada tipo de orbe aparecer.
        self.tipos_de_orbe = [
            (XPOrbPequeno, 70),  # 70% de chance para a orbe comum (10 XP)
            (XPOrbMedio, 25),   # 25% de chance para a orbe incomum (25 XP)
            (XPOrbGrande, 5)    # 5% de chance para a orbe rara (35 XP)
        ]
        # Separa as classes e os pesos para usar com random.choices
        self.classes_orbes, self.pesos_orbes = zip(*self.tipos_de_orbe)

    def _escolher_tipo_orbe(self):
        """Escolhe um tipo de orbe com base nas probabilidades definidas."""
        return random.choices(self.classes_orbes, weights=self.pesos_orbes, k=1)[0]

    def tentar_gerar_orbe(self, jogador_rect):
        """
        Verifica se é hora de criar uma nova orbe e, se for, cria-a em
        uma posição aleatória perto do jogador, mas fora da tela.
        """
        agora = pygame.time.get_ticks()
        
        if (agora - self.ultimo_spawn > self.intervalo_spawn_ms) and (len(self.orbes) < self.limite_orbes):
            self.ultimo_spawn = agora

            # Define uma distância de spawn para que a orbe apareça fora da visão do jogador
            distancia_min = 500
            distancia_max = 1200

            angulo = random.uniform(0, 2 * math.pi)
            distancia = random.uniform(distancia_min, distancia_max)

            # Calcula a posição de spawn em relação ao centro do jogador
            x = jogador_rect.centerx + distancia * math.cos(angulo)
            y = jogador_rect.centery + distancia * math.sin(angulo)

            ClasseOrbe = self._escolher_tipo_orbe()
            
            nova_orbe = ClasseOrbe(x, y)
            self.orbes.add(nova_orbe)

    def update(self, dt_ms):
        """Atualiza todas as orbes ativas (animação, tempo de vida, etc.)."""
        self.orbes.update(dt_ms)
