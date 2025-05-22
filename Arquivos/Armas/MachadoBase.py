from .weapon import * # Importa a classe base Weapon do mesmo pacote
import pygame

class MachadoBase(Weapon):
    def __init__(self, name="Machado Base", damage=10.0, attack_range=60, cooldown=0.8, level=1.0):
        # Reduzimos o dano base para machados aqui, se desejar
        super().__init__(name, damage * 0.8, attack_range, cooldown, level) # Exemplo: 20% menos dano que armas padrão
        self.attack_type = "vertical" # Novo atributo para indicar tipo de ataque

    def get_attack_hitbox(self, player_rect, player_direction, attack_hitbox_size):
        """
        Retorna o hitbox do ataque para um ataque vertical.
        Este método será chamado pelo jogador para determinar a área de acerto.
        """
        hitbox_width, hitbox_height = attack_hitbox_size
        
        # O hitbox vertical pode ser mais alto e mais estreito,
        # ou apenas posicionado de forma diferente para simular o "machado para baixo".
        # Exemplo: um hitbox que se estende mais acima/abaixo do jogador.
        # Ajuste esses valores conforme a animação e o alcance visual do seu machado.
        
        # Para um ataque vertical, o hitbox pode se estender mais na altura do que na largura.
        # Vamos assumir que ele foca na frente do jogador, mas cobrindo uma área vertical maior.
        
        attack_hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height * 1.5) # Mais alto
        
        if player_direction == "right":
            # À direita do jogador, ligeiramente abaixo ou cobrindo o corpo
            attack_hitbox.centerx = player_rect.centerx + self.attack_range / 2
            attack_hitbox.centery = player_rect.centery + player_rect.height / 4 # Ligeiramente abaixo do centro
        elif player_direction == "left":
            # À esquerda do jogador, ligeiramente abaixo ou cobrindo o corpo
            attack_hitbox.centerx = player_rect.centerx - self.attack_range / 2
            attack_hitbox.centery = player_rect.centery + player_rect.height / 4
            
        return attack_hitbox

    # Você pode adicionar mais lógica específica para machados aqui, se necessário