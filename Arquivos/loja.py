import pygame
import time
import random
import os # Importa os para verificar a existência de arquivos
import math # Importa math para cálculos (usado na seta, se aplicável)

# --- Configuração para o ciclo de cores da borda dourada ---
GOLD_PALETTE = [
    (255, 223, 0),  # Brilho máximo
    (255, 215, 0),  # Gold
    (230, 192, 0),  # Tom mais escuro
    (204, 171, 0),  # Tom ainda mais escuro
    (230, 192, 0),  # Voltando
    (255, 215, 0),  # Voltando
]
color_index = 0
color_cycle_speed = 5 # Mudar de cor a cada 5 frames
frame_count = 0
border_thickness = 5 # Espessura da borda (Aumentada)
border_radius = 10 # Raio do canto para arredondar as bordas

# --- Carregar recursos (imagens, fontes) - Idealmente, isso seria feito uma vez no jogo principal ---
# No entanto, para manter este arquivo auto-contido como uma "cena", carregamos aqui.
# Certifique-se de que os caminhos dos arquivos estão corretos em relação onde este script é executado.

# --- Inicializa a fonte placeholder de forma confiável ---
# Assumimos que pygame.font já foi inicializado pelo jogo principal
try:
    pygame.font.init() # Garante que a fonte está inicializada
    fonte_placeholder = pygame.font.Font(None, 20)
    # Cria o texto de erro para o placeholder
    texto_erro_placeholder = fonte_placeholder.render("Erro", True, (0, 0, 0))
except pygame.error as e:
    print(f"DEBUG(Loja): Erro ao inicializar fonte placeholder: {e}")
    # Cria um placeholder de texto simples se a fonte falhar
    fonte_placeholder = None
    texto_erro_placeholder = None


# Cria superfícies de placeholder em caso de erro de carregamento de imagem ou caminho vazio
placeholder_img_item = pygame.Surface((100, 100), pygame.SRCALPHA) # Tamanho ajustado para 100x100
pygame.draw.rect(placeholder_img_item, (255, 0, 255), (0, 0, 100, 100)) # Magenta placeholder
if texto_erro_placeholder: # Desenha o texto de erro apenas se a fonte placeholder foi inicializada
    placeholder_img_item.blit(texto_erro_placeholder, (25, 40)) # Posição ajustada


imagem_vendedor_placeholder = pygame.Surface((600, 400), pygame.SRCALPHA) # Tamanho ajustado para o placeholder do vendedor
pygame.draw.rect(imagem_vendedor_placeholder, (255, 0, 255), (0, 0, 600, 400))
if fonte_placeholder: # Desenha o texto de vendedor apenas se a fonte placeholder foi inicializada
    try:
        imagem_vendedor_placeholder.blit(fonte_placeholder.render("Vendedor", True, (0,0,0)), (250, 190))
    except pygame.error:
        pass # Ignora se a fonte não puder ser usada aqui


# Variáveis para armazenar as imagens carregadas
imagem_vendedor = imagem_vendedor_placeholder
imagem_Espada_1 = imagem_Espada_2 = imagem_Espada_3 = imagem_Espada_4 = imagem_Espada_5 = placeholder_img_item
imagem_Machado_1 = imagem_Machado_2 = imagem_Machado_3 = imagem_Machado_4 = imagem_Machado_5 = imagem_Machado_6 = placeholder_img_item
imagem_Cajado_1 = imagem_Cajado_2 = None # Inicializa como None, será atribuído no carregamento
imagem_Cajado_3 = None # Inicializa como None, será atribuído no carregamento


# Carregar imagens reais (com tratamento de erro e redimensionamento)
def carregar_recursos_loja(tamanho_item=(100, 100), tamanho_vendedor=(600, 400)):
    """Carrega e redimensiona as imagens para a loja."""
    global imagem_vendedor, imagem_Espada_1, imagem_Espada_2, imagem_Espada_3, imagem_Espada_4, imagem_Espada_5
    global imagem_Machado_1, imagem_Machado_2, imagem_Machado_3, imagem_Machado_4, imagem_Machado_5, imagem_Machado_6
    global imagem_Cajado_1, imagem_Cajado_2, imagem_Cajado_3 # Incluído imagem_Cajado_3
    global placeholder_img_item # Precisa acessar o placeholder para usar como fallback

    try:
        # Vendedor
        vendedor_path = "Sprites/Vendedor/Vendedor1.png"
        if os.path.exists(vendedor_path):
            imagem_vendedor = pygame.transform.scale(pygame.image.load(vendedor_path).convert_alpha(), tamanho_vendedor)
        else:
            print(f"DEBUG(Loja): Aviso: Imagem do vendedor não encontrada: {vendedor_path}")
            imagem_vendedor = imagem_vendedor_placeholder # Usa o placeholder se não encontrar

        # Espadas
        espadas_paths = [
            "Sprites/Armas/Espadas/Adaga/Adaga Basica.png",
            "Sprites/Armas/Espadas/Espada Comum/Espada Media.png",
            "Sprites/Armas/Espadas/Espada dos Corrompidos/Espada dos Corrompidos.png",
            "Sprites/Armas/Espadas/Espada Dos Deuses Caidos/20250513_2215_Evolução de Espada Pixelada_remix_01jv65r3wje7jabm8hfw5w7qts.png",
            "Sprites/Armas/Espadas/Espada Demoniaca/E_D lvl-1.png"
        ]
        espadas_imgs = []
        for path in espadas_paths:
            if os.path.exists(path):
                sprite = pygame.transform.scale(pygame.image.load(path).convert_alpha(), tamanho_item)
                espadas_imgs.append(sprite)
            else:
                print(f"DEBUG(Loja): Aviso: Sprite de espada não encontrado: {path}")
                espadas_imgs.append(placeholder_img_item) # Adiciona placeholder se não encontrar

        # Atribui as imagens carregadas (ou placeholders)
        imagem_Espada_1 = espadas_imgs[0] if len(espadas_imgs) > 0 else placeholder_img_item
        imagem_Espada_2 = espadas_imgs[1] if len(espadas_imgs) > 1 else placeholder_img_item
        imagem_Espada_3 = espadas_imgs[2] if len(espadas_imgs) > 2 else placeholder_img_item
        imagem_Espada_4 = espadas_imgs[3] if len(espadas_imgs) > 3 else placeholder_img_item
        imagem_Espada_5 = espadas_imgs[4] if len(espadas_imgs) > 4 else placeholder_img_item


        # Machados (usando placeholder_img_item para caminhos vazios)
        # >>> AJUSTE ESTES CAMINHOS QUANDO TIVER OS SPRITES REAIS DOS MACHADOS <<<
        machados_paths = [
            "Sprites/Armas/Machados/Machado Comum/Machado Comum.png", # Exemplo de path real
            "Sprites/Armas/Machados/Machado Dos Hereges/Machado Dos Hereges.png", # Exemplo de path real
            "Sprites/Armas/Machados/Machado de Batalha/Machado de Batalha.png", # Exemplo de path real
            "Sprites/Armas/Machados/Machado Duplo/Machado Duplo.png", # Exemplo de path real
            "Sprites/Armas/Machados/Machado de Gelo/Machado de Gelo.png", # Exemplo de path real
            "Sprites/Armas/Machados/Machado do Caos/Machado do Caos.png", # Exemplo de path real
        ]
        machados_imgs = []
        for path in machados_paths:
            if os.path.exists(path):
                sprite = pygame.transform.scale(pygame.image.load(path).convert_alpha(), tamanho_item)
                machados_imgs.append(sprite)
            else:
                print(f"DEBUG(Loja): Aviso: Sprite de machado não encontrado: {path}")
                machados_imgs.append(placeholder_img_item) # Adiciona placeholder se não encontrar

        imagem_Machado_1 = machados_imgs[0] if len(machados_imgs) > 0 else placeholder_img_item
        imagem_Machado_2 = machados_imgs[1] if len(machados_imgs) > 1 else placeholder_img_item
        imagem_Machado_3 = machados_imgs[2] if len(machados_imgs) > 2 else placeholder_img_item
        imagem_Machado_4 = machados_imgs[3] if len(machados_imgs) > 3 else placeholder_img_item
        imagem_Machado_5 = machados_imgs[4] if len(machados_imgs) > 4 else placeholder_img_item
        imagem_Machado_6 = machados_imgs[5] if len(machados_imgs) > 5 else placeholder_img_item


        # Cajados (usando placeholder_img_item para caminhos vazios)
        # >>> AJUSTE ESTES CAMINHOS QUANDO TIVER OS SPRITES REAIS DOS CAJADOS <<<
        cajados_paths = [
            "Sprites/Armas/Cajados/Cajado Comum/Cajado Comum.png", # Exemplo de path real
            "Sprites/Armas/Cajados/Cajado Magico/Cajado Magico.png", # Exemplo de path real
            "Sprites/Armas/Cajados/Cajado Arcana/Cajado Arcana.png", # Exemplo de path real
        ]
        cajados_imgs = []
        for path in cajados_paths:
            if os.path.exists(path):
                sprite = pygame.transform.scale(pygame.image.load(path).convert_alpha(), tamanho_item)
                cajados_imgs.append(sprite)
            else:
                print(f"DEBUG(Loja): Aviso: Sprite de cajado não encontrado: {path}")
                cajados_imgs.append(placeholder_img_item) # Adiciona placeholder si não encontrar

        imagem_Cajado_1 = cajados_imgs[0] if len(cajados_imgs) > 0 else placeholder_img_item
        imagem_Cajado_2 = cajados_imgs[1] if len(cajados_imgs) > 1 else placeholder_img_item
        imagem_Cajado_3 = cajados_imgs[2] if len(cajados_imgs) > 2 else placeholder_img_item # Adicionado imagem_Cajado_3


    except pygame.error as e:
        print(f"DEBUG(Loja): Erro geral ao carregar recursos: {e}")
        # Se ocorrer um erro ao carregar QUALQUER imagem, todas as imagens de item se tornam placeholder
        imagem_Espada_1 = imagem_Espada_2 = imagem_Espada_3 = imagem_Espada_4 = imagem_Espada_5 = placeholder_img_item
        imagem_Machado_1 = imagem_Machado_2 = imagem_Machado_3 = imagem_Machado_4 = imagem_Machado_5 = imagem_Machado_6 = placeholder_img_item
        imagem_Cajado_1 = imagem_Cajado_2 = imagem_Cajado_3 = placeholder_img_item # Incluído imagem_Cajado_3


# ----- Classe Loja -----
class Loja:
    """
    Gerencia a lista de itens, seleção e rolagem na loja.
    """
    def __init__(self, itens, fonte, largura, altura):
        """
        Inicializa a Loja.

        Args:
            itens (list): Lista de dicionários representando os itens.
            fonte (pygame.font.Font): Fonte para renderizar o texto.
            largura (int): Largura da área de desenho da loja.
            altura (int): Altura da área de desenho da loja.
        """
        self.itens = itens
        self.fonte = fonte
        self.espacamento = 120     # Espaço vertical entre os itens
        self.selecionado = 0       # Índice do item selecionado
        self.scroll_y = 0          # Offset de rolagem vertical
        self.largura = largura # Adicionado largura
        self.altura = altura   # Adicionado altura
        self.blink_counter = 0 # Contador para o efeito de piscar
        self.blink_speed = 50  # Velocidade do piscar (mudar estado a cada X frames)


    def desenhar(self, tela, area_desenho_rect):
        """
        Desenha a lista de itens dentro de uma área especificada.
        As imagens dos itens individuais NÃO são desenhadas aqui.

        Args:
            tela (pygame.Surface): A superfície onde desenhar.
            area_desenho_rect (pygame.Rect): O retângulo que define a área onde os itens serão desenhados.
        """
        # Clipa a área de desenho para que os itens não sejam desenhados fora dela
        clip_rect = tela.get_clip() # Salva a área de clip atual
        tela.set_clip(area_desenho_rect) # Define a nova área de clip

        # Desenha cada item
        for i, item in enumerate(self.itens):
            # Posição X e Y do item, considerando a área de desenho e a rolagem
            x = area_desenho_rect.left + 10 # Margem esquerda dentro da área de desenho
            y = area_desenho_rect.top + i * self.espacamento + self.scroll_y

            # Cria o retângulo do item para desenho e colisão
            item_rect = pygame.Rect(x, y, area_desenho_rect.width - 20, self.espacamento - 10)

            # Desenha o fundo do item
            pygame.draw.rect(tela, (70, 70, 70), item_rect)

            # Desenha a borda vermelha piscando se o item estiver selecionado
            if i == self.selecionado:
                # Verifica o estado do contador de piscar para desenhar ou não a borda
                if self.blink_counter < self.blink_speed // 2: # Desenha na primeira metade do ciclo
                    pygame.draw.rect(tela, (236, 00 , 00), item_rect, 3)

            # Desenha o nome e preço do item (posicionados mais à esquerda agora)
            # Verifica si a fonte está disponível antes de renderizar
            if self.fonte:
                nome = self.fonte.render(item["nome"], True, (255, 255, 255))
                preco = self.fonte.render(f"Preço: {item['preco']}g", True, (200, 255, 255))
                # Calcula a posição do texto (ajustado para começar mais à esquerda)
                nome_x = item_rect.left + 20 # Ajuste a margem conforme necessário
                nome_y = item_rect.top + 20
                preco_x = item_rect.left + 20 # Ajuste a margem conforme necessário
                preco_y = item_rect.top + 50
                tela.blit(nome, (nome_x, nome_y))
                tela.blit(preco, (preco_x, preco_y))
            else:
                print("DEBUG(Loja): Aviso: Fonte da loja não disponível. Não foi possível desenhar texto dos itens.")


        tela.set_clip(clip_rect) # Restaura a área de clip original


    def mover_selecao(self, direcao, area_loja_rect): # Adicionado area_loja_rect
        """
        Move a seleção do item para cima ou para baixo e ajusta a rolagem.

        Args:
            direcao (str): "cima" ou "baixo".
            area_loja_rect (pygame.Rect): O retângulo que define a área de desenho dos itens.
        """
        if not self.itens: # Evita erros se a lista de itens estiver vazia
            return

        selecionado_anterior = self.selecionado

        if direcao == "cima" and self.selecionado > 0:
            self.selecionado -= 1
        elif direcao == "baixo" and self.selecionado < len(self.itens) - 1:
            self.selecionado += 1

        # Calcula a posição Y do topo do item selecionado
        top_item_y_in_list = self.selecionado * self.espacamento
        # Calcula a posição Y da parte inferior do item selecionado
        bottom_item_y_in_list = top_item_y_in_list + self.espacamento

        # Altura visível da área de desenho da loja
        altura_visivel = area_loja_rect.height

        # Ajusta a rolagem para manter o item selecionado visível
        # Se o topo do item selecionado estiver acima do topo visível da área de desenho
        if top_item_y_in_list + self.scroll_y < 0:
             self.scroll_y = -top_item_y_in_list
        # Se a parte inferior do item selecionado estiver abaixo da parte inferior visível da área de desenho
        elif bottom_item_y_in_list + self.scroll_y > altura_visivel:
             self.scroll_y = altura_visivel - bottom_item_y_in_list

        # Garante que a rolagem não vá além do conteúdo
        max_scroll_y = 0
        if len(self.itens) * self.espacamento > altura_visivel:
             max_scroll_y = altura_visivel - len(self.itens) * self.espacamento
        self.scroll_y = max(self.scroll_y, max_scroll_y) # Não rola para baixo além do necessário
        self.scroll_y = min(self.scroll_y, 0) # Não rola para cima além do topo


    def comprar_item(self, jogador): # Recebe o objeto jogador para gerenciar dinheiro e inventário
        """
        Tenta comprar o item selecionado.

        Args:
            jogador (object): O objeto jogador com atributos como 'dinheiro' e um método 'adicionar_item_inventario'.

        Returns:
            tuple: (item comprado ou None, True se comprou, False caso contrário, mensagem).
        """
        if not self.itens: # Verifica se a lista de itens não está vazia
            return None, False, "Nenhum item na loja!"

        if not hasattr(jogador, 'dinheiro') or not hasattr(jogador, 'adicionar_item_inventario'):
             print("DEBUG(Loja): Objeto jogador não tem atributos 'dinheiro' ou método 'adicionar_item_inventario'.")
             return None, False, "Erro interno: Objeto jogador inválido."


        item = self.itens[self.selecionado]
        if jogador.dinheiro >= item["preco"]:
            # Lógica para adicionar o item ao inventário do jogador
            # Verifica se o jogador tem o método antes de chamar
            if hasattr(jogador, 'adicionar_item_inventario'):
                 sucesso_adicionar = jogador.adicionar_item_inventario(item) # Assume que o jogador tem este método
                 if sucesso_adicionar:
                     jogador.dinheiro -= item["preco"]
                     # print(f"Item '{item['nome']}' comprado!") # Mensagem de debug
                     return item, True, f"Comprou: {item['nome']}. Dinheiro restante: {jogador.dinheiro}g"
                 else:
                     return None, False, "Inventário cheio!" # Mensagem se o inventário estiver cheio (exemplo)
            else:
                 return None, False, "Erro interno: Jogador sem método de inventário."
        else:
            return None, False, "Dinheiro insuficiente!"


    def selecionar_item_por_posicao(self, mouse_pos, area_desenho_rect):
        """
        Seleciona um item com base na posição do mouse dentro da área de desenho.

        Args:
            mouse_pos (tuple): Posição (x, y) do mouse.
            area_desenho_rect (pygame.Rect): O retângulo da área onde os itens são desenhados.

        Returns:
            int: O índice do item selecionado, ou -1 si nenhum item foi clicado.
        """
        if not area_desenho_rect.collidepoint(mouse_pos):
            return -1 # Clique fora da área de desenho da loja

        # Ajusta a posição do mouse para ser relativa ao topo da área de desenho E considera a rolagem
        mouse_y_relativo = mouse_pos[1] - area_desenho_rect.top - self.scroll_y

        # Calcula o índice do item clicado
        # Garante que o cálculo não resulte em um índice negativo si clicar acima da área visível
        if mouse_y_relativo < 0:
            return -1

        indice_clicado = int(mouse_y_relativo // self.espacamento)

        # Verifica se o índice calculado é válido
        if 0 <= indice_clicado < len(self.itens):
            self.selecionado = indice_clicado # Seleciona o item clicado
            # Ajusta a rolagem para mostrar o item selecionado
            # self.mover_selecao("nenhuma", area_loja_rect) # Chama mover_selecao com uma direção neutra para ajustar a rolagem - Não precisa chamar aqui, o update já ajusta a rolagem.
            return indice_clicado

        return -1 # Nenhum item válido clicado


    def selecionar_item(self, indice, area_loja_rect): # Adicionado area_loja_rect
        """
        Define o item selecionado pelo índice e ajusta a rolagem.

        Args:
            indice (int): O índice do item a ser selecionado.
            area_loja_rect (pygame.Rect): O retângulo que define a área de desenho dos itens.
        """
        if 0 <= indice < len(self.itens):
            self.selecionado = indice
            # Ajusta a rolagem para que o item selecionado fique visível no topo da área de desenho.
            self.scroll_y = -indice * self.espacamento
            # Garante que a rolagem não vá além do conteúdo
            max_scroll_y = 0
            if len(self.itens) * self.espacamento > area_loja_rect.height:
                 max_scroll_y = area_loja_rect.height - len(self.itens) * self.espacamento
            self.scroll_y = max(self.scroll_y, max_scroll_y) # Não rola para baixo além do necessário
            self.scroll_y = min(self.scroll_y, 0) # Não rola para cima além do topo


    def update_blink(self):
        """Atualiza o contador de piscar para a borda vermelha."""
        self.blink_counter = (self.blink_counter + 1) % self.blink_speed

    def update_gold_border(self):
        """Atualiza o ciclo de cores da borda dourada."""
        global frame_count, color_index, color_cycle_speed, GOLD_PALETTE
        frame_count += 1
        if frame_count % color_cycle_speed == 0:
            color_index = (color_index + 1) % len(GOLD_PALETTE)
            frame_count = 0 # Reinicia o contador de frames


# --- Funções de Desenho (Adaptadas para serem chamadas de fora) ---

def desenhar_menu_superior(tela, abas, aba_atual, largura, fonte):
    """Desenha as abas de seleção de categoria de itens no topo da tela."""
    pygame.draw.rect(tela, (50, 50, 50), (0, 0, largura, 50)) # Fundo do menu superior
    for i, aba in enumerate(abas):
        # Cor de fundo da aba (vermelho para selecionada, cinza para outras)
        cor_fundo = (204, 17, 0) if i == aba_atual else (100, 100, 100)
        # Desenha o retângulo da aba
        aba_rect = pygame.Rect(i * (largura // len(abas)), 0, largura // len(abas), 50)
        pygame.draw.rect(tela, cor_fundo, aba_rect)
        # Desenha o texto da aba centralizado
        # Verifica si a fonte está disponível antes de renderizar
        if fonte:
            texto = fonte.render(aba, True, (255, 255, 255))
            texto_rect = texto.get_rect(center=aba_rect.center)
            tela.blit(texto, texto_rect)
        else:
            print("DEBUG(Loja): Aviso: Fonte da loja não disponível. Não foi possível desenhar texto das abas.")


def desenhar_conteudo_loja(tela, aba_atual, loja, area_loja_rect, itens_machados, itens_espadas, itens_cajados): # Adicionado listas de itens
    """
    Define a lista de itens da loja com base na aba atual e desenha os itens
    dentro da área especificada.

    Args:
        tela (pygame.Surface): A superfície onde desenhar.
        aba_atual (int): O índice da aba atual.
        loja (Loja): O objeto Loja.
        area_loja_rect (pygame.Rect): O retângulo que define a área de desenho dos itens.
        itens_machados (list): Lista de itens de machados.
        itens_espadas (list): Lista de itens de espadas.
        itens_cajados (list): Lista de itens de cajados.
    """
    # Define a lista de itens da loja com base na aba atual
    if aba_atual == 0:
        loja.itens = itens_machados
    elif aba_atual == 1:
        loja.itens = itens_espadas
    elif aba_atual == 2:
        loja.itens = itens_cajados
    # Adicione mais abas aqui se necessário

    # Garante que o item selecionado seja válido para a nova lista
    if loja.selecionado >= len(loja.itens):
        loja.selecionado = 0 # Reseta a seleção para o primeiro item
        loja.scroll_y = 0 # Reseta a rolagem

    # Desenha os itens usando o método da classe Loja
    loja.desenhar(tela, area_loja_rect)


def desenhar_dinheiro(tela, dinheiro, fonte, altura):
    """Desenha a quantidade de dinheiro do jogador."""
    # Verifica si a fonte está disponível antes de renderizar
    if fonte:
        texto_dinheiro = fonte.render(f"Quantidade de Aurums: {dinheiro}", True, (255, 255, 255))
        # Posiciona o texto do dinheiro no canto inferior esquerdo
        tela.blit(texto_dinheiro, (10, altura - 40))
    else:
        print("DEBUG(Loja): Aviso: Fonte da loja não disponível. Não foi possível desenhar o dinheiro.")


def desenhar_mensagem(tela, mensagem, fonte, largura, altura):
    """Desenha uma mensagem temporária no centro inferior da tela."""
    if mensagem and fonte: # Verifica se há mensagem e si a fonte está disponível
        texto_mensagem = fonte.render(mensagem, True, (255, 0, 0))
        # Posiciona a mensagem centralizada horizontalmente, um pouco acima da parte inferior
        tela.blit(texto_mensagem, (largura // 2 - texto_mensagem.get_width() // 2, altura - 80))
    elif mensagem and not fonte:
        print("DEBUG(Loja): Aviso: Fonte da loja não disponível. Não foi possível desenhar a mensagem.")


def verificar_clique_mouse_aba(mouse_pos, largura, abas):
    """Verifica si o clique do mouse ocorreu em uma das abas."""
    for i in range(len(abas)):
        aba_rect = pygame.Rect(i * (largura // len(abas)), 0, largura // len(abas), 50)
        if aba_rect.collidepoint(mouse_pos):
            return i # Retorna o índice da aba clicada
    return -1 # Retorna -1 si nenhuma aba foi clicada

def desenhar_item_selecionado_detalhes(tela, loja, largura, altura, fonte):
    """Desenha o fundo cinza, a borda dourada animada e a imagem do item selecionado."""
    global color_index, border_thickness, border_radius, GOLD_PALETTE

    # Verifica se há itens e se o índice selecionado é válido
    if loja.itens and 0 <= loja.selecionado < len(loja.itens):
        item_selecionado = loja.itens[loja.selecionado]
        # Verifica se o item selecionado tem uma imagem válida
        if item_selecionado and "imagem" in item_selecionado and item_selecionado["imagem"]:
            # Define o tamanho do fundo cinza
            fundo_item_largura = 150
            fundo_item_altura = 150

            # Calcula a posição para o fundo cinza no canto esquerdo central (ajustado)
            fundo_item_x = 270  # Margem da esquerda (ajustada)
            fundo_item_y = (altura // 2) - 270 # Centralizado verticalmente e subiu mais (ajustado)

            # Desenha o fundo cinza com bordas arredondadas
            pygame.draw.rect(tela, (0, 0, 0), (fundo_item_x, fundo_item_y, fundo_item_largura, fundo_item_altura), border_radius=border_radius)

            # --- Desenha a borda dourada animada com bordas arredondadas ---
            border_color = GOLD_PALETTE[color_index] # Obtém a cor atual da paleta
            # Calcula o retângulo da borda (ligeiramente maior que o fundo e centralizado)
            border_rect = (fundo_item_x - border_thickness,
                           fundo_item_y - border_thickness,
                           fundo_item_largura + 2 * border_thickness,
                           fundo_item_altura + 2 * border_thickness)
            # Desenha o retângulo da borda com bordas arredondadas e maior espessura
            pygame.draw.rect(tela, border_color, border_rect, border_thickness, border_radius=border_radius + 2) # Adicionado +2 para a borda ficar um pouco mais arredondada que o fundo
            # --- Fim do desenho da borda ---


            # Redimensiona a imagem do item para caber no fundo (opcional)
            # Usa o tamanho da imagem original ou um tamanho padrão se não houver imagem
            img_width, img_height = item_selecionado["imagem"].get_size() if item_selecionado["imagem"] else (100, 100)
            # Calcula o fator de escala para caber dentro do fundo sem distorcer
            scale_factor = min(fundo_item_largura / img_width, fundo_item_altura / img_height)
            imagem_item_redimensionada = pygame.transform.scale(item_selecionado["imagem"], (int(img_width * scale_factor * 0.8), int(img_height * scale_factor * 0.8))) # Escala para 80% do tamanho máximo para ter margem

            # Calcula a posição da imagem do item para centralizá-la no fundo cinza
            imagem_item_x = fundo_item_x + (fundo_item_largura - imagem_item_redimensionada.get_width()) // 2
            imagem_item_y = fundo_item_y + (fundo_item_altura - imagem_item_redimensionada.get_height()) // 2

            # Desenha a imagem do item
            tela.blit(imagem_item_redimensionada, (imagem_item_x, imagem_item_y))
        # else:
             # print(f"DEBUG(Loja): Aviso: Item selecionado ({item_selecionado.get('nome', 'Nome Desconhecido')}) não tem imagem válida.") # Debug se o item selecionado não tiver imagem


# --- Dados dos Itens ---
# Estas listas devem ser definidas APÓS o carregamento das imagens
itens_machados = []
itens_espadas = []
itens_cajados = []

# --- Função Principal para Rodar a Cena da Loja ---
def run_shop_scene(tela, jogador, largura_tela, altura_tela):
    """
    Executa a cena da loja.

    Args:
        tela (pygame.Surface): A superfície principal do jogo.
        jogador (object): O objeto jogador com atributos como 'dinheiro' e 'adicionar_item_inventario'.
        largura_tela (int): A largura da tela do jogo.
        altura_tela (int): A altura da tela do jogo.

    Returns:
        bool: True para continuar o jogo principal, False para sair do jogo.
    """
    global imagem_vendedor, imagem_Espada_1, imagem_Espada_2, imagem_Espada_3, imagem_Espada_4, imagem_Espada_5
    global imagem_Machado_1, imagem_Machado_2, imagem_Machado_3, imagem_Machado_4, imagem_Machado_5, imagem_Machado_6
    global imagem_Cajado_1, imagem_Cajado_2, imagem_Cajado_3 # Incluído imagem_Cajado_3
    global itens_machados, itens_espadas, itens_cajados
    global frame_count, color_index # Para a borda dourada animada
    global fonte_placeholder, texto_erro_placeholder # Acessa variáveis globais para placeholders

    # Carrega os recursos da loja (imagens)
    carregar_recursos_loja(tamanho_item=(100, 100), tamanho_vendedor=(600, 400)) # Carrega com tamanhos específicos

    # Define os itens AGORA que as imagens foram carregadas
    itens_machados = [
        {"nome": "Machado Comum", "preco": 120, "imagem": imagem_Machado_1},
        {"nome": "Machado Dos Heréges", "preco": 250, "imagem": imagem_Machado_2},
        {"nome": "Machado de Batalha", "preco": 300, "imagem": imagem_Machado_3},
        {"nome": "Machado Duplo", "preco": 400, "imagem": imagem_Machado_4},
        {"nome": "Machado de Gelo", "preco": 550, "imagem": imagem_Machado_5},
        {"nome": "Machado do Caos", "preco": 700, "imagem": imagem_Machado_6},
    ]
    itens_espadas = [
        {"nome": "Adaga Básica", "preco": 100, "imagem": imagem_Espada_1},
        {"nome": "Espada Média", "preco": 150, "imagem": imagem_Espada_2},
        {"nome": "Espada dos Corrompidos", "preco": 200, "imagem": imagem_Espada_3},
        {"nome": "Espada dos Deuses Caidos", "preco": 300, "imagem": imagem_Espada_4},
        {"nome": "Espada Demoniaca", "preco": 500, "imagem": imagem_Espada_5}
    ]
    itens_cajados = [
        {"nome": "Cajado Comum", "preco": 80, "imagem": imagem_Cajado_1},
        {"nome": "Cajado Mágico", "preco": 200, "imagem": imagem_Cajado_2},
        {"nome": "Cajado Arcana", "preco": 350, "imagem": imagem_Cajado_3},
    ]

    # Verifica se a fonte principal da loja pode ser inicializada
    try:
        fonte = pygame.font.SysFont(None, 36) # Define a fonte para a loja
    except pygame.error as e:
        print(f"DEBUG(Loja): Erro ao inicializar fonte principal da loja: {e}")
        fonte = None # Define como None se a fonte falhar

    # Inicializa loja com a primeira categoria de itens
    loja = Loja(itens_machados, fonte, largura_tela, altura_tela)

    abas = ["Machados", "Espadas", "Cajados"]
    aba_atual = 0

    mensagem = ""
    tempo_mensagem = 0
    duracao_mensagem = 180 # Duração da mensagem em frames (aprox. 3 segundos a 60 FPS)

    # Define a área onde a lista de itens será desenhada
    altura_menu_superior = 50
    altura_vendedor_display = 400 # Altura que a imagem do vendedor ocupa na tela
    margem_abaixo_vendedor = 30
    y_inicio_area_loja = altura_menu_superior + altura_vendedor_display + margem_abaixo_vendedor
    altura_area_loja = altura_tela - y_inicio_area_loja - 80 # Deixa espaço para dinheiro e mensagem

    area_loja_rect = pygame.Rect(50, y_inicio_area_loja, largura_tela - 100, altura_area_loja)

    # Loop da cena da loja
    rodando_cena_loja = True
    clock = pygame.time.Clock() # Clock local para a cena da loja

    while rodando_cena_loja:
        dt = clock.tick(60) # Limita o FPS para a cena da loja (60 FPS é comum)
        mouse_pos = pygame.mouse.get_pos() # Obtém a posição do mouse

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False # Indica para sair do jogo principal
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return True # Indica para voltar para o jogo principal
                elif evento.key == pygame.K_UP:
                    loja.mover_selecao("cima", area_loja_rect) # Passa area_loja_rect
                elif evento.key == pygame.K_DOWN:
                    loja.mover_selecao("baixo", area_loja_rect) # Passa area_loja_rect
                elif evento.key == pygame.K_RETURN:
                    # Lógica de compra ao pressionar Enter
                    item, sucesso, msg = loja.comprar_item(jogador) # Passa o objeto jogador
                    mensagem = msg
                    tempo_mensagem = duracao_mensagem # Define o tempo para exibir a mensagem
                elif evento.key == pygame.K_LEFT:
                    # Muda para a aba anterior
                    aba_atual = (aba_atual - 1) % len(abas)
                    loja.selecionar_item(0, area_loja_rect) # Reseta a seleção e rolagem na nova aba (Passa area_loja_rect)
                elif evento.key == pygame.K_RIGHT:
                    # Muda para a próxima aba
                    aba_atual = (aba_atual + 1) % len(abas)
                    loja.selecionar_item(0, area_loja_rect) # Reseta a seleção e rolagem na nova aba (Passa area_loja_rect)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                 # Verifica clique nas abas
                 aba_clicada = verificar_clique_mouse_aba(mouse_pos, largura_tela, abas)
                 if aba_clicada != -1:
                      aba_atual = aba_clicada
                      loja.selecionar_item(0, area_loja_rect) # Reseta a seleção e rolagem na nova aba (Passa area_loja_rect)
                 else:
                      # Verifica clique nos itens da loja
                      item_clicado_indice = loja.selecionar_item_por_posicao(mouse_pos, area_loja_rect)
                      if item_clicado_indice != -1:
                           # Define o item selecionado e tenta comprar
                           # A seleção já é feita dentro de selecionar_item_por_posicao
                           item, sucesso, msg = loja.comprar_item(jogador) # Passa o objeto jogador
                           mensagem = msg
                           tempo_mensagem = duracao_mensagem # Define o tempo para exibir a mensagem

        # --- Lógica de Atualização ---
        loja.update_blink() # Atualiza o contador de piscar
        loja.update_gold_border() # Atualiza o ciclo de cores da borda dourada

        # Atualiza a mensagem temporária
        if tempo_mensagem > 0:
            tempo_mensagem -= 1 # Decrementa o contador de frames da mensagem
            if tempo_mensagem <= 0:
                mensagem = "" # Limpa a mensagem quando o tempo acaba

        # --- Desenho ---
        tela.fill((30, 30, 30)) # Fundo escuro para a loja

        # Desenha a imagem do vendedor (posicionada no centro superior)
        # Verifica se a imagem do vendedor existe antes de desenhar
        if imagem_vendedor is not None:
             vendedor_x = (largura_tela - imagem_vendedor.get_width()) // 2
             vendedor_y = altura_menu_superior + 10 # Um pouco abaixo do menu superior
             tela.blit(imagem_vendedor, (vendedor_x, vendedor_y))

        # Desenha o menu superior (abas)
        desenhar_menu_superior(tela, abas, aba_atual, largura_tela, loja.fonte) # Usa a fonte da loja

        # Desenha a área de conteúdo da loja (itens)
        desenhar_conteudo_loja(tela, aba_atual, loja, area_loja_rect, itens_machados, itens_espadas, itens_cajados) # Passa as listas de itens

        # Desenha os detalhes do item selecionado (fundo, borda, imagem)
        desenhar_item_selecionado_detalhes(tela, loja, largura_tela, altura_tela, loja.fonte)

        # Desenha a quantidade de dinheiro do jogador
        # Verifica se o jogador e o atributo dinheiro existem
        if jogador is not None and hasattr(jogador, 'dinheiro'):
             desenhar_dinheiro(tela, jogador.dinheiro, loja.fonte, altura_tela)
        else:
             print("DEBUG(Loja): Objeto jogador ou atributo 'dinheiro' não disponível para desenhar dinheiro.")


        # Desenha a mensagem temporária (compra, erro, etc.)
        desenhar_mensagem(tela, mensagem, loja.fonte, largura_tela, altura_tela)


        # Atualizar a tela
        pygame.display.flip()

    # Este ponto só será alcançado se rodando_cena_loja se tornar False,
    # o que não é o fluxo de saída esperado baseado nos retornos True/False.
    # O jogo deve sair ou retornar ao loop principal através dos returns no evento QUIT/KEYDOWN.
    return True # Retorna True por padrão para não sair do jogo.
