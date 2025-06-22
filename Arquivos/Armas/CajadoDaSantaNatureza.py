import pygame
import os
import math # Importa o módulo math para calcular distâncias
from .weapon import Weapon
from .FolhaCortanteProjectile import FolhaCortanteProjectile

class CajadoDaSantaNatureza(Weapon):
    """
    Cajado mágico que dispara projéteis de Folha Cortante no inimigo mais próximo.
    """
    def __init__(self):
        # --- Constrói o caminho para a imagem de forma robusta ---
        caminho_icone = None
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            caminho_icone = os.path.join("Sprites", "Armas", "CajadoNatureza", "cajado.png")
        except Exception:
            caminho_icone = None

        # --- Chama o inicializador da classe base 'Weapon' ---
        super().__init__(
            name="Cajado da Santa Natureza",
            damage=22.0,
            attack_range=700.0,
            cooldown=1.0 / 1.5,
            description="Um cajado que canaliza a fúria da floresta.",
            rarity="Rara",
            weapon_type="Cajado", # Importante para a lógica do jogador
            element="Natureza",
            ui_icon_path=caminho_icone
        )
        self.last_shot_time = 0

    def can_attack(self):
        """Verifica se a arma pode atacar com base no cooldown."""
        return pygame.time.get_ticks() - self.last_shot_time >= (self.cooldown * 1000)

    # --- MÉTODO DE ATAQUE ATUALIZADO ---
    def attack(self, player, inimigos_lista):
        """
        Encontra o inimigo mais próximo e cria um projétil na direção dele.
        Agora recebe a lista de inimigos em vez da posição do mouse.
        """
        if self.can_attack():
            self.last_shot_time = pygame.time.get_ticks()
            
            inimigo_mais_proximo = None
            menor_distancia = float('inf')

            # 1. Encontra o inimigo mais próximo do jogador
            for inimigo in inimigos_lista:
                distancia = math.hypot(player.rect.centerx - inimigo.rect.centerx, 
                                      player.rect.centery - inimigo.rect.centery)
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    inimigo_mais_proximo = inimigo
            
            # 2. Se um inimigo foi encontrado, ataca na direção dele
            if inimigo_mais_proximo:
                alvo_pos = inimigo_mais_proximo.rect.center
                # Cria o projétil passando a posição do alvo
                return FolhaCortanteProjectile(player.rect.centerx, player.rect.centery, alvo_pos[0], alvo_pos[1])

        return None
