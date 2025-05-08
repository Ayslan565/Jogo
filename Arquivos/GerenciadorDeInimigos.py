import pygame
import random
from Fantasma import fantasma
from BonecoDeNeve import BonecoDeNeve

class GerenciadorDeInimigos:
    def __init__(self):
        self.inimigos = []  # Lista que armazena todos os inimigos
    
    def spawn_inimigos(self, estacao, jogador):
        """
        Responsável por gerar inimigos com base na estação do ano.
        """
        if estacao == "inverno":
            # Spawn de inimigos específicos do inverno
            x = random.randint(0, 1920)  # Local aleatório na tela
            y = random.randint(0, 1080)  # Local aleatório na tela
            novo_inimigo = fantasma(x, y)  # Criando o inimigo fantasma
            self.inimigos.append(novo_inimigo)
            print(f"Inimigo Fantasma spawnado em ({x}, {y}).")
        elif estacao == "verao":
            # Spawn de inimigos para o verão
            x = random.randint(0, 1920)  # Local aleatório na tela
            y = random.randint(0, 1080)  # Local aleatório na tela
            novo_inimigo = BonecoDeNeve(x, y)  # Criando o inimigo boneco de neve
            self.inimigos.append(novo_inimigo)
            print(f"Inimigo Boneco de Neve spawnado em ({x}, {y}).")
        # Adicione mais condições para outras estações se necessário

    def update_inimigos(self, jogador_rect):
        """
        Atualiza os inimigos, verificando colisões e movimentações.
        """
        for inimigo in self.inimigos:
            inimigo.atualizar(jogador_rect)  # Atualiza o inimigo com base na posição do jogador
    
    def desenhar_inimigos(self, janela, camera_x, camera_y):
        """
        Desenha todos os inimigos na tela.
        """
        for inimigo in self.inimigos:
            print(f"Desenhando inimigo na posição {inimigo.rect.x}, {inimigo.rect.y}")
            inimigo.desenhar(janela, camera_x, camera_y)  # Desenha cada inimigo na janela
