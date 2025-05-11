import pygame
import random
import math
from inimigos import Inimigo # Certifique-se de que Inimigo está acessível
import time # Importa time se for usado para cooldowns ou outras lógicas de tempo

"""
Classe para o inimigo Boneco de Neve.
Herda da classe base Inimigo.
"""
class BonecoDeNeve(Inimigo):
    # Variável de classe para armazenar os sprites carregados uma única vez
    sprites_carregados = None

    def __init__(self, x, y, velocidade=1.0):
        """
        Inicializa um novo objeto BonecoDeNeve.

        Args:
            x (int): A posição inicial x do boneco de neve.
            y (int): A posição inicial y do boneco de neve.
            velocidade (float): A velocidade de movimento do boneco de neve.
        """
        # Carrega os sprites apenas uma vez para todas as instâncias de BonecoDeNeve
        if BonecoDeNeve.sprites_carregados is None:
            caminhos = [
                "Sprites\\Inimigos\\Boneco de Neve\\Boneco De Neve 1.png",
                "Sprites\\Inimigos\\Boneco de Neve\\Boneco de Neve 2.png",
                "Sprites\\Inimigos\\Boneco de Neve\\Boneco de Neve 3.png",

            ]
            BonecoDeNeve.sprites_carregados = []
            for path in caminhos:
                 try:
                    sprite = pygame.image.load(path).convert_alpha()
                    # Opcional: Redimensionar sprites aqui se todos tiverem o mesmo tamanho desejado
                    # sprite = pygame.transform.scale(sprite, (64, 64))
                    BonecoDeNeve.sprites_carregados.append(sprite)
                 except pygame.error as e:
                    print(f"Erro ao carregar o sprite do Boneco de Neve: {path}")
                    print(f"Detalhes do erro: {e}")
                    # Se um sprite falhar, adicione um placeholder
                    placeholder = pygame.Surface((64, 64), pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (0, 255, 255), (0, 0, 64, 64)) # Cyan placeholder
                    fonte = pygame.font.Font(None, 20)
                    texto_erro = fonte.render("Sprite", True, (0, 0, 0))
                    placeholder.blit(texto_erro, (5, 15))
                    texto_erro2 = fonte.render("Erro", True, (0, 0, 0))
                    placeholder.blit(texto_erro2, (10, 35))
                    BonecoDeNeve.sprites_carregados.append(placeholder)

            # Certifique-se de que há pelo menos um sprite carregado
            if not BonecoDeNeve.sprites_carregados:
                 placeholder = pygame.Surface((64, 64), pygame.SRCALPHA)
                 pygame.draw.rect(placeholder, (0, 255, 255), (0, 0, 64, 64))
                 BonecoDeNeve.sprites_carregados.append(placeholder)


        # Inicializa a classe base Inimigo PASSANDO A SURFACE CARREGADA, não o caminho.
        # Certifique-se de que o sprite tem o tamanho correto antes de passar para a base Inimigo
        # A redimensão agora pode ser feita aqui ou na classe base Inimigo
        scaled_image = pygame.transform.scale(BonecoDeNeve.sprites_carregados[0], (64, 64))
        super().__init__(x, y, scaled_image)


        self.hp = 100 # Pontos de vida do boneco de neve
        self.velocidade = velocidade # Velocidade do boneco de neve
        self.sprites = BonecoDeNeve.sprites_carregados # Referência à lista de sprites carregados
        self.sprite_index = 0 # Índice do sprite atual para animação

        # Adicione atributos específicos do Boneco de Neve se houver (ex: cooldown de ataque)
        # self.tempo_ultimo_ataque = time.time()
        # self.cooldown_ataque = 3 # segundos


    def atualizar_animacao(self):
        """Atualiza o índice do sprite para a animação."""
        # Incrementa o índice do sprite lentamente para a animação
        self.sprite_index = (self.sprite_index + 0.1) % len(self.sprites)
        # Define a imagem atual com base no índice
        self.image = self.sprites[int(self.sprite_index)]
        # Opcional: Redimensionar a imagem atualizada se necessário
        # self.image = pygame.transform.scale(self.image, (64, 64))


    def mover_em_direcao(self, alvo_x, alvo_y):
        """
        Move o boneco de neve na direção de um ponto alvo.

        Args:
            alvo_x (int): A coordenada x do ponto alvo.
            alvo_y (int): A coordenada y do ponto alvo.
        """
        dx = alvo_x - self.rect.centerx
        dy = alvo_y - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia
            self.rect.x += dx * self.velocidade
            self.rect.y += dy * self.velocidade

    def update(self, player_rect):
        """
        Atualiza o estado do boneco de neve (movimento e animação).

        Args:
            player_rect (pygame.Rect): O retângulo do jogador para seguir.
        """
        self.mover_em_direcao(player_rect.centerx, player_rect.centery)
        self.atualizar_animacao()

    # Adicione métodos específicos do Boneco de Neve se houver (ex: atacar)
    # def atacar(self, player):
    #     pass # Implemente a lógica de ataque do boneco de neve aqui
