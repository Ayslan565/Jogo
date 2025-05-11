import pygame
import math # Importa math para a função hypot

class Inimigo(pygame.sprite.Sprite):
    """
    Classe base para inimigos no jogo.
    Herda de pygame.sprite.Sprite para facilitar o manuseio de grupos de sprites.
    Recebe uma Surface do Pygame já carregada.
    """
    # Removemos a lógica de carregamento de arquivo daqui.
    # As classes derivadas (Fantasma, BonecoDeNeve) devem carregar seus sprites
    # e passar a Surface carregada para esta classe base.
    def __init__(self, x, y, image_surface):
        """
        Inicializa um novo objeto Inimigo com uma Surface de imagem.

        Args:
            x (int): A posição inicial x do inimigo.
            y (int): A posição inicial y do inimigo.
            image_surface (pygame.Surface): A Surface do Pygame já carregada para o sprite.
        """
        super().__init__() # Inicializa a classe base Sprite

        # Usamos a Surface passada diretamente
        self.image = image_surface

        # Ajusta o tamanho conforme necessário (pode ser feito nas classes derivadas também)
        # Se você já redimensionou nas classes derivadas, pode remover ou ajustar esta linha.
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect(topleft=(x, y)) # Obtém o retângulo do sprite e define a posição inicial
        self.velocidade = 2 # Define a velocidade de movimento do inimigo

    def mover_em_direcao(self, alvo_x, alvo_y):
        """
        Move o inimigo na direção de um ponto alvo.

        Args:
            alvo_x (int): A coordenada x do ponto alvo.
            alvo_y (int): A coordenada y do ponto alvo.
        """
        dx = alvo_x - self.rect.centerx # Diferença no eixo x
        dy = alvo_y - self.rect.centery # Diferença no eixo y
        distancia = math.hypot(dx, dy) # Calcula a distância usando a hipotenusa (ou pygame.math.Vector2(dx, dy).length())

        if distancia > 0:
            # Normaliza o vetor direção para obter apenas a direção
            dx /= distancia
            dy /= distancia
            # Move o inimigo na direção do alvo pela velocidade definida
            self.rect.x += dx * self.velocidade
            self.rect.y += dy * self.velocidade

    def atualizar(self, jogador_rect):
        """
        Atualiza o estado do inimigo (neste caso, move em direção ao jogador).

        Args:
            jogador_rect (pygame.Rect): O retângulo do jogador para seguir.
        """
        self.mover_em_direcao(jogador_rect.centerx, jogador_rect.centery)

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
