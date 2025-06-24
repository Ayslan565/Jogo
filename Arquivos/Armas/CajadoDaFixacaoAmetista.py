import pygame
import os
import math
from .weapon import Weapon
from .AmetistaProjectile import AmetistaProjectile 

class CajadoDaFixacaoAmetista(Weapon):
    """
    Cajado mágico que dispara projéteis de Ametista que perseguem o inimigo mais próximo.
    Agora com sistema de níveis para fácil expansão.
    """
    def __init__(self):
        self._base_name = "Cajado da Fixacao Ametista"
        self.level = 1.0  # Nível inicial da arma
        self.price = 250  # Preço base na loja

        # --- DADOS DE PROGRESSÃO POR NÍVEL (Estrutura adaptada da EspadaCaida) ---
        self._stats_by_level = {
            1.0: {
                "damage": 25.0,
                "attack_range": 750.0,
                "cooldown": 1.0 / 1.8,
                "name_suffix": "",
                "ui_icon": "Sprites\Armas\Armas Magicas\Cajado da Fixacao Ametista\E1.png",
                "description": "Um cajado que dispara cristais de pura energia arcana que perseguem os inimigos."
            },
            2.0: {
                "damage": 35.0,
                "attack_range": 800.0,
                "cooldown": 1.0 / 2.0,
                "name_suffix": "Potencializado",
                "ui_icon": "Sprites\Armas\Armas Magicas\Cajado da Fixacao Ametista\E1.png",
                "description": "O cajado agora pulsa com um poder arcano ainda maior."
            },
            3.0: {
                "damage": 45.0,
                "attack_range": 850.0,
                "cooldown": 1.0 / 2.5,
                "name_suffix": " da Supremacia",
                "ui_icon": "Sprites\Armas\Armas Magicas\Cajado da Fixacao Ametista\E1.png",
                "description": "O cajado agora emite uma aura de poder que aumenta a velocidade de ataque."
            }
        }
        
        # Inicializa a classe base com os stats do nível 1
        initial_stats = self._get_stats_for_level_internal(1.0)
        super().__init__(
            name=self._base_name,
            damage=initial_stats.get("damage"),
            attack_range=initial_stats.get("attack_range"),
            cooldown=initial_stats.get("cooldown"),
            description=initial_stats.get("description"),
            rarity="Épica",
            weapon_type="Cajado",
            element="Arcano",
            ui_icon_path=initial_stats.get("ui_icon")
        )

        self.last_shot_time = 0
        # Aplica os status para garantir que tudo esteja configurado corretamente
        self._apply_level_stats()

    def _get_stats_for_level_internal(self, level_to_check):
        """Busca o dicionário de status para um determinado nível."""
        # Retorna os stats do nível especificado, ou do primeiro nível se não for encontrado
        return self._stats_by_level.get(level_to_check, self._stats_by_level.get(1.0))

    def _apply_level_stats(self):
        """Aplica os atributos do nível atual à instância da arma."""
        stats = self._get_stats_for_level_internal(self.level)
        if not stats: return

        # Atualiza os atributos da arma
        self.damage = stats.get("damage", self.damage)
        self.attack_range = stats.get("attack_range", self.attack_range)
        self.cooldown = stats.get("cooldown", self.cooldown)
        self.description = stats.get("description", self.description)
        
        # Atualiza o nome completo
        suffix = stats.get('name_suffix', '')
        self.name = f"{self._base_name} {suffix}".strip()

        # Atualiza o ícone da UI, se ele mudou
        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path and new_ui_icon_path != self.ui_icon_path:
            self.ui_icon_path = new_ui_icon_path
            # Recarrega o ícone na classe pai (Weapon)
            if hasattr(self, '_load_ui_icon'):
                self._load_ui_icon()

    def evolve(self, target_level: float):
        """Evolui a arma para um novo nível."""
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"'{self.name}' evoluiu para o nível {self.level}!")

    def can_attack(self):
        """Verifica se a arma pode atacar com base no cooldown."""
        return pygame.time.get_ticks() - self.last_shot_time >= (self.cooldown * 1000)

    def attack(self, player, inimigos_lista):
        """
        Encontra o inimigo mais próximo e cria um projétil de Ametista que o persegue.
        """
        if self.can_attack():
            self.last_shot_time = pygame.time.get_ticks()
            
            inimigo_mais_proximo = None
            menor_distancia = float('inf')

            # 1. Encontra o inimigo vivo mais próximo
            for inimigo in inimigos_lista:
                if not (hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo()):
                    continue

                distancia = math.hypot(player.rect.centerx - inimigo.rect.centerx, 
                                        player.rect.centery - inimigo.rect.centery)
                
                if distancia < self.attack_range and distancia < menor_distancia:
                    menor_distancia = distancia
                    inimigo_mais_proximo = inimigo
            
            # 2. Se um inimigo foi encontrado, cria o projétil
            if inimigo_mais_proximo:
                return AmetistaProjectile(player.rect.centerx, player.rect.centery, inimigo_mais_proximo)

        return None
