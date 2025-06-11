import pygame
import math
import os

class Projectile(pygame.sprite.Sprite):
    """
    Classe base para projéteis de armas.
    Lida com movimento, rotação, carregamento de imagem e remoção automática.
    """
    def _get_project_root(self):
        """ Retorna o diretório raiz do projeto (ex: a pasta 'Jogo'). """
        # Sobe na árvore de diretórios a partir deste arquivo até encontrar a raiz.
        # Jogo/Arquivos/Armas/projectile_weapon.py -> Jogo/
        try:
            current_path = os.path.abspath(__file__)
            # Sobe 3 níveis: Armas -> Arquivos -> Jogo
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
            return project_root
        except Exception:
            # Fallback caso __file__ não esteja disponível
            return os.getcwd()

    def __init__(self, x, y, target_x, target_y, speed, damage, image_path_from_root, scale=1.0, angle_offset=0):
        """
        Inicializa o projétil.
        Args:
            image_path_from_root (str): Caminho para a imagem RELATIVO à pasta raiz do projeto (ex: "Sprites/imagem.png").
        """
        super().__init__()
        
        # --- LÓGICA DE CARREGAMENTO DE IMAGEM MELHORADA ---
        full_image_path = ""
        try:
            project_root = self._get_project_root()
            # Constrói o caminho absoluto da imagem
            full_image_path = os.path.join(project_root, image_path_from_root.replace("/", os.sep))
            
            self.original_image = pygame.image.load(full_image_path).convert_alpha()
        except (pygame.error, FileNotFoundError) as e:
            print(f"ERRO: Não foi possível carregar a imagem do projétil: {full_image_path}")
            # Cria um placeholder visual para o projétil em caso de erro
            self.original_image = pygame.Surface((15, 15), pygame.SRCALPHA)
            self.original_image.fill((255, 0, 255)) # Cor magenta para fácil identificação do erro
        
        # O resto do código permanece o mesmo...
        width = int(self.original_image.get_width() * scale)
        height = int(self.original_image.get_height() * scale)
        if width > 0 and height > 0:
            self.original_image = pygame.transform.scale(self.original_image, (width, height))
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = speed
        self.damage = damage
        self.x = float(x)
        self.y = float(y)

        angle = math.atan2(target_y - y, target_x - x)
        self.vel_x = math.cos(angle) * self.speed
        self.vel_y = math.sin(angle) * self.speed
        
        degrees = math.degrees(angle)
        self.image = pygame.transform.rotate(self.original_image, -degrees + angle_offset)
        self.rect = self.image.get_rect(center=self.rect.center)


    def update(self):
        """
        Atualiza a posição do projétil e verifica se ele saiu da tela.
        """
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()