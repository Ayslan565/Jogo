import pygame
import time

class Timer:
    """
    Classe para gerenciar e desenhar um timer na tela do Pygame.
    """
    def __init__(self, pos_x, pos_y, font_size=36, text_color=(255, 255, 255), bg_color=(0, 0, 0, 128), border_color=(255, 255, 255), border_radius=10):
        """
        Inicializa o objeto Timer.

        Args:
            pos_x (int): Posição X do canto superior esquerdo do fundo do timer.
            pos_y (int): Posição Y do canto superior esquerdo do fundo do timer.
            font_size (int): Tamanho da fonte para o texto do timer.
            text_color (tuple): Cor do texto do timer (R, G, B).
            bg_color (tuple): Cor do fundo semi-transparente (R, G, B, Alpha).
            border_color (tuple): Cor da borda do fundo.
            border_radius (int): Raio da borda arredondada do fundo.
        """
        pygame.font.init() # Garante que o módulo de fonte está inicializado
        self.fonte = pygame.font.Font(None, font_size)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_radius = border_radius
        # Inicializa fundo_rect como None ou um valor padrão se necessário,
        # mas ele será calculado corretamente na primeira chamada de desenhar.
        self.fundo_rect = None # Inicializa para evitar o AttributeError na primeira verificação


    def desenhar(self, janela: pygame.Surface, tempo_decorrido_segundos: int):
        """
        Desenha o timer na superfície da janela.

        Args:
            janela (pygame.Surface): A superfície onde desenhar o timer.
            tempo_decorrido_segundos (int): O tempo decorrido em segundos.
        """
        minutos, segundos = divmod(tempo_decorrido_segundos, 60)
        tempo_txt = f"{minutos:02}:{segundos:02}"

        # Renderiza o texto do timer
        render_texto = self.fonte.render(tempo_txt, True, self.text_color)

        # >>> CORREÇÃO: Crie e atribua self.fundo_rect ANTES de usá-lo <<<
        # Cria o retângulo para o fundo com base no tamanho do texto renderizado
        self.fundo_rect = pygame.Rect(self.pos_x, self.pos_y, render_texto.get_width() + 10, render_texto.get_height() + 10)


        # Calcula a posição centralizada do texto dentro da área do timer
        # Note que a posição do fundo é o ponto de referência (pos_x, pos_y)
        # Agora self.fundo_rect já existe e tem suas dimensões calculadas
        texto_x = self.pos_x + (self.fundo_rect.width - render_texto.get_width()) // 2
        texto_y = self.pos_y + (self.fundo_rect.height - render_texto.get_height()) // 2

        # Cria e desenha o fundo semi-transparente
        fundo_surface = pygame.Surface(self.fundo_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(fundo_surface, self.bg_color, fundo_surface.get_rect(), border_radius=self.border_radius)
        pygame.draw.rect(fundo_surface, self.border_color, fundo_surface.get_rect(), 2, border_radius=self.border_radius)

        # Desenha o fundo e o texto na janela principal
        janela.blit(fundo_surface, (self.pos_x, self.pos_y))
        janela.blit(render_texto, (texto_x, texto_y))

