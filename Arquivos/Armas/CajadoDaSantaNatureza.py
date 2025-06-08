# Jogo/Arquivos/Armas/CajadoDaSantaNatureza.py
import pygame
import os
from .weapon import Weapon
from .FolhaCortanteProjectile import FolhaCortanteProjectile # Importa o projétil de folha

class CajadoDaSantaNatureza(Weapon):
    """
    Representa o Cajado da Santa Natureza, uma arma que dispara folhas cortantes.
    """
    def __init__(self):
        self._base_name = "Cajado Da santa Natureza"
        self.level = 1.0

        initial_stats = self._get_stats_for_level_internal(self.level, for_super_init=True)
        
        super().__init__(
            name=self._base_name,
            damage=initial_stats.get("damage", 15.0),
            attack_range=initial_stats.get("range", 500.0), # Alcance para encontrar um alvo
            cooldown=initial_stats.get("cooldown", 0.8),
            hitbox_dimensions=(0,0), # Não usa hitbox de melee
            hitbox_offset=(0,0),
            description="Uma arma única rara e que causa medo a todos os monstros da floresta. Esse cajado parece simples mas é feito com a madeira de uma árvore almadiçoada. A natureza estará sempre ao seu lado quando você estiver usando ele.",
            rarity="Rara",
            weapon_type="Cajado",
            element="Natureza",
            ui_icon_path=initial_stats.get("ui_icon", "Sprites/Armas/Armas Magicas/Cajado Da santa Natureza/E1.png")
        )

        # Atributos para ataque à distância
        self.attack_style = 'ranged' 
        self.projectile_class = FolhaCortanteProjectile
        self.projectile_speed = 8.0 # Folhas são rápidas
        self.projectile_lifetime = 2.0
        self.projectile_scale = 1.2

        # Configurações de evolução
        self._stats_by_level = {
            1.0: { "damage": 15.0, "cooldown": 0.8, "range": 500.0, "name_suffix": "" },
            2.0: { "damage": 22.0, "cooldown": 0.7, "range": 550.0, "name_suffix": " Abençoado" },
            3.0: { "damage": 30.0, "cooldown": 0.6, "range": 600.0, "name_suffix": " Ancestral" }
        }
        self._apply_level_stats()

    def _get_stats_for_level_internal(self, level, for_super_init=False):
        if for_super_init and (not hasattr(self, '_stats_by_level') or not self._stats_by_level):
            return { "damage": 15.0, "cooldown": 0.8, "range": 500.0, "ui_icon": "Sprites/Armas/Armas Magicas/Cajado Da santa Natureza/E1.png" }
        
        return self._stats_by_level.get(level, self._stats_by_level[1.0])

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(CajadoNatureza): '{self.name}' evoluiu para o Nível {self.level}!")
        else:
            print(f"WARN(CajadoNatureza): Nível de evolução {target_level} inválido.")

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        self.damage = stats["damage"]
        self.cooldown = stats["cooldown"]
        self.attack_range = stats["range"]
        suffix = stats.get("name_suffix", "")
        self.name = f"{self._base_name} {suffix}".strip()
