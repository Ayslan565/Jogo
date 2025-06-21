import pygame
import random
import math

from arvores import Arvore
from grama import Grama

class GeradorPlantas:
    def __init__(self, all_sprites, arvores, grama, player):
        """
        Inicializa o gerador de plantas.

        Args:
            all_sprites (pygame.sprite.Group): Grupo principal de sprites.
            arvores (pygame.sprite.Group): Grupo de sprites de árvores.
            grama (pygame.sprite.Group): Grupo de sprites de grama.
            player (Player): O objeto do jogador.
        """
        self.all_sprites = all_sprites
        self.arvores = arvores
        self.grama = grama
        self.player = player
        # --- MUDANÇA: O raio de spawn agora é a distância MÍNIMA de geração ---
        self.spawn_radius = 900  # Aumentado para garantir que nasça fora da tela

        # Gera 100 árvores iniciais em um círculo ao redor da posição inicial (0,0).
        for _ in range(100):
            angle = random.uniform(0, 2 * math.pi)
            # --- MUDANÇA: Aumenta a distância mínima das árvores iniciais ---
            # Gera as árvores a uma distância entre 900 e 2500 pixels do centro.
            distance = random.uniform(self.spawn_radius, 2500)
            x = distance * math.cos(angle)
            y = distance * math.sin(angle)
            
            arvore = Arvore(x, y, 180, 180)
            self.all_sprites.add(arvore)
            self.arvores.add(arvore)

    def update(self):
        """
        Atualiza o gerador, criando novas plantas ao redor do jogador em movimento.
        As plantas são geradas fora da tela para dar a impressão de um mundo contínuo.
        """
        # --- MUDANÇA: Reduz a frequência de geração para evitar excesso de plantas ---
        # Gera novas plantas com uma chance menor para não sobrecarregar.
        if random.randint(1, 10) == 1:
            player_x, player_y = self.player.rect.center
            rand_angle = random.uniform(0, 2 * math.pi)
            
            # --- MUDANÇA: Gera plantas mais longe do jogador ---
            # As plantas nascerão entre 900 e 1300 pixels de distância.
            rand_dist = random.uniform(self.spawn_radius, self.spawn_radius + 400)
            
            x = player_x + rand_dist * math.cos(rand_angle)
            y = player_y + rand_dist * math.sin(rand_angle)

            tipo_planta = random.choice(['arvore', 'grama', 'grama', 'grama'])

            if tipo_planta == 'arvore':
                if len(self.arvores) < 250:
                    arvore = Arvore(x, y, 180, 180)
                    self.all_sprites.add(arvore)
                    self.arvores.add(arvore)
            elif tipo_planta == 'grama':
                if len(self.grama) < 400:
                    folha = Grama(x, y, 50, 50)
                    self.all_sprites.add(folha)
                    self.grama.add(folha)
