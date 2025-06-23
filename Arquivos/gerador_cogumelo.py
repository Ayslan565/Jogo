import pygame
import random
import os
import time
import math

try:
    from cogumelo import Cogumelo, TIPO_CURA, TIPO_LENTIDAO, TIPO_RAPIDEZ
except ImportError as e:
    print(f"ERRO CRÍTICO(GeradorCogumelos): Classe 'Cogumelo' ou tipos não encontrados: {e}. Cogumelos não serão gerados.")
    Cogumelo = None
    TIPO_CURA, TIPO_LENTIDAO, TIPO_RAPIDEZ = None, None, None

class GeradorCogumelos:
    def __init__(self, max_cogumelos_na_tela=1):
        # --- ALTERADO: Renomeado de 'cogumelos_ativos' para 'cogumelos' para consistência ---
        self.cogumelos = pygame.sprite.Group()
        self.max_cogumelos_na_tela = max_cogumelos_na_tela
        
        self.spawn_cooldown_apos_coleta_s = 20
        self.spawn_chance_por_frame = 0.05 # 5% de chance de spawnar por frame

        # Distância máxima do jogador para um cogumelo antes de ser removido (em pixels).
        self.distancia_maxima_cogumelo = 2000

        self.tipos_de_cogumelo_disponiveis = []
        # Adiciona apenas os tipos que foram importados com sucesso
        if TIPO_CURA: self.tipos_de_cogumelo_disponiveis.append(TIPO_CURA)
        if TIPO_LENTIDAO: self.tipos_de_cogumelo_disponiveis.append(TIPO_LENTIDAO)
        if TIPO_RAPIDEZ: self.tipos_de_cogumelo_disponiveis.append(TIPO_RAPIDEZ)
        
        if not self.tipos_de_cogumelo_disponiveis:
            print("ERRO CRÍTICO(GeradorCogumelos): Nenhum tipo de cogumelo válido disponível para spawn. Verifique importações em cogumelo.py.")

        self.ultimo_cogumelo_coletado_time = 0
        self.deve_gerar_proximo_cogumelo = False
        self.ja_gerou_cogumelo_inicial = False
        
    def ajustar_geracao_cogumelos(self, novo_cooldown_s: int = None, nova_chance_por_frame: float = None, nova_distancia_maxima: int = None):
        """
        Permite ajustar as configurações de geração de cogumelos dinamicamente.
        :param novo_cooldown_s: Novo tempo de cooldown em segundos após a coleta.
        :param nova_chance_por_frame: Nova probabilidade (float 0.0-1.0) de tentar spawnar por frame (para spawns aleatórios).
        :param nova_distancia_maxima: Nova distância máxima para um cogumelo do jogador antes de ser removido.
        """
        if novo_cooldown_s is not None and novo_cooldown_s >= 0:
            self.spawn_cooldown_apos_coleta_s = novo_cooldown_s
        if nova_chance_por_frame is not None and 0.0 <= nova_chance_por_frame <= 1.0:
            self.spawn_chance_por_frame = nova_chance_por_frame
        if nova_distancia_maxima is not None and nova_distancia_maxima > 0:
            self.distancia_maxima_cogumelo = nova_distancia_maxima

    def _escolher_tipo_cogumelo_aleatorio(self):
        """
        Escolhe um tipo de cogumelo aleatoriamente entre os disponíveis.
        """
        if not self.tipos_de_cogumelo_disponiveis:
            return None
        return random.choice(self.tipos_de_cogumelo_disponiveis)

    def tentar_gerar_cogumelo(self, player_rect, blocos_ja_gerados_set):
        """
        Gerencia o spawn de cogumelos: um inicial, um garantido após coleta, e spawns aleatórios.
        """
        if Cogumelo is None:
            return

        # Lógica de Spawn Garantido (Inicial e Pós-Coleta)
        if (not self.ja_gerou_cogumelo_inicial) or \
           (self.deve_gerar_proximo_cogumelo and time.time() - self.ultimo_cogumelo_coletado_time >= self.spawn_cooldown_apos_coleta_s):
            
            if self._spawnar_novo_cogumelo_em_bloco(player_rect, blocos_ja_gerados_set):
                self.ja_gerou_cogumelo_inicial = True
                self.deve_gerar_proximo_cogumelo = False
            return

        # Lógica de Spawn Aleatório
        if len(self.cogumelos) < self.max_cogumelos_na_tela and not self.deve_gerar_proximo_cogumelo: 
            if random.random() < self.spawn_chance_por_frame:
                self._spawnar_novo_cogumelo_em_bloco(player_rect, blocos_ja_gerados_set)

        # Remoção de Cogumelos Distantes
        if player_rect and hasattr(player_rect, 'center'):
            player_center_x, player_center_y = player_rect.center
            for cogumelo in list(self.cogumelos):
                distancia = math.hypot(cogumelo.rect.centerx - player_center_x, cogumelo.rect.centery - player_center_y)
                if distancia > self.distancia_maxima_cogumelo:
                    cogumelo.kill()

    def _spawnar_novo_cogumelo_em_bloco(self, player_rect, blocos_ja_gerados_set, tipo_para_spawn=None):
        """Função auxiliar para realmente spawnar um cogumelo em um bloco conhecido."""
        if Cogumelo is None or not blocos_ja_gerados_set:
            return False

        bloco_spawn_x, bloco_spawn_y = random.choice(list(blocos_ja_gerados_set))
        
        bloco_tamanho_geracao = 1080
        base_x_mundo = bloco_spawn_x * bloco_tamanho_geracao
        base_y_mundo = bloco_spawn_y * bloco_tamanho_geracao

        spawn_x = base_x_mundo + random.randint(50, bloco_tamanho_geracao - 50)
        spawn_y = base_y_mundo + random.randint(50, bloco_tamanho_geracao - 50)
        
        if not tipo_para_spawn:
            tipo_para_spawn = self._escolher_tipo_cogumelo_aleatorio()

        if tipo_para_spawn:
            novo_cogumelo = Cogumelo(spawn_x, spawn_y, tipo_para_spawn)
            # --- ALTERADO: Usando 'self.cogumelos' ---
            self.cogumelos.add(novo_cogumelo)
            return True
        return False

    def update(self, jogador_ref, cam_x, cam_y, dt_ms):
        """Atualiza a lógica dos cogumelos, incluindo colisão com o jogador e gerenciamento de efeitos."""
        # --- ALTERADO: Usando 'self.cogumelos' ---
        self.cogumelos.update() 
        
        # Colisão com o jogador
        if jogador_ref and hasattr(jogador_ref, 'rect_colisao'):
            # --- ALTERADO: Usando 'self.cogumelos' ---
            cogumelos_coletados = pygame.sprite.spritecollide(jogador_ref, self.cogumelos, True)
            for cogumelo in cogumelos_coletados:
                cogumelo.aplicar_efeito(jogador_ref)
                self.ultimo_cogumelo_coletado_time = time.time()
                self.deve_gerar_proximo_cogumelo = True
    
        # Gerenciamento dos efeitos de status do jogador
        # Resetar lentidão
        if hasattr(jogador_ref, 'tempo_fim_efeito_lentidao') and jogador_ref.tempo_fim_efeito_lentidao > 0:
            if time.time() >= jogador_ref.tempo_fim_efeito_lentidao:
                if hasattr(jogador_ref, 'velocidade_original') and hasattr(jogador_ref, 'velocidade'):
                    jogador_ref.velocidade = jogador_ref.velocidade_original
                    jogador_ref.tempo_fim_efeito_lentidao = 0
        
        # Resetar rapidez
        if hasattr(jogador_ref, 'tempo_fim_efeito_rapidez') and jogador_ref.tempo_fim_efeito_rapidez > 0:
            if time.time() >= jogador_ref.tempo_fim_efeito_rapidez:
                if hasattr(jogador_ref, 'velocidade_original') and hasattr(jogador_ref, 'velocidade'):
                    jogador_ref.velocidade = jogador_ref.velocidade_original
                    jogador_ref.tempo_fim_efeito_rapidez = 0

    # --- REMOVIDO: O método 'desenhar_cogumelos' foi removido por ser redundante.
    # A lógica de desenho já é tratada no loop principal de 'Game.py'.
