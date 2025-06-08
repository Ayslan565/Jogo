# Jogo/Arquivos/Armas/AmetistaProjectile.py
import pygame
import math
import os

class AmetistaProjectile(pygame.sprite.Sprite):
    """
    Um projétil de ametista que persegue o alvo.
    """
    def __init__(self, start_pos, target_enemy, speed, damage, lifetime=3.0, scale=1.0):
        super().__init__()
        
        self.target = target_enemy
        self.speed = speed
        self.damage = damage
        self.lifetime = lifetime # Tempo de vida em segundos
        self.creation_time = pygame.time.get_ticks()

        try:
            # Constrói o caminho absoluto para a imagem do projétil
            base_dir = os.path.dirname(os.path.abspath(__file__)) # .../Jogo/Arquivos/Armas
            project_root = os.path.dirname(os.path.dirname(base_dir)) # .../Jogo/
            image_path = "Sprites/Armas/Cajados/Ametista/Projetil.png" 
            full_path = os.path.join(project_root, image_path.replace("/", os.sep))
            
            original_image = pygame.image.load(full_path).convert_alpha()
            w = int(original_image.get_width() * scale)
            h = int(original_image.get_height() * scale)
            self.original_image = pygame.transform.scale(original_image, (w, h))
            self.image = self.original_image
        except (pygame.error, FileNotFoundError) as e:
            # --- CÓDIGO DO PLACEHOLDER ---
            # Este bloco é executado se a imagem não for encontrada, criando um placeholder visual.
            print(f"AVISO(AmetistaProjectile): Imagem '{image_path}' não encontrada ({e}). Usando placeholder.")
            self.original_image = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(self.original_image, (150, 80, 200), (10, 10), 10) # Roxo ametista
            pygame.draw.circle(self.original_image, (220, 180, 255), (10, 10), 6) # Brilho lilás
            self.image = self.original_image

        self.rect = self.image.get_rect(center=start_pos)
        self.pos = pygame.math.Vector2(start_pos) 
        self.velocity = pygame.math.Vector2(0, 0)
        self._calculate_homing_velocity()

    def _calculate_homing_velocity(self):
        """Calcula e atualiza a velocidade do projétil para seguir o alvo."""
        if self.target and hasattr(self.target, 'rect') and hasattr(self.target, 'esta_vivo') and self.target.esta_vivo():
            direction = pygame.math.Vector2(self.target.rect.center) - self.pos
            if direction.length() > 0:
                self.velocity = direction.normalize() * self.speed
        # Se o alvo morrer ou não existir, o projétil continua em sua última direção.

    def update(self, enemies_group, dt_ms):
        """
        Move o projétil, re-calcula a rota (homing) e verifica colisões.
        """
        if (pygame.time.get_ticks() - self.creation_time) > (self.lifetime * 1000):
            self.kill()
            return

        # Re-calcula a direção para seguir o alvo (efeito teleguiado)
        self._calculate_homing_velocity()

        time_factor = dt_ms / (1000.0 / 60.0) if dt_ms > 0 else 1.0
        
        self.pos += self.velocity * time_factor
        self.rect.center = self.pos

        angle = self.velocity.angle_to(pygame.math.Vector2(1, 0))
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        hit_enemy = pygame.sprite.spritecollideany(self, enemies_group)
        if hit_enemy and hasattr(hit_enemy, 'receber_dano') and hasattr(hit_enemy, 'esta_vivo') and hit_enemy.esta_vivo():
            hit_enemy.receber_dano(self.damage, self.rect)
            self.kill()

        if not pygame.display.get_surface().get_rect().inflate(200, 200).colliderect(self.rect):
             self.kill()

    def draw(self, surface, camera_x, camera_y):
        """Desenha o projétil na tela com offset da câmera."""
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))