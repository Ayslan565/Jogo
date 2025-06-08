# Arquivo: loja_modulo.py
import pygame
import time
import random
import os

# --- IMPORTAÇÃO ÚNICA DAS CLASSES DE ARMAS ---
try:
    from importacoes import * # CORRIGIDO: Importa de 'importacoes.py'
    print("DEBUG(loja_modulo): Classes de armas e outros módulos importados de importacoes.py")
except ImportError as e:
    print(f"ERRO CRÍTICO(loja_modulo): Não foi possível importar de importacoes.py. Verifique o arquivo e o caminho. Erro: {e}")
    # Definir todas as classes de armas como None para evitar NameError mais tarde
    AdagaFogo = EspadaCaida = EspadaFogoAzul = EspadaLua = EspadaPenitencia = None
    EspadaSacraCerulea = EspadaSacraDasBrasas = LaminaDoCeuCentilhante = None
    MachadoBarbaro = MachadoCeruleo = MachadoDaDescidaSanta = MachadoDoFogoAbrasador = None
    MachadoMarfim = MachadoMacabro = None
    Cajado = None 
    Weapon = MachadoBase = None
    Vida = Player = RodaDeArmas = PauseMenuManager = XPManager = Menu = None
    GerenciadorDeInimigos = Estacoes = Grama = Arvore = Timer = shop_elements = None
    run_death_screen = BarraInventario = ItemInventario = None


# --- Configuração para o ciclo de cores da borda dourada ---
GOLD_PALETTE = [
    (255, 223, 0), (255, 215, 0), (230, 192, 0),
    (204, 171, 0), (230, 192, 0), (255, 215, 0),
]
color_index = 0
color_cycle_speed = 5 # Frames por mudança de cor
frame_count = 0
border_thickness = 5
border_radius = 10
FONTE_RETRO_PATH = "Fontes/Retro Gaming.ttf"

# --- Inicialização de variáveis globais para imagens e fontes ---
fonte_placeholder = None
texto_erro_placeholder = None
placeholder_img_item = None
imagem_vendedor_placeholder = None

imagem_vendedor = None
imagem_Espada_1 = imagem_Espada_2 = imagem_Espada_3 = imagem_Espada_4 = imagem_Espada_5 = None
imagem_Espada_6 = imagem_Espada_7 = None 
imagem_Machado_1 = imagem_Machado_2 = imagem_Machado_3 = imagem_Machado_4 = imagem_Machado_5 = imagem_Machado_6 = None
imagem_Cajado_1 = imagem_Cajado_2 = imagem_Cajado_3 = None
imagem_Pocao_Cura = None

itens_data_global = {"Machados": [], "Espadas": [], "Cajados": [], "Poções": []}

def tocar_musica_aleatoria(diretorio_musica_base):
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"DEBUG(Loja Modulo): Erro ao inicializar pygame.mixer: {e}")
            return
    lista_musicas_paths = [
        os.path.join(diretorio_musica_base, "Musica/Loja/Faixa_1.mp3"),
        os.path.join(diretorio_musica_base, "Musica/Loja/Faixa_2.mp3"),
        os.path.join(diretorio_musica_base, "Musica/Loja/Faixa_3.mp3"),
        os.path.join(diretorio_musica_base, "Musica/Loja/Faixa 4.mp3"),
    ]
    musicas_validas = [m for m in lista_musicas_paths if os.path.exists(m)]
    if not musicas_validas:
        print("DEBUG(Loja Modulo): Nenhuma música encontrada.")
        return
    pygame.mixer.music.set_volume(0.5)
    random.shuffle(musicas_validas)
    if musicas_validas:
        try:
            pygame.mixer.music.load(musicas_validas[0])
            pygame.mixer.music.play(-1) # Tocar em loop
            print(f"DEBUG(Loja Modulo): Tocando música: {musicas_validas[0]}")
        except pygame.error as e:
            print(f"DEBUG(Loja Modulo): Erro ao tocar música {musicas_validas[0]}: {e}")

def inicializar_placeholders_globais():
    global fonte_placeholder, texto_erro_placeholder, placeholder_img_item, imagem_vendedor_placeholder
    if fonte_placeholder is None:
        try:
            if not pygame.font.get_init(): pygame.font.init()
            if pygame.font.get_init():
                fonte_placeholder = pygame.font.Font(None, 20)
                texto_erro_placeholder = fonte_placeholder.render("Erro Img", True, (0,0,0))
            else:
                print("DEBUG(Loja Modulo): ERRO pygame.font para placeholders.")
        except pygame.error as e:
            print(f"DEBUG(Loja Modulo): Erro fonte placeholder: {e}")
    if placeholder_img_item is None:
        placeholder_img_item = pygame.Surface((100,100), pygame.SRCALPHA)
        pygame.draw.rect(placeholder_img_item, (255,0,255,128), (0,0,100,100))
        if texto_erro_placeholder:
            placeholder_img_item.blit(texto_erro_placeholder, (placeholder_img_item.get_width()//2 - texto_erro_placeholder.get_width()//2, placeholder_img_item.get_height()//2 - texto_erro_placeholder.get_height()//2))
        else: 
            pygame.draw.line(placeholder_img_item, (0,0,0), (10,10), (90,90), 2)
            pygame.draw.line(placeholder_img_item, (0,0,0), (10,90), (90,10), 2)
    if imagem_vendedor_placeholder is None:
        imagem_vendedor_placeholder = pygame.Surface((600,400), pygame.SRCALPHA)
        pygame.draw.rect(imagem_vendedor_placeholder, (255,0,255,128), (0,0,600,400))
        if fonte_placeholder:
            try:
                texto_vendedor_render = fonte_placeholder.render("Vendedor Placeholder", True, (0,0,0))
                imagem_vendedor_placeholder.blit(texto_vendedor_render, (imagem_vendedor_placeholder.get_width()//2 - texto_vendedor_render.get_width()//2, imagem_vendedor_placeholder.get_height()//2 - texto_vendedor_render.get_height()//2))
            except pygame.error: pass 
inicializar_placeholders_globais()

def carregar_recursos_loja(tamanho_item=(100, 100), tamanho_vendedor_img=(600, 400)):
    global imagem_vendedor, imagem_Espada_1, imagem_Espada_2, imagem_Espada_3, imagem_Espada_4, imagem_Espada_5, imagem_Espada_6, imagem_Espada_7
    global imagem_Machado_1, imagem_Machado_2, imagem_Machado_3, imagem_Machado_4, imagem_Machado_5, imagem_Machado_6
    global imagem_Cajado_1, imagem_Cajado_2, imagem_Cajado_3
    global imagem_Pocao_Cura
    global placeholder_img_item, imagem_vendedor_placeholder

    if placeholder_img_item is None or imagem_vendedor_placeholder is None:
        inicializar_placeholders_globais()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = base_dir
    if os.path.basename(base_dir).lower() in ["arquivos", "loja", "scripts"]: 
        project_root = os.path.dirname(base_dir)

    def get_full_path(relative_path_from_project_root):
        if not relative_path_from_project_root or not isinstance(relative_path_from_project_root, str): return None
        parts = relative_path_from_project_root.replace("\\", "/").split("/")
        return os.path.join(project_root, *parts)

    def load_and_scale_image(rel_path, size, default_img):
        if not rel_path: return default_img
        full_path = get_full_path(rel_path)
        if full_path and os.path.exists(full_path) and os.path.isfile(full_path):
            try:
                img = pygame.image.load(full_path).convert_alpha()
                return pygame.transform.scale(img, size)
            except pygame.error as e:
                print(f"DEBUG(Loja Modulo load_and_scale_image): Erro ao carregar '{full_path}': {e}")
                return default_img
        print(f"AVISO(Loja Modulo): Caminho não encontrado: {full_path}")
        return default_img
        
    try:
        vendedor_path_rel = "Sprites/Vendedor/Vendedor1.png"
        imagem_vendedor = load_and_scale_image(vendedor_path_rel, tamanho_vendedor_img, imagem_vendedor_placeholder)

        espadas_paths_rel = [
            "Sprites/Armas/Espadas/Adaga do Fogo Contudente/Adaga E-1.png", 
            "Sprites/Armas/Espadas/Espada de Fogo azul Sacra Cerulea/Espada Dos Deuses Caidos -E1.png", 
            "Sprites/Armas/Espadas/Espada do Olhar Da Penitencia/E1.png", 
            "Sprites/Armas/Espadas/Espada Sacra Caida/Espada dos Corrompidos -E1.png", 
            "Sprites/Armas/Espadas/Espada Sacra do Lua/E1.jpg", 
            "Sprites/Armas/Espadas/Lâmina do Ceu Centilhante/E1.jpg" 
        ]
        espadas_imgs_loaded = [load_and_scale_image(p, tamanho_item, placeholder_img_item) for p in espadas_paths_rel]
        full_espadas_list = (espadas_imgs_loaded + [placeholder_img_item]*7)[:7] 
        imagem_Espada_1, imagem_Espada_2, imagem_Espada_3, imagem_Espada_4, imagem_Espada_5, imagem_Espada_6, imagem_Espada_7 = full_espadas_list

        machados_paths_rel = [
            "Sprites/Armas/Machados/Machado Bárbaro Cravejado/Machado E-1.png", 
            "Sprites/Armas/Machados/Machado Cerúleo da Estrela Cadente/Machado dos Impuros -E1.png", 
            "Sprites/Armas/Machados/Machado da Descida Santa/E1.jpg", 
            "Sprites/Armas/Machados/Machado do Fogo Abrasador/E1.jpg", 
            "Sprites/Armas/Machados/Machado do Marfim Resplendor/E1.png", 
            "Sprites/Armas/Machados/Machado Macabro da Gula Infinita/E-1.png", 
        ]
        machados_imgs_loaded = [load_and_scale_image(p, tamanho_item, placeholder_img_item) for p in machados_paths_rel]
        full_machados_list = (machados_imgs_loaded + [placeholder_img_item]*6)[:6]
        imagem_Machado_1, imagem_Machado_2, imagem_Machado_3, imagem_Machado_4, imagem_Machado_5, imagem_Machado_6 = full_machados_list

        cajados_paths_rel = [
            "Sprites/Armas/Armas Magicas/Cajado da Fixacao Ametista/E1.png", 
            "Sprites/Armas/Armas Magicas/Cajado Da santa Natureza/E1.png", 
            "Sprites/Armas/Armas Magicas/Livro dos impuros/E1.jpg", 
        ]
        cajados_imgs_loaded = [load_and_scale_image(p, tamanho_item, placeholder_img_item) for p in cajados_paths_rel]
        full_cajados_list = (cajados_imgs_loaded + [placeholder_img_item]*3)[:3]
        imagem_Cajado_1, imagem_Cajado_2, imagem_Cajado_3 = full_cajados_list

        pocoes_paths_rel = ["Sprites/Pocao/Pocao.png"] 
        pocoes_imgs_loaded = [load_and_scale_image(p, tamanho_item, placeholder_img_item) for p in pocoes_paths_rel]
        imagem_Pocao_Cura = pocoes_imgs_loaded[0] if len(pocoes_imgs_loaded) > 0 else placeholder_img_item

    except Exception as e:
        print(f"DEBUG(Loja Modulo): Erro crítico durante carregar_recursos_loja: {e}")
        imagem_vendedor = imagem_vendedor_placeholder
        imagem_Espada_1 = imagem_Espada_2 = imagem_Espada_3 = imagem_Espada_4 = imagem_Espada_5 = imagem_Espada_6 = imagem_Espada_7 = placeholder_img_item
        imagem_Machado_1 = imagem_Machado_2 = imagem_Machado_3 = imagem_Machado_4 = imagem_Machado_5 = imagem_Machado_6 = placeholder_img_item
        imagem_Cajado_1 = imagem_Cajado_2 = imagem_Cajado_3 = placeholder_img_item
        imagem_Pocao_Cura = placeholder_img_item

class Loja:
    def __init__(self, itens, fonte, largura_inicial_tela, altura_inicial_tela):
        self.itens = itens
        self.fonte = fonte
        self.espacamento = 150 
        self.selecionado = 0
        self.scroll_y = 0
        self.blink_counter = 0
        self.blink_speed = 30

    def desenhar(self, tela, area_desenho_rect_externa): 
        borda_container_espessura = 2 
        padding_interno_lista = 8 
        inicio_x_conteudo_lista = area_desenho_rect_externa.left + borda_container_espessura + padding_interno_lista
        inicio_y_conteudo_lista = area_desenho_rect_externa.top + borda_container_espessura + padding_interno_lista
        largura_disponivel_para_itens = area_desenho_rect_externa.width - 2 * (borda_container_espessura + padding_interno_lista)
        
        clip_rect_original = tela.get_clip()
        tela.set_clip(area_desenho_rect_externa) 

        cor_descricao = (200, 200, 200) 
        padding_vertical_texto_item = 15 
        padding_horizontal_texto_item = 20 
        espaco_entre_linhas = 5 

        for i, item in enumerate(self.itens):
            y_item_relativo = i * self.espacamento
            y_tela_item = inicio_y_conteudo_lista + y_item_relativo + self.scroll_y
            altura_item_rect = self.espacamento - 10 
            item_rect = pygame.Rect(inicio_x_conteudo_lista, y_tela_item, largura_disponivel_para_itens, altura_item_rect)
            
            pygame.draw.rect(tela, (70, 70, 70), item_rect, border_radius=5)
            if i == self.selecionado:
                if self.blink_counter < self.blink_speed // 2:
                    pygame.draw.rect(tela, (236, 0, 0), item_rect, 3, border_radius=5)
            
            if self.fonte:
                pos_x_texto_no_item = item_rect.left + padding_horizontal_texto_item
                current_y_no_item = item_rect.top + padding_vertical_texto_item
                try:
                    nome_surf = self.fonte.render(item.get("nome", "Item Desconhecido"), True, (255, 255, 255))
                    tela.blit(nome_surf, (pos_x_texto_no_item, current_y_no_item))
                    current_y_no_item += nome_surf.get_height() + espaco_entre_linhas
                    
                    preco_render_temp = self.fonte.render(f"Preço: {item.get('preco', '??')}g", True, (200, 255, 255)) 
                    altura_preco = preco_render_temp.get_height()
                    preco_y_final_no_item = item_rect.bottom - altura_preco - padding_vertical_texto_item
                    limite_y_descricao_no_item = preco_y_final_no_item - espaco_entre_linhas 
                    
                    descricao_item = item.get("descricao", "")
                    if descricao_item: 
                        palavras_descricao = descricao_item.split(' ')
                        linha_atual_desc_str = "" 
                        largura_max_desc_no_item = item_rect.width - (2 * padding_horizontal_texto_item)
                        altura_linha_fonte = self.fonte.get_height()
                        for palavra in palavras_descricao:
                            teste_linha_str = linha_atual_desc_str + palavra + " "
                            if self.fonte.size(teste_linha_str.strip())[0] < largura_max_desc_no_item:
                                linha_atual_desc_str = teste_linha_str
                            else: 
                                if current_y_no_item + altura_linha_fonte <= limite_y_descricao_no_item:
                                    desc_surf_linha = self.fonte.render(linha_atual_desc_str.strip(), True, cor_descricao)
                                    tela.blit(desc_surf_linha, (pos_x_texto_no_item, current_y_no_item))
                                    current_y_no_item += altura_linha_fonte 
                                    linha_atual_desc_str = palavra + " " 
                                else: 
                                    linha_atual_desc_str = "" ; break 
                        if linha_atual_desc_str.strip(): 
                            if current_y_no_item + altura_linha_fonte <= limite_y_descricao_no_item:
                                desc_surf_linha = self.fonte.render(linha_atual_desc_str.strip(), True, cor_descricao)
                                tela.blit(desc_surf_linha, (pos_x_texto_no_item, current_y_no_item))
                    
                    preco_surf = preco_render_temp 
                    preco_x_pos_no_item = item_rect.right - preco_surf.get_width() - padding_horizontal_texto_item
                    tela.blit(preco_surf, (preco_x_pos_no_item, preco_y_final_no_item))

                except pygame.error as e: print(f"DEBUG(Loja Modulo-DesenharItem): Erro render: {e}")
                except KeyError as e: print(f"DEBUG(Loja Modulo-DesenharItem): Chave ausente: {e} - Item: {item}")
        tela.set_clip(clip_rect_original)

    def mover_selecao(self, direcao, area_loja_rect):
        if not self.itens: return
        if direcao == "cima" and self.selecionado > 0: self.selecionado -= 1
        elif direcao == "baixo" and self.selecionado < len(self.itens) - 1: self.selecionado += 1
        self.ajustar_scroll(area_loja_rect)

    def ajustar_scroll(self, area_loja_rect): 
        if not self.itens: self.scroll_y = 0; return
        if not hasattr(area_loja_rect, 'height') or area_loja_rect.height <= 0: return 
        borda_container_espessura = 2; padding_interno_lista = 8 
        altura_visivel_interna = max(1, area_loja_rect.height - 2 * (borda_container_espessura + padding_interno_lista))
        pos_y_item_selecionado_topo_na_lista = self.selecionado * self.espacamento
        pos_y_item_selecionado_base_na_lista = pos_y_item_selecionado_topo_na_lista + self.espacamento
        if pos_y_item_selecionado_topo_na_lista + self.scroll_y < 0: 
            self.scroll_y = -pos_y_item_selecionado_topo_na_lista
        elif pos_y_item_selecionado_base_na_lista + self.scroll_y > altura_visivel_interna: 
            self.scroll_y = altura_visivel_interna - pos_y_item_selecionado_base_na_lista
        altura_total_itens = len(self.itens) * self.espacamento
        if altura_total_itens <= altura_visivel_interna: self.scroll_y = 0
        else:
            max_scroll_y_negativo = altura_visivel_interna - altura_total_itens
            self.scroll_y = max(self.scroll_y, max_scroll_y_negativo)
            self.scroll_y = min(self.scroll_y, 0)

    def comprar_item(self, jogador):
        if not self.itens or not (0 <= self.selecionado < len(self.itens)):
            return None, False, "Nenhum item selecionado!"
        if not hasattr(jogador, 'dinheiro') or \
           not hasattr(jogador, 'adicionar_item_inventario') or \
           not hasattr(jogador, 'SHOP_ITEM_TO_WEAPON_CLASS'): 
            print("DEBUG(Loja comprar_item): Jogador inválido ou sem SHOP_ITEM_TO_WEAPON_CLASS.")
            return None, False, "Erro de configuração do jogador!"
        
        item_a_comprar = self.itens[self.selecionado]
        nome_item_loja = item_a_comprar.get("nome")
        if not nome_item_loja:
            return None, False, "Erro: Item da loja sem nome."

        weapon_class_from_player_map = jogador.SHOP_ITEM_TO_WEAPON_CLASS.get(nome_item_loja)
        if weapon_class_from_player_map is None: 
            mensagem_erro = f"Item '{nome_item_loja}' não configurado no Player.SHOP_ITEM_TO_WEAPON_CLASS!"
            print(f"AVISO(Loja): {mensagem_erro}")
            return None, False, mensagem_erro
        
        try:
            if jogador.dinheiro >= item_a_comprar["preco"]:
                print(f"DEBUG(Loja comprar_item): Tentando chamar jogador.adicionar_item_inventario para '{nome_item_loja}'")
                if jogador.adicionar_item_inventario(item_a_comprar): 
                    jogador.dinheiro -= item_a_comprar["preco"]
                    return item_a_comprar, True, f"Comprou: {item_a_comprar['nome']}! Aurums: {jogador.dinheiro}g"
                else:
                    return None, False, "Inventário cheio ou item não pôde ser adicionado!" 
            else:
                return None, False, "Dinheiro insuficiente!"
        except KeyError as e: 
            print(f"DEBUG(Loja comprar_item): KeyError - {e} no item {item_a_comprar}")
            return None, False, "Erro nos dados do item."
        except Exception as e: 
            print(f"DEBUG(Loja comprar_item): Exceção inesperada ao tentar comprar '{nome_item_loja}': {e}")
            return None, False, f"Erro inesperado na compra: {e}"

    def selecionar_item_por_posicao(self, mouse_pos, area_desenho_rect_externa):
        if not self.itens: return -1
        borda_container_espessura = 2; padding_interno_lista = 8 
        area_clicavel_interna = area_desenho_rect_externa.inflate(-2 * (borda_container_espessura + padding_interno_lista), -2 * (borda_container_espessura + padding_interno_lista))
        area_clicavel_interna.width = max(0, area_clicavel_interna.width); area_clicavel_interna.height = max(0, area_clicavel_interna.height)
        if not area_clicavel_interna.collidepoint(mouse_pos): return -1
        mouse_y_relativo_a_conteudo = mouse_pos[1] - area_clicavel_interna.top - self.scroll_y
        if mouse_y_relativo_a_conteudo < 0: return -1
        indice_clicado = int(mouse_y_relativo_a_conteudo // self.espacamento)
        if 0 <= indice_clicado < len(self.itens): self.selecionado = indice_clicado; return indice_clicado
        return -1

    def selecionar_item(self, indice, area_loja_rect): 
        if 0 <= indice < len(self.itens): self.selecionado = indice; self.ajustar_scroll(area_loja_rect) 
        elif not self.itens: self.selecionado = 0; self.scroll_y = 0

    def update_blink(self): self.blink_counter = (self.blink_counter + 1) % self.blink_speed
    def update_gold_border(self):
        global frame_count, color_index, color_cycle_speed, GOLD_PALETTE
        frame_count += 1
        if frame_count >= color_cycle_speed: color_index = (color_index + 1) % len(GOLD_PALETTE); frame_count = 0

def desenhar_menu_superior(tela, abas_nomes, aba_idx_atual, largura_tela_atual, fonte, y_pos_tabs, altura_tabs):
    if not abas_nomes: return
    largura_aba_individual = largura_tela_atual // len(abas_nomes) if len(abas_nomes) > 0 else largura_tela_atual
    pygame.draw.rect(tela, (50,50,50), (0, y_pos_tabs, largura_tela_atual, altura_tabs))
    for i, nome_aba in enumerate(abas_nomes):
        cor_fundo_aba = (204,17,0) if i == aba_idx_atual else (100,100,100)
        aba_rect = pygame.Rect(i * largura_aba_individual, y_pos_tabs, largura_aba_individual, altura_tabs)
        pygame.draw.rect(tela, cor_fundo_aba, aba_rect, border_top_left_radius=8, border_top_right_radius=8)
        pygame.draw.line(tela, (30,30,30), (aba_rect.right -1, y_pos_tabs), (aba_rect.right -1, y_pos_tabs + altura_tabs), 2)
        if fonte:
            try:
                texto_aba_surf = fonte.render(nome_aba, True, (255,255,255))
                tela.blit(texto_aba_surf, texto_aba_surf.get_rect(center=aba_rect.center))
            except pygame.error as e: print(f"DEBUG(Loja Modulo-MenuSup): Erro render aba: {e}")

def desenhar_conteudo_loja(loja_obj, aba_idx_atual, area_loja_rect_atual, todos_itens_por_cat):
    nomes_abas = list(todos_itens_por_cat.keys())
    if 0 <= aba_idx_atual < len(nomes_abas):
        nome_categoria_atual = nomes_abas[aba_idx_atual]
        loja_obj.itens = todos_itens_por_cat.get(nome_categoria_atual, [])
    else: loja_obj.itens = []
    if loja_obj.itens:
        if loja_obj.selecionado >= len(loja_obj.itens): loja_obj.selecionado = len(loja_obj.itens) -1 if loja_obj.itens else 0
        if loja_obj.selecionado < 0: loja_obj.selecionado = 0
    else: loja_obj.selecionado = 0; loja_obj.scroll_y = 0
    loja_obj.ajustar_scroll(area_loja_rect_atual)

def desenhar_dinheiro(tela, dinheiro_jog, fonte, largura_tela_atual, altura_tela_atual):
    if fonte:
        try:
            texto_dinheiro_surf = fonte.render(f"Aurums: {dinheiro_jog}", True, (255,223,0))
            tela.blit(texto_dinheiro_surf, (largura_tela_atual - texto_dinheiro_surf.get_width() - 10, altura_tela_atual - texto_dinheiro_surf.get_height() - 10))
        except pygame.error as e: print(f"DEBUG(Loja Modulo-Dinheiro): Erro render dinheiro: {e}")

def desenhar_mensagem(tela, texto_msg_atual, fonte, largura_tela_atual, altura_tela_atual):
    if texto_msg_atual and fonte:
        try:
            cor_texto = (0,255,0) if "Comprou" in texto_msg_atual else (255,100,100)
            texto_msg_surf = fonte.render(texto_msg_atual, True, cor_texto)
            padding_msg = 10 
            s_width = texto_msg_surf.get_width() + 2 * padding_msg
            s_height = texto_msg_surf.get_height() + 2 * padding_msg
            fundo_msg_surface = pygame.Surface((s_width, s_height), pygame.SRCALPHA)
            fundo_msg_surface.fill((0,0,0,180)) 
            fundo_msg_surface.blit(texto_msg_surf, (padding_msg, padding_msg)) 
            fundo_msg_rect = fundo_msg_surface.get_rect(centerx=largura_tela_atual // 2, bottom=altura_tela_atual - 20)
            tela.blit(fundo_msg_surface, fundo_msg_rect.topleft)
        except pygame.error as e: print(f"DEBUG(Loja Modulo-Mensagem): Erro render msg: {e}")

def verificar_clique_mouse_aba(mouse_pos, largura_tela_atual, num_abas_total, altura_tabs, y_pos_tabs):
    if num_abas_total == 0: return -1
    largura_aba_individual = largura_tela_atual // num_abas_total if num_abas_total > 0 else largura_tela_atual
    for i in range(num_abas_total):
        aba_rect = pygame.Rect(i * largura_aba_individual, y_pos_tabs, largura_aba_individual, altura_tabs)
        if aba_rect.collidepoint(mouse_pos): return i
    return -1

def desenhar_item_selecionado_detalhes(tela, loja_obj, fonte_usada, rect_referencia_vendedor): 
    global color_index, border_thickness, border_radius, GOLD_PALETTE
    if loja_obj.itens and 0 <= loja_obj.selecionado < len(loja_obj.itens):
        item_sel = loja_obj.itens[loja_obj.selecionado]
        if item_sel and "imagem" in item_sel and isinstance(item_sel["imagem"], pygame.Surface):
            fundo_w, fundo_h = 200,200; padding_horizontal_detalhes = 20; padding_vertical_detalhes = 120 
            fundo_x = rect_referencia_vendedor.left + padding_horizontal_detalhes
            fundo_y = rect_referencia_vendedor.top + padding_vertical_detalhes 
            if fundo_x + fundo_w > rect_referencia_vendedor.right - padding_horizontal_detalhes:
                fundo_x = max(rect_referencia_vendedor.left, rect_referencia_vendedor.right - padding_horizontal_detalhes - fundo_w)
            if fundo_y + fundo_h > rect_referencia_vendedor.bottom - padding_vertical_detalhes: 
                fundo_y = max(rect_referencia_vendedor.top, rect_referencia_vendedor.bottom - padding_vertical_detalhes - fundo_h)
            fundo_w = max(0, fundo_w); fundo_h = max(0, fundo_h)
            pygame.draw.rect(tela, (20,20,20), (fundo_x, fundo_y, fundo_w, fundo_h), border_radius=border_radius)
            cor_borda_animada = GOLD_PALETTE[color_index]
            borda_rect_animada = pygame.Rect(fundo_x - border_thickness//2, fundo_y - border_thickness//2, fundo_w + border_thickness, fundo_h + border_thickness)
            pygame.draw.rect(tela, cor_borda_animada, borda_rect_animada, border_thickness, border_radius=border_radius + (border_thickness//2))
            img_surf = item_sel["imagem"] 
            img_orig_w, img_orig_h = img_surf.get_size()
            if img_orig_w == 0 or img_orig_h == 0: return
            margem_int = 10; max_w_icone_grande, max_h_icone_grande = fundo_w - 2*margem_int, fundo_h - 2*margem_int
            if max_w_icone_grande <=0 or max_h_icone_grande <=0: return
            escala = min(max_w_icone_grande / img_orig_w, max_h_icone_grande / img_orig_h) 
            if escala > 0:
                nova_w_icone_grande, nova_h_icone_grande = int(img_orig_w * escala), int(img_orig_h * escala)
                if nova_w_icone_grande > 0 and nova_h_icone_grande > 0:
                    img_redim_grande = pygame.transform.scale(img_surf, (nova_w_icone_grande, nova_h_icone_grande))
                    tela.blit(img_redim_grande, (fundo_x + (fundo_w - nova_w_icone_grande)//2, fundo_y + (fundo_h - nova_h_icone_grande)//2))

def recalcular_layout_loja(largura_tela_atual, altura_tela_atual, img_vendedor_surf, margem_padrao, altura_barra_tabs_fixa):
    vendedor_rect = img_vendedor_surf.get_rect(centerx=largura_tela_atual // 2, top=margem_padrao)
    y_pos_abas = vendedor_rect.bottom + margem_padrao // 2
    _y_start_item_list = y_pos_abas + altura_barra_tabs_fixa + int(margem_padrao * 1.5) 
    altura_area_info_inf = 80 
    altura_lista = max(100, altura_tela_atual - _y_start_item_list - altura_area_info_inf - margem_padrao)
    largura_lista = max(200, largura_tela_atual - 2 * margem_padrao)
    area_lista_rect = pygame.Rect(margem_padrao, _y_start_item_list, largura_lista, altura_lista)
    return vendedor_rect, y_pos_abas, area_lista_rect

def run_shop_scene(tela_surface, jogador_obj, largura_inicial, altura_inicial):
    global imagem_vendedor, itens_data_global, fonte_placeholder
    global imagem_Pocao_Cura, imagem_Espada_1, imagem_Espada_2, imagem_Espada_3, imagem_Espada_4, imagem_Espada_5, imagem_Espada_6, imagem_Espada_7
    global imagem_Machado_1, imagem_Machado_2, imagem_Machado_3, imagem_Machado_4, imagem_Machado_5, imagem_Machado_6
    global imagem_Cajado_1, imagem_Cajado_2, imagem_Cajado_3

    largura_tela_atual = largura_inicial; altura_tela_atual = altura_inicial; tela = tela_surface 
    if not pygame.font.get_init(): pygame.font.init()
    if not pygame.font.get_init(): print("ERRO FATAL (Loja Modulo run_shop_scene): pygame.font não pôde ser inicializado."); return False

    tamanho_vendedor_para_carregar = (max(100, int(largura_inicial * 0.45)), max(100, int(altura_inicial * 0.50))) 
    carregar_recursos_loja(tamanho_item=(80,80), tamanho_vendedor_img=tamanho_vendedor_para_carregar)

    itens_data_global["Cajados"] = [
        {"nome": "Cajado da Fixacao Ametista", "preco": 200, "imagem": imagem_Cajado_1, "descricao": "Se não souber usa-lo não compre, uma arma extremamente poderosa mas incontrolável para aqueles que não possuem experiência"},
        {"nome": "Cajado Da santa Natureza", "preco": 300, "imagem": imagem_Cajado_2, "descricao": "Uma arma única rara e que causa medo a todos os monstros da floresta. Esse cajado parece simples mas é feito com a madeira de uma árvore almadiçoada. A natureza estará sempre ao seu lado quando você estiver usando ele."},
        {"nome": "Livro dos impuros", "preco": 450, "imagem": imagem_Cajado_3, "descricao": "Contém conhecimento proibido, pode ser que ele te ensine a dominar alguma arte mística, ou pode ser que ele te enlouqueça até a MORTE."},
    ]
    itens_data_global["Espadas"] = [
        {"nome": "Adaga do Fogo Contudente", "preco": 100, "imagem": imagem_Espada_1, "descricao": "Uma lâmina pequena, mas perigosa, sua ponta ao penetrar inimigos causa uma queimadura"},
        {"nome": "Espada de Fogo azul Sacra Cerulea", "preco": 150, "imagem": imagem_Espada_2, "descricao": "Lâmina de aço cintilante com punho dourado e uma gema safira-azul, forjada sob o calor das estrelas e abençoada com sabedoria celestia. Ela é Leal para os justos e forte para os destemidos."},
        {"nome": "Espada do Olhar Da Penitencia", "preco": 200, "imagem": imagem_Espada_3, "descricao": "Forjada nas profundezas do vazio com essência de pesadelos e almas perdidas. Os antigos portadores alegam ouvir vozes ver espíritos qquando seguravam a espada. Sua lamina vermelha escura e a guarda-mão em formato de chifres exalam malevolência, enquanto um olho no punho absorve a essência dos inimigos para empoderar o portador. É uma arma para quem busca dominação, mas exige um alto preço."},
        {"nome": "Espada Sacra Caida", "preco": 300, "imagem": imagem_Espada_4, "descricao": "Forjada sob a fúria de um Buraco Negro. Sua gema âmbar concede intuição aguçada para antecipar inimigos, sendo ideal para quem valoriza agilidade e estratégia, movendo-se como uma sombra para atacar com precisão."},
        {"nome": "Espada Sacra do Lua", "preco": 450, "imagem": imagem_Espada_5, "descricao": "Espada forjada com rochas lunares, encantada com o poder de uma estrela, ela guiará seus caminhos e voce jamais vai ficar na escuridão"},
        {"nome": "Lâmina do Ceu Centilhante", "preco": 600, "imagem": imagem_Espada_6, "descricao": "Uma chuva de meteoros estava caindo sob este pequeno mundo, os detritos restantes foram forjados junto com o calor de estrelas, gerando uma espada única. "}
    ]
    itens_data_global["Machados"] = [
        {"nome": "Machado Bárbaro Cravejado", "preco": 120, "imagem": imagem_Machado_1, "descricao": "Bruto e eficaz para golpes pesados. Seu material é tão resistente que ele nunca te deixará na mão."},
        {"nome": "Machado Cerúleo da Estrela Cadente", "preco": 250, "imagem": imagem_Machado_2, "descricao": "Forjado com metal celestial, as forças do universo estarão com você para te ajudar no que precisar."},
        {"nome": "Machado da Descida Santa", "preco": 300, "imagem": imagem_Machado_3, "descricao": "Abençoado para purificar o mal, feito com o doce som da arpa de anjos, promete lealdade e confiança ao portador."},
        {"nome": "Machado do Fogo Abrasador", "preco": 400, "imagem": imagem_Machado_4, "descricao": "Feito com as cinzas de fenix, uma arma poderosa feita com a morte de inimigos e que assusta qualquer inimigo que a vê. "},
        {"nome": "Machado do Marfim Resplendor", "preco": 550, "imagem": imagem_Machado_5, "descricao": "Belo e mortal, para aqueles que gostam de exibir suas forças e belezas aos inimigos. Feito com preciosas pedras de esmeralda que ficam reluentes ao segura-lo ."},
        {"nome": "Machado Macabro da Gula Infinita", "preco": 700, "imagem": imagem_Machado_6, "descricao": "Uma arma para quem tem fome de sangue e sede de justiça, uma fabricação sombria que assusta qualquer um"},
    ]
    itens_data_global["Poções"] = [ 
        {"nome": "Poção de Cura", "preco": 50, "imagem": imagem_Pocao_Cura, "descricao": "Restaura uma pequena quantidade de vida quando você mais precisar."},
    ]

    fonte_loja = None; tamanho_fonte_loja = 24 # Tamanho base da fonte
    try: 
        caminho_base_fonte = os.getcwd()
        if os.path.basename(caminho_base_fonte) == "Arquivos":
            caminho_base_fonte = os.path.dirname(caminho_base_fonte)
        caminho_fonte_completo = os.path.join(caminho_base_fonte, FONTE_RETRO_PATH.replace('\\', os.sep))

        if os.path.exists(caminho_fonte_completo):
            fonte_loja = pygame.font.Font(caminho_fonte_completo, tamanho_fonte_loja)
            print(f"DEBUG(Loja Modulo-Run): Fonte retro '{FONTE_RETRO_PATH}' carregada para a loja.")
        else:
            raise FileNotFoundError(f"Fonte não encontrada: {caminho_fonte_completo}")
    except (pygame.error, FileNotFoundError) as e:
        print(f"AVISO(Loja Modulo-Run): Fonte retro não encontrada ou falhou: {e}. Tentando 'Arial'.")
        try:
            fonte_loja = pygame.font.SysFont("Arial", tamanho_fonte_loja)
        except pygame.error:
            print(f"AVISO(Loja Modulo-Run): Fonte 'Arial' não encontrada. Usando fonte padrão do Pygame.")
            fonte_loja = pygame.font.Font(None, tamanho_fonte_loja)

    primeira_categoria_nome = list(itens_data_global.keys())[0] if itens_data_global else ""
    loja_inst = Loja(itens_data_global.get(primeira_categoria_nome, []), fonte_loja, largura_tela_atual, altura_tela_atual)
    nomes_abas = list(itens_data_global.keys())
    aba_atual_indice = 0; ALTURA_BARRA_ABAS_FIXA = 50; MARGEM_GERAL_FIXA = 20 
    mensagem_atual = ""; tempo_exibicao_msg = 0; DURACAO_MSG_FRAMES = 180
    
    vendedor_surf_para_layout = imagem_vendedor if isinstance(imagem_vendedor, pygame.Surface) else imagem_vendedor_placeholder
    if vendedor_surf_para_layout is None: 
        vendedor_surf_para_layout = pygame.Surface((10,10)) 
        print("AVISO(Loja Modulo-Run): imagem_vendedor e placeholder são None. Usando Surface mínima.")

    vendedor_rect_atual, y_pos_barra_abas_atual, area_lista_itens_atual = recalcular_layout_loja(largura_tela_atual, altura_tela_atual, vendedor_surf_para_layout, MARGEM_GERAL_FIXA, ALTURA_BARRA_ABAS_FIXA)
    
    if nomes_abas: 
        desenhar_conteudo_loja(loja_inst, aba_atual_indice, area_lista_itens_atual, itens_data_global)
        loja_inst.selecionar_item(0, area_lista_itens_atual)
    
    rodando_cena = True; clock = pygame.time.Clock()
    while rodando_cena:
        dt_segundos = clock.tick(60) / 1000.0; mouse_pos_atual = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            elif evento.type == pygame.VIDEORESIZE: 
                largura_tela_atual = evento.w; altura_tela_atual = evento.h
                tela = pygame.display.set_mode((largura_tela_atual, altura_tela_atual), pygame.RESIZABLE) 
                vendedor_surf_para_layout_resize = imagem_vendedor if isinstance(imagem_vendedor, pygame.Surface) else imagem_vendedor_placeholder
                if vendedor_surf_para_layout_resize is None: vendedor_surf_para_layout_resize = pygame.Surface((10,10))
                vendedor_rect_atual, y_pos_barra_abas_atual, area_lista_itens_atual = recalcular_layout_loja(largura_tela_atual, altura_tela_atual, vendedor_surf_para_layout_resize, MARGEM_GERAL_FIXA, ALTURA_BARRA_ABAS_FIXA)
                loja_inst.ajustar_scroll(area_lista_itens_atual)
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: return True 
                elif evento.key == pygame.K_UP: loja_inst.mover_selecao("cima", area_lista_itens_atual)
                elif evento.key == pygame.K_DOWN: loja_inst.mover_selecao("baixo", area_lista_itens_atual)
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    if loja_inst.itens: _, _, msg_retorno = loja_inst.comprar_item(jogador_obj); mensagem_atual = msg_retorno; tempo_exibicao_msg = DURACAO_MSG_FRAMES
                elif evento.key == pygame.K_LEFT:
                    if nomes_abas: aba_atual_indice = (aba_atual_indice - 1 + len(nomes_abas)) % len(nomes_abas); desenhar_conteudo_loja(loja_inst, aba_atual_indice, area_lista_itens_atual, itens_data_global); loja_inst.selecionar_item(0, area_lista_itens_atual)
                elif evento.key == pygame.K_RIGHT:
                    if nomes_abas: aba_atual_indice = (aba_atual_indice + 1) % len(nomes_abas); desenhar_conteudo_loja(loja_inst, aba_atual_indice, area_lista_itens_atual, itens_data_global); loja_inst.selecionar_item(0, area_lista_itens_atual)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if nomes_abas:
                    idx_aba_clicada = verificar_clique_mouse_aba(mouse_pos_atual, largura_tela_atual, len(nomes_abas), ALTURA_BARRA_ABAS_FIXA, y_pos_barra_abas_atual)
                    if idx_aba_clicada != -1:
                        if aba_atual_indice != idx_aba_clicada: aba_atual_indice = idx_aba_clicada; desenhar_conteudo_loja(loja_inst, aba_atual_indice, area_lista_itens_atual, itens_data_global); loja_inst.selecionar_item(0, area_lista_itens_atual)
                    else: 
                        item_idx_clicado = loja_inst.selecionar_item_por_posicao(mouse_pos_atual, area_lista_itens_atual)
                        if item_idx_clicado != -1:
                            _, _, msg_retorno = loja_inst.comprar_item(jogador_obj)
                            mensagem_atual = msg_retorno; tempo_exibicao_msg = DURACAO_MSG_FRAMES
            elif evento.type == pygame.MOUSEWHEEL:
                if area_lista_itens_atual.collidepoint(mouse_pos_atual):
                    if evento.y > 0: loja_inst.mover_selecao("cima", area_lista_itens_atual)
                    elif evento.y < 0: loja_inst.mover_selecao("baixo", area_lista_itens_atual)
        
        if tempo_exibicao_msg > 0: tempo_exibicao_msg -= 1
        else: mensagem_atual = ""
        
        loja_inst.update_blink(); loja_inst.update_gold_border()
        tela.fill((30,30,30))
        
        vendedor_blit_surf = imagem_vendedor if isinstance(imagem_vendedor, pygame.Surface) else imagem_vendedor_placeholder
        if vendedor_blit_surf: tela.blit(vendedor_blit_surf, vendedor_rect_atual.topleft)
        
        if fonte_loja and nomes_abas: desenhar_menu_superior(tela, nomes_abas, aba_atual_indice, largura_tela_atual, fonte_loja, y_pos_barra_abas_atual, ALTURA_BARRA_ABAS_FIXA)
        if fonte_loja: desenhar_item_selecionado_detalhes(tela, loja_inst, fonte_loja, vendedor_rect_atual)
        
        pygame.draw.rect(tela, (20,20,20), area_lista_itens_atual, border_radius=8)
        pygame.draw.rect(tela, (150,150,150), area_lista_itens_atual, 2, border_radius=8) 
        if fonte_loja: loja_inst.desenhar(tela, area_lista_itens_atual) 
        
        if hasattr(jogador_obj, 'dinheiro') and fonte_loja: desenhar_dinheiro(tela, jogador_obj.dinheiro, fonte_loja, largura_tela_atual, altura_tela_atual)
        if fonte_loja: desenhar_mensagem(tela, mensagem_atual, fonte_loja, largura_tela_atual, altura_tela_atual)
        
        pygame.display.flip()
    return True
