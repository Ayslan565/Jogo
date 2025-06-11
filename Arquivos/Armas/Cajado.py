import pygame
from weapon import Weapon

class Cajado(Weapon):
    """
    Classe base para todas as armas do tipo Cajado.
    Define o comportamento padrão de armas de longo alcance.
    """
    def __init__(self):
        super().__init__()
        self.last_shot = pygame.time.get_ticks()
        self.cooldown = 500  # Cooldown padrão, pode ser sobrescrito pelas subclasses
        self.is_ranged = True # Identificador para armas de longo alcance

    def can_attack(self):
        """Verifica se a arma pode atacar com base no tempo de recarga."""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot >= self.cooldown

    def attack(self, player, mouse_pos):
        """
        Método de ataque que deve ser implementado pelas subclasses.
        Deve retornar uma instância de um projétil.
        """
        raise NotImplementedError("A subclasse do Cajado deve implementar o método de ataque.")

    def update_weapon(self, player_rect, direction):
        """Atualiza a posição e a rotação da arma em relação ao jogador."""
        # Coloca a arma no centro do jogador
        self.rect.center = player_rect.center

        # Lógica para girar a arma com base na direção do jogador (opcional)
        if direction == 'up':
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif direction == 'down':
            self.image = pygame.transform.rotate(self.original_image, -90)
        elif direction == 'left':
            self.image = pygame.transform.flip(self.original_image, True, False)
        elif direction == 'right':
            self.image = self.original_image.copy()

