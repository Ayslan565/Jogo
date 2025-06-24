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

# --- Caminhos dos Recursos ---
# Certifique-se de que estes caminhos estão corretos na estrutura do seu projeto.
FONTE_RETRO_PATH = "Fontes/Retro Gaming.ttf"
IMAGEM_FUNDO_MENU_PATH = "Sprites/Menu/Menu.png"
MUSICAS_MENU = [
    "Musica/Menu/Faixa 1.mp3",
    "Musica/Menu/Faixa 2.mp3",
    "Musica/Menu/Faixa 3.mp3",
    "Musica/Menu/Faixa 4.mp3",
    "Musica/Menu/Faixa 5.mp3",
    "Musica/Menu/Faixa 6.mp3",
    "Musica/Menu/Faixa 7.mp3",
]

class Menu:
    """
    Classe para gerenciar e desenhar o menu principal do jogo.
    Utiliza botões desenhados via código.
    """
    def __init__(self, largura_tela, altura_tela):
        """
        Inicializa o objeto Menu.

        Args:
            largura_tela (int): Largura da janela do jogo.
            altura_tela (int): Altura da janela do jogo.
        """
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        pygame.font.init()

        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"AVISO: Erro ao inicializar o mixer de audio: {e}")

        self.espacamento_opcoes = 70
        self.espessura_contorno = 5
        self.fator_escala_hover = 1.1
        self.padding_texto_fundo_x = 10
        self.padding_texto_fundo_y = 5

        try:
            self.font = pygame.font.Font(FONTE_RETRO_PATH, 72)
            self.font_opcoes = pygame.font.Font(FONTE_RETRO_PATH, 36)
        except (FileNotFoundError, pygame.error) as e:
            print(f"AVISO: Fonte '{FONTE_RETRO_PATH}' não encontrada ou falhou ao carregar. Usando fonte padrão. Erro: {e}")
            self.font = pygame.font.Font(None, 72)
            self.font_opcoes = pygame.font.Font(None, 36)

        # Textos das opções do menu
        self.opcao_jogar_texto = "Jogar"
        self.opcao_opcoes_texto = "Opções"
        self.opcao_creditos_texto = "Creditos"
        self.opcao_sair_texto = "Sair"
        self.titulo_parte1_texto = "THE LEGEND OF "
        self.titulo_parte2_texto = "AZRAEL"

        self.titulo_parte1_render = self.font.render(self.titulo_parte1_texto, True, BRANCO)
        self.titulo_parte2_render = self.font.render(self.titulo_parte2_texto, True, AMARELO_SELECAO)
        
        # Define o tamanho do placeholder para os botões
        largura_placeholder = 300
        altura_placeholder = self.espacamento_opcoes - 20
        self.tamanho_fundo_original = (largura_placeholder, altura_placeholder)

        try:
            self.imagem = pygame.image.load(IMAGEM_FUNDO_MENU_PATH).convert()
            self.imagem = pygame.transform.scale(self.imagem, (self.largura_tela, self.altura_tela))
        except (pygame.error, FileNotFoundError) as e:
            print(f"ERRO: Imagem de fundo do menu '{IMAGEM_FUNDO_MENU_PATH}' não encontrada: {e}")
            self.imagem = pygame.Surface((self.largura_tela, self.altura_tela))
            self.imagem.fill(PRETO)

        self.opcoes = {
            "jogar": {"texto": self.opcao_jogar_texto, "cor_base": BRANCO, "cor_hover": AMARELO_SELECAO},
            "opcoes": {"texto": self.opcao_opcoes_texto, "cor_base": BRANCO, "cor_hover": AMARELO_SELECAO},
            "creditos": {"texto": self.opcao_creditos_texto, "cor_base": BRANCO, "cor_hover": AMARELO_SELECAO},
            "sair": {"texto": self.opcao_sair_texto, "cor_base": VERDE, "cor_hover": AMARELO_SELECAO},
        }
        
        # Gera os retângulos para cada opção, posicionando-os no canto inferior central
        num_opcoes = len(self.opcoes)
        # Define a posição Y central do último botão (mais abaixo) a 100 pixels da borda inferior
        y_centro_ultima_opcao = self.altura_tela - 100
        # Calcula a posição Y do centro do primeiro botão com base na posição do último
        y_inicial = y_centro_ultima_opcao - ((num_opcoes - 1) * self.espacamento_opcoes)

        for i, nome_opcao in enumerate(self.opcoes):
            rect = pygame.Rect(0, 0, self.tamanho_fundo_original[0], self.tamanho_fundo_original[1])
            # Posiciona cada botão com base na posição inicial e no espaçamento
            rect.center = (self.largura_tela // 2, y_inicial + i * self.espacamento_opcoes)
            self.opcoes[nome_opcao]["rect"] = rect

        self.rect_titulo_parte1 = self.titulo_parte1_render.get_rect()
        self.rect_titulo_parte2 = self.titulo_parte2_render.get_rect()

        self.musicas = MUSICAS_MENU
        self.musica_atual_index = -1
        self.tocar_proxima_musica()

    def desenhar(self, tela, mouse_pos):
        tela.blit(self.imagem, (0, 0))

        largura_total_titulo = self.rect_titulo_parte1.width + self.rect_titulo_parte2.width
        pos_titulo_x_inicial = (self.largura_tela - largura_total_titulo) // 2
        pos_titulo_y = 50

        self.rect_titulo_parte1.topleft = (pos_titulo_x_inicial, pos_titulo_y)
        self.rect_titulo_parte2.topleft = (self.rect_titulo_parte1.right, pos_titulo_y)

        tela.blit(self.titulo_parte1_render, self.rect_titulo_parte1)
        tela.blit(self.titulo_parte2_render, self.rect_titulo_parte2)

        for nome, dados in self.opcoes.items():
            rect_original = dados["rect"]
            
            # Desenha sempre o placeholder, pois a opção de imagem foi removida
            self.processar_opcao_desenho_placeholder(tela, mouse_pos, rect_original, PRETO, AZUL)

            cor_atual = dados["cor_hover"] if rect_original.collidepoint(mouse_pos) else dados["cor_base"]
            texto_render = self.font_opcoes.render(dados["texto"], True, cor_atual)
            texto_rect = texto_render.get_rect(center=rect_original.center)
            tela.blit(texto_render, texto_rect)

        pygame.display.update()

    def processar_opcao_desenho_placeholder(self, tela, mouse_pos, rect_fundo, cor_preenchimento, cor_contorno):
        centro_original = rect_fundo.center
        if rect_fundo.collidepoint(mouse_pos):
            tamanho = (int(self.tamanho_fundo_original[0] * self.fator_escala_hover),
                       int(self.tamanho_fundo_original[1] * self.fator_escala_hover))
        else:
            tamanho = self.tamanho_fundo_original
        
        rect_desenho = pygame.Rect((0,0), tamanho)
        rect_desenho.center = centro_original
        self.desenhar_contorno_placeholder(tela, rect_desenho, cor_preenchimento, cor_contorno, self.espessura_contorno)

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

    def tocar_proxima_musica(self):
        if not self.musicas: return
        
        novo_index = self.musica_atual_index
        if len(self.musicas) > 1:
            while novo_index == self.musica_atual_index:
                novo_index = random.randint(0, len(self.musicas) - 1)
        else:
            novo_index = 0

        self.musica_atual_index = novo_index
        musica_path = self.musicas[self.musica_atual_index]

        try:
            pygame.mixer.music.load(musica_path)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"ERRO: Falha ao carregar ou tocar música '{musica_path}': {e}")

    def parar_musica(self):
        pygame.mixer.music.stop()

    def verificar_click(self, x, y):
        mouse_pos = (x, y)
        for nome_opcao, dados in self.opcoes.items():
            if dados["rect"].collidepoint(mouse_pos):
                return nome_opcao
        return None

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
        menu.desenhar(tela, mouse_pos)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                acao = menu.verificar_click(*evento.pos)
                if acao:
                    print(f"Você clicou em: {acao}")
                    if acao == "sair":
                        rodando = False
                    elif acao == "creditos":
                        exibir_creditos(tela, clock)
                        menu.tocar_proxima_musica()
        
        if not pygame.mixer.music.get_busy() and rodando and menu.musicas:
             menu.tocar_proxima_musica()

        clock.tick(60)

    pygame.quit()
    sys.exit()
