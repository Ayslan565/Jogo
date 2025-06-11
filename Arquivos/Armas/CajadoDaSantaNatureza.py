# Jogo/Arquivos/Armas/CajadoDaSantaNatureza.py

import pygame
import os
from .weapon import Weapon  # Herda diretamente da classe base principal
from .FolhaCortanteProjectile import FolhaCortanteProjectile

class CajadoDaSantaNatureza(Weapon):
    """
    Cajado mágico que dispara projéteis de Folha Cortante.
    Versão corrigida para herdar de Weapon e inicializar corretamente.
    """
    def __init__(self):
        # --- Constrói o caminho para a imagem de forma robusta ---
        caminho_icone = None
        try:
            # Sobe na estrutura de pastas para encontrar a raiz do projeto (Jogo)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            caminho_icone = os.path.join("Sprites", "Armas", "CajadoNatureza", "cajado.png")
            # Validação extra do caminho completo para debug, se necessário
            # full_path_validation = os.path.join(project_root, caminho_icone)
            # if not os.path.exists(full_path_validation):
            #     print(f"AVISO: Ícone para CajadoDaSantaNatureza não encontrado em {full_path_validation}")
        except Exception:
             # Em caso de erro ao construir o caminho, ele permanecerá None
            caminho_icone = None

        # --- Chama o inicializador da classe base 'Weapon' com todos os parâmetros ---
        super().__init__(
            name="Cajado da Santa Natureza",
            damage=22.0,            # Dano base do projétil
            attack_range=700.0,     # Alcance para o jogador poder atirar
            cooldown=1.0 / 1.5,     # Cooldown em segundos (convertido de attack_speed)
            description="Um cajado que canaliza a fúria da floresta.",
            rarity="Rara",
            weapon_type="Cajado",
            element="Natureza",
            ui_icon_path=caminho_icone # Passa o caminho relativo para a classe base
        )

        # A classe Weapon já cuida do carregamento do ícone.
        # Estes atributos são para a lógica específica de ataque deste cajado.
        self.last_shot_time = 0

    def can_attack(self):
        """Verifica se a arma pode atacar com base no cooldown."""
        return pygame.time.get_ticks() - self.last_shot_time >= (self.cooldown * 1000)

    def attack(self, player, mouse_pos):
        """
        Cria e retorna um projétil de Folha Cortante se o cooldown permitir.
        Este método é chamado pelo loop principal do jogo.
        """
        if self.can_attack():
            self.last_shot_time = pygame.time.get_ticks()
            # O projétil usará o dano definido nos atributos da arma (self.damage)
            return FolhaCortanteProjectile(player.rect.centerx, player.rect.centery, mouse_pos[0], mouse_pos[1])
        return None