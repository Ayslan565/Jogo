import pygame
import os

# Caminho para a fonte personalizada, deve estar na pasta 'Fontes' na raiz do projeto
# O caminho é construído de forma a ser relativo à localização do script 'Game.py'
FONTE_RETRO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Fontes", "Retro Gaming.ttf")

class XPManager:
    """
    Gerencia a experiência (XP) e o nível do jogador, e desenha a UI correspondente.
    """
    def __init__(self, player_ref, largura_tela, altura_tela):
        """
        Inicializa o gerenciador de XP.
        
        Args:
            player_ref (Player): A referência para o objeto do jogador.
            largura_tela (int): A largura da tela do jogo.
            altura_tela (int): A altura da tela do jogo.
        """
        self.player = player_ref
        
        # Configurações da barra de XP
        self.largura_barra = 250 # Aumentei um pouco a largura para melhor visualização no centro
        self.altura_barra = 20
        self.cor_fundo_barra = (50, 50, 50, 200) # Fundo semi-transparente
        self.cor_xp = (0, 255, 0)
        self.cor_borda = (200, 200, 200) # Cor para a borda
        
        # Tenta carregar a fonte personalizada; se falhar, usa a fonte padrão do Pygame.
        try:
            # Garante que o caminho da fonte seja válido antes de tentar carregar
            if not os.path.exists(FONTE_RETRO_PATH):
                raise pygame.error(f"Arquivo de fonte não encontrado em: {FONTE_RETRO_PATH}")
            self.fonte = pygame.font.Font(FONTE_RETRO_PATH, 22)
            self.fonte_score = pygame.font.Font(FONTE_RETRO_PATH, 28)
        except pygame.error as e:
            print(f"AVISO (XPManager): {e}. Usando fonte padrão do sistema.")
            # Fallback para a fonte padrão se o arquivo não for encontrado
            self.fonte = pygame.font.Font(None, 24)
            self.fonte_score = pygame.font.Font(None, 28)
            
        self.cor_texto = (255, 255, 255)

        # Carregar imagem de fundo para o score
        self.fundo_score_img = None
        self.fundo_score_rect = None
        try:
            # Constrói o caminho para a imagem de fundo do score
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            caminho_imagem = os.path.join(base_dir, 'Sprites', 'Score', 'Score.png')
            
            self.fundo_score_img = pygame.image.load(caminho_imagem).convert_alpha()
            # Redimensiona a imagem para um tamanho adequado
            self.fundo_score_img = pygame.transform.scale(self.fundo_score_img, (250, 70))
            self.fundo_score_rect = self.fundo_score_img.get_rect()
        except pygame.error as e:
            print(f"AVISO (XPManager): Erro ao carregar a imagem de fundo do score: {e}")
            self.fundo_score_img = None
            self.fundo_score_rect = None

    def gain_xp(self, amount):
        """Adiciona uma quantidade de XP ao jogador e atualiza o score total."""
        if not self.player: return
        
        # Acessa os atributos de experiência diretamente no objeto do jogador
        self.player.experiencia += amount
        self.player.total_pontos_experiencia_acumulados += amount
        
        self.check_level_up()

    def check_level_up(self):
        """Verifica se o jogador tem XP suficiente para subir de nível e atualiza seu estado."""
        while self.player.experiencia >= self.player.experiencia_para_proximo_nivel:
            xp_excedente = self.player.experiencia - self.player.experiencia_para_proximo_nivel
            self.player.nivel += 1
            self.player.experiencia = xp_excedente
            
            # Aumenta a quantidade de XP necessária para o próximo nível (ex: 50% a mais)
            self.player.experiencia_para_proximo_nivel = int(self.player.experiencia_para_proximo_nivel * 1.5)
            
            print(f"DEBUG(XPManager): Jogador subiu para o Nível {self.player.nivel}!")

    def draw(self, screen):
        """Desenha todos os elementos da UI de XP na tela."""
        if not self.player: return
            
        largura_tela = screen.get_width()
        altura_tela = screen.get_height()
        
        # Garante que os valores de XP sejam inteiros para exibição
        xp_atual = int(self.player.experiencia)
        xp_necessario = int(self.player.experiencia_para_proximo_nivel)
        nivel_atual = self.player.nivel
        score_total = self.player.total_pontos_experiencia_acumulados

        # --- ALTERAÇÃO: Posição da Barra e Nível movidos para o centro inferior ---
        pos_x_barra = (largura_tela - self.largura_barra) // 2
        pos_y_barra = altura_tela - self.altura_barra - 20 # 20 pixels de margem do fundo

        # --- Desenha a Barra de XP com Bordas Arredondadas ---
        fundo_barra_rect = pygame.Rect(pos_x_barra, pos_y_barra, self.largura_barra, self.altura_barra)
        
        fundo_surf = pygame.Surface(fundo_barra_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(fundo_surf, self.cor_fundo_barra, fundo_surf.get_rect(), border_radius=8)
        screen.blit(fundo_surf, fundo_barra_rect.topleft)

        xp_ratio = min(xp_atual / xp_necessario, 1) if xp_necessario > 0 else 0
        largura_xp_atual = self.largura_barra * xp_ratio
        
        if largura_xp_atual > 0:
            clip_area = pygame.Rect(pos_x_barra, pos_y_barra, largura_xp_atual, self.altura_barra)
            screen.set_clip(clip_area)
            pygame.draw.rect(screen, self.cor_xp, fundo_barra_rect, border_radius=8)
            screen.set_clip(None)

        pygame.draw.rect(screen, self.cor_borda, fundo_barra_rect, width=2, border_radius=8)
        
        # --- Desenha o Nível com fundo arredondado, acima da barra de XP ---
        texto_nivel_render = self.fonte.render(f"Nivel: {nivel_atual}", True, self.cor_texto)
        
        level_bg_rect = pygame.Rect(0, 0, texto_nivel_render.get_width() + 15, texto_nivel_render.get_height() + 10)
        level_bg_rect.centerx = fundo_barra_rect.centerx  # Centraliza com a barra de XP
        level_bg_rect.bottom = fundo_barra_rect.top - 5  # Posiciona 5 pixels acima da barra
        
        level_bg_surface = pygame.Surface(level_bg_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(level_bg_surface, self.cor_fundo_barra, level_bg_surface.get_rect(), border_radius=8)
        pygame.draw.rect(level_bg_surface, self.cor_borda, level_bg_surface.get_rect(), width=2, border_radius=8)
        
        pos_texto_nivel = texto_nivel_render.get_rect(center=level_bg_surface.get_rect().center)
        level_bg_surface.blit(texto_nivel_render, pos_texto_nivel)
        
        screen.blit(level_bg_surface, level_bg_rect.topleft)

        # --- Desenha o Score Total (permanece no canto superior direito) ---
        if self.fundo_score_img and self.fundo_score_rect:
            self.fundo_score_rect.topright = (largura_tela - 15, 15)
            screen.blit(self.fundo_score_img, self.fundo_score_rect)
            center_pos = self.fundo_score_rect.center
        else:
            center_pos = (largura_tela - 140, 50)
        
        texto_score = f"Score: {score_total}"
        surface_score = self.fonte_score.render(texto_score, True, (255, 255, 255))
        
        pos_texto_score_rect = surface_score.get_rect(center=center_pos)
        screen.blit(surface_score, pos_texto_score_rect)
