import pygame
import random
import time
class Estacoes:
    def __init__(self):
        self.i = random.randint(0, 3)
        self.cor = self.definir_cor()
        self.tempo_troca = 10  # segundos
        self.ultimo_tempo = time.time()
        self.mensagem_estacao = self.nome_estacao()
        self.tempo_mensagem = self.ultimo_tempo

    def nome_estacao(self):
        if self.i == 0:
            return "Primavera"
        elif self.i == 1:
            return "Outono"
        elif self.i == 2:
            return "Verão"
        elif self.i == 3:
            return "Inverno"

    def definir_cor(self):
        if self.i == 0:
            return (137, 183, 137)
        elif self.i == 1:
            return (204, 153, 102)
        elif self.i == 2:
            return (81, 170, 72)
        elif self.i == 3:
            return (200, 220, 255)

    def atualizar(self):
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_tempo > self.tempo_troca:
            self.troca_estacao()
            self.ultimo_tempo = tempo_atual

    def troca_estacao(self):
        nova_i = random.randint(0, 3)
        while nova_i == self.i:
            nova_i = random.randint(0, 3)
        self.i = nova_i
        self.cor = self.definir_cor()
        self.mensagem_estacao = self.nome_estacao()
        self.tempo_mensagem = time.time()

    def desenhar(self, tela):
        tela.fill(self.cor)

    def desenhar_mensagem_estacao(self, janela):
        if time.time() - self.tempo_mensagem > 2:
            return  # não desenha mais após 2 segundos

        largura_tela, altura_tela = janela.get_size()
        fonte = pygame.font.Font(pygame.font.get_default_font(), 30)
        texto = fonte.render(self.mensagem_estacao.upper(), True, (255, 255, 255))
        
        largura_caixa = texto.get_width() + 1080  # ajuste para o tamanho do retângulo
        altura_caixa = texto.get_height() + 40  # ajuste para o tamanho do retângulo

        x = (largura_tela - largura_caixa) // 2
        y = (altura_tela - altura_caixa) // 2

        # Pontos do polígono com triângulos nas laterais
        pontos = [
            (x - 15, y + altura_caixa // 2),  # ponta esquerda do triângulo
            (x, y),                           # canto superior esquerdo do retângulo
            (x + largura_caixa, y),           # canto superior direito do retângulo
            (x + largura_caixa + 15, y + altura_caixa // 2),  # ponta direita do triângulo
            (x + largura_caixa, y + altura_caixa),  # canto inferior direito do retângulo
            (x, y + altura_caixa)             # canto inferior esquerdo do retângulo
        ]

        superficie = pygame.Surface((largura_caixa + 30, altura_caixa), pygame.SRCALPHA)
        desloc_x = x - 15  # pois expandimos a superfície em 15 px pra cada lado
        desloc_y = y

        pontos_deslocados = [(px - desloc_x, py - desloc_y) for px, py in pontos]

        pygame.draw.polygon(superficie, (0, 0, 0, 150), pontos_deslocados)
        pygame.draw.polygon(superficie, (205, 181, 171), pontos_deslocados, 2)

        janela.blit(superficie, (desloc_x, desloc_y))

        # Centraliza o texto no retângulo
        texto_x = x + (largura_caixa - texto.get_width()) // 2
        texto_y = y + (altura_caixa - texto.get_height()) // 2

        janela.blit(texto, (texto_x, texto_y))
