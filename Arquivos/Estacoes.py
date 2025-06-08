import pygame
import random
import time
import os

# Certifique-se que este caminho é válido a partir da raiz do projeto
FONTE_RETRO_PATH = "Fontes/Retro Gaming.ttf"

class Estacoes:
    def __init__(self, largura_tela, altura_tela):
        """
        Inicializa o sistema de estações, agora com suporte para sprites de fundo.
        
        Args:
            largura_tela (int): A largura da tela do jogo para dimensionar os fundos.
            altura_tela (int): A altura da tela do jogo.
        """
        pygame.font.init() 
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        
        self.nomes_estacoes_ordem = ["Primavera", "Verão", "Outono", "Inverno"]
        
        # --- NOVO: Dicionário de caminhos para os sprites de fundo ---
        # ATENÇÃO: Verifique se estes caminhos estão corretos e as imagens existem!
        # Os caminhos devem ser relativos à pasta raiz do seu projeto (pasta "Jogo").
        self.caminhos_imagens = {
            "Primavera": "Sprites\\Chao\\Primavera.png",
            "Ver o": "Sprites\\Chao\\Verao.png",
            "Outono": "Sprites\\Chao\\Primavera.png",
            "Inverno": "Sprites\\Chao\\Inverno.png"
        }
        
        self.imagem_fundo_atual = None  # Armazenará a imagem carregada
        self.cor_fallback = (128, 128, 128) # Cor para usar se a imagem falhar
        
        self.indice_estacao_atual = random.randint(0, 3)
        self.tempo_troca_estacao_seg = 120  # 2 minutos
        self.ultimo_tempo_troca_timestamp = time.time()
        
        self.mensagem_estacao_atual = ""
        self.tempo_inicio_mensagem_estacao = 0

        self.chefe_primavera_pendente = False
        self.chefe_primavera_derrotado_nesta_rodada_ciclica = False
        
        self._carregar_recursos_estacao(self.indice_estacao_atual) # Carrega recursos da estação inicial
        print(f"DEBUG(Estacoes): Iniciando na estação: {self.nome_estacao_atual()}")

    def nome_estacao_atual(self):
        return self.nomes_estacoes_ordem[self.indice_estacao_atual]

    def _carregar_recursos_estacao(self, indice):
        """Carrega o sprite de fundo e define a cor de fallback para a estação atual."""
        nome_estacao = self.nomes_estacoes_ordem[indice]
        caminho_imagem = self.caminhos_imagens.get(nome_estacao)
        
        # Define as cores de fallback para cada estação
        cores_fallback = {
            "Primavera": (137, 183, 137),
            "Verão": (81, 170, 72),
            "Outono": (204, 153, 102),
            "Inverno": (200, 220, 255)
        }
        self.cor_fallback = cores_fallback.get(nome_estacao, (128, 128, 128))

        try:
            if caminho_imagem and os.path.exists(caminho_imagem):
                imagem = pygame.image.load(caminho_imagem).convert()
                self.imagem_fundo_atual = pygame.transform.scale(imagem, (self.largura_tela, self.altura_tela))
                print(f"DEBUG(Estacoes): Sprite para '{nome_estacao}' carregado de '{caminho_imagem}'.")
            else:
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho_imagem}")
        except (pygame.error, FileNotFoundError) as e:
            print(f"AVISO(Estacoes): Falha ao carregar sprite para '{nome_estacao}' ({e}). Usando cor de fallback.")
            self.imagem_fundo_atual = None # Garante que usará a cor

        # Atualiza a mensagem da nova estação
        self.mensagem_estacao_atual = nome_estacao
        self.tempo_inicio_mensagem_estacao = time.time()

    def atualizar_ciclo_estacoes(self):
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_tempo_troca_timestamp > self.tempo_troca_estacao_seg:
            if self.nome_estacao_atual() == "Primavera" and \
               not self.chefe_primavera_pendente and \
               not self.chefe_primavera_derrotado_nesta_rodada_ciclica:
                
                self.chefe_primavera_pendente = True
                print(f"DEBUG(Estacoes): Sinalizando PENDENTE_CHEFE_PRIMAVERA.")
                return "PENDENTE_CHEFE_PRIMAVERA"
            else:
                self._avancar_para_proxima_estacao_ciclica()
                return True 
        return False

    def _avancar_para_proxima_estacao_ciclica(self):
        estacao_anterior_nome = self.nome_estacao_atual()
        
        self.indice_estacao_atual = (self.indice_estacao_atual + 1) % len(self.nomes_estacoes_ordem)
        
        if self.nome_estacao_atual() == "Primavera" and estacao_anterior_nome == "Inverno":
            self.chefe_primavera_derrotado_nesta_rodada_ciclica = False
            self.chefe_primavera_pendente = False
            print("DEBUG(Estacoes): Novo ciclo de estações iniciado.")

        self._carregar_recursos_estacao(self.indice_estacao_atual) # Carrega a imagem e cor da nova estação
        self.ultimo_tempo_troca_timestamp = time.time()
        print(f"DEBUG(Estacoes): Estação mudou para: {self.nome_estacao_atual()}")

    def confirmar_derrota_chefe_primavera_e_avancar(self):
        if self.nome_estacao_atual() == "Primavera" and self.chefe_primavera_pendente:
            print("DEBUG(Estacoes): Chefe da Primavera derrotado. Avançando para Verão.")
            self.chefe_primavera_pendente = False
            self.chefe_primavera_derrotado_nesta_rodada_ciclica = True
            
            self.indice_estacao_atual = 1 # Força a ida para o Verão
            self._carregar_recursos_estacao(self.indice_estacao_atual)
            self.ultimo_tempo_troca_timestamp = time.time()
            return True
        return False

    def desenhar(self, tela):
        """Desenha o fundo da estação atual (sprite ou cor de fallback)."""
        if self.imagem_fundo_atual:
            tela.blit(self.imagem_fundo_atual, (0, 0))
        else:
            tela.fill(self.cor_fallback)

    def desenhar_mensagem_estacao(self, janela):
        tempo_passado = time.time() - self.tempo_inicio_mensagem_estacao
        duracao_fade = 2.5

        if tempo_passado > duracao_fade:
            return

        alpha = int(255 * (1 - (tempo_passado / duracao_fade)))
        alpha = max(0, min(alpha, 255))

        largura_tela, altura_tela = janela.get_size()
        try:
            fonte = pygame.font.Font(FONTE_RETRO_PATH, 52) 
        except pygame.error:
            fonte = pygame.font.Font(pygame.font.get_default_font(), 40)

        texto_renderizado = fonte.render(self.mensagem_estacao_atual.upper(), True, (255, 255, 255))
        
        largura_texto = texto_renderizado.get_width()
        altura_texto = texto_renderizado.get_height()
        
        padding_caixa_horizontal = 120
        padding_caixa_vertical = 60

        largura_caixa = largura_texto + padding_caixa_horizontal
        altura_caixa = altura_texto + padding_caixa_vertical

        x_retangulo_interno = (largura_tela - largura_caixa) // 2
        y_retangulo_interno = (altura_tela - altura_caixa) // 2 - 50

        offset_ponta = 30
        pontos = [
            (x_retangulo_interno - offset_ponta, y_retangulo_interno + altura_caixa // 2),
            (x_retangulo_interno, y_retangulo_interno),
            (x_retangulo_interno + largura_caixa, y_retangulo_interno),
            (x_retangulo_interno + largura_caixa + offset_ponta, y_retangulo_interno + altura_caixa // 2),
            (x_retangulo_interno + largura_caixa, y_retangulo_interno + altura_caixa),
            (x_retangulo_interno, y_retangulo_interno + altura_caixa)
        ]

        min_x_poligono = min(p[0] for p in pontos)
        max_x_poligono = max(p[0] for p in pontos)
        min_y_poligono = min(p[1] for p in pontos)
        max_y_poligono = max(p[1] for p in pontos)
        
        largura_superficie_poligono = max_x_poligono - min_x_poligono
        altura_superficie_poligono = max_y_poligono - min_y_poligono

        if largura_superficie_poligono <=0 or altura_superficie_poligono <=0: return

        superficie_poligono = pygame.Surface((largura_superficie_poligono, altura_superficie_poligono), pygame.SRCALPHA)
        pontos_deslocados = [(px - min_x_poligono, py - min_y_poligono) for px, py in pontos]

        cor_fundo_poligono = (20, 20, 30, int(alpha * 0.75))
        pygame.draw.polygon(superficie_poligono, cor_fundo_poligono, pontos_deslocados)
        
        cor_borda_poligono = (230, 230, 240, alpha)
        pygame.draw.polygon(superficie_poligono, cor_borda_poligono, pontos_deslocados, 4)

        janela.blit(superficie_poligono, (min_x_poligono, min_y_poligono))

        texto_superficie_com_alpha = texto_renderizado.copy()
        texto_superficie_com_alpha.set_alpha(alpha)

        texto_x = x_retangulo_interno + (largura_caixa - largura_texto) // 2
        texto_y = y_retangulo_interno + (altura_caixa - altura_texto) // 2

        janela.blit(texto_superficie_com_alpha, (texto_x, texto_y))
