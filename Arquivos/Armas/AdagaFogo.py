import pygame
import os
# Assume que weapon.py está no mesmo diretório 'Armas' ou em um local acessível via Python path
from .weapon import Weapon

class AdagaFogo(Weapon):
    """
    Representa a Adaga de Fogo, uma arma ágil com níveis de evolução
    e sua própria animação de ataque.
    """
    def __init__(self):
        self._base_name = "Adaga do Fogo Contudente"
        self.level = 1.0 # Nível inicial

        # --- As estatísticas de cada nível são definidas aqui para que possam ser acedidas durante a inicialização.
        self._stats_by_level = {
            1.0: {
                "damage": 24.0, "range": 40, "cooldown": 0.6, "name_suffix": "",
                "hitbox_dim": (8, 8), #
                "hitbox_off": (100, 10), #(Distancia do Corpo do Jogador no Eixo X , Distancia do Corpo do Jogador no Eixo Y)
                # CORRIGIDO: Caminho aponta para a pasta 'Sprites'
                "effect_sprite_base": "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Efeitos//ImpactoFogoNv1.png",
                "effect_scale_base": 0.8,
                # CORRIGIDO: Caminhos apontam para a pasta 'Sprites'
                "animation_sprites": [
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT0-base0.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT1-base1.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT2-base2.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT3-base3.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT4-base4.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT5-base5.png"
                ],
                "animation_speed": 80,
                "animation_display_scale": 3.0,
                # CORRIGIDO: Caminho aponta para a pasta 'Sprites'
                "ui_icon": "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Adaga E-1.png"
            },
            2.0: {
                "damage": 30.0, "range": 90.0, "cooldown": 0.55, "name_suffix": "Afiada",
                "hitbox_dim": (65, 65), "hitbox_off": (12, 0),
                "effect_sprite_base": "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Efeitos\\ImpactoFogoNv1.png",
                "effect_scale_base": 0.85,
                "animation_sprites": [
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT0-base0.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT1-base1.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT1-base2.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT1-base3.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT1-base4.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT1-base5.png"

                ],
                "animation_speed": 70,
                "animation_display_scale": 3.05,
                "ui_icon": "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Adaga E-2.png"
            },
            3.0: {
                "damage": 36.0, "range": 100.0, "cooldown": 0.5, "name_suffix": "Incandescente",
                "hitbox_dim": (70, 70), "hitbox_off": (15, 0),
                "effect_sprite_base": "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Efeitos\\ImpactoFogoNv2.png",
                "effect_scale_base": 0.9,
                # CORRIGIDO: Caminhos apontam para a pasta 'Sprites' e typo corrigido
                "animation_sprites": [
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT0-base0.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT1-base1.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT1-base2.png",
                    "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Ataque//AT1//AT1-base3.png"
                ],
                "animation_speed": 65,
                "animation_display_scale": 3.1,
                "ui_icon": "Sprites//Armas//Espadas//Adaga do Fogo Contudente//Adaga E-3.png.png"
            }
        }

        # Pega os stats iniciais para passar para a classe mãe
        initial_stats_for_super = self._get_stats_for_level_internal(self.level, for_super_init=True)

        super().__init__(
            name=self._base_name,
            damage=initial_stats_for_super.get("damage", 15.0),
            attack_range=initial_stats_for_super.get("range", 85.0),
            cooldown=initial_stats_for_super.get("cooldown", 0.6),
            hitbox_dimensions=initial_stats_for_super.get("hitbox_dim", (60, 60)),
            hitbox_offset=initial_stats_for_super.get("hitbox_off", (10, 0)),
            description="Uma adaga que queima com o calor de uma forja.",
            rarity="Comum",
            weapon_type="Adaga",
            element="Fogo",
            attack_effect_sprite_path=initial_stats_for_super.get("effect_sprite_base", None),
            attack_effect_scale=initial_stats_for_super.get("effect_scale_base", 1.0),
            ui_icon_path=initial_stats_for_super.get("ui_icon", "Sprites\\Armas\\Espadas\\Adaga do Fogo Contudente\\Icone_AFC1.png")
        )

        self.attack_animation_sprites = []
        self.attack_animation_paths = []
        self.attack_animation_speed = 100
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = 1.0

        self._apply_level_stats()

    def _get_stats_for_level_internal(self, level_to_check, for_super_init=False):
        if for_super_init:
            return self._stats_by_level.get(level_to_check, self._stats_by_level.get(1.0, {}))

        if level_to_check in self._stats_by_level:
            return self._stats_by_level[level_to_check]
        else:
            first_level_key = next(iter(self._stats_by_level))
            return self._stats_by_level[first_level_key]

    def _load_weapon_attack_animation_sprites(self, caminhos, escala_animacao=1.0):
        sprites_carregados = []
        
        # A lógica de usar caminhos relativos está mantida e correta.
        if not caminhos:
            self.attack_animation_sprites = []
            return


        for path_relativo in caminhos:
            path_corrigido = path_relativo.replace("\\", os.sep).replace("//", os.sep)
            full_path = path_corrigido
            

            try:
                if os.path.exists(full_path):

                    imagem_original = pygame.image.load(full_path).convert_alpha()
                    novo_w, novo_h = 100, 100
                    imagem = pygame.transform.smoothscale(imagem_original, (novo_w, novo_h))
                    sprites_carregados.append(imagem)
                else:
                    placeholder = pygame.Surface((100, 100), pygame.SRCALPHA); placeholder.fill((255,140,0,100))
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                placeholder = pygame.Surface((100, 100), pygame.SRCALPHA); placeholder.fill((255,0,0,150))
                sprites_carregados.append(placeholder)
        
        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0

    # --- MÉTODOS DE ANIMAÇÃO ADICIONADOS ---
    def start_attack_animation(self):
        """Reinicia a animação de ataque para o primeiro frame."""
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = pygame.time.get_ticks()

    def update_animation(self, current_ticks):
        """Avança o frame da animação de ataque com base na velocidade da animação."""
        if not self.attack_animation_sprites:
            return  # Não faz nada se não houver sprites

        # Verifica se já passou tempo suficiente para atualizar para o próximo frame
        if current_ticks - self.last_attack_animation_update > self.attack_animation_speed:
            self.last_attack_animation_update = current_ticks
            
            # Avança para o próximo frame, fazendo um loop ao chegar no final
            # A duração do ataque é controlada em player.py, então o loop aqui é seguro.
            if len(self.attack_animation_sprites) > 0:
                self.current_attack_animation_frame = (self.current_attack_animation_frame + 1) % len(self.attack_animation_sprites)
    # --- FIM DOS MÉTODOS ADICIONADOS ---

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()


    def _apply_level_stats(self):
        stats = self._get_stats_for_level_internal(self.level)
        if not stats:
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
