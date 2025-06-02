# Armas/MachadoDoFogoAbrasador.py
import pygame
import os
# Importa a classe base para machados.
from MachadoBase import MachadoBase

class MachadoDoFogoAbrasador(MachadoBase):
    """
    Representa o Machado do Fogo Abrasador, uma arma com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Machado do Fogo Abrasador"
        self.level = 1.0 # Nível inicial

        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name,
            damage=initial_stats_for_super.get("damage", 28.0), # PLACEHOLDER
            attack_range=initial_stats_for_super.get("range", 95.0), # PLACEHOLDER
            cooldown=initial_stats_for_super.get("cooldown", 2.1), # PLACEHOLDER
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (90, 100)), # PLACEHOLDER
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (0, 0)), # PLACEHOLDER
            description="Deixa um rastro de cinzas.", # Descrição base da loja
            rarity="Épico", # SUGESTÃO
            weapon_type="Machado de Duas Mãos", # SUGESTÃO
            element="Fogo", # Definido pelo nome
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base", None),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 1.0),
            # Ícone da loja é "Sprites/Armas/Machados/Machado do Fogo Abrasador/E1.jpg"
            ui_icon_path=initial_stats_for_super.get("ui_icon", "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Icone_MFA1.png") # PLACEHOLDER
        )

        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        # Defina os caminhos e valores REAIS para os seus assets aqui.
        self._stats_by_level = {
            1.0: {
                "damage": 28.0, "range": 95.0, "cooldown": 2.1, "name_suffix": "",
                "hitbox_dim": (90, 100),   # PLACEHOLDER
                "hitbox_off": (0, 0),     # PLACEHOLDER
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Efeitos/ImpactoChamaNv1.png", # PLACEHOLDER
                "effect_scale_base": 1.0,
                "animation_sprites": [
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv1/ChamaFrame1.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv1/ChamaFrame2.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv1/ChamaFrame3.png"  # PLACEHOLDER
                ],
                "animation_speed": 115,    # PLACEHOLDER (ms por frame)
                "animation_display_scale": 1.2, # PLACEHOLDER
                "ui_icon": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Icone_MFA1.png" # PLACEHOLDER
            },
            1.5: {
                "damage": 34.0, "range": 100.0, "cooldown": 2.0, "name_suffix": "+1",
                "hitbox_dim": (95, 105), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Efeitos/ImpactoChamaNv1.png", # PLACEHOLDER
                "effect_scale_base": 1.05,
                "animation_sprites": [
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv1/ChamaFrame1.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv1/ChamaFrame2.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv1/ChamaFrame3.png"  # PLACEHOLDER
                ],
                "animation_speed": 110,
                "animation_display_scale": 1.2,
                "ui_icon": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Icone_MFA1.png" # PLACEHOLDER
            },
            2.0: {
                "damage": 42.0, "range": 110.0, "cooldown": 1.8, "name_suffix": "Infernal", # SUGESTÃO
                "hitbox_dim": (100, 110), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Efeitos/ImpactoChamaNv2.png", # PLACEHOLDER
                "effect_scale_base": 1.1,
                "animation_sprites": [
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv2/InfernalFrame1.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv2/InfernalFrame2.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv2/InfernalFrame3.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv2/InfernalFrame4.png"  # PLACEHOLDER
                ],
                "animation_speed": 100,
                "animation_display_scale": 1.25,
                "ui_icon": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Icone_MFA2.png" # PLACEHOLDER
            },
            2.5: {
                "damage": 50.0, "range": 115.0, "cooldown": 1.7, "name_suffix": "Infernal +1",
                "hitbox_dim": (105, 115), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Efeitos/ImpactoChamaNv2.png", # PLACEHOLDER
                "effect_scale_base": 1.15,
                "animation_sprites": [
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv2/InfernalFrame1.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv2/InfernalFrame2.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv2/InfernalFrame3.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv2/InfernalFrame4.png"  # PLACEHOLDER
                ],
                "animation_speed": 95,
                "animation_display_scale": 1.25,
                "ui_icon": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Icone_MFA2.png" # PLACEHOLDER
            },
            3.0: {
                "damage": 60.0, "range": 130.0, "cooldown": 1.5, "name_suffix": "Cataclísmico", # SUGESTÃO
                "hitbox_dim": (110, 120), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Efeitos/ImpactoChamaNv3.png", # PLACEHOLDER
                "effect_scale_base": 1.2,
                "animation_sprites": [
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv3/CataclismoFrame1.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv3/CataclismoFrame2.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv3/CataclismoFrame3.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv3/CataclismoFrame4.png", # PLACEHOLDER
                    "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Ataque/Nv3/CataclismoFrame5.png"  # PLACEHOLDER
                ],
                "animation_speed": 90,
                "animation_display_scale": 1.3,
                "ui_icon": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Icone_MFA3.png" # PLACEHOLDER
            }
        }

        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 100
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0

        self._apply_level_stats()
        # print(f"DEBUG(MachadoDoFogoAbrasador): Machado '{self.name}' criado no Nível {self.level}.")

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        if for_super_init or not hasattr(self, '_stats_by_level') or not self._stats_by_level:
            if hasattr(self, '_stats_by_level') and self._stats_by_level and 1.0 in self._stats_by_level:
                return self._stats_by_level[1.0]
            else: # Absolute fallback for super().__init__()
                return { 
                    "damage": 28.0, "range": 95.0, "cooldown": 2.1, "name_suffix": "",
                    "hitbox_dim": (90, 100), "hitbox_off": (0, 0),
                    "effect_sprite_base": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Efeitos/ImpactoChamaDefault.png", # PLACEHOLDER
                    "effect_scale_base": 1.0,
                    "animation_sprites": [], "animation_speed": 115, "animation_display_scale": 1.2,
                    "ui_icon": "Sprites/Armas/Machados/MachadoDoFogoAbrasador/Icone_DefaultMFA.png" # PLACEHOLDER
                }

        if level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else:
            print(f"WARN(MachadoDoFogoAbrasador): Nível {level_to_check} não encontrado. Usando fallback para o primeiro nível.")
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
                        print(f"WARN(MachadoDoFogoAbrasador): Escala inválida para '{full_path}'. Placeholder.")
                        ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 0.1)))
                        placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((255,100,0,100)) # Placeholder Laranja/Fogo
                        sprites_carregados.append(placeholder)
                else:
                    print(f"WARN(MachadoDoFogoAbrasador): Sprite de animação ATK não encontrado '{full_path}'. Placeholder.")
                    ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                    placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((255,100,0,100))
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"ERROR(MachadoDoFogoAbrasador): Erro ao carregar sprite ATK '{full_path}': {e}. Placeholder.")
                ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((255,100,0,100))
                sprites_carregados.append(placeholder)
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0
        # print(f"DEBUG(MachadoDoFogoAbrasador): {len(sprites_carregados)} sprites ATK carregados para {self.name} escala {escala_animacao}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            # print(f"DEBUG(MachadoDoFogoAbrasador): '{self.name}' evoluiu para Nível {self.level}!")
        else:
            print(f"WARN(MachadoDoFogoAbrasador): Nível {target_level} inválido. Níveis disponíveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        if not stats:
            print(f"ERROR(MachadoDoFogoAbrasador): Falha crítica ao obter stats para Nível {self.level} de '{self.name}'.")
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
                        print(f"WARN(MachadoDoFogoAbrasador): Escala do efeito ATK inválida para '{self.attack_effect_sprite_path}'.")
        else:
            self.attack_effect_sprite_path = new_base_effect_path
            self.attack_effect_scale = new_base_effect_scale
            # print(f"WARN(MachadoDoFogoAbrasador): MachadoBase não possui _load_attack_effect_sprite. Efeitos podem não ser carregados visualmente.")

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

# --- Bloco de Teste Standalone ---
if __name__ == '__main__':
    class MockPygameSurface:
        def __init__(self, width=100, height=100, color=(0,0,0)):
            self._width = width; self._height = height; self.color = color
        def get_width(self): return self._width
        def get_height(self): return self._height
        def convert_alpha(self): return self
        def fill(self, color): self.color = color
            
    class MockPygameImage:
        def load(self, path):
            if "placeholder" in path.lower() or ("naoexiste" in path.lower() and not original_os_path_exists(path)):
                return MockPygameSurface(10,10, (255,100,0)) # Placeholder Laranja/Fogo
            return MockPygameSurface()

    class MockPygameTransform:
        def smoothscale(self, surface, dimensions):
            return MockPygameSurface(dimensions[0], dimensions[1], surface.color)

    class MockPygame:
        image = MockPygameImage(); transform = MockPygameTransform()
        SRCALPHA = "SRCALPHA_FLAG"; error = type('MockPygameError', (Exception,), {})
        def Surface(self, dimensions, flags=0): return MockPygameSurface(dimensions[0], dimensions[1])

    pygame = MockPygame()

    class MockMachadoBase:
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
            # print(f"MockMachadoBase '{name}' inicializado.")

        def _load_attack_effect_sprite(self):
            # print(f"MockMachadoBase: _load_attack_effect_sprite() chamado para {self.attack_effect_sprite_path}")
            if self.attack_effect_sprite_path:
                self.attack_effect_original_image = pygame.image.load(self.attack_effect_sprite_path)
                if self.attack_effect_original_image:
                    w = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                    h = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                    if w > 0 and h > 0: self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (w,h))
                    else: self.attack_effect_image = None
            else: self.attack_effect_original_image = None; self.attack_effect_image = None

    MachadoBase = MockMachadoBase

    original_os_path_exists = os.path.exists
    def mock_os_path_exists(path):
        if "naoexiste" in path: return False
        return True
    os.path.exists = mock_os_path_exists

    print("\n--- INICIANDO TESTE STANDALONE DO MACHADO DO FOGO ABRASADOR ---")
    machado_fa_teste = MachadoDoFogoAbrasador()
    print(f"Machado Criado: '{machado_fa_teste.name}', Nível: {machado_fa_teste.level}, Dano: {machado_fa_teste.damage}")
    print(f"  Descrição: {machado_fa_teste.description}")
    print(f"  Ícone UI: {machado_fa_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {machado_fa_teste.attack_animation_paths}")
    print(f"  Sprite ATK (Frame 0): {machado_fa_teste.get_current_attack_animation_sprite()}")

    print("\n--- Testando Evolução para Nível 2.0 (Machado do Fogo Abrasador) ---")
    machado_fa_teste.evolve(2.0)
    print(f"Machado Evoluído: '{machado_fa_teste.name}', Nível: {machado_fa_teste.level}, Dano: {machado_fa_teste.damage}")
    print(f"  Ícone UI: {machado_fa_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {machado_fa_teste.attack_animation_paths}")

    print("\n--- Testando Evolução para Nível 3.0 (Machado do Fogo Abrasador) ---")
    machado_fa_teste.evolve(3.0)
    print(f"Machado Evoluído: '{machado_fa_teste.name}', Nível: {machado_fa_teste.level}, Dano: {machado_fa_teste.damage}")
    print(f"  Caminho Efeito ATK: {machado_fa_teste.attack_effect_sprite_path}, Escala: {machado_fa_teste.attack_effect_scale}")
    
    print("\n--- Testando Evolução para Nível Inválido (5.0) ---")
    machado_fa_teste.evolve(5.0)
    print(f"Após tentar evoluir para 5.0: '{machado_fa_teste.name}', Nível: {machado_fa_teste.level} (deve ser 3.0)")

    print("\n--- FIM DO TESTE STANDALONE (Machado do Fogo Abrasador) ---")
    os.path.exists = original_os_path_exists