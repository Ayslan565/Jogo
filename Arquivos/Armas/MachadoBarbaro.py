# Armas/MachadoBarbaro.py
import pygame
import os
# Importa a classe base para machados. Garanta que MachadoBase tenha uma interface compatível
# com a classe Weapon que usamos para as espadas, especialmente o método _load_attack_effect_sprite().
from .MachadoBase import MachadoBase

class MachadoBarbaro(MachadoBase):
    """
    Representa o Machado Bárbaro Cravejado, uma arma com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Machado Bárbaro Cravejado"
        self.level = 1.0 # Nível inicial

        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name, # O nome completo com sufixos será definido em _apply_level_stats
            damage=initial_stats_for_super.get("damage", 15.0), # Dano base do nível 1.0 original
            attack_range=initial_stats_for_super.get("range", 85.0), # Range base do nível 1.0 original
            cooldown=initial_stats_for_super.get("cooldown", 2.2), # Cooldown base do nível 1.0 original
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (90, 90)), # Exemplo
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (0, 0)),
            description="Um machado pesado e brutal, adornado com cravos ameaçadores.", # Descrição base
            rarity="Comum", # Exemplo
            weapon_type="Machado de Duas Mãos", # Exemplo
            element="Físico", # Ou "Bruto"
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base", None),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 1.0),
            ui_icon_path=initial_stats_for_super.get("ui_icon", "Sprites\Armas\Machados\Machado Bárbaro Cravejado\Machado E-1.png") # Exemplo
        )

        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        # Defina os caminhos e valores REAIS para os seus assets aqui.
        self._stats_by_level = {
            1.0: {
                "damage": 15.0, "range": 85.0, "cooldown": 2.2, "name_suffix": "",
                "hitbox_dim": (110, 300),   # CONFIGURÁVEL: Largura e altura da hitbox de dano
                "hitbox_off": (110, 0),      # CONFIGURÁVEL: Offset adicional da hitbox
                "effect_sprite_base": "Sprites\\Armas\\Machados\\MachadoBarbaro\\Efeitos\\ImpactoBrutoNv1.png", # Exemplo
                "effect_scale_base": 1.0,
                "animation_sprites": [
                    "Sprites\\Armas\\Machados\\Machado Bárbaro Cravejado\\Ataque\\AT1\\AT1-base0.png", # Exemplo
                    "Sprites\\Armas\\Machados\\Machado Bárbaro Cravejado\\Ataque\\AT1\\AT1-base1.png", # Exemplo
                    "Sprites\\Armas\\Machados\\Machado Bárbaro Cravejado\\Ataque\\AT1\\AT1-base2.png",
                    "Sprites\\Armas\\Machados\\Machado Bárbaro Cravejado\\Ataque\\AT1\\AT1-base3.png", # Exemplo
                    "Sprites\\Armas\\Machados\\Machado Bárbaro Cravejado\\Ataque\\AT1\\AT1-base4.png",  # Exemplo
                ],
                "animation_speed": 120,     # CONFIGURÁVEL (ms por frame), machados podem ser mais lentos
                "animation_display_scale": 3.0, # CONFIGURÁVEL, machados podem ser maiores
                "ui_icon": "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Machado E-1.png" # Exemplo
            },
            1.5: {
                "damage": 20.0, "range": 90.0, "cooldown": 0.1, "name_suffix": "+1",
                "hitbox_dim": (95, 95), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoBarbaro/Efeitos/ImpactoBrutoNv1.png",
                "effect_scale_base": 1.05,
                "animation_sprites": [
                    "Sprites\\Armas\\Machados\\Machado Bárbaro Cravejado\\Ataque\\AT1\\AT1-base0.png", # Exemplo
                    "Sprites\\Armas\\Machados\\Machado Bárbaro Cravejado\\Ataque\\AT1\\AT1-base1.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/ATA/AAT1-base2.png",
                    "Sprites\\Armas\\Machados\\Machado Bárbaro Cravejado\\Ataque\\AT1\\AT1-base3.png", # Exemplo
                    "Sprites\\Armas\\Machados\\Machado Bárbaro Cravejado\\Ataque\\AT1\\AT1-base4.png",  # Exemplo
                ],
                "animation_speed": 115,
                "animation_display_scale": 1.2,
                "ui_icon": "Sprites\\Armas\\Machados\\Machado Bárbaro Cravejado\\Machado E-1.png"
            },
            2.0: {
                "damage": 25.0, "range": 100.0, "cooldown": 1.9, "name_suffix": "Reforçado",
                "hitbox_dim": (100, 100), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoBarbaro/Efeitos/ImpactoBrutoNv2.png", # Exemplo
                "effect_scale_base": 1.1,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/AT2/AT2-base0.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/AT2/AT2-base1.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/ATA/AT2-base2.png",
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/AT2/AT2-base3.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/AT2/AT2-base4.png",  # Exemplo
                ],
                "animation_speed": 110,
                "animation_display_scale": 1.25,
                "ui_icon": "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Machado E-2.png" # Exemplo
            },
            2.5: {
                "damage": 30.0, "range": 105.0, "cooldown": 1.8, "name_suffix": "Reforçado +1",
                "hitbox_dim": (105, 105), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoBarbaro/Efeitos/ImpactoBrutoNv2.png",
                "effect_scale_base": 1.15,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/AT2/AT2-base0.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/AT2/AT2-base1.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/ATA/AT2-base2.png",
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/AT2/AT2-base3.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/AT2/AT2-base4.png",  # Exemplo
                ],
                "animation_speed": 105,
                "animation_display_scale": 1.25,
                "ui_icon": "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Machado E-2.png"
            },
            3.0: {
                "damage": 35.0, "range": 120.0, "cooldown": 1.6, "name_suffix": "Brutal",
                "hitbox_dim": (110, 110), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoBarbaro/Efeitos/ImpactoBrutoNv3.png", # Exemplo
                "effect_scale_base": 1.2,
                "animation_sprites": [
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/AT3/AT3-base0.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/AT3/AT3-base1.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/ATA/AT3-base2.png",
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/AT3/AT3-base3.png", # Exemplo
                    "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Ataque/AT3/AT3-base4.png",  # Exemplo
                ],
                "animation_speed": 100,
                "animation_display_scale": 1.3,
                "ui_icon": "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Machado E-3.png" # Exemplo
            }
        }

        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 100
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0

        self._apply_level_stats()
        # print(f"DEBUG(MachadoBarbaro): Machado '{self.name}' criado no Nível {self.level}.")

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        if for_super_init or not hasattr(self, '_stats_by_level') or not self._stats_by_level:
            if hasattr(self, '_stats_by_level') and self._stats_by_level and 1.0 in self._stats_by_level:
                return self._stats_by_level[1.0]
            else:
                # Absolute fallback for super().__init__()
                return {
                    "damage": 15.0, "range": 85.0, "cooldown": 2.2, "name_suffix": "",
                    "hitbox_dim": (90, 90), "hitbox_off": (0, 0),
                    "effect_sprite_base": "Sprites/Armas/Machados/MachadoBarbaro/Efeitos/ImpactoBrutoDefault.png",
                    "effect_scale_base": 1.0,
                    "animation_sprites": [], "animation_speed": 120, "animation_display_scale": 1.2,
                    "ui_icon": "Sprites/Armas/Machados/MachadoBarbaro/Icone_DefaultMB.png"
                }

        if level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else:
            print(f"WARN(MachadoBarbaro): Nível {level_to_check} não encontrado. Usando fallback para o primeiro nível.")
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
                        print(f"WARN(MachadoBarbaro): Escala inválida para '{full_path}'. Placeholder.")
                        ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 0.1)))
                        placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((100,100,100,100)) # Placeholder Cinza
                        sprites_carregados.append(placeholder)
                else:
                    print(f"WARN(MachadoBarbaro): Sprite de animação ATK não encontrado '{full_path}'. Placeholder.")
                    ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                    placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((100,100,100,100))
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"ERROR(MachadoBarbaro): Erro ao carregar sprite ATK '{full_path}': {e}. Placeholder.")
                ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((100,100,100,100))
                sprites_carregados.append(placeholder)
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0
        # print(f"DEBUG(MachadoBarbaro): {len(sprites_carregados)} sprites ATK carregados para {self.name} escala {escala_animacao}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            # print(f"DEBUG(MachadoBarbaro): '{self.name}' evoluiu para Nível {self.level}!")
        else:
            print(f"WARN(MachadoBarbaro): Nível {target_level} inválido. Níveis disponíveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        if not stats:
            print(f"ERROR(MachadoBarbaro): Falha crítica ao obter stats para Nível {self.level} de '{self.name}'.")
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

        # Garante que _load_attack_effect_sprite existe na classe base (MachadoBase)
        if hasattr(super(), '_load_attack_effect_sprite'):
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
                        print(f"WARN(MachadoBarbaro): Escala do efeito ATK inválida para '{self.attack_effect_sprite_path}'.")
        else:
            # Fallback ou aviso se MachadoBase não tiver _load_attack_effect_sprite
            self.attack_effect_sprite_path = new_base_effect_path # Apenas armazena o caminho
            self.attack_effect_scale = new_base_effect_scale
            # print(f"WARN(MachadoBarbaro): MachadoBase não possui _load_attack_effect_sprite. Efeitos podem não ser carregados visualmente.")


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
                 return MockPygameSurface(10,10, (100,100,100)) # Placeholder Cinza
            return MockPygameSurface()

    class MockPygameTransform:
        def smoothscale(self, surface, dimensions):
            return MockPygameSurface(dimensions[0], dimensions[1], surface.color)

    class MockPygame:
        image = MockPygameImage(); transform = MockPygameTransform()
        SRCALPHA = "SRCALPHA_FLAG"; error = type('MockPygameError', (Exception,), {})
        def Surface(self, dimensions, flags=0): return MockPygameSurface(dimensions[0], dimensions[1])

    pygame = MockPygame()

    # Mock para MachadoBase, garantindo que tenha _load_attack_effect_sprite se quisermos testar essa parte
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

        def _load_attack_effect_sprite(self): # Método crucial da interface esperada
            # print(f"MockMachadoBase: _load_attack_effect_sprite() chamado para {self.attack_effect_sprite_path}")
            if self.attack_effect_sprite_path:
                self.attack_effect_original_image = pygame.image.load(self.attack_effect_sprite_path)
                if self.attack_effect_original_image:
                    w = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                    h = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                    if w > 0 and h > 0: self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (w,h))
                    else: self.attack_effect_image = None
            else: self.attack_effect_original_image = None; self.attack_effect_image = None

    MachadoBase = MockMachadoBase # Sobrescreve a importação de MachadoBase com nosso mock

    original_os_path_exists = os.path.exists
    def mock_os_path_exists(path):
        if "naoexiste" in path: return False
        return True
    os.path.exists = mock_os_path_exists

    print("\n--- INICIANDO TESTE STANDALONE DO MACHADO BÁRBARO ---")
    machado_b_teste = MachadoBarbaro()
    print(f"Machado Criado: '{machado_b_teste.name}', Nível: {machado_b_teste.level}, Dano: {machado_b_teste.damage}")
    print(f"  Descrição: {machado_b_teste.description}")
    print(f"  Ícone UI: {machado_b_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {machado_b_teste.attack_animation_paths}")
    print(f"  Sprite ATK (Frame 0): {machado_b_teste.get_current_attack_animation_sprite()}")

    print("\n--- Testando Evolução para Nível 2.0 (Machado Bárbaro) ---")
    machado_b_teste.evolve(2.0)
    print(f"Machado Evoluído: '{machado_b_teste.name}', Nível: {machado_b_teste.level}, Dano: {machado_b_teste.damage}")
    print(f"  Ícone UI: {machado_b_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {machado_b_teste.attack_animation_paths}")
    print(f"  Sprite ATK (Frame 0): {machado_b_teste.get_current_attack_animation_sprite()}")

    print("\n--- Testando Evolução para Nível 3.0 (Machado Bárbaro) ---")
    machado_b_teste.evolve(3.0)
    print(f"Machado Evoluído: '{machado_b_teste.name}', Nível: {machado_b_teste.level}, Dano: {machado_b_teste.damage}")
    print(f"  Caminho Efeito ATK: {machado_b_teste.attack_effect_sprite_path}, Escala: {machado_b_teste.attack_effect_scale}")
    print(f"  Sprite ATK (Frame 0): {machado_b_teste.get_current_attack_animation_sprite()}")
    
    print("\n--- Testando Evolução para Nível Inválido (10.0) ---")
    machado_b_teste.evolve(10.0)
    print(f"Após tentar evoluir para 10.0: '{machado_b_teste.name}', Nível: {machado_b_teste.level} (deve ser 3.0)")

    print("\n--- FIM DO TESTE STANDALONE (Machado Bárbaro) ---")
    os.path.exists = original_os_path_exists
