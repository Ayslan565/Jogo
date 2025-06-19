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
        self.cogumelos_ativos = pygame.sprite.Group()
        self.max_cogumelos_na_tela = max_cogumelos_na_tela
        
        self.spawn_cooldown_apos_coleta_s = 20
      
        self.spawn_chance_por_frame = 0.05 #5% de chance de spawnar por frame

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
            print(f"DEBUG(GeradorCogumelos): Cooldown de spawn ajustado para: {self.spawn_cooldown_apos_coleta_s}s")

        if nova_chance_por_frame is not None and 0.0 <= nova_chance_por_frame <= 1.0:
            self.spawn_chance_por_frame = nova_chance_por_frame
            print(f"DEBUG(GeradorCogumelos): Chance de spawn por frame ajustada para: {self.spawn_chance_por_frame}")

        if nova_distancia_maxima is not None and nova_distancia_maxima > 0:
            self.distancia_maxima_cogumelo = nova_distancia_maxima
            print(f"DEBUG(GeradorCogumelos): Distância máxima para remoção de cogumelos ajustada para: {self.distancia_maxima_cogumelo}px")


    def _escolher_tipo_cogumelo_aleatorio(self):
        """
        Escolhe um tipo de cogumelo aleatoriamente entre os disponíveis.
        Todos os tipos disponíveis têm a mesma chance de serem escolhidos.
        """
        if not self.tipos_de_cogumelo_disponiveis:
            return None # Não há tipos disponíveis para spawnar
        return random.choice(self.tipos_de_cogumelo_disponiveis) # Escolhe aleatoriamente entre os tipos

    def tentar_gerar_cogumelo(self, player_rect, blocos_ja_gerados_set):
        """
        Gerencia o spawn de cogumelos: um inicial, um garantido após coleta, e spawns aleatórios.
        Também remove cogumelos muito distantes.
        """
        if Cogumelo is None: #
            return # Não gera se a classe Cogumelo não foi importada

        # --- Lógica de Spawn Garantido (Inicial e Pós-Coleta) ---
        # Garante que sempre haja 1 cogumelo se o limite é 1, ou spawna o inicial/pós-coleta.
        if (not self.ja_gerou_cogumelo_inicial) or \
           (self.deve_gerar_proximo_cogumelo and time.time() - self.ultimo_cogumelo_coletado_time >= self.spawn_cooldown_apos_coleta_s):
            
            if self._spawnar_novo_cogumelo_em_bloco(player_rect, blocos_ja_gerados_set):
                self.ja_gerou_cogumelo_inicial = True
                self.deve_gerar_proximo_cogumelo = False # Reseta a flag após spawn garantido
            return # Tenta gerar o garantido e sai

        # --- Lógica de Spawn Aleatório (se não houver cogumelos na tela e não estiver em cooldown de spawn garantido) ---
        # Só tenta spawnar aleatoriamente se a quantidade de cogumelos for menor que o máximo
        # E se não houver um cogumelo garantido esperando para ser spawnado.
        if len(self.cogumelos_ativos) < self.max_cogumelos_na_tela and \
           not self.deve_gerar_proximo_cogumelo: 
            # Verifica a probabilidade de ser gerado a cada frame
            if random.random() < self.spawn_chance_por_frame: # Usar '<' para 'chance' ser a probabilidade de SUCESSO
                self._spawnar_novo_cogumelo_em_bloco(player_rect, blocos_ja_gerados_set)

        # --- Remoção de Cogumelos Distantes ---
        if player_rect and hasattr(player_rect, 'center'):
            player_center_x, player_center_y = player_rect.center
            for cogumelo in list(self.cogumelos_ativos): # Itera sobre uma cópia para poder remover
                distancia = math.hypot(cogumelo.rect.centerx - player_center_x, cogumelo.rect.centery - player_center_y)
                if distancia > self.distancia_maxima_cogumelo:
                    cogumelo.kill()
                    print(f"DEBUG(GeradorCogumelos): Cogumelo em ({cogumelo.x}, {cogumelo.y}) removido por estar muito distante. Total: {len(self.cogumelos_ativos)}")
                    # Se um cogumelo distante for removido, podemos considerar isso como uma "coleta" forçada
                    # para tentar gerar um substituto mais perto, se a contagem permitir.
                    # No entanto, a lógica atual já lida com o max_cogumelos_na_tela e cooldown.
                    # Não setamos 'deve_gerar_proximo_cogumelo' aqui para evitar um spawn garantido por remoção de longe.


    def _spawnar_novo_cogumelo_em_bloco(self, player_rect, blocos_ja_gerados_set, tipo_para_spawn=None):
        """Função auxiliar para realmente spawnar um cogumelo em um bloco conhecido."""
        if Cogumelo is None: #
            return False # Não spawnou
        
        if not blocos_ja_gerados_set: #
            # print("AVISO(GeradorCogumelos): Não há blocos gerados para spawnar cogumelo.")
            return False

        # Verifica se há blocos válidos para escolher
        if not blocos_ja_gerados_set:
            # print("AVISO(GeradorCogumelos): Não há blocos gerados para spawnar cogumelo.")
            return False

        bloco_spawn_x, bloco_spawn_y = random.choice(list(blocos_ja_gerados_set))
        
        bloco_tamanho_geracao = 1080 # Mesma do Game.py
        base_x_mundo = bloco_spawn_x * bloco_tamanho_geracao
        base_y_mundo = bloco_spawn_y * bloco_tamanho_geracao

        spawn_x = base_x_mundo + random.randint(50, bloco_tamanho_geracao - 50)
        spawn_y = base_y_mundo + random.randint(50, bloco_tamanho_geracao - 50)
        
        if not tipo_para_spawn: # Se nenhum tipo for especificado, escolhe aleatoriamente
            tipo_para_spawn = self._escolher_tipo_cogumelo_aleatorio()

        if tipo_para_spawn: #
            novo_cogumelo = Cogumelo(spawn_x, spawn_y, tipo_para_spawn)
            self.cogumelos_ativos.add(novo_cogumelo)
            # último_cogumelo_coletado_time não é atualizado aqui para não interferir com o cooldown de coleta.
            print(f"DEBUG(GeradorCogumelos): Cogumelo de {tipo_para_spawn} gerado em ({spawn_x}, {spawn_y}). Total: {len(self.cogumelos_ativos)}")
            return True # Spawnou com sucesso
        return False # Falhou ao spawnar


    def update(self, jogador_ref, cam_x, cam_y, dt_ms):
        """Atualiza a lógica dos cogumelos na tela, incluindo colisão com o jogador e gerenciamento de efeitos."""
        self.cogumelos_ativos.update() # Se houver lógica de update na classe Cogumelo
        
        # Colisão com o jogador
        if jogador_ref and hasattr(jogador_ref, 'rect_colisao'):
            # Verifica colisão do ret_colisao do jogador com os cogumelos
            # Remove o sprite automaticamente ao coletar (coletar() chama kill())
            cogumelos_coletados = pygame.sprite.spritecollide(jogador_ref, self.cogumelos_ativos, True)
            for cogumelo in cogumelos_coletados:
                cogumelo.aplicar_efeito(jogador_ref) # Chama o método aplicar_efeito do cogumelo
                self.ultimo_cogumelo_coletado_time = time.time() # Registra o tempo da coleta
                self.deve_gerar_proximo_cogumelo = True # Seta a flag para gerar o próximo cogumelo garantidamente
    
        # Gerenciamento dos efeitos de status do jogador
        # Resetar lentidão
        if hasattr(jogador_ref, 'tempo_fim_efeito_lentidao') and jogador_ref.tempo_fim_efeito_lentidao > 0:
            if time.time() >= jogador_ref.tempo_fim_efeito_lentidao:
                if hasattr(jogador_ref, 'velocidade_original') and hasattr(jogador_ref, 'velocidade'):
                    jogador_ref.velocidade = jogador_ref.velocidade_original
                    jogador_ref.tempo_fim_efeito_lentidao = 0
                    print("DEBUG(GeradorCogumelos): Efeito de lentidão do jogador terminou.")
        
        # Resetar rapidez
        if hasattr(jogador_ref, 'tempo_fim_efeito_rapidez') and jogador_ref.tempo_fim_efeito_rapidez > 0:
            if time.time() >= jogador_ref.tempo_fim_efeito_rapidez:
                if hasattr(jogador_ref, 'velocidade_original') and hasattr(jogador_ref, 'velocidade'):
                    jogador_ref.velocidade = jogador_ref.velocidade_original
                    jogador_ref.tempo_fim_efeito_rapidez = 0
                    print("DEBUG(GeradorCogumelos): Efeito de rapidez do jogador terminou.")


    def desenhar_cogumelos(self, janela, camera_x, camera_y):
        """Desenha todos os cogumelos ativos na tela."""
        for cogumelo in self.cogumelos_ativos:
            cogumelo.desenhar(janela, camera_x, camera_y)
