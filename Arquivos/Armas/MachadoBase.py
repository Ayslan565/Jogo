import pygame
import os
from .weapon import Weapon # Importa a classe Weapon do mesmo diretório

class MachadoBase(Weapon):
    """
    Classe base para todos os machados.
    Herda de Weapon e define o comportamento padrão para ataques de machado,
    como o tipo de ataque e o cálculo da hitbox.
    """
    def __init__(self, name: str, damage: float, attack_range: float, cooldown: float,
                 level: float = 1.0,
                 # Permite que classes filhas passem todos os outros parâmetros para a classe Weapon
                 **kwargs):

        # Define o tipo de arma padrão para todos os machados
        kwargs['weapon_type'] = kwargs.get('weapon_type', 'Machado')
        
        # Chama o inicializador da classe pai (Weapon) com todos os parâmetros.
        # As classes filhas (como MachadoBarbaro) podem passar todos os detalhes
        # através de **kwargs.
        super().__init__(
            name=name,
            damage=damage,
            attack_range=attack_range,
            cooldown=cooldown,
            **kwargs
        )
        
        self.level = level
        # Define o tipo de ataque específico para machados, que pode determinar
        # a forma como a animação ou a hitbox é calculada.
        self.attack_type = "vertical_swing"

    def get_attack_hitbox(self, player_rect: pygame.Rect, player_direction: str) -> pygame.Rect:
        """
        Calcula e retorna a hitbox para o ataque de machado.
        Este método cria uma hitbox em frente ao jogador, baseada na sua direção.

        Args:
            player_rect (pygame.Rect): O retângulo de posição do jogador.
            player_direction (str): A direção para a qual o jogador está virado ("left" ou "right").

        Returns:
            pygame.Rect: O retângulo da hitbox do ataque.
        """
        hitbox_x = 0
        
        # Posiciona a hitbox à direita ou à esquerda do jogador
        if player_direction == "right":
            # O offset X é aplicado a partir da borda direita do jogador
            hitbox_x = player_rect.right + self.hitbox_offset_x
        else:  # "left"
            # O offset X é aplicado a partir da borda esquerda, considerando a largura da hitbox
            hitbox_x = player_rect.left - self.hitbox_width - self.hitbox_offset_x

        # O offset Y alinha a hitbox verticalmente com o centro do jogador
        hitbox_y = player_rect.centery - (self.hitbox_height / 2) + self.hitbox_offset_y

        return pygame.Rect(hitbox_x, hitbox_y, self.hitbox_width, self.hitbox_height)

    def _apply_level_stats(self):
        """
        Método que deve ser sobrescrito por classes de machados específicas.
        É aqui que você define como os atributos do machado (dano, alcance, sprites, etc.)
        mudam a cada nível.
        """
        # Exemplo de como uma classe filha poderia implementar isso:
        # stats = self._stats_by_level.get(self.level)
        # if stats:
        #     self.damage = stats['damage']
        #     self.cooldown = stats['cooldown']
        #     # ... e assim por diante para outros atributos.
        print(f"DEBUG(MachadoBase): _apply_level_stats chamado para '{self.name}', mas não implementado na classe base.")
        pass

