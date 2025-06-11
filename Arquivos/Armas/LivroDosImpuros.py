import pygame
from .Cajado import Cajado
from CaveiraImpuraProjectile import CaveiraImpuraProjectile
from .weapon import Weapon

class LivroDosImpuros(Cajado):
    """
    O Livro dos Impuros, uma arma mágica que dispara projéteis de caveira.
    """
    def __init__(self):
        super().__init__()
        try:
            self.original_image = pygame.image.load('Jogo/Sprites/Armas/LivroImpuro/livro.png').convert_alpha()
        except pygame.error as e:
            print(f"Não foi possível carregar a imagem do Livro dos Impuros: {e}")
            self.original_image = pygame.Surface((35, 35), pygame.SRCALPHA) # Imagem placeholder
            self.original_image.fill((100, 20, 100))

        self.original_image = pygame.transform.scale(self.original_image, (35, 35))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        
        self.name = "Livro dos Impuros"
        self.attack_speed = 1.0
        self.cooldown = 1000 / self.attack_speed
        self.last_shot = pygame.time.get_ticks() - self.cooldown # Permite atirar imediatamente

    def attack(self, player, mouse_pos):
        """Cria e retorna um projétil de caveira se o cooldown permitir."""
        if self.can_attack():
            self.last_shot = pygame.time.get_ticks()
            return CaveiraImpuraProjectile(player.rect.centerx, player.rect.centery, mouse_pos[0], mouse_pos[1])
        return None

