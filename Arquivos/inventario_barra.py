import pygame
import os
import random
import sys

# --- CONSTANTES ---
# Caminho para um ícone padrão, relativo à raiz do projeto (ex: Jogo/)
# Certifique-se que este arquivo exista ou o placeholder será usado.
DEFAULT_WEAPON_ICON_PATH = os.path.join("Sprites", "Interface", "Icons", "default_weapon_icon.png")

# Tenta importar a classe Weapon real. Se falhar, usa um placeholder.
try:
    # Assumindo que a pasta 'Armas' está na raiz do projeto ou acessível via PYTHONPATH
    from Armas.weapon import Weapon
except ImportError:
    print("ALERTA(BarraInventario): Classe 'Weapon' não encontrada em Armas.weapon. Usando placeholder.")
    class Weapon: # Placeholder se a classe Weapon real não for encontrada
        def __init__(self, name="Arma Desconhecida", ui_icon_path=None, damage=10, attack_range=50, cooldown=0.5, hitbox_dimensions=(0,0), hitbox_offset=(0,0), attack_animation_sprites=None, attack_animation_speed=100):
            self.name = name
            # Se ui_icon_path não for fornecido, usa o DEFAULT_WEAPON_ICON_PATH
            self.ui_icon_path = ui_icon_path if ui_icon_path else DEFAULT_WEAPON_ICON_PATH
            self._base_name = name
            self.level = 1
            self.damage = damage
            self.attack_range = attack_range
            self.cooldown = cooldown
            self.hitbox_width = hitbox_dimensions[0]
            self.hitbox_height = hitbox_dimensions[1]
            self.hitbox_offset_x = hitbox_offset[0]
            self.hitbox_offset_y = hitbox_offset[1]
            self.attack_animation_sprites = attack_animation_sprites if attack_animation_sprites else []
            self.attack_animation_speed = attack_animation_speed
            self.current_attack_animation_frame = 0
            self.last_attack_animation_update = 0
            self.animation_display_scale_factor = 1.0
            # Adiciona atributos que a classe base Weapon real pode ter e que AdagaFogo usa
            self.ui_icon_surface = None
            self.attack_effect_sprite_path = None
            self.attack_effect_scale = 1.0
            self.attack_effect_original_image = None
            self.attack_effect_image = None

        def get_current_attack_animation_sprite(self):
            if self.attack_animation_sprites and self.current_attack_animation_frame < len(self.attack_animation_sprites):
                return self.attack_animation_sprites[self.current_attack_animation_frame]
            return None

        # Métodos mock que a AdagaFogo pode chamar na superclasse
        def _get_project_root(self):
            # Este placeholder precisa de uma lógica para encontrar a raiz do projeto
            # para carregar seu próprio DEFAULT_WEAPON_ICON_PATH
            current_file_abs_path = os.path.abspath(__file__)
            dir_barra = os.path.dirname(current_file_abs_path)
            project_root_guess = os.path.dirname(dir_barra)
            if os.path.isdir(os.path.join(project_root_guess, "Sprites")): # Verifica se parece a raiz
                 return project_root_guess
            return dir_barra # Fallback para o diretório da BarraInventario

        def _load_ui_icon_sprite(self):
            project_r = self._get_project_root()
            if self.ui_icon_path and project_r:
                full_path = os.path.join(project_r, self.ui_icon_path.lstrip(os.sep))
                if os.path.exists(full_path):
                    try:
                        self.ui_icon_surface = pygame.image.load(full_path).convert_alpha()
                    except Exception as e:
                        print(f"ERRO(Placeholder Weapon): Falha ao carregar ícone placeholder '{full_path}': {e}")
                        self.ui_icon_surface = None
                else:
                    self.ui_icon_surface = None
            else:
                self.ui_icon_surface = None

        def _load_attack_effect_sprite(self): # Mock
            pass


# --- Tentativas de Importação de Armas Específicas (para teste standalone) ---
AdagaFogo = None
EspadaBrasas = None

# Bloco para configurar caminhos de importação (especialmente para testes standalone)
project_root_for_import = None
try:
    current_file_dir_for_import = os.path.dirname(os.path.abspath(__file__))
    temp_root = current_file_dir_for_import
    for _ in range(3): # Tenta subir até 3 níveis
        if os.path.isdir(os.path.join(temp_root, "Arquivos", "Armas")) or \
           os.path.isdir(os.path.join(temp_root, "Sprites")) or \
           os.path.exists(os.path.join(temp_root, "main.py")):
            project_root_for_import = temp_root
            break
        parent_dir = os.path.dirname(temp_root)
        if parent_dir == temp_root:
            break
        temp_root = parent_dir

    if not project_root_for_import:
        project_root_for_import = os.path.dirname(current_file_dir_for_import)
        # print(f"ALERTA(BarraInventario Imports): Raiz do projeto não determinada com certeza. Usando: {project_root_for_import}")

    # print(f"DEBUG(BarraInventario Imports): Raiz do projeto para imports (teste): {project_root_for_import}")

    if project_root_for_import not in sys.path:
        sys.path.insert(0, project_root_for_import)
        # print(f"DEBUG(BarraInventario Imports): Adicionado ao sys.path: {project_root_for_import}")

    from Arquivos.Armas.AdagaFogo import AdagaFogo
    # from Armas.EspadaBrasas import EspadaBrasas # Mantenha comentado se não existir
    # print("DEBUG(BarraInventario Imports): Importações de AdagaFogo (para teste) tentadas.")

except ImportError as e:
    # print(f"ALERTA(BarraInventario Imports): Falha ao importar classes de armas para teste: {e}.")
    # print(f"   sys.path atual: {sys.path}")
    pass
except Exception as e_gen:
    # print(f"ERRO(BarraInventario Imports): Erro inesperado durante configuração de importação: {e_gen}")
    pass


# Cores
COR_FUNDO_SLOT = (70, 70, 70, 200)
COR_BORDA_SLOT = (120, 120, 120, 220)
COR_BORDA_SELECIONADA = (236, 100, 0, 255)
COR_BORDA_EQUIPADA = (60, 180, 236, 255)
COR_TEXTO_TECLA_ATALHO = (230, 230, 230)
COR_FUNDO_PAINEL_CENTRAL = (35, 35, 35, 230)
COR_BORDA_PAINEL_CENTRAL = (100, 100, 100, 240)
COR_TEXTO_TITULO_INVENTARIO = (230, 230, 230)
COR_TEXTO_NOME_ARMA_DETALHE = (255, 255, 255)
COR_LOSANGO_BORDA = (140, 140, 140, 200)
COR_LOSANGO_PONTA_SELECIONADA = COR_BORDA_SELECIONADA
COR_TEXTO_DINHEIRO = (255, 215, 0)
COR_FUNDO_LOSANGO_CENTRAL = (50, 50, 50, 180)

# Espessuras e Raios
ESPESSURA_LOSANGO_NORMAL = 2
ESPESSURA_LOSANGO_PONTA_SELECIONADA = 3
ESPESSURA_BORDA_ICONE_CENTRAL = 2
RAIO_BORDA_ICONE_CENTRAL = 5
RAIO_BORDA_SLOT = 5


class BarraInventario:
    def __init__(self, x, y, largura_tela, altura_tela, num_slots_hud=4, slot_tamanho=(70, 70), espacamento=8):
        self.largura_tela_original = largura_tela
        self.altura_tela_original = altura_tela

        self.pos_x_hud = x
        self.pos_y_hud = y

        self.num_slots_hud = num_slots_hud
        self.num_slots_painel = 4 # Para o painel central em forma de losango

        self.slot_tamanho_hud = slot_tamanho
        self.espacamento_hud = espacamento

        self.slot_rects_hud = [pygame.Rect(0,0,0,0)] * self.num_slots_hud
        self.slot_rects_painel = [pygame.Rect(0,0,0,0)] * self.num_slots_painel

        self.item_selecionado_index_painel = 0

        self._icon_cache = {}
        self.visao_inventario_aberta = False

        try:
            pygame.font.init()
            self.fonte_tecla_atalho = pygame.font.Font(None, 22)
            self.fonte_nome_arma_fullview = pygame.font.Font(None, 24)
            self.fonte_titulo_inventario = pygame.font.Font(None, 30)
            self.fonte_dinheiro = pygame.font.Font(None, 26)
        except pygame.error as e:
            # print(f"DEBUG(InventarioBarra): Erro ao carregar fontes Pygame: {e}. Usando SysFont.")
            self.fonte_tecla_atalho = pygame.font.SysFont("arial", 18)
            self.fonte_nome_arma_fullview = pygame.font.SysFont("arial", 20)
            self.fonte_titulo_inventario = pygame.font.SysFont("arial", 26)
            self.fonte_dinheiro = pygame.font.SysFont("arial", 22)
        except Exception as e_font:
            # print(f"ERRO(InventarioBarra): Erro inesperado ao carregar fontes: {e_font}. Usando SysFont.")
            self.fonte_tecla_atalho = pygame.font.SysFont("arial", 18)
            self.fonte_nome_arma_fullview = pygame.font.SysFont("arial", 20)
            self.fonte_titulo_inventario = pygame.font.SysFont("arial", 26)
            self.fonte_dinheiro = pygame.font.SysFont("arial", 22)

        self._calcular_rects_painel_central()
        self._calcular_rects_barra_rapida()

    def _calcular_rects_painel_central(self):
        centro_x_tela = self.largura_tela_original // 2
        centro_y_tela = self.altura_tela_original // 2

        slot_w, slot_h = self.slot_tamanho_hud
        offset_do_centro_slots = 130 # Distância do centro da tela para o centro de cada slot do painel

        # Define os rects dos 4 slots do painel em forma de losango
        rect_top = pygame.Rect(0, 0, slot_w, slot_h)
        rect_top.center = (centro_x_tela, centro_y_tela - offset_do_centro_slots)
        rect_direita = pygame.Rect(0, 0, slot_w, slot_h)
        rect_direita.center = (centro_x_tela + offset_do_centro_slots, centro_y_tela)
        rect_bottom = pygame.Rect(0, 0, slot_w, slot_h)
        rect_bottom.center = (centro_x_tela, centro_y_tela + offset_do_centro_slots)
        rect_esquerda = pygame.Rect(0, 0, slot_w, slot_h)
        rect_esquerda.center = (centro_x_tela - offset_do_centro_slots, centro_y_tela)

        self.slot_rects_painel = [rect_top, rect_direita, rect_bottom, rect_esquerda]

        # Calcula o rect do painel de fundo que engloba os slots e outros elementos
        min_x_slots = min(r.left for r in self.slot_rects_painel)
        max_x_slots = max(r.right for r in self.slot_rects_painel)
        min_y_slots = min(r.top for r in self.slot_rects_painel)
        max_y_slots = max(r.bottom for r in self.slot_rects_painel)

        padding_painel_externo = self.espacamento_hud * 2.5
        altura_area_titulo = 45
        altura_area_nome_arma = 40
        altura_area_dinheiro = 35

        painel_largura = (max_x_slots - min_x_slots) + padding_painel_externo * 2

        painel_y_inicio = min_y_slots - altura_area_titulo - self.espacamento_hud # Acima do slot superior
        painel_y_fim = max_y_slots + altura_area_nome_arma + altura_area_dinheiro + self.espacamento_hud * 1.5 # Abaixo do slot inferior
        painel_altura_total = painel_y_fim - painel_y_inicio

        painel_x_inicio = centro_x_tela - painel_largura // 2
        self.rect_painel_fundo = pygame.Rect(painel_x_inicio, painel_y_inicio, painel_largura, painel_altura_total)

    def _calcular_rects_barra_rapida(self):
        start_x = self.pos_x_hud
        slot_w, slot_h = self.slot_tamanho_hud
        for i in range(self.num_slots_hud):
            rect_x = start_x + i * (slot_w + self.espacamento_hud)
            self.slot_rects_hud[i] = pygame.Rect(rect_x, self.pos_y_hud, slot_w, slot_h)

    def _get_project_root(self) -> str:
        """
        Tenta determinar a raiz do projeto (ex: 'Jogo/') subindo na árvore de diretórios
        a partir do local deste arquivo (BarraInventario.py).
        Assume que BarraInventario.py está em uma subpasta da raiz do projeto.
        """
        current_file_abs_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file_abs_path)
        project_root_candidate = os.path.dirname(current_dir)

        if os.path.isdir(os.path.join(project_root_candidate, "Sprites")) and \
           (os.path.isdir(os.path.join(project_root_candidate, "Armas")) or \
            os.path.isdir(os.path.join(project_root_candidate, "Arquivos", "Armas"))):
            return project_root_candidate

        if os.path.isdir(os.path.join(current_dir, "Sprites")) and \
           (os.path.isdir(os.path.join(current_dir, "Armas")) or \
            os.path.isdir(os.path.join(current_dir, "Arquivos", "Armas"))):
            return current_dir

        # print(f"ALERTA(BarraInventario _get_project_root): Não foi possível determinar a raiz do projeto com certeza. Usando fallback: {current_dir}. Verifique os caminhos dos assets.")
        return current_dir

    def _load_image_from_path(self, image_path_relativo_ao_projeto: str, cache_key_prefix="icon", novo_tamanho=None) -> pygame.Surface | None:
        if not image_path_relativo_ao_projeto:
            return None

        project_root = self._get_project_root()
        normalized_rel_path = os.path.normpath(image_path_relativo_ao_projeto.lstrip('/\\'))
        full_path = os.path.join(project_root, normalized_rel_path)

        tamanho_usado_para_cache = novo_tamanho if novo_tamanho else self.slot_tamanho_hud
        tamanho_str_cache = f"{tamanho_usado_para_cache[0]}x{tamanho_usado_para_cache[1]}"
        cache_key = f"{cache_key_prefix}_{normalized_rel_path.replace(os.sep, '-')}_{tamanho_str_cache}"

        if cache_key in self._icon_cache:
            return self._icon_cache[cache_key]

        tamanho_icone_final = tamanho_usado_para_cache
        if not novo_tamanho:
            padding_icone = max(4, int(min(tamanho_usado_para_cache) * 0.1))
            tamanho_icone_final = (max(1, tamanho_usado_para_cache[0] - padding_icone*2),
                                   max(1, tamanho_usado_para_cache[1] - padding_icone*2))

        if os.path.exists(full_path) and os.path.isfile(full_path):
            try:
                icone_surface = pygame.image.load(full_path).convert_alpha()
                icone_surface = pygame.transform.smoothscale(icone_surface, tamanho_icone_final)
                self._icon_cache[cache_key] = icone_surface
                return icone_surface
            except pygame.error as e:
                print(f"ALERTA(InventarioBarra _load_image_from_path): Erro Pygame ao carregar/escalar '{full_path}': {e}")
            except Exception as e_gen_load:
                print(f"ERRO(InventarioBarra _load_image_from_path): Erro inesperado ao carregar '{full_path}': {e_gen_load}")
        else:
            # print(f"FALHA(InventarioBarra _load_image_from_path): Imagem NÃO ENCONTRADA em '{full_path}'.")
            pass

        self._icon_cache[cache_key] = None
        return None

    def _carregar_icone_arma(self, arma_instancia: Weapon, tamanho_personalizado=None) -> pygame.Surface | None:
        if not isinstance(arma_instancia, Weapon):
            return None

        nome_arma_para_icone = getattr(arma_instancia, 'name', "ArmaDesconhecida")

        tamanho_ph_cache = tamanho_personalizado if tamanho_personalizado else self.slot_tamanho_hud
        padding_ph = max(4, int(min(tamanho_ph_cache) * 0.1)) if not tamanho_personalizado else 0
        tamanho_ph_interno = (max(1, tamanho_ph_cache[0] - padding_ph*2), max(1, tamanho_ph_cache[1] - padding_ph*2))

        placeholder_cache_key = f"placeholder_icon_{nome_arma_para_icone.replace(' ', '_')}_{tamanho_ph_interno[0]}x{tamanho_ph_interno[1]}"

        caminho_icone_especifico = getattr(arma_instancia, 'ui_icon_path', None)

        if caminho_icone_especifico:
            icone = self._load_image_from_path(caminho_icone_especifico,
                                               cache_key_prefix=f"icon_{nome_arma_para_icone.replace(' ', '_')}",
                                               novo_tamanho=tamanho_personalizado)
            if icone:
                return icone
            # else:
                # print(f"ALERTA(InventarioBarra _carregar_icone_arma): Falha ao carregar ícone específico de '{caminho_icone_especifico}' para '{nome_arma_para_icone}'. Tentando padrão.")

        icone_default = self._load_image_from_path(DEFAULT_WEAPON_ICON_PATH,
                                                   cache_key_prefix="default_icon",
                                                   novo_tamanho=tamanho_personalizado)
        if icone_default:
            return icone_default
        # else:
            # print(f"ALERTA(InventarioBarra _carregar_icone_arma): Falha ao carregar ícone padrão '{DEFAULT_WEAPON_ICON_PATH}'. Criando placeholder para '{nome_arma_para_icone}'.")


        if placeholder_cache_key in self._icon_cache:
             return self._icon_cache[placeholder_cache_key]

        placeholder_icone = self._criar_icone_placeholder_arma(nome_arma_para_icone, tamanho_icone=tamanho_ph_interno)
        if placeholder_icone:
            self._icon_cache[placeholder_cache_key] = placeholder_icone
        return placeholder_icone

    def _criar_icone_placeholder_arma(self, nome_arma="?", tamanho_icone=None):
        if tamanho_icone is None or not (isinstance(tamanho_icone, tuple) and len(tamanho_icone) == 2):
            padding_default = max(4, int(min(self.slot_tamanho_hud) * 0.1))
            tamanho_icone = (max(1,self.slot_tamanho_hud[0] - padding_default*2),
                             max(1,self.slot_tamanho_hud[1] - padding_default*2))

        placeholder_surf = pygame.Surface(tamanho_icone, pygame.SRCALPHA)
        cor_r, cor_g, cor_b = random.randint(80, 160), random.randint(80, 160), random.randint(80, 160)
        placeholder_surf.fill((cor_r, cor_g, cor_b, 180))

        try:
            fonte_tam_ph = max(10, int(tamanho_icone[1] * 0.55))
            fonte_placeholder = pygame.font.Font(None, fonte_tam_ph)
            texto_ph = nome_arma[0].upper() if nome_arma and len(nome_arma)>0 else "?"
            texto_surface_ph = fonte_placeholder.render(texto_ph, True, (240,240,240))
            rect_texto_ph = texto_surface_ph.get_rect(center=(tamanho_icone[0]//2, tamanho_icone[1]//2))
            placeholder_surf.blit(texto_surface_ph, rect_texto_ph)
            pygame.draw.rect(placeholder_surf, (cor_r-20, cor_g-20, cor_b-20), (0,0,tamanho_icone[0],tamanho_icone[1]), 1)
        except Exception as e_ph_text:
            # print(f"DEBUG(InventarioBarra): Erro ao criar texto para placeholder '{nome_arma}': {e_ph_text}")
            pass
        return placeholder_surf

    def handle_input(self, evento, jogador_ref):
        if not hasattr(jogador_ref, 'owned_weapons') or not hasattr(jogador_ref, 'equip_weapon') or not hasattr(jogador_ref, 'current_weapon'):
            return False

        armas_jogador = jogador_ref.owned_weapons

        if evento.type == pygame.KEYDOWN:
            novo_slot_selecionado_teclado = -1
            if evento.key == pygame.K_1: novo_slot_selecionado_teclado = 0
            elif evento.key == pygame.K_2: novo_slot_selecionado_teclado = 1
            elif evento.key == pygame.K_3: novo_slot_selecionado_teclado = 2
            elif evento.key == pygame.K_4: novo_slot_selecionado_teclado = 3

            if 0 <= novo_slot_selecionado_teclado < self.num_slots_painel:
                self.item_selecionado_index_painel = novo_slot_selecionado_teclado

                arma_para_equipar_teclado = None
                if novo_slot_selecionado_teclado < len(armas_jogador) and armas_jogador[novo_slot_selecionado_teclado] is not None:
                    arma_para_equipar_teclado = armas_jogador[novo_slot_selecionado_teclado]

                if arma_para_equipar_teclado:
                    jogador_ref.equip_weapon(arma_para_equipar_teclado)
                return False

        elif evento.type == pygame.MOUSEBUTTONDOWN and self.visao_inventario_aberta:
            if evento.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.rect_painel_fundo.collidepoint(mouse_pos):
                    for i, slot_rect in enumerate(self.slot_rects_painel):
                        if slot_rect.collidepoint(mouse_pos):
                            self.item_selecionado_index_painel = i

                            arma_para_equipar_clique = None
                            if i < len(armas_jogador) and armas_jogador[i] is not None:
                                arma_para_equipar_clique = armas_jogador[i]

                            if arma_para_equipar_clique:
                                jogador_ref.equip_weapon(arma_para_equipar_clique)
                            return True
                    return True
                else:
                    self.toggle_visao_inventario(jogador_ref)
                    return True
        return False

    def toggle_visao_inventario(self, jogador_ref):
        self.visao_inventario_aberta = not self.visao_inventario_aberta

        if self.visao_inventario_aberta:
            arma_equipada_jogador = getattr(jogador_ref, 'current_weapon', None)
            armas_possuidas_jogador = getattr(jogador_ref, 'owned_weapons', [])

            self.item_selecionado_index_painel = 0
            if arma_equipada_jogador and armas_possuidas_jogador:
                try:
                    idx_arma_equipada = -1
                    for i, arma_inv in enumerate(armas_possuidas_jogador):
                        if arma_inv is arma_equipada_jogador:
                            idx_arma_equipada = i
                            break

                    if 0 <= idx_arma_equipada < self.num_slots_painel:
                        self.item_selecionado_index_painel = idx_arma_equipada
                except ValueError:
                    pass

    def desenhar(self, tela: pygame.Surface, jogador_ref):
        self._desenhar_barra_rapida_hud(tela, jogador_ref)

        if not self.visao_inventario_aberta:
            return

        arma_equipada_jogador = getattr(jogador_ref, 'current_weapon', None)
        armas_do_jogador = getattr(jogador_ref, 'owned_weapons', [])
        dinheiro_jogador = getattr(jogador_ref, 'dinheiro', 0)
        nome_arma_para_exibir_painel = ""

        fundo_inv_surface = pygame.Surface(self.rect_painel_fundo.size, pygame.SRCALPHA)
        fundo_inv_surface.fill(COR_FUNDO_PAINEL_CENTRAL)
        tela.blit(fundo_inv_surface, self.rect_painel_fundo.topleft)
        pygame.draw.rect(tela, COR_BORDA_PAINEL_CENTRAL, self.rect_painel_fundo, 2, border_radius=RAIO_BORDA_SLOT + 2)

        titulo_surface = self.fonte_titulo_inventario.render("Inventário", True, COR_TEXTO_TITULO_INVENTARIO)
        titulo_rect = titulo_surface.get_rect(centerx=self.rect_painel_fundo.centerx,
                                              top=self.rect_painel_fundo.top + self.espacamento_hud + 5)
        tela.blit(titulo_surface, titulo_rect)

        cx_tela = self.largura_tela_original // 2
        cy_tela = self.altura_tela_original // 2
        offset_losango_visual = 80
        tamanho_icone_central_arma = (int(offset_losango_visual * 0.85), int(offset_losango_visual * 0.85))

        p_sup = (cx_tela, cy_tela - offset_losango_visual)
        p_dir = (cx_tela + offset_losango_visual, cy_tela)
        p_inf = (cx_tela, cy_tela + offset_losango_visual)
        p_esq = (cx_tela - offset_losango_visual, cy_tela)
        pontos_losango_desenho = [p_sup, p_dir, p_inf, p_esq]

        pygame.draw.polygon(tela, COR_FUNDO_LOSANGO_CENTRAL, pontos_losango_desenho)
        pygame.draw.polygon(tela, COR_LOSANGO_BORDA, pontos_losango_desenho, ESPESSURA_LOSANGO_NORMAL)

        if arma_equipada_jogador:
            icone_arma_eq_central = self._carregar_icone_arma(arma_equipada_jogador, tamanho_personalizado=tamanho_icone_central_arma)
            if icone_arma_eq_central:
                rect_icone_eq_central = icone_arma_eq_central.get_rect(center=(cx_tela, cy_tela))
                tela.blit(icone_arma_eq_central, rect_icone_eq_central)
                pygame.draw.rect(tela, COR_BORDA_EQUIPADA, rect_icone_eq_central.inflate(6,6), ESPESSURA_BORDA_ICONE_CENTRAL, border_radius=RAIO_BORDA_ICONE_CENTRAL)

        idx_painel_sel = self.item_selecionado_index_painel
        cor_ponta_sel_losango = COR_LOSANGO_PONTA_SELECIONADA
        esp_ponta_sel_losango = ESPESSURA_LOSANGO_PONTA_SELECIONADA
        if 0 <= idx_painel_sel < 4:
            if idx_painel_sel == 0:
                pygame.draw.line(tela, cor_ponta_sel_losango, p_esq, p_sup, esp_ponta_sel_losango)
                pygame.draw.line(tela, cor_ponta_sel_losango, p_sup, p_dir, esp_ponta_sel_losango)
            elif idx_painel_sel == 1:
                pygame.draw.line(tela, cor_ponta_sel_losango, p_sup, p_dir, esp_ponta_sel_losango)
                pygame.draw.line(tela, cor_ponta_sel_losango, p_dir, p_inf, esp_ponta_sel_losango)
            elif idx_painel_sel == 2:
                pygame.draw.line(tela, cor_ponta_sel_losango, p_dir, p_inf, esp_ponta_sel_losango)
                pygame.draw.line(tela, cor_ponta_sel_losango, p_inf, p_esq, esp_ponta_sel_losango)
            elif idx_painel_sel == 3:
                pygame.draw.line(tela, cor_ponta_sel_losango, p_inf, p_esq, esp_ponta_sel_losango)
                pygame.draw.line(tela, cor_ponta_sel_losango, p_esq, p_sup, esp_ponta_sel_losango)

        for i, slot_rect_painel_item in enumerate(self.slot_rects_painel):
            fundo_slot_surf = pygame.Surface(self.slot_tamanho_hud, pygame.SRCALPHA)
            fundo_slot_surf.fill(COR_FUNDO_SLOT)
            tela.blit(fundo_slot_surf, slot_rect_painel_item.topleft)

            arma_no_slot_painel = None
            if i < len(armas_do_jogador):
                arma_no_slot_painel = armas_do_jogador[i]

            cor_borda_atual_slot = COR_BORDA_SLOT
            espessura_borda_atual_slot = 2

            if arma_no_slot_painel and arma_equipada_jogador and arma_no_slot_painel is arma_equipada_jogador:
                cor_borda_atual_slot = COR_BORDA_EQUIPADA
                espessura_borda_atual_slot = 3
            elif i == self.item_selecionado_index_painel:
                cor_borda_atual_slot = COR_BORDA_SELECIONADA
                espessura_borda_atual_slot = 3

            pygame.draw.rect(tela, cor_borda_atual_slot, slot_rect_painel_item, espessura_borda_atual_slot, border_radius=RAIO_BORDA_SLOT)

            if arma_no_slot_painel:
                icone_arma_slot = self._carregar_icone_arma(arma_no_slot_painel, tamanho_personalizado=self.slot_tamanho_hud)
                if icone_arma_slot:
                    icone_rect_slot = icone_arma_slot.get_rect(center=slot_rect_painel_item.center)
                    tela.blit(icone_arma_slot, icone_rect_slot)

                if i == self.item_selecionado_index_painel:
                    nome_arma_para_exibir_painel = arma_no_slot_painel.name

            if i == self.item_selecionado_index_painel and not arma_no_slot_painel:
                nome_arma_para_exibir_painel = "Vazio"

            texto_atalho_painel = self.fonte_tecla_atalho.render(str(i + 1), True, COR_TEXTO_TECLA_ATALHO)
            tela.blit(texto_atalho_painel, (slot_rect_painel_item.left + 5, slot_rect_painel_item.top + 3))

        if nome_arma_para_exibir_painel:
            nome_arma_surf_detalhe = self.fonte_nome_arma_fullview.render(nome_arma_para_exibir_painel, True, COR_TEXTO_NOME_ARMA_DETALHE)
            pos_y_nome_arma = self.slot_rects_painel[2].bottom + self.espacamento_hud + nome_arma_surf_detalhe.get_height() // 2 + 5
            nome_arma_rect_detalhe = nome_arma_surf_detalhe.get_rect(centerx=self.rect_painel_fundo.centerx,
                                                                     centery=pos_y_nome_arma)
            tela.blit(nome_arma_surf_detalhe, nome_arma_rect_detalhe)

        texto_dinheiro_str = f"Ouro: {dinheiro_jogador}"
        surface_dinheiro_jogador = self.fonte_dinheiro.render(texto_dinheiro_str, True, COR_TEXTO_DINHEIRO)
        rect_dinheiro_jogador = surface_dinheiro_jogador.get_rect(left=self.rect_painel_fundo.left + self.espacamento_hud + 10,
                                                                  bottom=self.rect_painel_fundo.bottom - self.espacamento_hud - 5)
        tela.blit(surface_dinheiro_jogador, rect_dinheiro_jogador)


    def _desenhar_barra_rapida_hud(self, tela: pygame.Surface, jogador_ref):
        arma_equipada_jogador_hud = getattr(jogador_ref, 'current_weapon', None)
        armas_para_hud = getattr(jogador_ref, 'owned_weapons', [])

        for i, slot_rect_hud_item in enumerate(self.slot_rects_hud):
            if i >= self.num_slots_hud: continue

            fundo_slot_hud_surf = pygame.Surface(self.slot_tamanho_hud, pygame.SRCALPHA)
            fundo_slot_hud_surf.fill(COR_FUNDO_SLOT)
            tela.blit(fundo_slot_hud_surf, slot_rect_hud_item.topleft)

            arma_neste_slot_hud_item = None
            if i < len(armas_para_hud):
                arma_neste_slot_hud_item = armas_para_hud[i]

            cor_borda_hud_slot = COR_BORDA_SLOT
            espessura_borda_hud_slot = 2

            if arma_neste_slot_hud_item and arma_equipada_jogador_hud and arma_neste_slot_hud_item is arma_equipada_jogador_hud:
                cor_borda_hud_slot = COR_BORDA_EQUIPADA
                espessura_borda_hud_slot = 3

            pygame.draw.rect(tela, cor_borda_hud_slot, slot_rect_hud_item, espessura_borda_hud_slot, border_radius=RAIO_BORDA_SLOT)

            if arma_neste_slot_hud_item:
                icone_arma_hud = self._carregar_icone_arma(arma_neste_slot_hud_item, tamanho_personalizado=self.slot_tamanho_hud)
                if icone_arma_hud:
                    icone_rect_hud = icone_arma_hud.get_rect(center=slot_rect_hud_item.center)
                    tela.blit(icone_arma_hud, icone_rect_hud)

            if i < 4 :
                texto_atalho_hud_render = self.fonte_tecla_atalho.render(str(i + 1), True, COR_TEXTO_TECLA_ATALHO)
                tela.blit(texto_atalho_hud_render, (slot_rect_hud_item.left + 5, slot_rect_hud_item.top + 3))


# --- Bloco para Teste Standalone ---
if __name__ == '__main__':
    pygame.init()
    LARGURA_TELA_TESTE = 800
    ALTURA_TELA_TESTE = 600
    tela_teste = pygame.display.set_mode((LARGURA_TELA_TESTE, ALTURA_TELA_TESTE))
    pygame.display.set_caption("Teste da Barra de Inventário - Adaga Inicial")
    clock = pygame.time.Clock()

    class MockJogador:
        def __init__(self):
            self.dinheiro = 1250
            self.max_owned_weapons = 4 # Ajustado para corresponder ao num_slots_painel
            self.owned_weapons: list[Weapon | None] = [None] * self.max_owned_weapons
            self.current_weapon: Weapon | None = None

            arma_adaga_para_mock = None
            if AdagaFogo: # Verifica se a classe AdagaFogo foi importada com sucesso
                    arma_adaga_para_mock = AdagaFogo() # Tenta instanciar a AdagaFogo real