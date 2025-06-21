import pygame
import os
# Garante que a classe base Weapon seja importada do local correto
from .weapon import Weapon

class EspadaCaida(Weapon):
    """
    Representa a Espada Caída, uma arma lendária com poder sombrio,
    níveis de evolução e animação de ataque própria.
    """
    def __init__(self):
        # 1. Nome base da arma
        self._base_name = "Espada Caída"
        self.level = 1.0  # Nível inicial

        # 2. Estatísticas e sprites para cada nível de evolução
        self._stats_by_level = {
            1.0: {
                "damage": 35.0,      # Dano inicial alto
                "range": 40.0,
                "cooldown": 0.8,     # Ataque um pouco mais lento
                "name_suffix": "",
                "hitbox_dim": (10, 20),
                "hitbox_off": (100, 10),
                
                # --- SUBSTITUA PELOS CAMINHOS DOS SEUS SPRITES ---
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaCaida/Efeitos/ImpactoSombrio.png",
                "effect_scale_base": 1.2,
                "animation_sprites": [
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT1//AT1-base0.png",
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT1//AT1-base1.png",
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT1//AT1-base2.png",
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT1//AT1-base3.png",
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT1//AT1-base4.png",
                ],
                "animation_speed": 90,
                "animation_display_scale": 0.16,
                "ui_icon": "Sprites//Armas//Espadas//Espada Sacra Caida//Espada dos Corrompidos -E1.png"
            },
            2.0: {
                "damage": 50.0, "range": 90.0, "cooldown": 0.75, "name_suffix": "Corrompida",
                "hitbox_dim": (140, 95),
                "hitbox_off": (80, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaCaida/Efeitos/ImpactoSombrio.png",
                "effect_scale_base": 0.5,
                "animation_sprites": [ 
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT2//AT2-base0.png",
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT2//AT2-base1.png",
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT2//AT2-base2.png",
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT2//AT2-base3.png",
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT2//AT2-base4.png",
                ],
                "animation_speed": 80,
                "animation_display_scale": 0.1,
                "ui_icon": "Sprites//Armas//Espadas//Espada Sacra Caida//Espada dos Corrompidos -E2.png"
            },
            3.0: {
                "damage": 70.0, "range": 100.0, "cooldown": 0.7, "name_suffix": "do Abismo",
                "hitbox_dim": (150, 100),
                "hitbox_off": (90, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaCaida/Efeitos/ImpactoAbissal.png",
                "effect_scale_base": 1.4,
                "animation_sprites": [
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT3//AT3-base0.png",
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT3//AT3-base1.png",
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT3//AT3-base2.png",
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT3//AT3-base3.png",
                    "Sprites//Armas//Espadas//Espada Sacra Caida//Ataque//AT3//AT3-base4.png",
                ],
                "animation_speed": 75,
                "animation_display_scale": 1.3,
                "ui_icon": "Sprites//Armas//Espadas//Espada Sacra Caida//Espada dos Corrompidos -E3.png"
            }
        }

        # 3. Passe os valores iniciais e a descrição para a classe base
        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)
        super().__init__(
            name=self._base_name,
            damage=initial_stats_for_super.get("damage", 35.0),
            attack_range=initial_stats_for_super.get("range", 85.0),
            cooldown=initial_stats_for_super.get("cooldown", 0.8),
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (60, 60)),
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (75, 0)),
            description="Relíquia de um herói esquecido, agora maculada por uma energia sombria.",
            rarity="Lendária",
            weapon_type="Espada",
            element="Sombras", # Elemento da arma
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base"),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 1.0),
            ui_icon_path=initial_stats_for_super.get("ui_icon")
        )

        # O restante da lógica é genérico e não precisa ser alterado.
        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 100
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0

        self._apply_level_stats()

    # --- MÉTODOS GENÉRICOS (NÃO PRECISAM DE ALTERAÇÃO) ---
    
    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        if for_super_init:
            return self._stats_by_level.get(level_to_check, self._stats_by_level.get(1.0, {}))

        if level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else:
            print(f"WARN({self.__class__.__name__}): Nível {level_to_check} não encontrado. Usando fallback para o primeiro nível.")
            first_level_key = next(iter(self._stats_by_level))
            return self._stats_by_level[first_level_key]

    def _load_weapon_attack_animation_sprites(self, caminhos, escala_animacao=1.0):
        sprites_carregados = []
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        except NameError:
            project_root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

        if not caminhos:
            self.attack_animation_sprites = []
            return

        for path_relativo in caminhos:
            path_corrigido = path_relativo.replace("\\", os.sep).replace("/", os.sep)
            full_path = os.path.join(project_root, path_corrigido)
            
            try:
                if os.path.exists(full_path):
                    imagem_original = pygame.image.load(full_path).convert_alpha()
                    novo_w = int(imagem_original.get_width() * escala_animacao)
                    novo_h = int(imagem_original.get_height() * escala_animacao)
                    if novo_w > 0 and novo_h > 0:
                        imagem = pygame.transform.smoothscale(imagem_original, (novo_w, novo_h))
                        sprites_carregados.append(imagem)
                    else:
                        raise ValueError("Dimensões de sprite inválidas após escala.")
                else:
                    print(f"!!! WARN({self.__class__.__name__}): CAMINHO NÃO EXISTE: '{full_path}'.")
                    placeholder = pygame.Surface((50, 50), pygame.SRCALPHA); placeholder.fill((50,50,50,150))
                    sprites_carregados.append(placeholder)
            except (pygame.error, ValueError) as e:
                print(f"!!! ERROR({self.__class__.__name__}): Erro ao carregar '{full_path}': {e}.")
                placeholder = pygame.Surface((50, 50), pygame.SRCALPHA); placeholder.fill((255,0,0,150))
                sprites_carregados.append(placeholder)
        
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0

    def start_attack_animation(self):
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = pygame.time.get_ticks()

    def update_animation(self, current_ticks):
        if not self.attack_animation_sprites:
            return
        if current_ticks - self.last_attack_animation_update > self.attack_animation_speed:
            self.last_attack_animation_update = current_ticks
            if len(self.attack_animation_sprites) > 0:
                self.current_attack_animation_frame = (self.current_attack_animation_frame + 1) % len(self.attack_animation_sprites)

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
        else:
            print(f"WARN({self.__class__.__name__}): Nível {target_level} inválido. Níveis disponíveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        if not stats:
            print(f"ERROR({self.__class__.__name__}): Falha crítica ao obter stats para Nível {self.level} de '{self.name}'.")
            return

        self.damage = stats["damage"]
        self.attack_range = stats["range"]
        self.cooldown = stats["cooldown"]

        if "hitbox_dim" in stats: self.hitbox_width, self.hitbox_height = stats["hitbox_dim"]
        if "hitbox_off" in stats: self.hitbox_offset_x, self.hitbox_offset_y = stats["hitbox_off"]

        new_effect_path = stats.get("effect_sprite_base")
        new_effect_scale = stats.get("effect_scale_base", self.attack_effect_scale)

        if new_effect_path and new_effect_path != self.attack_effect_sprite_path:
            self.attack_effect_sprite_path = new_effect_path
            self.attack_effect_scale = new_effect_scale
            super()._load_attack_effect_sprite()
        elif new_effect_scale != self.attack_effect_scale and self.attack_effect_original_image:
            self.attack_effect_scale = new_effect_scale
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

        new_anim_paths = stats.get("animation_sprites")
        new_anim_scale = stats.get("animation_display_scale", 1.0)
        
        if new_anim_paths is not None and (new_anim_paths != self.attack_animation_paths or new_anim_scale != self.animation_display_scale_factor or not self.attack_animation_sprites):
            self.attack_animation_paths = new_anim_paths
            self.animation_display_scale_factor = new_anim_scale
            self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)

        self.attack_animation_speed = stats.get("animation_speed", 100)
        name_suffix = stats.get("name_suffix", "")
        self.name = f"{self._base_name} {name_suffix}".strip()

    def get_current_attack_animation_sprite(self):
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None