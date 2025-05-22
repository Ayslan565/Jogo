# C:\Users\aysla\Documents\Jogo_Asrahel\Jogo\Arquivos\xp_manager.py

import pygame

class XPManager:
    """
    Gerencia o sistema de experiência (XP) e nivelamento do jogador,
    e desenha a barra de XP na tela.
    """
    def __init__(self, player_ref, largura_tela, altura_tela):
        self.player_ref = player_ref # Referência ao objeto Player
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100 # XP inicial necessário para o Nível 2
        self.base_xp_needed = 100 # XP base para o próximo nível
        self.xp_scale_factor = 1.5 # Fator de aumento de XP por nível (ex: 100 -> 150 -> 225)

        # Fontes para o desenho da XP
        self.font_level = pygame.font.Font(None, 28) # Fonte para o nível
        self.font_xp_value = pygame.font.Font(None, 22) # Fonte para o valor de XP

        # Atributos para o efeito visual de ganho de XP (flash)
        self.flash_start_time = 0 # Tempo em que o flash começou
        self.flash_duration = 200 # Duração do flash em milissegundos (0.2 segundos)
        self.flash_color = (100, 255, 100) # Cor do flash (verde claro)


    def gain_xp(self, amount):
        """Adiciona XP ao jogador e verifica se ele subiu de nível."""
        self.xp += amount
        print(f"DEBUG(XPManager): Ganhou {amount} XP. Total: {self.xp}/{self.xp_to_next_level}")
        self.flash_start_time = pygame.time.get_ticks() # Ativa o flash ao ganhar XP

        while self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        """Aumenta o nível do jogador e ajusta as estatísticas."""
        self.level += 1
        self.xp -= self.xp_to_next_level # Subtrai o XP necessário para o nível atual
        self.xp_to_next_level = int(self.base_xp_needed * (self.xp_scale_factor ** (self.level - 1)))
        
        # Aplica os bônus de nível ao jogador referenciado
        if self.player_ref:
            if hasattr(self.player_ref, 'vida') and self.player_ref.vida:
                self.player_ref.vida.vida_maxima += 10 # Exemplo: +10 vida máxima por nível
                self.player_ref.vida.curar(self.player_ref.vida.vida_maxima) # Cura totalmente ao subir de nível
            
            if hasattr(self.player_ref, 'velocidade'):
                self.player_ref.velocidade += 0.5 # Aumenta a velocidade base do jogador (exemplo)

        print(f"DEBUG(XPManager): Jogador subiu para o Nível {self.level}!")
        print(f"DEBUG(XPManager): Próximo nível em {self.xp_to_next_level} XP. Vida Máxima: {self.player_ref.vida.vida_maxima if self.player_ref and hasattr(self.player_ref, 'vida') else 'N/A'}.")

    def draw(self, janela):
        """
        Desenha a barra de XP e o nível na parte inferior central da tela.
        """
        xp_bar_width = 200 # Largura da barra de XP
        xp_bar_height = 20 # Altura da barra de XP
        padding = 10 # Espaçamento da borda inferior

        # Posição central inferior
        xp_bar_x = (self.largura_tela // 2) - (xp_bar_width // 2)
        xp_bar_y = self.altura_tela - xp_bar_height - padding

        # Fundo da barra de XP
        pygame.draw.rect(janela, (50, 50, 50), (xp_bar_x, xp_bar_y, xp_bar_width, xp_bar_height), border_radius=5)

        # Preenchimento da barra de XP
        xp_percentage = self.xp / self.xp_to_next_level if self.xp_to_next_level > 0 else 0
        current_xp_width = int(xp_bar_width * xp_percentage)
        
        # Define a cor de preenchimento: flash ou normal
        current_time = pygame.time.get_ticks()
        if current_time - self.flash_start_time < self.flash_duration:
            fill_color = self.flash_color # Cor do flash
        else:
            fill_color = (0, 200, 255) # Azul claro normal

        pygame.draw.rect(janela, fill_color, (xp_bar_x, xp_bar_y, current_xp_width, xp_bar_height), border_radius=5)

        # Borda da barra de XP
        pygame.draw.rect(janela, (255, 255, 255), (xp_bar_x, xp_bar_y, xp_bar_width, xp_bar_height), 2, border_radius=5)

        # Texto do Nível
        level_text_surface = self.font_level.render(f"Nível: {self.level}", True, (255, 255, 255))
        level_text_rect = level_text_surface.get_rect(midbottom=(self.largura_tela // 2, xp_bar_y - 5)) # Acima da barra
        janela.blit(level_text_surface, level_text_rect)

        # Texto do XP (opcional, para mais detalhes)
        xp_value_text_surface = self.font_xp_value.render(f"{self.xp}/{self.xp_to_next_level} XP", True, (255, 255, 255))
        xp_value_text_rect = xp_value_text_surface.get_rect(midtop=(self.largura_tela // 2, xp_bar_y + xp_bar_height + 5)) # Abaixo da barra
        janela.blit(xp_value_text_surface, xp_value_text_rect)

