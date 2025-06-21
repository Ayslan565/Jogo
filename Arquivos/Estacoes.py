import pygame
import random
import time
import os

# Certifique-se que este caminho é válido a partir da raiz do projeto
FONTE_RETRO_PATH = "Fontes/Retro Gaming.ttf"

class Estacoes:
    def __init__(self, largura_tela, altura_tela):
        """
        Inicializa o sistema de estações, agora com suporte para fundo dinâmico (tiling).
        
        Args:
            largura_tela (int): A largura da tela do jogo.
            altura_tela (int): A altura da tela do jogo.
        """
        pygame.font.init() 
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        
        self.nomes_estacoes_ordem = ["Primavera", "Verão", "Outono", "Inverno"]
        
        self.caminhos_imagens = {
            "Primavera": "Sprites\\Chao\\Primavera.png",
            "Verão": "Sprites\\Chao\\Verao.png",
            "Outono": "Sprites\\Chao\\Outono.png",
            "Inverno": "Sprites\\Chao\\Inverno.png"
        }
        
        self.imagem_fundo_tile = None 
        self.cor_fallback = (128, 128, 128)
        
        self.indice_estacao_atual = random.randint(0, 3)
        self.tempo_troca_estacao_seg = 300 # Tempo de duração de cada estação em segundos
        self.ultimo_tempo_troca_timestamp = time.time()
        
        self.mensagem_estacao_atual = ""
        self.tempo_inicio_mensagem_estacao = 0

        # ADICIONADO: Flag genérica para controlar o estado de "chefe pendente"
        self.chefe_pendente = False
        
        self._carregar_recursos_estacao(self.indice_estacao_atual)
        print(f"DEBUG(Estacoes): Iniciando na estação: {self.nome_estacao_atual()}")

    def nome_estacao_atual(self):
        return self.nomes_estacoes_ordem[self.indice_estacao_atual]

    def _carregar_recursos_estacao(self, indice):
        """Carrega e redimensiona o sprite de fundo (tile) para a estação atual."""
        nome_estacao = self.nomes_estacoes_ordem[indice]
        caminho_imagem = self.caminhos_imagens.get(nome_estacao)
        
        cores_fallback = {
            "Primavera": (137, 183, 137), "Verão": (81, 170, 72),
            "Outono": (204, 153, 102), "Inverno": (200, 220, 255)
        }
        self.cor_fallback = cores_fallback.get(nome_estacao, (128, 128, 128))

        try:
            if caminho_imagem and os.path.exists(caminho_imagem):
                imagem_original = pygame.image.load(caminho_imagem).convert()
                
                fator_escala_tile = 0.4
                
                largura_original, altura_original = imagem_original.get_size()
                nova_largura = int(largura_original * fator_escala_tile)
                nova_altura = int(altura_original * fator_escala_tile)
                
                if nova_largura > 0 and nova_altura > 0:
                    self.imagem_fundo_tile = pygame.transform.scale(imagem_original, (nova_largura, nova_altura))
                else:
                    self.imagem_fundo_tile = imagem_original
            else:
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho_imagem}")
        except (pygame.error, FileNotFoundError) as e:
            print(f"AVISO(Estacoes): Falha ao carregar sprite para '{nome_estacao}' ({e}). Usando cor de fallback.")
            self.imagem_fundo_tile = None

        self.mensagem_estacao_atual = nome_estacao
        self.tempo_inicio_mensagem_estacao = time.time()

    # MÉTODO MODIFICADO: Torna a verificação genérica para qualquer estação
    def atualizar_ciclo_estacoes(self):
        """
        Verifica se o tempo da estação acabou. Se sim, sinaliza que uma luta
        contra o chefe deve começar.
        Retorna um sinal para o loop principal do jogo.
        """
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_tempo_troca_timestamp > self.tempo_troca_estacao_seg:
            # Se o tempo da estação acabou e um chefe ainda não está pendente para esta estação
            if not self.chefe_pendente:
                self.chefe_pendente = True
                print(f"DEBUG(Estacoes): Fim da estação '{self.nome_estacao_atual()}'. Sinalizando para iniciar luta contra chefe.")
                return "INICIAR_LUTA_CHEFE" # Sinal genérico para o Game.py
        return False # Retorna False se não for hora de fazer nada

    # NOVO MÉTODO: Generalizado para avançar a estação após qualquer chefe
    def avancar_estacao_apos_chefe(self):
        """
        Avança para a próxima estação após a derrota de um chefe.
        Este método deve ser chamado pelo loop principal do jogo (Game.py) ou pelo
        módulo de luta (Luta_boss.py) quando a luta for concluída com sucesso.
        """
        if self.chefe_pendente:
            print(f"DEBUG(Estacoes): Chefe da estação '{self.nome_estacao_atual()}' derrotado. Avançando para a próxima estação.")
            self.chefe_pendente = False
            
            # Avança o índice da estação para a próxima de forma cíclica
            self.indice_estacao_atual = (self.indice_estacao_atual + 1) % len(self.nomes_estacoes_ordem)
            
            # Carrega os recursos da nova estação e reseta o timer
            self._carregar_recursos_estacao(self.indice_estacao_atual)
            self.ultimo_tempo_troca_timestamp = time.time()
            return True
        return False

    def desenhar(self, tela, camera_x, camera_y):
        """Desenha o fundo da estação com efeito parallax distante."""
        if self.imagem_fundo_tile:
            tile_w, tile_h = self.imagem_fundo_tile.get_size()
            if tile_w == 0 or tile_h == 0:
                tela.fill(self.cor_fallback)
                return
            
            parallax_factor = 1.0
            
            scroll_x = int(camera_x * parallax_factor)
            scroll_y = int(camera_y * parallax_factor)
            
            start_x = -(scroll_x % tile_w)
            start_y = -(scroll_y % tile_h)
            
            for y in range(start_y, self.altura_tela, tile_h):
                for x in range(start_x, self.largura_tela, tile_w):
                    tela.blit(self.imagem_fundo_tile, (x, y))
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
        largura_texto, altura_texto = texto_renderizado.get_size()
        
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
        
        superficie_poligono = pygame.Surface(janela.get_size(), pygame.SRCALPHA)
        cor_fundo = (20, 20, 30, int(alpha * 0.75))
        cor_borda = (230, 230, 240, alpha)
        
        pygame.draw.polygon(superficie_poligono, cor_fundo, pontos)
        pygame.draw.polygon(superficie_poligono, cor_borda, pontos, 4)
        janela.blit(superficie_poligono, (0,0))
        
        texto_superficie_com_alpha = texto_renderizado.copy()
        texto_superficie_com_alpha.set_alpha(alpha)
        texto_x = x_retangulo_interno + (largura_caixa - largura_texto) // 2
        texto_y = y_retangulo_interno + (altura_caixa - altura_texto) // 2
        janela.blit(texto_superficie_com_alpha, (texto_x, texto_y))