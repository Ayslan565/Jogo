import pygame
import os
# Importa a classe base 'Weapon'
from .weapon import Weapon

class EspadaLua(Weapon):
    """
    Representa a Espada Sacra da Lua, uma arma com níveis de evolução,
    ataque horizontal e progressão de stats.
    """
    def __init__(self):
        self._base_name = "Espada Sacra da Lua"
        self.level = 1.0
        self.price = 450 # Preço base para a loja

        # --- DADOS DE PROGRESSÃO POR NÍVEL (COM CAMINHOS CORRIGIDOS) ---
        self._stats_by_level = {
            1.0: {
                "damage": 26.0, "range": 115.0, "cooldown": 1.2, "name_suffix": "(Azul com Roxo)",
                "hitbox_dim": (90 , 35),  # Hitbox horizontal
                "hitbox_off": (80, 5),    # Posicionada à frente
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaLua/Efeitos/ImpactoLunarNv1.png",
                "effect_scale_base": 1.0,
                # CORRIGIDO: Nomes dos arquivos de animação ajustados para corresponder à imagem
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT1/E0.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT1/E1.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT1/E2.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT1/E3.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT1/E4.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT1/E5.png"
                ],
                "animation_speed": 85, "animation_display_scale": 0.2, # Escala ajustada
                "ui_icon": "Sprites/Armas/Espadas/Espada Sacra da Lua/E1.png",
                "description": "Uma espada imbuída com o poder místico da lua, brilhando em tons de azul e roxo."
            },
            1.5: {
                "damage": 29.0, "range": 120.0, "cooldown": 1.15, "name_suffix": "(Azul com Roxo) +1",
                "hitbox_dim": (95 , 40), "hitbox_off": (85, 5),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaLua/Efeitos/ImpactoLunarNv1.png",
                "effect_scale_base": 1.05,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT1/E0.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT1/E1.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT1/E2.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT1/E3.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT1/E4.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT1/E5.png"
                ],
                "animation_speed": 82, "animation_display_scale": 0.2,
                "ui_icon": "Sprites/Armas/Espadas/Espada Sacra da Lua/E1.png" 
            },
            2.0: {
                "damage": 36.0, "range": 130.0, "cooldown": 1.0, "name_suffix": "Crescente (Azul e Lilás)",
                "hitbox_dim": (100 , 45), "hitbox_off": (90, 5),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaLua/Efeitos/ImpactoLunarNv2.png",
                "effect_scale_base": 1.15,
                # Assumindo que os arquivos em AT2 seguem o mesmo padrão E0, E1...
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT2/E0.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT2/E1.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT2/E2.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT2/E3.png"
                ],
                "animation_speed": 80, "animation_display_scale": 0.2,
                "ui_icon": "Sprites/Armas/Espadas/Espada Sacra da Lua/E2.png"
            },
            2.5: {
                "damage": 39.0, "range": 135.0, "cooldown": 0.95, "name_suffix": "Crescente (Azul e Lilás) +1",
                "hitbox_dim": (105 , 50), "hitbox_off": (95, 5),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaLua/Efeitos/ImpactoLunarNv2.png",
                "effect_scale_base": 1.2,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT2/E0.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT2/E1.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT2/E2.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT2/E3.png"
                ],
                "animation_speed": 78, "animation_display_scale": 0.2,
                "ui_icon": "Sprites/Armas/Espadas/Espada Sacra da Lua/E2.png"
            },
            3.0: {
                "damage": 42.0, "range": 150.0, "cooldown": 0.8, "name_suffix": "Plena (Índigo e Violeta)",
                "hitbox_dim": (110 , 55), "hitbox_off": (100, 5),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaLua/Efeitos/ImpactoLunarNv3.png",
                "effect_scale_base": 1.25,
                 # Assumindo que os arquivos em AT3 seguem o mesmo padrão E0, E1...
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT3/E0.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT3/E1.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT3/E2.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT3/E3.png",
                    "Sprites/Armas/Espadas/Espada Sacra da Lua/Ataque/AT3/E4.png"
                ],
                "animation_speed": 75, "animation_display_scale": 0.2,
                "ui_icon": "Sprites/Armas/Espadas/Espada Sacra da Lua/E3.png"
            }
        }
        
        initial_stats = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name,
            damage=initial_stats.get("damage"),
            attack_range=initial_stats.get("range"),
            cooldown=initial_stats.get("cooldown"),
            hitbox_dimensions=initial_stats.get("hitbox_dim"),
            hitbox_offset=initial_stats.get("hitbox_off"),
            description=initial_stats.get("description"),
            rarity="Lendária",
            weapon_type="Espada Lunar",
            element="Lunar",
            attack_effect_sprite_path=initial_stats.get("effect_sprite_base"),
            attack_effect_scale=initial_stats.get("effect_scale_base"),
            ui_icon_path=initial_stats.get("ui_icon")
        )

        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 100
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0

        self._apply_level_stats()

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        stats_dict = self._stats_by_level
        if for_super_init:
            return stats_dict.get(1.0, {})
        return stats_dict.get(level_to_check, stats_dict.get(1.0))

    def _load_weapon_attack_animation_sprites(self, caminhos, escala_animacao=1.0):
        sprites_carregados = []
        if not caminhos:
            self.attack_animation_sprites = []
            return
        for path_relativo in caminhos:
            path_corrigido = path_relativo.replace("\\", os.sep).replace("/", os.sep)
            full_path = path_corrigido
            try:
                if os.path.exists(full_path):
                    imagem_original = pygame.image.load(full_path).convert_alpha()
                    novo_w = int(imagem_original.get_width() * escala_animacao)
                    novo_h = int(imagem_original.get_height() * escala_animacao)
                    if novo_w > 0 and novo_h > 0:
                        imagem = pygame.transform.smoothscale(imagem_original, (novo_w, novo_h))
                        sprites_carregados.append(imagem)
                else:
                    print(f"WARN(EspadaLua): Sprite de animação não encontrado '{full_path}'.")
                    placeholder = pygame.Surface((32, 32), pygame.SRCALPHA); placeholder.fill((75, 0, 130, 100))
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"ERROR(EspadaLua): Erro ao carregar sprite '{full_path}': {e}.")
                placeholder = pygame.Surface((32, 32), pygame.SRCALPHA); placeholder.fill((255, 0, 0, 150))
                sprites_carregados.append(placeholder)
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0

    def start_attack_animation(self):
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = pygame.time.get_ticks()

    def update_animation(self, current_ticks):
        if not self.attack_animation_sprites: return
        if current_ticks - self.last_attack_animation_update > self.attack_animation_speed:
            self.last_attack_animation_update = current_ticks
            if self.attack_animation_sprites:
                self.current_attack_animation_frame = (self.current_attack_animation_frame + 1) % len(self.attack_animation_sprites)

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        if not stats: return

        self.damage = stats.get("damage", self.damage)
        self.attack_range = stats.get("range", self.attack_range)
        self.cooldown = stats.get("cooldown", self.cooldown)
        if "hitbox_dim" in stats: self.hitbox_width, self.hitbox_height = stats["hitbox_dim"]
        if "hitbox_off" in stats: self.hitbox_offset_x, self.hitbox_offset_y = stats["hitbox_off"]
        self.description = stats.get("description", self.description)

        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path and new_ui_icon_path != self.ui_icon_path:
            self.ui_icon_path = new_ui_icon_path
            if hasattr(super(), '_load_ui_icon'): super()._load_ui_icon()

        new_animation_paths = stats.get("animation_sprites")
        new_animation_display_scale = stats.get("animation_display_scale", 1.0)
        if new_animation_paths:
            if (new_animation_paths != self.attack_animation_paths or
                new_animation_display_scale != self.animation_display_scale_factor or
                not self.attack_animation_sprites):
                self.attack_animation_paths = new_animation_paths
                self.animation_display_scale_factor = new_animation_display_scale
                self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)

        self.attack_animation_speed = stats.get("animation_speed", self.attack_animation_speed)
        self.name = f"{self._base_name} {stats.get('name_suffix', '')}".strip()

    def get_current_attack_animation_sprite(self):
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None