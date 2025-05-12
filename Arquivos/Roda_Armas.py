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
# Corrigindo o caminho para ser relativo ao diretório de trabalho, assumindo que Musicas está dentro de Arquivos
# Usando os.path.join para criar caminhos compatíveis com o sistema operativo
MUSICAS_MENU = [
    os.path.join("Arquivos", "Musicas", "musica_menu_1.ogg"),  # Exemplo de caminho corrigido
    os.path.join("Arquivos", "Musicas", "musica_menu_2.ogg"),  # Exemplo de caminho corrigido
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
            self.font = pygame.font.Font(FONTE_RETRO_PATH, 36) # Ajuste o tamanho (36) conforme necessário
            print(f"Menu: Fonte retro '{FONTE_RETRO_PATH}' carregada com sucesso.")
        except FileNotFoundError:
            # Captura especificamente o erro de arquivo não encontrado
            print(f"Menu: Erro: Arquivo da fonte retro não encontrado em '{FONTE_RETRO_PATH}'.")
            print(f"Menu: Diretorio de trabalho atual: {os.getcwd()}") # Imprime o diretório de trabalho para ajudar na depuração
            print("Menu: Usando a fonte padrão do Pygame como fallback.")
            self.font = pygame.font.Font(pygame.font.get_default_font(), 36) # Usa fonte padrão
        except pygame.error as e:
            # Captura outros erros de carregamento de fonte do Pygame
            print(f"Menu: Erro do Pygame ao carregar a fonte retro: {FONTE_RETRO_PATH}.")
            print(f"Menu: Detalhes do erro: {e}")
            print("Menu: Usando a fonte padrão do Pygame como fallback.")
            self.font = pygame.font.Font(pygame.font.get_default_font(), 36) # Usa fonte padrão
        except Exception as e:
            # Captura quaisquer outros erros inesperados
            print(f"Menu: Ocorreu um erro inesperado ao carregar a fonte: {e}")
            print("Menu: Usando a fonte padrão do Pygame como fallback.")
            self.font = pygame.font.Font(pygame.font.get_default_font(), 36) # Usa fonte padrão


        # Define os textos das opções de menu
        self.opcao_jogar_texto = "Jogar"
        self.opcao_carregar_texto = "Carregar"
        self.opcao_opcoes_texto = "Opções"
        self.opcao_creditos_texto = "Creditos"
        self.opcao_sair_texto = "Sair"
        # self.titulo_texto = "Tela Inicial" # Removido o texto do título

        # >>> RENDERIZA OS TEXTOS INICIALMENTE AQUI (ANTES DE OBTER OS RETÂNGULOS) <<<
        # As letras azuis agora serão brancas
        self.opcao_jogar_render = self.font.render(self.opcao_jogar_texto, True, BRANCO) # Cor alterada para BRANCO
        self.opcao_carregar_render = self.font.render(self.opcao_carregar_texto, True, BRANCO) # Cor alterada para BRANCO
        self.opcao_opcoes_render = self.font.render(self.opcao_opcoes_texto, True, BRANCO) # Cor alterada para BRANCO
        self.opcao_creditos_render = self.font.render(self.opcao_creditos_texto, True, BRANCO) # Cor alterada para BRANCO
        self.opcao_sair_render = self.font.render(self.opcao_sair_texto, True, VERDE) # Mantido VERDE para Sair
        # self.titulo_render = self.font.render(self.titulo_texto, True, BRANCO) # Removida a renderização do título

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
        # self.rect_titulo = self.titulo_render.get_rect() # Removido o retângulo do título


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

        # Posição do Título (opcional, pode ser em cima ou no centro)
        # Exemplo: Título no topo, centralizado
        # self.rect_titulo.center = (self.largura_tela // 2, 50) # Posição no topo (Removido)
        # tela.blit(self.titulo_render, self.rect_titulo) # Removido o desenho do título


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
        opcao_jogar_render_dinamico = self.font.render(self.opcao_jogar_texto, True, cor_jogar)
        opcao_carregar_render_dinamico = self.font.render(self.opcao_carregar_texto, True, cor_carregar)
        opcao_opcoes_render_dinamico = self.font.render(self.opcao_opcoes_texto, True, cor_opcoes)
        opcao_creditos_render_dinamico = self.font.render(self.opcao_creditos_texto, True, cor_creditos)
        opcao_sair_render_dinamico = self.font.render(self.opcao_sair_texto, True, cor_sair)

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
            novo_tamanho = (int(s