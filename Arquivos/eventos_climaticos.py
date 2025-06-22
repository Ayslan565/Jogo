# Arquivo: eventos_climaticos.py (Atualizado com HUD de status)

import pygame
import random
import time
import math
import os

class GerenciadorDeEventos:
    """
    Gerencia eventos climáticos como chuva e neve, o ciclo de dia e noite,
    e agora também desenha um HUD com o status do tempo e o contador da estação.
    """
    def __init__(self, largura_tela, altura_tela, estacoes_obj):
        """
        Inicializa o gerenciador de eventos climáticos.
        """
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.estacoes = estacoes_obj # Referência ao objeto de estações

        # --- Configurações do Ciclo Dia/Noite ---
        self.duracao_dia_noite_seg = 50
        self.ultimo_tempo_ciclo = time.time()
        self.alpha_noite = 0
        self.e_noite = False

        # --- Configurações dos Efeitos Climáticos ---
        self.particulas_chuva = []
        self.particulas_neve = []
        self.clima_atual = "limpo"
        self.tempo_troca_clima_seg = 15 # Aumentado para trocas menos frequentes
        self.ultimo_tempo_troca_clima = time.time()
        
        # --- Variáveis para Intensidade e Escurecimento ---
        self.intensidade_max_chuva = 1050
        self.intensidade_max_neve = 1000
        self.tempo_inicio_evento = 0
        self.duracao_intensificacao = 30
        
        self.alpha_clima = 0
        self.max_alpha_clima = 100
        self.cor_escura_chuva = (20, 20, 30)
        self.cor_escura_neve = (60, 60, 75)

        # --- Configurações do novo HUD ---
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fonte_path = os.path.join(project_root, "Fontes", "Retro Gaming.ttf")
        try:
            self.fonte_hud = pygame.font.Font(fonte_path, 28)
        except pygame.error:
            print(f"AVISO: Fonte '{fonte_path}' não encontrada. Usando fonte padrão.")
            self.fonte_hud = pygame.font.Font(None, 32)
        
        # <<< AQUI VOCÊ PODE GERENCIAR A POSIÇÃO DO HUD >>>
        # Valores representam a distância a partir do canto superior direito.
        self.hud_offset_x = 20  # Distância da borda direita
        self.hud_offset_y = 90  # Distância da borda de cima
        
        # Criação dos ícones de status
        self.icones = {
            "sol": self._criar_icone_sol(),
            "lua": self._criar_icone_lua(),
            "chuva": self._criar_icone_chuva(),
            "neve": self._criar_icone_neve()
        }

        self.atualizar_clima()

    def _criar_icone_sol(self):
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 220, 0), (16, 16), 10) # Sol
        return surf

    def _criar_icone_lua(self):
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(surf, (230, 230, 250), (16, 16), 10) # Lua cheia
        pygame.draw.circle(surf, (0, 0, 0, 0), (22, 12), 8) # Recorte para crescente
        return surf

    def _criar_icone_chuva(self):
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(surf, (150, 150, 170), (6, 5, 20, 10), border_radius=5) # Nuvem
        pygame.draw.line(surf, (100, 149, 237), (12, 18), (8, 28), 2) # Gota
        pygame.draw.line(surf, (100, 149, 237), (20, 18), (16, 28), 2) # Gota
        return surf

    def _criar_icone_neve(self):
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        p_centro = (16, 16)
        pygame.draw.line(surf, (200, 220, 255), (p_centro[0], p_centro[1]-12), (p_centro[0], p_centro[1]+12), 3) # Linha vertical
        pygame.draw.line(surf, (200, 220, 255), (p_centro[0]-12, p_centro[1]), (p_centro[0]+12, p_centro[1]), 3) # Linha horizontal
        pygame.draw.line(surf, (200, 220, 255), (p_centro[0]-8, p_centro[1]-8), (p_centro[0]+8, p_centro[1]+8), 3) # Diagonal 1
        pygame.draw.line(surf, (200, 220, 255), (p_centro[0]-8, p_centro[1]+8), (p_centro[0]+8, p_centro[1]-8), 3) # Diagonal 2
        return surf

    def _criar_particula_chuva(self):
        x = random.randint(0, self.largura_tela)
        y = random.randint(-self.altura_tela, 0)
        tamanho = random.randint(2, 4)
        velocidade = random.randint(12, 18)
        cor = (100, 149, 237)
        return {"rect": pygame.Rect(x, y, tamanho, tamanho), "velocidade": velocidade, "cor": cor}

    def _criar_particula_neve(self):
        x = random.randint(0, self.largura_tela)
        y = random.randint(-self.altura_tela, 0)
        raio = random.randint(2, 5)
        velocidade_y = random.uniform(1, 3)
        velocidade_x = random.uniform(-1, 1)
        cor = (255, 255, 255)
        return {"x": x, "y": y, "raio": raio, "vy": velocidade_y, "vx": velocidade_x, "cor": cor}

    def atualizar_ciclo_dia_noite(self):
        tempo_decorrido = (time.time() - self.ultimo_tempo_ciclo) % self.duracao_dia_noite_seg
        progresso_ciclo = tempo_decorrido / self.duracao_dia_noite_seg
        fator_escuridao = (1 - math.cos(progresso_ciclo * math.pi * 2)) / 2
        self.alpha_noite = int(fator_escuridao * 150)
        self.e_noite = self.alpha_noite > 75

    def atualizar_clima(self):
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_tempo_troca_clima > self.tempo_troca_clima_seg:
            self.ultimo_tempo_troca_clima = tempo_atual
            nome_estacao = self.estacoes.nome_estacao_atual()
            probabilidade = random.random()
            novo_clima = "limpo"
            if nome_estacao == "Inverno":
                if probabilidade < 0.6: novo_clima = "neve"
            elif nome_estacao in ["Primavera", "Outono"]:
                if probabilidade < 0.5: novo_clima = "chuva"
            else: # Verão
                if probabilidade < 0.15: novo_clima = "chuva"
            if novo_clima != self.clima_atual and novo_clima != "limpo":
                self.tempo_inicio_evento = time.time()
            self.clima_atual = novo_clima

    def atualizar_particulas(self):
        if self.clima_atual != "limpo":
            tempo_decorrido = time.time() - self.tempo_inicio_evento
            progresso = min(1.0, tempo_decorrido / self.duracao_intensificacao)
            self.alpha_clima = int(progresso * self.max_alpha_clima)
            if self.clima_atual == "chuva":
                num_alvo_particulas = int(progresso * self.intensidade_max_chuva)
                while len(self.particulas_chuva) < num_alvo_particulas:
                    self.particulas_chuva.append(self._criar_particula_chuva())
                self.particulas_neve.clear()
            elif self.clima_atual == "neve":
                num_alvo_particulas = int(progresso * self.intensidade_max_neve)
                while len(self.particulas_neve) < num_alvo_particulas:
                    self.particulas_neve.append(self._criar_particula_neve())
                self.particulas_chuva.clear()
        else:
            if self.alpha_clima > 0: self.alpha_clima = max(0, self.alpha_clima - 2)
            if self.particulas_chuva: self.particulas_chuva.pop(0)
            if self.particulas_neve: self.particulas_neve.pop(0)

        for particula in self.particulas_chuva:
            particula["rect"].y += particula["velocidade"]
            if particula["rect"].top > self.altura_tela:
                particula["rect"].bottom = 0
                particula["rect"].x = random.randint(0, self.largura_tela)
        for particula in self.particulas_neve:
            particula["y"] += particula["vy"]
            particula["x"] += particula["vx"]
            if particula["y"] > self.altura_tela:
                particula["y"] = random.randint(-50, -10)
                particula["x"] = random.randint(0, self.largura_tela)

    def desenhar(self, tela):
        """
        Desenha as sobreposições de clima/noite, as partículas E o novo HUD de status.
        """
        if self.alpha_noite > 0:
            sobreposicao_noite = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
            sobreposicao_noite.fill((0, 0, 15, self.alpha_noite))
            tela.blit(sobreposicao_noite, (0, 0))
        if self.alpha_clima > 0:
            sobreposicao_clima = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
            cor_atual = self.cor_escura_chuva if self.clima_atual == 'chuva' else self.cor_escura_neve
            sobreposicao_clima.fill((*cor_atual, self.alpha_clima))
            tela.blit(sobreposicao_clima, (0,0))
        for particula in self.particulas_chuva:
            pygame.draw.rect(tela, particula["cor"], particula["rect"])
        for particula in self.particulas_neve:
            pygame.draw.circle(tela, particula["cor"], (int(particula["x"]), int(particula["y"])), particula["raio"])

        self.desenhar_hud_status(tela)

    def desenhar_hud_status(self, tela):
        """Desenha o ícone de status e o contador de tempo com um fundo e borda."""
        # Seleciona o ícone correto
        if self.clima_atual == "chuva":
            icone_atual = self.icones["chuva"]
        elif self.clima_atual == "neve":
            icone_atual = self.icones["neve"]
        elif self.e_noite:
            icone_atual = self.icones["lua"]
        else:
            icone_atual = self.icones["sol"]
        
        # Obtém o tempo restante da estação
        tempo_restante_str = "00:00"
        if hasattr(self.estacoes, 'get_tempo_restante_formatado'):
            tempo_restante_str = self.estacoes.get_tempo_restante_formatado()
        
        # Renderiza o texto do tempo
        texto_surface = self.fonte_hud.render(tempo_restante_str, True, (255, 255, 255))
        texto_rect = texto_surface.get_rect()

        # --- Lógica do Fundo com Borda ---
        padding = 5
        espacamento = 10
        largura_hud = icone_atual.get_width() + espacamento + texto_rect.width + padding * 2
        altura_hud = max(icone_atual.get_height(), texto_rect.height) + padding * 2
        
        # Cria a superfície para o HUD
        hud_surf = pygame.Surface((largura_hud, altura_hud), pygame.SRCALPHA)
        
        # Desenha o fundo e a borda
        fundo_color = (20, 20, 30, 180) # Cinza escuro semi-transparente
        borda_color = (200, 200, 220, 200) # Borda clara
        pygame.draw.rect(hud_surf, fundo_color, hud_surf.get_rect(), border_radius=5)
        pygame.draw.rect(hud_surf, borda_color, hud_surf.get_rect(), width=2, border_radius=5)
        
        # Desenha o ícone na superfície do HUD
        pos_icone_y = (altura_hud - icone_atual.get_height()) // 2
        hud_surf.blit(icone_atual, (padding, pos_icone_y))
        
        # Desenha o texto na superfície do HUD
        pos_texto_y = (altura_hud - texto_rect.height) // 2
        hud_surf.blit(texto_surface, (padding + icone_atual.get_width() + espacamento, pos_texto_y))
        
        # Posiciona e desenha o HUD completo na tela principal
        pos_final_x = self.largura_tela - self.hud_offset_x - largura_hud
        pos_final_y = self.hud_offset_y
        tela.blit(hud_surf, (pos_final_x, pos_final_y))

    def interromper_evento_climatico(self):
        """
        Interrompe forçadamente qualquer evento climático (chuva ou neve).
        """
        if self.clima_atual != "limpo":
            print(f"INFO: Interrompendo evento climático '{self.clima_atual}' para a luta de chefe.")
        
        self.clima_atual = "limpo"
        self.particulas_chuva.clear()
        self.particulas_neve.clear()
        self.alpha_clima = 0
        self.ultimo_tempo_troca_clima = time.time()

    def reativar_eventos_climaticos(self):
        """
        Reativa o sistema de eventos climáticos após uma interrupção.
        """
        print("INFO: Sistema de clima reativado. O clima voltará ao normal.")
        self.ultimo_tempo_troca_clima = time.time()
