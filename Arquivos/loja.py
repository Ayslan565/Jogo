# Arquivo: loja.py
import pygame
import time
import random
import os # Importa os para verificar a existência de arquivos

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

# --- Carregar recursos (imagens, fontes) ---
# Inicializa a fonte placeholder de forma confiável
fonte_placeholder = None
texto_erro_placeholder = None
try:
    if pygame.font.get_init():
        fonte_placeholder = pygame.font.Font(None, 20)
        texto_erro_placeholder = fonte_placeholder.render("Erro", True, (0, 0, 0))
    else:
        pygame.font.init()
        if pygame.font.get_init():
            fonte_placeholder = pygame.font.Font(None, 20)
            texto_erro_placeholder = fonte_placeholder.render("Erro", True, (0, 0, 0))
        else:
            print("DEBUG(Loja): ERRO CRÍTICO: Não foi possível inicializar pygame.font.")
except pygame.error as e:
    print(f"DEBUG(Loja): Erro ao inicializar fonte placeholder: {e}")


placeholder_img_item = pygame.Surface((100, 100), pygame.SRCALPHA) 
pygame.draw.rect(placeholder_img_item, (255, 0, 255), (0, 0, 100, 100)) 
if texto_erro_placeholder: 
    placeholder_img_item.blit(texto_erro_placeholder, (25, 40)) 


imagem_vendedor_placeholder = pygame.Surface((600, 400), pygame.SRCALPHA) 
pygame.draw.rect(imagem_vendedor_placeholder, (255, 0, 255), (0, 0, 600, 400))
if fonte_placeholder: 
    try:
        imagem_vendedor_placeholder.blit(fonte_placeholder.render("Vendedor", True, (0,0,0)), (250, 190))
    except pygame.error:
        pass 


imagem_vendedor = imagem_vendedor_placeholder
imagem_Espada_1 = imagem_Espada_2 = imagem_Espada_3 = imagem_Espada_4 = imagem_Espada_5 = placeholder_img_item
imagem_Machado_1 = imagem_Machado_2 = imagem_Machado_3 = imagem_Machado_4 = imagem_Machado_5 = imagem_Machado_6 = placeholder_img_item
imagem_Cajado_1 = imagem_Cajado_2 = imagem_Cajado_3 = placeholder_img_item


def carregar_recursos_loja(tamanho_item=(100, 100), tamanho_vendedor=(600, 400)):
    global imagem_vendedor, imagem_Espada_1, imagem_Espada_2, imagem_Espada_3, imagem_Espada_4, imagem_Espada_5
    global imagem_Machado_1, imagem_Machado_2, imagem_Machado_3, imagem_Machado_4, imagem_Machado_5, imagem_Machado_6
    global imagem_Cajado_1, imagem_Cajado_2, imagem_Cajado_3 
    global placeholder_img_item 

    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = base_dir
    if os.path.basename(base_dir).lower() == "arquivos": 
         project_root = os.path.dirname(base_dir)

    def get_full_path(relative_path):
        if not relative_path or not isinstance(relative_path, str): 
            return None
        parts = relative_path.replace("\\", "/").split("/")
        return os.path.join(project_root, *parts)

    def load_and_scale_image(rel_path, size, default_img):
        if not rel_path: 
            return default_img
        
        full_path = get_full_path(rel_path)
        if full_path and os.path.exists(full_path) and os.path.isfile(full_path): 
            try:
                img = pygame.image.load(full_path).convert_alpha()
                return pygame.transform.scale(img, size)
            except pygame.error as e:
                print(f"DEBUG(Loja): Erro ao carregar ou transformar imagem '{full_path}': {e}")
                return default_img
        else:
            return default_img

    try:
        vendedor_path_rel = "Sprites/Vendedor/Vendedor1.png" 
        imagem_vendedor = load_and_scale_image(vendedor_path_rel, tamanho_vendedor, imagem_vendedor_placeholder)

        espadas_paths_rel = ["", "", "", "", ""] # Mantenha vazias se não houver sprites
        espadas_imgs_loaded = [load_and_scale_image(p, tamanho_item, placeholder_img_item) for p in espadas_paths_rel]
        
        imagem_Espada_1 = espadas_imgs_loaded[0] if len(espadas_imgs_loaded) > 0 else placeholder_img_item
        imagem_Espada_2 = espadas_imgs_loaded[1] if len(espadas_imgs_loaded) > 1 else placeholder_img_item
        imagem_Espada_3 = espadas_imgs_loaded[2] if len(espadas_imgs_loaded) > 2 else placeholder_img_item
        imagem_Espada_4 = espadas_imgs_loaded[3] if len(espadas_imgs_loaded) > 3 else placeholder_img_item
        imagem_Espada_5 = espadas_imgs_loaded[4] if len(espadas_imgs_loaded) > 4 else placeholder_img_item

        machados_paths_rel = [
            "Sprites/Armas/Machados/Machado Bárbaro Cravejado/E-1.png", 
            "Sprites/Armas/Machados/Machado Cerúleo da Estrela Cadente/E-1.png", 
            "Sprites/Armas/Machados/Machado do Marfim Resplendor/E1.png", 
            "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/E-1.png",
            "", "",
        ]
        machados_imgs_loaded = [load_and_scale_image(p, tamanho_item, placeholder_img_item) for p in machados_paths_rel]

        imagem_Machado_1 = machados_imgs_loaded[0] if len(machados_imgs_loaded) > 0 else placeholder_img_item
        imagem_Machado_2 = machados_imgs_loaded[1] if len(machados_imgs_loaded) > 1 else placeholder_img_item
        imagem_Machado_3 = machados_imgs_loaded[2] if len(machados_imgs_loaded) > 2 else placeholder_img_item
        imagem_Machado_4 = machados_imgs_loaded[3] if len(machados_imgs_loaded) > 3 else placeholder_img_item
        imagem_Machado_5 = machados_imgs_loaded[4] if len(machados_imgs_loaded) > 4 else placeholder_img_item
        imagem_Machado_6 = machados_imgs_loaded[5] if len(machados_imgs_loaded) > 5 else placeholder_img_item

        cajados_paths_rel = [
            "Sprites/Armas/Cajados/Cajado Comum/Cajado Comum.png", 
            "Sprites/Armas/Cajados/Cajado Magico/Cajado Magico.png", 
            "Sprites/Armas/Cajados/Cajado Arcana/Cajado Arcana.png", 
        ]
        cajados_imgs_loaded = [load_and_scale_image(p, tamanho_item, placeholder_img_item) for p in cajados_paths_rel]

        imagem_Cajado_1 = cajados_imgs_loaded[0] if len(cajados_imgs_loaded) > 0 else placeholder_img_item
        imagem_Cajado_2 = cajados_imgs_loaded[1] if len(cajados_imgs_loaded) > 1 else placeholder_img_item
        imagem_Cajado_3 = cajados_imgs_loaded[2] if len(cajados_imgs_loaded) > 2 else placeholder_img_item

    except Exception as e: 
        print(f"DEBUG(Loja): Erro crítico durante carregar_recursos_loja: {e}")
        imagem_vendedor = imagem_vendedor_placeholder
        imagem_Espada_1 = imagem_Espada_2 = imagem_Espada_3 = imagem_Espada_4 = imagem_Espada_5 = placeholder_img_item
        imagem_Machado_1 = imagem_Machado_2 = imagem_Machado_3 = imagem_Machado_4 = imagem_Machado_5 = imagem_Machado_6 = placeholder_img_item
        imagem_Cajado_1 = imagem_Cajado_2 = imagem_Cajado_3 = placeholder_img_item


class Loja:
    def __init__(self, itens, fonte, largura, altura):
        self.itens = itens
        self.fonte = fonte
        self.espacamento = 120  
        self.selecionado = 0    
        self.scroll_y = 0      
        self.largura = largura 
        self.altura = altura   
        self.blink_counter = 0 
        self.blink_speed = 50  

    def desenhar(self, tela, area_desenho_rect):
        clip_rect = tela.get_clip() 
        tela.set_clip(area_desenho_rect) 
        for i, item in enumerate(self.itens):
            x = area_desenho_rect.left + 10 
            y = area_desenho_rect.top + i * self.espacamento + self.scroll_y
            item_rect = pygame.Rect(x, y, area_desenho_rect.width - 20, self.espacamento - 10)
            pygame.draw.rect(tela, (70, 70, 70), item_rect)
            if i == self.selecionado:
                if self.blink_counter < self.blink_speed // 2: 
                    pygame.draw.rect(tela, (236, 00 , 00), item_rect, 3)
            if self.fonte:
                nome = self.fonte.render(item["nome"], True, (255, 255, 255))
                preco = self.fonte.render(f"Preço: {item['preco']}g", True, (200, 255, 255))
                nome_x = item_rect.left + 20; nome_y = item_rect.top + 20
                preco_x = item_rect.left + 20; preco_y = item_rect.top + 50
                tela.blit(nome, (nome_x, nome_y)); tela.blit(preco, (preco_x, preco_y))
        tela.set_clip(clip_rect) 

    def mover_selecao(self, direcao, area_loja_rect): 
        if not self.itens: return
        if direcao == "cima" and self.selecionado > 0: self.selecionado -= 1
        elif direcao == "baixo" and self.selecionado < len(self.itens) - 1: self.selecionado += 1
        top_item_y_in_list = self.selecionado * self.espacamento
        bottom_item_y_in_list = top_item_y_in_list + self.espacamento
        altura_visivel = area_loja_rect.height
        if top_item_y_in_list + self.scroll_y < 0: self.scroll_y = -top_item_y_in_list
        elif bottom_item_y_in_list + self.scroll_y > altura_visivel: self.scroll_y = altura_visivel - bottom_item_y_in_list
        max_scroll_y = 0
        if len(self.itens) * self.espacamento > altura_visivel: max_scroll_y = altura_visivel - len(self.itens) * self.espacamento
        self.scroll_y = max(self.scroll_y, max_scroll_y); self.scroll_y = min(self.scroll_y, 0) 

    def comprar_item(self, jogador): 
        if not self.itens: return None, False, "Nenhum item na loja!"
        if not hasattr(jogador, 'dinheiro') or not hasattr(jogador, 'adicionar_item_inventario'):
            return None, False, "Erro interno: Objeto jogador inválido."
        item = self.itens[self.selecionado]
        if jogador.dinheiro >= item["preco"]:
            if hasattr(jogador, 'adicionar_item_inventario'):
                sucesso_adicionar = jogador.adicionar_item_inventario(item) 
                if sucesso_adicionar:
                    jogador.dinheiro -= item["preco"]
                    return item, True, f"Comprou: {item['nome']}. Dinheiro restante: {jogador.dinheiro}g"
                else: return None, False, "Inventário cheio ou item já existe!" 
            else: return None, False, "Erro interno: Jogador sem método de inventário."
        else: return None, False, "Dinheiro insuficiente!"

    def selecionar_item_por_posicao(self, mouse_pos, area_desenho_rect):
        if not area_desenho_rect.collidepoint(mouse_pos): return -1 
        mouse_y_relativo = mouse_pos[1] - area_desenho_rect.top - self.scroll_y
        if mouse_y_relativo < 0: return -1
        indice_clicado = int(mouse_y_relativo // self.espacamento)
        if 0 <= indice_clicado < len(self.itens): self.selecionado = indice_clicado; return indice_clicado
        return -1 

    def selecionar_item(self, indice, area_loja_rect): 
        if 0 <= indice < len(self.itens):
            self.selecionado = indice; self.scroll_y = -indice * self.espacamento
            max_scroll_y = 0
            if len(self.itens) * self.espacamento > area_loja_rect.height: max_scroll_y = area_loja_rect.height - len(self.itens) * self.espacamento
            self.scroll_y = max(self.scroll_y, max_scroll_y); self.scroll_y = min(self.scroll_y, 0) 

    def update_blink(self): self.blink_counter = (self.blink_counter + 1) % self.blink_speed
    def update_gold_border(self):
        global frame_count, color_index, color_cycle_speed, GOLD_PALETTE
        frame_count += 1
        if frame_count % color_cycle_speed == 0: color_index = (color_index + 1) % len(GOLD_PALETTE); frame_count = 0 

def desenhar_menu_superior(tela, abas, aba_atual, largura, fonte, pos_y=0): # Adicionado pos_y
    """Desenha as abas de seleção de categoria de itens."""
    altura_aba = 50
    pygame.draw.rect(tela, (50, 50, 50), (0, pos_y, largura, altura_aba)) 
    for i, aba in enumerate(abas):
        cor_fundo = (204, 17, 0) if i == aba_atual else (100, 100, 100)
        # Ajusta o rect da aba para usar pos_y
        aba_rect = pygame.Rect(i * (largura // len(abas)), pos_y, largura // len(abas), altura_aba)
        pygame.draw.rect(tela, cor_fundo, aba_rect)
        if fonte:
            texto = fonte.render(aba, True, (255, 255, 255))
            texto_rect = texto.get_rect(center=aba_rect.center)
            tela.blit(texto, texto_rect)

def desenhar_conteudo_loja(tela, aba_atual, loja, area_loja_rect, itens_machados, itens_espadas, itens_cajados): 
    if aba_atual == 0: loja.itens = itens_machados
    elif aba_atual == 1: loja.itens = itens_espadas
    elif aba_atual == 2: loja.itens = itens_cajados
    if loja.selecionado >= len(loja.itens) and loja.itens: loja.selecionado = 0; loja.scroll_y = 0 
    elif not loja.itens: loja.selecionado = 0; loja.scroll_y = 0
    loja.desenhar(tela, area_loja_rect)

def desenhar_dinheiro(tela, dinheiro, fonte, altura_tela_total): # Renomeado para clareza
    if fonte:
        texto_dinheiro = fonte.render(f"Quantidade de Aurums: {dinheiro}", True, (255, 255, 255))
        tela.blit(texto_dinheiro, (10, altura_tela_total - 40)) # Posicionado relativo à altura total da tela

def desenhar_mensagem(tela, mensagem, fonte, largura_tela_total, altura_tela_total): # Renomeado para clareza
    if mensagem and fonte: 
        texto_mensagem = fonte.render(mensagem, True, (255, 0, 0))
        tela.blit(texto_mensagem, (largura_tela_total // 2 - texto_mensagem.get_width() // 2, altura_tela_total - 80))

def verificar_clique_mouse_aba(mouse_pos, largura, abas, pos_y_abas=0): # Adicionado pos_y_abas
    """Verifica se o clique do mouse ocorreu em uma das abas, considerando sua nova posição Y."""
    altura_aba = 50
    for i in range(len(abas)):
        # Ajusta o rect da aba para usar pos_y_abas
        aba_rect = pygame.Rect(i * (largura // len(abas)), pos_y_abas, largura // len(abas), altura_aba)
        if aba_rect.collidepoint(mouse_pos):
            return i 
    return -1 

def desenhar_item_selecionado_detalhes(tela, loja, largura_tela_total, altura_tela_total, fonte, vendedor_rect_ref):
    """Desenha o fundo cinza, a borda dourada animada e a imagem do item selecionado,
       posicionado relativo à imagem do vendedor."""
    global color_index, border_thickness, border_radius, GOLD_PALETTE

    if loja.itens and 0 <= loja.selecionado < len(loja.itens):
        item_selecionado = loja.itens[loja.selecionado]
        if item_selecionado and "imagem" in item_selecionado and item_selecionado["imagem"]:
            fundo_item_largura = 150
            fundo_item_altura = 150
            
            # Posiciona o painel de detalhes no canto superior esquerdo da área do vendedor
            # com um pequeno padding.
            padding_detalhes = 20
            fundo_item_x = vendedor_rect_ref.left + padding_detalhes
            fundo_item_y = vendedor_rect_ref.top + padding_detalhes
            
            # Garante que o painel de detalhes não saia da área do vendedor
            if fundo_item_x + fundo_item_largura > vendedor_rect_ref.right - padding_detalhes:
                fundo_item_x = vendedor_rect_ref.right - padding_detalhes - fundo_item_largura
            if fundo_item_y + fundo_item_altura > vendedor_rect_ref.bottom - padding_detalhes:
                fundo_item_y = vendedor_rect_ref.bottom - padding_detalhes - fundo_item_altura


            pygame.draw.rect(tela, (0, 0, 0), (fundo_item_x, fundo_item_y, fundo_item_largura, fundo_item_altura), border_radius=border_radius)

            border_color = GOLD_PALETTE[color_index] 
            border_rect_obj = pygame.Rect(fundo_item_x - border_thickness,
                                       fundo_item_y - border_thickness,
                                       fundo_item_largura + 2 * border_thickness,
                                       fundo_item_altura + 2 * border_thickness)
            pygame.draw.rect(tela, border_color, border_rect_obj, border_thickness, border_radius=border_radius + 2) 
            
            img_item_surface = item_selecionado["imagem"]
            img_width, img_height = img_item_surface.get_size()
            
            if img_width == 0: img_width = 1
            if img_height == 0: img_height = 1

            # Escala para caber dentro do fundo_item_largura/altura com margem
            max_w_icone = fundo_item_largura - 20 
            max_h_icone = fundo_item_altura - 20
            scale_factor = min(max_w_icone / img_width, max_h_icone / img_height)
            
            if scale_factor > 0 : # Evita erro se a imagem for maior que o espaço e scale_factor for 0 ou negativo
                imagem_item_redimensionada = pygame.transform.scale(img_item_surface, (int(img_width * scale_factor), int(img_height * scale_factor))) 
                imagem_item_x = fundo_item_x + (fundo_item_largura - imagem_item_redimensionada.get_width()) // 2
                imagem_item_y = fundo_item_y + (fundo_item_altura - imagem_item_redimensionada.get_height()) // 2
                tela.blit(imagem_item_redimensionada, (imagem_item_x, imagem_item_y))

itens_machados = []
itens_espadas = []
itens_cajados = []

def run_shop_scene(tela, jogador, largura_tela, altura_tela):
    global imagem_vendedor, imagem_Espada_1, imagem_Espada_2, imagem_Espada_3, imagem_Espada_4, imagem_Espada_5
    global imagem_Machado_1, imagem_Machado_2, imagem_Machado_3, imagem_Machado_4, imagem_Machado_5, imagem_Machado_6
    global imagem_Cajado_1, imagem_Cajado_2, imagem_Cajado_3 
    global itens_machados, itens_espadas, itens_cajados
    global frame_count, color_index 
    global fonte_placeholder, texto_erro_placeholder 

    if not pygame.font.get_init():
        pygame.font.init()
        if fonte_placeholder is None:
            try:
                fonte_placeholder = pygame.font.Font(None, 20)
                texto_erro_placeholder = fonte_placeholder.render("Erro", True, (0, 0, 0))
            except pygame.error: texto_erro_placeholder = None

    carregar_recursos_loja(tamanho_item=(100, 100), tamanho_vendedor=(1080, 720)) 

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

    fonte = None
    try:
        if pygame.font.get_init(): fonte = pygame.font.SysFont(None, 36) 
    except pygame.error as e: print(f"DEBUG(Loja): Erro ao inicializar SysFont: {e}")
    if fonte is None: 
        try: fonte = pygame.font.Font(None, 36) 
        except pygame.error: print("DEBUG(Loja): Falha ao criar fonte de fallback Font(None, 36).")
             
    loja = Loja(itens_machados, fonte, largura_tela, altura_tela) 

    abas = ["Machados", "Espadas", "Cajados"]
    aba_atual = 0
    altura_aba = 50 # Definido para uso consistente

    mensagem = ""; tempo_mensagem = 0; duracao_mensagem = 180 

    # Definições de layout
    margem_topo_tela = 10
    margem_entre_elementos = 10

    # Posição do Vendedor
    vendedor_x = (largura_tela - imagem_vendedor.get_width()) // 2
    vendedor_y = margem_topo_tela
    vendedor_rect = imagem_vendedor.get_rect(topleft=(vendedor_x, vendedor_y))

    # Posição das Abas (abaixo do vendedor)
    y_posicao_abas = vendedor_rect.bottom + margem_entre_elementos

    # Área da lista de itens (abaixo das abas)
    y_inicio_area_loja = y_posicao_abas + altura_aba + margem_entre_elementos
    altura_area_loja = altura_tela - y_inicio_area_loja - 80 # Espaço para dinheiro/mensagem
    area_loja_rect = pygame.Rect(50, y_inicio_area_loja, largura_tela - 100, altura_area_loja)

    rodando_cena_loja = True
    clock = pygame.time.Clock() 

    while rodando_cena_loja:
        dt = clock.tick(60) 
        mouse_pos = pygame.mouse.get_pos() 

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False 
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: return True 
                elif evento.key == pygame.K_UP: loja.mover_selecao("cima", area_loja_rect) 
                elif evento.key == pygame.K_DOWN: loja.mover_selecao("baixo", area_loja_rect) 
                elif evento.key == pygame.K_RETURN:
                    item, sucesso, msg = loja.comprar_item(jogador) 
                    mensagem = msg; tempo_mensagem = duracao_mensagem 
                elif evento.key == pygame.K_LEFT:
                    aba_atual = (aba_atual - 1) % len(abas)
                    loja.selecionar_item(0, area_loja_rect) 
                elif evento.key == pygame.K_RIGHT:
                    aba_atual = (aba_atual + 1) % len(abas)
                    loja.selecionar_item(0, area_loja_rect) 
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Passa y_posicao_abas para verificar_clique_mouse_aba
                aba_selecionada = verificar_clique_mouse_aba(mouse_pos, largura_tela, abas, y_posicao_abas)
                if aba_selecionada != -1:
                    aba_atual = aba_selecionada
                    loja.selecionar_item(0, area_loja_rect) 
                else:
                    item_selecionado_indice = loja.selecionar_item_por_posicao(mouse_pos, area_loja_rect)
                    if item_selecionado_indice != -1:
                        item, sucesso, msg = loja.comprar_item(jogador) 
                        mensagem = msg; tempo_mensagem = duracao_mensagem 

        if tempo_mensagem > 0: tempo_mensagem -= 1
        else: mensagem = "" 

        loja.update_blink()
        loja.update_gold_border()

        tela.fill((0, 0, 0)) 
        
        # Desenha o Vendedor primeiro
        tela.blit(imagem_vendedor, vendedor_rect.topleft)
        
        # Desenha as Abas abaixo do vendedor
        desenhar_menu_superior(tela, abas, aba_atual, largura_tela, loja.fonte, y_posicao_abas) 
        
        # Desenha detalhes do item selecionado (agora precisa do vendedor_rect para posicionamento)
        desenhar_item_selecionado_detalhes(tela, loja, largura_tela, altura_tela, loja.fonte, vendedor_rect) 
        
        # Desenha fundo da área da lista de itens
        pygame.draw.rect(tela, (20, 20, 20), area_loja_rect)
        pygame.draw.rect(tela, (150, 150, 150), area_loja_rect, 2) 
        
        # Desenha conteúdo da loja
        desenhar_conteudo_loja(tela, aba_atual, loja, area_loja_rect, itens_machados, itens_espadas, itens_cajados) 

        if hasattr(jogador, 'dinheiro'): desenhar_dinheiro(tela, jogador.dinheiro, loja.fonte, altura_tela) 
        desenhar_mensagem(tela, mensagem, loja.fonte, largura_tela, altura_tela) 
        
        pygame.display.flip()
    return True
