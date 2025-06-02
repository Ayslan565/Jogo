# Armas/LaminaDoCeuCentilante.py (ou LaminaCeuCinti.py, conforme seu nome de arquivo)
import pygame
import os
# Assume que weapon.py está no mesmo diretório 'Armas' ou em um local acessível via Python path
from .weapon import Weapon

class LaminaDoCeuCentilhante(Weapon):
    """
    Representa a Lâmina do Ceu Centilhante, uma arma específica com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Lâmina do Ceu Centilhante"
        self.level = 1.0 # Nível inicial

        # Obtém stats iniciais para o construtor da superclasse
        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name, # O nome completo com sufixos será definido em _apply_level_stats
            damage=initial_stats_for_super.get("damage", 35.0), # Placeholder
            attack_range=initial_stats_for_super.get("range", 110.0), # Placeholder
            cooldown=initial_stats_for_super.get("cooldown", 1.3), # Placeholder
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (60, 110)), # Placeholder
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (0, 0)), # Placeholder
            description="Rápida como um raio, afiada como uma estrela.", # Descrição base
            rarity="Lendária", # SUGESTÃO - Adapte conforme necessário
            weapon_type="Espada",
            element="Raio", # SUGESTÃO - Adapte conforme necessário (Ex: Luz, Vento)
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base", None),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 1.0),
            # Ícone UI base - o da loja é "Sprites/Armas/Espadas/Lâmina do Ceu Centilhante/E1.jpg"
            # Adapte para o ícone específico de inventário/UI se necessário.
            ui_icon_path=initial_stats_for_super.get("ui_icon", "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Icone_LCC1.png") # PLACEHOLDER
        )

        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        # Defina os caminhos e valores REAIS para os seus assets e balanceamento aqui.
        self._stats_by_level = {
            1.0: {
                "damage": 35.0, "range": 110.0, "cooldown": 1.3, "name_suffix": "",
                "hitbox_dim": (60, 110),    # PLACEHOLDER
                "hitbox_off": (0, 0),       # PLACEHOLDER
                "effect_sprite_base": "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Efeitos/ImpactoRaioNv1.png", # PLACEHOLDER
                "effect_scale_base": 1.0,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv1/RaioFrame1.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv1/RaioFrame2.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv1/RaioFrame3.png"   # PLACEHOLDER
                ],
                "animation_speed": 80,      # PLACEHOLDER (ms por frame)
                "animation_display_scale": 1.0, # PLACEHOLDER
                "ui_icon": "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Icone_LCC1.png" # PLACEHOLDER
            },
            1.5: { # Exemplo de evolução intermediária
                "damage": 42.0, "range": 115.0, "cooldown": 1.25, "name_suffix": "+1",
                "hitbox_dim": (65, 115), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Efeitos/ImpactoRaioNv1.png", # PLACEHOLDER
                "effect_scale_base": 1.05,
                "animation_sprites": [ # Pode reutilizar ou ter novos sprites
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv1/RaioFrame1.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv1/RaioFrame2.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv1/RaioFrame3.png"   # PLACEHOLDER
                ],
                "animation_speed": 75,
                "animation_display_scale": 1.0,
                "ui_icon": "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Icone_LCC1.png" # PLACEHOLDER
            },
            2.0: { # Exemplo de segunda evolução principal
                "damage": 55.0, "range": 125.0, "cooldown": 1.1, "name_suffix": "Fulgorante", # SUGESTÃO de nome
                "hitbox_dim": (70, 120), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Efeitos/ImpactoRaioNv2.png", # PLACEHOLDER
                "effect_scale_base": 1.1,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv2/FulgorFrame1.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv2/FulgorFrame2.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv2/FulgorFrame3.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv2/FulgorFrame4.png"   # PLACEHOLDER
                ],
                "animation_speed": 70,
                "animation_display_scale": 1.1,
                "ui_icon": "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Icone_LCC2.png" # PLACEHOLDER
            },
            2.5: { # Exemplo de evolução intermediária
                "damage": 63.0, "range": 130.0, "cooldown": 1.05, "name_suffix": "Fulgorante +1",
                "hitbox_dim": (75, 125), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Efeitos/ImpactoRaioNv2.png", # PLACEHOLDER
                "effect_scale_base": 1.15,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv2/FulgorFrame1.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv2/FulgorFrame2.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv2/FulgorFrame3.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv2/FulgorFrame4.png"   # PLACEHOLDER
                ],
                "animation_speed": 65,
                "animation_display_scale": 1.1,
                "ui_icon": "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Icone_LCC2.png" # PLACEHOLDER
            },
            3.0: { # Exemplo de evolução final
                "damage": 80.0, "range": 140.0, "cooldown": 0.9, "name_suffix": "Celestial", # SUGESTÃO de nome
                "hitbox_dim": (80, 130), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Efeitos/ImpactoRaioNv3.png", # PLACEHOLDER
                "effect_scale_base": 1.2,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv3/CelestialFrame1.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv3/CelestialFrame2.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv3/CelestialFrame3.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv3/CelestialFrame4.png", # PLACEHOLDER
                    "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Ataque/Nv3/CelestialFrame5.png"   # PLACEHOLDER
                ],
                "animation_speed": 60,
                "animation_display_scale": 1.15,
                "ui_icon": "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Icone_LCC3.png" # PLACEHOLDER
            }
        }

        self.attack_animation_sprites = []
        self.attack_animation_paths = [] 
        self.attack_animation_speed = 100
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0 

        self._apply_level_stats() 
        # print(f"DEBUG(LaminaDoCeuCentilante): Lâmina '{self.name}' criada no Nível {self.level}.")

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        """ Obtém os stats brutos para um nível. Uso interno e para inicialização. """
        if for_super_init or not hasattr(self, '_stats_by_level') or not self._stats_by_level:
            if hasattr(self, '_stats_by_level') and self._stats_by_level and 1.0 in self._stats_by_level:
                return self._stats_by_level[1.0]
            else:
                print(f"WARN(LaminaDoCeuCentilante): Fallback absoluto em _get_stats_for_level_internal para Nível {level_to_check}")
                return {
                    "damage": 35.0, "range": 110.0, "cooldown": 1.3, "name_suffix": "",
                    "hitbox_dim": (60, 110), "hitbox_off": (0, 0),
                    "effect_sprite_base": "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Efeitos/ImpactoRaioDefault.png", 
                    "effect_scale_base": 1.0,
                    "animation_sprites": [], "animation_speed": 100, "animation_display_scale": 1.0,
                    "ui_icon": "Sprites/Armas/Espadas/LaminaDoCeuCentilante/Icone_DefaultLCC.png" 
                }

        if level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else:
            print(f"WARN(LaminaDoCeuCentilante): Nível {level_to_check} não encontrado em _stats_by_level. Usando fallback para o primeiro nível.")
            first_level_key = next(iter(self._stats_by_level)) 
            return self._stats_by_level[first_level_key]

    def _load_weapon_attack_animation_sprites(self, caminhos, escala_animacao=1.0):
        """ Carrega e escala os sprites da animação de ataque da arma. """
        sprites_carregados = []
        base_dir_arma = os.path.dirname(os.path.abspath(__file__)) 
        project_root = os.path.dirname(base_dir_arma) 

        for path_relativo_ao_projeto in caminhos: 
            path_corrigido = path_relativo_ao_projeto.replace("\\", os.sep).replace("/", os.sep)
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
                        print(f"WARN(LaminaDoCeuCentilante): Escala inválida para sprite de animação '{full_path}'. Criando placeholder.")
                        ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 0.1))) 
                        placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((100,100,255,100)) 
                        sprites_carregados.append(placeholder)
                else:
                    print(f"WARN(LaminaDoCeuCentilante): Sprite de animação ATK não encontrado em '{full_path}'. Criando placeholder.")
                    ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                    placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((100,100,255,100))
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"ERROR(LaminaDoCeuCentilante): Erro ao carregar sprite ATK '{full_path}': {e}. Criando placeholder.")
                ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((100,100,255,100))
                sprites_carregados.append(placeholder)
        
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0 
        # print(f"DEBUG(LaminaDoCeuCentilante): {len(sprites_carregados)} sprites de animação ATK carregados para '{self.name}' com escala {escala_animacao}.")

    def evolve(self, target_level: float):
        """ Evolui a arma para um nível específico, se definido em _stats_by_level. """
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            # print(f"DEBUG(LaminaDoCeuCentilante): '{self.name}' evoluiu para Nível {self.level}!")
        else:
            print(f"WARN(LaminaDoCeuCentilante): Tentativa de evoluir para nível inválido {target_level}. Níveis disponíveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        """ Aplica os stats, nome, sprites de efeito e animação para o nível atual da arma. """
        stats = self._get_stats_for_level_internal(self.level)
        if not stats: 
            print(f"ERROR(LaminaDoCeuCentilante): Falha crítica ao obter stats para Nível {self.level} de '{self._base_name}'. Nenhuma alteração aplicada.")
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
                    print(f"WARN(LaminaDoCeuCentilante): Escala do efeito de ataque inválida para '{self.attack_effect_sprite_path}'. Efeito desabilitado.")
        
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
        """ Retorna o sprite atual da animação de ataque. """
        if self.attack_animation_sprites and \
           0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None
