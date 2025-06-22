import pygame
import os
import math
from .MachadoBase import MachadoBase

class MachadoBarbaro(MachadoBase):
    """
    Representa o Machado Bárbaro Cravejado, uma arma com níveis de evolução
    e sua própria animação de ataque, agora com carregamento de assets robusto.
    """
    def __init__(self):
        self._base_name = "Machado Bárbaro Cravejado"
        self.level = 1.0
        self.is_collectible = True

        # --- CONFIGURAÇÕES POR NÍVEL ---
        # Caminhos agora usam tuplos para compatibilidade entre sistemas
        self._stats_by_level = {
            1.0: {
                "damage": 15.0, "range": 85.0, "cooldown": 2.2, "name_suffix": "",
                "hitbox_dim": (110, 300), "hitbox_off": (110, 0),
                "effect_sprite_base": ("Sprites", "Armas", "Machados", "MachadoBarbaro", "Efeitos", "ImpactoBrutoNv1.png"),
                "effect_scale_base": 1.0,
                "animation_sprites": [
                    ("Sprites", "Armas", "Machados", "Machado Bárbaro Cravejado", "Ataque", "AT1", f"AT1-base{i}.png") for i in range(5)
                ],
                "animation_speed": 120, "animation_display_scale": 1.2,
                "ui_icon": ("Sprites", "Armas", "Machados", "Machado Bárbaro Cravejado", "Machado E-1.png")
            },
            1.5: {
                "damage": 20.0, "range": 90.0, "cooldown": 2.1, "name_suffix": "+1",
                "animation_sprites": [
                    ("Sprites", "Armas", "Machados", "Machado Bárbaro Cravejado", "Ataque", "AT1", f"AT1-base{i}.png") for i in range(5)
                ],
                "animation_speed": 115, "animation_display_scale": 1.2,
                "ui_icon": ("Sprites", "Armas", "Machados", "Machado Bárbaro Cravejado", "Machado E-1.png")
            },
            2.0: {
                "damage": 25.0, "range": 100.0, "cooldown": 1.9, "name_suffix": "Reforçado",
                "effect_sprite_base": ("Sprites", "Armas", "Machados", "MachadoBarbaro", "Efeitos", "ImpactoBrutoNv2.png"),
                "animation_sprites": [
                    ("Sprites", "Armas", "Machados", "Machado Bárbaro Cravejado", "Ataque", "AT2", f"AT2-base{i}.png") for i in range(5)
                ],
                "animation_speed": 110, "animation_display_scale": 1.25,
                "ui_icon": ("Sprites", "Armas", "Machados", "Machado Bárbaro Cravejado", "Machado E-2.png")
            },
            2.5: {
                "damage": 30.0, "range": 105.0, "cooldown": 1.8, "name_suffix": "Reforçado +1",
                "animation_sprites": [
                    ("Sprites", "Armas", "Machados", "Machado Bárbaro Cravejado", "Ataque", "AT2", f"AT2-base{i}.png") for i in range(5)
                ],
                "animation_speed": 105, "animation_display_scale": 1.25,
                "ui_icon": ("Sprites", "Armas", "Machados", "Machado Bárbaro Cravejado", "Machado E-2.png")
            },
            3.0: {
                "damage": 35.0, "range": 120.0, "cooldown": 1.6, "name_suffix": "Brutal",
                "effect_sprite_base": ("Sprites", "Armas", "Machados", "MachadoBarbaro", "Efeitos", "ImpactoBrutoNv3.png"),
                "animation_sprites": [
                    ("Sprites", "Armas", "Machados", "Machado Bárbaro Cravejado", "Ataque", "AT3", f"AT3-base{i}.png") for i in range(5)
                ],
                "animation_speed": 100, "animation_display_scale": 1.3,
                "ui_icon": ("Sprites", "Armas", "Machados", "Machado Bárbaro Cravejado", "Machado E-3.png")
            }
        }

        initial_stats = self._get_stats_for_level_internal(self.level, for_super_init=True)
        super().__init__(
            name=self._base_name,
            damage=initial_stats.get("damage", 15.0),
            attack_range=initial_stats.get("range", 85.0),
            cooldown=initial_stats.get("cooldown", 2.2),
            level=self.level
        )

        self.description = "Um machado pesado e brutal, adornado com cravos ameaçadores."
        self.rarity = "Comum"
        self.weapon_type = "Machado de Duas Mãos"
        self.element = "Físico"

        self.ui_icon = None
        self.attack_animation_sprites = []
        self.attack_animation_speed = 120
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0

        self._apply_level_stats()

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", "..", ".."))

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        if for_super_init:
            return self._stats_by_level[1.0]
        return self._stats_by_level.get(level_to_check, self._stats_by_level[1.0])

    def _load_ui_icon(self, caminhos_segmentados):
        if not caminhos_segmentados:
            self.ui_icon = None
            return
        
        project_root = self._obter_pasta_raiz_jogo()
        full_path = os.path.join(project_root, *caminhos_segmentados)
        try:
            if os.path.exists(full_path):
                self.ui_icon = pygame.image.load(full_path).convert_alpha()
            else:
                print(f"AVISO(MachadoBarbaro): Ícone de UI não encontrado em '{full_path}'.")
                self.ui_icon = None
        except pygame.error as e:
            print(f"ERRO(MachadoBarbaro): Falha ao carregar ícone de UI '{full_path}': {e}.")
            self.ui_icon = None

    def _load_weapon_attack_animation_sprites(self, caminhos_segmentados, escala_animacao=1.0):
        sprites_carregados = []
        project_root = self._obter_pasta_raiz_jogo()

        for path_segments in caminhos_segmentados:
            full_path = os.path.join(project_root, *path_segments)
            try:
                if os.path.exists(full_path):
                    imagem_original = pygame.image.load(full_path).convert_alpha()
                    novo_w = int(imagem_original.get_width() * escala_animacao)
                    novo_h = int(imagem_original.get_height() * escala_animacao)
                    if novo_w > 0 and novo_h > 0:
                        imagem = pygame.transform.smoothscale(imagem_original, (novo_w, novo_h))
                        sprites_carregados.append(imagem)
                else:
                    print(f"AVISO(MachadoBarbaro): Sprite de animação ATK não encontrado em '{full_path}'.")
            except pygame.error as e:
                print(f"ERRO(MachadoBarbaro): Falha ao carregar '{full_path}': {e}.")
        
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
        else:
            print(f"AVISO(MachadoBarbaro): Nível {target_level} inválido. Níveis disponíveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        
        self.damage = stats["damage"]
        self.attack_range = stats["range"]
        self.cooldown = stats["cooldown"]
        self.name = f"{self._base_name} {stats.get('name_suffix', '')}".strip()
        
        # O resto dos atributos...
        self.hitbox_width, self.hitbox_height = stats.get("hitbox_dim", (90, 90))
        self.hitbox_offset_x, self.hitbox_offset_y = stats.get("hitbox_off", (0, 0))
        self.attack_animation_speed = stats.get("animation_speed", 120)
        
        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path:
            self._load_ui_icon(new_ui_icon_path)

        new_animation_paths = stats.get("animation_sprites")
        new_animation_display_scale = stats.get("animation_display_scale", 1.0)
        if new_animation_paths:
            self._load_weapon_attack_animation_sprites(new_animation_paths, new_animation_display_scale)
            
    def get_current_attack_animation_sprite(self):
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None

if __name__ == '__main__':
    pass
