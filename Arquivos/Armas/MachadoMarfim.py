# Armas/MachadoMarfim.py
import pygame
import os
# Importa a classe base para machados.
from .MachadoBase import MachadoBase

class MachadoMarfim(MachadoBase):
    """
    Representa o Machado do Marfim Resplendor, uma arma com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Machado do Marfim Resplendor"
        self.level = 1.0 # Nível inicial
        self.is_collectible = True

        self._stats_by_level = {
            1.0: {
                "damage": 48.0, "range": 95.0, "cooldown": 1.8, "name_suffix": "",
                "hitbox_dim": (90, 90), "hitbox_off": (0, 0),
                "effect_sprite_base": ("Sprites", "Armas", "Machados", "MachadoMarfim", "Efeitos", "ImpactoLuzNv1.png"),
                "effect_scale_base": 1.0,
                "animation_sprites": [
                    ("Sprites", "Armas", "Machados", "Machado do Marfim Resplendor", "Ataque", "AT1", f"AT1-base{i}.png") for i in range(5)
                ],
                "animation_speed": 100, "animation_display_scale": 1.15,
                "ui_icon": ("Sprites", "Armas", "Machados", "Machado do Marfim Resplendor", "E1.png"),
                "description": "Um machado elegante feito de marfim polido, que brilha com uma luz suave.",
                "rarity": "Épica", "weapon_type": "Machado Nobre", "element": "Luz"
            },
            1.5: {
                "damage": 53.0, "range": 100.0, "cooldown": 1.7, "name_suffix": "+1",
                "hitbox_dim": (95, 95), "hitbox_off": (0, 0),
                "effect_sprite_base": ("Sprites", "Armas", "Machados", "MachadoMarfim", "Efeitos", "ImpactoLuzNv1.png"),
                "effect_scale_base": 1.05,
                "animation_sprites": [
                    ("Sprites", "Armas", "Machados", "Machado do Marfim Resplendor", "Ataque", "AT1", f"AT1-base{i}.png") for i in range(5)
                ],
                "animation_speed": 95, "animation_display_scale": 1.15,
                "ui_icon": ("Sprites", "Armas", "Machados", "Machado do Marfim Resplendor", "E1.png")
            },
            2.0: {
                "damage": 65.0, "range": 110.0, "cooldown": 1.5, "name_suffix": "Iluminado",
                "hitbox_dim": (100, 100), "hitbox_off": (0, 0),
                "effect_sprite_base": ("Sprites", "Armas", "Machados", "MachadoMarfim", "Efeitos", "ImpactoLuzNv2.png"),
                "effect_scale_base": 1.1,
                "animation_sprites": [
                    ("Sprites", "Armas", "Machados", "Machado do Marfim Resplendor", "Ataque", "AT2", f"AT2-base{i}.png") for i in range(5)
                ],
                "animation_speed": 90, "animation_display_scale": 1.2,
                "ui_icon": ("Sprites", "Armas", "Machados", "Machado do Marfim Resplendor", "E2.png")
            },
            2.5: {
                "damage": 70.0, "range": 115.0, "cooldown": 1.4, "name_suffix": "Iluminado +1",
                "hitbox_dim": (105, 105), "hitbox_off": (0, 0),
                "effect_sprite_base": ("Sprites", "Armas", "Machados", "MachadoMarfim", "Efeitos", "ImpactoLuzNv2.png"),
                "effect_scale_base": 1.15,
                "animation_sprites": [
                    ("Sprites", "Armas", "Machados", "Machado do Marfim Resplendor", "Ataque", "AT2", f"AT2-base{i}.png") for i in range(5)
                ],
                "animation_speed": 85, "animation_display_scale": 1.2,
                "ui_icon": ("Sprites", "Armas", "Machados", "Machado do Marfim Resplendor", "E2.png")
            },
            3.0: {
                "damage": 85.0, "range": 130.0, "cooldown": 1.2, "name_suffix": "Divino",
                "hitbox_dim": (110, 110), "hitbox_off": (0, 0),
                "effect_sprite_base": ("Sprites", "Armas", "Machados", "MachadoMarfim", "Efeitos", "ImpactoLuzNv3.png"),
                "effect_scale_base": 1.2,
                "animation_sprites": [
                    ("Sprites", "Armas", "Machados", "Machado do Marfim Resplendor", "Ataque", "AT3", f"AT3-base{i}.png") for i in range(5)
                ],
                "animation_speed": 80, "animation_display_scale": 1.25,
                "ui_icon": ("Sprites", "Armas", "Machados", "Machado do Marfim Resplendor", "E3.png")
            }
        }

        initial_stats = self._get_stats_for_level_internal(self.level, for_super_init=True)
        intended_damage = initial_stats.get("damage", 48.0)
        damage_to_pass_to_base = intended_damage / 0.8 if 0.8 > 0 else intended_damage

        super().__init__(
            name=self._base_name, 
            damage=damage_to_pass_to_base,
            attack_range=initial_stats.get("range", 95.0),
            cooldown=initial_stats.get("cooldown", 1.8),
            level=self.level 
        )

        self.description = initial_stats.get("description", "...")
        self.rarity = initial_stats.get("rarity", "...")
        self.weapon_type = initial_stats.get("weapon_type", "...")
        self.element = initial_stats.get("element", "...")
        
        self.ui_icon = None
        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 100
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.15

        self._apply_level_stats()

    @staticmethod
    def _obter_pasta_raiz_jogo():
        # Navega para cima a partir de /Jogo/Arquivos/Armas/ para a pasta raiz /Jogo
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", "..", ".."))

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        if for_super_init:
            return self._stats_by_level[1.0]
        return self._stats_by_level.get(level_to_check, self._stats_by_level[1.0])

    def _load_ui_icon(self, caminhos_segmentados):
        """Carrega a imagem do ícone da arma para a UI."""
        if not caminhos_segmentados:
            self.ui_icon = None
            return
        
        project_root = self._obter_pasta_raiz_jogo()
        full_path = os.path.join(project_root, *caminhos_segmentados)
        try:
            if os.path.exists(full_path):
                self.ui_icon = pygame.image.load(full_path).convert_alpha()
            else:
                print(f"AVISO(MachadoMarfim): Ícone de UI não encontrado em '{full_path}'.")
                self.ui_icon = None
        except pygame.error as e:
            print(f"ERRO(MachadoMarfim): Falha ao carregar ícone de UI '{full_path}': {e}.")
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
                    print(f"AVISO(MachadoMarfim): Sprite de animação ATK não encontrado em '{full_path}'.")
            except pygame.error as e:
                print(f"ERRO(MachadoMarfim): Falha ao carregar '{full_path}': {e}.")
        
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
        else:
            print(f"AVISO(MachadoMarfim): Nível {target_level} inválido. Níveis disponíveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        
        self.damage = stats["damage"]
        self.attack_range = stats["range"]
        self.cooldown = stats["cooldown"]
        self.name = f"{self._base_name} {stats.get('name_suffix', '')}".strip()
        
        self.hitbox_width, self.hitbox_height = stats.get("hitbox_dim", (90, 90))
        self.hitbox_offset_x, self.hitbox_offset_y = stats.get("hitbox_off", (0, 0))
        self.attack_animation_speed = stats.get("animation_speed", 100)
        self.description = stats.get("description", self.description)
        self.rarity = stats.get("rarity", self.rarity)
        
        # Carrega o ícone
        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path:
            self._load_ui_icon(new_ui_icon_path)

        # Carrega a animação de ataque
        new_animation_paths = stats.get("animation_sprites")
        new_animation_display_scale = stats.get("animation_display_scale", 1.0)
        if new_animation_paths:
            self._load_weapon_attack_animation_sprites(new_animation_paths, new_animation_display_scale)
            
    def get_current_attack_animation_sprite(self):
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None

# Bloco de teste...
if __name__ == '__main__':
    pass
