import pygame
import random
import time

FONTE_RETRO_PATH = "Fontes/Retro Gaming.ttf" # Certifique-se que este caminho é válido a partir da raiz do projeto
class Estacoes:
    def __init__(self):
        pygame.font.init() 
        self.nomes_estacoes_ordem = ["Primavera", "Verão", "Outono", "Inverno"] # Ordem definida
        self.indice_estacao_atual = random.randint(0, 3) # Começa em uma estação aleatória
        
        self.cor_atual = self._definir_cor_para_indice(self.indice_estacao_atual)
        self.tempo_troca_estacao_seg = 5  # segundos (2 minutos) - Ajustado para um tempo mais longo
        self.ultimo_tempo_troca_timestamp = time.time()
        
        self.mensagem_estacao_atual = self.nomes_estacoes_ordem[self.indice_estacao_atual]
        self.tempo_inicio_mensagem_estacao = self.ultimo_tempo_troca_timestamp

        # Controle do chefe da Primavera
        self.chefe_primavera_pendente = False
        self.chefe_primavera_derrotado_nesta_rodada_ciclica = False
        print(f"DEBUG(Estacoes): Iniciando na estação: {self.nome_estacao_atual()}")

    def nome_estacao_atual(self):
        """Retorna o nome da estação atual."""
        return self.nomes_estacoes_ordem[self.indice_estacao_atual]

    def _definir_cor_para_indice(self, indice):
        """Define a cor de fundo para a estação com base no índice."""
        if indice == 0: # Primavera
            return (137, 183, 137) 
        elif indice == 1: # Verão (após Primavera + Chefe)
            return (81, 170, 72)  
        elif indice == 2: # Outono
            return (204, 153, 102) 
        elif indice == 3: # Inverno
            return (200, 220, 255) 
        return (128, 128, 128) # Fallback

    def atualizar_ciclo_estacoes(self):
        """
        Verifica se é hora de trocar de estação ou iniciar luta de chefe.
        Retorna:
            - "PENDENTE_CHEFE_PRIMAVERA" se o chefe da primavera deve aparecer.
            - True se a estação mudou normalmente.
            - False se nada mudou.
        """
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_tempo_troca_timestamp > self.tempo_troca_estacao_seg:
            # Condição para chefe da Primavera
            if self.nome_estacao_atual() == "Primavera" and \
               not self.chefe_primavera_pendente and \
               not self.chefe_primavera_derrotado_nesta_rodada_ciclica:
                
                self.chefe_primavera_pendente = True
                # Não reseta ultimo_tempo_troca_timestamp aqui, pois a estação "Primavera" continua
                # até o chefe ser derrotado. O timer para a próxima estação (Verão)
                # será resetado em confirmar_derrota_chefe_primavera_e_avancar.
                print(f"DEBUG(Estacoes): Sinalizando PENDENTE_CHEFE_PRIMAVERA. Estação visual: {self.nome_estacao_atual()}")
                return "PENDENTE_CHEFE_PRIMAVERA"
            else:
                # Troca normal de estação (se não for Primavera esperando chefe)
                self._avancar_para_proxima_estacao_ciclica()
                return True 
        return False

    def _avancar_para_proxima_estacao_ciclica(self):
        """Avança para a próxima estação na ordem definida e reseta o timer."""
        estacao_anterior_nome = self.nome_estacao_atual()
        
        self.indice_estacao_atual = (self.indice_estacao_atual + 1) % len(self.nomes_estacoes_ordem)
        
        # Se completou um ciclo e voltou para Primavera, reseta o estado do chefe da primavera
        if self.nome_estacao_atual() == "Primavera" and estacao_anterior_nome == "Inverno":
            self.chefe_primavera_derrotado_nesta_rodada_ciclica = False
            self.chefe_primavera_pendente = False # Garante que não fique pendente ao iniciar nova primavera
            print("DEBUG(Estacoes): Novo ciclo de estações iniciado. Chefe da Primavera resetado.")

        self.cor_atual = self._definir_cor_para_indice(self.indice_estacao_atual)
        self.mensagem_estacao_atual = self.nomes_estacoes_ordem[self.indice_estacao_atual]
        self.tempo_inicio_mensagem_estacao = time.time()
        self.ultimo_tempo_troca_timestamp = time.time() # Reseta o timer para a nova estação
        print(f"DEBUG(Estacoes): Estação mudou para: {self.mensagem_estacao_atual}")

    def confirmar_derrota_chefe_primavera_e_avancar(self):
        """
        Chamado após o chefe da Primavera ser derrotado.
        Avança para Verão e reseta os timers e flags relevantes.
        Retorna True se a transição foi bem-sucedida, False caso contrário.
        """
        if self.nome_estacao_atual() == "Primavera" and self.chefe_primavera_pendente:
            print(f"DEBUG(Estacoes): Chefe da Primavera derrotado. Avançando para Verão.")
            self.chefe_primavera_pendente = False
            self.chefe_primavera_derrotado_nesta_rodada_ciclica = True
            
            # Força a transição para Verão (índice 1 na nossa ordem)
            self.indice_estacao_atual = 1 # 0:Primavera, 1:Verão, 2:Outono, 3:Inverno
            self.cor_atual = self._definir_cor_para_indice(self.indice_estacao_atual)
            self.mensagem_estacao_atual = self.nomes_estacoes_ordem[self.indice_estacao_atual]
            self.tempo_inicio_mensagem_estacao = time.time()
            self.ultimo_tempo_troca_timestamp = time.time() # Inicia a contagem para a duração do Verão
            print(f"DEBUG(Estacoes): Estação definida para: {self.mensagem_estacao_atual} após chefe.")
            return True
        else:
            print(f"AVISO(Estacoes): confirmar_derrota_chefe_primavera_e_avancar chamada em estado inesperado. Estação: {self.nome_estacao_atual()}, Pendente: {self.chefe_primavera_pendente}")
            # Não avança a estação se não estiver no estado correto para evitar lógica inesperada.
            return False


    def desenhar(self, tela):
        """Preenche a tela com a cor da estação atual."""
        tela.fill(self.cor_atual)

    def desenhar_mensagem_estacao(self, janela):
        """Desenha a mensagem da estação atual com efeito de fade out."""
        tempo_passado = time.time() - self.tempo_inicio_mensagem_estacao
        duracao_fade = 2.5 # Segundos para a mensagem desaparecer

        if tempo_passado > duracao_fade:
            return # Mensagem já desapareceu

        alpha = int(255 * (1 - (tempo_passado / duracao_fade)))
        alpha = max(0, min(alpha, 255))  # Garante que alpha esteja entre 0 e 255

        largura_tela, altura_tela = janela.get_size()
        try:
            # Tenta carregar a fonte customizada
            # Certifique-se que FONTE_RETRO_PATH está correto e o arquivo existe
            # Ex: FONTE_RETRO_PATH = os.path.join("Caminho", "Para", "Fontes", "Retro Gaming.ttf")
            # Se o script Estacoes.py está na raiz e Fontes é uma subpasta:
            # FONTE_RETRO_PATH = os.path.join("Fontes", "Retro Gaming.ttf")
            fonte = pygame.font.Font(FONTE_RETRO_PATH, 52) 
        except pygame.error: # Fallback para fonte padrão se a customizada falhar
            print(f"AVISO(Estacoes): Falha ao carregar fonte '{FONTE_RETRO_PATH}'. Usando fonte padrão.")
            fonte = pygame.font.Font(pygame.font.get_default_font(), 40)

        texto_renderizado = fonte.render(self.mensagem_estacao_atual.upper(), True, (255, 255, 255))
        
        largura_texto = texto_renderizado.get_width()
        altura_texto = texto_renderizado.get_height()
        
        # Padding para a caixa de fundo do texto
        padding_caixa_horizontal = 120 # Reduzido para um banner mais justo
        padding_caixa_vertical = 60

        largura_caixa = largura_texto + padding_caixa_horizontal
        altura_caixa = altura_texto + padding_caixa_vertical

        # Posição do retângulo interno (base para o polígono)
        x_retangulo_interno = (largura_tela - largura_caixa) // 2
        y_retangulo_interno = (altura_tela - altura_caixa) // 2 - 50 # Um pouco mais para cima

        # Pontos do polígono para o fundo (forma de banner)
        offset_ponta = 30 # Quão "pontudo" é o banner nas laterais
        pontos = [
            (x_retangulo_interno - offset_ponta, y_retangulo_interno + altura_caixa // 2), # Ponto esquerdo do meio
            (x_retangulo_interno, y_retangulo_interno),                                    # Canto superior esquerdo
            (x_retangulo_interno + largura_caixa, y_retangulo_interno),                    # Canto superior direito
            (x_retangulo_interno + largura_caixa + offset_ponta, y_retangulo_interno + altura_caixa // 2), # Ponto direito do meio
            (x_retangulo_interno + largura_caixa, y_retangulo_interno + altura_caixa),     # Canto inferior direito
            (x_retangulo_interno, y_retangulo_interno + altura_caixa)                      # Canto inferior esquerdo
        ]

        # Calcula dimensões da superfície para o polígono
        min_x_poligono = min(p[0] for p in pontos)
        max_x_poligono = max(p[0] for p in pontos)
        min_y_poligono = min(p[1] for p in pontos)
        max_y_poligono = max(p[1] for p in pontos)
        
        largura_superficie_poligono = max_x_poligono - min_x_poligono
        altura_superficie_poligono = max_y_poligono - min_y_poligono

        if largura_superficie_poligono <=0 or altura_superficie_poligono <=0: return # Evita erro

        # Cria uma superfície para desenhar o polígono com transparência
        superficie_poligono = pygame.Surface((largura_superficie_poligono, altura_superficie_poligono), pygame.SRCALPHA)
        # Desloca os pontos para as coordenadas locais da superfície do polígono
        pontos_deslocados = [(px - min_x_poligono, py - min_y_poligono) for px, py in pontos]

        cor_fundo_poligono = (20, 20, 30, int(alpha * 0.75)) # Fundo escuro semi-transparente
        pygame.draw.polygon(superficie_poligono, cor_fundo_poligono, pontos_deslocados)
        
        cor_borda_poligono = (230, 230, 240, alpha) # Borda clara
        pygame.draw.polygon(superficie_poligono, cor_borda_poligono, pontos_deslocados, 4) # Espessura da borda

        # Desenha a superfície do polígono na janela principal
        janela.blit(superficie_poligono, (min_x_poligono, min_y_poligono))

        # Aplica alpha ao texto e o desenha
        texto_superficie_com_alpha = texto_renderizado.copy()
        texto_superficie_com_alpha.set_alpha(alpha)

        # Centraliza o texto dentro da área do retângulo interno (sem as pontas do banner)
        texto_x = x_retangulo_interno + (largura_caixa - largura_texto) // 2
        texto_y = y_retangulo_interno + (altura_caixa - altura_texto) // 2

        janela.blit(texto_superficie_com_alpha, (texto_x, texto_y))
