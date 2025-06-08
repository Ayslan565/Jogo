# Jogo/Arquivos/Armas/CajadoDaFixacaoAmetista.py
import pygame
import os
from .weapon import Weapon
from .AmetistaProjectile import AmetistaProjectile # Importa o novo projétil

class CajadoDaFixacaoAmetista(Weapon):
    """
    Representa o Cajado da Fixação da Ametista, uma arma mágica que dispara projéteis teleguiados.
    """
    def __init__(self):
        self._base_name = "Cajado da Fixação da Ametista"
        self.level = 1.0

        initial_stats = self._get_stats_for_level_internal(self.level, for_super_init=True)
        
        super().__init__(
            name=self._base_name,
            damage=initial_stats.get("damage", 18.0),
            attack_range=initial_stats.get("range", 400.0), # Alcance para encontrar um alvo
            cooldown=initial_stats.get("cooldown", 1.2),
            # Hitbox não é usada para dano, mas pode ser para a animação do cajado
            hitbox_dimensions=(0,0), 
            hitbox_offset=(0,0),
            description="Dispara um orbe de ametista que persegue os inimigos.",
            rarity="Mágica",
            weapon_type="Cajado",
            element="Arcano",
            ui_icon_path=initial_stats.get("ui_icon", "Sprites/Armas/Cajados/Ametista/Icone.png")
        )

        # Atributo especial para identificar como arma de longo alcance
        self.attack_style = 'ranged' 
        self.projectile_class = AmetistaProjectile # Define qual classe de projétil usar
        self.projectile_speed = 6.5
        self.projectile_lifetime = 3.0 # Segundos
        self.projectile_scale = 1.0

        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        self._stats_by_level = {
            1.0: { "damage": 18.0, "cooldown": 1.2, "range": 400.0, "name_suffix": "" },
            2.0: { "damage": 25.0, "cooldown": 1.1, "range": 450.0, "name_suffix": "+1" },
            3.0: { "damage": 33.0, "cooldown": 1.0, "range": 500.0, "name_suffix": "+2" }
        }
        self._apply_level_stats()

    def _get_stats_for_level_internal(self, level, for_super_init=False):
        # Fallback para o construtor da superclasse
        if for_super_init and (not hasattr(self, '_stats_by_level') or not self._stats_by_level):
            return { "damage": 18.0, "cooldown": 1.2, "range": 400.0, "ui_icon": "Sprites/Armas/Cajados/Ametista/Icone.png" }
        
        return self._stats_by_level.get(level, self._stats_by_level[1.0])

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(CajadoAmetista): '{self.name}' evoluiu para o Nível {self.level}!")
        else:
            print(f"WARN(CajadoAmetista): Nível de evolução {target_level} inválido.")

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        self.damage = stats["damage"]
        self.cooldown = stats["cooldown"]
        self.attack_range = stats["range"]
        suffix = stats.get("name_suffix", "")
        self.name = f"{self._base_name} {suffix}".strip()   