import pygame
import time

class PopupMensagem:
    def __init__(self, mensagem="Os ventos estão mudando", duracao=3.0, fonte_path=None):
        self.mensagem = mensagem
        self.duracao = duracao
        self.inicio = None
        self.fonte = pygame.font.Font(fonte_path, 60) if fonte_path else pygame.font.Font(None, 60)
        self.ativo = False

    def iniciar(self):
        self.inicio = time.time()
        self.ativo = True

    def desenhar(self, janela):
        if not self.ativo:
            return

        tempo_passado = time.time() - self.inicio
        if tempo_passado > self.duracao:
            self.ativo = False
            return

        largura, altura = janela.get_size()
        texto_surface = self.fonte.render(self.mensagem, True, (255, 255, 255))
        text_rect = texto_surface.get_rect(center=(largura // 2, altura // 2))

        padding_x, padding_y = 80, 40
        rect_w, rect_h = text_rect.width + padding_x, text_rect.height + padding_y
        rect_x, rect_y = largura // 2 - rect_w // 2, altura // 2 - rect_h // 2
        triangle = 30
        pontos = [
            (rect_x, rect_y),
            (rect_x + rect_w, rect_y),
            (rect_x + rect_w + triangle, rect_y + rect_h // 2),
            (rect_x + rect_w, rect_y + rect_h),
            (rect_x, rect_y + rect_h),
            (rect_x - triangle, rect_y + rect_h // 2)
        ]

        popup_surface = pygame.Surface((rect_w + 2 * triangle, rect_h), pygame.SRCALPHA)
        pygame.draw.polygon(
            popup_surface, (50, 50, 50, 230),
            [(p[0] - rect_x + triangle, p[1] - rect_y) for p in pontos]
        )
        popup_surface.blit(
            texto_surface,
            ((popup_surface.get_width() - text_rect.width) // 2,
             (popup_surface.get_height() - text_rect.height) // 2)
        )
        janela.blit(popup_surface, (rect_x - triangle, rect_y))


class ContagemRegressiva:
    def __init__(self, segundos=5, fonte_path=None):
        self.segundos = segundos
        self.inicio = None
        self.ativo = False
        self.fonte = pygame.font.Font(fonte_path, 160) if fonte_path else pygame.font.Font(None, 160)

    def iniciar(self):
        self.inicio = time.time()
        self.ativo = True

    def desenhar(self, janela):
        if not self.ativo:
            return

        tempo_passado = time.time() - self.inicio
        restante = max(0, self.segundos - int(tempo_passado))
        fade = 1 - (tempo_passado % 1)
        alpha = int(255 * fade)

        if restante <= 0:
            self.ativo = False
            return

        largura, altura = janela.get_size()
        texto = self.fonte.render(str(restante), True, (255, 255, 255))
        texto.set_alpha(alpha)
        x = (largura - texto.get_width()) // 2
        y = (altura - texto.get_height()) // 2

        bg_radius = max(texto.get_width(), texto.get_height()) // 2 + 60
        bg_surface = pygame.Surface((bg_radius * 2, bg_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(bg_surface, (20, 20, 30, 220), (bg_radius, bg_radius), bg_radius)
        bg_surface.set_alpha(alpha)

        janela.blit(bg_surface, (x + texto.get_width() // 2 - bg_radius, y + texto.get_height() // 2 - bg_radius))
        janela.blit(texto, (x, y))


def exibir_tela_loading(janela, clock, texto="Carregando...", fonte_path=None, duracao=2.0):
    largura, altura = janela.get_size()
    fonte = pygame.font.Font(fonte_path, 80) if fonte_path else pygame.font.Font(None, 80)
    inicio = time.time()
    while time.time() - inicio < duracao:
        janela.fill((20, 20, 30))
        texto_render = fonte.render(texto, True, (255, 255, 255))
        x = (largura - texto_render.get_width()) // 2
        y = (altura - texto_render.get_height()) // 2
        janela.blit(texto_render, (x, y))
        pygame.display.flip()
        clock.tick(60)


def pausar_elementos_jogo(contexto):
    """
    Pausa elementos do jogo (ex: inimigos, eventos climáticos), mas não o jogador.
    'contexto' pode ser o resultado de locals() do loop principal.
    """
    # Pausa o spawn de inimigos
    if 'gerenciador_inimigos' in contexto and contexto['gerenciador_inimigos']:
        contexto['gerenciador_inimigos'].pausar_spawn_normal(True)
    # Pausa eventos climáticos se existir
    if 'gerenciador_eventos' in contexto and contexto['gerenciador_eventos']:
        if hasattr(contexto['gerenciador_eventos'], 'pausar_eventos'):
            contexto['gerenciador_eventos'].pausar_eventos(True)

def despausar_elementos_jogo(contexto):
    """
    Despausa elementos do jogo (ex: inimigos, eventos climáticos), mas não o jogador.
    'contexto' pode ser o resultado de locals() do loop principal.
    """
    if 'gerenciador_inimigos' in contexto and contexto['gerenciador_inimigos']:
        contexto['gerenciador_inimigos'].pausar_spawn_normal(False)
    if 'gerenciador_eventos' in contexto and contexto['gerenciador_eventos']:
        if hasattr(contexto['gerenciador_eventos'], 'pausar_eventos'):
            contexto['gerenciador_eventos'].pausar_eventos(False)
