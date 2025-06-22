import pygame
import os
# Importa a classe base para machados.
from .MachadoBase import MachadoBase

class MachadoDoFogoAbrasador(MachadoBase):
    """
    Representa o Machado do Fogo Abrasador, uma arma com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Machado do Fogo Abrasador"
        self.level = 1.0 # Nível inicial

        # --- DADOS DOS NÍVEIS ---
        # Caminhos padronizados e valores de placeholder para serem ajustados.
        self._stats_by_level = {
            1.0: {
                "damage": 28.0, "range": 100.0, "cooldown": 2.1, "name_suffix": "",
                "hitbox_dim": (100, 100), "hitbox_off": (100, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Efeitos/ImpactoChamaNv1.png",
                "effect_scale_base": 1.0,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT1/AT1-base0.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT1/AT1-base1.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT1/AT1-base2.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT1/AT1-base3.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT1/AT1-base4.png",
                ],
                "animation_speed": 50, "animation_display_scale": 0.25,
                "ui_icon": "Sprites/Armas/Machados/Machado do Fogo Abrasador/E1.png"
            },
            1.5: {
                "damage": 34.0, "range": 100.0, "cooldown": 2.0, "name_suffix": "+1",
                "hitbox_dim": (95, 105), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Efeitos/ImpactoChamaNv1.png",
                "effect_scale_base": 1.05,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT1/AT1-base0.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT1/AT1-base1.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT1/AT1-base2.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT1/AT1-base3.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT1/AT1-base4.png",
                ],
                "animation_speed": 40, "animation_display_scale": 0.25,
                "ui_icon": "Sprites/Armas/Machados/Machado do Fogo Abrasador/E1.png"
            },
            2.0: {
                "damage": 42.0, "range": 110.0, "cooldown": 1.8, "name_suffix": "Infernal",
                "hitbox_dim": (100, 110), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Efeitos/ImpactoChamaNv2.png",
                "effect_scale_base": 1.1,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT2/AT2-base0.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT2/AT2-base1.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT2/AT2-base2.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT2/AT2-base3.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT2/AT2-base4.png",
                ],
                "animation_speed": 30, "animation_display_scale": 0.25,
                "ui_icon": "Sprites/Armas/Machados/Machado do Fogo Abrasador/E2.png"
            },
            2.5: {
                "damage": 50.0, "range": 115.0, "cooldown": 1.7, "name_suffix": "Infernal +1",
                "hitbox_dim": (105, 115), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Efeitos/ImpactoChamaNv2.png",
                "effect_scale_base": 1.15,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT2/AT2-base0.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT2/AT2-base1.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT2/AT2-base2.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT2/AT2-base3.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT2/AT2-base4.png",
                ],
                "animation_speed": 25, "animation_display_scale": 0.255,
                "ui_icon": "Sprites/Armas/Machados/Machado do Fogo Abrasador/E2.jpg"
            },
            3.0: {
                "damage": 60.0, "range": 130.0, "cooldown": 1.5, "name_suffix": "Cataclísmico",
                "hitbox_dim": (110, 120), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Efeitos/ImpactoChamaNv3.png",
                "effect_scale_base": 0.20,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT3/AT3-base0.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT3/AT3-base1.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT3/AT3-base2.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT3/AT3-base3.png",
                    "Sprites/Armas/Machados/Machado do Fogo Abrasador/Ataque/AT3/AT3-base4.png",
                ],
                "animation_speed": 20, "animation_display_scale": 1.3,
                "ui_icon": "Sprites/Armas/Machados/Machado do Fogo Abrasador/E3.png"
            }
        }

        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name, damage=initial_stats_for_super.get("damage"),
            attack_range=initial_stats_for_super.get("range"), cooldown=initial_stats_for_super.get("cooldown"),
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim"),
            hitbox_offset=initial_stats_for_super.get("hitbox_off"),
            description="Deixa um rastro de cinzas.", rarity="Épico",
            weapon_type="Machado de Duas Mãos", element="Fogo",
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base"),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base"),
            ui_icon_path=initial_stats_for_super.get("ui_icon")
        )

        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 100
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 0.25

        self._apply_level_stats()

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        stats_dict = self._stats_by_level
        if for_super_init:
            return stats_dict.get(1.0, {})
        if level_to_check in stats_dict:
            return stats_dict[level_to_check]
        else:
            first_level_key = next(iter(stats_dict))
            return stats_dict[first_level_key]

    # <<<!!! FUNÇÃO DE CARREGAMENTO CORRIGIDA !!!>>>
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
                        placeholder = pygame.Surface((32, 32), pygame.SRCALPHA); placeholder.fill((255, 100, 0, 100))
                        sprites_carregados.append(placeholder)
                else:
                    print(f"WARN(MachadoDoFogoAbrasador): Sprite de animação ATK não encontrado '{full_path}'.")
                    placeholder = pygame.Surface((32, 32), pygame.SRCALPHA); placeholder.fill((255, 100, 0, 100))
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"ERROR(MachadoDoFogoAbrasador): Erro ao carregar sprite ATK '{full_path}': {e}.")
                placeholder = pygame.Surface((32, 32), pygame.SRCALPHA); placeholder.fill((255, 0, 0, 150))
                sprites_carregados.append(placeholder)
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0

    # --- MÉTODOS DE ANIMAÇÃO ADICIONADOS ---
    def start_attack_animation(self):
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = pygame.time.get_ticks()

    def update_animation(self, current_ticks):
        if not self.attack_animation_sprites:
            return
        if current_ticks - self.last_attack_animation_update > self.attack_animation_speed:
            self.last_attack_animation_update = current_ticks
            if self.attack_animation_sprites:
                self.current_attack_animation_frame = (self.current_attack_animation_frame + 1) % len(self.attack_animation_sprites)
    # --- FIM DOS MÉTODOS ADICIONADOS ---

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        if not stats: return

        self.damage = stats["damage"]
        self.attack_range = stats["range"]
        self.cooldown = stats["cooldown"]

        if "hitbox_dim" in stats: self.hitbox_width, self.hitbox_height = stats["hitbox_dim"]
        if "hitbox_off" in stats: self.hitbox_offset_x, self.hitbox_offset_y = stats["hitbox_off"]

        new_base_effect_path = stats.get("effect_sprite_base")
        new_base_effect_scale = stats.get("effect_scale_base", self.attack_effect_scale)

        if hasattr(super(), '_load_attack_effect_sprite'):
            if new_base_effect_path and new_base_effect_path != self.attack_effect_sprite_path:
                self.attack_effect_sprite_path = new_base_effect_path
                self.attack_effect_scale = new_base_effect_scale
                super()._load_attack_effect_sprite()
            elif new_base_effect_scale != self.attack_effect_scale and hasattr(self, 'attack_effect_original_image') and self.attack_effect_original_image:
                self.attack_effect_scale = new_base_effect_scale
                if self.attack_effect_original_image:
                    width = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                    height = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                    if width > 0 and height > 0:
                        self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (width, height))
                    else:
                        self.attack_effect_image = None

        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path and new_ui_icon_path != self.ui_icon_path:
            self.ui_icon_path = new_ui_icon_path
            if hasattr(super(), '_load_ui_icon'):
                super()._load_ui_icon()

        new_animation_paths = stats.get("animation_sprites")
        new_animation_display_scale = stats.get("animation_display_scale", 0.20)

        if new_animation_paths is not None:
            if (new_animation_paths != self.attack_animation_paths or
                new_animation_display_scale != self.animation_display_scale_factor or
                not self.attack_animation_sprites):
                self.attack_animation_paths = new_animation_paths
                self.animation_display_scale_factor = new_animation_display_scale
                self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)

        self.attack_animation_speed = stats.get("animation_speed", 1000)
        name_suffix = stats.get("name_suffix", "")
        self.name = f"{self._base_name} {name_suffix}".strip()

    def get_current_attack_animation_sprite(self):
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None

# O bloco de teste foi removido para manter o arquivo limpo, mas a lógica dele estava correta para testes.