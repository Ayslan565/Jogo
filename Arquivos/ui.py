# ui.py
# Responsável pelos elementos da interface do usuário (HUD), como barra de vida e timer

import pygame
import time

# Importa configurações
try:
    import config # Importa o arquivo de configuração
except ImportError:
    print("AVISO(UI): Módulo 'config.py' não encontrado.")
    config = None # Define como None para evitar NameError


class Vida:
    """Representa a vida de uma entidade e a exibe como uma barra."""
    def __init__(self, vida_maxima, vida_atual):
        self.vida_maxima = vida_maxima
        self.vida_atual = vida_atual
        # Define a fonte para exibir o texto da vida
        # Verifica se pygame.font está inicializado antes de usar
        if pygame.font.get_init():
             self.font = pygame.font.SysFont(None, 30) # Ajuste o tamanho da fonte si necessário
        else:
             # print("AVISO(UI): Pygame.font não inicializado. Não foi possível criar a fonte para a vida.") # Debug removido
             self.font = None # Define como None si a fonte não puder ser criada

        # Cores para a barra de vida
        self.cor_barra = (0, 255, 0) # Verde (ajuste si necessário)
        self.cor_fundo = (255, 0, 0) # Vermelho (ajuste si necessário)
        self.cor_texto = (255, 255, 255) # Branco (ajuste si necessário)

    def receber_dano(self, dano):
        """Reduz a vida atual pela quantidade de dano."""
        self.vida_atual -= dano
        if self.vida_atual < 0:
            self.vida_atual = 0 # Garante que a vida não fique negativa
        # print(f"DEBUG(UI - Vida): Recebeu {dano} de dano. HP restante: {self.vida_atual}") # Debug removido

    def curar(self, quantidade):
        """Aumenta a vida atual pela quantidade de cura."""
        self.vida_atual += quantidade
        if self.vida_atual > self.vida_maxima:
            self.vida_atual = self.vida_maxima # Garante que a vida não ultrapasse o máximo
        # print(f"DEBUG(UI - Vida): Curado {quantidade}. HP atual: {self.vida_atual}") # Debug removido

    def esta_vivo(self):
        """Retorna True si a vida atual for maior que zero."""
        return self.vida_atual > 0

    def desenhar(self, surface, x, y, largura_barra=100, altura_barra=15):
        """
        Desenha a barra de vida e o texto da vida na superfície.

        Args:
            surface (pygame.Surface): A superfície onde desenhar.
            x (int): A posição x onde desenhar a barra.
            y (int): A posição y onde desenhar a barra.
            largura_barra (int): A largura total da barra de vida.
            altura_barra (int): A altura da barra de vida.
        """
        # Calcula a largura da barra de vida atual com base na porcentagem
        largura_atual = (self.vida_atual / self.vida_maxima) * largura_barra

        # Desenha o fundo da barra de vida (vermelho)
        fundo_barra_rect = pygame.Rect(x, y, largura_barra, altura_barra)
        pygame.draw.rect(surface, self.cor_fundo, fundo_barra_rect)

        # Desenha a barra de vida atual (verde)
        barra_vida_rect = pygame.Rect(x, y, largura_atual, altura_barra)
        pygame.draw.rect(surface, self.cor_barra, barra_vida_rect)

        # Desenha o texto da vida (ex: "HP: 85")
        if self.font: # Verifica si a fonte foi criada com sucesso
             texto_vida = self.font.render(f"HP: {self.vida_atual}", True, self.cor_texto)
             # Posiciona o texto abaixo ou ao lado da barra (ajuste conforme necessário)
             surface.blit(texto_vida, (x, y + altura_barra + 5)) # 5 pixels abaixo da barra


class Timer:
    """Controla e exibe o tempo de jogo."""
    def __init__(self):
        self.start_time = time.time() # Tempo em que o timer começou
        # Define a fonte para exibir o tempo
        # Verifica se pygame.font está inicializado antes de usar
        if pygame.font.get_init():
             self.font = pygame.font.SysFont(None, 30) # Ajuste o tamanho da fonte si necessário
        else:
             # print("AVISO(UI): Pygame.font não inicializado. Não foi possível criar a fonte para o timer.") # Debug removido
             self.font = None # Define como None si a fonte não puder ser criada

        self.color = (255, 255, 255) # Cor do texto do timer (branco)

    def get_time(self):
        """Retorna o tempo decorrido em segundos."""
        return time.time() - self.start_time

    def desenhar(self, surface, x, y):
        """
        Desenha o tempo decorrido na superfície.

        Args:
            surface (pygame.Surface): A superfície onde desenhar.
            x (int): A posição x onde desenhar o texto.
            y (int): A posição y onde desenhar o texto.
        """
        if self.font: # Verifica si a fonte foi criada com sucesso
             tempo_segundos = int(self.get_time())
             texto_timer = self.font.render(f"Tempo: {tempo_segundos}s", True, self.color)
             surface.blit(texto_timer, (x, y))
        # else:
             # print("AVISO(UI): Fonte do timer não disponível para desenho.") # Debug removido

# Outras classes ou funções relacionadas à UI podem ser adicionadas aqui, como:
# - Pontuação
# - Mensagens na tela
# - Inventário
