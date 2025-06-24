# inventario_barra.py
import pygame
import os
import random
import sys

# --- CONSTANTES ---
DEFAULT_WEAPON_ICON_PATH = "Sprites/Armas/Espadas/Adaga/Adaga E-1.png"

# Tenta importar a classe Weapon real. Se falhar, usa um placeholder.
try:
    from Armas.weapon import Weapon 
except ImportError:
    class Weapon: # Placeholder se a classe Weapon real não for encontrada
        def __init__(self, name="Arma Desconhecida", ui_icon_path=None, damage=10, attack_range=50, cooldown=0.5, hitbox_dimensions=(0,0), hitbox_offset=(0,0)):
            self.name = name
            self.ui_icon_path = ui_icon_path 
            self._base_name = name # Para evitar duplicatas da mesma arma base
            self.level = 1
            self.damage = damage
            self.attack_range = attack_range
            self.cooldown = cooldown
            self.hitbox_width = hitbox_dimensions[0]
            self.hitbox_height = hitbox_dimensions[1]
            self.hitbox_offset_x = hitbox_offset[0]
            self.hitbox_offset_y = hitbox_offset[1]
            self.attack_animation_sprites = [] 
            self.attack_animation_paths = []   
            self.attack_animation_speed = 100  
            self.current_attack_animation_frame = 0
            self.last_attack_animation_update = 0
            self.animation_display_scale_factor = 1.0
        def get_current_attack_animation_sprite(self): 
            return None # Placeholder

# Placeholders para classes de armas específicas, caso não sejam encontradas
# (útil para o bloco de teste standalone)
if 'AdagaFogo' not in globals(): AdagaFogo = None 
if 'EspadaBrasas' not in globals(): EspadaBrasas = None

# Configuração do sys.path para importações relativas no teste standalone
if __name__ == '__main__':
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir_test = current_file_dir
    if os.path.basename(current_file_dir).lower() == "arquivos" and \
       os.path.basename(os.path.dirname(current_file_dir)).lower() != "testes_isolados":
        potential_root = os.path.dirname(current_file_dir)
        if os.path.isdir(os.path.join(potential_root, "Armas")) or \
           os.path.isdir(os.path.join(potential_root, "Sprites")):
            project_root_dir_test = potential_root
    
    if project_root_dir_test not in sys.path:
        sys.path.insert(0, project_root_dir_test)
    
    armas_dir = os.path.join(project_root_dir_test, "Armas")
    if os.path.isdir(armas_dir) and armas_dir not in sys.path:
        sys.path.insert(0, armas_dir)

# Tenta importar as classes de armas novamente após ajustar o path (para o teste)
try: from Armas.AdagaFogo import AdagaFogo
except ImportError: AdagaFogo = None
try: from Armas.EspadaBrasas import EspadaBrasas
except ImportError: EspadaBrasas = None


# Cores
COR_FUNDO_SLOT = (70, 70, 70, 210)
COR_BORDA_SLOT = (120, 120, 120)
COR_BORDA_SELECIONADA = (255, 223, 0) # Amarelo para seleção
COR_BORDA_EQUIPADA = (50, 205, 50) # Verde para equipado
COR_TEXTO_TECLA_ATALHO = (220, 220, 220)
COR_FUNDO_PAINEL_CENTRAL = (35, 35, 35, 240)
COR_BORDA_PAINEL_CENTRAL = (100, 100, 100)
COR_TEXTO_TITULO_INVENTARIO = (230, 230, 230)
COR_TEXTO_NOME_ARMA_DETALHE = (255, 255, 255)
COR_LOSANGO_BORDA = (140, 140, 140) 
COR_LOSANGO_PONTA_SELECIONADA = COR_BORDA_SELECIONADA
COR_TEXTO_DINHEIRO = (255, 215, 0) # Dourado para o dinheiro

# Espessuras para o losango
ESPESSURA_LOSANGO_NORMAL = 2
ESPESSURA_LOSANGO_PONTA_SELECIONADA = 3


class BarraInventario:
    def __init__(self, largura_tela, altura_tela, num_slots=4, slot_tamanho=(60, 60), espacamento=10):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        self.num_slots = num_slots # A barra sempre terá este número de slots visuais
        if self.num_slots != 4: # Mantém a lógica para layout em cruz
            self.num_slots = 4

        self.slot_tamanho = slot_tamanho
        self.espacamento = espacamento

        self.slot_rects = [pygame.Rect(0,0,0,0)] * self.num_slots # Rects para a UI dos slots

        self.item_selecionado_index = 0 # Índice do slot visualmente selecionado (0 a num_slots-1)
        self._icon_cache = {}
        self.visivel = False

        try:
            pygame.font.init()
            self.fonte_tecla_atalho = pygame.font.Font(None, 24)
            self.fonte_nome_arma_fullview = pygame.font.Font(None, 26)
            self.fonte_titulo_inventario = pygame.font.Font(None, 32)
            self.fonte_dinheiro = pygame.font.Font(None, 28) # Fonte para o dinheiro
        except pygame.error as e:
            self.fonte_tecla_atalho = pygame.font.SysFont("arial", 20)
            self.fonte_nome_arma_fullview = pygame.font.SysFont("arial", 22)
            self.fonte_titulo_inventario = pygame.font.SysFont("arial", 28)
            self.fonte_dinheiro = pygame.font.SysFont("arial", 24)

        self._calcular_rects_painel_central()

    def _calcular_rects_painel_central(self):
        centro_x_tela = self.largura_tela // 2
        centro_y_tela = self.altura_tela // 2
        slot_w, slot_h = self.slot_tamanho
        offset_do_centro = 150 
        rect_top = pygame.Rect(0, 0, slot_w, slot_h)
        rect_top.center = (centro_x_tela, centro_y_tela - offset_do_centro)
        rect_direita_para_slot2 = pygame.Rect(0, 0, slot_w, slot_h)
        rect_direita_para_slot2.center = (centro_x_tela + offset_do_centro, centro_y_tela)
        rect_bottom = pygame.Rect(0, 0, slot_w, slot_h)
        rect_bottom.center = (centro_x_tela, centro_y_tela + offset_do_centro)
        rect_esquerda_para_slot4 = pygame.Rect(0, 0, slot_w, slot_h)
        rect_esquerda_para_slot4.center = (centro_x_tela - offset_do_centro, centro_y_tela)
        self.slot_rects = [rect_top, rect_direita_para_slot2, rect_bottom, rect_esquerda_para_slot4]
        min_x = min(r.left for r in self.slot_rects)
        max_x = max(r.right for r in self.slot_rects)
        min_y = min(r.top for r in self.slot_rects)
        max_y = max(r.bottom for r in self.slot_rects)
        padding_painel = self.espacamento * 2
        altura_titulo = 45 
        altura_nome_arma = 40 
        painel_largura = (max_x - min_x) + padding_painel * 2
        painel_altura_total = (max_y - min_y) + altura_titulo + altura_nome_arma + padding_painel * 2.5
        painel_x = centro_x_tela - painel_largura // 2
        painel_y = self.slot_rects[0].top - padding_painel - altura_titulo
        self.rect_painel_fundo = pygame.Rect(painel_x, painel_y, painel_largura, painel_altura_total)

    def _get_project_root(self):
        current_file_path = os.path.abspath(__file__)
        path_parts = current_file_path.lower().split(os.sep)
        if "arquivos" in path_parts and len(path_parts) > path_parts.index("arquivos"):
            arquivos_index = path_parts.index("arquivos")
            if arquivos_index > 0 and path_parts[arquivos_index-1] != "testes_isolados":
                 return os.path.dirname(os.path.dirname(current_file_path))
        if "testes_isolados" in path_parts and "arquivos" in path_parts:
            if path_parts.index("arquivos") > path_parts.index("testes_isolados"):
                return os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
        temp_path = os.path.dirname(current_file_path)
        for _ in range(3): 
            if os.path.isdir(os.path.join(temp_path, "Sprites")) or \
               os.path.isdir(os.path.join(temp_path, "Armas")):
                return temp_path
            parent = os.path.dirname(temp_path)
            if parent == temp_path: 
                break
            temp_path = parent
        return os.path.dirname(current_file_path) 

    def _load_image_from_path(self, image_path_relativo_ao_projeto, cache_key_prefix="icon"):
        if not image_path_relativo_ao_projeto: return None
        project_root = self._get_project_root()
        normalized_path_parts = image_path_relativo_ao_projeto.replace("\\", "/").split("/")
        full_path = os.path.join(project_root, *normalized_path_parts)
        
        # Cria uma chave de cache baseada no prefixo e no caminho normalizado
        # Substitui separadores de diretório por underscores para uma chave mais robusta
        cache_key = f"{cache_key_prefix}_{image_path_relativo_ao_projeto.replace(os.sep, '_').replace('/', '_')}"

        if cache_key in self._icon_cache: return self._icon_cache[cache_key]
        
        tamanho_icone_desejado = (self.slot_tamanho[0] - 12, self.slot_tamanho[1] - 12)
        if os.path.exists(full_path):
            try:
                icone_surface = pygame.image.load(full_path).convert_alpha()
                icone_surface = pygame.transform.smoothscale(icone_surface, tamanho_icone_desejado)
                self._icon_cache[cache_key] = icone_surface # Armazena no cache
                return icone_surface
            except pygame.error as e:
                # Em caso de erro ao carregar, não armazena nada e retorna None abaixo
                pass
        return None # Retorna None se o arquivo não existe ou houve erro

    def _carregar_icone_arma(self, arma_instancia: Weapon) -> pygame.Surface | None:
        if not isinstance(arma_instancia, Weapon): return None
        nome_arma = arma_instancia.name if hasattr(arma_instancia, 'name') else "???"
        
        # Chave de cache para o placeholder específico desta arma
        # Usar um prefixo distinto para placeholders para evitar colisões com ícones reais
        placeholder_cache_key = f"placeholder_icon_{nome_arma.replace(' ', '_')}"
        if placeholder_cache_key in self._icon_cache:
            return self._icon_cache[placeholder_cache_key]

        caminho_especifico = getattr(arma_instancia, 'ui_icon_path', None)
        if caminho_especifico:
            # _load_image_from_path já lida com o cache para ícones carregados de arquivos
            icone = self._load_image_from_path(caminho_especifico, cache_key_prefix=f"icon_{nome_arma.replace(' ', '_')}")
            if icone: return icone 
        
        icone_default = self._load_image_from_path(DEFAULT_WEAPON_ICON_PATH, cache_key_prefix="default_icon")
        if icone_default: return icone_default
        
        # Se chegou aqui, nem o específico nem o default foram encontrados/carregados.
        # Cria o placeholder, armazena em cache e retorna.
        placeholder_icone = self._criar_icone_placeholder_arma(nome_arma)
        if placeholder_icone: 
            self._icon_cache[placeholder_cache_key] = placeholder_icone
        return placeholder_icone

    def _criar_icone_placeholder_arma(self, nome_arma="?", tamanho_icone=None):
        if tamanho_icone is None:
            tamanho_icone = (self.slot_tamanho[0] - 12, self.slot_tamanho[1] - 12)
        placeholder = pygame.Surface(tamanho_icone, pygame.SRCALPHA) 
        # A cor aleatória é gerada uma vez quando o placeholder é criado pela primeira vez para uma arma
        cor_r, cor_g, cor_b = random.randint(60, 180), random.randint(60, 180), random.randint(60, 180)
        placeholder.fill((cor_r, cor_g, cor_b, 200)) 
        try:
            fonte_placeholder = pygame.font.Font(None, int(tamanho_icone[1]*0.7)) 
            texto_renderizado = nome_arma[0].upper() if nome_arma and len(nome_arma)>0 else "?"
            texto_surface = fonte_placeholder.render(texto_renderizado, True, (255,255,255)) 
            rect_texto = texto_surface.get_rect(center=(tamanho_icone[0]//2, tamanho_icone[1]//2))
            placeholder.blit(texto_surface, rect_texto)
        except Exception as e:
            pass 
        return placeholder

    def handle_input(self, evento, jogador_ref):
        if not hasattr(jogador_ref, 'owned_weapons') or not hasattr(jogador_ref, 'equip_weapon'):
            return False 

        if evento.type == pygame.KEYDOWN:
            novo_slot_selecionado_teclado = -1
            if evento.key == pygame.K_1: novo_slot_selecionado_teclado = 0
            elif evento.key == pygame.K_2: novo_slot_selecionado_teclado = 1
            elif evento.key == pygame.K_3: novo_slot_selecionado_teclado = 2
            elif evento.key == pygame.K_4: novo_slot_selecionado_teclado = 3

            if 0 <= novo_slot_selecionado_teclado < self.num_slots:
                self.item_selecionado_index = novo_slot_selecionado_teclado
                if novo_slot_selecionado_teclado < len(jogador_ref.owned_weapons):
                    arma_para_equipar = jogador_ref.owned_weapons[novo_slot_selecionado_teclado]
                    if arma_para_equipar: 
                        jogador_ref.equip_weapon(arma_para_equipar)
                return False 

        elif evento.type == pygame.MOUSEBUTTONDOWN and self.visivel:
            if evento.button == 1: 
                mouse_pos = pygame.mouse.get_pos()
                if self.rect_painel_fundo.collidepoint(mouse_pos):
                    for i, slot_rect in enumerate(self.slot_rects):
                        if slot_rect.collidepoint(mouse_pos):
                            self.item_selecionado_index = i
                            if i < len(jogador_ref.owned_weapons):
                                arma_para_equipar = jogador_ref.owned_weapons[i]
                                if arma_para_equipar:
                                    jogador_ref.equip_weapon(arma_para_equipar)
                            return True 
                    return True 
                else:
                    self.toggle_visibilidade(jogador_ref) 
                    return True 
        return False 

    def toggle_visibilidade(self, jogador_ref):
        self.visivel = not self.visivel
        if self.visivel:
            arma_equipada_jogador = getattr(jogador_ref, 'current_weapon', None)
            if arma_equipada_jogador and hasattr(jogador_ref, 'owned_weapons'):
                encontrou_equipada = False
                for i, arma_no_slot in enumerate(jogador_ref.owned_weapons):
                    if i < self.num_slots and arma_no_slot is arma_equipada_jogador:
                        self.item_selecionado_index = i
                        encontrou_equipada = True
                        break
                if not encontrou_equipada: 
                    self.item_selecionado_index = 0 
            else:
                self.item_selecionado_index = 0

    def desenhar(self, tela, jogador_ref):
        if not self.visivel:
            return

        arma_equipada_jogador = getattr(jogador_ref, 'current_weapon', None)
        armas_do_jogador = getattr(jogador_ref, 'owned_weapons', [])
        dinheiro_jogador = getattr(jogador_ref, 'dinheiro', 0)
        nome_arma_para_exibir = "" 

        fundo_inv_surface = pygame.Surface(self.rect_painel_fundo.size, pygame.SRCALPHA)
        fundo_inv_surface.fill(COR_FUNDO_PAINEL_CENTRAL)
        tela.blit(fundo_inv_surface, self.rect_painel_fundo.topleft)
        pygame.draw.rect(tela, COR_BORDA_PAINEL_CENTRAL, self.rect_painel_fundo, 3, border_radius=7)
        titulo_surface = self.fonte_titulo_inventario.render("Inventário de Armas", True, COR_TEXTO_TITULO_INVENTARIO)
        titulo_rect = titulo_surface.get_rect(centerx=self.rect_painel_fundo.centerx, top=self.rect_painel_fundo.top + self.espacamento)
        tela.blit(titulo_surface, titulo_rect)

        cx = self.largura_tela // 2
        cy = self.altura_tela // 2
        offset_losango = 30 
        p_sup = (cx, cy - offset_losango)    
        p_dir = (cx + offset_losango, cy)    
        p_inf = (cx, cy + offset_losango)    
        p_esq = (cx - offset_losango, cy)    
        pontos_losango = [p_sup, p_dir, p_inf, p_esq]
        pygame.draw.polygon(tela, COR_LOSANGO_BORDA, pontos_losango, ESPESSURA_LOSANGO_NORMAL)
        idx = self.item_selecionado_index
        cor_ponta = COR_LOSANGO_PONTA_SELECIONADA
        espessura_ponta = ESPESSURA_LOSANGO_PONTA_SELECIONADA
        if idx == 0: 
            pygame.draw.line(tela, cor_ponta, p_esq, p_sup, espessura_ponta)
            pygame.draw.line(tela, cor_ponta, p_sup, p_dir, espessura_ponta)
        elif idx == 1: 
            pygame.draw.line(tela, cor_ponta, p_sup, p_dir, espessura_ponta)
            pygame.draw.line(tela, cor_ponta, p_dir, p_inf, espessura_ponta)
        elif idx == 2: 
            pygame.draw.line(tela, cor_ponta, p_dir, p_inf, espessura_ponta)
            pygame.draw.line(tela, cor_ponta, p_inf, p_esq, espessura_ponta)
        elif idx == 3: 
            pygame.draw.line(tela, cor_ponta, p_inf, p_esq, espessura_ponta)
            pygame.draw.line(tela, cor_ponta, p_esq, p_sup, espessura_ponta)

        for i, slot_rect in enumerate(self.slot_rects):
            fundo_surface_slot = pygame.Surface(self.slot_tamanho, pygame.SRCALPHA)
            fundo_surface_slot.fill(COR_FUNDO_SLOT)
            tela.blit(fundo_surface_slot, slot_rect.topleft)

            arma_no_slot_visual = None
            if i < len(armas_do_jogador): 
                arma_no_slot_visual = armas_do_jogador[i]

            cor_borda = COR_BORDA_SLOT
            espessura_borda = 2
            
            if arma_no_slot_visual and arma_equipada_jogador and arma_no_slot_visual is arma_equipada_jogador:
                cor_borda = COR_BORDA_EQUIPADA
                espessura_borda = 3
            elif i == self.item_selecionado_index: 
                cor_borda = COR_BORDA_SELECIONADA
                espessura_borda = 3

            pygame.draw.rect(tela, cor_borda, slot_rect, espessura_borda, border_radius=5)

            if arma_no_slot_visual:
                icone = self._carregar_icone_arma(arma_no_slot_visual) # Agora usa o cache para placeholders
                if icone:
                    icone_rect = icone.get_rect(center=slot_rect.center)
                    tela.blit(icone, icone_rect)
                if i == self.item_selecionado_index: 
                    nome_arma_para_exibir = arma_no_slot_visual.name
            
            if i == self.item_selecionado_index and not arma_no_slot_visual:
                nome_arma_para_exibir = "" 

            texto_atalho = self.fonte_tecla_atalho.render(str(i + 1), True, COR_TEXTO_TECLA_ATALHO)
            tela.blit(texto_atalho, (slot_rect.left + 5, slot_rect.top + 3))

        if nome_arma_para_exibir: 
            nome_arma_surface = self.fonte_nome_arma_fullview.render(nome_arma_para_exibir, True, COR_TEXTO_NOME_ARMA_DETALHE)
            pos_y_nome = self.rect_painel_fundo.bottom - self.espacamento - nome_arma_surface.get_height() // 2 - 10 
            nome_arma_rect = nome_arma_surface.get_rect(centerx=self.rect_painel_fundo.centerx, centery=pos_y_nome)
            tela.blit(nome_arma_surface, nome_arma_rect)
        
        texto_dinheiro_str = f"Dinheiro: {dinheiro_jogador}"
        surface_dinheiro = self.fonte_dinheiro.render(texto_dinheiro_str, True, COR_TEXTO_DINHEIRO)
        rect_dinheiro = surface_dinheiro.get_rect(left=self.espacamento, bottom=self.altura_tela - self.espacamento)
        tela.blit(surface_dinheiro, rect_dinheiro)


# --- Bloco para Teste Standalone ---
if __name__ == '__main__':
    pygame.init()
    LARGURA_TELA_TESTE = 800
    ALTURA_TELA_TESTE = 600
    tela_teste = pygame.display.set_mode((LARGURA_TELA_TESTE, ALTURA_TELA_TESTE))
    pygame.display.set_caption("Teste da Barra de Inventário (Integrado)")
    clock = pygame.time.Clock()

    class MockJogador: 
        def __init__(self):
            self.dinheiro = 500 
            self.owned_weapons: list[Weapon | None] = [None] * 4 
            self.current_weapon: Weapon | None = None
            self.max_owned_weapons = 4 

        def equip_weapon(self, weapon_instance: Weapon | None):
            if weapon_instance is None or weapon_instance in self.owned_weapons:
                self.current_weapon = weapon_instance

        def add_owned_weapon(self, weapon_object: Weapon, slot_index: int | None = None):
            if not isinstance(weapon_object, Weapon): return False
            if any(w and w._base_name == weapon_object._base_name for w in self.owned_weapons if w):
                return False
            if slot_index is not None and 0 <= slot_index < self.max_owned_weapons:
                if self.owned_weapons[slot_index] is None:
                    self.owned_weapons[slot_index] = weapon_object
                    if self.current_weapon is None: self.equip_weapon(weapon_object)
                    return True
            else: 
                for i in range(self.max_owned_weapons):
                    if self.owned_weapons[i] is None:
                        self.owned_weapons[i] = weapon_object
                        if self.current_weapon is None: self.equip_weapon(weapon_object)
                        return True
            return False 

    mock_jogador = MockJogador()
    
    arma_teste_1 = None
    if AdagaFogo: arma_teste_1 = AdagaFogo()
    else: arma_teste_1 = Weapon(name="Adaga Fogo T", ui_icon_path="Sprites/Armas/Espadas/Adaga/Adaga E-1.png")
    
    arma_teste_2 = None
    if EspadaBrasas: arma_teste_2 = EspadaBrasas()
    else: arma_teste_2 = Weapon(name="Espada Brasas T", ui_icon_path="Sprites/Armas/Espadas/Espada Longa/Espada Longa E-1.png")

    arma_teste_3 = Weapon(name="Machado Teste", ui_icon_path="Caminho/Invalido_Para_Testar_Placeholder.png") # Forçar placeholder
    arma_teste_4_sem_icone = Weapon(name="Lança Teste") # Forçar placeholder via default e depois _criar_icone_placeholder

    if arma_teste_1: mock_jogador.add_owned_weapon(arma_teste_1, 0)
    if arma_teste_2: mock_jogador.add_owned_weapon(arma_teste_2, 1)
    mock_jogador.add_owned_weapon(arma_teste_3, 2)
    mock_jogador.add_owned_weapon(arma_teste_4_sem_icone, 3)


    if mock_jogador.owned_weapons[0]:
        mock_jogador.equip_weapon(mock_jogador.owned_weapons[0])
    
    barra_teste = BarraInventario(LARGURA_TELA_TESTE, ALTURA_TELA_TESTE, num_slots=4, slot_tamanho=(70,70), espacamento=15)
    
    if mock_jogador.current_weapon:
        try:
            # Garante que owned_weapons não tenha Nones inesperados ao buscar o índice
            valid_owned_weapons = [w for w in mock_jogador.owned_weapons if w is not None]
            if mock_jogador.current_weapon in valid_owned_weapons:
                 barra_teste.item_selecionado_index = valid_owned_weapons.index(mock_jogador.current_weapon)
            # Se a arma atual não estiver na lista (ou for None), o item_selecionado_index
            # será tratado pelo toggle_visibilidade ou permanecerá 0.
        except ValueError:
            barra_teste.item_selecionado_index = 0 
    else:
         barra_teste.item_selecionado_index = 0
    
    barra_teste.visivel = True 

    rodando_teste = True
    while rodando_teste:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando_teste = False
            
            evento_controlou_inventario = barra_teste.handle_input(event, mock_jogador)

            if not evento_controlou_inventario: 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if barra_teste.visivel:
                            barra_teste.toggle_visibilidade(mock_jogador)
                        else:
                            rodando_teste = False 
                    elif event.key == pygame.K_TAB:
                        barra_teste.toggle_visibilidade(mock_jogador)
        
        tela_teste.fill((30, 30, 30)) 
        barra_teste.desenhar(tela_teste, mock_jogador) 
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()
