# C:\Users\aysla\Documents\Jogo_Asrahel\Jogo\Arquivos\xp_manager.py

import pygame

class XPManager:
    """
    Gerencia o sistema de experiência (XP) e nivelamento do jogador,
    desenha a barra de XP na tela e lida com evoluções de armas em certos níveis.
    """
    def __init__(self, player_ref, largura_tela, altura_tela):
        self.player_ref = player_ref # Referência ao objeto Player
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 1000 # XP inicial necessário para o Nível 2
        self.base_xp_needed = 1000 # XP base para o próximo nível
        self.xp_scale_factor = 1.5 # Fator de aumento de XP por nível (ex: 100 -> 150 -> 225)

        # Fontes para o desenho da XP e Avisos
        try:
            pygame.font.init() # Garante que o módulo de fontes está inicializado
            self.font_level = pygame.font.Font(None, 28) 
            self.font_xp_value = pygame.font.Font(None, 22)
            self.font_aviso = pygame.font.Font(None, 36) # Fonte para avisos
        except pygame.error as e:
            print(f"DEBUG(XPManager): Erro ao carregar fontes: {e}. Usando fallbacks.")
            self.font_level = pygame.font.SysFont("arial", 28)
            self.font_xp_value = pygame.font.SysFont("arial", 22)
            self.font_aviso = pygame.font.SysFont("arial", 36)


        # Atributos para o efeito visual de ganho de XP (flash)
        self.flash_start_time = 0 
        self.flash_duration = 200 # ms 
        self.flash_color = (100, 255, 100) 

        # --- Sistema de Avisos na Tela ---
        self.avisos_na_tela = [] # Lista de tuplas: (texto_surface, rect, tempo_expiracao_ms)
        self.duracao_aviso_ms = 3000 # 3 segundos
        self.cor_aviso_texto = (255, 223, 0) # Dourado

        # --- Mapas de Evolução de Armas ---
        # Estes mapas serão preenchidos pelo Game.py após a inicialização.
        # Chave: nome da arma atual (string), Valor: Classe da arma evoluída (type)
        self.evolucoes_para_nivel_2 = {}
        self.evolucoes_para_nivel_3 = {}
        # Exemplo de como preencher em Game.py:
        # if AdagaFogo and AdagaFogoNv2: # Verifica se as classes existem
        #     xp_manager.evolucoes_para_nivel_2[AdagaFogo().name] = AdagaFogoNv2


    def _adicionar_aviso_tela(self, texto):
        """Adiciona uma mensagem de aviso para ser exibida na tela."""
        if not texto: return
        try:
            texto_surface = self.font_aviso.render(texto, True, self.cor_aviso_texto)
            # Posiciona o aviso no centro superior da tela
            aviso_rect = texto_surface.get_rect(center=(self.largura_tela // 2, self.altura_tela // 5))
            tempo_expiracao = pygame.time.get_ticks() + self.duracao_aviso_ms
            self.avisos_na_tela.append({"surface": texto_surface, "rect": aviso_rect, "expiry": tempo_expiracao})
            print(f"DEBUG(XPManager): Aviso adicionado: {texto}")
        except Exception as e:
            print(f"DEBUG(XPManager): Erro ao criar aviso na tela: {e}")

    def gain_xp(self, amount):
        """Adiciona XP ao jogador e verifica se ele subiu de nível."""
        if amount <= 0: return # Não processa XP negativo ou zero
        
        self.xp += amount
        print(f"DEBUG(XPManager): Ganhou {amount} XP. Total: {self.xp}/{self.xp_to_next_level}")
        self.flash_start_time = pygame.time.get_ticks() # Ativa o flash ao ganhar XP

        while self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        """Aumenta o nível do jogador, ajusta estatísticas e tenta evoluir a arma."""
        self.level += 1
        xp_excedente = self.xp - self.xp_to_next_level
        self.xp = xp_excedente if xp_excedente > 0 else 0 # Mantém o XP excedente ou zera
        
        self.xp_to_next_level = int(self.base_xp_needed * (self.xp_scale_factor ** (self.level - 1)))
        
        print(f"DEBUG(XPManager): Jogador subiu para o Nível {self.level}!")
        self._adicionar_aviso_tela(f"Nível Acima! Você alcançou o Nível {self.level}!")

        # Aplica os bônus de nível ao jogador referenciado
        if self.player_ref:
            # Bônus de Vida
            if hasattr(self.player_ref, 'vida') and self.player_ref.vida and hasattr(self.player_ref.vida, 'vida_maxima'):
                self.player_ref.vida.vida_maxima += 10 
                if hasattr(self.player_ref.vida, 'curar'):
                    self.player_ref.vida.curar(self.player_ref.vida.vida_maxima) # Cura totalmente
                else: # Fallback se 'curar' não existir
                    self.player_ref.vida.vida_atual = self.player_ref.vida.vida_maxima
                print(f"DEBUG(XPManager): Vida Máxima aumentada para {self.player_ref.vida.vida_maxima}.")
            
            # Bônus de Velocidade
            if hasattr(self.player_ref, 'velocidade'):
                self.player_ref.velocidade += 0.5 
                print(f"DEBUG(XPManager): Velocidade aumentada para {self.player_ref.velocidade}.")

            # --- LÓGICA DE EVOLUÇÃO DE ARMA ---
            arma_evoluida_nome = None
            mapa_evolucoes_usar = None

            if self.level == 2:
                mapa_evolucoes_usar = self.evolucoes_para_nivel_2
            elif self.level == 3:
                mapa_evolucoes_usar = self.evolucoes_para_nivel_3
            
            if mapa_evolucoes_usar is not None and hasattr(self.player_ref, 'evoluir_arma_atual'):
                if self.player_ref.current_weapon: # Verifica se há uma arma equipada
                    arma_evoluida_nome = self.player_ref.evoluir_arma_atual(mapa_evolucoes_usar)
                    if arma_evoluida_nome:
                        self._adicionar_aviso_tela(f"Sua arma evoluiu para: {arma_evoluida_nome}!")
                        print(f"DEBUG(XPManager): Arma evoluiu para {arma_evoluida_nome}.")
                    # else:
                        # print(f"DEBUG(XPManager): Arma atual não tinha evolução definida para o Nível {self.level}.")
                # else:
                    # print(f"DEBUG(XPManager): Jogador sem arma equipada para evoluir no Nível {self.level}.")
            # elif mapa_evolucoes_usar is not None:
                # print(f"DEBUG(XPManager): Player ref não tem método 'evoluir_arma_atual' para o Nível {self.level}.")
            # --- FIM LÓGICA DE EVOLUÇÃO ---
        else:
            print("DEBUG(XPManager): player_ref não definido. Bônus de nível não aplicados.")

        vida_max_str = 'N/A'
        if self.player_ref and hasattr(self.player_ref, 'vida') and self.player_ref.vida:
            vida_max_str = str(self.player_ref.vida.vida_maxima)
        print(f"DEBUG(XPManager): Próximo nível ({self.level + 1}) em {self.xp_to_next_level} XP. Vida Máxima atual: {vida_max_str}.")


    def draw(self, janela):
        """
        Desenha a barra de XP, o nível e os avisos na tela.
        """
        # --- Desenho da Barra de XP ---
        xp_bar_width = 200 
        xp_bar_height = 20 
        padding = 10 

        xp_bar_x = (self.largura_tela // 2) - (xp_bar_width // 2)
        xp_bar_y = self.altura_tela - xp_bar_height - padding

        pygame.draw.rect(janela, (50, 50, 50), (xp_bar_x, xp_bar_y, xp_bar_width, xp_bar_height), border_radius=5)

        xp_percentage = self.xp / self.xp_to_next_level if self.xp_to_next_level > 0 else 0
        current_xp_width = int(xp_bar_width * xp_percentage)
        
        current_time_ticks = pygame.time.get_ticks()
        fill_color = self.flash_color if current_time_ticks - self.flash_start_time < self.flash_duration else (0, 200, 255)
        pygame.draw.rect(janela, fill_color, (xp_bar_x, xp_bar_y, current_xp_width, xp_bar_height), border_radius=5)
        pygame.draw.rect(janela, (255, 255, 255), (xp_bar_x, xp_bar_y, xp_bar_width, xp_bar_height), 2, border_radius=5)

        level_text_surface = self.font_level.render(f"Nível: {self.level}", True, (255, 255, 255))
        level_text_rect = level_text_surface.get_rect(midbottom=(self.largura_tela // 2, xp_bar_y - 5)) 
        janela.blit(level_text_surface, level_text_rect)

        xp_value_text_surface = self.font_xp_value.render(f"{self.xp}/{self.xp_to_next_level} XP", True, (255, 255, 255))
        xp_value_text_rect = xp_value_text_surface.get_rect(midtop=(self.largura_tela // 2, xp_bar_y + xp_bar_height + 5)) 
        janela.blit(xp_value_text_surface, xp_value_text_rect)

        # --- Desenho dos Avisos na Tela ---
        # Itera sobre uma cópia da lista para permitir remoção segura durante a iteração
        for i in range(len(self.avisos_na_tela) -1, -1, -1): # Itera de trás para frente
            aviso = self.avisos_na_tela[i]
            if current_time_ticks < aviso["expiry"]:
                # Adiciona um fundo semi-transparente para o aviso
                bg_rect = aviso["rect"].inflate(20, 10) # Aumenta um pouco o fundo
                s = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
                s.fill((0,0,0,180)) # Preto com alpha 180
                janela.blit(s, bg_rect.topleft)
                janela.blit(aviso["surface"], aviso["rect"])
            else:
                self.avisos_na_tela.pop(i) # Remove aviso expirado
