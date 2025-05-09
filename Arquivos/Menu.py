# menu.py
import pygame

# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# Classe Menu
class Menu:
    def __init__(self, largura_tela, altura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.font = pygame.font.Font(pygame.font.get_default_font(), 50)
        self.opcao_jogar = self.font.render("Jogar", True, AZUL)
        self.opcao_sair = self.font.render("Sair", True, VERDE)
        self.titulo = self.font.render("Tela Inicial", True, BRANCO)

    def desenhar(self, tela):
        tela.fill(PRETO)

        # Posições dos textos
        x_titulo = (self.largura_tela - self.titulo.get_width()) // 2
        y_titulo = self.altura_tela // 4

        x_jogar = (self.largura_tela - self.opcao_jogar.get_width()) // 2
        y_jogar = self.altura_tela // 2

        x_sair = (self.largura_tela - self.opcao_sair.get_width()) // 2
        y_sair = self.altura_tela // 2 + 100

        # Desenha os textos
        tela.blit(self.titulo, (x_titulo, y_titulo))
        tela.blit(self.opcao_jogar, (x_jogar, y_jogar))
        tela.blit(self.opcao_sair, (x_sair, y_sair))

        pygame.display.update()

    def verificar_click(self, x, y):
        # Verifica se o click foi dentro da área do botão "Jogar"
        if (self.largura_tela // 2 - self.opcao_jogar.get_width() // 2 < x < self.largura_tela // 2 + self.opcao_jogar.get_width() // 2) and (self.altura_tela // 2 < y < self.altura_tela // 2 + self.opcao_jogar.get_height()):
            return "jogar"
        
        # Verifica se o click foi dentro da área do botão "Sair"
        if (self.largura_tela // 2 - self.opcao_sair.get_width() // 2 < x < self.largura_tela // 2 + self.opcao_sair.get_width() // 2) and (self.altura_tela // 2 + 100 < y < self.altura_tela // 2 + 150):
            return "sair"

