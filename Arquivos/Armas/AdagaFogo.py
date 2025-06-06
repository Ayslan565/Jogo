import pygame
import os
# Assume que weapon.py está no mesmo diretório 'Armas' ou em um local acessível via Python path
# Se weapon.py estiver em Armas/, e este arquivo também, o import relativo é o ideal.
from .weapon import Weapon

class AdagaFogo(Weapon):
    """
    Representa a Adaga de Fogo, uma arma com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Adaga de Fogo"
        self.level = 1.0 # Nível inicial

        # Obtém os stats iniciais para o nível 1.0 para passar ao construtor da classe base.
        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name, # O nome já será processado com sufixo em _apply_level_stats
            damage=initial_stats_for_super.get("damage", 15.0), # Dano base menor para adaga
            attack_range=initial_stats_for_super.get("range", 45.0), # Alcance menor para adaga
            cooldown=initial_stats_for_super.get("cooldown", 0.8), # Cooldown menor para adaga
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (30, 60)), # Hitbox menor
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (0, 0)),
            description="Uma adaga ágil envolta em chamas.", # Descrição base
            rarity="Comum", # Exemplo de raridade
            weapon_type="Adaga", # Tipo de arma
            element="Fogo", # Elemento
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base", None),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 0.8),
            ui_icon_path=initial_stats_for_super.get("ui_icon", "Arquivos\Armas\Armas\Espadas\Adaga do Fogo Contudente\Adaga E-1.png") # Exemplo
        )

        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        # Defina os caminhos e valores REAIS para os seus assets aqui.
        self._stats_by_level = {
            # Nível 1.0
            1.0: {
                "damage": 15.0,
                "range": 45.0, # Ex: (largura_sprite_jogador/2) + (hitbox_dim[0]/2) -> 30 + 15 = 45
                "cooldown": 0.8,
                "name_suffix": "",
                "hitbox_dim": (30, 60),   # Largura e altura da hitbox de dano
                "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Adagas/AdagaFogo/Efeitos/ImpactoLeveNv1.png",
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
            2.0: {
                "damage": 22.0, "range": 50.0, "cooldown": 0.65, "name_suffix": " Afiada",
                "hitbox_dim": (35, 65), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Adagas/AdagaFogo/Efeitos/ImpactoMedioNv2.png",
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
            3.0: {
                "damage": 30.0, "range": 55.0, "cooldown": 0.5, "name_suffix": " Incandescente",
                "hitbox_dim": (40, 70), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Adagas/AdagaFogo/Efeitos/ImpactoForteNv3.png",
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
        self.attack_animation_speed = 70
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0

        self._apply_level_stats() # Aplica os stats do nível inicial
        # print(f"DEBUG(AdagaFogo): Adaga '{self.name}' criada no Nível {self.level}.")

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        """
        Retorna o dicionário de stats para um nível específico.
        Se 'for_super_init' é True, ou se _stats_by_level não está definido,
        retorna um dicionário de fallback com valores padrão.
        """
        if for_super_init or not hasattr(self, '_stats_by_level') or not self._stats_by_level:
            if hasattr(self, '_stats_by_level') and self._stats_by_level and 1.0 in self._stats_by_level:
                return self._stats_by_level[1.0]
            else:
                # Fallback hardcoded para AdagaFogo
                return {
                    "damage": 15.0, "range": 45.0, "cooldown": 0.8, "name_suffix": "",
                    "hitbox_dim": (30, 60), "hitbox_off": (0, 0),
                    "effect_sprite_base": "Sprites/Armas/Adagas/AdagaFogo/Efeitos/ImpactoDefault.png",
                    "effect_scale_base": 0.8,
                    "animation_sprites": [], "animation_speed": 70, "animation_display_scale": 0.9,
                    "ui_icon": "Sprites/Armas/Adagas/AdagaFogo/Icone_Default.png"
                }

        if level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else:
            print(f"WARN(AdagaFogo): Nível {level_to_check} não encontrado em _stats_by_level. Usando fallback para o primeiro nível.")
            first_level_key = next(iter(self._stats_by_level))
            return self._stats_by_level[first_level_key]


    def _load_weapon_attack_animation_sprites(self, caminhos, escala_animacao=1.0):
        """
        Carrega e escala os sprites de animação de ATK da adaga.
        """
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
                        print(f"WARN(AdagaFogo): Escala da animação resultou em dimensão inválida para '{full_path}'. Usando placeholder.")
                        ph_size = max(1, int(30 * (escala_animacao if escala_animacao > 0 else 0.1)))
                        placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((255,0,255,100))
                        sprites_carregados.append(placeholder)
                else:
                    print(f"WARN(AdagaFogo): Sprite de animação de ATK não encontrado '{full_path}'. Usando placeholder.")
                    ph_size = max(1, int(30 * (escala_animacao if escala_animacao > 0 else 1.0)))
                    placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((255,0,255,100))
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"ERROR(AdagaFogo): Erro ao carregar sprite de animação de ATK '{full_path}': {e}. Usando placeholder.")
                ph_size = max(1, int(30 * (escala_animacao if escala_animacao > 0 else 1.0)))
                placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((255,0,255,100))
                sprites_carregados.append(placeholder)

        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0
        # print(f"DEBUG(AdagaFogo): {len(sprites_carregados)} sprites de animação de ATK carregados para {self.name} com escala {escala_animacao}.")


    def evolve(self, target_level: float):
        """
        Evolui a adaga para um nível específico.
        """
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            # print(f"DEBUG(AdagaFogo): '{self.name}' evoluiu para o Nível {self.level}!")
        else:
            print(f"WARN(AdagaFogo): Nível de evolução {target_level} inválido para {self.name}. Níveis disponíveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        """
        Aplica todas as estatísticas e atributos visuais correspondentes ao nível atual da adaga.
        """
        stats = self._get_stats_for_level_internal(self.level)
        
        if not stats:
            print(f"ERROR(AdagaFogo): Falha crítica ao obter stats para o nível {self.level} de '{self.name}'. Nenhuma alteração aplicada.")
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
                    print(f"WARN(AdagaFogo): Escala do efeito de ataque resultou em dimensão inválida para '{self.attack_effect_sprite_path}'.")

        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path and new_ui_icon_path != self.ui_icon_path :
            self.ui_icon_path = new_ui_icon_path
            # Se houver um método para carregar o ícone na classe base, seria chamado aqui.

        new_animation_paths = stats.get("animation_sprites")
        new_animation_display_scale = stats.get("animation_display_scale", 1.0)

        if new_animation_paths is not None:
            if new_animation_paths != self.attack_animation_paths or \
               new_animation_display_scale != self.animation_display_scale_factor or \
               not self.attack_animation_paths:
                
                self.attack_animation_paths = new_animation_paths
                self.animation_display_scale_factor = new_animation_display_scale
                self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)

        self.attack_animation_speed = stats.get("animation_speed", 70)

        name_suffix = stats.get("name_suffix", "")
        self.name = f"{self._base_name} {name_suffix}".strip()

    def get_current_attack_animation_sprite(self):
        """ Retorna o sprite atual da animação de ATK da adaga. """
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None

# --- Bloco de Teste Standalone ---
if __name__ == '__main__':
    # Mock da classe Weapon e pygame para permitir teste.
    class MockPygameSurface:
        def __init__(self, width=50, height=50, color=(0,0,0)): # Dimensões menores para adaga
            self._width = width
            self._height = height
            self.color = color
        def get_width(self): return self._width
        def get_height(self): return self._height
        def convert_alpha(self): return self
        def fill(self, color): self.color = color
            
    class MockPygameImage:
        def load(self, path):
            if "placeholder" in path.lower() or not os.path.exists(path):
                return MockPygameSurface(8,8, (255,0,255)) # Placeholder menor
            return MockPygameSurface()

    class MockPygameTransform:
        def smoothscale(self, surface, dimensions):
            return MockPygameSurface(dimensions[0], dimensions[1], surface.color)

    class MockPygame:
        image = MockPygameImage()
        transform = MockPygameTransform()
        SRCALPHA = "SRCALPHA_FLAG"
        error = type('MockPygameError', (Exception,), {})
        def Surface(self, dimensions, flags=0):
            return MockPygameSurface(dimensions[0], dimensions[1])

    pygame = MockPygame()

    class BaseWeaponMock:
        def __init__(self, name, damage, attack_range, cooldown, hitbox_dimensions, hitbox_offset,
                     description, rarity, weapon_type, element,
                     attack_effect_sprite_path, attack_effect_scale, ui_icon_path):
            self.name = name
            self.damage = damage
            self.attack_range = attack_range
            self.cooldown = cooldown
            self.hitbox_width, self.hitbox_height = hitbox_dimensions
            self.hitbox_offset_x, self.hitbox_offset_y = hitbox_offset
            self.description = description
            self.rarity = rarity
            self.weapon_type = weapon_type
            self.element = element
            self.attack_effect_sprite_path = attack_effect_sprite_path
            self.attack_effect_scale = attack_effect_scale
            self.ui_icon_path = ui_icon_path
            self.attack_effect_original_image = None
            self.attack_effect_image = None
            # print(f"Mock da Classe Base Weapon '{name}' inicializada para Adaga.")

        def _load_attack_effect_sprite(self):
            # print(f"WeaponBaseMock (Adaga): _load_attack_effect_sprite() chamado para {self.attack_effect_sprite_path}")
            if self.attack_effect_sprite_path:
                self.attack_effect_original_image = pygame.image.load(self.attack_effect_sprite_path)
                if self.attack_effect_original_image:
                    w = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                    h = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                    if w > 0 and h > 0:
                        self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (w,h))
                    else: self.attack_effect_image = None
            else:
                self.attack_effect_original_image = None
                self.attack_effect_image = None

    Weapon = BaseWeaponMock

    original_os_path_exists = os.path.exists
    def mock_os_path_exists(path):
        if "naoexiste" in path: return False
        return True # Assume que a maioria dos caminhos existe
    os.path.exists = mock_os_path_exists

    print("\n--- INICIANDO TESTE STANDALONE DA ADAGA DE FOGO ---")
    adaga_teste = AdagaFogo()
    print(f"Adaga Criada: '{adaga_teste.name}', Nível: {adaga_teste.level}, Dano: {adaga_teste.damage}, Cooldown: {adaga_teste.cooldown}")
    print(f"  Ícone UI: {adaga_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {adaga_teste.attack_animation_paths}")
    print(f"  Hitbox: {adaga_teste.hitbox_width}x{adaga_teste.hitbox_height} @ ({adaga_teste.hitbox_offset_x},{adaga_teste.hitbox_offset_y})")
    print(f"  Sprite de Animação ATK Atual (Frame 0): {adaga_teste.get_current_attack_animation_sprite()}")

    print("\n--- Testando Evolução para Nível 1.5 ---")
    adaga_teste.evolve(1.5)
    print(f"Adaga Evoluída: '{adaga_teste.name}', Nível: {adaga_teste.level}, Dano: {adaga_teste.damage}, Cooldown: {adaga_teste.cooldown}")
    print(f"  Ícone UI: {adaga_teste.ui_icon_path}")
    print(f"  Sprite de Animação ATK Atual (Frame 0): {adaga_teste.get_current_attack_animation_sprite()}")

    print("\n--- Testando Evolução para Nível 2.0 (Afiada) ---")
    adaga_teste.evolve(2.0)
    print(f"Adaga Evoluída: '{adaga_teste.name}', Nível: {adaga_teste.level}, Dano: {adaga_teste.damage}")
    print(f"  Ícone UI: {adaga_teste.ui_icon_path}") # Deve ter mudado
    print(f"  Animação ATK Paths: {adaga_teste.attack_animation_paths}") # Devem ter mudado
    print(f"  Velocidade Animação ATK: {adaga_teste.attack_animation_speed}ms, Escala: {adaga_teste.animation_display_scale_factor}")
    print(f"  Sprite de Animação ATK Atual (Frame 0): {adaga_teste.get_current_attack_animation_sprite()}")

    print("\n--- Testando Evolução para Nível 3.0 (Incandescente) ---")
    adaga_teste.evolve(3.0)
    print(f"Adaga Evoluída: '{adaga_teste.name}', Nível: {adaga_teste.level}, Dano: {adaga_teste.damage}")
    print(f"  Ícone UI: {adaga_teste.ui_icon_path}")
    print(f"  Caminho Efeito de Ataque: {adaga_teste.attack_effect_sprite_path}, Escala: {adaga_teste.attack_effect_scale}")
    print(f"  Sprite de Animação ATK Atual (Frame 0): {adaga_teste.get_current_attack_animation_sprite()}")

    print("\n--- Testando Evolução para Nível Inválido (7.0) ---")
    adaga_teste.evolve(7.0)
    print(f"Após tentar evoluir para 7.0: '{adaga_teste.name}', Nível: {adaga_teste.level} (deve ser 3.0)")

    print("\n--- FIM DO TESTE STANDALONE DA ADAGA ---")
    os.path.exists = original_os_path_exists
