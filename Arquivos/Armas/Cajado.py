# Jogo/Arquivos/Armas/Projectile.py
import pygame
import math
import os

class Projectile(pygame.sprite.Sprite):
    """
    Classe genérica para projéteis disparados por armas de longo alcance.
    """
    def __init__(self, start_pos, target_enemy, speed, damage, image_path, scale=1.0):
        super().__init__()
        
        self.target = target_enemy
        self.speed = speed
        self.damage = damage

        try:
            # Constrói o caminho absoluto para a imagem do projétil
            base_dir = os.path.dirname(os.path.abspath(__file__)) # .../Jogo/Arquivos/Armas
            project_root = os.path.dirname(os.path.dirname(base_dir)) # .../Jogo/
            full_path = os.path.join(project_root, image_path.replace("/", os.sep))
            
            original_image = pygame.image.load(full_path).convert_alpha()
            w = int(original_image.get_width() * scale)
            h = int(original_image.get_height() * scale)
            self.image = pygame.transform.scale(original_image, (w, h))
        except (pygame.error, FileNotFoundError) as e:
            print(f"AVISO(Projectile): Imagem '{image_path}' não encontrada ({e}). Usando placeholder.")
            self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 255), (7, 7), 7)

        self.rect = self.image.get_rect(center=start_pos)
        self.pos = pygame.math.Vector2(start_pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self._calculate_initial_velocity()

    def _calculate_initial_velocity(self):
        """Calcula a direção inicial do projétil em direção ao alvo."""
        if self.target and hasattr(self.target, 'rect'):
            direction = pygame.math.Vector2(self.target.rect.center) - self.pos
            if direction.length() > 0:
                self.velocity = direction.normalize() * self.speed

    def update(self, enemies_group, dt_ms):
        """
        Move o projétil e verifica colisões.
        Args:
            enemies_group (pygame.sprite.Group): Grupo de inimigos para checar colisão.
            dt_ms (float): Delta time em milissegundos para movimento consistente.
        """
        # Fator de tempo para movimento consistente independente do FPS
        time_factor = dt_ms / (1000.0 / 60.0) if dt_ms > 0 else 1.0
        
        # Move o projétil
        self.pos += self.velocity * time_factor
        self.rect.center = self.pos

        # Verifica colisão com inimigos
        hit_enemy = pygame.sprite.spritecollideany(self, enemies_group)
        if hit_enemy and hasattr(hit_enemy, 'receber_dano') and hit_enemy.esta_vivo():
            hit_enemy.receber_dano(self.damage)
            self.kill() # Remove o projétil após colidir

        # Remove o projétil se sair da tela (opcional, pode ser melhorado)
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
             self.kill()

    def draw(self, surface, camera_x, camera_y):
        """Desenha o projétil na tela com offset da câmera."""
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

