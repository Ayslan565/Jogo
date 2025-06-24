import pygame
import os

class Weapon:
    """
    Classe base para todas as armas no jogo.
    Define atributos comuns como nome, dano, alcance, cooldown,
    dimensões/offset da hitbox de ataque, e sprites de efeito/UI.
    """
    def __init__(self, name: str, damage: float, attack_range: float, cooldown: float,
                 hitbox_dimensions: tuple[float, float] = (50, 50),
                 hitbox_offset: tuple[float, float] = (0, 0),
                 description: str = "Uma arma genérica.",
                 rarity: str = "Comum",
                 weapon_type: str = "Arma",  # Ex: "Espada", "Adaga", "Machado"
                 element: str | None = None,  # Ex: "Fogo", "Gelo"
                 # Sprite de efeito visual secundário (ex: rastro, brilho)
                 attack_effect_sprite_path: str | None = None,
                 attack_effect_scale: float = 1.0,
                 # Ícone para interfaces como a roda de armas
                 ui_icon_path: str | None = None,
                 # Sprites para a animação principal do golpe da arma
                 animation_sprites_paths: list[str] | None = None,  # Lista de caminhos
                 animation_speed: int = 100,  # ms por frame
                 animation_display_scale: float = 1.0  # Escala para os sprites da animação
                 ):

        self.name = name
        self._base_name = name  # Guardar o nome base para sufixos de nível
        self.damage = damage
        self.attack_range = attack_range
        self.cooldown = cooldown

        self.hitbox_width = hitbox_dimensions[0]
        self.hitbox_height = hitbox_dimensions[1]
        self.hitbox_offset_x = hitbox_offset[0]
        self.hitbox_offset_y = hitbox_offset[1]

        self.description = description
        self.rarity = rarity
        self.weapon_type = weapon_type
        self.element = element
        self.level = 1.0

        # Para o efeito visual secundário (opcional)
        self.attack_effect_sprite_path = attack_effect_sprite_path
        self.attack_effect_image = None
        self.attack_effect_original_image = None
        self.attack_effect_scale = attack_effect_scale

        self.ui_icon_path = ui_icon_path

        # Atributos para animação de ataque principal da arma
        self.attack_animation_paths = animation_sprites_paths if animation_sprites_paths else []
        self.attack_animation_sprites = []  # Lista de Surfaces carregadas
        self.attack_animation_speed = animation_speed
        self.current_attack_animation_frame = 0
        self.last_attack_animation_update = 0
        self.animation_display_scale_factor = animation_display_scale
        self._last_loaded_anim_scale = animation_display_scale  # Para verificar se precisa recarregar

        if self.attack_effect_sprite_path:
            self._load_attack_effect_sprite()  # Carrega o efeito secundário

        if self.attack_animation_paths:
            self._load_weapon_attack_animation_sprites(self.attack_animation_paths, self.animation_display_scale_factor)

    def _get_project_root(self):
        """
        Retorna o diretório raiz do projeto (assumindo estrutura Jogo/Arquivos/Armas).
        Esta função sobe três níveis na árvore de diretórios a partir deste arquivo.
        Ex: .../Jogo/Arquivos/Armas/weapon.py -> .../Jogo/
        """
        try:
            base_dir_weapon = os.path.dirname(os.path.abspath(__file__))  # .../Jogo/Arquivos/Armas
            base_dir_arquivos = os.path.dirname(base_dir_weapon)       # .../Jogo/Arquivos
            project_root = os.path.dirname(base_dir_arquivos)          # .../Jogo/
            return project_root
        except Exception:
            # Fallback para caso __file__ não esteja disponível
            return os.getcwd()

    def _load_attack_effect_sprite(self):
        """Carrega e prepara o sprite de efeito de ataque secundário (da classe base)."""
        if not self.attack_effect_sprite_path: return

        project_root = self._get_project_root()
        full_path = os.path.join(project_root, self.attack_effect_sprite_path.replace("\\", os.sep))

        if os.path.exists(full_path):
                self.attack_effect_original_image = pygame.image.load(full_path).convert_alpha()
                width = int(self.attack_effect_original_image.get_width() * self.attack_effect_scale)
                height = int(self.attack_effect_original_image.get_height() * self.attack_effect_scale)
                if width > 0 and height > 0:
                    self.attack_effect_image = pygame.transform.smoothscale(self.attack_effect_original_image, (width, height))
                else:
                    self._create_placeholder_effect("Dimensões inválidas para efeito base após escala")

                self._create_placeholder_effect("Arquivo de efeito base não encontrado")

    def _create_placeholder_effect(self, reason=""):
        """Cria um placeholder para o efeito de ataque secundário."""
        #print(f"DEBUG(Weapon): Usando placeholder para efeito de ataque base de {self.name}. Razão: {reason}")
        # Pode ser None ou um pequeno sprite transparente para não desenhar nada se falhar
        self.attack_effect_image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.attack_effect_image.fill((0, 0, 0, 0))

    def _load_weapon_attack_animation_sprites(self, caminhos, escala_animacao=1.0):
        """Carrega os sprites para a animação de ataque principal desta arma."""
        sprites_carregados = []
        project_root = self._get_project_root()

        for path_relativo in caminhos:
            full_path = os.path.join(project_root, path_relativo.replace("\\", os.sep))
            try:
                if os.path.exists(full_path):
                    imagem_original = pygame.image.load(full_path).convert_alpha()
                    novo_w = int(imagem_original.get_width() * escala_animacao)
                    novo_h = int(imagem_original.get_height() * escala_animacao)
                    if novo_w > 0 and novo_h > 0:
                        imagem = pygame.transform.smoothscale(imagem_original, (novo_w, novo_h))
                        sprites_carregados.append(imagem)
                    else:
                        #print(f"DEBUG({self.__class__.__name__}): Dimensões inválidas para sprite de animação {full_path}. Usando placeholder.")
                        placeholder = pygame.Surface((int(50 * escala_animacao) if escala_animacao > 0 else 50, int(50 * escala_animacao) if escala_animacao > 0 else 50), pygame.SRCALPHA); placeholder.fill((255, 0, 255, 100))
                        sprites_carregados.append(placeholder)
                else:
                    #print(f"DEBUG({self.__class__.__name__}): Sprite de animação de ataque não encontrado: {full_path}")
                    placeholder = pygame.Surface((int(50 * escala_animacao) if escala_animacao > 0 else 50, int(50 * escala_animacao) if escala_animacao > 0 else 50), pygame.SRCALPHA); placeholder.fill((255, 0, 255, 100))
                    sprites_carregados.append(placeholder)
            except pygame.error as e:
                #print(f"DEBUG({self.__class__.__name__}): Erro ao carregar sprite de animação '{full_path}': {e}")
                placeholder = pygame.Surface((int(50 * escala_animacao) if escala_animacao > 0 else 50, int(50 * escala_animacao) if escala_animacao > 0 else 50), pygame.SRCALPHA); placeholder.fill((255, 0, 255, 100))
                sprites_carregados.append(placeholder)

        self.attack_animation_sprites = sprites_carregados
        self.current_attack_animation_frame = 0
        self._last_loaded_anim_scale = escala_animacao  # Guarda a escala usada para carregar


    def __str__(self):
        return (f"{self.name} (Nv: {self.level}, Dano: {self.damage}, "
                f"Alcance: {self.attack_range}, Cooldown: {self.cooldown}s, "
                f"Hitbox: {self.hitbox_width}x{self.hitbox_height}, "
                f"Offset: ({self.hitbox_offset_x},{self.hitbox_offset_y}))")

    def evolve(self, target_level: float):
        """
        Método placeholder para evolução. Classes filhas devem sobrescrever.
        Normalmente, chamaria _apply_level_stats após mudar self.level.
        """
        self.level = target_level
        self._apply_level_stats()  # Garante que os stats sejam aplicados após a mudança de nível

    def _apply_level_stats(self):
        """
        Método placeholder para aplicar estatísticas baseadas no nível.
        Classes filhas DEVEM sobrescrever isso para definir como os stats,
        hitbox, sprites de animação, etc., mudam com self.level.
        """
        #print(f"DEBUG(Weapon): _apply_level_stats base chamado para {self.name} no nível {self.level}. Nenhuma alteração feita pela classe base.")
        pass  # Deve ser implementado por classes filhas

    def get_current_attack_animation_sprite(self):
        """Retorna o sprite atual da animação de ataque principal da arma."""
        if self.attack_animation_sprites and 0 <= self.current_attack_animation_frame < len(self.attack_animation_sprites):
            return self.attack_animation_sprites[self.current_attack_animation_frame]
        return None  # Ou um sprite placeholder se preferir

    # --- NOVO MÉTODO ADICIONADO ---
    def _load_from_individual_configs(self, configs):
        """
        Carrega sprites de animação a partir de uma lista de configurações individuais.
        Cada configuração é um dicionário com 'path' e 'scale'.
        """
        #print(f"DEBUG({self.__class__.__name__}): Carregando sprites com configurações individuais.")
        sprites_carregados = []
        project_root = self._get_project_root()

        for config in configs:
            path_relativo = config.get("path")
            escala_individual = config.get("scale", 1.0) # Usa 1.0 como padrão se 'scale' não for encontrado

            if not path_relativo:
                continue
            
            full_path = os.path.join(project_root, path_relativo.replace("\\", os.sep).replace("/", os.sep))

            if os.path.exists(full_path):
                    imagem_original = pygame.image.load(full_path).convert_alpha()
                    novo_w = int(imagem_original.get_width() * escala_individual)
                    novo_h = int(imagem_original.get_height() * escala_individual)
                    if novo_w > 0 and novo_h > 0:
                        imagem = pygame.transform.smoothscale(imagem_original, (novo_w, novo_h))
                        sprites_carregados.append(imagem)
                    else:
                        #print(f"WARN({self.__class__.__name__}): Dimensões inválidas para sprite '{full_path}' após escala.")
                            self.attack_animation_sprites = sprites_carregados
                            self.current_attack_animation_frame = 0
