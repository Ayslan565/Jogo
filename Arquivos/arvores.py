import pygame
import random
import os

class Arvore(pygame.sprite.Sprite):
    """
    Representa uma árvore no jogo. Esta versão foi atualizada com o mapeamento
    correto das estações e pré-carrega todos os sprites para garantir
    performance e funcionamento correto.
    """
    # Dicionário para pré-carregar e armazenar todos os sprites.
    _sprites_por_estacao = {}
    _recursos_carregados = False

    @staticmethod
    def _carregar_recursos(largura, altura):
        """
        Carrega todos os sprites de uma só vez, executado apenas uma vez.
        Usa uma lógica robusta para encontrar os ficheiros.
        """
        if Arvore._recursos_carregados:
            return

        # Lógica para encontrar a raiz do projeto de forma segura.
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        except NameError:
            project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))

        # MODIFICAÇÃO: O mapeamento de estações e os nomes dos ficheiros foram corrigidos.
        mapa_sprites = {
            0: ['Sprites/Arvore/Arvore.png', 'Sprites/Arvore/Carvalho_Primavera.png'],    # Primavera
            1: ['Sprites/Arvore/Arvore.png', 'Sprites/Arvore/Carvalho_Verao-.png'],         # Verão
            2: ['Sprites/Arvore/Arvore_Outono.png', 'Sprites/Arvore/Carvalho_Outono.png'],  # Outono
            3: ['Sprites/Arvore/Arvore_Inverno.png', 'Sprites/Arvore/Carvalho_Inverno-.png'] # Inverno
        }

        # Itera sobre o mapa para carregar, redimensionar e armazenar cada sprite.
        for estacao_idx, caminhos in mapa_sprites.items():
            Arvore._sprites_por_estacao[estacao_idx] = []
            for caminho_relativo in caminhos:
                caminho_absoluto = os.path.join(project_root, caminho_relativo)
                try:
                    imagem = pygame.image.load(caminho_absoluto).convert_alpha()
                    imagem_redimensionada = pygame.transform.scale(imagem, (largura, altura))
                    Arvore._sprites_por_estacao[estacao_idx].append(imagem_redimensionada)
                except (pygame.error, FileNotFoundError):
                    print(f"❌ ERRO CRÍTICO EM ARVORES.PY: Não foi possível encontrar '{caminho_absoluto}'")
                    fallback = pygame.Surface((largura, altura))
                    fallback.fill((139, 69, 19))
                    Arvore._sprites_por_estacao[estacao_idx].append(fallback)
        
        Arvore._recursos_carregados = True
        print("INFO: Sprites de todas as árvores foram pré-carregados com sucesso.")

    def __init__(self, x, y, largura, altura, estacao_inicial=0):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.rect = pygame.Rect(x, y, largura, altura)
        self.image = None

        # Garante que os recursos sejam carregados (apenas na primeira vez).
        Arvore._carregar_recursos(largura, altura)
        
        # Define a imagem inicial da árvore.
        self.atualizar_sprite(estacao_inicial)

    def atualizar_sprite(self, nova_estacao):
        """
        Atualiza a imagem da árvore para a nova estação, usando os sprites pré-carregados.
        """
        self.estacao = nova_estacao
        sprites_disponiveis = Arvore._sprites_por_estacao.get(self.estacao)

        if sprites_disponiveis:
            self.image = random.choice(sprites_disponiveis)
        else:
            # Fallback caso a estação não seja encontrada.
            print(f"AVISO: Estação com índice {self.estacao} não possui sprites definidos.")
            if 0 in Arvore._sprites_por_estacao and Arvore._sprites_por_estacao[0]:
                 self.image = Arvore._sprites_por_estacao[0][0]
            else:
                 fallback = pygame.Surface((self.largura, self.altura))
                 fallback.fill((139, 69, 19))
                 self.image = fallback

        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def desenhar(self, tela, camera_x=0, camera_y=0):
        pos_x = self.rect.x - camera_x
        pos_y = self.rect.y - camera_y
        tela.blit(self.image, (pos_x, pos_y))
