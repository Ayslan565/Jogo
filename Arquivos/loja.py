import pygame
import time
import random


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
        self.espacamento = 120    # Espaço vertical entre os itens
        self.selecionado = 0      # Índice do item selecionado
        self.scroll_y = 0         # Offset de rolagem vertical
        self.largura = largura # Adicionado largura
        self.altura = altura   # Adicionado altura


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
            # Desenha a borda vermelha se o item estiver selecionado
            if i == self.selecionado:
                pygame.draw.rect(tela, (236, 00 , 00), item_rect, 3)

            # Desenha o nome e preço do item (posicionados mais à esquerda agora)
            nome = self.fonte.render(item["nome"], True, (255, 255, 255))
            preco = self.fonte.render(f"Preço: {item['preco']}g", True, (200, 255, 255))
            # Calcula a posição do texto (ajustado para começar mais à esquerda)
            nome_x = item_rect.left + 20 # Ajuste a margem conforme necessário
            nome_y = item_rect.top + 20
            preco_x = item_rect.left + 20 # Ajuste a margem conforme necessário
            preco_y = item_rect.top + 50
            tela.blit(nome, (nome_x, nome_y))
            tela.blit(preco, (preco_x, preco_y))

        tela.set_clip(clip_rect) # Restaura a área de clip original


    def mover_selecao(self, direcao):
        """
        Move a seleção do item para cima ou para baixo e ajusta a rolagem.

        Args:
            direcao (str): "cima" ou "baixo".
        """
        if not self.itens: # Evita erros se a lista de itens estiver vazia
            return

        selecionado_anterior = self.selecionado

        if direcao == "cima" and self.selecionado > 0:
            self.selecionado -= 1
        elif direcao == "baixo" and self.selecionado < len(self.itens) - 1:
            self.selecionado += 1

        # Calcula a posição Y do topo do item selecionado
        top_item_y = self.selecionado * self.espacamento + self.scroll_y
        # Calcula a posição Y da parte inferior do item selecionado
        bottom_item_y = top_item_y + self.espacamento

        # Altura visível da área de desenho da loja
        altura_visivel = area_loja_rect.height # Altura da area_loja_rect

        # Ajusta a rolagem para manter o item selecionado visível
        # Se o item selecionado estiver acima do topo visível
        if top_item_y < 0:
             self.scroll_y = -self.selecionado * self.espacamento
        # Se o item selecionado estiver abaixo da parte inferior visível
        elif bottom_item_y > area_loja_rect.height:
             # Calcula quanto precisa rolar para que a parte inferior do item fique visível
             self.scroll_y = area_loja_rect.height - bottom_item_y + self.scroll_y


    def comprar_item(self, dinheiro):
        """
        Tenta comprar o item selecionado.

        Args:
            dinheiro (int): Quantidade de dinheiro atual do jogador.

        Returns:
            tuple: (item comprado ou None, dinheiro restante, True se comprou, False caso contrário).
        """
        if not self.itens: # Verifica se a lista de itens não está vazia
            return None, dinheiro, False

        item = self.itens[self.selecionado]
        if dinheiro >= item["preco"]:
            # Lógica para adicionar o item ao inventário do jogador seria aqui
            # print(f"Item '{item['nome']}' comprado!") # Mensagem de debug
            return item, dinheiro - item["preco"], True
        else:
            return None, dinheiro, False

    def selecionar_item_por_posicao(self, mouse_pos, area_desenho_rect):
        """
        Seleciona um item com base na posição do mouse dentro da área de desenho.

        Args:
            mouse_pos (tuple): Posição (x, y) do mouse.
            area_desenho_rect (pygame.Rect): O retângulo da área onde os itens são desenhados.

        Returns:
            int: O índice do item selecionado, ou -1 se nenhum item foi clicado.
        """
        if not area_desenho_rect.collidepoint(mouse_pos):
            return -1 # Clique fora da área de desenho da loja

        # Ajusta a posição do mouse para ser relativa ao topo da área de desenho E considera a rolagem
        mouse_y_relativo = mouse_pos[1] - area_desenho_rect.top - self.scroll_y

        # Calcula o índice do item clicado
        indice_clicado = int(mouse_y_relativo // self.espacamento)

        # Verifica se o índice calculado é válido
        if 0 <= indice_clicado < len(self.itens):
            self.selecionado = indice_clicado # Seleciona o item clicado
            # Ajusta a rolagem para mostrar o item selecionado
            self.mover_selecao("nenhuma") # Chama mover_selecao com uma direção neutra para ajustar a rolagem
            return indice_clicado

        return -1 # Nenhum item válido clicado


    def selecionar_item(self, indice):
        """
        Define o item selecionado pelo índice e ajusta a rolagem.

        Args:
            indice (int): O índice do item a ser selecionado.
        """
        if 0 <= indice < len(self.itens):
            self.selecionado = indice
            # Ajusta a rolagem para que o item selecionado fique visível no topo da área de desenho.
            self.scroll_y = -indice * self.espacamento


# ----- Código Principal -----
pygame.init()
pygame.mixer.init()

# Carregar música de fundo
try:
    faixas = [
        "Musica/Loja/Faixa_1.mp3",
        "Musica/Loja/Echoes_of_the_Forest.mp3",
        "Musica/Loja/Shadows of a Fallen Heart.mp3",
        "Musica/Loja/faixa_4.mp3",
    ]
    pygame.mixer.music.load(random.choice(faixas))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Erro ao carregar música: {e}")

largura, altura = 1080, 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Véu do Abismo")
fonte = pygame.font.SysFont(None, 36)

# Cria superfícies de placeholder em caso de erro de carregamento de imagem ou caminho vazio
placeholder_img = pygame.Surface((100, 100), pygame.SRCALPHA) # Tamanho ajustado para 100x100
pygame.draw.rect(placeholder_img, (255, 0, 255), (0, 0, 100, 100)) # Magenta placeholder
fonte_erro = pygame.font.Font(None, 20)
texto_erro = fonte_erro.render("Erro", True, (0, 0, 0))
placeholder_img.blit(texto_erro, (25, 40)) # Posição ajustada

imagem_vendedor = pygame.Surface((600, 400), pygame.SRCALPHA) # Tamanho ajustado para o placeholder do vendedor
pygame.draw.rect(imagem_vendedor, (255, 0, 255), (0, 0, 600, 400))
imagem_vendedor.blit(fonte_erro.render("Vendedor", True, (0,0,0)), (250, 190))


# Carregar imagens
try:
    # Assumindo que 'Sprites/Vendedor/Vendedor1.png' é o caminho correto
    imagem_vendedor = pygame.transform.scale(pygame.image.load("Sprites/Vendedor/Vendedor1.png").convert_alpha(), (600, 400))

    # Espadas (usando os caminhos fornecidos)
    imagem_Espada_1 = pygame.transform.scale(pygame.image.load("Sprites/Armas/Espadas/Adaga/Adaga Basica.png").convert_alpha(), (150, 150))
    imagem_Espada_2 = pygame.transform.scale(pygame.image.load("Sprites/Armas/Espadas/Espada Comum/Espada Media.png").convert_alpha(), (200, 200))
    imagem_Espada_3 = pygame.transform.scale(pygame.image.load("Sprites/Armas/Espadas/Espada dos Corrompidos/Espada dos Corrompidos.png").convert_alpha(), (100, 100))
    imagem_Espada_4 = pygame.transform.scale(pygame.image.load("Sprites/Armas/Espadas/Espada Dos Deuses Caidos/20250513_2215_Evolução de Espada Pixelada_remix_01jv65r3wje7jabm8hfw5w7qts.png").convert_alpha(), (100, 100))
    imagem_Espada_5 = pygame.transform.scale(pygame.image.load("Sprites/Armas/Espadas/Espada Demoniaca/E_D lvl-1.png").convert_alpha(), (100, 100))

    # Machados (usando placeholder_img para caminhos vazios)
    imagem_Machado_1 = placeholder_img
    imagem_Machado_2 = placeholder_img # Mantido como placeholder
    imagem_Machado_3 = placeholder_img # Adicionado placeholder para os caminhos extras
    imagem_Machado_4 = placeholder_img
    imagem_Machado_5 = placeholder_img
    imagem_Machado_6 = placeholder_img

    # Cajados (usando placeholder_img para caminhos vazios)
    imagem_Cajado_1 = placeholder_img
    imagem_Cajado_2 = placeholder_img

except pygame.error as e:
    print(f"Erro ao carregar imagem: {e}")
    # Se ocorrer um erro ao carregar QUALQUER imagem, todas as imagens de item se tornam placeholder
    imagem_Espada_1 = imagem_Espada_2 = imagem_Espada_3 = imagem_Espada_4 = imagem_Espada_5 = placeholder_img
    imagem_Machado_1 = imagem_Machado_2 = imagem_Machado_3 = imagem_Machado_4 = imagem_Machado_5 = imagem_Machado_6 = placeholder_img
    imagem_Cajado_1 = imagem_Cajado_2 = placeholder_img


# Itens
itens_machados = [
    {"nome": "Machado Comum", "preco": 120, "imagem": imagem_Machado_1},
    {"nome": "Machado Dos Heréges", "preco": 250, "imagem": imagem_Machado_2},
    {"nome": "Machado de Batalha", "preco": 300, "imagem": imagem_Machado_3}, # Novos itens com placeholder
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
    {"nome": "Cajado Arcana", "preco": 350, "imagem": placeholder_img}, # Novo item com placeholder
]


# Inicializa loja
itens = itens_machados # Começa com os machados
loja = Loja(itens, fonte, largura, altura) # A loja gerencia a lista de itens atual

dinheiro = 200 # Dinheiro inicial do jogador

abas = ["Machados", "Espadas", "Cajados"]
aba_atual = 0

mensagem = ""
tempo_mensagem = 0
duracao_mensagem = 180 # Duração da mensagem em frames (aprox. 3 segundos a 60 FPS)

# Define a área onde a lista de itens será desenhada
# Começa abaixo do menu superior (50px) e abaixo da área do vendedor.
# Ajuste a altura_area_loja conforme necessário para caber na tela.
altura_menu_superior = 50
altura_vendedor = 400 # Altura da imagem do vendedor (ajustado para 400)
margem_abaixo_vendedor = 30 # Aumentei a margem para criar mais espaço
y_inicio_area_loja = altura_menu_superior + altura_vendedor + margem_abaixo_vendedor
# Ajusta a altura da área da loja para caber na tela, deixando espaço para o dinheiro e mensagem
altura_area_loja = altura - y_inicio_area_loja - 80

area_loja_rect = pygame.Rect(50, y_inicio_area_loja, largura - 100, altura_area_loja)

# --- Configuração para o ciclo de cores da borda ---
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


# Desenhar elementos visuais
def desenhar_menu_superior(tela, abas, aba_atual, largura):
    """Desenha as abas de seleção de categoria de itens no topo da tela."""
    pygame.draw.rect(tela, (50, 50, 50), (0, 0, largura, 50)) # Fundo do menu superior
    for i, aba in enumerate(abas):
        # Cor de fundo da aba (vermelho para selecionada, cinza para outras)
        cor_fundo = (204, 17, 0) if i == aba_atual else (100, 100, 100)
        # Desenha o retângulo da aba
        aba_rect = pygame.Rect(i * (largura // len(abas)), 0, largura // len(abas), 50)
        pygame.draw.rect(tela, cor_fundo, aba_rect)
        # Desenha o texto da aba centralizado
        texto = fonte.render(aba, True, (255, 255, 255))
        texto_rect = texto.get_rect(center=aba_rect.center)
        tela.blit(texto, texto_rect)

def desenhar_conteudo_loja(tela, aba_atual, loja, area_loja_rect):
    """
    Define a lista de itens da loja com base na aba atual e desenha os itens
    dentro da área especificada.

    Args:
        tela (pygame.Surface): A superfície onde desenhar.
        aba_atual (int): O índice da aba atual.
        loja (Loja): O objeto Loja.
        area_loja_rect (pygame.Rect): O retângulo que define a área de desenho dos itens.
    """
    # Define a lista de itens da loja com base na aba atual
    if aba_atual == 0:
        loja.itens = itens_machados
    elif aba_atual == 1:
        loja.itens = itens_espadas
    elif aba_atual == 2:
        loja.itens = itens_cajados

    # Garante que o item selecionado seja válido para a nova lista
    if loja.selecionado >= len(loja.itens):
        loja.selecionado = 0 # Reseta a seleção para o primeiro item
        loja.scroll_y = 0 # Reseta a rolagem

    # Desenha os itens usando o método da classe Loja
    loja.desenhar(tela, area_loja_rect)


def desenhar_dinheiro(tela, dinheiro, fonte, altura):
    """Desenha a quantidade de dinheiro do jogador."""
    texto_dinheiro = fonte.render(f"Quantidade de Aurums: {dinheiro}", True, (255, 255, 255))
    # Posiciona o texto do dinheiro no canto inferior esquerdo
    tela.blit(texto_dinheiro, (10, altura - 40))

def desenhar_mensagem(tela, mensagem, fonte, largura, altura):
    """Desenha uma mensagem temporária no centro inferior da tela."""
    if mensagem:
        texto_mensagem = fonte.render(mensagem, True, (255, 0, 0))
        # Posiciona a mensagem centralizada horizontalmente, um pouco acima da parte inferior
        tela.blit(texto_mensagem, (largura // 2 - texto_mensagem.get_width() // 2, altura - 80))

def verificar_clique_mouse_aba(mouse_pos, largura, abas):
    """Verifica se o clique do mouse ocorreu em uma das abas."""
    for i in range(len(abas)):
        aba_rect = pygame.Rect(i * (largura // len(abas)), 0, largura // len(abas), 50)
        if aba_rect.collidepoint(mouse_pos):
            return i # Retorna o índice da aba clicada
    return -1 # Retorna -1 se nenhuma aba foi clicada

# Loop principal
clock = pygame.time.Clock()
rodando = True

while rodando:
    dt = clock.tick(30) # Limita o FPS e obtém o tempo por frame
    mouse_pos = pygame.mouse.get_pos() # Obtém a posição do mouse

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                loja.mover_selecao("cima")
            elif evento.key == pygame.K_DOWN:
                loja.mover_selecao("baixo")
            elif evento.key == pygame.K_RETURN:
                # Lógica de compra ao pressionar Enter
                item, dinheiro, sucesso = loja.comprar_item(dinheiro)
                if sucesso:
                    mensagem = f"Comprou: {item['nome']}. Dinheiro restante: {dinheiro}g"
                else:
                    mensagem = "Dinheiro insuficiente!"
                tempo_mensagem = duracao_mensagem # Define o tempo para exibir a mensagem
            elif evento.key == pygame.K_LEFT:
                # Muda para a aba anterior
                aba_atual = (aba_atual - 1) % len(abas)
                loja.selecionar_item(0) # Reseta a seleção e rolagem na nova aba
            elif evento.key == pygame.K_RIGHT:
                # Muda para a próxima aba
                aba_atual = (aba_atual + 1) % len(abas)
                loja.selecionar_item(0) # Reseta a seleção e rolagem na nova aba

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Verifica clique nas abas
            aba_selecionada = verificar_clique_mouse_aba(mouse_pos, largura, abas)
            if aba_selecionada != -1:
                aba_atual = aba_selecionada
                loja.selecionar_item(0) # Reseta a seleção e rolagem na nova aba
            else:
                # Verifica clique nos itens da loja
                item_selecionado_indice = loja.selecionar_item_por_posicao(mouse_pos, area_loja_rect)
                if item_selecionado_indice != -1:
                    # Define o item selecionado e tenta comprar
                    item, dinheiro, sucesso = loja.comprar_item(dinheiro)
                    if sucesso:
                        mensagem = f"Comprou: {item['nome']}. Dinheiro restante: {dinheiro}g"
                    else:
                        mensagem = "Dinheiro insuficiente!"
                    tempo_mensagem = duracao_mensagem # Define o tempo para exibir a mensagem


    # Atualiza a mensagem temporária
    if tempo_mensagem > 0:
        tempo_mensagem -= 1
    else:
        mensagem = "" # Limpa a mensagem quando o tempo acabar

    # --- Atualiza o ciclo de cores da borda ---
    frame_count += 1
    if frame_count % color_cycle_speed == 0:
        color_index = (color_index + 1) % len(GOLD_PALETTE)
        frame_count = 0 # Reinicia o contador de frames


    # --- Desenho ---
    tela.fill((0, 0, 0)) # Preenche o fundo

    # Desenha o menu superior (abas)
    desenhar_menu_superior(tela, abas, aba_atual, largura)

    # Desenha o vendedor no topo, centralizado horizontalmente
    vendedor_x = (largura - imagem_vendedor.get_width()) // 2
    vendedor_y = altura_menu_superior + 10 # Um pouco abaixo do menu superior
    tela.blit(imagem_vendedor, (vendedor_x, vendedor_y))

    # >>> Desenha o fundo cinza, a borda dourada animada e a imagem do item selecionado <<<
    # Verifica se há itens e se o índice selecionado é válido
    if loja.itens and 0 <= loja.selecionado < len(loja.itens):
        item_selecionado = loja.itens[loja.selecionado]
        if item_selecionado["imagem"]:
            # Define o tamanho do fundo cinza
            fundo_item_largura = 120
            fundo_item_altura = 120

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
            imagem_item_redimensionada = pygame.transform.scale(item_selecionado["imagem"], (100, 100)) # Ajuste o tamanho

            # Calcula a posição da imagem do item para centralizá-la no fundo cinza
            imagem_item_x = fundo_item_x + (fundo_item_largura - imagem_item_redimensionada.get_width()) // 2
            imagem_item_y = fundo_item_y + (fundo_item_altura - imagem_item_redimensionada.get_height()) // 2

            # Desenha a imagem do item
            tela.blit(imagem_item_redimensionada, (imagem_item_x, imagem_item_y))


    # Desenha um fundo para a área da lista de itens (opcional, para visualização)
    pygame.draw.rect(tela, (20, 20, 20), area_loja_rect)
    pygame.draw.rect(tela, (150, 150, 150), area_loja_rect, 2) # Borda

    # Desenha o conteúdo da loja (itens) dentro da área definida
    desenhar_conteudo_loja(tela, aba_atual, loja, area_loja_rect)

    # Desenha a quantidade de dinheiro
    desenhar_dinheiro(tela, dinheiro, fonte, altura)

    # Desenha a mensagem temporária
    desenhar_mensagem(tela, mensagem, fonte, largura, altura)


    # Atualizar a tela
    pygame.display.flip()

# Finaliza o Pygame
pygame.quit()
