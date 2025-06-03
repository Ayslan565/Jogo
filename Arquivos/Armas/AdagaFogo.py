# Nome do Arquivo: AdagaFogo.py
# Local: Jogo/Arquivos/Armas/AdagaFogo.py
import pygame
import os
from .weapon import Weapon # Importa a classe base Weapon do mesmo pacote

class AdagaFogo(Weapon):
    """
    Representa a Adaga do Fogo Contudente, uma arma com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Adaga do Fogo Contudente"
        self.level = 1.0 # Nível inicial

        # Obtém os stats iniciais para o nível 1.0 para passar ao construtor da classe base.
        # Este método deve retornar um dicionário com os stats do nível 1.0.
        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name, 
            damage=initial_stats_for_super.get("damage", 15.0), # Dano do Nível 1
            attack_range=initial_stats_for_super.get("range", 87.5), # Range do Nível 1
            cooldown=initial_stats_for_super.get("cooldown", 0.35), # Cooldown do Nível 1
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (60, 60)), # Hitbox do Nível 1
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (0, 0)), 
            description="Uma adaga rápida envolta em chamas.",
            rarity="Comum",
            weapon_type="Adaga",
            element="Fogo",
            # Caminho relativo à pasta 'Jogo/'
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base", "Sprites/Efeitos/Genericos/CorteSimples.png"),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 1.0),
            # Caminho relativo à pasta 'Jogo/' para o ícone UI do Nível 1
            ui_icon_path=initial_stats_for_super.get("ui_icon", "Sprites/Armas/Icones/AdagaFogo_Nv1.png")
        )
        
        # --- CONFIGURAÇÕES MODIFICÁVEIS POR NÍVEL ---
        # Todos os caminhos de sprites aqui devem ser RELATIVOS à pasta 'Jogo/'
        self._stats_by_level = {
            # Nível 1.0
            1.0: {
                "damage": 15.0, 
                "range": 80 + (15/2), # Exemplo: 87.5
                "cooldown": 0.35, 
                "name_suffix": "", 
                "hitbox_dim": (60, 60),
                "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Efeitos/Fogo/ImpactoChamaPequena.png", # Exemplo de efeito de fogo
                "effect_scale_base": 1.0,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT0-base0.png", 
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT1-base1.png", 
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT2-base2.png",
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT3-base3.png", 
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT4-base4.png",
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT5-base5.png",
                ], 
                "animation_speed": 60,
                "animation_display_scale":0.4,
                # Caminho RELATIVO à pasta 'Jogo/'
                "ui_icon": "Sprites/Armas/Icones/AdagaFogo_Nv1.png" # Exemplo de ícone para Nv1
            },
            1.5: {
                "damage": 18.0, "range": 80 + (18/2), "cooldown": 0.33, "name_suffix": "+1", 
                "hitbox_dim": (62, 62), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Efeitos/Fogo/ImpactoChamaPequena.png", "effect_scale_base": 1.1,
                "animation_sprites": [
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT0-base0.png", 
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT1-base1.png", 
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT2-base2.png",
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT3-base3.png", 
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT4-base4.png",
                    "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Ataque/AT1/AT5-base5.png",
                ], 
                "animation_speed": 55, "animation_display_scale": 0.42,
                "ui_icon": "Sprites/Armas/Icones/AdagaFogo_Nv1.png" # Pode ser o mesmo ou diferente
            },
            2.0: {
                "damage": 22.0, "range": 80 + (22/2), "cooldown": 0.30, "name_suffix": " Reforjada", 
                "hitbox_dim": (65, 65), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Efeitos/Fogo/ImpactoChamaMedia.png", "effect_scale_base": 1.2,
                "animation_sprites": [
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT2\AT2-base0.png", 
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT2\AT2-base1.png", 
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT2\AT2-base2.png",
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT2\AT2-base3.png",
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT2\AT2-base4.png",
                ], 
                "animation_speed": 50, "animation_display_scale": 0.45,
                "ui_icon": "Sprites/Armas/Icones/AdagaFogo_Nv2.png" # Exemplo de ícone para Nv2
            },
            2.5: {
                "damage": 26.0, "range": 80 + (26/2), "cooldown": 0.28, "name_suffix": " Reforjada +1", 
                "hitbox_dim": (67, 67), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Efeitos/Fogo/ImpactoChamaMedia.png", "effect_scale_base": 1.3, 
                "animation_sprites": [
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT2\AT2-base0.png", 
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT2\AT2-base1.png", 
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT2\AT2-base2.png",
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT2\AT2-base3.png",
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT2\AT2-base4.png",
                ], 
                "animation_speed": 45, "animation_display_scale": 0.47,
                "ui_icon": "Sprites/Armas/Icones/AdagaFogo_Nv2.png",
            },
            3.0: {
                "damage": 30.0, "range": 80 + (30/2), "cooldown": 0.25, "name_suffix": " Magistral", 
                "hitbox_dim": (70, 70), "hitbox_off": (0, 0),
                "effect_sprite_base": "Sprites/Efeitos/Fogo/ImpactoChamaGrande.png", "effect_scale_base": 1.4, 
                "animation_sprites": [
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT3\AT3-base0.png", 
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT3\AT3-base1.png",
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT3\AT3-base2.png",
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT3\AT3-base3.png",
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT3\AT3-base4.png",
                    "Sprites\Armas\Espadas\Adaga do Fogo Contudente\Ataque\AT2\AT2-base5.png",
                ], 
                "animation_speed": 40, "animation_display_scale": 0.5,
                "ui_icon": "Sprites/Armas/Icones/AdagaFogo_Nv3.png" # Exemplo de ícone para Nv3
            }
        }

        # Atributos para a animação de ataque (gerenciados pela classe AdagaFogo)
        self.attack_animation_sprites = [] 
        self.attack_animation_paths = []   
        self.attack_animation_speed = 100  
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0 
        self.animation_display_scale_factor = 1.0 
        self._last_loaded_anim_scale = 1.0 # Para verificar se precisa recarregar sprites da animação

        # Aplica os stats do nível inicial, incluindo o carregamento dos sprites de animação e UI icon.
        self._apply_level_stats() 

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        """
        Obtém os stats brutos para um nível. Usado internamente e para a inicialização da superclasse.
        Garante que, para a inicialização da superclasse, sempre retorne os stats do nível 1.0.
        """
        if for_super_init:
            # Para o super().__init__(), sempre use os stats definidos para o nível 1.0, se disponíveis.
            # Se _stats_by_level ainda não foi definido (o que não deveria acontecer aqui, mas por segurança),
            # ou se 1.0 não estiver lá, usa um fallback absoluto.
            if hasattr(self, '_stats_by_level') and self._stats_by_level and 1.0 in self._stats_by_level:
                return self._stats_by_level[1.0]
            else:
                # Fallback absoluto para o __init__ da classe base, se _stats_by_level[1.0] não estiver acessível.
                # Isso garante que o super().__init__() receba valores válidos.
                # print("AVISO(AdagaFogo): Usando fallback absoluto em _get_stats_for_level_internal para super init.")
                return {
                    "damage": 15.0, "range": 87.5, "cooldown": 0.35, 
                    "name_suffix": "", 
                    "hitbox_dim": (60, 60), "hitbox_off": (0, 0), 
                    "effect_sprite_base": "Sprites/Efeitos/Genericos/CorteSimples.png", 
                    "effect_scale_base": 1.0,
                    "animation_sprites": [], 
                    "animation_speed": 60,
                    "animation_display_scale": 0.4, 
                    "ui_icon": "Sprites/Armas/Icones/AdagaFogo_Default.png" # Ícone de fallback
                }
        
        # Para chamadas normais (não for_super_init)
        if hasattr(self, '_stats_by_level') and self._stats_by_level and level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        
        # Fallback se o nível não for encontrado e não for para o super init
        # print(f"AVISO(AdagaFogo): Nível {level_to_check} não encontrado. Usando stats do primeiro nível disponível ou fallback.")
        if hasattr(self, '_stats_by_level') and self._stats_by_level:
            first_level_key = next(iter(self._stats_by_level)) 
            return self._stats_by_level[first_level_key]
        else:
            # Fallback mais genérico se _stats_by_level estiver completamente vazio (improvável)
            return {"damage": 10, "range": 30, "cooldown": 0.5, "hitbox_dim": (30,30), "hitbox_off": (0,0), 
                    "effect_sprite_base": None, "effect_scale_base": 1.0, 
                    "animation_sprites": [], "animation_speed": 100, "animation_display_scale": 1.0, 
                    "name_suffix": "", "ui_icon": None}


    def _load_weapon_attack_animation_sprites(self, caminhos_relativos, escala_animacao=1.0):
        """
        Carrega e escala os sprites da animação de ataque da arma.
        Os caminhos são relativos à pasta raiz do projeto (ex: 'Jogo/').
        """
        sprites_carregados = []
        # project_root é onde está a pasta 'Sprites', geralmente 'Jogo/'
        project_root = self._get_project_root() # Método herdado de Weapon.py

        for path_relativo_ao_jogo in caminhos_relativos:
            # Garante que o separador de diretório está correto para o OS atual
            # e remove qualquer separador inicial para evitar problemas com os.path.join
            path_corrigido = path_relativo_ao_jogo.replace("\\", os.sep).replace("/", os.sep).lstrip(os.sep)
            full_path = os.path.join(project_root, path_corrigido)
            
            try:
                if os.path.exists(full_path):
                    imagem_original = pygame.image.load(full_path).convert_alpha()
                    novo_w = int(imagem_original.get_width() * escala_animacao)
                    novo_h = int(imagem_original.get_height() * escala_animacao)
                    if novo_w > 0 and novo_h > 0 : 
                        imagem = pygame.transform.smoothscale(imagem_original, (novo_w, novo_h))
                        sprites_carregados.append(imagem)
                    else:
                        # print(f"AVISO(AdagaFogo): Escala inválida para sprite de animação '{full_path}'. Criando placeholder.")
                        ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 0.1)))
                        placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((255,0,255,100)) 
                        sprites_carregados.append(placeholder)
                else:
                    # print(f"AVISO(AdagaFogo): Sprite de animação ATK não encontrado em '{full_path}'. Criando placeholder.")
                    ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                    placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((255,0,255,100)) 
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                print(f"ERRO(AdagaFogo): Erro ao carregar sprite ATK '{full_path}': {e}. Criando placeholder.")
                ph_size = max(1, int(50 * (escala_animacao if escala_animacao > 0 else 1.0)))
                placeholder = pygame.Surface((ph_size, ph_size), pygame.SRCALPHA); placeholder.fill((255,0,255,100))
                sprites_carregados.append(placeholder)
        
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0 
        # print(f"DEBUG(AdagaFogo): {len(sprites_carregados)} sprites de animação ATK carregados para '{self.name}' com escala {escala_animacao}.")


    def evolve(self, target_level: float):
        """Evolui a arma para um nível específico, se definido em _stats_by_level."""
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats() # Aplica todos os novos stats, incluindo recarregar sprites se necessário
            # print(f"DEBUG(AdagaFogo): '{self.name}' evoluiu para Nível {self.level}!")
        else:
            print(f"AVISO(AdagaFogo): Tentativa de evoluir para nível inválido {target_level}. Níveis disponíveis: {list(self._stats_by_level.keys())}")

    def _apply_level_stats(self):
        """
        Aplica os stats, nome, sprites de efeito, UI icon e animação para o nível atual da arma.
        """
        stats = self._get_stats_for_level_internal(self.level) # Usa o método interno que tem fallbacks
        if not stats: 
            print(f"ERRO(AdagaFogo): Falha crítica ao obter stats para Nível {self.level} de '{self._base_name}'. Nenhuma alteração aplicada.")
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

        # Lógica para carregar/recarregar o efeito de ataque (herdado de Weapon.py)
        new_base_effect_path = stats.get("effect_sprite_base") 
        new_base_effect_scale = stats.get("effect_scale_base", self.attack_effect_scale) 
        
        if new_base_effect_path and new_base_effect_path != self.attack_effect_sprite_path:
            self.attack_effect_sprite_path = new_base_effect_path
            self.attack_effect_scale = new_base_effect_scale 
            super()._load_attack_effect_sprite() # Chama o método da classe base
        elif new_base_effect_scale != self.attack_effect_scale and self.attack_effect_original_image:
            self.attack_effect_scale = new_base_effect_scale
            # Recarrega com a nova escala se a imagem original já existe
            if self.attack_effect_original_image: 
                width = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                height = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                if width > 0 and height > 0:
                    self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (width, height))
                else:
                    self.attack_effect_image = None # Ou um placeholder
                    # print(f"AVISO(AdagaFogo): Escala do efeito de ataque inválida para '{self.attack_effect_sprite_path}'. Efeito desabilitado.")

        # Lógica para carregar/recarregar o ícone da UI (herdado de Weapon.py)
        new_ui_icon_path = stats.get("ui_icon")
        if new_ui_icon_path and (new_ui_icon_path != self.ui_icon_path or self.ui_icon_surface is None):
            self.ui_icon_path = new_ui_icon_path
            self._load_ui_icon_sprite() # Chama o método da classe base (Weapon)

        # Lógica para carregar/recarregar a animação de ataque principal (da própria AdagaFogo)
        new_animation_paths = stats.get("animation_sprites")
        new_animation_display_scale = stats.get("animation_display_scale", 1.0) 
        
        if new_animation_paths: 
            # Recarrega se os paths mudaram OU se a escala da animação mudou OU se não há sprites carregados
            if (new_animation_paths != self.attack_animation_paths or
                new_animation_display_scale != self._last_loaded_anim_scale or # Compara com a última escala usada para carregar
                not self.attack_animation_sprites):
                
                self.attack_animation_paths = new_animation_paths
                self.animation_display_scale_factor = new_animation_display_scale # Atualiza o fator de escala usado pela arma
                self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)
                self._last_loaded_anim_scale = self.animation_display_scale_factor # Guarda a escala que foi usada para carregar
        
        self.attack_animation_speed = stats.get("animation_speed", 100)

        name_suffix = stats.get("name_suffix", "")
        self.name = f"{self._base_name} {name_suffix}".strip()

    def get_current_attack_animation_sprite(self):
        """Retorna o sprite atual da animação de ataque principal da arma."""
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None
