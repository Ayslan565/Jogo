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
        tempo_passado = time.time() - self.tempo_mensagem
        duracao = 2

        if tempo_passado > duracao:
            return

        # Calcula a opacidade (255 no início, 0 no final)
        alpha = int(255 * (1 - tempo_passado / duracao))
        alpha = max(0, min(alpha, 255))  # Garante que fique no intervalo válido

        largura_tela, altura_tela = janela.get_size()
        fonte = pygame.font.Font(pygame.font.get_default_font(), 30)
        texto = fonte.render(self.mensagem_estacao.upper(), True, (255, 255, 255))
        
        largura_caixa = texto.get_width() + 1080
        altura_caixa = texto.get_height() + 40

        x = (largura_tela - largura_caixa) // 2
        y = (altura_tela - altura_caixa) // 2

        pontos = [
            (x - 15, y + altura_caixa // 2),
            (x, y),
            (x + largura_caixa, y),
            (x + largura_caixa + 15, y + altura_caixa // 2),
            (x + largura_caixa, y + altura_caixa),
            (x, y + altura_caixa)
        ]

        superficie = pygame.Surface((largura_caixa + 30, altura_caixa), pygame.SRCALPHA)
        desloc_x = x - 15
        desloc_y = y
        pontos_deslocados = [(px - desloc_x, py - desloc_y) for px, py in pontos]

        pygame.draw.polygon(superficie, (0, 0, 0, alpha // 1.7), pontos_deslocados)  # fundo semitransparente
        pygame.draw.polygon(superficie, (205, 181, 171, alpha), pontos_deslocados, 2)  # borda

        janela.blit(superficie, (desloc_x, desloc_y))

        # Cria uma superfície para o texto com alpha
        texto_superficie = fonte.render(self.mensagem_estacao.upper(), True, (255, 255, 255))
        texto_superficie.set_alpha(alpha)

        texto_x = x + (largura_caixa - texto.get_width()) // 2
        texto_y = y + (altura_caixa - texto.get_height()) // 2

        janela.blit(texto_superficie, (texto_x, texto_y))
