# Armas/EspadaLua.py
import pygame
import os
# Assume que weapon.py está no mesmo diretório 'Armas' ou em um local acessível via Python path
from .weapon import Weapon

class EspadaLua(Weapon):
    """
    Representa a Espada Sacra da Lua (Azul com Roxo), uma arma com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Espada Sacra da Lua" # Nome base sem cor para sufixos
        self.level = 1.0 # Nível inicial

        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name, # O nome completo com cores e sufixos será definido em _apply_level_stats
            damage=initial_stats_for_super.get("damage", 45.0),
            attack_range=initial_stats_for_super.get("range", 115.0), # Usando o range fornecido como base
            cooldown=initial_stats_for_super.get("cooldown", 1.2),
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (70, 135)), # Exemplo
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (0, 0)),
            description="Uma espada imbuída com o poder místico da lua, brilhando em tons de azul e roxo.", # Descrição base
            rarity="Lendária", # Exemplo
            weapon_type="Espada Lunar", # Exemplo
            element="Lunar", # Ou "Arcano", "Cósmico"
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base", None),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 1.0),
            ui_icon_path=initial_stats_for_super.get("ui_icon", "Sprites/Armas/Espadas/EspadaLua/Icone_EL1.png") # Exemplo
        )

        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        # Defina os caminhos e valores REAIS para os seus assets aqui.
        # Os valores de 'range' abaixo são os fornecidos originalmente.
        # Se precisar de cálculo (player_width/2 + hitbox_dim[0]/2), ajuste-os.
        self._stats_by_level = {
            1.0: {
                "damage": 45.0, "range": 115.0, "cooldown": 1.2, "name_suffix": "(Azul com Roxo)",
                "hitbox_dim": (70, 120),   # CONFIGURÁVEL
                "hitbox_off": (0, 0),      # CONFIGURÁVEL
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaLua/Efeitos/ImpactoLunarNv1.png", # Exemplo
                "effect_scale_base": 1.0,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv1/LuaFrame1.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv1/LuaFrame2.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv1/LuaFrame3.png"  # Exemplo
                ],
                "animation_speed": 85,     # CONFIGURÁVEL (ms por frame)
                "animation_display_scale": 1.1, # CONFIGURÁVEL
                "ui_icon": "Sprites//Armas//Espadas//Espada Sacra do Lua//E1.jpg" # Exemplo
            },
            1.5: {
                "damage": 50.0, "range": 120.0, "cooldown": 1.15, "name_suffix": "(Azul com Roxo) +1",
                "hitbox_dim": (75, 125), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaLua/Efeitos/ImpactoLunarNv1.png",
                "effect_scale_base": 1.05,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv1/LuaFrame1.png",
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv1/LuaFrame2.png",
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv1/LuaFrame3.png"
                ],
                "animation_speed": 82,
                "animation_display_scale": 1.1,
                "ui_icon": "Sprites//Armas//Espadas//Espada Sacra do Lua//E2.jpg" # Pode ser o mesmo
            },
            2.0: {
                "damage": 62.0, "range": 130.0, "cooldown": 1.0, "name_suffix": "Crescente (Azul e Lilás)", # Exemplo de mudança de cor/nome
                "hitbox_dim": (80, 130), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaLua/Efeitos/ImpactoLunarNv2.png", # Exemplo
                "effect_scale_base": 1.15,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv2/LuaCrescente1.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv2/LuaCrescente2.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv2/LuaCrescente3.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv2/LuaCrescente4.png"  # Exemplo
                ],
                "animation_speed": 80,
                "animation_display_scale": 1.15,
                "ui_icon": "Sprites//Armas//Espadas//Espada Sacra do Lua//E2.jpg" # Exemplo
            },
            2.5: {
                "damage": 68.0, "range": 135.0, "cooldown": 0.95, "name_suffix": "Crescente (Azul e Lilás) +1",
                "hitbox_dim": (85, 135), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaLua/Efeitos/ImpactoLunarNv2.png",
                "effect_scale_base": 1.2,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv2/LuaCrescente1.png",
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv2/LuaCrescente2.png",
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv2/LuaCrescente3.png",
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv2/LuaCrescente4.png"
                ],
                "animation_speed": 78,
                "animation_display_scale": 1.15,
                "ui_icon": "Sprites//Armas//Espadas//Espada Sacra do Lua//E2.jpg"
            },
            3.0: {
                "damage": 85.0, "range": 150.0, "cooldown": 0.8, "name_suffix": "Plena (Índigo e Violeta)", # Exemplo
                "hitbox_dim": (90, 140), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaLua/Efeitos/ImpactoLunarNv3.png", # Exemplo
                "effect_scale_base": 1.25,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv3/LuaPlena1.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv3/LuaPlena2.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv3/LuaPlena3.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv3/LuaPlena4.png", # Exemplo
                    "Sprites/Armas/Espadas/EspadaLua/Ataque/Nv3/LuaPlena5.png"  # Exemplo
                ],
                "animation_speed": 75,
                "animation_display_scale": 1.2,
                "ui_icon": "Sprites//Armas//Espadas//Espada Sacra do Lua//E3.jpg" # Exemplo
            }
        }

        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 100
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0

        self._apply_level_stats()
        # print(f"DEBUG(EspadaLua): Espada '{self.name}' criada no Nível {self.level}.")

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        if for_super_init or not hasattr(self, '_stats_by_level') or not self._stats_by_level:
            if hasattr(self, '_stats_by_level') and self._stats_by_level and 1.0 in self._stats_by_level:
                # This case is unlikely if for_super_init is true and called before self._stats_by_level is set
                return self._stats_by_level[1.0]
            else:
                # Absolute fallback for super().__init__()
                return {
                    "damage": 45.0, "range": 115.0, "cooldown": 1.2, "name_suffix": "(Azul com Roxo)",
                    "hitbox_dim": (70, 135), "hitbox_off": (0, 0),
                    "effect_sprite_base": "Sprites/Armas/Espadas/EspadaLua/Efeitos/ImpactoLunarDefault.png",
                    "effect_scale_base": 1.0,
                    "animation_sprites": [], "animation_speed": 100, "animation_display_scale": 1.0,
                    "ui_icon": "Sprites/Armas/Espadas/EspadaLua/Icone_DefaultEL.png"
                }

        if level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else:
            print(f"WARN(EspadaLua): Nível {level_to_check} não encontrado. Usando fallback para o primeiro nível.")
            # Fallback to the first defined level if the exact level is not found
            first_level_key = next(iter(self._stats_by_level)) # Assumes _stats_by_level is not empty
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
                        print(f"WARN(EspadaLua): Escala inválida para '{full_path}'. Placeholder.")
                        ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 0.1)))
                        placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((75,0,130,100)) # Placeholder Roxo/Índigo
                        sprites_carregados.append(placeholder)
                else:
                    print(f"WARN(EspadaLua): Sprite de animação ATK não encontrado '{full_path}'. Placeholder.")
                    ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                    placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((75,0,130,100)) # Placeholder Roxo/Índigo
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"ERROR(EspadaLua): Erro ao carregar sprite ATK '{full_path}': {e}. Placeholder.")
                ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((75,0,130,100)) # Placeholder Roxo/Índigo
                sprites_carregados.append(placeholder)
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0
        # print(f"DEBUG(EspadaLua): {len(sprites_carregados)} sprites ATK carregados para {self.name} escala {escala_animacao}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            # print(f"DEBUG(EspadaLua): '{self.name}' evoluiu para Nível {self.level}!")
        else:
            print(f"WARN(EspadaLua): Nível {target_level} inválido. Níveis disponíveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        if not stats: # Should be handled by _get_stats_for_level_internal, but as a safeguard
            print(f"ERROR(EspadaLua): Falha crítica ao obter stats para Nível {self.level} de '{self.name}'. Nenhuma alteração aplicada.")
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
            if self.attack_effect_original_image: # Ensure original image is loaded
                width = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                height = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                if width > 0 and height > 0:
                    self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (width, height))
                else:
                    self.attack_effect_image = None # Or a placeholder
                    print(f"WARN(EspadaLua): Escala do efeito ATK resultou em dimensão inválida para '{self.attack_effect_sprite_path}'.")

        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path and new_ui_icon_path != self.ui_icon_path: # Avoid unnecessary path updates if not changing
            self.ui_icon_path = new_ui_icon_path
            # If your base Weapon class or UI manager handles loading UI icon surfaces, call that here.

        new_animation_paths = stats.get("animation_sprites")
        new_animation_display_scale = stats.get("animation_display_scale", 1.0)

        if new_animation_paths is not None: # Ensure there are animation paths defined
            if new_animation_paths != self.attack_animation_paths or \
               new_animation_display_scale != self.animation_display_scale_factor or \
               not self.attack_animation_paths: # Force load on first apply or if paths/scale change
                
                self.attack_animation_paths = new_animation_paths # Store the new paths
                self.animation_display_scale_factor = new_animation_display_scale
                self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)

        self.attack_animation_speed = stats.get("animation_speed", 100) # Default if not specified
        
        name_suffix = stats.get("name_suffix", "")
        self.name = f"{self._base_name} {name_suffix}".strip()


    def get_current_attack_animation_sprite(self):
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None

# --- Bloco de Teste Standalone ---
if __name__ == '__main__':
    # Mocks para teste standalone (semelhantes aos anteriores)
    class MockPygameSurface:
        def __init__(self, width=100, height=100, color=(0,0,0)):
            self._width = width; self._height = height; self.color = color
        def get_width(self): return self._width
        def get_height(self): return self._height
        def convert_alpha(self): return self # Simplificado
        def fill(self, color): self.color = color
            
    class MockPygameImage:
        def load(self, path):
            # Simula falha para placeholders ou caminhos específicos
            if "placeholder" in path.lower() or ("naoexiste" in path.lower() and not original_os_path_exists(path)):
                 return MockPygameSurface(10,10, (75,0,130)) # Placeholder roxo para Lua
            return MockPygameSurface() # Mock de sucesso

    class MockPygameTransform:
        def smoothscale(self, surface, dimensions):
            # Retorna uma nova superfície mock com as novas dimensões
            return MockPygameSurface(dimensions[0], dimensions[1], surface.color)

    class MockPygame: # Define o mock do Pygame
        image = MockPygameImage()
        transform = MockPygameTransform()
        SRCALPHA = "SRCALPHA_FLAG" # Mock flag
        error = type('MockPygameError', (Exception,), {}) # Mock para pygame.error
        def Surface(self, dimensions, flags=0): # Mock para pygame.Surface
            return MockPygameSurface(dimensions[0], dimensions[1])

    pygame = MockPygame() # Sobrescreve o import real do pygame

    class BaseWeaponMock: # Mock da classe Weapon base
        def __init__(self, name, damage, attack_range, cooldown, hitbox_dimensions, hitbox_offset,
                     description, rarity, weapon_type, element,
                     attack_effect_sprite_path, attack_effect_scale, ui_icon_path):
            # Atribui todos os parâmetros aos atributos da instância
            self.name = name; self.damage = damage; self.attack_range = attack_range; self.cooldown = cooldown
            self.hitbox_width, self.hitbox_height = hitbox_dimensions
            self.hitbox_offset_x, self.hitbox_offset_y = hitbox_offset
            self.description = description; self.rarity = rarity; self.weapon_type = weapon_type; self.element = element
            self.attack_effect_sprite_path = attack_effect_sprite_path
            self.attack_effect_scale = attack_effect_scale
            self.ui_icon_path = ui_icon_path
            self.attack_effect_original_image = None; self.attack_effect_image = None
        def _load_attack_effect_sprite(self): # Mock do método de carregar sprite de efeito
            if self.attack_effect_sprite_path:
                self.attack_effect_original_image = pygame.image.load(self.attack_effect_sprite_path) # Usa o mock do pygame.image.load
                if self.attack_effect_original_image:
                    w = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                    h = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                    if w > 0 and h > 0: self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (w,h))
                    else: self.attack_effect_image = None
            else: self.attack_effect_original_image = None; self.attack_effect_image = None
    Weapon = BaseWeaponMock # Sobrescreve a importação de Weapon

    original_os_path_exists = os.path.exists # Salva a função original
    def mock_os_path_exists(path): # Mock para os.path.exists
        if "naoexiste" in path: return False # Simula arquivo não existente
        return True # Assume que outros caminhos existem
    os.path.exists = mock_os_path_exists

    print("\n--- INICIANDO TESTE STANDALONE DA ESPADA DA LUA ---")
    espada_lua_teste = EspadaLua()
    print(f"Espada Criada: '{espada_lua_teste.name}', Nível: {espada_lua_teste.level}, Dano: {espada_lua_teste.damage}")
    print(f"  Descrição: {espada_lua_teste.description}")
    print(f"  Ícone UI: {espada_lua_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {espada_lua_teste.attack_animation_paths}")
    print(f"  Sprite ATK (Frame 0): {espada_lua_teste.get_current_attack_animation_sprite()}")

    print("\n--- Testando Evolução para Nível 2.0 (Espada da Lua) ---")
    espada_lua_teste.evolve(2.0)
    print(f"Espada Evoluída: '{espada_lua_teste.name}', Nível: {espada_lua_teste.level}, Dano: {espada_lua_teste.damage}")
    print(f"  Ícone UI: {espada_lua_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {espada_lua_teste.attack_animation_paths}")
    print(f"  Sprite ATK (Frame 0): {espada_lua_teste.get_current_attack_animation_sprite()}")

    print("\n--- Testando Evolução para Nível 3.0 (Espada da Lua) ---")
    espada_lua_teste.evolve(3.0)
    print(f"Espada Evoluída: '{espada_lua_teste.name}', Nível: {espada_lua_teste.level}, Dano: {espada_lua_teste.damage}")
    print(f"  Caminho Efeito ATK: {espada_lua_teste.attack_effect_sprite_path}, Escala: {espada_lua_teste.attack_effect_scale}")
    print(f"  Sprite ATK (Frame 0): {espada_lua_teste.get_current_attack_animation_sprite()}")
    
    print("\n--- Testando Evolução para Nível Inválido (4.0) ---")
    espada_lua_teste.evolve(4.0)
    print(f"Após tentar evoluir para 4.0: '{espada_lua_teste.name}', Nível: {espada_lua_teste.level} (deve ser 3.0)")


    print("\n--- FIM DO TESTE STANDALONE (Espada da Lua) ---")
    os.path.exists = original_os_path_exists # Restaura a função original
