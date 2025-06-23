import pygame
import os
# Assume que weapon.py está no mesmo diretório 'Armas' ou em um local acessível via Python path
from .weapon import Weapon

class LaminaDoCeuCintilante(Weapon):
    """
    Representa a Lâmina do Céu Cintilante, uma arma com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        # --- NOME CORRIGIDO PARA CONSISTÊNCIA ---
        self._base_name = "Lâmina do Céu Cintilante"
        self.level = 1.0 # Nível inicial

        # --- CAMINHOS DOS ARQUIVOS CORRIGIDOS ---
        self._stats_by_level = {
            1.0: {
                "damage": 38.0, "range": 80.0, "cooldown": 0.7, "name_suffix": "",
                "hitbox_dim": (400, 100),
                "hitbox_off": (100, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Efeitos/ImpactoEstelarNv1.png",
                "effect_scale_base": 1.1,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT1/AT1-base0.png",
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT1/AT1-base1.png",
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT1/AT1-base2.png",
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT1/AT1-base3.png",
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT1/AT1-base4.png",
                ],
                "animation_speed": 70,
                "animation_display_scale": 0.25,
                "ui_icon": "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/E1.png" # CORRIGIDO: .jpg para .png
            },
            2.0: {
                "damage": 52.0, "range": 90.0, "cooldown": 0.65, "name_suffix": "Meteórica",
                "hitbox_dim": (400, 100), "hitbox_off": (100, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Efeitos/ImpactoEstelarNv2.png",
                "effect_scale_base": 0.25,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT2/AT2-base0.png",
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT2/AT2-base1.png",
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT2/AT2-base2.png",
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT2/AT2-base3.png",
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT2/AT2-base4.png",
                ],
                "animation_speed": 60,
                "animation_display_scale": 0.25,
                "ui_icon": "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/E2.png" # CORRIGIDO: .jpg para .png
            },
            3.0: {
                "damage": 75.0, "range": 105.0, "cooldown": 0.55, "name_suffix": "da Supernova",
                "hitbox_dim": (400, 100), "hitbox_off": (100, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Efeitos/ImpactoEstelarNv3.png",
                "effect_scale_base": 1.4,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT3/AT3-base0.png",
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT3/AT3-base1.png",
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT3/AT3-base2.png",
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT3/AT3-base3.png",
                    "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/Ataque/AT3/AT3-base4.png",
                ],
                "animation_speed": 50,
                "animation_display_scale": 1.35,
                "ui_icon": "Sprites/Armas/Espadas/Lâmina do Ceu Cintilante/E3.jpg" # Mantido como .jpg conforme a imagem
            }
        }

        # Pega os stats iniciais para passar para a classe mãe
        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name,
            damage=initial_stats_for_super.get("damage", 38.0),
            attack_range=initial_stats_for_super.get("range", 80.0),
            cooldown=initial_stats_for_super.get("cooldown", 0.7),
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (75, 90)),
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (45, 0)),
            description="Forjada com detritos de estrelas e o calor de meteoros.",
            rarity="Lendária",
            weapon_type="Espada",
            element="Cósmico",
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base"),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 1.0),
            ui_icon_path=initial_stats_for_super.get("ui_icon")
        )

        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 100
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0

        self._apply_level_stats()

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        if for_super_init:
            return self._stats_by_level.get(level_to_check, self._stats_by_level.get(1.0, {}))

        if level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else:
            print(f"WARN(Lamina DoCeuCintilante): Nível {level_to_check} não encontrado. Usando fallback para o primeiro nível.")
            first_level_key = next(iter(self._stats_by_level))
            return self._stats_by_level[first_level_key]

    def _load_weapon_attack_animation_sprites(self, caminhos, escala_animacao=1.0):
        sprites_carregados = []
        
        if not caminhos:
            print("DEBUG(Lamina DoCeuCintilante): A lista de caminhos para os sprites de animação está vazia.")
            self.attack_animation_sprites = []
            return

        print(f"--- Carregando Sprites para {self.name} ---")

        for path_relativo in caminhos:
            path_corrigido = path_relativo.replace("\\", os.sep).replace("//", os.sep)
            full_path = path_corrigido
            
            print(f"DEBUG(Lamina DoCeuCintilante): Tentando carregar sprite: '{full_path}'")

            try:
                if os.path.exists(full_path):
                    print(f"SUCCESS(Lamina DoCeuCintilante): Ficheiro encontrado! '{full_path}'")
                    imagem_original = pygame.image.load(full_path).convert_alpha()
                    novo_w = int(imagem_original.get_width() * escala_animacao)
                    novo_h = int(imagem_original.get_height() * escala_animacao)
                    imagem = pygame.transform.smoothscale(imagem_original, (novo_w, novo_h))
                    sprites_carregados.append(imagem)
                else:
                    print(f"!!! WARN(Lamina DoCeuCintilante): CAMINHO NÃO EXISTE: '{full_path}'. A criar placeholder.")
                    placeholder = pygame.Surface((int(50*escala_animacao), int(50*escala_animacao)), pygame.SRCALPHA); placeholder.fill((173, 216, 230, 150)) # Azul claro
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"!!! ERROR(Lamina DoCeuCintilante): Erro ao carregar imagem em '{full_path}': {e}. A criar placeholder.")
                placeholder = pygame.Surface((int(50*escala_animacao), int(50*escala_animacao)), pygame.SRCALPHA); placeholder.fill((255,0,0,150))
                sprites_carregados.append(placeholder)
        
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0
        print(f"--- Carga de sprites para {self.name} concluída. Total de sprites carregados: {len(self.attack_animation_sprites)} ---")

    def start_attack_animation(self):
        """Reinicia a animação de ataque para o primeiro frame."""
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = pygame.time.get_ticks()

    def update_animation(self, current_ticks):
        """Avança o frame da animação de ataque com base na velocidade da animação."""
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
            print(f"WARN(Lamina DoCeuCintilante): Nível {target_level} inválido. Níveis disponíveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        if not stats:
            print(f"ERROR(Lamina DoCeuCintilante): Falha crítica ao obter stats para Nível {self.level} de '{self.name}'.")
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
                width = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                height = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                if width > 0 and height > 0:
                    self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (width, height))
                else:
                    self.attack_effect_image = None

        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path and new_ui_icon_path != self.ui_icon_path:
            self.ui_icon_path = new_ui_icon_path

        new_animation_paths = stats.get("animation_sprites")
        new_animation_display_scale = stats.get("animation_display_scale", 1.0)

        if new_animation_paths is not None:
            if new_animation_paths != self.attack_animation_paths or \
               new_animation_display_scale != self.animation_display_scale_factor or \
               not self.attack_animation_sprites:
                self.attack_animation_paths = new_animation_paths
                self.animation_display_scale_factor = new_animation_display_scale
                self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)

        self.attack_animation_speed = stats.get("animation_speed", 100)
        name_suffix = stats.get("name_suffix", "")
        self.name = f"{self._base_name} {name_suffix}".strip()

    def get_current_attack_animation_sprite(self):
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None