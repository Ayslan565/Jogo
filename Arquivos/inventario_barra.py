# inventario_barra.py
import pygame
import os
import random

# Cores
COR_FUNDO_SLOT = (50, 50, 50, 180) # Cinza escuro semi-transparente
COR_BORDA_SLOT = (150, 150, 150)
COR_BORDA_SELECIONADA = (255, 215, 0) # Dourado
COR_TEXTO_QUANTIDADE = (255, 255, 255)
COR_TEXTO_TECLA_ATALHO = (200, 200, 200)

class ItemInventario:
    """Representa um item dentro de um slot da barra."""
    def __init__(self, nome, quantidade, icone_path, item_id=None, descricao=""):
        self.nome = nome
        self.quantidade = quantidade
        self.icone_path = icone_path # Caminho para a imagem do ícone
        self.item_id = item_id if item_id is not None else nome # Um ID único para o tipo de item
        self.descricao = descricao
        self.icone_surface = None # Será carregado
        self._carregar_icone()

    def _carregar_icone(self, tamanho_icone=(40,40)):
        if self.icone_path and os.path.exists(self.icone_path):
            try:
                self.icone_surface = pygame.image.load(self.icone_path).convert_alpha()
                self.icone_surface = pygame.transform.scale(self.icone_surface, tamanho_icone)
            except pygame.error as e:
                print(f"Erro ao carregar ícone do item '{self.nome}': {e}")
                self._criar_icone_placeholder(tamanho_icone)
        else:
            if self.icone_path: # Se o caminho foi fornecido mas não existe
                print(f"Aviso: Ícone não encontrado para '{self.nome}' em '{self.icone_path}'. Usando placeholder.")
            self._criar_icone_placeholder(tamanho_icone)

    def _criar_icone_placeholder(self, tamanho_icone):
        self.icone_surface = pygame.Surface(tamanho_icone, pygame.SRCALPHA)
        cor_placeholder = random.randint(50, 200) # Cor aleatória para placeholder
        self.icone_surface.fill((cor_placeholder, cor_placeholder // 2, cor_placeholder // 3, 200))
        # Desenha a primeira letra do nome no placeholder
        try:
            fonte_placeholder = pygame.font.Font(None, 20)
            texto_placeholder = fonte_placeholder.render(self.nome[0] if self.nome else "?", True, (255,255,255))
            rect_texto = texto_placeholder.get_rect(center=(tamanho_icone[0]//2, tamanho_icone[1]//2))
            self.icone_surface.blit(texto_placeholder, rect_texto)
        except Exception: # Se fontes não estiverem prontas ou houver outro erro
            pass


    def usar(self, jogador):
        """Lógica para usar o item. Deve ser implementada por classes de item específicas."""
        print(f"Usando {self.nome} no jogador {jogador}")
        # Exemplo: jogador.aplicar_efeito_pocao(self.tipo_pocao)
        self.quantidade -= 1
        return self.quantidade > 0 # Retorna True se ainda houver itens, False se acabar

class BarraInventario:
    def __init__(self, x, y, num_slots=4, slot_tamanho=(50, 50), espacamento=10):
        self.x = x
        self.y = y
        self.num_slots = num_slots
        self.slot_tamanho = slot_tamanho
        self.espacamento = espacamento
        
        self.slots = [None] * self.num_slots # Lista para armazenar objetos ItemInventario ou None
        self.slot_rects = []
        self.item_selecionado_index = 0 # Índice do slot selecionado

        # Fontes
        try:
            pygame.font.init() # Garante que o módulo de fontes está inicializado
            self.fonte_quantidade = pygame.font.Font(None, 20)
            self.fonte_tecla_atalho = pygame.font.Font(None, 18)
        except pygame.error as e:
            print(f"DEBUG(BarraInventario): Erro ao carregar fontes: {e}. Usando SysFont.")
            self.fonte_quantidade = pygame.font.SysFont("arial", 18)
            self.fonte_tecla_atalho = pygame.font.SysFont("arial", 16)


        # Calcula a largura total da barra e os rects dos slots
        largura_total_barra = (self.num_slots * self.slot_tamanho[0]) + ((self.num_slots - 1) * self.espacamento)
        self.rect_barra = pygame.Rect(self.x, self.y, largura_total_barra, self.slot_tamanho[1])

        for i in range(self.num_slots):
            slot_x = self.x + i * (self.slot_tamanho[0] + self.espacamento)
            slot_y = self.y
            self.slot_rects.append(pygame.Rect(slot_x, slot_y, self.slot_tamanho[0], self.slot_tamanho[1]))
        
        print("DEBUG(BarraInventario): Barra de Inventário inicializada.")
        # Exemplo: Adicionar alguns itens placeholder para teste
        # self.adicionar_item(ItemInventario("Poção de Cura", 3, "Sprites/Itens/pocao_cura.png"))
        # self.adicionar_item(ItemInventario("Bomba", 5, "Sprites/Itens/bomba.png"))


    def adicionar_item(self, novo_item_instancia: ItemInventario, slot_especifico=None):
        """Adiciona uma instância de ItemInventario à barra."""
        if not isinstance(novo_item_instancia, ItemInventario):
            print("DEBUG(BarraInventario): Tentativa de adicionar objeto que não é ItemInventario.")
            return False

        # Tenta empilhar se o item já existe
        for i, slot_item in enumerate(self.slots):
            if slot_item and slot_item.item_id == novo_item_instancia.item_id:
                # Adicionar lógica de max_stack aqui se necessário
                slot_item.quantidade += novo_item_instancia.quantidade
                print(f"DEBUG(BarraInventario): Item '{novo_item_instancia.nome}' empilhado. Nova quantidade: {slot_item.quantidade}")
                return True

        # Se não empilhou, tenta adicionar a um slot específico ou ao próximo vazio
        if slot_especifico is not None and 0 <= slot_especifico < self.num_slots:
            if self.slots[slot_especifico] is None:
                self.slots[slot_especifico] = novo_item_instancia
                print(f"DEBUG(BarraInventario): Item '{novo_item_instancia.nome}' adicionado ao slot {slot_especifico}.")
                return True
            else:
                # Slot específico ocupado, tenta o próximo vazio
                print(f"DEBUG(BarraInventario): Slot específico {slot_especifico} ocupado. Tentando próximo vazio.")
                pass # Cai para a lógica de encontrar slot vazio

        # Tenta encontrar o primeiro slot vazio
        for i in range(self.num_slots):
            if self.slots[i] is None:
                self.slots[i] = novo_item_instancia
                print(f"DEBUG(BarraInventario): Item '{novo_item_instancia.nome}' adicionado ao slot {i}.")
                return True
        
        print(f"DEBUG(BarraInventario): Barra de inventário cheia. Não foi possível adicionar '{novo_item_instancia.nome}'.")
        return False # Barra cheia

    def usar_item_selecionado(self, jogador_ref):
        """Usa o item no slot atualmente selecionado."""
        if 0 <= self.item_selecionado_index < self.num_slots:
            item_no_slot = self.slots[self.item_selecionado_index]
            if item_no_slot:
                print(f"DEBUG(BarraInventario): Tentando usar item '{item_no_slot.nome}' do slot {self.item_selecionado_index}.")
                # A lógica de 'usar' deve estar no próprio objeto ItemInventario ou sua subclasse
                if hasattr(item_no_slot, 'usar') and callable(getattr(item_no_slot, 'usar')):
                    ainda_tem_item = item_no_slot.usar(jogador_ref) # Passa a referência do jogador
                    if not ainda_tem_item:
                        self.slots[self.item_selecionado_index] = None # Remove se a quantidade for zero
                        print(f"DEBUG(BarraInventario): Item '{item_no_slot.nome}' consumido.")
                else:
                    print(f"DEBUG(BarraInventario): Item '{item_no_slot.nome}' não tem método 'usar'.")
            else:
                print(f"DEBUG(BarraInventario): Nenhum item no slot selecionado {self.item_selecionado_index}.")
        else:
            print(f"DEBUG(BarraInventario): Índice de slot selecionado inválido: {self.item_selecionado_index}.")


    def handle_input(self, evento, jogador_ref): # Adicionado jogador_ref
        """Processa input para selecionar slots ou usar itens."""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1: self.item_selecionado_index = 0
            elif evento.key == pygame.K_2: self.item_selecionado_index = 1
            elif evento.key == pygame.K_3: self.item_selecionado_index = 2
            elif evento.key == pygame.K_4: self.item_selecionado_index = 3
            # Adicione mais teclas se tiver mais slots

            # Exemplo de tecla para USAR o item selecionado (ex: Q ou E)
            elif evento.key == pygame.K_q: # Ou qualquer outra tecla que você preferir
                self.usar_item_selecionado(jogador_ref)

            # Garante que o índice selecionado esteja dentro dos limites
            self.item_selecionado_index = max(0, min(self.item_selecionado_index, self.num_slots - 1))
            # print(f"DEBUG(BarraInventario): Slot selecionado: {self.item_selecionado_index + 1}")


    def desenhar(self, tela):
        """Desenha a barra de inventário na tela."""
        for i, slot_rect in enumerate(self.slot_rects):
            # Desenha o fundo do slot com transparência
            fundo_surface = pygame.Surface(self.slot_tamanho, pygame.SRCALPHA)
            fundo_surface.fill(COR_FUNDO_SLOT)
            tela.blit(fundo_surface, slot_rect.topleft)

            # Desenha a borda
            cor_borda = COR_BORDA_SELECIONADA if i == self.item_selecionado_index else COR_BORDA_SLOT
            pygame.draw.rect(tela, cor_borda, slot_rect, 2, border_radius=3) # Borda com cantos arredondados

            # Desenha o item (ícone e quantidade)
            item = self.slots[i]
            if item and item.icone_surface:
                icone_rect = item.icone_surface.get_rect(center=slot_rect.center)
                tela.blit(item.icone_surface, icone_rect)
                
                # Desenha a quantidade
                if item.quantidade > 1:
                    texto_qtd = self.fonte_quantidade.render(str(item.quantidade), True, COR_TEXTO_QUANTIDADE)
                    # Posição do texto da quantidade (canto inferior direito do slot)
                    pos_qtd_x = slot_rect.right - texto_qtd.get_width() - 5
                    pos_qtd_y = slot_rect.bottom - texto_qtd.get_height() - 3
                    tela.blit(texto_qtd, (pos_qtd_x, pos_qtd_y))
            
            # Desenha o número do slot (tecla de atalho)
            texto_atalho = self.fonte_tecla_atalho.render(str(i + 1), True, COR_TEXTO_TECLA_ATALHO)
            pos_atalho_x = slot_rect.left + 5
            pos_atalho_y = slot_rect.top + 3
            tela.blit(texto_atalho, (pos_atalho_x, pos_atalho_y))

