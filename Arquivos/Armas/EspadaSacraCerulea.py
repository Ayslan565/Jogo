import pygame
import os
from .weapon import Weapon

class EspadaSacraCerulea(Weapon):
    """
    Representa a Espada Sacra Cerúlea. A escala da animação é controlada
    por um único valor em cada nível.
    """
    def __init__(self):
        self._base_name = "Espada Sacra Cerúlea"
        self.level = 1.0
        self.price = 150

        self._stats_by_level = {
            1.0: {
                "damage": 25.0, "range": 100.0, "cooldown": 1.2, "name_suffix": "",
                "hitbox_dim": (100 , 45),
                "hitbox_off": (90, 5),
                "animation_speed": 90,
                "animation_display_scale": 0.15, # <- CONTROLE A ESCALA DO NÍVEL 1 AQUI
                "ui_icon": "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Espada Dos Deuses Caidos -E1.png",
                "description": "Lâmina de aço cintilante com punho dourado e uma gema safira-azul.",
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Ataque/AT1/AT1-base0.png",
                    "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Ataque/AT1/AT1-base1.png",
                    "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Ataque/AT1/AT1-base2.png",
                    "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Ataque/AT1/AT1-base3.png",
                ]
            },
            2.0: {
                "damage": 32.0, "range": 105.0, "cooldown": 1.1, "name_suffix": " Desperta",
                "hitbox_dim": (105 , 50),
                "hitbox_off": (95, 5),
                "animation_speed": 85,
                "animation_display_scale": 0.20, # <- CONTROLE A ESCALA DO NÍVEL 2 AQUI
                "ui_icon": "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Espada Dos Deuses Caidos -E2.png",
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Ataque/AT2/AT2-base0.png",
                    "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Ataque/AT2/AT2-base1.png",
                    "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Ataque/AT2/AT2-base2.png",
                    "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Ataque/AT2/AT2-base3.png",
                ]
            },
            3.0: {
                "damage": 36.0, "range": 110.0, "cooldown": 1.0, "name_suffix": " Celestial",
                "hitbox_dim": (110 , 55),
                "hitbox_off": (100, 5),
                "animation_speed": 80,
                "animation_display_scale": 0.25, # <- CONTROLE A ESCALA DO NÍVEL 3 AQUI
                "ui_icon": "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Espada Dos Deuses Caidos -E3.png",
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Ataque/AT3/AT3-base0.png",
                    "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Ataque/AT3/AT3-base1.png",
                    "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Ataque/AT3/AT3-base2.png",
                    "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Ataque/AT3/AT3-base3.png",
                ]
            }
        }
        
        initial_stats = self._get_stats_for_level_internal(1.0)
        super().__init__(
            name=self._base_name,
            damage=initial_stats.get("damage"),
            attack_range=initial_stats.get("range"),
            cooldown=initial_stats.get("cooldown"),
            hitbox_dimensions=initial_stats.get("hitbox_dim"),
            hitbox_offset=initial_stats.get("hitbox_off"),
            description=initial_stats.get("description"),
            rarity="Lendária",
            weapon_type="Espada Longa",
            element="Fogo Azul",
            ui_icon_path=initial_stats.get("ui_icon")
        )
        self._apply_level_stats()

    def _get_stats_for_level_internal(self, level_to_check):
        return self._stats_by_level.get(level_to_check, self._stats_by_level.get(1.0))

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        if not stats: return

        self.damage = stats.get("damage", self.damage)
        self.attack_range = stats.get("range", self.attack_range)
        self.cooldown = stats.get("cooldown", self.cooldown)
        self.attack_animation_speed = stats.get("animation_speed", self.attack_animation_speed)
        if "hitbox_dim" in stats: self.hitbox_width, self.hitbox_height = stats["hitbox_dim"]
        if "hitbox_off" in stats: self.hitbox_offset_x, self.hitbox_offset_y = stats["hitbox_off"]

        new_animation_paths = stats.get("animation_sprites")
        new_scale = stats.get("animation_display_scale", 1.0)
        
        # Recarrega os sprites se os caminhos ou a escala mudarem
        if new_animation_paths and (new_animation_paths != self.attack_animation_paths or new_scale != self.animation_display_scale_factor):
            self.attack_animation_paths = new_animation_paths
            self.animation_display_scale_factor = new_scale
            self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)

        self.name = f"{self._base_name} {stats.get('name_suffix', '')}".strip()
        
    def update_animation(self, current_ticks):
        if not self.attack_animation_sprites: return
        if current_ticks - self.last_attack_animation_update > self.attack_animation_speed:
            self.last_attack_animation_update = current_ticks
            if self.attack_animation_sprites:
                self.current_attack_animation_frame = (self.current_attack_animation_frame + 1) % len(self.attack_animation_sprites)