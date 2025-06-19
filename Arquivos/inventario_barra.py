import pygame
import os
import random
import sys

# --- CONSTANTES ---
DEFAULT_WEAPON_ICON_PATH = os.path.join("Sprites", "Interface", "Icons", "default_weapon_icon.png")

try:
    from Armas.weapon import Weapon 
except ImportError:
    print("ALERTA(BarraInventario): Classe 'Weapon' não encontrada. Usando placeholder.")
    class Weapon:
        def __init__(self, name="Arma Desconhecida", ui_icon_path=None, damage=10, attack_range=50, cooldown=0.5, hitbox_dimensions=(0,0), hitbox_offset=(0,0), attack_animation_sprites=None, attack_animation_speed=100):
            self.name = name
            self.ui_icon_path = ui_icon_path if ui_icon_path else DEFAULT_WEAPON_ICON_PATH
            self._base_name = name
            self.level = 1
            self.damage = damage
            self.attack_range = attack_range
            self.cooldown = cooldown
            self.hitbox_width, self.hitbox_height = hitbox_dimensions
            self.hitbox_offset_x, self.hitbox_offset_y = hitbox_offset
            self.attack_animation_sprites = attack_animation_sprites or []
            self.attack_animation_speed = attack_animation_speed
            self.current_attack_animation_frame = 0
            self.last_attack_animation_update = 0
            self.ui_icon_surface = None
            self._load_ui_icon_sprite()

        def get_current_attack_animation_sprite(self):
            if self.attack_animation_sprites:
                return self.attack_animation_sprites[self.current_attack_animation_frame]
            return None

        def _get_project_root(self):
            # Lógica de placeholder para encontrar a raiz do projeto
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return base_path

        def _load_ui_icon_sprite(self):
            full_path = os.path.join(self._get_project_root(), self.ui_icon_path)
            if os.path.exists(full_path):
                try:
                    self.ui_icon_surface = pygame.image.load(full_path).convert_alpha()
                except Exception as e:
                    print(f"ERRO(Placeholder Weapon): Falha ao carregar ícone '{full_path}': {e}")
                    self.ui_icon_surface = None
            else:
                self.ui_icon_surface = None

# --- CLASSE PARA ITEM GENÉRICO ---
class ItemInventario:
    """Classe base para um item genérico no inventário."""
    def __init__(self, nome: str, icone_path: str = None, descricao: str = ""):
        self.nome = nome
        self.icone_path = icone_path
        self.descricao = descricao
        self.icone_surface = None

    def carregar_icone(self, tamanho: tuple[int, int] = (50, 50)):
        """Carrega e escala o ícone do item."""
        if not self.icone_path: return
        
        # Lógica para encontrar o caminho absoluto do ícone
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        full_path = os.path.join(base_path, self.icone_path)

        if os.path.exists(full_path):
            try:
                self.icone_surface = pygame.image.load(full_path).convert_alpha()
                self.icone_surface = pygame.transform.scale(self.icone_surface, tamanho)
            except pygame.error as e:
                print(f"ERRO(ItemInventario): Falha ao carregar ícone '{full_path}': {e}")
        else:
            print(f"ALERTA(ItemInventario): Ícone não encontrado em '{full_path}'.")

# --- BLOCO DE CONFIGURAÇÃO DE IMPORTS (PARA TESTE) ---
try:
    # Adiciona a raiz do projeto ao sys.path para importações relativas
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from Armas.AdagaFogo import AdagaFogo
    from Armas.EspadaBrasas import EspadaBrasas
except ImportError as e:
    # Silencia o erro de importação, pois é esperado no ambiente de produção
    AdagaFogo = EspadaBrasas = None
    pass

# --- CORES E CONSTANTES DE UI ---
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
COR_FUNDO_LOSANGO_CENTRAL = (50, 50, 50, 180)
COR_TEXTO_DINHEIRO = (255, 215, 0)
RAIO_BORDA_SLOT = 5

class BarraInventario:
    def __init__(self, x, y, largura_tela, altura_tela, num_slots_hud=4, slot_tamanho=(70, 70), espacamento=8):
        self.largura_tela_original = largura_tela
        self.altura_tela_original = altura_tela
        self.pos_x_hud, self.pos_y_hud = x, y
        self.num_slots_hud = num_slots_hud
        self.num_slots_painel = 4
        self.slot_tamanho_hud = slot_tamanho
        self.espacamento_hud = espacamento
        self.item_selecionado_index_painel = 0
        self._icon_cache = {}
        self.visao_inventario_aberta = False
        
        try:
            pygame.font.init()
            self.fonte_tecla_atalho = pygame.font.Font(None, 22)
            self.fonte_nome_arma_fullview = pygame.font.Font(None, 24)
            self.fonte_titulo_inventario = pygame.font.Font(None, 30)
            self.fonte_dinheiro = pygame.font.Font(None, 26)
        except pygame.error:
            self.fonte_tecla_atalho = pygame.font.SysFont("arial", 18)
            self.fonte_nome_arma_fullview = pygame.font.SysFont("arial", 20)
            self.fonte_titulo_inventario = pygame.font.SysFont("arial", 26)
            self.fonte_dinheiro = pygame.font.SysFont("arial", 22)

        self._calcular_rects_painel_central()
        self._calcular_rects_barra_rapida()

    def _calcular_rects_painel_central(self):
        cx, cy = self.largura_tela_original // 2, self.altura_tela_original // 2
        sw, sh = self.slot_tamanho_hud
        offset = 130 # Distância do centro
        self.slot_rects_painel = [
            pygame.Rect(cx - sw // 2, cy - offset - sh // 2, sw, sh), # Topo
            pygame.Rect(cx + offset - sw // 2, cy - sh // 2, sw, sh), # Direita
            pygame.Rect(cx - sw // 2, cy + offset - sh // 2, sw, sh), # Baixo
            pygame.Rect(cx - offset - sw // 2, cy - sh // 2, sw, sh), # Esquerda
        ]
        
        # Painel de fundo
        min_x = min(r.left for r in self.slot_rects_painel)
        max_x = max(r.right for r in self.slot_rects_painel)
        min_y = min(r.top for r in self.slot_rects_painel)
        max_y = max(r.bottom for r in self.slot_rects_painel)
        padding = self.espacamento_hud * 2.5
        self.rect_painel_fundo = pygame.Rect(min_x - padding, min_y - 50, (max_x - min_x) + padding*2, (max_y - min_y) + 120)

    def _calcular_rects_barra_rapida(self):
        self.slot_rects_hud = []
        for i in range(self.num_slots_hud):
            rect_x = self.pos_x_hud + i * (self.slot_tamanho_hud[0] + self.espacamento_hud)
            self.slot_rects_hud.append(pygame.Rect(rect_x, self.pos_y_hud, *self.slot_tamanho_hud))

    def _get_project_root(self):
        try:
            return sys._MEIPASS
        except Exception:
            return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    def _load_image(self, path, size):
        cache_key = f"{path}_{size[0]}x{size[1]}"
        if cache_key in self._icon_cache:
            return self._icon_cache[cache_key]

        full_path = os.path.join(self._get_project_root(), path)
        if os.path.exists(full_path):
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.smoothscale(img, size)
                self._icon_cache[cache_key] = img
                return img
            except pygame.error as e:
                print(f"ALERTA(BarraInventario): Erro ao carregar imagem '{full_path}': {e}")
        return None

    def _carregar_icone_arma(self, arma: Weapon, tamanho):
        if not isinstance(arma, Weapon): return None
        
        # Tenta carregar o ícone específico da arma
        if hasattr(arma, 'ui_icon_path') and arma.ui_icon_path:
            icon = self._load_image(arma.ui_icon_path, tamanho)
            if icon: return icon

        # Se falhar, tenta carregar o ícone padrão
        return self._load_image(DEFAULT_WEAPON_ICON_PATH, tamanho)

    def handle_input(self, evento, jogador):
        if not hasattr(jogador, 'owned_weapons'): return False

        if evento.type == pygame.KEYDOWN:
            if evento.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                index = evento.key - pygame.K_1
                if 0 <= index < len(jogador.owned_weapons) and jogador.owned_weapons[index]:
                    jogador.equip_weapon(jogador.owned_weapons[index])
                self.item_selecionado_index_painel = index
                return False

        if self.visao_inventario_aberta and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_painel_fundo.collidepoint(evento.pos):
                for i, rect in enumerate(self.slot_rects_painel):
                    if rect.collidepoint(evento.pos) and i < len(jogador.owned_weapons) and jogador.owned_weapons[i]:
                        jogador.equip_weapon(jogador.owned_weapons[i])
                        self.item_selecionado_index_painel = i
                        return True
                return True # Clicou dentro do painel, mas não em um item
            else:
                self.toggle_visao_inventario() # Fecha se clicar fora
                return True
        return False
        
    def toggle_visao_inventario(self, jogador_ref=None):
        self.visao_inventario_aberta = not self.visao_inventario_aberta
        if self.visao_inventario_aberta and jogador_ref and hasattr(jogador_ref, 'current_weapon'):
            try:
                self.item_selecionado_index_painel = jogador_ref.owned_weapons.index(jogador_ref.current_weapon)
            except (ValueError, AttributeError):
                self.item_selecionado_index_painel = 0

    def desenhar(self, tela, jogador):
        self._desenhar_barra_rapida_hud(tela, jogador)
        if self.visao_inventario_aberta:
            self._desenhar_painel_inventario(tela, jogador)

    def _desenhar_painel_inventario(self, tela, jogador):
        # Fundo do painel
        fundo_surf = pygame.Surface(self.rect_painel_fundo.size, pygame.SRCALPHA)
        fundo_surf.fill(COR_FUNDO_PAINEL_CENTRAL)
        tela.blit(fundo_surf, self.rect_painel_fundo.topleft)
        pygame.draw.rect(tela, COR_BORDA_PAINEL_CENTRAL, self.rect_painel_fundo, 2, border_radius=RAIO_BORDA_SLOT + 2)

        # Título
        titulo_surf = self.fonte_titulo_inventario.render("Inventário", True, COR_TEXTO_TITULO_INVENTARIO)
        tela.blit(titulo_surf, titulo_surf.get_rect(centerx=self.rect_painel_fundo.centerx, top=self.rect_painel_fundo.top + 15))

        # Losango central e ícone da arma equipada
        cx, cy = self.rect_painel_fundo.center
        offset_losango = 80
        pontos_losango = [(cx, cy - offset_losango), (cx + offset_losango, cy), (cx, cy + offset_losango), (cx - offset_losango, cy)]
        pygame.draw.polygon(tela, COR_FUNDO_LOSANGO_CENTRAL, pontos_losango)
        pygame.draw.polygon(tela, COR_LOSANGO_BORDA, pontos_losango, 2)
        
        if hasattr(jogador, 'current_weapon') and jogador.current_weapon:
            icon_size = (int(offset_losango * 0.85), int(offset_losango * 0.85))
            icon = self._carregar_icone_arma(jogador.current_weapon, icon_size)
            if icon:
                tela.blit(icon, icon.get_rect(center=(cx, cy)))

        # Slots do inventário
        nome_arma_selecionada = "Vazio"
        for i, rect in enumerate(self.slot_rects_painel):
            # Desenha o slot
            pygame.draw.rect(tela, COR_FUNDO_SLOT, rect, border_radius=RAIO_BORDA_SLOT)
            
            arma_no_slot = jogador.owned_weapons[i] if i < len(jogador.owned_weapons) else None
            
            # Desenha ícone da arma no slot
            if arma_no_slot:
                icon = self._carregar_icone_arma(arma_no_slot, (rect.width - 10, rect.height - 10))
                if icon:
                    tela.blit(icon, icon.get_rect(center=rect.center))
                if i == self.item_selecionado_index_painel:
                    nome_arma_selecionada = arma_no_slot.name
            
            # Destaque de borda
            cor_borda = COR_BORDA_SLOT
            espessura = 2
            if arma_no_slot and arma_no_slot == jogador.current_weapon:
                cor_borda, espessura = COR_BORDA_EQUIPADA, 3
            elif i == self.item_selecionado_index_painel:
                cor_borda, espessura = COR_BORDA_SELECIONADA, 3
            pygame.draw.rect(tela, cor_borda, rect, espessura, border_radius=RAIO_BORDA_SLOT)

            # Número do atalho
            texto_atalho = self.fonte_tecla_atalho.render(str(i + 1), True, COR_TEXTO_TECLA_ATALHO)
            tela.blit(texto_atalho, (rect.left + 5, rect.top + 3))

        # Nome da arma selecionada
        nome_surf = self.fonte_nome_arma_fullview.render(nome_arma_selecionada, True, COR_TEXTO_NOME_ARMA_DETALHE)
        tela.blit(nome_surf, nome_surf.get_rect(centerx=self.rect_painel_fundo.centerx, bottom=self.rect_painel_fundo.bottom - 45))

        # Dinheiro
        dinheiro_surf = self.fonte_dinheiro.render(f"Ouro: {getattr(jogador, 'dinheiro', 0)}", True, COR_TEXTO_DINHEIRO)
        tela.blit(dinheiro_surf, dinheiro_surf.get_rect(left=self.rect_painel_fundo.left + 20, bottom=self.rect_painel_fundo.bottom - 15))


    def _desenhar_barra_rapida_hud(self, tela, jogador):
        for i, rect in enumerate(self.slot_rects_hud):
            pygame.draw.rect(tela, COR_FUNDO_SLOT, rect, border_radius=RAIO_BORDA_SLOT)
            arma_no_slot = jogador.owned_weapons[i] if i < len(jogador.owned_weapons) else None

            if arma_no_slot:
                icon = self._carregar_icone_arma(arma_no_slot, (rect.width - 10, rect.height - 10))
                if icon:
                    tela.blit(icon, icon.get_rect(center=rect.center))

            cor_borda = COR_BORDA_EQUIPADA if arma_no_slot and arma_no_slot == jogador.current_weapon else COR_BORDA_SLOT
            espessura = 3 if arma_no_slot and arma_no_slot == jogador.current_weapon else 2
            pygame.draw.rect(tela, cor_borda, rect, espessura, border_radius=RAIO_BORDA_SLOT)
            
            if i < 4:
                texto_atalho = self.fonte_tecla_atalho.render(str(i + 1), True, COR_TEXTO_TECLA_ATALHO)
                tela.blit(texto_atalho, (rect.left + 5, rect.top + 3))

# --- BLOCO DE TESTE STANDALONE ---
if __name__ == '__main__':
    pygame.init()
    LARGURA_TELA, ALTURA_TELA = 800, 600
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Teste da Barra de Inventário")
    clock = pygame.time.Clock()

    class MockJogador:
        def __init__(self):
            self.dinheiro = 1250
            self.owned_weapons = [None] * 4
            self.current_weapon = None
            
            # Tenta instanciar armas reais para o teste
            if AdagaFogo: self.owned_weapons[0] = AdagaFogo()
            if EspadaBrasas: self.owned_weapons[1] = EspadaBrasas()
            # Adicione outras armas para teste se necessário
            
            self.current_weapon = self.owned_weapons[0]

        def equip_weapon(self, weapon):
            self.current_weapon = weapon
            print(f"MockJogador: Arma '{weapon.name}' equipada.")

    mock_jogador = MockJogador()
    barra_inventario = BarraInventario(25, ALTURA_TELA - 85, LARGURA_TELA, ALTURA_TELA)
    barra_inventario.toggle_visao_inventario(mock_jogador)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            barra_inventario.handle_input(event, mock_jogador)

        tela.fill((50, 50, 50))
        barra_inventario.desenhar(tela, mock_jogador)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
