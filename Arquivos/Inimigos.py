# Inimigos.py
import pygame
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()

class Inimigo(pygame.sprite.Sprite):
    """
    Classe base para inimigos no jogo.
    Herda de pygame.sprite.Sprite para facilitar o manuseio de grupos de sprites.
    Recebe uma Surface do Pygame já carregada.
    """
    def __init__(self, x, y, image_surface, velocidade=1):
        """
        Inicializa um novo objeto Inimigo com uma Surface de imagem.

        Args:
            x (int): A posição inicial x do inimigo.
            y (int): A posição inicial y do inimigo.
            image_surface (pygame.Surface): A Surface do Pygame já carregada para o sprite.
            velocidade (float): A velocidade de movimento do inimigo.
        """
        super().__init__() # Inicializa a classe base Sprite

        self.image = image_surface # Usa a Surface passada diretamente
        self.rect = self.image.get_rect(topleft=(x, y)) # Obtém o retângulo do sprite e define a posição inicial
        self.velocidade = velocidade # Define a velocidade de movimento base do inimigo

        # Atributos de combate comuns (podem ser sobrescritos nas classes derivadas)
        self.hp = 100 # Pontos de vida padrão
        self.is_attacking = False # Flag para indicar si o inimigo está atacando
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Retângulo para a hitbox de ataque (inicialmente vazio)
        self.hit_by_player_this_attack = False # Flag para controle de hit por ataque do jogador
        self.contact_damage = 5 # Dano por contato padrão
        self.contact_cooldown = 1000 # Cooldown de dano de contato padrão (em milissegundos)
        self.last_contact_time = pygame.time.get_ticks() # Tempo do último contato (em milissegundos)

    def mover_em_direcao(self, alvo_x, alvo_y):
        """
        Move o inimigo na direção de um ponto alvo.
        Este método deve ser chamado pelas classes derivadas em seus métodos update.

        Args:
            alvo_x (int): A coordenada x do ponto alvo.
            alvo_y (int): A coordenada y do ponto alvo.
        """
        # Só move si estiver vivo e tiver velocidade
        # Adiciona verificação para evitar movimento si a distância for muito pequena (evita tremer)
        if self.esta_vivo() and self.velocidade > 0:
            dx = alvo_x - self.rect.centerx # Diferença no eixo x
            dy = alvo_y - self.rect.centery # Diferença no eixo y
            distancia = math.hypot(dx, dy) # Calcula a distância usando a hipotenusa

            # Define uma pequena margem para evitar tremer quando muito perto
            if distancia > self.velocidade / 2: # Move apenas si a distância for maior que metade da velocidade
                # Normaliza o vetor direção para obter apenas a direção
                dx_norm = dx / distancia
                dy_norm = dy / distancia
                # Move o inimigo na direção do alvo pela velocidade definida
                self.rect.x += dx_norm * self.velocidade
                self.rect.y += dy_norm * self.velocidade
            else:
                 # Si a distância for menor ou igual à metade da velocidade, move diretamente para o alvo
                 self.rect.centerx = alvo_x
                 self.rect.centery = alvo_y


    def update(self, player):
        """
        Método placeholder para atualização do inimigo.
        As classes derivadas devem sobrescrever este método para implementar
        movimento, ataque, animação, etc. Deve receber o objeto player.
        """
        pass # Implementação real deve estar nas classes derivadas

    def desenhar(self, janela, camera_x, camera_y):
        """
        Desenha o inimigo na janela, aplicando o offset da câmera.

        Args:
            janela (pygame.Surface): A superfície onde desenhar.
            camera_x (int): O offset x da câmera.
            camera_y (int): O offset y da câmera.
        """
        # Desenha a imagem do inimigo na posição corrigida pela câmera
        janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

    def esta_vivo(self):
        """Retorna True se o inimigo estiver vivo."""
        return self.hp > 0 # Assume que o inimigo está vivo se HP > 0

    def receber_dano(self, dano):
        """
        Método placeholder para receber dano.
        As classes derivadas devem sobrescrever este método.
        """
        # print(f"DEBUG(Inimigo Base): Método receber_dano chamado na classe base. Dano: {dano}") # Debug
        pass # Implementação real deve estar nas classes derivadas

