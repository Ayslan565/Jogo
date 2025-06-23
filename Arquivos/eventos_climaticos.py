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
        self.particulas_chuva = [] # <-- ALTERADO: Inicializado como lista vazia
        self.particulas_neve = []  # <-- ALTERADO: Inicializado como lista vazia
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
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # --- ADICIONADO: Configurações de Som ---
        self.som_chuva = None
        self.som_neve = None
        self.canal_clima = pygame.mixer.Channel(1) # Usa o canal 1 para sons de clima
        
        try:
            # <-- ALTERADO: Corrigido o caminho para "Eventos climaticos"
            caminho_som_chuva = os.path.join(project_root, "Musica", "Eventos climaticos", "chuva.mp3")
            self.som_chuva = pygame.mixer.Sound(caminho_som_chuva)
            self.som_chuva.set_volume(0.4) # Ajuste o volume conforme necessário
        except pygame.error:
            print(f"AVISO: Arquivo de som de chuva não encontrado em '{caminho_som_chuva}'.")
            
        try:
            # <-- ALTERADO: Corrigido o caminho para "Eventos climaticos"
            caminho_som_neve = os.path.join(project_root, "Musica", "Eventos climaticos", "neve.mp3")
            self.som_neve = pygame.mixer.Sound(caminho_som_neve)
            self.som_neve.set_volume(0.5) # Ajuste o volume conforme necessário
        except pygame.error:
            print(f"AVISO: Arquivo de som de neve não encontrado em '{caminho_som_neve}'.")
        # --- FIM DA ADIÇÃO ---

        # --- Configurações do novo HUD ---
        fonte_path = os.path.join(project_root, "Fontes", "Retro Gaming.ttf")
        try:
            self.fonte_hud = pygame.font.Font(fonte_path, 28)
        except pygame.error:
            print(f"AVISO: Fonte '{fonte_path}' não encontrada. Usando fonte padrão.")
            self.fonte_hud = pygame.font.Font(None, 32)
        
        self.hud_offset_x = 20
        self.hud_offset_y = 90
        
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
        pygame.draw.line(surf, (200, 220, 255), (p_centro[0], p_centro[1]-12), (p_centro[0], p_centro[1]+12), 3)
        pygame.draw.line(surf, (200, 220, 255), (p_centro[0]-12, p_centro[1]), (p_centro[0]+12, p_centro[1]), 3)
        pygame.draw.line(surf, (200, 220, 255), (p_centro[0]-8, p_centro[1]-8), (p_centro[0]+8, p_centro[1]+8), 3)
        pygame.draw.line(surf, (200, 220, 255), (p_centro[0]-8, p_centro[1]+8), (p_centro[0]+8, p_centro[1]-8), 3)
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
            
            if novo_clima != self.clima_atual:
                self.tempo_inicio_evento = time.time()
                
                # --- ADICIONADO: Controle de som do clima ---
                self.canal_clima.fadeout(1500) # Para o som atual suavemente

                if novo_clima == "chuva" and self.som_chuva:
                    self.canal_clima.play(self.som_chuva, loops=-1, fade_ms=2000)
                elif novo_clima == "neve" and self.som_neve:
                    self.canal_clima.play(self.som_neve, loops=-1, fade_ms=2000)
                # --- FIM DA ADIÇÃO ---

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

        # Laço para atualizar partículas de chuva
        for particula in self.particulas_chuva:
            # Verifica se 'particula' é um dicionário antes de tentar acessar 'rect'
            if isinstance(particula, dict):
                particula["rect"].y += particula["velocidade"]
                if particula["rect"].top > self.altura_tela:
                    particula["rect"].bottom = 0
                    particula["rect"].x = random.randint(0, self.largura_tela)

        # Laço para atualizar partículas de neve
        for particula in self.particulas_neve:
            # Verifica se 'particula' é um dicionário antes de acessar suas chaves
            if isinstance(particula, dict):
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

        # Laço para desenhar partículas de chuva
        for particula in self.particulas_chuva:
            if isinstance(particula, dict):
                pygame.draw.rect(tela, particula["cor"], particula["rect"])

        # Laço para desenhar partículas de neve
        for particula in self.particulas_neve:
            if isinstance(particula, dict):
                pygame.draw.circle(tela, particula["cor"], (int(particula["x"]), int(particula["y"])), particula["raio"])

        self.desenhar_hud_status(tela)

    def desenhar_hud_status(self, tela):
        """Desenha o ícone de status e o contador de tempo com um fundo e borda."""
        if self.clima_atual == "chuva":
            icone_atual = self.icones["chuva"]
        elif self.clima_atual == "neve":
            icone_atual = self.icones["neve"]
        elif self.e_noite:
            icone_atual = self.icones["lua"]
        else:
            icone_atual = self.icones["sol"]
        
        tempo_restante_str = "00:00"
        if hasattr(self.estacoes, 'get_tempo_restante_formatado'):
            tempo_restante_str = self.estacoes.get_tempo_restante_formatado()
        
        texto_surface = self.fonte_hud.render(tempo_restante_str, True, (255, 255, 255))
        texto_rect = texto_surface.get_rect()

        padding = 5
        espacamento = 10
        largura_hud = icone_atual.get_width() + espacamento + texto_rect.width + padding * 2
        altura_hud = max(icone_atual.get_height(), texto_rect.height) + padding * 2
        
        hud_surf = pygame.Surface((largura_hud, altura_hud), pygame.SRCALPHA)
        
        fundo_color = (20, 20, 30, 180)
        borda_color = (200, 200, 220, 200)
        pygame.draw.rect(hud_surf, fundo_color, hud_surf.get_rect(), border_radius=5)
        pygame.draw.rect(hud_surf, borda_color, hud_surf.get_rect(), width=2, border_radius=5)
        
        pos_icone_y = (altura_hud - icone_atual.get_height()) // 2
        hud_surf.blit(icone_atual, (padding, pos_icone_y))
        
        pos_texto_y = (altura_hud - texto_rect.height) // 2
        hud_surf.blit(texto_surface, (padding + icone_atual.get_width() + espacamento, pos_texto_y))
        
        pos_final_x = self.largura_tela - self.hud_offset_x - largura_hud
        pos_final_y = self.hud_offset_y
        tela.blit(hud_surf, (pos_final_x, pos_final_y))

    def interromper_evento_climatico(self):
        """
        Interrompe forçadamente qualquer evento climático (chuva ou neve).
        """
        # --- ADICIONADO: Parada suave do som ---
        if self.canal_clima.get_busy():
            self.canal_clima.fadeout(1000) # Para o som em 1 segundo
        
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