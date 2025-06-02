# Armas/EspadaFogoAzul.py
import pygame
import os
# Assume que weapon.py está no mesmo diretório 'Armas' ou em um local acessível via Python path
from weapon import Weapon

class EspadaFogoAzul(Weapon):
    """
    Representa a Espada de Fogo Azul Sacra Cerúlea, uma arma com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Espada de Fogo Azul Sacra Cerúlea"
        self.level = 1.0 # Nível inicial

        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name,
            damage=initial_stats_for_super.get("damage", 42.0),
            attack_range=initial_stats_for_super.get("range", 110.0),
            cooldown=initial_stats_for_super.get("cooldown", 1.3),
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (60, 130)), # Exemplo
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (0, 0)),
            description="Uma lâmina elegante que arde com uma chama azul mística.", # Descrição base
            rarity="Épica", # Exemplo
            weapon_type="Espada Longa", # Exemplo
            element="Fogo Azul", # Exemplo
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base", None),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 1.0),
            ui_icon_path=initial_stats_for_super.get("ui_icon", "Sprites/Armas/Espadas/EspadaFogoAzul/Icone_EFA1.png") # Exemplo
        )

        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        # Defina os caminhos e valores REAIS para os seus assets aqui.
        self._stats_by_level = {
            1.0: {
                "damage": 42.0, "range": 75.0, "cooldown": 1.3, "name_suffix": "", # Ajuste range: (largura_jogador/2) + (hitbox_dim[0]/2)
                "hitbox_dim": (70, 110),   # CONFIGURÁVEL
                "hitbox_off": (0, 0),      # CONFIGURÁVEL
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaFogoAzul/Efeitos/ImpactoAzulNv1.png", # Exemplo
                "effect_scale_base": 1.0,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv1/FrameAzul1.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv1/FrameAzul2.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv1/FrameAzul3.png"  # Exemplo
                ],
                "animation_speed": 90,     # CONFIGURÁVEL (ms por frame)
                "animation_display_scale": 1.05, # CONFIGURÁVEL
                "ui_icon": "Sprites/Armas/Espadas/EspadaFogoAzul/Icone_EFA1.png" # Exemplo
            },
            1.5: {
                "damage": 48.0, "range": 80.0, "cooldown": 1.25, "name_suffix": "+1",
                "hitbox_dim": (75, 115), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaFogoAzul/Efeitos/ImpactoAzulNv1.png",
                "effect_scale_base": 1.05,
                "animation_sprites": [ # Reutilizando ou leve variação
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv1/FrameAzul1.png",
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv1/FrameAzul2.png",
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv1/FrameAzul3.png"
                ],
                "animation_speed": 85,
                "animation_display_scale": 1.05,
                "ui_icon": "Sprites/Armas/Espadas/EspadaFogoAzul/Icone_EFA1.png"
            },
            2.0: {
                "damage": 60.0, "range": 85.0, "cooldown": 1.1, "name_suffix": " Cerúlea",
                "hitbox_dim": (80, 120), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaFogoAzul/Efeitos/ImpactoAzulNv2.png", # Exemplo
                "effect_scale_base": 1.1,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv2/FrameCeruleo1.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv2/FrameCeruleo2.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv2/FrameCeruleo3.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv2/FrameCeruleo4.png"  # Exemplo
                ],
                "animation_speed": 80,
                "animation_display_scale": 1.1,
                "ui_icon": "Sprites/Armas/Espadas/EspadaFogoAzul/Icone_EFA2.png" # Exemplo
            },
            2.5: {
                "damage": 65.0, "range": 90.0, "cooldown": 1.05, "name_suffix": " Cerúlea +1",
                "hitbox_dim": (85, 125), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaFogoAzul/Efeitos/ImpactoAzulNv2.png",
                "effect_scale_base": 1.15,
                "animation_sprites": [ # Reutilizando
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv2/FrameCeruleo1.png",
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv2/FrameCeruleo2.png",
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv2/FrameCeruleo3.png",
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv2/FrameCeruleo4.png"
                ],
                "animation_speed": 75,
                "animation_display_scale": 1.1,
                "ui_icon": "Sprites/Armas/Espadas/EspadaFogoAzul/Icone_EFA2.png"
            },
            3.0: {
                "damage": 80.0, "range": 95.0, "cooldown": 0.9, "name_suffix": " Sacra Cerúlea",
                "hitbox_dim": (90, 130), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaFogoAzul/Efeitos/ImpactoAzulNv3.png", # Exemplo
                "effect_scale_base": 1.2,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv3/FrameSacro1.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv3/FrameSacro2.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv3/FrameSacro3.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv3/FrameSacro4.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaFogoAzul/Ataque/Nv3/FrameSacro5.png"  # Exemplo
                ],
                "animation_speed": 70,
                "animation_display_scale": 1.15,
                "ui_icon": "Sprites/Armas/Espadas/EspadaFogoAzul/Icone_EFA3.png" # Exemplo
            }
        }

        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 100
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0

        self._apply_level_stats()
        # print(f"DEBUG(EspadaFogoAzul): Espada '{self.name}' criada no Nível {self.level}.")

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        if for_super_init or not hasattr(self, '_stats_by_level') or not self._stats_by_level:
            if hasattr(self, '_stats_by_level') and self._stats_by_level and 1.0 in self._stats_by_level:
                return self._stats_by_level[1.0]
            else:
                return {
                    "damage": 42.0, "range": 110.0, "cooldown": 1.3, "name_suffix": "",
                    "hitbox_dim": (60, 130), "hitbox_off": (0, 0),
                    "effect_sprite_base": "Sprites/Armas/Espadas/EspadaFogoAzul/Efeitos/ImpactoAzulDefault.png",
                    "effect_scale_base": 1.0,
                    "animation_sprites": [], "animation_speed": 100, "animation_display_scale": 1.0,
                    "ui_icon": "Sprites/Armas/Espadas/EspadaFogoAzul/Icone_DefaultEFA.png"
                }
        if level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else:
            print(f"WARN(EspadaFogoAzul): Nível {level_to_check} não encontrado. Usando fallback para o primeiro nível.")
            first_level_key = next(iter(self._stats_by_level))
            return self._stats_by_level[first_level_key]

    def _load_weapon_attack_animation_sprites(self, caminhos, escala_animacao=1.0):
        sprites_carregados = []
        base_dir_arma = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir_arma)

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
                        print(f"WARN(EspadaFogoAzul): Escala inválida para '{full_path}'. Placeholder.")
                        ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 0.1)))
                        placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((0,0,255,100)) # Placeholder azul
                        sprites_carregados.append(placeholder)
                else:
                    print(f"WARN(EspadaFogoAzul): Sprite de animação ATK não encontrado '{full_path}'. Placeholder.")
                    ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                    placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((0,0,255,100)) # Placeholder azul
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"ERROR(EspadaFogoAzul): Erro ao carregar sprite ATK '{full_path}': {e}. Placeholder.")
                ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((0,0,255,100)) # Placeholder azul
                sprites_carregados.append(placeholder)
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0
        # print(f"DEBUG(EspadaFogoAzul): {len(sprites_carregados)} sprites ATK carregados para {self.name} escala {escala_animacao}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            # print(f"DEBUG(EspadaFogoAzul): '{self.name}' evoluiu para Nível {self.level}!")
        else:
            print(f"WARN(EspadaFogoAzul): Nível {target_level} inválido. Níveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        if not stats:
            print(f"ERROR(EspadaFogoAzul): Falha crítica ao obter stats para Nível {self.level} de '{self.name}'.")
            return

        self.damage = stats["damage"]
        self.attack_range = stats["range"]
        self.cooldown = stats["cooldown"]

        if "hitbox_dim" in stats:
            self.hitbox_width = stats["hitbox_dim"][0]
            self.hitbox_height = stats["hitbox_dim"][1]
        if "hitbox_off" in stats:
            self.hitbox_offset_x = stats["hitbox_off"][0]
            self.hitbox_offset_y = stats["hitbox_off"][1]

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
                    print(f"WARN(EspadaFogoAzul): Escala do efeito ATK inválida para '{self.attack_effect_sprite_path}'.")

        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path and new_ui_icon_path != self.ui_icon_path:
            self.ui_icon_path = new_ui_icon_path

        new_animation_paths = stats.get("animation_sprites")
        new_animation_display_scale = stats.get("animation_display_scale", 1.0)

        if new_animation_paths is not None:
            if new_animation_paths != self.attack_animation_paths or \
               new_animation_display_scale != self.animation_display_scale_factor or \
               not self.attack_animation_paths:
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

# --- Bloco de Teste Standalone ---
if __name__ == '__main__':
    # Mocks para teste standalone
    class MockPygameSurface:
        def __init__(self, width=100, height=100, color=(0,0,0)):
            self._width = width; self._height = height; self.color = color
        def get_width(self): return self._width
        def get_height(self): return self._height
        def convert_alpha(self): return self
        def fill(self, color): self.color = color
            
    class MockPygameImage:
        def load(self, path):
            if "placeholder" in path.lower() or ("naoexiste" in path.lower() and not os.path.exists(path)): # Adicionado cheque original
                 return MockPygameSurface(10,10, (0,0,255)) # Placeholder azul para Fogo Azul
            return MockPygameSurface()

    class MockPygameTransform:
        def smoothscale(self, surface, dimensions):
            return MockPygameSurface(dimensions[0], dimensions[1], surface.color)

    class MockPygame:
        image = MockPygameImage(); transform = MockPygameTransform()
        SRCALPHA = "SRCALPHA_FLAG"; error = type('MockPygameError', (Exception,), {})
        def Surface(self, dimensions, flags=0): return MockPygameSurface(dimensions[0], dimensions[1])

    pygame = MockPygame()

    class BaseWeaponMock:
        def __init__(self, name, damage, attack_range, cooldown, hitbox_dimensions, hitbox_offset,
                     description, rarity, weapon_type, element,
                     attack_effect_sprite_path, attack_effect_scale, ui_icon_path):
            self.name = name; self.damage = damage; self.attack_range = attack_range; self.cooldown = cooldown
            self.hitbox_width, self.hitbox_height = hitbox_dimensions
            self.hitbox_offset_x, self.hitbox_offset_y = hitbox_offset
            self.description = description; self.rarity = rarity; self.weapon_type = weapon_type; self.element = element
            self.attack_effect_sprite_path = attack_effect_sprite_path
            self.attack_effect_scale = attack_effect_scale
            self.ui_icon_path = ui_icon_path
            self.attack_effect_original_image = None; self.attack_effect_image = None
        def _load_attack_effect_sprite(self):
            if self.attack_effect_sprite_path:
                self.attack_effect_original_image = pygame.image.load(self.attack_effect_sprite_path)
                if self.attack_effect_original_image:
                    w = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                    h = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                    if w > 0 and h > 0: self.attack_effect_im