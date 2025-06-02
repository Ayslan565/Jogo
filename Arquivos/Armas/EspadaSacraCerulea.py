# Armas/EspadaSacraCerulea.py
import pygame
import os
# Assume que weapon.py está no mesmo diretório 'Armas' ou em um local acessível via Python path
# Se weapon.py estiver em Armas/, e este arquivo também, o import relativo é o ideal.
from weapon import Weapon

class EspadaSacraCerulea(Weapon):
    """
    Representa a Espada Sacra das Brasas, uma arma com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Espada Sacra das Brasas"
        self.level = 1.0 # Nível inicial

        # Obtém os stats iniciais para o nível 1.0 para passar ao construtor da classe base.
        # É crucial que _get_stats_for_level_internal possa lidar com uma chamada
        # antes de self._stats_by_level ser totalmente definido, usando fallbacks.
        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name, # O nome já será processado com sufixo em _apply_level_stats
            damage=initial_stats_for_super.get("damage", 30.0),
            # CONFIGURÁVEL: Distância do centro do player ao CENTRO da hitbox da arma.
            attack_range=initial_stats_for_super.get("range", 100.0),
            cooldown=initial_stats_for_super.get("cooldown", 1.5),
            # CONFIGURÁVEL: (largura, altura) da HITBOX LÓGICA de dano.
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (50, 120)), # Exemplo
            # CONFIGURÁVEL: Offset (dx, dy) para o CENTRO da hitbox LÓGICA, relativo ao ponto definido por attack_range.
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (0, 0)),
            description="Uma espada imbuída com o poder das brasas sagradas.", # Descrição base
            rarity="Rara", # Exemplo de raridade
            weapon_type="Espada", # Exemplo de tipo
            element="Fogo", # Exemplo de elemento
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base", None),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 1.0),
            ui_icon_path=initial_stats_for_super.get("ui_icon", "Sprites/Armas/Espadas/EspadaSacraCerulea/Icone_E1.png") # Exemplo
        )

        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        # Defina os caminhos e valores REAIS para os seus assets aqui.
        self._stats_by_level = {
            # Nível 1.0
            1.0: {
                "damage": 30.0,
                # Exemplo de cálculo de range: (largura_sprite_jogador/2) + (hitbox_dim[0]/2)
                # Se jogador tem 60 de largura (borda a 30 do centro), e hitbox_dim[0] é 70 (metade 35), range = 30 + 35 = 65
                "range": 65.0, # Ajuste este valor!
                "cooldown": 1.5,
                "name_suffix": "", # Sem sufixo para o nome base
                "hitbox_dim": (70, 100),   # CONFIGURÁVEL: Largura e altura da hitbox de dano
                "hitbox_off": (0, 0),      # CONFIGURÁVEL: Offset adicional da hitbox (normalmente 0,0)
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaSacraCerulea/Efeitos/ImpactoNv1.png", # Exemplo
                "effect_scale_base": 1.0,  # Escala do efeito de impacto
                "animation_sprites": [     # CONFIGURÁVEL: Caminhos para os sprites da animação de ataque
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv1/Frame1.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv1/Frame2.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv1/Frame3.png"
                ],
                "animation_speed": 100,     # CONFIGURÁVEL: Velocidade da animação visual (ms por frame)
                "animation_display_scale": 1.0, # CONFIGURÁVEL: Escala do sprite da animação visual
                "ui_icon": "Sprites/Armas/Espadas/EspadaSacraCerulea/Icone_E1.png" # Exemplo
            },
            1.5: {
                "damage": 35.0, "range": 70.0, "cooldown": 1.4, "name_suffix": "+1",
                "hitbox_dim": (75, 105), "hitbox_off": (0, 0), # Exemplo
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaSacraCerulea/Efeitos/ImpactoNv1.png", # Pode ser o mesmo ou mudar
                "effect_scale_base": 1.05,
                "animation_sprites": [ # Pode reusar ou ter animação levemente diferente
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv1/Frame1.png", # Reutilizando
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv1/Frame2.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv1/Frame3.png"
                ],
                "animation_speed": 95,
                "animation_display_scale": 1.0, # Mesma escala de animação
                "ui_icon": "Sprites/Armas/Espadas/EspadaSacraCerulea/Icone_E1.png" # Exemplo, pode ser o mesmo
            },
            2.0: {
                "damage": 45.0, "range": 75.0, "cooldown": 1.2, "name_suffix": " Desperta",
                "hitbox_dim": (80, 110), "hitbox_off": (0, 0), # Exemplo
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaSacraCerulea/Efeitos/ImpactoNv2.png", # Exemplo
                "effect_scale_base": 1.1,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv2/Frame1.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv2/Frame2.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv2/Frame3.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv2/Frame4.png"
                ],
                "animation_speed": 90,
                "animation_display_scale": 1.1, # Animação um pouco maior
                "ui_icon": "Sprites/Armas/Espadas/EspadaSacraCerulea/Icone_E2.png" # Exemplo
            },
            2.5: {
                "damage": 50.0, "range": 80.0, "cooldown": 1.1, "name_suffix": " Desperta +1",
                "hitbox_dim": (85, 115), "hitbox_off": (0, 0), # Exemplo
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaSacraCerulea/Efeitos/ImpactoNv2.png", # Exemplo
                "effect_scale_base": 1.15,
                "animation_sprites": [ # Reutilizando animação do Nv2
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv2/Frame1.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv2/Frame2.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv2/Frame3.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv2/Frame4.png"
                ],
                "animation_speed": 85,
                "animation_display_scale": 1.1,
                "ui_icon": "Sprites/Armas/Espadas/EspadaSacraCerulea/Icone_E2.png" # Exemplo
            },
            3.0: {
                "damage": 65.0, "range": 85.0, "cooldown": 0.9, "name_suffix": " Sacra",
                "hitbox_dim": (90, 120), "hitbox_off": (0, 0), # Exemplo
                "effect_sprite_base": "Sprites/Armas/Espadas/EspadaSacraCerulea/Efeitos/ImpactoNv3.png", # Exemplo
                "effect_scale_base": 1.2,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv3/Frame1.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv3/Frame2.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv3/Frame3.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv3/Frame4.png",
                    "Sprites/Armas/Espadas/EspadaSacraCerulea/Ataque/Nv3/Frame5.png"
                ],
                "animation_speed": 80,
                "animation_display_scale": 1.2, # Animação maior e mais imponente
                "ui_icon": "Sprites/Armas/Espadas/EspadaSacraCerulea/Icone_E3.png" # Exemplo
            }
        }

        # Atributos para a animação de ataque da arma (não o efeito visual do impacto)
        self.attack_animation_sprites = []  # Lista de superfícies pygame carregadas para a animação
        self.attack_animation_paths = []    # Mantém os caminhos atuais para checagem de mudança
        self.attack_animation_speed = 100   # Velocidade da animação em ms por frame
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0 # Timestamp da última atualização do frame da animação
        self.animation_display_scale_factor = 1.0 # Escala aplicada aos sprites da animação

        self._apply_level_stats() # Aplica os stats do nível inicial
        # print(f"DEBUG(EspadaSacraCerulea): Espada '{self.name}' criada no Nível {self.level}.")

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        """
        Retorna o dicionário de stats para um nível específico.
        Se 'for_super_init' é True, ou se _stats_by_level não está definido,
        retorna um dicionário de fallback com valores padrão para garantir que super().__init__() funcione.
        """
        # Caso especial para o super().__init__() ou se _stats_by_level ainda não foi inicializado
        if for_super_init or not hasattr(self, '_stats_by_level') or not self._stats_by_level:
            # Estes são valores de fallback absolutos para o construtor da classe base.
            # Tente usar o nível 1.0 de _stats_by_level se já estiver definido, caso contrário, use hardcoded defaults.
            # No entanto, _stats_by_level pode não estar disponível quando este método é chamado por for_super_init.
            if hasattr(self, '_stats_by_level') and self._stats_by_level and 1.0 in self._stats_by_level:
                 # Se estamos em for_super_init mas _stats_by_level já foi preenchido (improvável na ordem normal)
                 # ou se não é for_super_init mas estamos aqui por alguma razão (ex: _stats_by_level vazio)
                return self._stats_by_level[1.0] # Use o nível 1.0 como base
            else:
                # Fallback hardcoded se _stats_by_level não estiver disponível ou não contiver o nível 1.0
                return {
                    "damage": 30.0, "range": 100.0, "cooldown": 1.5, "name_suffix": "",
                    "hitbox_dim": (50, 100), "hitbox_off": (0, 0),
                    "effect_sprite_base": "Sprites/Armas/Espadas/EspadaSacraCerulea/Efeitos/ImpactoDefault.png", # Caminho de fallback
                    "effect_scale_base": 1.0,
                    "animation_sprites": [], "animation_speed": 100, "animation_display_scale": 1.0,
                    "ui_icon": "Sprites/Armas/Espadas/EspadaSacraCerulea/Icone_Default.png" # Caminho de fallback
                }

        # Se _stats_by_level existe e o nível está lá
        if level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else:
            # Fallback para o nível mais próximo ou o primeiro nível definido se o exato não existir
            # E não estamos na chamada do super().__init__()
            print(f"WARN(EspadaSacraCerulea): Nível {level_to_check} não encontrado em _stats_by_level. Usando fallback para o primeiro nível.")
            first_level_key = next(iter(self._stats_by_level))
            return self._stats_by_level[first_level_key]


    def _load_weapon_attack_animation_sprites(self, caminhos, escala_animacao=1.0):
        """
        Carrega e escala os sprites de animação de ATK da arma (não confundir com efeito de impacto).
        Estes são os sprites que mostram a arma se movendo, por exemplo.
        """
        sprites_carregados = []
        # Determina o caminho base do projeto para encontrar a pasta 'Sprites'
        # __file__ é o caminho para EspadaSacraCerulea.py (ex: .../SeuJogo/Armas/EspadaSacraCerulea.py)
        base_dir_arma = os.path.dirname(os.path.abspath(__file__)) # .../SeuJogo/Armas
        project_root = os.path.dirname(base_dir_arma) # .../SeuJogo (assume que 'Armas' está um nível abaixo da raiz do projeto)

        for path_relativo in caminhos:
            # Garante que o separador de diretório está correto para o OS atual
            # Remove barras iniciais se houver para garantir que os.path.join funcione corretamente
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
                        print(f"WARN(EspadaSacraCerulea): Escala da animação resultou em dimensão inválida para '{full_path}'. Usando placeholder.")
                        # Cria um placeholder pequeno mas válido
                        ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 0.1))) # Garante ph_size > 0
                        placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((255,0,255,100))
                        sprites_carregados.append(placeholder)
                else:
                    print(f"WARN(EspadaSacraCerulea): Sprite de animação de ATK não encontrado '{full_path}'. Usando placeholder.")
                    ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                    placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((255,0,255,100))
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"ERROR(EspadaSacraCerulea): Erro ao carregar sprite de animação de ATK '{full_path}': {e}. Usando placeholder.")
                ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((255,0,255,100))
                sprites_carregados.append(placeholder)

        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0 # Reseta o frame ao carregar nova animação
        # print(f"DEBUG(EspadaSacraCerulea): {len(sprites_carregados)} sprites de animação de ATK carregados para {self.name} com escala {escala_animacao}.")


    def evolve(self, target_level: float):
        """
        Evolui a espada para um nível específico, atualizando suas estatísticas e aparência.
        """
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            # print(f"DEBUG(EspadaSacraCerulea): '{self.name}' evoluiu para o Nível {self.level}!")
        else:
            print(f"WARN(EspadaSacraCerulea): Nível de evolução {target_level} inválido para {self.name}. Níveis disponíveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        """
        Aplica todas as estatísticas e atributos visuais correspondentes ao nível atual da espada.
        """
        stats = self._get_stats_for_level_internal(self.level) # Usa o método interno para garantir fallback
        
        if not stats: # Segurança adicional, embora _get_stats_for_level_internal deva sempre retornar algo
            print(f"ERROR(EspadaSacraCerulea): Falha crítica ao obter stats para o nível {self.level} de '{self.name}'. Nenhuma alteração aplicada.")
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

        # Atualiza o efeito de ataque (o sprite visual que aparece no impacto)
        new_base_effect_path = stats.get("effect_sprite_base")
        new_base_effect_scale = stats.get("effect_scale_base", self.attack_effect_scale)

        if new_base_effect_path and new_base_effect_path != self.attack_effect_sprite_path:
            self.attack_effect_sprite_path = new_base_effect_path
            self.attack_effect_scale = new_base_effect_scale
            super()._load_attack_effect_sprite() # Chama o método da classe base Weapon
        elif new_base_effect_scale != self.attack_effect_scale and self.attack_effect_original_image:
            self.attack_effect_scale = new_base_effect_scale
            if self.attack_effect_original_image:
                width = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                height = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                if width > 0 and height > 0:
                    self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (width, height))
                else:
                    self.attack_effect_image = None
                    print(f"WARN(EspadaSacraCerulea): Escala do efeito de ataque resultou em dimensão inválida para '{self.attack_effect_sprite_path}'.")

        # Atualiza o ícone da UI
        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path and new_ui_icon_path != self.ui_icon_path :
            self.ui_icon_path = new_ui_icon_path
            # A classe Weapon base já armazena ui_icon_path. Se houver um método para carregar o ícone
            # na classe base ou em uma classe de UI, ele seria chamado aqui. Ex: self._load_ui_icon_surface()
            # Por enquanto, apenas o path é atualizado.

        # Atualiza a animação de ataque da arma (sprites da arma se movendo)
        new_animation_paths = stats.get("animation_sprites")
        new_animation_display_scale = stats.get("animation_display_scale", 1.0)

        # Verifica se os caminhos da animação mudaram OU se a escala da animação mudou
        # OU se self.attack_animation_paths ainda não foi definido (primeira carga)
        # E se new_animation_paths não é None (para evitar erro se não definido no stats)
        if new_animation_paths is not None:
            if new_animation_paths != self.attack_animation_paths or \
               new_animation_display_scale != self.animation_display_scale_factor or \
               not self.attack_animation_paths: # Força o carregamento na primeira vez
                
                self.attack_animation_paths = new_animation_paths # Atualiza a referência dos caminhos
                self.animation_display_scale_factor = new_animation_display_scale
                self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)

        self.attack_animation_speed = stats.get("animation_speed", 100)

        # Atualiza o nome da arma com o sufixo do nível
        name_suffix = stats.get("name_suffix", "")
        self.name = f"{self._base_name} {name_suffix}".strip()

    def get_current_attack_animation_sprite(self):
        """ Retorna o sprite atual da animação de ATK da arma. """
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None

# --- Bloco de Teste Standalone ---
if __name__ == '__main__':
    # Mock da classe Weapon e pygame para permitir teste sem um ambiente Pygame completo.
    # Isto é útil para verificar a lógica da classe EspadaSacraCerulea isoladamente.

    class MockPygameSurface:
        def __init__(self, width=100, height=100, color=(0,0,0)):
            self._width = width
            self._height = height
            self.color = color
            # print(f"MockPygameSurface criada: {width}x{height}")

        def get_width(self):
            return self._width

        def get_height(self):
            return self._height

        def convert_alpha(self):
            # print("MockPygameSurface.convert_alpha() chamada")
            return self # Retorna a si mesma para simplificar

        def fill(self, color):
            # print(f"MockPygameSurface.fill() chamada com {color}")
            self.color = color
            
    class MockPygameImage:
        def load(self, path):
            # print(f"MockPygame.image.load() chamado para: {path}")
            if "placeholder" in path.lower() or not os.path.exists(path): # Simula falha para placeholders
                 # print(f"Simulando falha ao carregar (ou é placeholder): {path}")
                 return MockPygameSurface(10,10, (255,0,255)) # Retorna um placeholder pequeno
            return MockPygameSurface() # Retorna uma superfície mock bem-sucedida

    class MockPygameTransform:
        def smoothscale(self, surface, dimensions):
            # print(f"MockPygame.transform.smoothscale() chamado para {dimensions}")
            # Retorna uma nova superfície mock com as novas dimensões
            return MockPygameSurface(dimensions[0], dimensions[1], surface.color)

    class MockPygame:
        image = MockPygameImage()
        transform = MockPygameTransform()
        SRCALPHA = "SRCALPHA_FLAG" # Flag mock
        error = type('MockPygameError', (Exception,), {}) # Mock para pygame.error

        def Surface(self, dimensions, flags=0):
            # print(f"MockPygame.Surface() chamada com {dimensions}, flags={flags}")
            return MockPygameSurface(dimensions[0], dimensions[1])

    pygame = MockPygame() # Sobrescreve o import real do pygame com nosso mock

    # Mock simples da classe base Weapon
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
            self.attack_effect_original_image = None # Mock: imagem original do efeito
            self.attack_effect_image = None          # Mock: imagem do efeito, possivelmente escalada
            # print(f"Mock da Classe Base Weapon '{name}' inicializada.")

        def _load_attack_effect_sprite(self):
            # Simula o carregamento do sprite de efeito da classe base
            # print(f"WeaponBaseMock: _load_attack_effect_sprite() chamado para {self.attack_effect_sprite_path} com escala {self.attack_effect_scale}")
            if self.attack_effect_sprite_path:
                self.attack_effect_original_image = pygame.image.load(self.attack_effect_sprite_path)
                if self.attack_effect_original_image:
                    w = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                    h = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                    if w > 0 and h > 0:
                         self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (w,h))
                    else:
                        self.attack_effect_image = None # Falha na escala
            else:
                self.attack_effect_original_image = None
                self.attack_effect_image = None

    Weapon = BaseWeaponMock # Sobrescreve a importação de Weapon com nosso mock

    # Mock para os.path.exists para simular que os arquivos de sprite existem
    # (exceto se o caminho contiver "placeholder" ou um caminho que você queira testar como não existente)
    original_os_path_exists = os.path.exists
    def mock_os_path_exists(path):
        if "naoexiste" in path: # Exemplo para simular um arquivo que não existe
            return False
        # print(f"Mock os.path.exists verificando: {path}")
        return True # Assume que a maioria dos caminhos existe para o teste
    os.path.exists = mock_os_path_exists


    print("\n--- INICIANDO TESTE STANDALONE DA ESPADA BRASAS ---")
    espada_teste = EspadaSacraCerulea()
    print(f"Espada Criada: '{espada_teste.name}', Nível: {espada_teste.level}, Dano: {espada_teste.damage}")
    print(f"  Ícone UI: {espada_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {espada_teste.attack_animation_paths}")
    print(f"  Hitbox: {espada_teste.hitbox_width}x{espada_teste.hitbox_height} @ ({espada_teste.hitbox_offset_x},{espada_teste.hitbox_offset_y})")
    print(f"  Sprite de Animação ATK Atual (Frame 0): {espada_teste.get_current_attack_animation_sprite()}")

    print("\n--- Testando Evolução para Nível 1.5 ---")
    espada_teste.evolve(1.5)
    print(f"Espada Evoluída: '{espada_teste.name}', Nível: {espada_teste.level}, Dano: {espada_teste.damage}, Cooldown: {espada_teste.cooldown}")
    print(f"  Ícone UI: {espada_teste.ui_icon_path}")
    print(f"  Animação ATK Paths: {espada_teste.attack_animation_paths}") # Deve ser o mesmo do Nv1 neste exemplo
    print(f"  Sprite de Animação ATK Atual (Frame 0): {espada_teste.get_current_attack_animation_sprite()}")


    print("\n--- Testando Evolução para Nível 2.0 ---")
    espada_teste.evolve(2.0)
    print(f"Espada Evoluída: '{espada_teste.name}', Nível: {espada_teste.level}, Dano: {espada_teste.damage}")
    print(f"  Ícone UI: {espada_teste.ui_icon_path}") # Deve ter mudado
    print(f"  Animação ATK Paths: {espada_teste.attack_animation_paths}") # Devem ter mudado
    print(f"  Velocidade Animação ATK: {espada_teste.attack_animation_speed}ms, Escala: {espada_teste.animation_display_scale_factor}")
    print(f"  Sprite de Animação ATK Atual (Frame 0): {espada_teste.get_current_attack_animation_sprite()}")


    print("\n--- Testando Evolução para Nível 3.0 ---")
    espada_teste.evolve(3.0)
    print(f"Espada Evoluída: '{espada_teste.name}', Nível: {espada_teste.level}, Dano: {espada_teste.damage}")
    print(f"  Ícone UI: {espada_teste.ui_icon_path}")
    print(f"  Caminho Efeito de Ataque: {espada_teste.attack_effect_sprite_path}, Escala: {espada_teste.attack_effect_scale}")
    print(f"  Sprite de Animação ATK Atual (Frame 0): {espada_teste.get_current_attack_animation_sprite()}")


    print("\n--- Testando Evolução para Nível Inválido (5.0) ---")
    espada_teste.evolve(5.0) # Não deve mudar nada e imprimir aviso.
    print(f"Após tentar evoluir para 5.0: '{espada_teste.name}', Nível: {espada_teste.level} (deve ser 3.0)")

    print("\n--- FIM DO TESTE STANDALONE ---")

    # Restaura os mocks se necessário para outros testes no mesmo ambiente
    os.path.exists = original_os_path_exists
