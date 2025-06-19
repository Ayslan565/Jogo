import pygame

class XPManager:
    def __init__(self, player_ref, largura_tela, altura_tela, fonte_path=None, tamanho_fonte=24):
        self.player = player_ref
        self.level = 1
        self.xp_atual = 0
        self.xp_para_proximo_nivel = 100
        # Variável para a pontuação total do jogo
        self.total_score = 0
        
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        
        # Posição e dimensões da barra de XP
        self.x = 20
        self.y = self.altura_tela - 40
        self.largura_barra = self.largura_tela - 40
        self.altura_barra = 20
        
        self.mapa_evolucoes = {}
        
        try:
            self.fonte = pygame.font.Font(fonte_path, tamanho_fonte)
            # Fonte para o score
            self.fonte_score = pygame.font.Font(fonte_path, 28)
        except pygame.error:
            self.fonte = pygame.font.SysFont("arial", tamanho_fonte - 2)
            # Fonte de fallback para o score
            self.fonte_score = pygame.font.SysFont("arial", 24)

    def gain_xp(self, amount):
        if not self.player.esta_vivo():
            return
            
        self.xp_atual += amount
        # Cada ponto de XP também aumenta a pontuação total
        self.total_score += amount
        
        while self.xp_atual >= self.xp_para_proximo_nivel:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp_atual -= self.xp_para_proximo_nivel
        self.xp_para_proximo_nivel = int(self.xp_para_proximo_nivel * 1.5)
        
        # Lógica de evolução de arma
        if self.player and self.player.current_weapon:
            mapa_evolucoes_nivel = self.mapa_evolucoes.get(self.level)
            if mapa_evolucoes_nivel:
                nome_nova_arma = self.player.evoluir_arma_atual(mapa_evolucoes_nivel)
                if nome_nova_arma:
                    print(f"Arma evoluiu para {nome_nova_arma} no nível {self.level}!")

    def draw(self, screen):
        # Cor de fundo da barra
        pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.largura_barra, self.altura_barra), border_radius=5)
        
        # Barra de progresso do XP
        progresso_xp = self.xp_atual / self.xp_para_proximo_nivel
        largura_progresso = int(self.largura_barra * progresso_xp)
        pygame.draw.rect(screen, (100, 200, 255), (self.x, self.y, largura_progresso, self.altura_barra), border_radius=5)
        
        # Borda da barra
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.largura_barra, self.altura_barra), 2, border_radius=5)
        
        # Texto (Nível e XP)
        texto_level = f"Nível: {self.level}"
        texto_xp = f"XP: {self.xp_atual} / {self.xp_para_proximo_nivel}"
        
        surface_level = self.fonte.render(texto_level, True, (255, 255, 255))
        surface_xp = self.fonte.render(texto_xp, True, (255, 255, 255))
        
        screen.blit(surface_level, (self.x + 10, self.y))
        screen.blit(surface_xp, (self.x + self.largura_barra - surface_xp.get_width() - 10, self.y))

        # MODIFICADO: Desenha o XP total no canto superior esquerdo
        texto_score = f"XP: {self.total_score}"
        surface_score = self.fonte_score.render(texto_score, True, (255, 215, 0)) # Cor de ouro
        # Posição no canto superior esquerdo, abaixo da barra de vida
        pos_x_score = 20 
        pos_y_score = 60 
        screen.blit(surface_score, (pos_x_score, pos_y_score))
