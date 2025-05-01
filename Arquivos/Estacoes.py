import pygame
import random
import time

class Estacoes:
    def __init__(self):
        self.i = random.randint(0, 3)
        self.cor = self.definir_cor()
        self.tempo_troca = 10  # segundos
        self.ultimo_tempo = time.time()

    def definir_cor(self):
        if self.i == 0:
            print("Primavera 🌸")
            return (137, 183, 137)  # verde suave
        elif self.i == 1:
            print("Outono 🍂")
            return (204, 153, 102)  # marrom alaranjado
        elif self.i == 2:
            print("Verão ☀️")
            return (81, 170, 72)  # verde intenso
        elif self.i == 3:
            print("Inverno ❄️")
            return (200, 220, 255)  # azul claro quase branco

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

    def desenhar(self, tela):
        tela.fill(self.cor)
