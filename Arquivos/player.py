# player.py
import pygame
import random
from vida import Vida
from arvores import Arvore # Importado mas não usado no código fornecido, mantido por compatibilidade
from grama import Grama # Importado mas não usado no código fornecido, mantido por compatibilidade
import math
import os # Importa os para verificar a existência de arquivos

class Player(pygame.sprite.Sprite):
    def __init__(self, velocidade=5, vida_maxima=100):
        super().__init__()

        self.x = random.randint(0, 800) # Posição inicial aleatória (pode ser ajustada)
        self.y = random.randint(0, 600) # Posição inicial aleatória (pode ser ajustada)

        self.velocidade = velocidade
        self.vida = Vida(vida_maxima) # Inicializa o objeto Vida

        # --- Carregamento e Escalonamento dos Sprites ---
        tamanho_sprite_desejado = (60, 60) # Tamanho desejado para todos os sprites

        # Sprites de animação de movimento (Esquerda)
        caminhos_esquerda = [
            "Sprites/Asrahel/Esquerda/Ashael_E1.png",
            "Sprites/Asrahel/Esquerda/Ashael_E2.png",
            "Sprites/Asrahel/Esquerda/Ashael_E3.png",
            "Sprites/Asrahel/Esquerda/Ashael_E4.png",
            "Sprites/Asrahel/Esquerda/Ashael_E5.png",
            "Sprites/Asrahel/Esquerda/Ashael_E6.png",
        ]
        self.sprites_esquerda = self._carregar_sprites(caminhos_esquerda, tamanho_sprite_desejado, "Esquerda")

        # Sprites de animação de idle (Esquerda)
        caminhos_idle_esquerda = [
            "Sprites/Asrahel/Esquerda/Ashael_E1.png",
        ]
        self.sprites_idle_esquerda = self._carregar_sprites(caminhos_idle_esquerda, tamanho_sprite_desejado, "Idle Esquerda")

        # Sprites de animação de movimento (Direita) - Assumindo que você terá esses arquivos
        # >>> AJUSTE ESTES CAMINHOS PARA OS SEUS SPRITES DE DIREITA <<<
        caminhos_direita = [
            "Sprites/Asrahel/Direita/Ashael_D1.png",
            "Sprites/Asrahel/Direita/Ashael_D2.png",
            "Sprites/Asrahel/Direita/Ashael_D3.png",
            "Sprites/Asrahel/Direita/Ashael_D4.png",
            "Sprites/Asrahel/Direita/Ashael_D5.png",
            "Sprites/Asrahel/Direita/Ashael_D6.png",
        ]
        self.sprites_direita = self._carregar_sprites(caminhos_direita, tamanho_sprite_desejado, "Direita")

        # Sprites de animação de idle (Direita) - Assumindo que você terá esses arquivos
        # >>> AJUSTE ESTES CAMINHOS PARA OS SEUS SPRITES DE IDLE DIREITA <<<
        caminhos_idle_direita = [
            "Sprites/Asrahel/Direita/Ashael_D1.png",
        ]
        self.sprites_idle_direita = self._carregar_sprites(caminhos_idle_direita, tamanho_sprite_desejado, "Idle Direita")


        # Define o sprite inicial e o retângulo de colisão
        self.atual = 0 # Índice do sprite de movimento atual
        self.frame_idle = 0 # Índice do sprite de idle atual
        self.parado = True # Estado de movimento
        self.direction = "right" # Direção inicial (pode ser "left" ou "right")

        # Define a imagem inicial (começa virado para a direita por padrão)
        self.image = self.sprites_idle_direita[self.frame_idle] if self.sprites_idle_direita else (self.sprites_idle_esquerda[self.frame_idle] if self.sprites_idle_esquerda else pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        # Ajusta o tamanho do retângulo de colisão (hitbox)
        self.rect_colisao = self.rect.inflate(-30, -20) # Exemplo: reduz a hitbox em 30px na largura e 20px na altura


        # Controle de tempo de animação
        self.tempo_animacao = 100  # milissegundos entre frames
        self.ultimo_update = pygame.time.get_ticks()

    def _carregar_sprites(self, caminhos, tamanho, nome_conjunto):
        """Carrega e escala uma lista de sprites, com tratamento de erro e placeholder."""
        sprites = []
        for path in caminhos:
            if not os.path.exists(path):
                print(f"DEBUG(Player): Aviso: Arquivo de sprite não encontrado: {path}")
                # Cria um placeholder se o arquivo não existir
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255, 0, 255), (0, 0, tamanho[0], tamanho[1])) # Placeholder Magenta
                # >>> AQUI ESTÁ A LINHA QUE CAUSA O ERRO SE PYGAME.FONT NÃO FOI INICIALIZADO <<<
                # Removido o uso direto de pygame.font.Font aqui para evitar o erro de inicialização
                # A mensagem de erro será apenas no console se o sprite falhar ao carregar
                sprites.append(placeholder)
                continue # Pula para o próximo caminho

            try:
                sprite = pygame.image.load(path).convert_alpha()
                sprite = pygame.transform.scale(sprite, tamanho)
                sprites.append(sprite)
            except pygame.error as e:
                print(f"DEBUG(Player): Erro ao carregar o sprite '{path}': {e}")
                # Cria um placeholder se houver erro de carregamento
                # Removido o uso direto de pygame.font.Font aqui para evitar o erro de inicialização
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255, 0, 255), (0, 0, tamanho[0], tamanho[1])) # Placeholder Magenta
                sprites.append(placeholder)

        if not sprites:
            print(f"DEBUG(Player): Aviso: Nenhum sprite carregado para o conjunto '{nome_conjunto}'. Usando placeholder padrão.")
            # Adiciona um placeholder se a lista de sprites estiver vazia
            # Removido o uso direto de pygame.font.Font aqui para evitar o erro de inicialização
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (255, 0, 255), (0, 0, tamanho[0], tamanho[1])) # Placeholder Magenta
            sprites.append(placeholder)

        return sprites


    def receber_dano(self, dano):
        """Reduz a vida do jogador."""
        self.vida.receber_dano(dano)
        if not self.vida.esta_vivo():
            print("Você morreu!")
            # Adicionar lógica para fim de jogo aqui

    def update(self):
        """Atualiza o estado do jogador (animação e posição do retângulo de colisão)."""
        agora = pygame.time.get_ticks()

        # Lógica de animação
        if agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            if self.parado:
                # Verifica se a lista de sprites de idle esquerda não está vazia antes de usar
                if self.sprites_idle_esquerda:
                    self.frame_idle = (self.frame_idle + 1) % len(self.sprites_idle_esquerda)
                    # Seleciona o sprite de idle correto com base na direção
                    if self.direction == "left" and self.sprites_idle_esquerda:
                        self.image = self.sprites_idle_esquerda[self.frame_idle]
                    elif self.direction == "right" and self.sprites_idle_direita:
                        self.image = self.sprites_idle_direita[self.frame_idle]
                    else: # Fallback para esquerda se direita não existir
                         self.image = self.sprites_idle_esquerda[self.frame_idle]
                elif self.sprites_idle_direita: # Fallback para direita se esquerda estiver vazia
                     self.frame_idle = (self.frame_idle + 1) % len(self.sprites_idle_direita)
                     self.image = self.sprites_idle_direita[self.frame_idle]
                elif self.sprites_esquerda: # Fallback para primeiro sprite de movimento esquerdo
                     self.image = self.sprites_esquerda[0]
                else: # Fallback para um placeholder se nenhuma lista de sprites de idle ou movimento existir
                     self.image = pygame.Surface((60, 60), pygame.SRCALPHA) # Placeholder

            else: # Se não estiver parado (a mover)
                # Verifica se a lista de sprites de movimento esquerda não está vazia antes de usar
                if self.sprites_esquerda:
                    self.atual = (self.atual + 1) % len(self.sprites_esquerda)
                    # Seleciona o sprite de movimento correto com base na direção
                    if self.direction == "left" and self.sprites_esquerda:
                        self.image = self.sprites_esquerda[self.atual]
                    elif self.direction == "right" and self.sprites_direita:
                        self.image = self.sprites_direita[self.atual]
                    else: # Fallback para esquerda se direita não existir
                         self.image = self.sprites_esquerda[self.atual]
                elif self.sprites_direita: # Fallback para direita se esquerda estiver vazia
                     self.atual = (self.atual + 1) % len(self.sprites_direita)
                     self.image = self.sprites_direita[self.atual]
                elif self.sprites_idle_esquerda: # Fallback para primeiro sprite de idle esquerdo
                     self.image = self.sprites_idle_esquerda[0]
                else: # Fallback para um placeholder se nenhuma lista de sprites de movimento ou idle existir
                     self.image = pygame.Surface((60, 60), pygame.SRCALPHA) # Placeholder


        # Atualiza a posição do retângulo de colisão (rect) para a posição atual do jogador
        self.rect.center = (self.x, self.y)
        # Atualiza a posição do retângulo de colisão secundário (rect_colisao)
        self.rect_colisao.center = self.rect.center


    def mover(self, teclas, arvores):
        """Move o jogador e atualiza a direção."""
        dx = dy = 0

        if teclas[pygame.K_LEFT]:
            dx = -self.velocidade
            self.direction = "left" # Atualiza a direção para esquerda
        if teclas[pygame.K_RIGHT]:
            dx = self.velocidade
            self.direction = "right" # Atualiza a direção para direita
        if teclas[pygame.K_UP]:
            dy = -self.velocidade
            # Não muda a direção horizontal para cima/baixo, mantém a última horizontal
        if teclas[pygame.K_DOWN]:
            dy = self.velocidade
            # Não muda a direção horizontal para cima/baixo, mantém a última horizontal

        # Move o jogador
        self.x += dx
        self.y += dy

        # Atualiza o estado de parado
        self.parado = (dx == 0 and dy == 0)

        # A posição do self.rect e self.rect_colisao é atualizada no método update()


    def trocar_arma(self):
        """Lógica para trocar de arma (se aplicável)."""
        # Implemente a lógica de troca de arma aqui
        pass # Placeholder

    def usar_arma(self, inimigo):
        """Lógica para usar a arma atual (se aplicável)."""
        # Implemente a lógica de uso da arma aqui
        pass # Placeholder

    def atacar(self, teclas, inimigos):
        """Lógica de ataque do jogador."""
        # Implemente a lógica de ataque aqui
        pass # Placeholder

    def empurrar_jogador(self, inimigo):
        """Lógica para empurrar o jogador (se aplicável)."""
        # Implemente a lógica de empurrar aqui
        pass # Placeholder

    def desenhar_vida(self, tela, x, y):
        """Desenha a barra de vida do jogador."""
        self.vida.desenhar(tela, x, y)
