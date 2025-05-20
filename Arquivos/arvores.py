# arvores.py
import pygame
import random
import os # Importa os para verificar a existência de arquivos

# Importa a classe Estacoes se ela for usada para atualizar o sprite
try:
    from Estacoes import Estacoes
except ImportError:
    print("AVISO(Arvore): Módulo 'Estacoes.py' ou classe 'Estacoes' não encontrado.")
    Estacoes = None # Define como None para evitar NameError


class Arvore(pygame.sprite.Sprite):
    """Representa uma árvore no jogo."""

    # Variável de classe para armazenar os sprites carregados por estação
    # Usamos um dicionário para armazenar listas de sprites por estação,
    # permitindo ter múltiplos sprites por estação (ex: carvalho e pinheiro)
    sprites_por_estacao = {
        0: [], # Primavera
        1: [], # Outono (ajustado a ordem para corresponder ao seu código anterior)
        2: [], # Primavera (ajustado a ordem para corresponder ao seu código anterior)
        3: [], # Inverno
        # Adicione mais estações si necessário
    }

    # Variável de classe para controlar si os sprites já foram carregados
    sprites_carregados_flag = False

    def __init__(self, x, y, largura, altura, estacao_inicial=0):
        """
        Inicializa um novo objeto Arvore.

        Args:
            x (int): A posição inicial x da árvore.
            y (int): A posição inicial y da árvore.
            largura (int): A largura desejada do sprite da árvore.
            altura (int): A altura desejada do sprite da árvore.
            estacao_inicial (int): O índice da estação inicial (0: Primavera, 1: Outono, 2: Primavera, 3: Inverno).
        """
        super().__init__()

        self.largura = largura
        self.altura = altura
        self.estacao_atual = estacao_inicial # Armazena a estação atual

        # Carrega os sprites para todas as estações apenas uma vez
        if not Arvore.sprites_carregados_flag:
            self._carregar_sprites()
            Arvore.sprites_carregados_flag = True # Marca como carregado

        # Define a imagem inicial com base na estação atual, escolhendo um sprite aleatório da lista da estação
        self.image = self._get_random_sprite_por_estacao(self.estacao_atual)

        # Define o retângulo principal do sprite (usado para desenho e posição geral)
        # A posição inicial é o canto superior esquerdo
        self.rect = self.image.get_rect(topleft=(x, y))

        # >>> Define a hitbox de colisão reduzida <<<
        # Tamanho da hitbox de colisão (4x4 pixels)
        collision_width = 64
        collision_height = 32

        # Calcula a posição da hitbox para ser no centro inferior da área original do sprite
        # O centro x da hitbox será o mesmo centro x do rect principal
        collision_center_x = self.rect.centerx
        # O fundo da hitbox será o mesmo fundo do rect principal
        collision_bottom = self.rect.bottom

        # Cria o novo retângulo de colisão
        self.collision_rect = pygame.Rect(0, 0, collision_width, collision_height)
        # Posiciona o centro inferior da nova hitbox no centro inferior do rect principal
        self.collision_rect.centerx = collision_center_x
        self.collision_rect.bottom = collision_bottom

        # print(f"DEBUG(Arvore): Árvore criada em ({x}, {y}), rect: {self.rect}, collision_rect: {self.collision_rect}") # Debug removido


    def _carregar_sprites(self):
        """Carrega os sprites da árvore para cada estação."""
        # >>> AJUSTE ESTES CAMINHOS PARA OS SEUS ARQUIVOS DE SPRITE DA ÁRVORE POR ESTAÇÃO <<<
        # Use listas de caminhos para ter múltiplos sprites por estação
        caminhos_por_estacao = {
            # Primavera (índice 0 ou 2 no seu código anterior)
            0: ['./Sprites/Arvore/Arvore.png', './Sprites/Arvore/Carvalho_Primavera.png'],
            2: ['./Sprites/Arvore/Arvore.png', './Sprites/Arvore/Carvalho_Primavera.png'],
            # Outono (índice 1 no seu código anterior)
            1: ['./Sprites/Arvore/Arvore_Outono.png', './Sprites/Arvore/Carvalho_Outono.png'],
            # Inverno (índice 3 no seu código anterior)
            3: ['./Sprites/Arvore/Arvore_Inverno.png', 'Sprites\Arvore\Carvalho_Inverno-.png'], # Verifique o caminho do Carvalho_Inverno-.png
            # Verão (sem índice específico no seu código anterior, usando como padrão 4 ou outro)
            # Adicione um índice para o Verão se necessário no seu sistema de Estações
            # Exemplo para Verão (índice 4):
            # 4: ['./Sprites/Arvore/Arvore.png', './Sprites/Arvore/Carvalho_Verao-.png'],
        }

        tamanho_sprite_desejado = (self.largura, self.altura) # Usa a largura e altura passadas no __init__

        for estacao, caminhos_lista in caminhos_por_estacao.items():
            for path in caminhos_lista:
                try:
                    if os.path.exists(path): # Verifica se o arquivo existe
                         sprite = pygame.image.load(path).convert_alpha()
                         # Redimensiona o sprite para o tamanho desejado
                         sprite = pygame.transform.scale(sprite, tamanho_sprite_desejado)
                         Arvore.sprites_por_estacao[estacao].append(sprite)
                    else:
                         print(f"AVISO(Arvore): Sprite da Árvore não encontrado para a estação {estacao}, caminho: {path}")
                         # Si o arquivo não existir, adicione um placeholder
                         placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                         pygame.draw.rect(placeholder, (100, 50, 0), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1])) # Brown placeholder
                         Arvore.sprites_por_estacao[estacao].append(placeholder)


                except pygame.error as e:
                    print(f"ERRO(Arvore): Erro ao carregar o sprite da Árvore para a estação {estacao}, caminho: {path}")
                    print(f"ERRO(Arvore): Detalhes do erro: {e}")
                    # Si ocorrer um erro, adicione um placeholder
                    placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (100, 50, 0), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1])) # Brown placeholder
                    Arvore.sprites_por_estacao[estacao].append(placeholder)

        # Garante que cada estação tenha pelo menos um sprite (placeholder si nenhum carregou)
        tamanho_sprite_desejado = (self.largura, self.altura)
        placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
        pygame.draw.rect(placeholder, (100, 50, 0), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1]))
        for estacao in [0, 1, 2, 3]: # Verifique os índices das suas estações
             if not Arvore.sprites_por_estacao.get(estacao):
                 print(f"AVISO(Arvore): Nenhum sprite carregado para a estação {estacao}. Usando placeholder.")
                 Arvore.sprites_por_estacao[estacao] = [placeholder] # Adiciona o placeholder como uma lista


    def _get_random_sprite_por_estacao(self, estacao):
        """Retorna um sprite aleatório correspondente à estação."""
        # Retorna um sprite aleatório da lista da estação especificada.
        # Si a estação não existir no dicionário ou a lista estiver vazia, retorna o sprite da estação 0 como fallback.
        sprites_da_estacao = Arvore.sprites_por_estacao.get(estacao, Arvore.sprites_por_estacao.get(0, []))

        if sprites_da_estacao:
             return random.choice(sprites_da_estacao)
        else:
             # Fallback final si mesmo a estação 0 não tiver sprites
             tamanho_sprite_desejado = (self.largura, self.altura)
             placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
             pygame.draw.rect(placeholder, (100, 50, 0), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1]))
             return placeholder


    def atualizar_sprite(self, nova_estacao):
        """Atualiza o sprite da árvore com base na nova estação."""
        # Verifica si a estação mudou e si a nova estação é válida
        if self.estacao_atual != nova_estacao and nova_estacao in Arvore.sprites_por_estacao:
            self.estacao_atual = nova_estacao
            # Escolhe um novo sprite aleatório para a nova estação
            self.image = self._get_random_sprite_por_estacao(self.estacao_atual)
            # Opcional: Atualizar a posição do rect si o novo sprite tiver um tamanho diferente
            # self.rect = self.image.get_rect(topleft=self.rect.topleft)


    def desenhar(self, surface, camera_x=0, camera_y=0):
        """
        Desenha a árvore na superfície, aplicando o offset da câmera.
        Opcional: Desenha a hitbox de colisão para debug.
        """
        # Desenha o sprite principal da árvore
        pos_x = self.rect.x - camera_x
        pos_y = self.rect.y - camera_y
        surface.blit(self.image, (pos_x, pos_y))

        # >>> Opcional: Desenhar a hitbox de colisão para visualização <<<
        # Descomente as linhas abaixo para ver a hitbox durante o desenvolvimento
        # collision_rect_on_screen = pygame.Rect(self.collision_rect.x - camera_x, self.collision_rect.y - camera_y, self.collision_rect.width, self.collision_rect.height)
        # pygame.draw.rect(surface, (255, 0, 0), collision_rect_on_screen, 1) # Desenha um retângulo vermelho de 1 pixel de largura

    # O método update pode ser adicionado aqui si a árvore tiver alguma lógica de atualização (ex: animação)
    # def update(self):
    #     pass
