import pygame
import math
import os

class AmetistaProjectile(pygame.sprite.Sprite):
    """
    Projétil de Ametista que persegue um alvo.
    """
    def __init__(self, start_pos, target_enemy, speed=250, damage=25, lifetime=4.0):
        super().__init__()
        
        self.target = target_enemy
        self.speed = speed
        self.damage = damage
        self.lifetime = lifetime * 1000  # Convertido para milissegundos
        self.creation_time = pygame.time.get_ticks()

        # Tenta carregar a imagem do projétil ou cria um placeholder
        try:
            # Caminho relativo à raiz do projeto
            image_path = "Sprites/Armas/Armas Magicas/Cajado da Fixacao Ametista/Projetil.png"
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            full_path = os.path.join(project_root, image_path.replace("/", os.sep))
            
            if not os.path.exists(full_path):
                raise FileNotFoundError
            
            self.original_image = pygame.image.load(full_path).convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (30, 30))
        except (pygame.error, FileNotFoundError):
            self.original_image = pygame.Surface((18, 18), pygame.SRCALPHA)
            pygame.draw.circle(self.original_image, (180, 50, 255), (9, 9), 9)
            pygame.draw.circle(self.original_image, (255, 220, 255), (9, 9), 5)
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=start_pos)
        self.pos = pygame.math.Vector2(start_pos)

    def update(self):
        """
        Move o projétil em direção ao alvo e verifica seu tempo de vida.
        """
        if (pygame.time.get_ticks() - self.creation_time) > self.lifetime or not self.target.esta_vivo():
            self.kill()
            return

        direction = pygame.math.Vector2(self.target.rect.center) - self.pos
        if direction.length() > 0:
            direction.normalize_ip()
            self.pos += direction * self.speed * (1/60.0) # Assume 60 FPS
            self.rect.center = self.pos

    def draw(self, surface, camera_x, camera_y):
        """
        Desenha o projétil na tela, ajustado pela câmera.
        """
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))