# C:\Users\aysla\Documents\Jogo_Asrahel\Jogo\Arquivos\Pause.py

import pygame
import sys
import os
import random

# Variáveis globais para os volumes (serão inicializadas e passadas pelo Game.py)
# Estes valores são padrões e podem ser sobrescritos pela instância de PauseMenuManager
current_music_volume = 0.5
current_sfx_volume = 0.5

# Caminho para a fonte arcade
# ATENÇÃO: VERIFIQUE SE ESTE CAMINHO E NOME DE ARQUIVO ESTÃO CORRETOS PARA SUA FONTE!
# O caminho deve ser relativo ao diretório onde o script Pause.py está,
# ou um caminho absoluto.
FONTE_ARCADE_PATH = "Fontes/Arcade.ttf" 

class PauseMenuManager:
    """
    Gerencia a exibição e interação dos menus de pausa e opções usando apenas Pygame.
    """
    def __init__(self, pygame_janela, largura_tela, altura_tela, main_game_loop_function, main_menu_function, initial_music_vol, initial_sfx_vol):
        self.pygame_janela = pygame_janela
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.main_game_loop_function = main_game_loop_function # Callback para reiniciar o jogo/loop principal
        self.main_menu_function = main_menu_function # Callback para voltar ao menu principal do jogo

        self.current_music_volume = initial_music_vol
        self.current_sfx_volume = initial_sfx_vol

        # Cores e fontes para o tema escuro (Pygame)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_GRAY = (200, 200, 200)
        self.DARK_BG = (44, 44, 44) # RGB para #2C2C2C
        self.TEXT_COLOR = (255, 255, 255)
        self.BUTTON_BG = (74, 74, 74) # RGB para #4A4A4A
        self.BUTTON_HOVER = (0, 122, 204) # RGB para #007ACC (Highlight Color)
        self.SLIDER_TRACK_COLOR = (85, 85, 85) # RGB para #555555
        self.SLIDER_KNOB_COLOR = (200, 200, 200) # LIGHT_GRAY
        self.SLIDER_HOVER_COLOR = (0, 122, 204) # HIGHLIGHT_COLOR

        # Fontes Pygame
        # Tenta carregar a fonte personalizada, caso contrário, usa a fonte padrão do Pygame
        try:
            # Constrói o caminho absoluto para a fonte, assumindo que Pause.py está em 'Arquivos'
            # e 'Fontes' está no mesmo nível que 'Arquivos' (dentro de 'Jogo')
            # Se a estrutura for diferente, ajuste este caminho.
            base_dir = os.path.dirname(os.path.abspath(__file__)) # Diretório de Pause.py (Arquivos)
            font_dir = os.path.join(os.path.dirname(base_dir), "Fontes") # Caminho para Jogo/Fontes
            arcade_font_full_path = os.path.join(font_dir, "Arcade.ttf") # Caminho completo para Arcade.ttf

            if os.path.exists(arcade_font_full_path):
                self.font_title = pygame.font.Font(arcade_font_full_path, 80)
                self.font_option = pygame.font.Font(arcade_font_full_path, 50)
                self.font_slider_label = pygame.font.Font(arcade_font_full_path, 30)
                print(f"DEBUG(PauseMenuManager): Fonte arcade carregada de: {arcade_font_full_path}")
            else: # Tenta o caminho original se o construído falhar (para retrocompatibilidade ou estrutura diferente)
                if os.path.exists(FONTE_ARCADE_PATH):
                    self.font_title = pygame.font.Font(FONTE_ARCADE_PATH, 80)
                    self.font_option = pygame.font.Font(FONTE_ARCADE_PATH, 50)
                    self.font_slider_label = pygame.font.Font(FONTE_ARCADE_PATH, 30)
                    print(f"DEBUG(PauseMenuManager): Fonte arcade carregada de (caminho original): {FONTE_ARCADE_PATH}")
                else:
                    self.font_title = pygame.font.Font(None, 80)
                    self.font_option = pygame.font.Font(None, 50)
                    self.font_slider_label = pygame.font.Font(None, 30)
                    print(f"DEBUG(PauseMenuManager): Aviso: Fonte arcade não encontrada em '{arcade_font_full_path}' ou '{FONTE_ARCADE_PATH}'. Usando fonte padrão.")
        except Exception as e:
            self.font_title = pygame.font.Font(None, 80)
            self.font_option = pygame.font.Font(None, 50)
            self.font_slider_label = pygame.font.Font(None, 30)
            print(f"DEBUG(PauseMenuManager): Erro ao carregar fonte arcade: {e}. Usando fonte padrão.")

        self.current_menu_state = "pause" # "pause" ou "options"
        self.action_result = None # Para armazenar a ação do menu ("resume", "options", "main_menu", "quit")

        # Variáveis para o slider de volume (Pygame)
        self.music_slider_rect = None
        self.music_slider_knob_rect = None
        self.sfx_slider_rect = None
        self.sfx_slider_knob_rect = None
        self.dragging_music_slider = False
        self.dragging_sfx_slider = False

        # Variáveis para os botões do menu de pausa (Pygame)
        self.pause_menu_buttons = {} # Dicionário para armazenar Rects dos botões
        self.options_back_button_rect = None # Rect para o botão "Voltar" no menu de opções

    def _draw_background_overlay(self):
        """Desenha uma sobreposição preta semi-transparente na janela Pygame."""
        s = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150)) # Preto com 150 de transparência (0-255)
        self.pygame_janela.blit(s, (0, 0))

    def show_menu(self):
        """
        Exibe o menu principal (pausa) e gerencia a transição para o menu de opções,
        tudo dentro da janela Pygame. Retorna a ação selecionada e os volumes.
        """
        # Pausa a música do jogo se estiver tocando
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

        self.action_result = None # Reseta a ação
        self.current_menu_state = "pause" # Começa no menu de pausa

        running_menu = True
        while running_menu:
            self._draw_background_overlay() 
            
            mouse_pos = pygame.mouse.get_pos() # Pega a posição do mouse uma vez por frame

            if self.current_menu_state == "pause":
                self._draw_pause_menu_elements(mouse_pos)
            elif self.current_menu_state == "options":
                self._draw_options_menu_elements(mouse_pos)

            pygame.display.flip() 
            pygame.time.Clock().tick(60) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.action_result = "quit"
                    running_menu = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_menu_state == "pause":
                            self.action_result = "resume"
                            running_menu = False
                        elif self.current_menu_state == "options":
                            self.current_menu_state = "pause" 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Botão esquerdo do mouse
                        if self.current_menu_state == "pause":
                            self._handle_pause_menu_click(event.pos)
                            if self.action_result is not None and self.action_result != "options": 
                                running_menu = False
                        elif self.current_menu_state == "options":
                            self._handle_options_menu_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    if self.current_menu_state == "options":
                        self._handle_options_menu_drag(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging_music_slider = False
                        self.dragging_sfx_slider = False
        
        if self.action_result == "resume":
            if pygame.mixer.music.get_busy(): # Só despausa se estava tocando
                 pygame.mixer.music.unpause()
        elif self.action_result == "main_menu" or self.action_result == "quit":
            pygame.mixer.music.stop() # Para a música completamente

        return self.action_result, self.current_music_volume, self.current_sfx_volume

    def _draw_pause_menu_elements(self, mouse_pos):
        """Desenha os elementos visuais do menu de pausa diretamente no Pygame."""
        title_text = self.font_title.render("PAUSADO", True, self.TEXT_COLOR)
        title_rect = title_text.get_rect(center=(self.largura_tela // 2, self.altura_tela // 4))
        self.pygame_janela.blit(title_text, title_rect)

        options = ["Continuar", "Opções", "Menu Principal", "Sair"]
        button_height = 60 # Altura do botão
        button_spacing = 20 # Espaçamento entre botões
        total_button_height = len(options) * button_height + (len(options) - 1) * button_spacing
        
        start_y = (self.altura_tela - total_button_height) // 2 + self.altura_tela // 10 # Desloca um pouco para baixo

        self.pause_menu_buttons.clear()

        for i, option_text in enumerate(options):
            button_rect = pygame.Rect(0, 0, 400, button_height) # Largura aumentada
            button_rect.center = (self.largura_tela // 2, start_y + i * (button_height + button_spacing))
            
            button_color = self.BUTTON_BG
            if button_rect.collidepoint(mouse_pos):
                button_color = self.BUTTON_HOVER
            
            pygame.draw.rect(self.pygame_janela, button_color, button_rect, border_radius=10)
            
            text_surface = self.font_option.render(option_text, True, self.TEXT_COLOR)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.pygame_janela.blit(text_surface, text_rect)
            
            self.pause_menu_buttons[option_text] = button_rect

    def _handle_pause_menu_click(self, mouse_pos):
        """Lida com cliques nos botões do menu de pausa."""
        for option, rect in self.pause_menu_buttons.items():
            if rect.collidepoint(mouse_pos):
                if option == "Continuar":
                    self.action_result = "resume"
                elif option == "Opções":
                    self.current_menu_state = "options"
                    self.action_result = "options" # Para que o loop principal não saia
                elif option == "Voltar ao Menu Principal":
                    self.action_result = "main_menu"
                elif option == "Sair":
                    self.action_result = "quit"
                break 

    def _draw_options_menu_elements(self, mouse_pos):
        """Desenha os elementos visuais do menu de opções diretamente no Pygame."""
        title_text = self.font_title.render("Opções", True, self.TEXT_COLOR)
        title_rect = title_text.get_rect(center=(self.largura_tela // 2, self.altura_tela // 4 - 50)) # Um pouco mais para cima
        self.pygame_janela.blit(title_text, title_rect)

        slider_width = 300 # Largura aumentada para os sliders
        slider_height = 25
        knob_radius = 12
        label_slider_spacing = 20 # Espaço entre o label e o slider
        slider_y_start = self.altura_tela // 2 - 50

        # Música
        music_label = self.font_slider_label.render("Música:", True, self.TEXT_COLOR)
        music_label_rect = music_label.get_rect(midright=(self.largura_tela // 2 - slider_width // 2 - label_slider_spacing, slider_y_start))
        self.pygame_janela.blit(music_label, music_label_rect)

        self.music_slider_rect = pygame.Rect(0, 0, slider_width, slider_height)
        self.music_slider_rect.midleft = (music_label_rect.right + label_slider_spacing, slider_y_start)
        pygame.draw.rect(self.pygame_janela, self.SLIDER_TRACK_COLOR, self.music_slider_rect, border_radius=5)

        music_knob_x = self.music_slider_rect.x + (self.music_slider_rect.width * self.current_music_volume)
        self.music_slider_knob_rect = pygame.Rect(0, 0, knob_radius * 2, knob_radius * 2)
        self.music_slider_knob_rect.center = (music_knob_x, self.music_slider_rect.centery)
        
        knob_color_music = self.SLIDER_KNOB_COLOR
        if self.music_slider_knob_rect.collidepoint(mouse_pos) or self.dragging_music_slider:
            knob_color_music = self.SLIDER_HOVER_COLOR
        pygame.draw.circle(self.pygame_janela, knob_color_music, self.music_slider_knob_rect.center, knob_radius)

        # Efeitos Sonoros
        sfx_y_pos = slider_y_start + 70
        sfx_label = self.font_slider_label.render("Efeitos:", True, self.TEXT_COLOR)
        sfx_label_rect = sfx_label.get_rect(midright=(self.largura_tela // 2 - slider_width // 2 - label_slider_spacing, sfx_y_pos))
        self.pygame_janela.blit(sfx_label, sfx_label_rect)

        self.sfx_slider_rect = pygame.Rect(0, 0, slider_width, slider_height)
        self.sfx_slider_rect.midleft = (sfx_label_rect.right + label_slider_spacing, sfx_y_pos)
        pygame.draw.rect(self.pygame_janela, self.SLIDER_TRACK_COLOR, self.sfx_slider_rect, border_radius=5)

        sfx_knob_x = self.sfx_slider_rect.x + (self.sfx_slider_rect.width * self.current_sfx_volume)
        self.sfx_slider_knob_rect = pygame.Rect(0, 0, knob_radius * 2, knob_radius * 2)
        self.sfx_slider_knob_rect.center = (sfx_knob_x, self.sfx_slider_rect.centery)

        knob_color_sfx = self.SLIDER_KNOB_COLOR
        if self.sfx_slider_knob_rect.collidepoint(mouse_pos) or self.dragging_sfx_slider:
            knob_color_sfx = self.SLIDER_HOVER_COLOR
        pygame.draw.circle(self.pygame_janela, knob_color_sfx, self.sfx_slider_knob_rect.center, knob_radius)

        # Botão Voltar
        back_button_rect = pygame.Rect(0, 0, 200, 50) # Tamanho ajustado
        back_button_rect.center = (self.largura_tela // 2, sfx_y_pos + 100)
        
        button_color_back = self.BUTTON_BG
        if back_button_rect.collidepoint(mouse_pos):
            button_color_back = self.BUTTON_HOVER
        
        pygame.draw.rect(self.pygame_janela, button_color_back, back_button_rect, border_radius=10)
        
        back_text_surface = self.font_option.render("Voltar", True, self.TEXT_COLOR)
        back_text_rect = back_text_surface.get_rect(center=back_button_rect.center)
        self.pygame_janela.blit(back_text_surface, back_text_rect)
        self.options_back_button_rect = back_button_rect

    def _handle_options_menu_click(self, mouse_pos):
        """Lida com cliques nos elementos do menu de opções."""
        if self.music_slider_knob_rect and self.music_slider_knob_rect.collidepoint(mouse_pos): # Verifica se rect existe
            self.dragging_music_slider = True
            # Ajusta o volume imediatamente ao clicar no knob
            self._handle_options_menu_drag(mouse_pos) 
        elif self.sfx_slider_knob_rect and self.sfx_slider_knob_rect.collidepoint(mouse_pos): # Verifica se rect existe
            self.dragging_sfx_slider = True
            # Ajusta o volume imediatamente ao clicar no knob
            self._handle_options_menu_drag(mouse_pos)
        elif self.options_back_button_rect and self.options_back_button_rect.collidepoint(mouse_pos): # Verifica se rect existe
            self.current_menu_state = "pause" 

    def _handle_options_menu_drag(self, mouse_pos):
        """Lida com o arrasto dos sliders de volume."""
        if self.dragging_music_slider and self.music_slider_rect: # Verifica se rect existe
            new_knob_x = max(self.music_slider_rect.x, min(mouse_pos[0], self.music_slider_rect.right))
            self.current_music_volume = (new_knob_x - self.music_slider_rect.x) / self.music_slider_rect.width
            self.set_music_volume(self.current_music_volume)
        elif self.dragging_sfx_slider and self.sfx_slider_rect: # Verifica se rect existe
            new_knob_x = max(self.sfx_slider_rect.x, min(mouse_pos[0], self.sfx_slider_rect.right))
            self.current_sfx_volume = (new_knob_x - self.sfx_slider_rect.x) / self.sfx_slider_rect.width
            self.set_sfx_volume(self.current_sfx_volume)

    def set_music_volume(self, volume):
        """Define o volume global da música e aplica-o ao mixer do Pygame."""
        self.current_music_volume = max(0.0, min(1.0, volume)) # Garante que o volume está entre 0 e 1
        pygame.mixer.music.set_volume(self.current_music_volume)

    def set_sfx_volume(self, volume):
        """Define o volume global dos efeitos sonoros."""
        self.current_sfx_volume = max(0.0, min(1.0, volume)) # Garante que o volume está entre 0 e 1
        # A aplicação real do volume dos SFX dependerá de como você gerencia
        # e reproduz os sons no seu jogo (ex: cada Sound object pode ter seu volume ajustado).
        # print(f"DEBUG(PauseMenuManager): Volume SFX definido para: {self.current_sfx_volume:.2f}")


# Exemplo de uso (para testar o arquivo em isolamento)
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init() # Inicializa o mixer para música

    # Tenta obter as dimensões da tela cheia, ou usa um padrão
    try:
        info = pygame.display.Info()
        largura_tela = info.current_w
        altura_tela = info.current_h
        janela = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN | pygame.SCALED)
    except pygame.error: # Fallback para caso FULLSCREEN não seja suportado (ex: alguns ambientes virtuais)
        largura_tela = 1280
        altura_tela = 720
        janela = pygame.display.set_mode((largura_tela, altura_tela), pygame.RESIZABLE | pygame.SCALED)

    pygame.display.set_caption("Teste de Pausa (Pygame-only)")

    # Carrega uma música de exemplo para testar o volume
    # Crie uma pasta 'Musica/Gameplay' no mesmo nível que 'Arquivos' e coloque 'Faixa 1.mp3' lá.
    try:
        music_path_test = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Musica", "Gameplay", "Faixa 1.mp3")
        if os.path.exists(music_path_test):
            pygame.mixer.music.load(music_path_test) 
            pygame.mixer.music.play(-1) # Toca em loop
            pygame.mixer.music.set_volume(current_music_volume) # Define o volume inicial
            print(f"Música de teste '{music_path_test}' carregada e tocando.")
        else:
            print(f"Música de teste não encontrada em '{music_path_test}'.")
    except pygame.error as e:
        print(f"Erro ao carregar música de teste: {e}. O teste de volume da música não funcionará.")

    def dummy_game_loop():
        print("Retomando o loop do jogo (dummy)...")
        pass

    def dummy_main_menu():
        print("Voltando ao menu principal (dummy)...")
        pass

    janela.fill((50, 50, 150)) 
    pygame.display.flip()
    print("Jogo em execução (simulado). Pressione ESC para pausar.")

    # Cria a instância do gerenciador de menu
    pause_manager = PauseMenuManager(janela, largura_tela, altura_tela, dummy_game_loop, dummy_main_menu, current_music_volume, current_sfx_volume)

    running = True
    game_paused = False # Para controlar o estado de pausa no loop de teste

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not game_paused: # Se o jogo não está pausado, pausa e mostra o menu
                        print("ESC pressionado. Chamando menu de pausa.")
                        game_paused = True
                        # Salva o estado atual da tela para desenhar por baixo do overlay
                        game_screen_capture = janela.copy() 
                        
                        action, music_vol, sfx_vol = pause_manager.show_menu()
                        
                        # Atualiza os volumes globais (se necessário no seu jogo principal)
                        current_music_volume = music_vol
                        current_sfx_volume = sfx_vol
                        # O volume da música já é ajustado dentro do PauseMenuManager

                        if action == "resume":
                            print("Ação: Continuar")
                            game_paused = False
                        elif action == "main_menu":
                            print("Ação: Voltar ao Menu Principal")
                            # No jogo real, aqui você chamaria a função que reinicia o menu principal
                            # dummy_main_menu() 
                            running = False # Para este teste, sair do loop
                        elif action == "quit":
                            print("Ação: Sair")
                            running = False
                        else: # Se o menu foi fechado de outra forma (ex: clicando fora), retoma
                            game_paused = False
                    else: # Se já estava pausado e ESC é pressionado novamente (pode ser tratado pelo show_menu)
                        pass 
            
            if not game_paused:
                # Simula a atualização do jogo quando não está pausado
                janela.fill((random.randint(0,50), random.randint(0,50), random.randint(100,200)))
                # Adicione aqui o desenho do seu jogo real quando não estiver pausado
                test_text = pause_manager.font_option.render("Jogo Rodando...", True, pause_manager.WHITE)
                janela.blit(test_text, (50,50))

            pygame.display.flip()
            pygame.time.Clock().tick(30) # Limita o FPS do loop de teste

    pygame.quit()
    sys.exit()
