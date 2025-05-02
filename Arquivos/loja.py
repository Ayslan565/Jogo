import pygame

# ----- Classe Loja ----- 
class Loja:
    def __init__(self, itens, fonte, largura, altura):
        self.itens = itens
        self.fonte = fonte
        self.largura = largura
        self.altura = altura
        self.espacamento = 120
        self.selecionado = 0
        self.scroll_y = 0

    def desenhar(self, tela, y_offset):
        for i, item in enumerate(self.itens):
            # Controla a exibição de itens antes do selecionado
            if i < self.selecionado:
                continue  # Não desenha itens antes do selecionado

            x = 50
            y = y_offset + i * self.espacamento + self.scroll_y
            item_rect = pygame.Rect(x, y, self.largura - 100, self.espacamento - 10)

            pygame.draw.rect(tela, (70, 70, 70), item_rect)
            if i == self.selecionado:
                pygame.draw.rect(tela, (200, 200, 0), item_rect, 3)

            if item["imagem"]:
                fundo_imagem_rect = pygame.Rect(x + 10, y + 10, 100, 100)
                pygame.draw.rect(tela, (100, 100, 100), fundo_imagem_rect)
                tela.blit(item["imagem"], (x + 10, y + 10))

            nome = self.fonte.render(item["nome"], True, (255, 255, 255))
            preco = self.fonte.render(f"Preço: {item['preco']}g", True, (200, 255, 255))
            tela.blit(nome, (x + 150, y + 20))
            tela.blit(preco, (x + 150, y + 50))

    def mover_selecao(self, direcao):
        if direcao == "cima" and self.selecionado > 0:
            self.selecionado -= 1
            self.scroll_y += self.espacamento
        elif direcao == "baixo" and self.selecionado < len(self.itens) - 1:
            self.selecionado += 1
            self.scroll_y -= self.espacamento

    def comprar_item(self, dinheiro):
        item = self.itens[self.selecionado]
        if dinheiro >= item["preco"]:
            return item, dinheiro - item["preco"], True
        else:
            return None, dinheiro, False

    def selecionar_item(self, indice):
        if 0 <= indice < len(self.itens):
            self.selecionado = indice
            self.scroll_y = -indice * self.espacamento

# ----- Código Principal ----- 
pygame.init()
pygame.mixer.init()

# Carregar música de fundo
pygame.mixer.music.load("Musica/Loja/Faixa_1.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Véu do Abismo")
fonte = pygame.font.SysFont(None, 36)

# Carregar imagens
imagem_vendedor = pygame.transform.scale(pygame.image.load("Sprites/Vendedor/Vendedor.png").convert_alpha(), (200, 200))

# Espadas
imagem_Espada_1 = pygame.transform.scale(pygame.image.load("Sprites/Armas/Espadas/Adaga Basica.png").convert_alpha(), (100, 100))
imagem_Espada_2 = pygame.transform.scale(pygame.image.load("Sprites/Armas/Espadas/Espada Media.png").convert_alpha(), (100, 100))
imagem_Espada_3 = pygame.transform.scale(pygame.image.load("Sprites/Armas/Espadas/Espada Hard.png").convert_alpha(), (100, 100))
imagem_Espada_4 = pygame.transform.scale(pygame.image.load("Sprites/Armas/Espadas/Espada Amaldiçoada pelos Demonios.png").convert_alpha(), (100, 100))
imagem_Espada_5 = pygame.transform.scale(pygame.image.load("Sprites/Armas/Espadas/Espada Dos Deuses Caidos.png").convert_alpha(), (100, 100))

# Machados
imagem_Machado_1 = pygame.transform.scale(pygame.image.load("Sprites/Armas/Machado - Comum.png").convert_alpha(), (100, 100))
imagem_Machado_2 = pygame.transform.scale(pygame.image.load("Sprites/Armas/Machado-Epico.png").convert_alpha(), (100, 100))

# Cajados (reutilizando imagem temporariamente)
imagem_Cajado_1 = imagem_Machado_1
imagem_Cajado_2 = imagem_Machado_2

# Itens
itens_machados = [
    {"nome": "Machado Comum", "preco": 120, "imagem": imagem_Machado_1},
    {"nome": "Machado Dos Heréges", "preco": 250, "imagem": imagem_Machado_2}
]
itens_espadas = [
    {"nome": "Adaga Básica", "preco": 100, "imagem": imagem_Espada_1},
    {"nome": "Espada Média", "preco": 150, "imagem": imagem_Espada_2},
    {"nome": "Espada Hard", "preco": 200, "imagem": imagem_Espada_3},
    {"nome": "Espada Amaldiçoada", "preco": 300, "imagem": imagem_Espada_4},
    {"nome": "Espada dos Deuses", "preco": 500, "imagem": imagem_Espada_5}
]
itens_cajados = [
    {"nome": "Cajado Comum", "preco": 80, "imagem": imagem_Cajado_1},
    {"nome": "Cajado Mágico", "preco": 200, "imagem": imagem_Cajado_2}
]

# Inicializa loja
itens = itens_machados
loja = Loja(itens, fonte, largura, altura)
dinheiro = 200

abas = ["Machados", "Espadas", "Cajados"]
aba_atual = 0

mensagem = ""
tempo_mensagem = 0
duracao_mensagem = 180

# Desenhar elementos visuais
def desenhar_menu_superior(tela, abas, aba_atual, largura):
    pygame.draw.rect(tela, (50, 50, 50), (0, 0, largura, 50))
    for i, aba in enumerate(abas):
        cor_fundo = (204, 17, 0) if i == aba_atual else (100, 100, 100)
        pygame.draw.rect(tela, cor_fundo, (i * (largura // len(abas)), 0, largura // len(abas), 50))
        texto = fonte.render(aba, True, (255, 255, 255))
        tela.blit(texto, (i * (largura // len(abas)) + (largura // len(abas)) // 2 - texto.get_width() // 2, 15))

def desenhar_conteudo(tela, aba_atual, loja):
    y_offset = 100
    if aba_atual == 0:
        loja.itens = itens_machados
    elif aba_atual == 1:
        loja.itens = itens_espadas
    elif aba_atual == 2:
        loja.itens = itens_cajados
    loja.desenhar(tela, y_offset)

def desenhar_dinheiro(tela, dinheiro, fonte):
    texto_dinheiro = fonte.render(f"Quantidade de Aurums: {dinheiro}", True, (255, 255, 255))
    tela.blit(texto_dinheiro, (10, altura - 40))

def desenhar_mensagem(tela, mensagem):
    if mensagem:
        texto_mensagem = fonte.render(mensagem, True, (255, 0, 0))
        tela.blit(texto_mensagem, (largura // 2 - texto_mensagem.get_width() // 2, altura - 80))

def verificar_clique_mouse(mouse_pos, loja):
    for i, item in enumerate(loja.itens):
        x = 50
        y = 100 + i * loja.espacamento + loja.scroll_y
        item_rect = pygame.Rect(x, y, loja.largura - 100, loja.espacamento - 10)
        if item_rect.collidepoint(mouse_pos):
            return i
    return -1

def verificar_clique_aba(mouse_pos, largura, abas):
    for i in range(len(abas)):
        aba_rect = pygame.Rect(i * (largura // len(abas)), 0, largura // len(abas), 50)
        if aba_rect.collidepoint(mouse_pos):
            return i
    return -1
# Loop principal
clock = pygame.time.Clock()
rodando = True
while rodando:
    mouse_pos = pygame.mouse.get_pos()  # Definir mouse_pos antes de ser utilizado
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                loja.mover_selecao("cima")
            elif evento.key == pygame.K_DOWN:
                loja.mover_selecao("baixo")
            elif evento.key == pygame.K_RETURN:
                item, dinheiro, sucesso = loja.comprar_item(dinheiro)
                if sucesso:
                    mensagem = f"Comprou: {item['nome']}. Dinheiro restante: {dinheiro}g"
                else:
                    mensagem = "Dinheiro insuficiente!"
                tempo_mensagem = duracao_mensagem
            elif evento.key == pygame.K_LEFT:
                aba_atual = (aba_atual - 1) % len(abas)
                loja.selecionar_item(0)
            elif evento.key == pygame.K_RIGHT:
                aba_atual = (aba_atual + 1) % len(abas)
                loja.selecionar_item(0)
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            item_selecionado = verificar_clique_mouse(mouse_pos, loja)
            if item_selecionado != -1:
                item, dinheiro, sucesso = loja.comprar_item(dinheiro)
                if sucesso:
                    mensagem = f"Comprou: {item['nome']}. Dinheiro restante: {dinheiro}g"
                else:
                    mensagem = "Dinheiro insuficiente!"
                tempo_mensagem = duracao_mensagem

        aba_selecionada = verificar_clique_aba(mouse_pos, largura, abas)
        if aba_selecionada != -1:
            aba_atual = aba_selecionada
            loja.selecionar_item(0)

        tela.fill((0, 0, 0))
        desenhar_menu_superior(tela, abas, aba_atual, largura)
        desenhar_conteudo(tela, aba_atual, loja)
        desenhar_dinheiro(tela, dinheiro, fonte)
        desenhar_mensagem(tela, mensagem)

        # Vendedor
        pos_x = largura - imagem_vendedor.get_width() - 10
        pos_y = altura - imagem_vendedor.get_height() - 10
        tela.blit(imagem_vendedor, (pos_x, pos_y))

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
