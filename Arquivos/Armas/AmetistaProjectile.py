import pygame
import math

class AmetistaProjectile(pygame.sprite.Sprite):
    """
    Projétil de Ametista que persegue um alvo, renderizado em estilo pixel art 64x64.
    """
    def __init__(self, start_pos, target_enemy, speed=250, damage=25, lifetime=4.0):
        super().__init__()
        
        self.target = target_enemy
        self.speed = speed
        self.damage = damage
        self.lifetime = lifetime * 1000  # Convertido para milissegundos
        self.creation_time = pygame.time.get_ticks()

        # --- Bloco de Geração de Pixel Art (64x64) ---
        tamanho = 64
        centro = tamanho // 2
        
        # Cria a superfície transparente de 64x64 pixels
        self.original_image = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        
        # Paleta de cores roxas para o estilo pixel art
        cor_borda = (87, 15, 157)       # Roxo escuro para a aura externa
        cor_principal = (148, 0, 211)   # Roxo vibrante principal
        cor_brilho = (199, 81, 255)      # Roxo claro para o brilho interno
        cor_nucleo = (255, 240, 255)     # Quase branco para o núcleo de energia

        # Desenha as camadas do orbe, do maior para o menor
        # Aura externa
        pygame.draw.circle(self.original_image, cor_borda, (centro, centro), 28)
        # Corpo principal do orbe
        pygame.draw.circle(self.original_image, cor_principal, (centro, centro), 24)
        # Brilho interno
        pygame.draw.circle(self.original_image, cor_brilho, (centro, centro), 16)
        # Núcleo de energia
        pygame.draw.circle(self.original_image, cor_nucleo, (centro, centro), 8)
        
        # Adiciona um pequeno brilho/reflexo em pixel art
        self.original_image.set_at((centro - 6, centro - 6), cor_nucleo)
        self.original_image.set_at((centro - 7, centro - 6), cor_brilho)
        self.original_image.set_at((centro - 6, centro - 7), cor_brilho)
        # --- Fim do Bloco de Geração ---

        self.image = self.original_image
        self.rect = self.image.get_rect(center=start_pos)
        self.pos = pygame.math.Vector2(start_pos)

    def update(self):
        """
        Move o projétil em direção ao alvo e verifica seu tempo de vida.
        """
        if not self.target or not self.target.esta_vivo() or (pygame.time.get_ticks() - self.creation_time) > self.lifetime:
            self.kill()
            return

        direction = pygame.math.Vector2(self.target.rect.center) - self.pos
        if direction.length() > 0:
            direction.normalize_ip()
            self.pos += direction * self.speed * (1/60.0) 
            self.rect.center = self.pos

    def draw(self, surface, camera_x, camera_y):
        """
        Desenha o projétil na tela, ajustado pela câmera.
        """
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))