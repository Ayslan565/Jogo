# Jogo/Arquivos/Armas/FolhaCortanteProjectile.py
import pygame
import math
import os

class FolhaCortanteProjectile(pygame.sprite.Sprite):
    """
    Um projétil em forma de folha que viaja em linha reta.
    """
    def __init__(self, start_pos, target_enemy, speed, damage, lifetime=2.5, scale=1.0):
        super().__init__()
        
        self.speed = speed
        self.damage = damage
        self.lifetime = lifetime # Tempo de vida em segundos
        self.creation_time = pygame.time.get_ticks()

        try:
            # Constrói o caminho absoluto para a imagem do projétil
            base_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(base_dir))
            # Crie um sprite para o projétil neste caminho
            image_path = "Sprites/Armas/Armas Magicas/Cajado Da santa Natureza/Projetil.png" 
            full_path = os.path.join(project_root, image_path.replace("/", os.sep))
            
            original_image = pygame.image.load(full_path).convert_alpha()
            w = int(original_image.get_width() * scale)
            h = int(original_image.get_height() * scale)
            self.original_image = pygame.transform.scale(original_image, (w, h))
            self.image = self.original_image
        except (pygame.error, FileNotFoundError) as e:
            print(f"AVISO(FolhaCortante): Imagem '{image_path}' não encontrada ({e}). Usando placeholder.")
            self.original_image = pygame.Surface((25, 15), pygame.SRCALPHA)
            pygame.draw.ellipse(self.original_image, (40, 180, 90), self.original_image.get_rect()) # Elipse verde
            pygame.draw.line(self.original_image, (20, 100, 40), (12, 0), (12, 15), 1) # Veio central
            self.image = self.original_image

        self.rect = self.image.get_rect(center=start_pos)
        self.pos = pygame.math.Vector2(start_pos)
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Calcula a direção inicial e a mantém
        self._calculate_initial_velocity(target_enemy)

    def _calculate_initial_velocity(self, target_enemy):
        """Calcula a direção inicial do projétil e a fixa."""
        if target_enemy and hasattr(target_enemy, 'rect'):
            direction = pygame.math.Vector2(target_enemy.rect.center) - self.pos
            if direction.length() > 0:
                self.velocity = direction.normalize() * self.speed
                # Rotaciona a imagem original uma vez
                angle = self.velocity.angle_to(pygame.math.Vector2(1, 0))
                self.image = pygame.transform.rotate(self.original_image, -angle)
                self.rect = self.image.get_rect(center=self.rect.center)
        # Se não houver alvo, o projétil não terá velocidade e será removido pelo tempo de vida

    def update(self, enemies_group, dt_ms):
        """Move o projétil em sua direção fixa e verifica colisões."""
        # Verifica se o tempo de vida expirou
        if (pygame.time.get_ticks() - self.creation_time) > (self.lifetime * 1000):
            self.kill()
            return

        time_factor = dt_ms / (1000.0 / 60.0) if dt_ms > 0 else 1.0
        
        self.pos += self.velocity * time_factor
        self.rect.center = self.pos

        # Verifica colisão com inimigos
        hit_enemy = pygame.sprite.spritecollideany(self, enemies_group)
        if hit_enemy and hasattr(hit_enemy, 'receber_dano') and hit_enemy.esta_vivo():
            hit_enemy.receber_dano(self.damage, self.rect)
            self.kill()

        # Remove se sair muito da tela
        if not pygame.display.get_surface().get_rect().inflate(200, 200).colliderect(self.rect):
             self.kill()

    def draw(self, surface, camera_x, camera_y):
        """Desenha o projétil na tela com offset da câmera."""
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

