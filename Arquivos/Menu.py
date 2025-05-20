# menu.py
import pygame
import sys
import os # Importa os para ajudar a verificar o caminho
import random # Importa random para tocar músicas aleatoriamente

# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255) # Cor azul original
VERDE = (0, 255, 0)
AMARELO_SELECAO = (255, 255, 0) # Cor para indicar seleção (opcional)
CINZA_FUNDO_OPCAO = (100, 100, 100) # Cor para o fundo da opção (se a imagem não carregar) - Mantido para a função desenhar_contorno_placeholder, mas não usado para preenchimento principal
VERMELHO = (255, 255, 0) # Cor vermelha para "ASHAEL"

# Nome do arquivo da fonte retro. Certifique-se de que este arquivo está na pasta correta!
# Você pode baixar a fonte "Retro Gaming.ttf" ou "Press Start 2P" de sites como Google Fonts.
# Lembre-se de que este caminho é RELATIVO ao diretório de onde você executa o script principal.
FONTE_RETRO_PATH = "Fontes\Retro Gaming.ttf" # <--- VERIFIQUE ESTE CAMINHO!

# Nome do arquivo da imagem de fundo para as opções de menu
IMAGEM_FUNDO_OPCAO_PATH = "Sprites/Menu/botao_menu.png" # <--- COLOQUE O CAMINHO CORRETO PARA A IMAGEM DO SEU BOTÃO AQUI

# Nome do arquivo da imagem de fundo principal do menu
IMAGEM_FUNDO_MENU_PATH = "Sprites/Menu/Menu.png" # <--- COLOQUE O CAMINHO CORRETO PARA A IMAGEM DE FUNDO DO MENU

# >>> LISTA DE ARQUIVOS DE MÚSICA PARA O MENU <<<
# Certifique-se de que esses arquivos existam e os caminhos estejam corretos!
# Formatos comuns incluem .mp3, .ogg, .wav
# Caminhos atualizados com base na sua solicitação, usando barras normais
MUSICAS_MENU = [
    "Musica/Menu/Faixa 1.mp3",  # Exemplo de caminho
    "Musica/Menu/Faixa 2.mp3",  # Exemplo de caminho
    "Musica/Menu/Faixa 3.mp3",  # Exemplo de caminho
    # Adicione mais caminhos de música aqui conforme necessário
]


# Classe Menu
class Menu:
    """
    Classe para gerenciar e desenhar o menu principal do jogo.
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
        # Inicializa a fonte.
        pygame.font.init() # Garante que o módulo de fonte está inicializado

        # >>> INICIALIZA O MIXER DE ÁUDIO <<<
        # É importante inicializar o mixer antes de carregar qualquer som ou música
        try:
            pygame.mixer.init()
            print("Menu: Mixer de audio inicializado com sucesso.")
        except pygame.error as e:
            print(f"Menu: Erro ao inicializar o mixer de audio: {e}")
            # Continue mesmo se o mixer falhar, mas a música não funcionará


        # >>> DEFINE O ESPACAMENTO VERTICAL ENTRE AS OPÇÕES AQUI <<<
        self.espacamento_opcoes = 70 # Espaço vertical entre os itens

        # Define a espessura do contorno para os placeholders (ajustado para aspecto pixel art)
        self.espessura_contorno = 5 # Aumentado para dar um aspecto mais "pixelado"

        # Define o fator de escala para o efeito hover
        self.fator_escala_hover = 1.1 # Aumenta em 10% ao passar o mouse

        # Define o padding para o fundo do texto (mantido, mas não usado para desenhar o fundo)
        self.padding_texto_fundo_x = 10 # Padding horizontal
        self.padding_texto_fundo_y = 5  # Padding vertical


        # >>> ESTE É O LUGAR ONDE A FONTE DO MENU É CARREGADA <<<
        # Tenta carregar a fonte retro, usa fonte padrão como fallback.
        try:
            # Tenta carregar a fonte retro
            self.font = pygame.font.Font(FONTE_RETRO_PATH, 72) # Ajuste o tamanho (72 para o título) conforme necessário
            self.font_opcoes = pygame.font.Font(FONTE_RETRO_PATH, 36) # Fonte menor para as opções
            print(f"Menu: Fonte retro '{FONTE_RETRO_PATH}' carregada com sucesso.")
        except FileNotFoundError:
            # Captura especificamente o erro de arquivo não encontrado
            print(f"Menu: Erro: Arquivo da fonte retro não encontrado em '{FONTE_RETRO_PATH}'.")
            print(f"Menu: Diretorio de trabalho atual: {os.getcwd()}") # Imprime o diretório de trabalho para ajudar na depuração
            print("Menu: Usando a fonte padrão do Pygame como fallback.")
            self.font = pygame.font.Font(pygame.font.get_default_font(), 72) # Usa fonte padrão para título
            self.font_opcoes = pygame.font.Font(pygame.font.get_default_font(), 36) # Usa fonte padrão para opções
        except pygame.error as e:
            # Captura outros erros de carregamento de fonte do Pygame
            print(f"Menu: Erro do Pygame ao carregar a fonte retro: {FONTE_RETRO_PATH}.")
            print(f"Menu: Detalhes do erro: {e}")
            print("Menu: Usando a fonte padrão do Pygame como fallback.")
            self.font = pygame.font.Font(pygame.font.get_default_font(), 72) # Usa fonte padrão para título
            self.font_opcoes = pygame.font.Font(pygame.font.get_default_font(), 36) # Usa fonte padrão para opções
        except Exception as e:
            # Captura quaisquer outros erros inesperados
            print(f"Menu: Ocorreu um erro inesperado ao carregar a fonte: {e}")
            print("Menu: Usando a fonte padrão do Pygame como fallback.")
            self.font = pygame.font.Font(pygame.font.get_default_font(), 72) # Usa fonte padrão para título
            self.font_opcoes = pygame.font.Font(pygame.font.get_default_font(), 36) # Usa fonte padrão para opções


        # Define os textos das opções de menu
        self.opcao_jogar_texto = "Jogar"
        self.opcao_carregar_texto = "Carregar"
        self.opcao_opcoes_texto = "Opções"
        self.opcao_creditos_texto = "Creditos"
        self.opcao_sair_texto = "Sair"
        self.titulo_parte1_texto = "A LENDA DE " # Primeira parte do título
        self.titulo_parte2_texto = "AZRAEL" # Segunda parte do título (em vermelho)


        # >>> RENDERIZA OS TEXTOS INICIALMENTE AQUI (ANTES DE OBTER OS RETÂNGULOS) <<<
        # As letras azuis agora serão brancas
        self.opcao_jogar_render = self.font_opcoes.render(self.opcao_jogar_texto, True, BRANCO) # Usando font_opcoes
        self.opcao_carregar_render = self.font_opcoes.render(self.opcao_carregar_texto, True, BRANCO) # Usando font_opcoes
        self.opcao_opcoes_render = self.font_opcoes.render(self.opcao_opcoes_texto, True, BRANCO) # Usando font_opcoes
        self.opcao_creditos_render = self.font_opcoes.render(self.opcao_creditos_texto, True, BRANCO) # Usando font_opcoes
        self.opcao_sair_render = self.font_opcoes.render(self.opcao_sair_texto, True, VERDE) # Mantido VERDE para Sair, usando font_opcoes

        # Renderiza as partes do título com cores diferentes
        self.titulo_parte1_render = self.font.render(self.titulo_parte1_texto, True, BRANCO) # Primeira parte em BRANCO
        self.titulo_parte2_render = self.font.render(self.titulo_parte2_texto, True, VERMELHO) # Segunda parte em VERMELHO


        # >>> CARREGA A IMAGEM DE FUNDO PARA AS OPÇÕES DE MENU <<<
        # O cálculo do placeholder agora pode usar self.espacamento_opcoes
        try:
            self.imagem_fundo_opcao_original = pygame.image.load(IMAGEM_FUNDO_OPCAO_PATH).convert_alpha() # Use convert_alpha() para transparência
            # Opcional: Redimensionar a imagem de fundo da opção se necessário
            # self.imagem_fundo_opcao_original = pygame.transform.scale(self.imagem_fundo_opcao_original, (nova_largura, nova_altura))
            print(f"Menu: Imagem de fundo da opção '{IMAGEM_FUNDO_OPCAO_PATH}' carregada com sucesso.")
            self.usar_imagem_fundo = True # Flag para indicar que a imagem foi carregada
            self.tamanho_fundo_original = self.imagem_fundo_opcao_original.get_size() # Armazena o tamanho original
        except FileNotFoundError:
            # Captura especificamente o erro de arquivo não encontrado para a imagem
            print(f"Menu: Erro: Arquivo da imagem de fundo da opção não encontrado em '{IMAGEM_FUNDO_OPCAO_PATH}'.")
            print(f"Menu: Diretorio de trabalho atual: {os.getcwd()}") # Imprime o diretório de trabalho para ajudar na depuração
            print("Menu: Criando superficie de placeholder para o fundo da opção.")
            self.usar_imagem_fundo = False # Flag para indicar que a imagem NÃO foi carregada
            # Cria uma superfície de placeholder em caso de erro
            # Define um tamanho razoável para o placeholder, talvez baseado no tamanho do texto mais largo
            largura_placeholder = max(self.opcao_jogar_render.get_width(), self.opcao_carregar_render.get_width(),
                                      self.opcao_opcoes_render.get_width(), self.opcao_creditos_render.get_width(),
                                      self.opcao_sair_render.get_width()) + 40 # Adiciona um padding
            altura_placeholder = self.espacamento_opcoes - 20 # Altura baseada no espaçamento
            self.imagem_fundo_opcao_original = pygame.Surface((largura_placeholder, altura_placeholder), pygame.SRCALPHA)
            self.imagem_fundo_opcao_original.fill((CINZA_FUNDO_OPCAO[0], CINZA_FUNDO_OPCAO[1], CINZA_FUNDO_OPCAO[2], 0)) # Preenchimento transparente para placeholder


            self.tamanho_fundo_original = self.imagem_fundo_opcao_original.get_size() # Armazena o tamanho do placeholder original


        except pygame.error as e:
            print(f"Menu: Erro do Pygame ao carregar a imagem de fundo da opção: {IMAGEM_FUNDO_OPCAO_PATH}.")
            print(f"Menu: Detalhes do erro: {e}")
            print("Menu: Criando superficie de placeholder para o fundo da opção.")
            self.usar_imagem_fundo = False # Flag para indicar que a imagem NÃO foi carregada
            # Cria uma superfície de placeholder em caso de erro
            largura_placeholder = max(self.opcao_jogar_render.get_width(), self.opcao_carregar_render.get_width(),
                                      self.opcao_opcoes_render.get_width(), self.opcao_creditos_render.get_width(),
                                      self.opcao_sair_render.get_width()) + 40 # Adiciona um padding
            altura_placeholder = self.espacamento_opcoes - 20 # Altura baseada no espaçamento
            self.imagem_fundo_opcao_original = pygame.Surface((largura_placeholder, altura_placeholder), pygame.SRCALPHA)
            self.imagem_fundo_opcao_original.fill((CINZA_FUNDO_OPCAO[0], CINZA_FUNDO_OPCAO[1], CINZA_FUNDO_OPCAO[2], 0)) # Preenchimento transparente para placeholder

            self.tamanho_fundo_original = self.imagem_fundo_opcao_original.get_size() # Armazena o tamanho do placeholder original


        except Exception as e:
            print(f"Menu: Ocorreu um erro inesperado ao carregar a imagem de fundo da opção: {e}")
            print("Menu: Criando superficie de placeholder para o fundo da opção.")
            self.usar_imagem_fundo = False # Flag para indicar que a imagem NÃO foi carregada
            largura_placeholder = max(self.opcao_jogar_render.get_width(), self.opcao_carregar_render.get_width(),
                                      self.opcao_opcoes_render.get_width(), self.opcao_creditos_render.get_width(),
                                      self.opcao_sair_render.get_width()) + 40 # Adiciona um padding
            altura_placeholder = self.espacamento_opcoes - 20 # Altura baseada no espaçamento
            self.imagem_fundo_opcao_original = pygame.Surface((largura_placeholder, altura_placeholder), pygame.SRCALPHA)
            self.imagem_fundo_opcao_original.fill((CINZA_FUNDO_OPCAO[0], CINZA_FUNDO_OPCAO[1], CINZA_FUNDO_OPCAO[2], 0)) # Preenchimento transparente para placeholder

            self.tamanho_fundo_original = self.imagem_fundo_opcao_original.get_size() # Armazena o tamanho do placeholder original


        # Carrega e redimensiona a imagem de fundo do menu principal
        try:
            self.imagem = pygame.image.load(IMAGEM_FUNDO_MENU_PATH).convert() # Use convert() para otimizar
            # Redimensiona a imagem para cobrir a tela inteira
            self.imagem = pygame.transform.scale(self.imagem, (self.largura_tela, self.altura_tela))
            print(f"Menu: Imagem de fundo do menu principal '{IMAGEM_FUNDO_MENU_PATH}' carregada com sucesso.")
        except pygame.error as e:
            print(f"Menu: Erro ao carregar a imagem de fundo do menu principal: {e}")
            # Cria uma superfície de placeholder em caso de erro
            self.imagem = pygame.Surface((self.largura_tela, self.altura_tela))
            self.imagem.fill(PRETO) # Preenche com preto
            fonte_erro = pygame.font.Font(None, 50)
            texto_erro = fonte_erro.render("Erro ao carregar imagem de fundo principal", True, BRANCO)
            self.imagem.blit(texto_erro, (self.largura_tela // 2 - texto_erro.get_width() // 2, self.altura_tela // 2 - texto_erro.get_height() // 2))


        # Define os retângulos para as opções de menu para detecção de clique
        # AGORA OS RETÂNGULOS SÃO OBTIDOS DEPOIS QUE AS SUPERFÍCIES DE TEXTO SÃO RENDERIZADAS
        self.rect_jogar = self.opcao_jogar_render.get_rect()
        self.rect_carregar = self.opcao_carregar_render.get_rect()
        self.rect_opcoes = self.opcao_opcoes_render.get_rect()
        self.rect_creditos = self.opcao_creditos_render.get_rect()
        self.rect_sair = self.opcao_sair_render.get_rect()

        # Obtém os retângulos das partes do título
        self.rect_titulo_parte1 = self.titulo_parte1_render.get_rect()
        self.rect_titulo_parte2 = self.titulo_parte2_render.get_rect()


        # Posições base para centralizar as opções sobre a imagem
        # self.pos_base_y_opcoes = self.altura_tela // 2 # Posição anterior (centro vertical)

        # Define a margem inferior para a última opção (centro)
        margin_inferior_ultima_opcao = 50 # Distância do centro da última opção para a base da tela

        # Calcula a posição Y do centro da primeira opção
        # Posição Y da última opção (centro) = self.altura_tela - margin_inferior_ultima_opcao
        # Posição Y da primeira opção (centro) = Posição Y da última opção - (num_opcoes - 1) * espacamento_opcoes
        num_opcoes = 5
        y_centro_primeira_opcao = (self.altura_tela - margin_inferior_ultima_opcao) - (num_opcoes - 1) * self.espacamento_opcoes

        # Define a posição base Y para o grupo de opções (que é o centro da primeira opção)
        self.pos_base_y_opcoes_inferior = y_centro_primeira_opcao

        # >>> CRIA OS RETÂNGULOS PARA OS FUNDOS DAS OPÇÕES <<<
        # Estes retângulos serão usados para posicionar as imagens de fundo
        # Se a imagem foi carregada, usamos o tamanho dela. Se não, usamos o tamanho do placeholder.
        tamanho_fundo = self.imagem_fundo_opcao_original.get_size() # Usar original aqui
        self.rect_fundo_jogar = pygame.Rect((0, 0), tamanho_fundo)
        self.rect_fundo_carregar = pygame.Rect((0, 0), tamanho_fundo)
        self.rect_fundo_opcoes = pygame.Rect((0, 0), tamanho_fundo)
        self.rect_fundo_creditos = pygame.Rect((0, 0), tamanho_fundo)
        self.rect_fundo_sair = pygame.Rect((0, 0), tamanho_fundo)

        # >>> CARREGA E TOCA A MÚSICA DE FUNDO DO MENU <<<
        self.musicas = MUSICAS_MENU
        self.musica_atual_index = -1 # Começa com -1 para garantir que a primeira música tocada seja aleatória
        self.tocar_proxima_musica() # Toca a primeira música (aleatória) ao inicializar o menu


    def desenhar(self, tela, mouse_pos):
        """
        Desenha o menu na tela.

        Args:
            tela (pygame.Surface): A superfície onde desenhar o menu.
            mouse_pos (tuple): A posição (x, y) atual do mouse.
        """
        # Desenha a imagem de fundo principal primeiro
        tela.blit(self.imagem, (0, 0)) # Desenha a imagem cobrindo toda a tela

        # >>> POSIÇÃO E DESENHO DO TÍTULO <<<
        # Calcula a largura total do título combinado
        largura_total_titulo = self.rect_titulo_parte1.width + self.rect_titulo_parte2.width
        # Calcula a posição x inicial para centralizar o título
        pos_titulo_x_inicial = (self.largura_tela // 2) - (largura_total_titulo // 2)
        # Define a posição y do título (ajuste conforme necessário para o topo)
        pos_titulo_y = 50 # Distância do topo da tela

        # Define a posição da primeira parte do título
        self.rect_titulo_parte1.topleft = (pos_titulo_x_inicial, pos_titulo_y)
        # Define a posição da segunda parte do título (imediatamente após a primeira)
        self.rect_titulo_parte2.topleft = (self.rect_titulo_parte1.topright[0], pos_titulo_y)

        # Desenha as partes do título
        tela.blit(self.titulo_parte1_render, self.rect_titulo_parte1)
        tela.blit(self.titulo_parte2_render, self.rect_titulo_parte2)


        # Posições das opções de menu (centralizadas no campo inferior)
        # Calcula a posição Y inicial para o grupo de opções na parte inferior
        y_inicio_grupo_opcoes = self.pos_base_y_opcoes_inferior

        # Define a cor do fundo da opção (pode ser a cor do placeholder ou outra cor)
        cor_fundo_opcao = CINZA_FUNDO_OPCAO # Cor base para o fundo
        cor_contorno_opcao = AZUL # Cor do contorno alterada para AZUL

        # >>> POSICIONA, ESCALA E DESENHA OS FUNDOS E CONTORNOS <<<
        # Desenha os fundos ANTES dos textos para que fiquem por baixo

        # Processa "Jogar"
        self.rect_fundo_jogar.center = (self.largura_tela // 2, y_inicio_grupo_opcoes)
        if self.usar_imagem_fundo:
            self.processar_opcao_desenho_imagem(tela, mouse_pos, self.rect_fundo_jogar)
        else:
            self.processar_opcao_desenho_placeholder(tela, mouse_pos, self.rect_fundo_jogar, PRETO, cor_contorno_opcao) # Passa PRETO para preenchimento


        # Processa "Carregar"
        self.rect_fundo_carregar.center = (self.largura_tela // 2, y_inicio_grupo_opcoes + self.espacamento_opcoes)
        if self.usar_imagem_fundo:
            self.processar_opcao_desenho_imagem(tela, mouse_pos, self.rect_fundo_carregar)
        else:
            self.processar_opcao_desenho_placeholder(tela, mouse_pos, self.rect_fundo_carregar, PRETO, cor_contorno_opcao) # Passa PRETO para preenchimento

        # Processa "Opções"
        self.rect_fundo_opcoes.center = (self.largura_tela // 2, y_inicio_grupo_opcoes + 2 * self.espacamento_opcoes)
        if self.usar_imagem_fundo:
            self.processar_opcao_desenho_imagem(tela, mouse_pos, self.rect_fundo_opcoes)
        else:
            self.processar_opcao_desenho_placeholder(tela, mouse_pos, self.rect_fundo_opcoes, PRETO, cor_contorno_opcao) # Passa PRETO para preenchimento


        # Processa "Creditos"
        self.rect_fundo_creditos.center = (self.largura_tela // 2, y_inicio_grupo_opcoes + 3 * self.espacamento_opcoes)
        if self.usar_imagem_fundo:
            self.processar_opcao_desenho_imagem(tela, mouse_pos, self.rect_fundo_creditos)
        else:
            self.processar_opcao_desenho_placeholder(tela, mouse_pos, self.rect_fundo_creditos, PRETO, cor_contorno_opcao) # Passa PRETO para preenchimento


        # Processa "Sair"
        self.rect_fundo_sair.center = (self.largura_tela // 2, y_inicio_grupo_opcoes + 4 * self.espacamento_opcoes)
        if self.usar_imagem_fundo:
            self.processar_opcao_desenho_imagem(tela, mouse_pos, self.rect_fundo_sair)
        else:
            self.processar_opcao_desenho_placeholder(tela, mouse_pos, self.rect_fundo_sair, PRETO, cor_contorno_opcao) # Passa PRETO para preenchimento


        # Posições dos textos das opções (centralizadas sobre os fundos)
        # Os retângulos dos textos são posicionados no mesmo centro que os retângulos dos fundos
        # Estes retângulos são usados para detecção de colisão e posicionamento do texto renderizado dinamicamente
        self.rect_jogar.center = self.rect_fundo_jogar.center
        self.rect_carregar.center = self.rect_fundo_carregar.center
        self.rect_opcoes.center = self.rect_fundo_opcoes.center
        self.rect_creditos.center = self.rect_fundo_creditos.center
        self.rect_sair.center = self.rect_fundo_sair.center


        # Renderiza as opções com cores dinâmicas (ao passar o mouse)
        # As cores das opções ao passar o mouse continuam as mesmas (AMARELO_SELECAO)
        cor_jogar = AMARELO_SELECAO if self.rect_jogar.collidepoint(mouse_pos) else BRANCO # Cor base alterada para BRANCO
        cor_carregar = AMARELO_SELECAO if self.rect_carregar.collidepoint(mouse_pos) else BRANCO # Cor base alterada para BRANCO
        cor_opcoes = AMARELO_SELECAO if self.rect_opcoes.collidepoint(mouse_pos) else BRANCO # Cor base alterada para BRANCO
        cor_creditos = AMARELO_SELECAO if self.rect_creditos.collidepoint(mouse_pos) else BRANCO # Cor base alterada para BRANCO
        cor_sair = AMARELO_SELECAO if self.rect_sair.collidepoint(mouse_pos) else VERDE # Mantido VERDE para Sair


        # >>> RENDERIZA O TEXTO COM A FONTE (RETRO OU PADRÃO) E CORES DINÂMICAS <<<
        # Renderiza o texto dinamicamente com base na cor atual
        opcao_jogar_render_dinamico = self.font_opcoes.render(self.opcao_jogar_texto, True, cor_jogar)
        opcao_carregar_render_dinamico = self.font_opcoes.render(self.opcao_carregar_texto, True, cor_carregar)
        opcao_opcoes_render_dinamico = self.font_opcoes.render(self.opcao_opcoes_texto, True, cor_opcoes)
        opcao_creditos_render_dinamico = self.font_opcoes.render(self.opcao_creditos_texto, True, cor_creditos)
        opcao_sair_render_dinamico = self.font_opcoes.render(self.opcao_sair_texto, True, cor_sair)

        # >>> DESENHA O TEXTO (SEM FUNDO) <<<

        # Desenha texto para "Jogar"
        self.desenhar_texto_sem_fundo(tela, opcao_jogar_render_dinamico, self.rect_jogar.center)

        # Desenha texto para "Carregar"
        self.desenhar_texto_sem_fundo(tela, opcao_carregar_render_dinamico, self.rect_carregar.center)

        # Desenha texto para "Opções"
        self.desenhar_texto_sem_fundo(tela, opcao_opcoes_render_dinamico, self.rect_opcoes.center)

        # Desenha texto para "Creditos"
        self.desenhar_texto_sem_fundo(tela, opcao_creditos_render_dinamico, self.rect_creditos.center)

        # Desenha texto para "Sair"
        self.desenhar_texto_sem_fundo(tela, opcao_sair_render_dinamico, self.rect_sair.center)


        pygame.display.update() # Atualiza a tela para mostrar as mudanças

    def processar_opcao_desenho_imagem(self, tela, mouse_pos, rect_fundo):
        """
        Processa o desenho da imagem de fundo de uma única opção de menu,
        incluindo o efeito hover.

        Args:
            tela (pygame.Surface): A superfície onde desenhar.
            mouse_pos (tuple): A posição (x, y) atual do mouse.
            rect_fundo (pygame.Rect): O retângulo da imagem de fundo da opção.
        """
        if rect_fundo.collidepoint(mouse_pos):
            # Se estiver em hover, calcula o novo tamanho escalado
            novo_tamanho = (int(self.tamanho_fundo_original[0] * self.fator_escala_hover),
                            int(self.tamanho_fundo_original[1] * self.fator_escala_hover))
            imagem_escalada = pygame.transform.scale(self.imagem_fundo_opcao_original, novo_tamanho)
            rect_escalado = imagem_escalada.get_rect(center=rect_fundo.center)
            tela.blit(imagem_escalada, rect_escalado)

            # Atualiza o retângulo de colisão para a área escalada para detecção precisa do hover
            rect_fundo.size = novo_tamanho
            rect_fundo.center = rect_escalado.center # Mantém o centro original após o redimensionamento
        else:
            # Se não estiver em hover, usa o tamanho original
            tela.blit(self.imagem_fundo_opcao_original, rect_fundo)

            # Garante que o retângulo de colisão esteja no tamanho original quando não estiver em hover
            rect_fundo.size = self.tamanho_fundo_original
            # O centro já está correto pois não foi alterado no hover


    def processar_opcao_desenho_placeholder(self, tela, mouse_pos, rect_fundo, cor_preenchimento_placeholder, cor_contorno):
        """
        Processa o desenho do placeholder de fundo e contorno de uma única opção de menu,
        incluindo o efeito hover.

        Args:
            tela (pygame.Surface): A superfície onde desenhar.
            mouse_pos (tuple): A posição (x, y) atual do mouse.
            rect_fundo (pygame.Rect): O retângulo do placeholder de fundo da opção.
            cor_preenchimento_placeholder (tuple): A cor de preenchimento do placeholder (PRETO).
            cor_contorno (tuple): A cor do contorno.
        """
        if rect_fundo.collidepoint(mouse_pos):
            # Se estiver em hover, calcula o novo tamanho escalado
            novo_tamanho = (int(self.tamanho_fundo_original[0] * self.fator_escala_hover),
                            int(self.tamanho_fundo_original[1] * self.fator_escala_hover))
            # Cria um placeholder escalado (transparente)
            placeholder_escalado = pygame.Surface(novo_tamanho, pygame.SRCALPHA)
            # Não preenche o placeholder escalado
            rect_escalado = placeholder_escalado.get_rect(center=rect_fundo.center)
            # Não desenha o placeholder escalado preenchido

            # Desenha o contorno e triângulos para o placeholder escalado (apenas contorno)
            self.desenhar_contorno_placeholder(tela, rect_escalado, cor_preenchimento_placeholder, cor_contorno, self.espessura_contorno)

            # Atualiza o retângulo de colisão para a área escalada para detecção precisa do hover
            rect_fundo.size = novo_tamanho
            rect_fundo.center = rect_escalado.center # Mantém o centro original após o redimensionamento

        else:
            # Se não estiver em hover, usa o tamanho original
            # Não desenha o retângulo placeholder preenchido no tamanho original

            # Desenha o contorno e triângulos para o placeholder no tamanho original (apenas contorno)
            self.desenhar_contorno_placeholder(tela, rect_fundo, cor_preenchimento_placeholder, cor_contorno, self.espessura_contorno)

            # Garante que o retângulo de colisão esteja no tamanho original quando não estiver em hover
            rect_fundo.size = self.tamanho_fundo_original
            # O centro já está correto pois não foi alterado no hover


    def desenhar_contorno_placeholder(self, tela, rect_fundo, cor_preenchimento, cor_contorno, espessura_contorno):
        """
        Desenha o contorno do retângulo placeholder e dos triângulos laterais.
        Desenha o preenchimento (agora PRETO) e o contorno.

        Args:
            tela (pygame.Surface): A superfície onde desenhar.
            rect_fundo (pygame.Rect): O retângulo de referência para posicionar o contorno.
            cor_preenchimento (tuple): A cor de preenchimento dos triângulos e retângulo (agora PRETO).
            cor_contorno (tuple): A cor do contorno.
            espessura_contorno (int): A espessura do contorno.
        """
        # Desenha o retângulo placeholder preenchido (agora com cor_preenchimento, que será PRETO)
        pygame.draw.rect(tela, cor_preenchimento, rect_fundo)

        # Desenha as linhas de contorno superior e inferior do retângulo
        pygame.draw.line(tela, cor_contorno, rect_fundo.topleft, rect_fundo.topright, espessura_contorno)
        pygame.draw.line(tela, cor_contorno, rect_fundo.bottomleft, rect_fundo.bottomright, espessura_contorno)

        # Define a largura dos triângulos (ajustado para aspecto pixel art)
        # Pode ser um valor fixo ou baseado na altura do retângulo
        largura_triangulo = int(rect_fundo.height * 0.6) # Ajuste este fator para controlar a largura do triângulo


        # Vértices do triângulo da esquerda
        ponto_topo_esquerdo = (rect_fundo.left, rect_fundo.top)
        ponto_base_esquerdo = (rect_fundo.left, rect_fundo.bottom)
        ponto_ponta_esquerda = (rect_fundo.left - largura_triangulo, rect_fundo.centery)
        vertices_esquerdo = [ponto_topo_esquerdo, ponto_base_esquerdo, ponto_ponta_esquerda]

        # Vértices do triângulo da direita
        ponto_topo_direito = (rect_fundo.right, rect_fundo.top)
        ponto_base_direito = (rect_fundo.right, rect_fundo.bottom)
        ponto_ponta_direito = (rect_fundo.right + largura_triangulo, rect_fundo.centery)
        vertices_direito = [ponto_topo_direito, ponto_base_direito, ponto_ponta_direito]

        # Desenha os triângulos preenchidos (agora com cor_preenchimento, que será PRETO)
        pygame.draw.polygon(tela, cor_preenchimento, vertices_esquerdo)
        pygame.draw.polygon(tela, cor_preenchimento, vertices_direito)

        # >>> DESENHA O CONTORNO DOS TRIÂNGULOS (APENAS AS BORDAS EXTERNAS) <<<
        # Contorno do triângulo da esquerda (bordas superior e inferior inclinadas)
        pygame.draw.line(tela, cor_contorno, ponto_topo_esquerdo, ponto_ponta_esquerda, espessura_contorno)
        pygame.draw.line(tela, cor_contorno, ponto_base_esquerdo, ponto_ponta_esquerda, espessura_contorno)

        # Contorno do triângulo da direita (bordas superior e inferior inclinadas)
        pygame.draw.line(tela, cor_contorno, ponto_topo_direito, ponto_ponta_direito, espessura_contorno)
        pygame.draw.line(tela, cor_contorno, ponto_base_direito, ponto_ponta_direito, espessura_contorno)


    def desenhar_texto_sem_fundo(self, tela, texto_renderizado, centro_pos):
        """
        Desenha o texto renderizado centralizado, sem fundo.

        Args:
            tela (pygame.Surface): A superfície onde desenhar.
            texto_renderizado (pygame.Surface): A superfície com o texto já renderizado.
            centro_pos (tuple): A posição (x, y) onde centralizar o texto.
        """
        # Obtém o retângulo do texto renderizado e o centraliza
        rect_texto = texto_renderizado.get_rect(center=centro_pos)

        # Não cria nem desenha o fundo do texto

        # Desenha o texto na tela (centralizado)
        tela.blit(texto_renderizado, rect_texto)

    def tocar_proxima_musica(self):
        """Carrega e toca uma música aleatória da lista em loop."""
        if not self.musicas:
            print("Menu: Nenhuma música configurada para o menu.")
            return

        # Seleciona um índice aleatório
        novo_musica_index = random.randint(0, len(self.musicas) - 1)

        # Opcional: Evitar tocar a mesma música duas vezes seguidas se houver mais de uma música
        if len(self.musicas) > 1:
            while novo_musica_index == self.musica_atual_index:
                novo_musica_index = random.randint(0, len(self.musicas) - 1)

        self.musica_atual_index = novo_musica_index
        musica_path = self.musicas[self.musica_atual_index]

        # Adicionado print para depuração
        print(f"Menu: Tentando carregar música: {os.path.abspath(musica_path)}")

        try:
            pygame.mixer.music.load(musica_path)
            pygame.mixer.music.play(-1) # O -1 faz a música tocar em loop infinito
            print(f"Menu: Tocando música: {musica_path}")
        except pygame.error as e:
            print(f"Menu: Erro ao carregar ou tocar a música '{musica_path}': {e}")
            # Tenta tocar outra música aleatória se houver um erro
            if len(self.musicas) > 1:
                print("Menu: Tentando tocar outra música aleatória...")
                # Remove a música com erro da lista para não tentar novamente
                # Cuidado: Modificar a lista enquanto itera ou seleciona pode ser complicado.
                # Uma abordagem mais segura é apenas tentar outra música aleatória sem remover.
                # Se o erro persistir para todas as músicas, a mensagem final será exibida.
                self.tocar_proxima_musica() # Chama recursivamente para tentar outra música
            else:
                print("Menu: Nenhuma outra música disponível ou erro persistente.")


    def parar_musica(self):
        """Para a música que está tocando."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            print("Menu: Musica do menu parada.")


    def verificar_click(self, x, y):
        """
        Verifica se um clique do mouse ocorreu em uma das opções de menu.

        Args:
            x (int): Coordenada x do clique do mouse.
            y (int): Coordenada y do clique do mouse.

        Returns:
            str or None: Ação correspondente à opção clicada ("jogar", "carregar", "opcoes", "creditos", "sair"), ou None caso contrário.
        """
        mouse_pos = (x, y) # Converte as coordenadas para uma tupla

        # Verifica se o clique colidiu com o retângulo de cada opção (usando os retângulos dos fundos para uma área de clique maior)
        # Note que a detecção de clique usa o retângulo de fundo, que é redimensionado no hover
        if self.rect_fundo_jogar.collidepoint(mouse_pos):
            return "jogar"
        if self.rect_fundo_carregar.collidepoint(mouse_pos):
            return "carregar"
        if self.rect_fundo_opcoes.collidepoint(mouse_pos):
            return "opcoes"
        if self.rect_creditos.collidepoint(mouse_pos):
            return "creditos"
        if self.rect_sair.collidepoint(mouse_pos):
            return "sair"


        return None # Nenhuma opção clicada

# Código principal para teste
if __name__ == "__main__":
    pygame.init()
    # Define o tamanho da tela (usando as variáveis de largura/altura)
    largura, altura = 1920, 1080

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Teste do Menu")

    # Cria uma instância do Menu
    menu = Menu(largura, altura)

    rodando = True
    while rodando:
        mouse_pos = pygame.mouse.get_pos() # Obtém a posição do mouse para o efeito hover
        menu.desenhar(tela, mouse_pos) # Passa a posição do mouse para o método desenhar

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Passa as coordenadas do clique para verificar_click
                acao = menu.verificar_click(*evento.pos)
                if acao == "jogar":
                    print("Você clicou em Jogar!")
                    menu.parar_musica() # Para a música do menu ao iniciar o jogo
                    # Adicione sua lógica para iniciar o jogo principal aqui
                    pass
                elif acao == "carregar":
                    print("Você clicou em Carregar!")
                    # Adicione sua lógica para carregar o jogo aqui
                    pass
                elif acao == "opcoes":
                    print("Você clicou em Opções!")
                    # Adicione sua lógica para o menu de opções aqui
                    pass
                elif acao == "creditos":
                    print("Você clicou em Créditos!")
                    # Adicione sua lógica para a tela de créditos aqui
                    pass
                elif acao == "sair":
                    print("Saindo...")
                    menu.parar_musica() # Para a música do menu ao sair
                    rodando = False # Define rodando como False para sair do loop

        # Verifica se a música terminou e toca a próxima
        # Isso é útil se você não estiver usando loop infinito (-1 no play)
        # if not pygame.mixer.music.get_busy():
        #     menu.tocar_proxima_musica() # Toca a próxima música quando a atual terminar


        # Não precisa de pygame.display.update() ou flip() aqui, pois já está no menu.desenhar()
        # pygame.display.update() # Removido
        # pygame.time.Clock().tick(60) # Opcional: Controlar FPS no menu

    pygame.quit() # Finaliza o Pygame
    sys.exit() # Sai do script
