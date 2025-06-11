# Jogo/Arquivos/Armas/CaveiraImpuraProjectile.py
import pygame
import math
import os

class CaveiraImpuraProjectile(pygame.sprite.Sprite):
    """
    Um projétil em forma de caveira profana que viaja com um leve movimento ondulado.
    """
    def __init__(self, start_pos, target_enemy, speed, damage, lifetime=3.0, scale=1.0):
        super().__init__()
        
        self.speed = speed
        self.damage = damage
        self.lifetime = lifetime
        self.creation_time = pygame.time.get_ticks()

        try:
            # Tenta carregar o sprite do projétil. Crie a imagem neste caminho.
            base_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(base_dir))
            image_path = "Sprites/Armas/Armas Magicas/Livro dos impuros/Projetil.png" 
            full_path = os.path.join(project_root, image_path.replace("/", os.sep))
            
            original_image = pygame.image.load(full_path).convert_alpha()
            w = int(original_image.get_width() * scale)
            h = int(original_image.get_height() * scale)
            self.original_image = pygame.transform.scale(original_image, (w, h))
            self.image = self.original_image
        except (pygame.error, FileNotFoundError) as e:
            print(f"AVISO(CaveiraImpura): Imagem '{image_path}' não encontrada ({e}). Usando placeholder.")
            self.original_image = pygame.Surface((22, 22), pygame.SRCALPHA)
            pygame.draw.circle(self.original_image, (100, 20, 140), (11, 11), 11) # Roxo escuro
            pygame.draw.circle(self.original_image, (200, 150, 255), (11, 11), 6)  # Brilho lilás
            self.image = self.original_image

        self.rect = self.image.get_rect(center=start_pos)
        self.pos = pygame.math.Vector2(start_pos)
        self.velocity = pygame.math.Vector2(0, 0)

        # Movimento ondulado
        self.wave_frequency = 0.05
        self.wave_amplitude = 4
        self.angle = 0
        
        self._calculate_initial_velocity(target_enemy)

    def _calculate_initial_velocity(self, target_enemy):
        """Calcula a direção inicial e a fixa."""
        if target_enemy and hasattr(target_enemy, 'rect'):
            direction = pygame.math.Vector2(target_enemy.rect.center) - self.pos
            if direction.length() > 0:
                self.velocity = direction.normalize() * self.speed
        # O projétil continuará em linha reta mesmo que não tenha um alvo inicial

    def update(self, enemies_group, dt_ms):
        """Move o projétil com ondulação e verifica colisões."""
        if (pygame.time.get_ticks() - self.creation_time) > (self.lifetime * 1000):
            self.kill()
            return

        time_factor = dt_ms / (1000.0 / 60.0) if dt_ms > 0 else 1.0
        
        # Movimento base em linha reta
        self.pos += self.velocity * time_factor
        
        # Adiciona o movimento de ondulação perpendicular à direção do projétil
        self.angle += self.wave_frequency * time_factor
        perpendicular_vector = self.velocity.rotate(90).normalize()
        offset = perpendicular_vector * math.sin(self.angle) * self.wave_amplitude
        
        final_pos = self.pos + offset
        self.rect.center = final_pos

        # Verifica colisão
        hit_enemy = pygame.sprite.spritecollideany(self, enemies_group)
        if hit_enemy and hasattr(hit_enemy, 'receber_dano') and hit_enemy.esta_vivo():
            hit_enemy.receber_dano(self.damage, self.rect)
            self.kill()

        if not pygame.display.get_surface().get_rect().inflate(200, 200).colliderect(self.rect):
             self.kill()

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
