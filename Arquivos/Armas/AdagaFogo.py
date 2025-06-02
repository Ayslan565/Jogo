# AdagaFogo.py
import pygame
import os
from weapon import Weapon

class AdagaFogo(Weapon):
    """
    Representa a Adaga do Fogo Contudente, uma arma com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Adaga do Fogo Contudente"
        self.level = 1.0 # Nível inicial

        # Obtém os stats iniciais para o nível 1.0 para passar ao construtor da classe base.
        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name, 
            damage=initial_stats_for_super.get("damage", 500.0), 
            # CONFIGURÁVEL: Distância do centro do player ao CENTRO da hitbox da arma.
            # Ajuste isto para posicionar a hitbox ao lado do jogador.
            # Ex: (largura_sprite_jogador / 2) + (largura_hitbox_arma / 2)'
            attack_range=initial_stats_for_super.get("range",80 ), 
            cooldown=initial_stats_for_super.get("cooldown", 0.35), 
            # CONFIGURÁVEL: (largura, altura) da HITBOX LÓGICA de dano.
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (150, 45)), 
            # CONFIGURÁVEL: Offset (dx, dy) para o CENTRO da hitbox LÓGICA, relativo ao ponto definido por attack_range.
            # Geralmente (0,0) se 'attack_range' estiver bem calculado.
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (0, 0)), 
            description="Uma adaga rápida envolta em chamas.",
            rarity="Comum",
            weapon_type="Adaga",
            element="Fogo",
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base", None),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 1.0),
            ui_icon_path=initial_stats_for_super.get("ui_icon", "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Adaga E-1.png")
        )
        
        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        self._stats_by_level = {
            # Nível 1.0
            1.0: {
                "damage": 15.0, 
                # CONFIGURÁVEL: (largura_sprite_jogador/2) + (hitbox_dim[0]/2)
                # Se o jogador tem 60 de largura, sua borda está a 30 do centro.
                # Se hitbox_dim[0] é 35, metade é 17.5. Range = 30 + 17.5 = 47.5
                "range": 80 + (15/2), 
                "cooldown": 0.35, 
                "name_suffix": "", 
                "hitbox_dim": (60, 60),     # CONFIGURÁVEL: Largura e altura da hitbox de dano
                "hitbox_off": (0, 0),       # CONFIGURÁVEL: Offset adicional da hitbox (normalmente 0,0)
                "effect_sprite_base": "Sprites/Armas/Espadas/Adaga/Ataque/Corte1.png", # Efeito secundário (opcional)
                "effect_scale_base": 1.0,                                            # Escala do efeito secundário
                # CONFIGURÁVEL: Caminhos para os sprites da animação de ataque principal
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT0.png", 
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/Corte1.png", 
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/Corte2.png", 
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/Corte3.png", 
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/Corte4.png", 
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/Corte5.png",
                ], 
                "animation_speed": 60,      # CONFIGURÁVEL: Velocidade da animação visual (ms por frame)
                "animation_display_scale":0.4, # CONFIGURÁVEL: Escala do sprite da animação visual
                "ui_icon": "C:/Users/aysla/Documents/Jogo_Asrahel/Jogo/Arquivos/Armas/Armas/Espadas/Adaga do Fogo Contudente/Adaga E-1.png"
            },
            1.5: {
                "damage": 18.0, "range": 30 + (37/2), "cooldown": 0.33, "name_suffix": "+1", 
                "hitbox_dim": (37, 47), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/Adaga/Ataque/Corte1.png", "effect_scale_base": 1.1,
                "animation_sprites": ["Sprites/Armas/Espadas/Adaga/Ataque/Corte2.png", "Sprites/Armas/Espadas/Adaga/Ataque/Corte3.png", "Sprites/Armas/Espadas/Adaga/Ataque/Corte4.png","Sprites/Armas/Espadas/Adaga/Ataque/Corte5.png"], 
                "animation_speed": 55, "animation_display_scale": 2.1,
                "ui_icon": "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Adaga E-1.png" 
            },
            2.0: {
                "damage": 22.0, "range": 30 + (40/2), "cooldown": 0.30, "name_suffix": " Reforjada", 
                "hitbox_dim": (40, 50), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Armas/Espadas/Adaga/Ataque/CorteForte1.png", "effect_scale_base": 1.2,
                "animation_sprites": ["Sprites/Armas/Espadas/Adaga/Ataque/CorteForte1.png", "Sprites/Armas/Espadas/Adaga/Ataque/CorteForte2.png", "Sprites/Armas/Espadas/Adaga/Ataque/CorteForte3.png","Sprites/Armas/Espadas/Adaga/Ataque/CorteForte4.png","Sprites/Armas/Espadas/Adaga/Ataque/CorteForte5.png"], 
                "animation_speed": 50, "animation_display_scale": 2.3,
                "ui_icon": "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Adaga E-2.png"
            },
             2.5: {"damage": 26.0, "range": 30 + (42/2), "cooldown": 0.28, "name_suffix": " Reforjada +1", 
                  "hitbox_dim": (42, 52), "hitbox_off": (0, 0),
                  "effect_sprite_base": "Sprites/Armas/Espadas/Adaga/Ataque/CorteForte1.png", "effect_scale_base": 1.3, 
                  "animation_sprites": ["Sprites/Armas/Espadas/Adaga/Ataque/CorteForte1.png", "Sprites/Armas/Espadas/Adaga/Ataque/CorteForte2.png", "Sprites/Armas/Espadas/Adaga/Ataque/CorteForte3.png","Sprites/Armas/Espadas/Adaga/Ataque/CorteForte4.png","Sprites/Armas/Espadas/Adaga/Ataque/CorteForte5.png"], 
                  "animation_speed": 55, "animation_display_scale": 2.1,
                  "ui_icon": "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Adaga E-2.png",
},



            3.0: {"damage": 30.0, "range": 30 + (45/2), "cooldown": 0.25, "name_suffix": " Magistral", 
                  "hitbox_dim": (45, 55), "hitbox_off": (0, 0),
                  "effect_sprite_base": "Sprites/Armas/Espadas/Adaga/Ataque/CorteSupremo.png", "effect_scale_base": 1.4, 
                  "animation_sprites": ["Sprites/Armas/Espadas/Adaga/Ataque/CorteSupremo1.png", "Sprites/Armas/Espadas/Adaga/Ataque/CorteSupremo2.png", "Sprites/Armas/Espadas/Adaga/Ataque/CorteSupremo3.png","Sprites/Armas/Espadas/Adaga/Ataque/CorteSupremo4.png","Sprites/Armas/Espadas/Adaga/Ataque/CorteSupremo5.png"], 
                  "animation_speed": 50, "animation_display_scale": 2.2,
                  "ui_icon": "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Adaga E-3.png"}
        }

        self.attack_animation_sprites = [] 
        self.attack_animation_paths = []   
        self.attack_animation_speed = 100  
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0 
        self.animation_display_scale_factor = 1.0 

        self._apply_level_stats() 

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        if hasattr(self, '_stats_by_level') and self._stats_by_level and level_to_check in self._stats_by_level and not for_super_init:
             return self._stats_by_level[level_to_check]
        
        # Fallback para o __init__ da classe base, usando valores do nível 1.0 como padrão
        default_level_1_stats = {
            "damage": 15.0, "range": 30 + (35/2), "cooldown": 0.35, 
            "name_suffix": "", 
            "hitbox_dim": (35, 45), "hitbox_off": (0, 0), 
            "effect_sprite_base": "Sprites/Armas/Espadas/Adaga/Ataque/Corte1.png", 
            "effect_scale_base": 1.0,
            "animation_sprites": ["Sprites/Armas/Espadas/Adaga/Ataque/Corte2.png", "Sprites/Armas/Espadas/Adaga/Ataque/Corte3.png", "Sprites/Armas/Espadas/Adaga/Ataque/Corte4.png","Sprites/Armas/Espadas/Adaga/Ataque/Corte5.png"], 
            "animation_speed": 60,
            "animation_display_scale": 2.0, 
            "ui_icon": "Sprites/Armas/Icones/adaga_fogo_icon_nv1.png"
        }
        if for_super_init: # Se chamado pelo super().__init__
            return default_level_1_stats
        
        # Fallback mais genérico se o nível não for 1.0 e _stats_by_level não estiver pronto
        return {"damage": 10, "range": 30, "cooldown": 0.5, "hitbox_dim": (30,30), "hitbox_off": (0,0), 
                "effect_sprite_base": None, "effect_scale_base": 1.0, 
                "animation_sprites": [], "animation_speed": 100, "animation_display_scale": 1.0, 
                "name_suffix": "", "ui_icon": None}

    def _load_weapon_attack_animation_sprites(self, caminhos, escala_animacao=1.0):
        sprites_carregados = []
        base_dir_arma = os.path.dirname(os.path.abspath(__file__)) 
        base_dir_arquivos = os.path.dirname(base_dir_arma) 
        project_root = os.path.dirname(base_dir_arquivos) 

        for path_relativo in caminhos:
            full_path = os.path.join(project_root, path_relativo.replace("\\", os.sep))
            try:
                if os.path.exists(full_path):
                    imagem_original = pygame.image.load(full_path).convert_alpha()
                    novo_w = int(imagem_original.get_width() * escala_animacao)
                    novo_h = int(imagem_original.get_height() * escala_animacao)
                    if novo_w > 0 and novo_h > 0 : 
                        imagem = pygame.transform.smoothscale(imagem_original, (novo_w, novo_h))
                        sprites_carregados.append(imagem)
                    else:
                        placeholder = pygame.Surface((int(50*escala_animacao) if escala_animacao > 0 else 50, int(50*escala_animacao) if escala_animacao > 0 else 50), pygame.SRCALPHA); placeholder.fill((255,0,255,100)) 
                        sprites_carregados.append(placeholder)
                else:
                    placeholder = pygame.Surface((int(50*escala_animacao) if escala_animacao > 0 else 50, int(50*escala_animacao) if escala_animacao > 0 else 50), pygame.SRCALPHA); placeholder.fill((255,0,255,100)) 
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"DEBUG(AdagaFogo): Erro ao carregar sprite de animação de ataque '{full_path}': {e}")
                placeholder = pygame.Surface((int(50*escala_animacao) if escala_animacao > 0 else 50, int(50*escala_animacao) if escala_animacao > 0 else 50), pygame.SRCALPHA); placeholder.fill((255,0,255,100))
                sprites_carregados.append(placeholder)
        
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0 

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()

    def _apply_level_stats(self):
        stats = self._stats_by_level.get(self.level)
        if stats:
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
                width = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                height = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                if width > 0 and height > 0:
                    self.attack_effect_image = pygame.transform.scale(self.attack_effect_original_image, (width, height))

            new_ui_icon_path = stats.get("ui_icon")
            if new_ui_icon_path:
                self.ui_icon_path = new_ui_icon_path

            new_animation_paths = stats.get("animation_sprites")
            self.animation_display_scale_factor = stats.get("animation_display_scale", 1.0) 
            
            if new_animation_paths: 
                # Recarrega se os paths mudaram OU se a escala da animação mudou
                if new_animation_paths != self.attack_animation_paths or \
                   (not hasattr(self, '_last_loaded_anim_scale') or self._last_loaded_anim_scale != self.animation_display_scale_factor):
                    self.attack_animation_paths = new_animation_paths
                    self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)
            
            self._last_loaded_anim_scale = self.animation_display_scale_factor 

            self.attack_animation_speed = stats.get("animation_speed", 100)

            name_suffix = stats.get("name_suffix", "")
            self.name = f"{self._base_name} {name_suffix}".strip()

    def get_current_attack_animation_sprite(self):
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None
