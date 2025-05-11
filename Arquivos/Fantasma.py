import time
import pygame
import random
import math
from inimigos import Inimigo # Certifique-se de que Inimigo está acessível

# Certifique-se de que BonecoDeNeve está acessível, embora não seja usado diretamente nesta classe
# from BonecoDeNeve import BonecoDeNeve

class fantasma(Inimigo):
    """
    Classe para o inimigo Fantasma.
    Herda da classe base Inimigo.
    """
    # Variável de classe para armazenar os sprites carregados uma única vez
    sprites_carregados = None

    def __init__(self, x, y, velocidade=1.5):
        """
        Inicializa um novo objeto Fantasma.

        Args:
            x (int): A posição inicial x do fantasma.
            y (int): A posição inicial y do fantasma.
            velocidade (float): A velocidade de movimento do fantasma.
        """
        # Carrega os sprites apenas uma vez para todas as instâncias de Fantasma
        if fantasma.sprites_carregados is None:
            caminhos = [
                "Sprites/Inimigos/Fantasma/Fantasma1.png",
                "Sprites/Inimigos/Fantasma/Fantasma2.png",
                "Sprites/Inimigos/Fantasma/Fantasma3.png",
                "Sprites/Inimigos/Fantasma/Fantasma4.png",
                "Sprites/Inimigos/Fantasma/Fantasma5.png",
                "Sprites/Inimigos/Fantasma/Fantasma6.png",
                "Sprites/Inimigos/Fantasma/Fantasma8.png",
                "Sprites/Inimigos/Fantasma/Fantasma9.png"
            ]
            fantasma.sprites_carregados = []
            for path in caminhos:
                try:
                    sprite = pygame.image.load(path).convert_alpha()
                    # Opcional: Redimensionar sprites aqui se todos tiverem o mesmo tamanho desejado
                    # sprite = pygame.transform.scale(sprite, (64, 64))
                    fantasma.sprites_carregados.append(sprite)
                except pygame.error as e:
                    print(f"Erro ao carregar o sprite do fantasma: {path}")
                    print(f"Detalhes do erro: {e}")
                    # Se um sprite falhar, adicione um placeholder para evitar erros futuros
                    placeholder = pygame.Surface((64, 64), pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (255, 0, 255), (0, 0, 64, 64)) # Magenta placeholder
                    fonte = pygame.font.Font(None, 20)
                    texto_erro = fonte.render("Sprite", True, (0, 0, 0))
                    placeholder.blit(texto_erro, (5, 15))
                    texto_erro2 = fonte.render("Erro", True, (0, 0, 0))
                    placeholder.blit(texto_erro2, (10, 35))
                    fantasma.sprites_carregados.append(placeholder)

            # Certifique-se de que há pelo menos um sprite carregado, mesmo que seja um placeholder
            if not fantasma.sprites_carregados:
                 placeholder = pygame.Surface((64, 64), pygame.SRCALPHA)
                 pygame.draw.rect(placeholder, (255, 0, 255), (0, 0, 64, 64))
                 fantasma.sprites_carregados.append(placeholder)


        # Inicializa a classe base Inimigo PASSANDO A SURFACE CARREGADA, não o caminho.
        # Certifique-se de que o sprite tem o tamanho correto antes de passar para a base Inimigo
        # A redimensão agora pode ser feita aqui ou na classe base Inimigo
        scaled_image = pygame.transform.scale(fantasma.sprites_carregados[0], (64, 64))
        super().__init__(x, y, scaled_image)


        self.hp = 100 # Pontos de vida do fantasma
        self.velocidade = velocidade # Velocidade do fantasma
        self.sprites = fantasma.sprites_carregados # Referência à lista de sprites carregados
        self.sprite_index = 0 # Índice do sprite atual para animação
        self.tempo_ultimo_ataque = time.time() # Tempo do último ataque para controle de cooldown
        self.cooldown_ataque = 2  # Cooldown do ataque em segundos

    def atualizar_animacao(self):
        """Atualiza o índice do sprite para a animação."""
        # Incrementa o índice do sprite lentamente para a animação
        self.sprite_index = (self.sprite_index + 0.2) % len(self.sprites)
        # Define a imagem atual com base no índice
        self.image = self.sprites[int(self.sprite_index)]
        # Opcional: Redimensionar a imagem atualizada se necessário
        # self.image = pygame.transform.scale(self.image, (64, 64))


    def mover_em_direcao(self, alvo_x, alvo_y):
        """
        Move o fantasma na direção de um ponto alvo.

        Args:
            alvo_x (int): A coordenada x do ponto alvo.
            alvo_y (int): A coordenada y do ponto alvo.
        """
        dx = alvo_x - self.rect.centerx # Diferença no eixo x
        dy = alvo_y - self.rect.centery # Diferença no eixo y
        distancia = math.hypot(dx, dy) # Calcula a distância usando a hipotenusa

        if distancia > 0:
            # Normaliza o vetor direção para obter apenas a direção
            dx /= distancia
            dy /= distancia
            # Move o fantasma na direção do alvo pela velocidade definida
            self.rect.x += dx * self.velocidade
            self.rect.y += dy * self.velocidade

    def update(self, player_rect):
        """
        Atualiza o estado do fantasma (movimento e animação).

        Args:
            player_rect (pygame.Rect): O retângulo do jogador para seguir.
        """
        self.mover_em_direcao(player_rect.centerx, player_rect.centery) # Move em direção ao jogador
        self.atualizar_animacao() # Atualiza a animação do sprite

    def atacar(self, player):
        """
        Realiza um ataque no jogador se estiver em alcance e o cooldown permitir.

        Args:
            player (Player): O objeto Player a ser atacado.
        """
        agora = time.time() # Tempo atual
        # Verifica colisão com o jogador e se o cooldown do ataque passou
        if self.rect.colliderect(player.rect) and (agora - self.tempo_ultimo_ataque >= self.cooldown_ataque):
            dano = 10 # Quantidade de dano a ser aplicado
            player.receber_dano(dano) # Aplica dano ao jogador

            # Lógica para empurrar o jogador para longe
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distancia = math.hypot(dx, dy)
            if distancia > 0:
                dx /= distancia
                dy /= distancia
                empurrar_forca = 15
                player.rect.x += dx * empurrar_forca
                player.rect.y += dy * empurrar_forca

            self.tempo_ultimo_ataque = agora # Atualiza o tempo do último ataque
