# Armas/MachadoMacabro.py
import pygame
import os
# Importa a classe base para machados.
from .MachadoBase import MachadoBase

class MachadoMacabro(MachadoBase):
    """
    Representa o Machado Macabro da Gula Infinita, uma arma com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Machado Macabro da Gula Infinita"
        self.level = 1.0 # Nível inicial

        # Obtém os stats base para o construtor e para atributos não passados ao MachadoBase.__init__
        initial_stats = self._get_stats_for_level_internal(self.level, for_super_init=True)
        
        # Calcula o dano a ser passado para MachadoBase para compensar sua escala de 0.8
        intended_damage = initial_stats.get("damage", 40.0) # Dano base do nível 1.0 original
        damage_to_pass_to_base = intended_damage / 0.8 if 0.8 > 0 else intended_damage

        # Chama o __init__ de MachadoBase com os parâmetros que ele espera
        super().__init__(
            name=self._base_name, 
            damage=damage_to_pass_to_base,
            attack_range=initial_stats.get("range", 80.0), # Range base do nível 1.0 original
            cooldown=initial_stats.get("cooldown", 2.0),   # Cooldown base do nível 1.0 original
            level=self.level 
        )

        # Atributos descritivos e outros que MachadoBase.__init__ não lida diretamente
        self.description = initial_stats.get("description", "Um machado grotesco que parece faminto, com runas que pulsam com uma luz sinistra.")
        self.rarity = initial_stats.get("rarity", "Mítica")
        self.weapon_type = initial_stats.get("weapon_type", "Machado de Gula") 
        self.element = initial_stats.get("element", "Sombra") # Ou "Profano", "Voraz"
        
        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        self._stats_by_level = {
            1.0: {
                "damage": 40.0, "range": 80.0, "cooldown": 2.0, "name_suffix": "",
                "hitbox_dim": (85, 85),   # CONFIGURÁVEL
                "hitbox_off": (0, 0),      # CONFIGURÁVEL
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoMacabro/Efeitos/ImpactoVorazNv1.png", # Exemplo
                "effect_scale_base": 1.0,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT1/AT1-base0.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT1/AT1-base1.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT1/AT1-base2.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT1/AT1-base3.png",
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT1/AT1-base4.png",  # Exemplo
                ],
                "animation_speed": 115,     # CONFIGURÁVEL (ms por frame)
                "animation_display_scale": 1.2, # CONFIGURÁVEL
                "ui_icon": "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/E-1.png", # Exemplo
                "description": "Um machado grotesco que parece faminto, com runas que pulsam com uma luz sinistra.",
                "rarity": "Mítica",
                "weapon_type": "Machado de Gula",
                "element": "Sombra"
            },
            1.5: {
                "damage": 45.0, "range": 85.0, "cooldown": 1.9, "name_suffix": "+1",
                "hitbox_dim": (90, 90), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoMacabro/Efeitos/ImpactoVorazNv1.png",
                "effect_scale_base": 1.05,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base0.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base1.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base2.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base3.png",
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base4.png",
                ],
                "animation_speed": 110,
                "animation_display_scale": 1.2,
                "ui_icon": "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/E-1.png"
            },
            2.0: {
                "damage": 55.0, "range": 95.0, "cooldown": 1.7, "name_suffix": "Insaciável",
                "hitbox_dim": (95, 95), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoMacabro/Efeitos/ImpactoVorazNv2.png", 
                "effect_scale_base": 1.1,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base0.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base1.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base2.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base3.png",
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base4.png",
                ],
                "animation_speed": 105,
                "animation_display_scale": 1.25,
                "ui_icon": "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/E-2.png" 
            },
            2.5: {
                "damage": 60.0, "range": 100.0, "cooldown": 1.6, "name_suffix": "Insaciável +1",
                "hitbox_dim": (100, 100), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoMacabro/Efeitos/ImpactoVorazNv2.png",
                "effect_scale_base": 1.15,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base0.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base2.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base2.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base3.png",
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT2/AT2-base4.png",                ],
                "animation_speed": 100,
                "animation_display_scale": 1.25,
                "ui_icon": "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/E-2.png"
            },
            3.0: {
                "damage": 75.0, "range": 115.0, "cooldown": 1.4, "name_suffix": "Devorador de Mundos",
                "hitbox_dim": (105, 105), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoMacabro/Efeitos/ImpactoVorazNv3.png", 
                "effect_scale_base": 1.2,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT3/AT3-base0.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT3/AT3-base1.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT3/AT3-base2.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT3/AT3-base3.png",
                    "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/Ataque/AT3/AT3-base4.png",
                ],
                "animation_speed": 95,
                "animation_display_scale": 1.3,
                "ui_icon": "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/E-3.png"
            }
        }

        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 115 # Valor base, será atualizado
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.2 # Valor base, será atualizado

        self._apply_level_stats()
        # print(f"DEBUG(MachadoMacabro): Machado '{self.name}' criado no Nível {self.level}.")

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        if for_super_init:
            return {
                "damage": 40.0, "range": 80.0, "cooldown": 2.0, "name_suffix": "",
                "hitbox_dim": (85, 85), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoMacabro/Efeitos/ImpactoVorazDefault.png",
                "effect_scale_base": 1.0,
                "animation_sprites": [], "animation_speed": 115, "animation_display_scale": 1.2,
                "ui_icon": "Sprites/Armas/Machados/MachadoMacabro/Icone_DefaultMM.png",
                "description": "Um machado grotesco que parece faminto, com runas que pulsam com uma luz sinistra.",
                "rarity": "Mítica",
                "weapon_type": "Machado de Gula",
                "element": "Sombra"
            }

        if hasattr(self, '_stats_by_level') and self._stats_by_level and level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else:
            if hasattr(self, '_stats_by_level') and self._stats_by_level:
                print(f"WARN(MachadoMacabro): Nível {level_to_check} não encontrado. Usando fallback para o primeiro nível.")
                first_level_key = next(iter(self._stats_by_level))
                return self._stats_by_level[first_level_key]
            else:
                print(f"ERROR(MachadoMacabro): _stats_by_level não definido ao tentar buscar nível {level_to_check}.")
                return { # Fallback extremo
                    "damage": 40.0, "range": 80.0, "cooldown": 2.0, "name_suffix": "",
                    "hitbox_dim": (85, 85), "hitbox_off": (0, 0),
                    "effect_sprite_base": "Sprites/Armas/Machados/MachadoMacabro/Efeitos/ImpactoVorazDefault.png",
                    "effect_scale_base": 1.0, "animation_sprites": [], "animation_speed": 115,
                    "animation_display_scale": 1.2, "ui_icon": "Sprites/Armas/Machados/MachadoMacabro/Icone_DefaultMM.png",
                    "description": "Um machado grotesco que parece faminto, com runas que pulsam com uma luz sinistra.",
                    "rarity": "Mítica", "weapon_type": "Machado de Gula", "element": "Sombra"
                }

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
                        print(f"WARN(MachadoMacabro): Escala inválida para '{full_path}'. Placeholder.")
                        ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 0.1)))
                        placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((75,0,130,100)) # Placeholder Roxo Escuro
                        sprites_carregados.append(placeholder)
                else:
                    print(f"WARN(MachadoMacabro): Sprite de animação ATK não encontrado '{full_path}'. Placeholder.")
                    ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                    placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((75,0,130,100))
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"ERROR(MachadoMacabro): Erro ao carregar sprite ATK '{full_path}': {e}. Placeholder.")
                ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((75,0,130,100))
                sprites_carregados.append(placeholder)
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
        else:
            print(f"WARN(MachadoMacabro): Nível {target_level} inválido. Níveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        if not stats:
            print(f"ERROR(MachadoMacabro): Falha crítica ao obter stats para Nível {self.level} de '{self.name}'.")
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
                        print(f"WARN(MachadoMacabro): Escala do efeito ATK inválida para '{self.attack_effect_sprite_path}'.")
        else:
            self.attack_effect_sprite_path = new_base_effect_path
            self.attack_effect_scale = new_base_effect_scale
            # print(f"WARN(MachadoMacabro): MachadoBase não possui _load_attack_effect_sprite.")

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
        
        self.description = stats.get("description", self.description)
        self.rarity = stats.get("rarity", self.rarity)
        self.weapon_type = stats.get("weapon_type", self.weapon_type)
        self.element = stats.get("element", self.element)

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
                 return MockPygameSurface(10,10, (75,0,130)) # Placeholder Roxo Escuro
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
        def __init__(self, name, damage, attack_range, cooldown, level):
            self.name = name
            self.damage_passed_to_weapon = damage 
            self.attack_range = attack_range
            self.cooldown = cooldown
            self.level = level
            self.attack_type = "vertical"
            self.hitbox_width = 0; self.hitbox_height = 0; self.hitbox_offset_x = 0; self.hitbox_offset_y = 0
            self.description = ""; self.rarity = ""; self.weapon_type = ""; self.element = ""
            self.attack_effect_sprite_path = None; self.attack_effect_scale = 1.0
            self.ui_icon_path = None
            self.attack_effect_original_image = None; self.attack_effect_image = None

        def _load_attack_effect_sprite(self):
            if hasattr(self, 'attack_effect_sprite_path') and self.attack_effect_sprite_path:
                self.attack_effect_original_image = pygame.image.load(self.attack_effect_sprite_path)
                if self.attack_effect_original_image:
                    w = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                    h = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                    if w > 0 and h > 0: self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (w,h))
                    else: self.attack_effect_image = None
            else: self.attack_effect_original_image = None; self.attack_effect_image = None
        
        def get_attack_hitbox(self, player_rect, player_direction, attack_hitbox_size):
            return pygame.Rect(0,0, attack_hitbox_size[0], attack_hitbox_size[1])

    MachadoBase = MockMachadoBase 

    original_os_path_exists = os.path.exists
    def mock_os_path_exists(path):
        if "naoexiste" in path: return False
        return True
    os.path.exists = mock_os_path_exists

    print("\n--- INICIANDO TESTE STANDALONE DO MACHADO MACABRO ---")
    machado_m_teste = MachadoMacabro()
    print(f"Machado Criado: '{machado_m_teste.name}', Nível: {machado_m_teste.level}, Dano Final: {machado_m_teste.damage}")
    print(f"  Descrição: {machado_m_teste.description}, Raridade: {machado_m_teste.rarity}")
    print(f"  Tipo: {machado_m_teste.weapon_type}, Elemento: {machado_m_teste.element}, Tipo Ataque: {machado_m_teste.attack_type}")
    print(f"  Ícone UI: {machado_m_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {machado_m_teste.attack_animation_paths}")
    print(f"  Sprite ATK (Frame 0): {machado_m_teste.get_current_attack_animation_sprite()}")
    print(f"  Hitbox: {machado_m_teste.hitbox_width}x{machado_m_teste.hitbox_height}")

    print("\n--- Testando Evolução para Nível 2.0 (Machado Macabro) ---")
    machado_m_teste.evolve(2.0)
    print(f"Machado Evoluído: '{machado_m_teste.name}', Nível: {machado_m_teste.level}, Dano Final: {machado_m_teste.damage}")
    print(f"  Ícone UI: {machado_m_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {machado_m_teste.attack_animation_paths}")
    print(f"  Sprite ATK (Frame 0): {machado_m_teste.get_current_attack_animation_sprite()}")

    print("\n--- Testando Evolução para Nível 3.0 (Machado Macabro) ---")
    machado_m_teste.evolve(3.0)
    print(f"Machado Evoluído: '{machado_m_teste.name}', Nível: {machado_m_teste.level}, Dano Final: {machado_m_teste.damage}")
    print(f"  Caminho Efeito ATK: {machado_m_teste.attack_effect_sprite_path}, Escala: {machado_m_teste.attack_effect_scale}")
    print(f"  Sprite ATK (Frame 0): {machado_m_teste.get_current_attack_animation_sprite()}")
    
    print("\n--- Testando Evolução para Nível Inválido (0.5) ---")
    machado_m_teste.evolve(0.5)
    print(f"Após tentar evoluir para 0.5: '{machado_m_teste.name}', Nível: {machado_m_teste.level} (deve ser 3.0)")

    print("\n--- FIM DO TESTE STANDALONE (Machado Macabro) ---")
    os.path.exists = original_os_path_exists
