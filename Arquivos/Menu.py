import pygame
import sys
import os
import random

# Importa a função de créditos
from Creditos import exibir_creditos

# --- Constantes ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO_SELECAO = (255, 255, 0)
VERMELHO = (255, 0, 0)
CINZA_ESCURO = (50, 50, 50)
CINZA_CLARO = (80, 80, 80)

# --- Caminhos dos Recursos ---
FONTE_RETRO_PATH = "Fontes/Retro Gaming.ttf"
IMAGEM_FUNDO_MENU_PATH = "Sprites/Menu/Menu.png"
MUSICAS_MENU = [
    os.path.join("Musica", "Menu", "Faixa 1.mp3"),
    os.path.join("Musica", "Menu", "Faixa 2.mp3"),
    os.path.join("Musica", "Menu", "Faixa 3.mp3"),
    os.path.join("Musica", "Menu", "Faixa 4.mp3"),
    os.path.join("Musica", "Menu", "Faixa 5.mp3"),
    os.path.join("Musica", "Menu", "Faixa 6.mp3"),
    os.path.join("Musica", "Menu", "Faixa 7.mp3"),
]

class Slider:
    """Cria um controle deslizante para ajustar valores como volume."""
    def __init__(self, x, y, w, h, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.grabbed = False
        self.knob_radius = h // 2 + 5
        self.knob_rect = pygame.Rect(0, 0, self.knob_radius * 2, self.knob_radius * 2)
        self.update_knob_pos()

    def update_knob_pos(self):
        """Atualiza a posição do botão deslizante com base no valor atual."""
        if self.max_val == self.min_val:
            ratio = 0
        else:
            ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        self.knob_rect.center = (self.rect.x + ratio * self.rect.width, self.rect.centery)

    def handle_event(self, event):
        """Processa eventos de mouse para o controle deslizante."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.knob_rect.collidepoint(event.pos):
                self.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION and self.grabbed:
            new_x = max(self.rect.left, min(event.pos[0], self.rect.right))
            ratio = (new_x - self.rect.left) / self.rect.width
            self.val = self.min_val + ratio * (self.max_val - self.min_val)
            self.update_knob_pos()

    def draw(self, screen):
        """Desenha o controle deslizante na tela."""
        pygame.draw.rect(screen, CINZA_ESCURO, self.rect, border_radius=5)
        fill_width = (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, AMARELO_SELECAO, fill_rect, border_radius=5)
        pygame.draw.circle(screen, BRANCO, self.knob_rect.center, self.knob_radius)

class Menu:
    """
    Classe para gerenciar e desenhar o menu principal e a tela de opções.
    """
    def __init__(self, largura_tela, altura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.estado = "principal"  # Pode ser 'principal' ou 'opcoes'

        pygame.font.init()
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"AVISO: Erro ao inicializar o mixer de audio: {e}")

        # --- Configurações Visuais e de Fonte ---
        self.espacamento_opcoes = 70
        self.espessura_contorno = 5
        self.fator_escala_hover = 1.1
        try:
            self.font_titulo = pygame.font.Font(FONTE_RETRO_PATH, 72)
            self.font_opcoes = pygame.font.Font(FONTE_RETRO_PATH, 36)
            self.font_slider_label = pygame.font.Font(FONTE_RETRO_PATH, 28)
        except (FileNotFoundError, pygame.error) as e:
            print(f"AVISO: Fonte '{FONTE_RETRO_PATH}' não encontrada. Usando fonte padrão. Erro: {e}")
            self.font_titulo = pygame.font.Font(None, 72)
            self.font_opcoes = pygame.font.Font(None, 42)
            self.font_slider_label = pygame.font.Font(None, 32)
        
        # --- Imagem de Fundo ---
        try:
            self.imagem = pygame.image.load(IMAGEM_FUNDO_MENU_PATH).convert()
            self.imagem = pygame.transform.scale(self.imagem, (self.largura_tela, self.altura_tela))
        except (pygame.error, FileNotFoundError) as e:
            print(f"ERRO: Imagem de fundo '{IMAGEM_FUNDO_MENU_PATH}' não encontrada: {e}")
            self.imagem = pygame.Surface((self.largura_tela, self.altura_tela))
            self.imagem.fill(PRETO)
            
        # --- Configuração dos Elementos da UI ---
        self.setup_ui_principal()
        self.setup_ui_opcoes()

        # --- Música e Volume ---
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        self.musicas = MUSICAS_MENU
        self.musica_atual_index = -1
        self.tocar_proxima_musica() # Isso já chama self.atualizar_volumes()


    def setup_ui_principal(self):
        """Configura os botões do menu principal."""
        self.titulo_parte1_render = self.font_titulo.render("THE LEGEND OF ", True, BRANCO)
        self.titulo_parte2_render = self.font_titulo.render("ASRAHEL", True, AMARELO_SELECAO)
        self.rect_titulo_parte1 = self.titulo_parte1_render.get_rect()
        self.rect_titulo_parte2 = self.titulo_parte2_render.get_rect()

        largura_placeholder = 300
        altura_placeholder = self.espacamento_opcoes - 20
        self.tamanho_fundo_original = (largura_placeholder, altura_placeholder)

        self.opcoes = {
            "jogar": {"texto": "Jogar", "cor_base": BRANCO, "cor_hover": AMARELO_SELECAO},
            "opcoes": {"texto": "Opções", "cor_base": BRANCO, "cor_hover": AMARELO_SELECAO},
            "creditos": {"texto": "Créditos", "cor_base": BRANCO, "cor_hover": AMARELO_SELECAO},
            "sair": {"texto": "Sair", "cor_base": VERDE, "cor_hover": AMARELO_SELECAO},
        }

        num_opcoes = len(self.opcoes)
        y_centro_ultima_opcao = self.altura_tela - 100
        y_inicial = y_centro_ultima_opcao - ((num_opcoes - 1) * self.espacamento_opcoes)

        for i, nome_opcao in enumerate(self.opcoes):
            rect = pygame.Rect(0, 0, self.tamanho_fundo_original[0], self.tamanho_fundo_original[1])
            rect.center = (self.largura_tela // 2, y_inicial + i * self.espacamento_opcoes)
            self.opcoes[nome_opcao]["rect"] = rect

    def setup_ui_opcoes(self):
        """Configura a UI da tela de opções."""
        self.opcoes_titulo_render = self.font_titulo.render("Opções", True, BRANCO)
        self.opcoes_titulo_rect = self.opcoes_titulo_render.get_rect(center=(self.largura_tela // 2, self.altura_tela // 4))

        slider_width = 300
        slider_height = 20
        center_x = self.largura_tela // 2
        
        self.sliders = {
            "Música": Slider(center_x - slider_width // 2, self.altura_tela // 2 - 50, slider_width, slider_height, 0.0, 1.0, 0.5),
            "Efeitos (SFX)": Slider(center_x - slider_width // 2, self.altura_tela // 2 + 50, slider_width, slider_height, 0.0, 1.0, 0.5)
        }

        self.botao_voltar_rect = pygame.Rect(0, 0, 200, 60)
        self.botao_voltar_rect.center = (center_x, self.altura_tela // 2 + 150)

    def desenhar(self, tela, mouse_pos):
        """Desenha o estado atual do menu (principal ou opções)."""
        tela.blit(self.imagem, (0, 0))
        
        if self.estado == "principal":
            self.desenhar_principal(tela, mouse_pos)
        elif self.estado == "opcoes":
            self.desenhar_opcoes(tela, mouse_pos)

        pygame.display.update()

    def desenhar_principal(self, tela, mouse_pos):
        """Desenha os elementos do menu principal."""
        largura_total_titulo = self.rect_titulo_parte1.width + self.rect_titulo_parte2.width
        pos_titulo_x_inicial = (self.largura_tela - largura_total_titulo) // 2
        pos_titulo_y = 50
        self.rect_titulo_parte1.topleft = (pos_titulo_x_inicial, pos_titulo_y)
        self.rect_titulo_parte2.topleft = (self.rect_titulo_parte1.right, pos_titulo_y)

        tela.blit(self.titulo_parte1_render, self.rect_titulo_parte1)
        tela.blit(self.titulo_parte2_render, self.rect_titulo_parte2)

        for nome, dados in self.opcoes.items():
            self.desenhar_botao_principal(tela, mouse_pos, dados)

    def desenhar_botao_principal(self, tela, mouse_pos, dados_botao):
        """Desenha um botão do menu principal com seu estilo único."""
        rect_original = dados_botao["rect"]
        centro_original = rect_original.center
        
        is_hovered = rect_original.collidepoint(mouse_pos)
        
        tamanho = (int(self.tamanho_fundo_original[0] * self.fator_escala_hover),
                   int(self.tamanho_fundo_original[1] * self.fator_escala_hover)) if is_hovered else self.tamanho_fundo_original
        
        rect_desenho = pygame.Rect((0,0), tamanho)
        rect_desenho.center = centro_original
        
        self.desenhar_contorno_placeholder(tela, rect_desenho, PRETO, AZUL, self.espessura_contorno)

        cor_texto = dados_botao["cor_hover"] if is_hovered else dados_botao["cor_base"]
        texto_render = self.font_opcoes.render(dados_botao["texto"], True, cor_texto)
        texto_rect = texto_render.get_rect(center=rect_original.center)
        tela.blit(texto_render, texto_rect)

    def desenhar_opcoes(self, tela, mouse_pos):
        """Desenha a tela de opções."""
        # Overlay para escurecer o fundo
        overlay = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        tela.blit(overlay, (0, 0))
        
        tela.blit(self.opcoes_titulo_render, self.opcoes_titulo_rect)

        # Desenha sliders e rótulos
        for label, slider in self.sliders.items():
            slider.draw(tela)
            label_surf = self.font_slider_label.render(label, True, BRANCO)
            label_rect = label_surf.get_rect(center=(slider.rect.centerx, slider.rect.y - 30))
            tela.blit(label_surf, label_rect)
        
        # Desenha botão Voltar
        is_hovered = self.botao_voltar_rect.collidepoint(mouse_pos)
        bg_color = CINZA_CLARO if is_hovered else CINZA_ESCURO
        text_color = AMARELO_SELECAO if is_hovered else BRANCO
        pygame.draw.rect(tela, bg_color, self.botao_voltar_rect, border_radius=8)
        texto_voltar_surf = self.font_opcoes.render("Voltar", True, text_color)
        texto_voltar_rect = texto_voltar_surf.get_rect(center=self.botao_voltar_rect.center)
        tela.blit(texto_voltar_surf, texto_voltar_rect)

    def desenhar_contorno_placeholder(self, tela, rect, cor_preenchimento, cor_contorno, espessura):
        pygame.draw.rect(tela, cor_preenchimento, rect)
        pygame.draw.line(tela, cor_contorno, rect.topleft, rect.topright, espessura)
        pygame.draw.line(tela, cor_contorno, rect.bottomleft, rect.bottomright, espessura)
        largura_triangulo = int(rect.height * 0.6)
        p_topo_esq, p_base_esq = rect.topleft, rect.bottomleft
        p_ponta_esq = (rect.left - largura_triangulo, rect.centery)
        verts_esq = [p_topo_esq, p_base_esq, p_ponta_esq]
        p_topo_dir, p_base_dir = rect.topright, rect.bottomright
        p_ponta_dir = (rect.right + largura_triangulo, rect.centery)
        verts_dir = [p_topo_dir, p_base_dir, p_ponta_dir]
        pygame.draw.polygon(tela, cor_preenchimento, verts_esq)
        pygame.draw.polygon(tela, cor_preenchimento, verts_dir)
        pygame.draw.line(tela, cor_contorno, p_topo_esq, p_ponta_esq, espessura)
        pygame.draw.line(tela, cor_contorno, p_base_esq, p_ponta_esq, espessura)
        pygame.draw.line(tela, cor_contorno, p_topo_dir, p_ponta_dir, espessura)
        pygame.draw.line(tela, cor_contorno, p_base_dir, p_ponta_dir, espessura)

    def handle_event(self, event):
        """Processa um único evento, especialmente para os sliders."""
        if self.estado == 'opcoes':
            for slider in self.sliders.values():
                slider.handle_event(event)
            self.music_volume = self.sliders["Música"].val
            self.sfx_volume = self.sliders["Efeitos (SFX)"].val
            self.atualizar_volumes()

    def verificar_click(self, x, y):
        """Verifica cliques nos botões do estado atual."""
        mouse_pos = (x, y)
        if self.estado == "principal":
            for nome_opcao, dados in self.opcoes.items():
                if dados["rect"].collidepoint(mouse_pos):
                    if nome_opcao == "opcoes":
                        self.estado = "opcoes"
                        return None # Não retorna ação, apenas muda o estado
                    return nome_opcao
        elif self.estado == "opcoes":
            if self.botao_voltar_rect.collidepoint(mouse_pos):
                self.estado = "principal"
        return None

    def tocar_proxima_musica(self):
        if not self.musicas or not pygame.mixer.get_init(): return
        novo_index = self.musica_atual_index
        if len(self.musicas) > 1:
            while novo_index == self.musica_atual_index:
                novo_index = random.randint(0, len(self.musicas) - 1)
        else: novo_index = 0
        self.musica_atual_index = novo_index
        musica_path = self.musicas[self.musica_atual_index]
        try:
            pygame.mixer.music.load(musica_path)
            pygame.mixer.music.play(-1)
            self.atualizar_volumes()
        except pygame.error as e:
            print(f"ERRO: Falha ao tocar música '{musica_path}': {e}")

    def atualizar_volumes(self):
        """Aplica os valores de volume atuais."""
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(self.music_volume)
            # Para SFX, você precisaria gerenciar o volume de cada som individualmente
            # Ex: som_pulo.set_volume(self.sfx_volume)

    def parar_musica(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

if __name__ == "__main__":
    pygame.init()
    largura, altura = 1920, 1080
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Teste do Menu")
    clock = pygame.time.Clock()
    menu = Menu(largura, altura)
    rodando = True

    while rodando:
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            # Passa todos os eventos para o manipulador do menu
            menu.handle_event(evento)

            if evento.type == pygame.MOUSEBUTTONDOWN:
                acao = menu.verificar_click(*evento.pos)
                if acao:
                    print(f"Você clicou em: {acao}")
                    if acao == "sair":
                        rodando = False
                    elif acao == "creditos":
                        exibir_creditos(tela, clock)
                        menu.tocar_proxima_musica()
            
            # Permite voltar das opções com a tecla ESC
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                if menu.estado == 'opcoes':
                    menu.estado = 'principal'
        
        # Desenha o menu
        menu.desenhar(tela, mouse_pos)
        
        if not pygame.mixer.music.get_busy() and rodando and menu.musicas:
            menu.tocar_proxima_musica()

        clock.tick(60)

    pygame.quit()
    sys.exit()
