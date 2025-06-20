# Arquivo: eventos_climaticos.py (Atualizado com Escurecimento Gradual)

import pygame
import random
import time
import math

class GerenciadorDeEventos:
    """
    Gerencia eventos climáticos como chuva e neve, e o ciclo de dia e noite,
    de forma complementar ao sistema de estações.
    Os eventos climáticos agora começam fracos, se intensificam com o tempo
    e escurecem a tela gradualmente.
    """
    def __init__(self, largura_tela, altura_tela, estacoes_obj):
        """
        Inicializa o gerenciador de eventos climáticos.
        """
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.estacoes = estacoes_obj

        # --- Configurações do Ciclo Dia/Noite ---
        self.duracao_dia_noite_seg = 30
        self.ultimo_tempo_ciclo = time.time()
        self.alpha_noite = 0
        self.e_noite = False

        # --- Configurações dos Efeitos Climáticos ---
        self.particulas_chuva = []
        self.particulas_neve = []
        self.clima_atual = "limpo"
        self.tempo_troca_clima_seg = 40
        self.ultimo_tempo_troca_clima = time.time()
        
        # --- Variáveis para Intensidade e Escurecimento ---
        self.intensidade_max_chuva = 1050  # Número máximo de gotas de chuva
        self.intensidade_max_neve = 1000   # Número máximo de flocos de neve
        self.tempo_inicio_evento = 0      # Marca quando o evento (chuva/neve) começou
        self.duracao_intensificacao = 30  # Segundos para atingir a intensidade máxima
        
        # Novo: Controles para o escurecimento gradual da tela
        self.alpha_clima = 0
        self.max_alpha_clima = 100  # Nível máximo de escuridão (0-255)
        self.cor_escura_chuva = (20, 20, 30) # Cor de sobreposição para chuva
        self.cor_escura_neve = (60, 60, 75)   # Cor de sobreposição para neve

        self.atualizar_clima()

    def _criar_particula_chuva(self):
        """Cria uma nova partícula de chuva como um quadrado azul."""
        x = random.randint(0, self.largura_tela)
        y = random.randint(-self.altura_tela, 0)
        tamanho = random.randint(2, 4) # Tamanho do quadrado
        velocidade = random.randint(12, 18)
        cor = (100, 149, 237)  # Azul-cornflower
        return {"rect": pygame.Rect(x, y, tamanho, tamanho), "velocidade": velocidade, "cor": cor}

    def _criar_particula_neve(self):
        """Cria uma nova partícula de neve."""
        x = random.randint(0, self.largura_tela)
        y = random.randint(-self.altura_tela, 0)
        raio = random.randint(2, 5)
        velocidade_y = random.uniform(1, 3)
        velocidade_x = random.uniform(-1, 1)
        cor = (255, 255, 255)
        return {"x": x, "y": y, "raio": raio, "vy": velocidade_y, "vx": velocidade_x, "cor": cor}

    def atualizar_ciclo_dia_noite(self):
        """
        Atualiza a transparência da sobreposição de noite.
        """
        tempo_decorrido = (time.time() - self.ultimo_tempo_ciclo) % self.duracao_dia_noite_seg
        progresso_ciclo = tempo_decorrido / self.duracao_dia_noite_seg
        fator_escuridao = (1 - math.cos(progresso_ciclo * math.pi * 2)) / 2
        self.alpha_noite = int(fator_escuridao * 150)
        self.e_noite = self.alpha_noite > 75

    def atualizar_clima(self):
        """
        Verifica se deve mudar o clima e inicia um novo evento climático,
        resetando a intensidade.
        """
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_tempo_troca_clima > self.tempo_troca_clima_seg:
            self.ultimo_tempo_troca_clima = tempo_atual
            
            nome_estacao = self.estacoes.nome_estacao_atual()
            probabilidade = random.random()

            novo_clima = "limpo" # Padrão
            
            if nome_estacao == "Inverno":
                if probabilidade < 0.6: # 60% de chance de nevasca
                    novo_clima = "neve"
            elif nome_estacao in ["Primavera", "Outono"]:
                if probabilidade < 0.5: # 50% de chance de chuva
                    novo_clima = "chuva"
            else: # Verão
                if probabilidade < 0.15: # 15% de chance de chuva de verão
                    novo_clima = "chuva"
            
            # Se o clima mudou para um evento, reseta o temporizador de intensidade
            # Não reseta se já estiver chovendo/nevando para manter a intensidade
            if novo_clima != self.clima_atual and novo_clima != "limpo":
                self.tempo_inicio_evento = time.time()
            
            self.clima_atual = novo_clima
            print(f"DEBUG(EventosClimaticos): O clima mudou para '{self.clima_atual}'.")

    def atualizar_particulas(self):
        """
        Atualiza a intensidade dos eventos, o escurecimento e o movimento das partículas.
        """
        # --- Lógica de Intensidade e Escurecimento ---
        if self.clima_atual != "limpo":
            tempo_decorrido = time.time() - self.tempo_inicio_evento
            progresso = min(1.0, tempo_decorrido / self.duracao_intensificacao)
            
            # Atualiza o alpha do escurecimento
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
            # Clareia a tela e remove partículas gradualmente
            if self.alpha_clima > 0:
                self.alpha_clima = max(0, self.alpha_clima - 2)
            if self.particulas_chuva: self.particulas_chuva.pop(0)
            if self.particulas_neve: self.particulas_neve.pop(0)

        # --- Lógica de Movimento das Partículas ---
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
        Desenha as sobreposições de noite/clima e os efeitos de partículas.
        """
        # --- Sobreposição de Noite ---
        if self.alpha_noite > 0:
            sobreposicao_noite = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
            sobreposicao_noite.fill((0, 0, 15, self.alpha_noite))
            tela.blit(sobreposicao_noite, (0, 0))
            
        # --- Sobreposição de Escurecimento do Clima ---
        if self.alpha_clima > 0:
            sobreposicao_clima = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
            cor_atual = self.cor_escura_chuva if self.clima_atual == 'chuva' else self.cor_escura_neve
            sobreposicao_clima.fill((cor_atual[0], cor_atual[1], cor_atual[2], self.alpha_clima))
            tela.blit(sobreposicao_clima, (0,0))

        # --- Partículas ---
        for particula in self.particulas_chuva:
            pygame.draw.rect(tela, particula["cor"], particula["rect"])

        for particula in self.particulas_neve:
            pygame.draw.circle(tela, particula["cor"], (int(particula["x"]), int(particula["y"])), particula["raio"])
