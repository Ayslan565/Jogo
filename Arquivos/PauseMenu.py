# PauseMenu.py
import pygame
import sys

class PauseMenu:
    """
    Representa o menu de pausa do jogo.
    Permite ao jogador pausar o jogo e escolher entre continuar ou sair.
    """
    def __init__(self, largura_tela, altura_tela):
        """
        Inicializa o menu de pausa.

        Args:
            largura_tela (int): A largura da janela do jogo.
            altura_tela (int): A altura da janela do jogo.
        """
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        # Configurações visuais
        self.cor_fundo_overlay = (0, 0, 0, 150)  # Preto semi-transparente (RGBA)
        self.cor_texto_titulo = (255, 255, 255) # Branco
        self.cor_texto_botoes = (200, 200, 200) # Cinza claro
        self.cor_texto_botoes_hover = (255, 255, 255) # Branco (ao passar o mouse)
        self.cor_fundo_botoes = (50, 50, 50) # Cinza escuro
        self.cor_fundo_botoes_hover = (80, 80, 80) # Cinza um pouco mais claro

        # Fontes
        try:
            self.fonte_titulo = pygame.font.Font(None, 74) # Fonte padrão do Pygame, tamanho 74
            self.fonte_botoes = pygame.font.Font(None, 50) # Fonte padrão do Pygame, tamanho 50
        except pygame.error as e:
            print(f"DEBUG(PauseMenu): Erro ao carregar fonte padrão do Pygame: {e}")
            # Fallback para fonte do sistema si a fonte padrão falhar
            self.fonte_titulo = pygame.font.SysFont(None, 74)
            self.fonte_botoes = pygame.font.SysFont(None, 50)


        # Elementos do menu
        self.titulo = self.fonte_titulo.render("Jogo Pausado", True, self.cor_texto_titulo)
        self.rect_titulo = self.titulo.get_rect(center=(self.largura_tela // 2, self.altura_tela // 4))

        # Botões (texto e retângulos)
        self.texto_continuar = self.fonte_botoes.render("Continuar", True, self.cor_texto_botoes)
        self.rect_continuar = self.texto_continuar.get_rect(center=(self.largura_tela // 2, self.altura_tela // 2))

        self.texto_sair = self.fonte_botoes.render("Sair", True, self.cor_texto_botoes)
        self.rect_sair = self.texto_sair.get_rect(center=(self.largura_tela // 2, self.altura_tela // 2 + 70)) # 70 pixels abaixo do botão Continuar

        # Adiciona um pouco de padding aos retângulos dos botões para facilitar o clique/hover
        self.rect_continuar_padded = self.rect_continuar.inflate(20, 10) # Aumenta 20px na largura e 10px na altura
        self.rect_sair_padded = self.rect_sair.inflate(20, 10) # Aumenta 20px na largura e 10px na altura


        print("DEBUG(PauseMenu): Menu de Pausa inicializado.") # Debug inicialização


    def desenhar(self, janela, mouse_pos):
        """
        Desenha o menu de pausa na janela.

        Args:
            janela (pygame.Surface): A superfície da janela onde desenhar.
            mouse_pos (tuple): A posição atual do mouse (x, y).
        """
        # Desenha um overlay semi-transparente sobre a tela do jogo
        overlay = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        overlay.fill(self.cor_fundo_overlay)
        janela.blit(overlay, (0, 0))

        # Desenha o título
        janela.blit(self.titulo, self.rect_titulo)

        # Desenha os botões, verificando o hover para mudar a cor
        # Desenha o fundo do botão (opcional, mas melhora a visualização)
        if self.rect_continuar_padded.collidepoint(mouse_pos):
            pygame.draw.rect(janela, self.cor_fundo_botoes_hover, self.rect_continuar_padded, border_radius=5) # Fundo mais claro no hover
            texto_continuar_render = self.fonte_botoes.render("Continuar", True, self.cor_texto_botoes_hover) # Texto branco no hover
        else:
            pygame.draw.rect(janela, self.cor_fundo_botoes, self.rect_continuar_padded, border_radius=5) # Fundo escuro normal
            texto_continuar_render = self.texto_continuar # Texto cinza claro normal

        if self.rect_sair_padded.collidepoint(mouse_pos):
            pygame.draw.rect(janela, self.cor_fundo_botoes_hover, self.rect_sair_padded, border_radius=5) # Fundo mais claro no hover
            texto_sair_render = self.fonte_botoes.render("Sair", True, self.cor_texto_botoes_hover) # Texto branco no hover
        else:
            pygame.draw.rect(janela, self.cor_fundo_botoes, self.rect_sair_padded, border_radius=5) # Fundo escuro normal
            texto_sair_render = self.texto_sair # Texto cinza claro normal


        # Desenha o texto dos botões
        janela.blit(texto_continuar_render, self.rect_continuar)
        janela.blit(texto_sair_render, self.rect_sair)


    def handle_event(self, evento):
        """
        Processa eventos para o menu de pausa.

        Args:
            evento (pygame.event.Event): O evento a ser processado.

        Returns:
            str or None: Ação a ser tomada ('continuar', 'sair') ou None si nenhum botão foi clicado.
        """
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: # Botão esquerdo do mouse
                mouse_pos = evento.pos
                # Verifica si o clique foi no botão Continuar
                if self.rect_continuar_padded.collidepoint(mouse_pos):
                    print("DEBUG(PauseMenu): Botão 'Continuar' clicado.") # Debug clique
                    return 'continuar'
                # Verifica si o clique foi no botão Sair
                if self.rect_sair_padded.collidepoint(mouse_pos):
                    print("DEBUG(PauseMenu): Botão 'Sair' clicado.") # Debug clique
                    return 'sair'

        # Permite sair do menu de pausa pressionando ESC também
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                print("DEBUG(PauseMenu): Tecla ESC pressionada no menu de pausa. Retornando 'continuar'.") # Debug tecla ESC
                return 'continuar' # Retorna para o jogo ao pressionar ESC no menu de pausa

        return None # Retorna None si nenhum botão foi clicado ou evento relevante ocorreu
