# Jogo/Arquivos/Armas/LivroDosImpuros.py
import pygame
import os
from .weapon import Weapon
from .CaveiraImpuraProjectile import CaveiraImpuraProjectile # Importa o novo projétil

class LivroDosImpuros(Weapon):
    """
    Representa o Livro dos Impuros, uma arma que dispara caveiras profanas.
    """
    def __init__(self):
        self._base_name = "Livro dos Impuros"
        self.level = 1.0

        initial_stats = self._get_stats_for_level_internal(self.level, for_super_init=True)
        
        super().__init__(
            name=self._base_name,
            damage=initial_stats.get("damage", 25.0),
            attack_range=initial_stats.get("range", 600.0),
            cooldown=initial_stats.get("cooldown", 1.5),
            hitbox_dimensions=(0,0), # Arma de longo alcance, não usa hitbox de melee
            hitbox_offset=(0,0),
            description="Contém conhecimento proibido, pode ser que ele te ensine a dominar alguma arte mística, ou pode ser que ele te enlouqueça até a MORTE.",
            rarity="Épica",
            weapon_type="Grimório",
            element="Profano",
            ui_icon_path=initial_stats.get("ui_icon", "Sprites/Armas/Armas Magicas/Livro dos impuros/E1.jpg")
        )

        # Atributos para ataque à distância
        self.attack_style = 'ranged' 
        self.projectile_class = CaveiraImpuraProjectile
        self.projectile_speed = 7.0
        self.projectile_lifetime = 3.5
        self.projectile_scale = 1.1

        # Configurações de evolução
        self._stats_by_level = {
            1.0: { "damage": 25.0, "cooldown": 1.5, "range": 600.0, "name_suffix": "" },
            2.0: { "damage": 35.0, "cooldown": 1.3, "range": 650.0, "name_suffix": " Profano" },
            3.0: { "damage": 48.0, "cooldown": 1.1, "range": 700.0, "name_suffix": " do Abismo" }
        }
        self._apply_level_stats()

    def _get_stats_for_level_internal(self, level, for_super_init=False):
        if for_super_init and (not hasattr(self, '_stats_by_level') or not self._stats_by_level):
            return { "damage": 25.0, "cooldown": 1.5, "range": 600.0, "ui_icon": "Sprites/Armas/Armas Magicas/Livro dos impuros/E1.jpg" }
        
        return self._stats_by_level.get(level, self._stats_by_level[1.0])

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(LivroImpuros): '{self.name}' evoluiu para o Nível {self.level}!")
        else:
            print(f"WARN(LivroImpuros): Nível de evolução {target_level} inválido.")

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        self.damage = stats["damage"]
        self.cooldown = stats["cooldown"]
        self.attack_range = stats["range"]
        suffix = stats.get("name_suffix", "")
        self.name = f"{self._base_name} {suffix}".strip()
