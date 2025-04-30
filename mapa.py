import random
from grama import Grama
import pygame
from arvores import Arvore

# Definindo as dimensões do mapa
LARGURA_MAPA = 1920
ALTURA_MAPA = 1080
TAMANHO_CELULA = 50  # Tamanho das células do grid

class MapaProcedural:
    def __init__(self):
        self.largura = LARGURA_MAPA // TAMANHO_CELULA
        self.altura = ALTURA_MAPA // TAMANHO_CELULA
        self.grid = [[None for _ in range(self.altura)] for _ in range(self.largura)]

        # Geração do mapa
        self.gerar_mapa()

    def gerar_mapa(self):
        for x in range(self.largura):
            for y in range(self.altura):
                # Aleatoriamente, cria objetos de grama, árvore, etc.
                tipo_terreno = random.choice(['grama', 'arvore', 'vazio'])
                if tipo_terreno == 'grama':
                    self.grid[x][y] = Grama(x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA)
                elif tipo_terreno == 'arvore':
                    if random.random() < 0.1:  # Menor chance para árvores
                        self.grid[x][y] = Arvore(x * TAMANHO_CELULA, y * TAMANHO_CELULA, 180, 180)

    def desenhar(self, tela):
        for x in range(self.largura):
            for y in range(self.altura):
                if self.grid[x][y] is not None:
                    self.grid[x][y].desenhar(tela)
                    
class Tela:
    def __init__(self):
        self.mapa = MapaProcedural()  # O mapa é gerado uma vez
        self.camera_x = 0
        self.camera_y = 0
        self.mapa_gerado = False  # Flag para saber se o mapa foi gerado
        self.temporizador = 0  # Armazena o tempo de espera para a geração do mapa
        self.gerou_mapa = False  # Controle para garantir que o mapa só seja gerado uma vez

    def atualizar_tela(self, Asrahel, dt):
        # Verifica o tempo restante para permitir a regeneração do mapa
        if self.temporizador > 0:
            self.temporizador -= dt  # Decrementa o temporizador com o delta time

        # Verificar se o jogador alcançou o limite da tela
        if self.temporizador <= 0 and not self.gerou_mapa:  # Verifica se o tempo de espera acabou e ainda não gerou o mapa
            if Asrahel.rect.left > LARGURA_MAPA - 10:  # Se o jogador passar 10 pixels antes da borda direita
                self.camera_x = 0  # Reseta a posição do lado esquerdo
                self.mapa = MapaProcedural()  # Gera um novo mapa
                Asrahel.rect.left = 10  # Posiciona o jogador 10 pixels antes da borda direita
                self.temporizador = 30000  # Define o temporizador para 30 segundos (em milissegundos)
                self.gerou_mapa = True  # Marca que o mapa foi gerado

            elif Asrahel.rect.right < 10:  # Se o jogador passar 10 pixels antes da borda esquerda
                self.camera_x = LARGURA_MAPA - Asrahel.rect.width  # Teletransporta o jogador para o lado direito
                self.mapa = MapaProcedural()  # Gera um novo mapa
                Asrahel.rect.right = LARGURA_MAPA - 10  # Posiciona o jogador 10 pixels antes da borda esquerda
                self.temporizador = 30000  # Define o temporizador para 30 segundos (em milissegundos)
                self.gerou_mapa = True  # Marca que o mapa foi gerado

            elif Asrahel.rect.top > ALTURA_MAPA - 10:  # Se o jogador passar 10 pixels antes da borda inferior
                self.camera_y = 0
                self.mapa = MapaProcedural()  # Gera um novo mapa
                Asrahel.rect.top = 10  # Posiciona o jogador 10 pixels antes da borda inferior
                self.temporizador = 30000  # Define o temporizador para 30 segundos (em milissegundos)
                self.gerou_mapa = True  # Marca que o mapa foi gerado

            elif Asrahel.rect.bottom < 10:  # Se o jogador passar 10 pixels antes da borda superior
                self.camera_y = ALTURA_MAPA - Asrahel.rect.height
                self.mapa = MapaProcedural()  # Gera um novo mapa
                Asrahel.rect.bottom = ALTURA_MAPA - 10  # Posiciona o jogador 10 pixels antes da borda superior
                self.temporizador = 30000  # Define o temporizador para 30 segundos (em milissegundos)
                self.gerou_mapa = True  # Marca que o mapa foi gerado

    def desenhar(self, janela, Asrahel):
        # Atualiza a tela e gera novos mapas quando necessário
        self.atualizar_tela(Asrahel, pygame.time.get_ticks())  # Passa o tempo de execução do jogo para o temporizador
        self.mapa.desenhar(janela)

        # Quando o tempo de espera terminar, reinicia a geração do mapa
        if self.temporizador <= 0:
            self.gerou_mapa = False  # Permite a geração de um novo mapa após o tempo passar
