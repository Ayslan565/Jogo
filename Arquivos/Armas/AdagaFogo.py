# Armas/AdagaFogo.py
import pygame
import os
# Importa a classe base Weapon. O '.' indica um import relativo do mesmo pacote ('Armas').
from .weapon import Weapon

class AdagaFogo(Weapon):
    """
    Representa a Adaga de Fogo, uma arma ágil com múltiplos níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        # Nome base usado para evoluções e identificação.
        self._base_name = "Adaga de Fogo"
        self.level = 1.0 # Nível inicial da arma.

        # Obtém os stats iniciais para o nível 1.0 para o construtor da classe base.
        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        # Chama o construtor da classe pai (Weapon) com os valores iniciais.
        super().__init__(
            name=self._base_name,
            damage=initial_stats_for_super.get("damage", 15.0),
            attack_range=initial_stats_for_super.get("range", 55.0),
            cooldown=initial_stats_for_super.get("cooldown", 0.5),
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (40, 60)),
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (10, 0)),
            description="Uma adaga rápida que queima ao toque.",
            rarity="Comum",
            weapon_type="Adaga",
            element="Fogo",
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base", None),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 1.0),
            ui_icon_path=initial_stats_for_super.get("ui_icon", "Sprites/Armas/Adagas/AdagaFogo/Icone_E1.png")
        )

        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        # Defina aqui os atributos específicos para cada nível da Adaga de Fogo.
        self._stats_by_level = {
            # Nível 1.0
            1.0: {
                "damage": 15.0,
                "range": 55.0, # Adagas têm menor alcance
                "cooldown": 0.5, # Adagas são mais rápidas
                "name_suffix": "",
                "hitbox_dim": (40, 60),
                "hitbox_off": (10, 0),
                "effect_sprite_base": "Sprites/Armas/Adagas/AdagaFogo/Efeitos/ImpactoNv1.png",
                "effect_scale_base": 0.8,
                "animation_sprites": [
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT1\\AT0-base0.png", 
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT1\\AT1-base1.png", 
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT1\\AT2-base2.png",
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT1\\AT3-base3.png", 
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT1\\AT4-base4.png",
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT1\\AT5-base5.png",
                ], 
                "animation_speed": 60,
                "animation_display_scale":0.4,
                # Caminho RELATIVO à pasta 'Jogo/'
                "ui_icon": "Sprites\\Armas\\Icones\\AdagaFogo_Nv1.png" # Exemplo de ícone para Nv1
            },
            1.5: {
                "damage": 18.0, "range": 48.0, "cooldown": 0.75, "name_suffix": "+1",
                "hitbox_dim": (32, 62), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Adagas/AdagaFogo/Efeitos/ImpactoLeveNv1.png",
                "effect_scale_base": 0.85,
                "animation_sprites": [
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT1\\AT0-base0.png", 
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT1\\AT1-base1.png", 
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT1\\AT2-base2.png",
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT1\\AT3-base3.png", 
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT1\\AT4-base4.png",
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT1\\AT5-base5.png",
                ], 
                "animation_speed": 55, "animation_display_scale": 0.42,
                "ui_icon": "Sprites/Armas/Icones/AdagaFogo_Nv1.png" # Pode ser o mesmo ou diferente
            },
            # Nível 2.0
            2.0: {
                "damage": 22.0,
                "range": 60.0,
                "cooldown": 0.45,
                "name_suffix": " Afiada",
                "hitbox_dim": (45, 65),
                "hitbox_off": (12, 0),
                "effect_sprite_base": "Sprites/Armas/Adagas/AdagaFogo/Efeitos/ImpactoNv2.png",
                "effect_scale_base": 0.9,
                "animation_sprites": [
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT2\\AT2-base0.png", 
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT2\\AT2-base1.png", 
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT2\\AT2-base2.png",
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT2\\AT2-base3.png",
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT2\\AT2-base4.png",
                ], 
                "animation_speed": 50, "animation_display_scale": 0.45,
                "ui_icon": "Sprites\\Armas\\Icones\\AdagaFogo_Nv2.png" # Exemplo de ícone para Nv2
            },
            2.5: {
                "damage": 25.0, "range": 52.0, "cooldown": 0.6, "name_suffix": " Afiada +1",
                "hitbox_dim": (37, 67), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Adagas/AdagaFogo/Efeitos/ImpactoMedioNv2.png",
                "effect_scale_base": 0.95,
                "animation_sprites": [
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT2\\AT2-base0.png", 
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT2\\AT2-base1.png", 
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT2\\AT2-base2.png",
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT2\\AT2-base3.png",
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT2\\AT2-base4.png",
                ], 
                "animation_speed": 45, "animation_display_scale": 0.47,
                "ui_icon": "Sprites/Armas/Icones/AdagaFogo_Nv2.png",
            },
            # Nível 3.0
            3.0: {
                "damage": 30.0,
                "range": 65.0,
                "cooldown": 0.4,
                "name_suffix": " Infernal",
                "hitbox_dim": (50, 70),
                "hitbox_off": (15, 0),
                "effect_sprite_base": "Sprites/Armas/Adagas/AdagaFogo/Efeitos/ImpactoNv3.png",
                "effect_scale_base": 1.0,
                "animation_sprites": [
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT3\\AT3-base0.png", 
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT3\\AT3-base1.png",
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT3\\AT3-base2.png",
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT3\\AT3-base3.png",
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT3\\AT3-base4.png",
                    "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Ataque\\AT2\\AT2-base5.png",
                ], 
                "animation_speed": 40, "animation_display_scale": 0.5,
                "ui_icon": "Sprites\\Armas\\Icones\\AdagaFogo_Nv3.png" # Exemplo de ícone para Nv3
            }
        }

        # Atributos para a animação de ataque da arma
        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 100
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0

        # Aplica os stats do nível inicial para configurar a arma.
        self._apply_level_stats()

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        """Retorna o dicionário de stats para um nível específico, com fallbacks."""
        if for_super_init or not hasattr(self, '_stats_by_level') or not self._stats_by_level:
            return {
                "damage": 15.0, "range": 55.0, "cooldown": 0.5, "name_suffix": "",
                "hitbox_dim": (40, 60), "hitbox_off": (10, 0),
                "effect_sprite_base": "Sprites/Armas/Adagas/AdagaFogo/Efeitos/ImpactoDefault.png",
                "effect_scale_base": 1.0, "animation_sprites": [], "animation_speed": 100,
                "animation_display_scale": 1.0, "ui_icon": "Sprites/Armas/Adagas/AdagaFogo/Icone_Default.png"
            }
        
        if level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else:
            print(f"AVISO(AdagaFogo): Nível {level_to_check} não encontrado. Usando o primeiro nível definido.")
            first_level_key = next(iter(self._stats_by_level))
            return self._stats_by_level[first_level_key]

    def _load_weapon_attack_animation_sprites(self, caminhos, escala_animacao=1.0):
        """Carrega e escala os sprites da animação de ataque da arma."""
        sprites_carregados = []
        try:
            base_dir_arma = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(base_dir_arma)
        except NameError:
            project_root = os.getcwd()

        for path_relativo in caminhos:
            path_relativo_corrigido = path_relativo.replace("\\", os.sep).replace("/", os.sep).lstrip(os.sep)
            full_path = os.path.join(project_root, path_relativo_corrigido)
            try:
                if os.path.exists(full_path):
                    imagem_original = pygame.image.load(full_path).convert_alpha()
                    novo_w = int(imagem_original.get_width() * escala_animacao)
                    novo_h = int(imagem_original.get_height() * escala_animacao)
                    if novo_w > 0 and novo_h > 0:
                        imagem = pygame.transform.smoothscale(imagem_original, (novo_w, novo_h))
                        sprites_carregados.append(imagem)
                    else:
                        print(f"AVISO(AdagaFogo): Escala de animação inválida para '{full_path}'.")
                else:
                    print(f"AVISO(AdagaFogo): Sprite de animação não encontrado '{full_path}'.")
            except pygame.error as e:
                print(f"ERRO(AdagaFogo): Erro ao carregar sprite de animação '{full_path}': {e}")
        
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0

    def evolve(self, target_level: float):
        """Evolui a adaga para um nível específico."""
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
        else:
            print(f"AVISO(AdagaFogo): Nível de evolução {target_level} inválido. Níveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        """Aplica os atributos correspondentes ao nível atual da adaga."""
        stats = self._get_stats_for_level_internal(self.level)
        if not stats:
            return

        self.damage = stats["damage"]
        self.attack_range = stats["range"]
        self.cooldown = stats["cooldown"]

        if "hitbox_dim" in stats:
            self.hitbox_width, self.hitbox_height = stats["hitbox_dim"]
        if "hitbox_off" in stats:
            self.hitbox_offset_x, self.hitbox_offset_y = stats["hitbox_off"]

        new_base_effect_path = stats.get("effect_sprite_base")
        new_base_effect_scale = stats.get("effect_scale_base", self.attack_effect_scale)
        if new_base_effect_path and new_base_effect_path != self.attack_effect_sprite_path:
            self.attack_effect_sprite_path = new_base_effect_path
            self.attack_effect_scale = new_base_effect_scale
            super()._load_attack_effect_sprite()
        elif new_base_effect_scale != self.attack_effect_scale and self.attack_effect_original_image:
            self.attack_effect_scale = new_base_effect_scale
            if self.attack_effect_original_image:
                w = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                h = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                if w > 0 and h > 0:
                    self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (w,h))

        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path and new_ui_icon_path != self.ui_icon_path:
            self.ui_icon_path = new_ui_icon_path

        new_animation_paths = stats.get("animation_sprites")
        new_animation_display_scale = stats.get("animation_display_scale", 1.0)
        if new_animation_paths is not None and (new_animation_paths != self.attack_animation_paths or new_animation_display_scale != self.animation_display_scale_factor or not self.attack_animation_paths):
            self.attack_animation_paths = new_animation_paths
            self.animation_display_scale_factor = new_animation_display_scale
            self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)

        self.attack_animation_speed = stats.get("animation_speed", 100)
        self.name = f"{self._base_name} {stats.get('name_suffix', '')}".strip()

    def get_current_attack_animation_sprite(self):
        """Retorna o sprite atual da animação de ataque da arma."""
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None
