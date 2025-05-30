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

        # Obtém os stats base para o construtor e para atributos não passados ao MachadoBase.__init__
        initial_stats = self._get_stats_for_level_internal(self.level, for_super_init=True)
        
        # Calcula o dano a ser passado para MachadoBase para compensar sua escala de 0.8
        intended_damage = initial_stats.get("damage", 15.0)
        damage_to_pass_to_base = intended_damage / 0.8 if 0.8 > 0 else intended_damage

        # Chama o __init__ de MachadoBase com os parâmetros que ele espera
        super().__init__(
            name=self._base_name, 
            damage=damage_to_pass_to_base,
            attack_range=initial_stats.get("range", 85.0),
            cooldown=initial_stats.get("cooldown", 2.2),
            level=self.level 
        )

        # Atributos que MachadoBase.__init__ não lida, mas são parte da "interface" Weapon
        # e são esperados pela lógica de _apply_level_stats ou pela UI.
        # Se MachadoBase não os encaminha para Weapon.__init__, os definimos aqui.
        # _apply_level_stats irá configurar muitos deles com base no nível.
        # Estes são para garantir que existam desde o início, com valores base.
        self.description = initial_stats.get("description", "Um machado pesado e brutal, adornado com cravos ameaçadores.")
        self.rarity = initial_stats.get("rarity", "Comum")
        # MachadoBase define self.attack_type. self.weapon_type é para classificação/UI.
        self.weapon_type = initial_stats.get("weapon_type", "Machado de Duas Mãos") 
        self.element = initial_stats.get("element", "Físico")
        
        # ui_icon_path, hitbox_dimensions, etc., serão tratados por _apply_level_stats
        # com base nos valores de initial_stats e _stats_by_level.
        # O importante é que initial_stats forneça esses valores para o nível 1.

        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        # Defina os caminhos e valores REAIS para os seus assets aqui.
        self._stats_by_level = {
            1.0: {
                "damage": 15.0, "range": 85.0, "cooldown": 2.2, "name_suffix": "",
                "hitbox_dim": (90, 90),   # CONFIGURÁVEL: Largura e altura da hitbox de dano
                "hitbox_off": (0, 0),      # CONFIGURÁVEL: Offset adicional da hitbox
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoBarbaro/Efeitos/ImpactoBrutoNv1.png", # Exemplo
                "effect_scale_base": 1.0,
                "animation_sprites": [
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv1/BarbaroFrame1.png", # Exemplo
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv1/BarbaroFrame2.png", # Exemplo
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv1/BarbaroFrame3.png"  # Exemplo
                ],
                "animation_speed": 120,     # CONFIGURÁVEL (ms por frame), machados podem ser mais lentos
                "animation_display_scale": 1.2, # CONFIGURÁVEL, machados podem ser maiores
                "ui_icon": "Sprites/Armas/Machados/MachadoBarbaro/Icone_MB1.png", # Exemplo
                # Adicionando os atributos descritivos aqui também para consistência, embora _apply_level_stats não os use diretamente.
                "description": "Um machado pesado e brutal, adornado com cravos ameaçadores.",
                "rarity": "Comum",
                "weapon_type": "Machado de Duas Mãos",
                "element": "Físico"
            },
            1.5: {
                "damage": 20.0, "range": 90.0, "cooldown": 2.1, "name_suffix": "+1",
                "hitbox_dim": (95, 95), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoBarbaro/Efeitos/ImpactoBrutoNv1.png",
                "effect_scale_base": 1.05,
                "animation_sprites": [
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv1/BarbaroFrame1.png",
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv1/BarbaroFrame2.png",
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv1/BarbaroFrame3.png"
                ],
                "animation_speed": 115,
                "animation_display_scale": 1.2,
                "ui_icon": "Sprites/Armas/Machados/MachadoBarbaro/Icone_MB1.png"
            },
            2.0: {
                "damage": 25.0, "range": 100.0, "cooldown": 1.9, "name_suffix": "Reforçado",
                "hitbox_dim": (100, 100), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoBarbaro/Efeitos/ImpactoBrutoNv2.png", 
                "effect_scale_base": 1.1,
                "animation_sprites": [
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv2/ReforcadoFrame1.png", 
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv2/ReforcadoFrame2.png", 
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv2/ReforcadoFrame3.png", 
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv2/ReforcadoFrame4.png"
                ],
                "animation_speed": 110,
                "animation_display_scale": 1.25,
                "ui_icon": "Sprites/Armas/Machados/MachadoBarbaro/Icone_MB2.png" 
            },
            2.5: {
                "damage": 30.0, "range": 105.0, "cooldown": 1.8, "name_suffix": "Reforçado +1",
                "hitbox_dim": (105, 105), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoBarbaro/Efeitos/ImpactoBrutoNv2.png",
                "effect_scale_base": 1.15,
                "animation_sprites": [
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv2/ReforcadoFrame1.png",
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv2/ReforcadoFrame2.png",
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv2/ReforcadoFrame3.png",
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv2/ReforcadoFrame4.png"
                ],
                "animation_speed": 105,
                "animation_display_scale": 1.25,
                "ui_icon": "Sprites/Armas/Machados/MachadoBarbaro/Icone_MB2.png"
            },
            3.0: {
                "damage": 35.0, "range": 120.0, "cooldown": 1.6, "name_suffix": "Brutal",
                "hitbox_dim": (110, 110), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoBarbaro/Efeitos/ImpactoBrutoNv3.png", 
                "effect_scale_base": 1.2,
                "animation_sprites": [
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv3/BrutalFrame1.png", 
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv3/BrutalFrame2.png", 
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv3/BrutalFrame3.png", 
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv3/BrutalFrame4.png", 
                    "Sprites/Armas/Machados/MachadoBarbaro/Ataque/Nv3/BrutalFrame5.png"
                ],
                "animation_speed": 100,
                "animation_display_scale": 1.3,
                "ui_icon": "Sprites/Armas/Machados/MachadoBarbaro/Icone_MB3.png"
            }
        }

        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 100 # Será atualizado por _apply_level_stats
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0 # Será atualizado por _apply_level_stats

        self._apply_level_stats() # Aplica os status do nível atual (1.0)
        # print(f"DEBUG(MachadoBarbaro): Machado '{self.name}' criado no Nível {self.level}.")

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        # Se for para o super init ou _stats_by_level não estiver pronto, retorna um dict de fallback completo
        if for_super_init: # Simplificado para sempre retornar este bloco para for_super_init
            return {
                "damage": 15.0, "range": 85.0, "cooldown": 2.2, "name_suffix": "",
                "hitbox_dim": (90, 90), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Machados/MachadoBarbaro/Efeitos/ImpactoBrutoDefault.png",
                "effect_scale_base": 1.0,
                "animation_sprites": [], "animation_speed": 120, "animation_display_scale": 1.2,
                "ui_icon": "Sprites/Armas/Machados/MachadoBarbaro/Icone_DefaultMB.png",
                # Adicionando os atributos descritivos para que initial_stats os tenha
                "description": "Um machado pesado e brutal, adornado com cravos ameaçadores.",
                "rarity": "Comum",
                "weapon_type": "Machado de Duas Mãos",
                "element": "Físico"
            }

        # Se _stats_by_level existe e o nível está lá
        if hasattr(self, '_stats_by_level') and self._stats_by_level and level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else: # Fallback para o primeiro nível definido se o exato não existir e não for para super_init
            if hasattr(self, '_stats_by_level') and self._stats_by_level:
                print(f"WARN(MachadoBarbaro): Nível {level_to_check} não encontrado em _stats_by_level. Usando fallback para o primeiro nível.")
                first_level_key = next(iter(self._stats_by_level))
                return self._stats_by_level[first_level_key]
            else: # Caso extremo: _stats_by_level não existe mesmo após for_super_init (não deveria acontecer)
                print(f"ERROR(MachadoBarbaro): _stats_by_level não definido ao tentar buscar nível {level_to_check}.")
                # Retorna o mesmo que for_super_init como último recurso
                return {
                    "damage": 15.0, "range": 85.0, "cooldown": 2.2, "name_suffix": "",
                    "hitbox_dim": (90, 90), "hitbox_off": (0, 0),
                    "effect_sprite_base": "Sprites/Armas/Machados/MachadoBarbaro/Efeitos/ImpactoBrutoDefault.png",
                    "effect_scale_base": 1.0, "animation_sprites": [], "animation_speed": 120,
                    "animation_display_scale": 1.2, "ui_icon": "Sprites/Armas/Machados/MachadoBarbaro/Icone_DefaultMB.png",
                    "description": "Um machado pesado e brutal, adornado com cravos ameaçadores.", "rarity": "Comum",
                    "weapon_type": "Machado de Duas Mãos", "element": "Físico"
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
        stats = self._get_stats_for_level_internal(self.level) # Pega os stats do nível atual
        if not stats:
            print(f"ERROR(MachadoBarbaro): Falha crítica ao obter stats para Nível {self.level} de '{self.name}'.")
            return

        # Atributos principais de combate
        self.damage = stats["damage"] # O dano aqui é o final, já considerado o ajuste no __init__ para MachadoBase
        self.attack_range = stats["range"]
        self.cooldown = stats["cooldown"]

        # Atributos da hitbox
        if "hitbox_dim" in stats:
            self.hitbox_width = stats["hitbox_dim"][0]
            self.hitbox_height = stats["hitbox_dim"][1]
        if "hitbox_off" in stats:
            self.hitbox_offset_x = stats["hitbox_off"][0]
            self.hitbox_offset_y = stats["hitbox_off"][1]

        # Efeito visual do ataque (impacto)
        new_base_effect_path = stats.get("effect_sprite_base")
        new_base_effect_scale = stats.get("effect_scale_base", self.attack_effect_scale)

        if hasattr(super(), '_load_attack_effect_sprite'): # Verifica se MachadoBase (ou sua superclasse) tem o método
            if new_base_effect_path and new_base_effect_path != self.attack_effect_sprite_path:
                self.attack_effect_sprite_path = new_base_effect_path
                self.attack_effect_scale = new_base_effect_scale
                super()._load_attack_effect_sprite()
            elif new_base_effect_scale != self.attack_effect_scale and hasattr(self, 'attack_effect_original_image') and self.attack_effect_original_image:
                self.attack_effect_scale = new_base_effect_scale
                if self.attack_effect_original_image: # Garante que a imagem original existe
                    width = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                    height = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                    if width > 0 and height > 0:
                        self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (width, height))
                    else:
                        self.attack_effect_image = None
                        print(f"WARN(MachadoBarbaro): Escala do efeito ATK inválida para '{self.attack_effect_sprite_path}'.")
        else:
            # Se _load_attack_effect_sprite não existir, apenas armazena os paths/scales
            self.attack_effect_sprite_path = new_base_effect_path
            self.attack_effect_scale = new_base_effect_scale
            # print(f"WARN(MachadoBarbaro): MachadoBase não possui _load_attack_effect_sprite. Efeitos visuais de ataque podem não ser carregados.")

        # Ícone da UI
        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path and new_ui_icon_path != self.ui_icon_path:
            self.ui_icon_path = new_ui_icon_path
            # Se houver um método para carregar a superfície do ícone, chame-o aqui.
            # Ex: if hasattr(self, '_load_ui_icon_surface'): self._load_ui_icon_surface()

        # Animação de ataque da arma (sprites da arma se movendo)
        new_animation_paths = stats.get("animation_sprites")
        new_animation_display_scale = stats.get("animation_display_scale", 1.0)

        if new_animation_paths is not None: # Garante que há caminhos de animação definidos
            # Recarrega se os paths, a escala mudaram, ou se ainda não foram carregados
            if new_animation_paths != self.attack_animation_paths or \
               new_animation_display_scale != self.animation_display_scale_factor or \
               not self.attack_animation_sprites: # Força o carregamento na primeira vez ou se lista vazia
                
                self.attack_animation_paths = new_animation_paths 
                self.animation_display_scale_factor = new_animation_display_scale
                self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)

        self.attack_animation_speed = stats.get("animation_speed", 100)
        
        # Nome da arma com sufixo do nível
        name_suffix = stats.get("name_suffix", "")
        self.name = f"{self._base_name} {name_suffix}".strip()
        
        # Atributos descritivos (geralmente não mudam com o nível, mas podem ser definidos no dict do nível se necessário)
        # Se não estiverem em stats[level], os valores de __init__ (via initial_stats) permanecem.
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

    class MockMachadoBase:
        def __init__(self, name, damage, attack_range, cooldown, level): # Assumindo a assinatura correta de MachadoBase
            self.name = name
            # MachadoBase aplica damage * 0.8 internamente ao chamar super().__init__(..., damage=damage*0.8, ...)
            # Para o mock, vamos simular o dano que seria passado para Weapon (a superclasse de MachadoBase)
            self.damage_passed_to_weapon = damage # No mock, o dano já está "ajustado"
            self.attack_range = attack_range
            self.cooldown = cooldown
            self.level = level
            self.attack_type = "vertical" # Definido por MachadoBase
            
            # Atributos que Weapon (super de MachadoBase) normalmente inicializaria
            self.hitbox_width = 0 
            self.hitbox_height = 0
            self.hitbox_offset_x = 0
            self.hitbox_offset_y = 0
            self.description = ""
            self.rarity = ""
            self.weapon_type = "" # Este é o tipo descritivo, não o attack_type
            self.element = ""
            self.attack_effect_sprite_path = None
            self.attack_effect_scale = 1.0
            self.ui_icon_path = None
            self.attack_effect_original_image = None
            self.attack_effect_image = None
            # print(f"MockMachadoBase '{name}' inicializado. Dano recebido (pré-ajuste interno de MachadoBase): {damage}, Nível: {level}")

        def _load_attack_effect_sprite(self):
            # print(f"MockMachadoBase: _load_attack_effect_sprite() chamado para {getattr(self, 'attack_effect_sprite_path', 'N/A')}")
            if hasattr(self, 'attack_effect_sprite_path') and self.attack_effect_sprite_path:
                self.attack_effect_original_image = pygame.image.load(self.attack_effect_sprite_path)
                if self.attack_effect_original_image:
                    w = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                    h = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                    if w > 0 and h > 0: self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (w,h))
                    else: self.attack_effect_image = None
            else: self.attack_effect_original_image = None; self.attack_effect_image = None
        
        def get_attack_hitbox(self, player_rect, player_direction, attack_hitbox_size):
            # Mock simples do get_attack_hitbox de MachadoBase
            # print(f"MockMachadoBase.get_attack_hitbox chamada com hitbox_size: {attack_hitbox_size}")
            return pygame.Rect(0,0, attack_hitbox_size[0], attack_hitbox_size[1])


    MachadoBase = MockMachadoBase 

    original_os_path_exists = os.path.exists
    def mock_os_path_exists(path):
        if "naoexiste" in path: return False
        return True
    os.path.exists = mock_os_path_exists

    print("\n--- INICIANDO TESTE STANDALONE DO MACHADO BÁRBARO ---")
    machado_b_teste = MachadoBarbaro()
    print(f"Machado Criado: '{machado_b_teste.name}', Nível: {machado_b_teste.level}, Dano Final: {machado_b_teste.damage}")
    # O dano em MachadoBase (e subsequentemente em Weapon) seria 15.0 (dano do nivel 1 / 0.8 * 0.8)
    # No mock, self.damage_passed_to_weapon em MockMachadoBase teria 15.0 / 0.8 = 18.75
    # E o dano final em MachadoBarbaro (self.damage) é 15.0, o que está correto.
    print(f"  Descrição: {machado_b_teste.description}, Raridade: {machado_b_teste.rarity}")
    print(f"  Tipo: {machado_b_teste.weapon_type}, Elemento: {machado_b_teste.element}, Tipo Ataque: {machado_b_teste.attack_type}")
    print(f"  Ícone UI: {machado_b_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {machado_b_teste.attack_animation_paths}")
    print(f"  Sprite ATK (Frame 0): {machado_b_teste.get_current_attack_animation_sprite()}")
    print(f"  Hitbox: {machado_b_teste.hitbox_width}x{machado_b_teste.hitbox_height}")

    print("\n--- Testando Evolução para Nível 2.0 (Machado Bárbaro) ---")
    machado_b_teste.evolve(2.0)
    print(f"Machado Evoluído: '{machado_b_teste.name}', Nível: {machado_b_teste.level}, Dano Final: {machado_b_teste.damage}")
    print(f"  Ícone UI: {machado_b_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {machado_b_teste.attack_animation_paths}")
    print(f"  Sprite ATK (Frame 0): {machado_b_teste.get_current_attack_animation_sprite()}")
    print(f"  Hitbox: {machado_b_teste.hitbox_width}x{machado_b_teste.hitbox_height}")


    print("\n--- Testando Evolução para Nível 3.0 (Machado Bárbaro) ---")
    machado_b_teste.evolve(3.0)
    print(f"Machado Evoluído: '{machado_b_teste.name}', Nível: {machado_b_teste.level}, Dano Final: {machado_b_teste.damage}")
    print(f"  Caminho Efeito ATK: {machado_b_teste.attack_effect_sprite_path}, Escala: {machado_b_teste.attack_effect_scale}")
    print(f"  Sprite ATK (Frame 0): {machado_b_teste.get_current_attack_animation_sprite()}")
    
    print("\n--- Testando Evolução para Nível Inválido (10.0) ---")
    machado_b_teste.evolve(10.0)
    print(f"Após tentar evoluir para 10.0: '{machado_b_teste.name}', Nível: {machado_b_teste.level} (deve ser 3.0)")

    print("\n--- FIM DO TESTE STANDALONE (Machado Bárbaro) ---")
    os.path.exists = original_os_path_exists
