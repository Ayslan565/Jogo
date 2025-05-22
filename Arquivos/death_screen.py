# death_screen.py
import pygame
import sys
import os # Importa os para ajudar a verificar caminhos

# Definir o caminho padrão para a música da tela de morte
# VOCÊ DEVE ALTERAR ESTE CAMINHO PARA O SEU ARQUIVO DE MÚSICA REAL
DEATH_SCREEN_MUSIC_PATH = "Musica\\Game Over\\OverLord.mp3" # Substitua pelo seu caminho real
FONTE_RETRO_PATH = "Fontes\\Retro Gaming.ttf" # <--- VERIFIQUE ESTE CAMINHO!

def run_death_screen(janela, restart_game_callback, main_menu_callback, background_image_path=None):
    """
    Exibe a tela de morte com uma imagem de fundo e música, e espera pela interação do jogador.
    Recebe funções de callback para reiniciar o jogo ou voltar ao menu principal.
    """
    # Tenta carregar a fonte personalizada, caso contrário, usa a fonte padrão do Pygame
    try:
        if os.path.exists(FONTE_RETRO_PATH):
            fonte = pygame.font.Font(FONTE_RETRO_PATH, 45)
            print(f"DEBUG(death_screen): Fonte personalizada carregada: {FONTE_RETRO_PATH}")
        else:
            fonte = pygame.font.Font(None, 45)
            print(f"DEBUG(death_screen): Aviso: Fonte personalizada não encontrada em '{FONTE_RETRO_PATH}'. Usando fonte padrão.")
    except Exception as e:
        fonte = pygame.font.Font(None, 45)
        print(f"DEBUG(death_screen): Erro ao carregar fonte personalizada: {e}. Usando fonte padrão.")
    
    # Cores
    ORANGE = (255, 165, 0) # Cor laranja
    WHITE = (255, 255, 255) # Cor branca

    # Renderiza as partes dos textos com as cores específicas
    texto_r_surface = fonte.render("R", True, ORANGE)
    texto_restart_complement_surface = fonte.render(" - Reiniciar", True, WHITE)

    texto_esc_surface = fonte.render("ESC", True, ORANGE)
    texto_menu_complement_surface = fonte.render(" - Menu Inicial", True, WHITE)

    background_image_path = "Sprites\\Game Over\\game_over_horizontal.png"
    original_background_image = None  # Armazena a imagem original para manipulação de alpha
    if background_image_path and os.path.exists(background_image_path):
        try:
            original_background_image = pygame.image.load(background_image_path).convert_alpha() # Usar convert_alpha para transparência
            # Escala a imagem para preencher a tela
            original_background_image = pygame.transform.scale(original_background_image, (janela.get_width(), janela.get_height()))
            print(f"DEBUG(death_screen): Imagem de fundo da tela de morte carregada: {background_image_path}")
        except pygame.error as e:
            print(f"DEBUG(death_screen): Erro ao carregar imagem de fundo da tela de morte '{background_image_path}': {e}")
            original_background_image = None
    else:
        print(f"DEBUG(death_screen): Aviso: Caminho da imagem de fundo da tela de morte não encontrado ou não fornecido: {background_image_path}")

    # Para a música do jogo atual (se estiver tocando)
    pygame.mixer.music.stop()
    print("DEBUG(death_screen): Música do jogo parada.")

    # Variáveis para o efeito de fade-in
    alpha = 0 # Começa totalmente transparente
    fade_speed = 1 # Velocidade do fade-in (quanto maior, mais rápido)
    
    # Flag para controlar o início da música
    music_started = False
    music_start_time = pygame.time.get_ticks() # Tempo em que a tela de morte começou
    music_delay_ms = 1000 # 3 segundos de atraso para a música

    clock = pygame.time.Clock() # Para controlar o framerate do loop da tela de morte

    # Loop da tela de morte
    while True:
        for evento in pygame.event.get():
            # Se o evento for fechar a janela, sai do jogo
            if evento.type == pygame.QUIT:
                pygame.mixer.music.stop() # Para a música da tela de morte
                pygame.quit()
                sys.exit()
            # Se a tecla ESC for pressionada, vai para o menu inicial
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop() # Para a música da tela de morte
                main_menu_callback() # Chama a função de callback para o menu principal
                return # Sai da função run_death_screen
            # Se a tecla R for pressionada, reinicia o jogo chamando a função de callback
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                pygame.mixer.music.stop() # Para a música da tela de morte antes de reiniciar
                restart_game_callback()
                return # Sai da função run_death_screen para voltar ao loop principal do jogo (reiniciado)

        # Lógica de fade-in
        if alpha < 255:
            alpha += fade_speed
            if alpha > 255:
                alpha = 255
        
        # Desenha a imagem de fundo com fade-in
        if original_background_image:
            background_image = original_background_image.copy() # Cria uma cópia para não alterar a original
            background_image.set_alpha(alpha) # Define o alpha para a imagem
            janela.blit(background_image, (0, 0))
        else:
            janela.fill((0, 0, 0)) # Fundo preto se não houver imagem

        # Calcula a posição para centralizar o texto no canto inferior central
        screen_width = janela.get_width()
        screen_height = janela.get_height()

        # Calcula a largura total de cada linha de texto
        total_width_restart_line = texto_r_surface.get_width() + texto_restart_complement_surface.get_width()
        total_width_menu_line = texto_esc_surface.get_width() + texto_menu_complement_surface.get_width()

        # Posiciona "ESC - Menu Inicial" mais abaixo
        pos_x_menu_line = screen_width // 2 - total_width_menu_line // 2
        pos_y_menu_line = screen_height - texto_menu_complement_surface.get_height() - 50 # 50 pixels da parte inferior

        # Posiciona "R - Reiniciar" logo acima do texto do menu
        pos_x_restart_line = screen_width // 2 - total_width_restart_line // 2
        pos_y_restart_line = pos_y_menu_line - texto_restart_complement_surface.get_height() - 10 # 10 pixels de espaçamento entre eles

        # Desenha os textos com fade-in
        # Define o alpha para ambas as partes de cada linha
        texto_r_surface.set_alpha(alpha)
        texto_restart_complement_surface.set_alpha(alpha)
        texto_esc_surface.set_alpha(alpha)
        texto_menu_complement_surface.set_alpha(alpha)

        # Blit das partes de "R - Reiniciar"
        janela.blit(texto_r_surface, (pos_x_restart_line, pos_y_restart_line))
        janela.blit(texto_restart_complement_surface, (pos_x_restart_line + texto_r_surface.get_width(), pos_y_restart_line))

        # Blit das partes de "ESC - Menu Inicial"
        janela.blit(texto_esc_surface, (pos_x_menu_line, pos_y_menu_line))
        janela.blit(texto_menu_complement_surface, (pos_x_menu_line + texto_esc_surface.get_width(), pos_y_menu_line))

        # Lógica de atraso para a música
        if not music_started and pygame.time.get_ticks() - music_start_time >= music_delay_ms:
            if os.path.exists(DEATH_SCREEN_MUSIC_PATH):
                try:
                    pygame.mixer.music.load(DEATH_SCREEN_MUSIC_PATH)
                    pygame.mixer.music.play(-1) # Toca a música em loop infinito
                    music_started = True
                    print(f"DEBUG(death_screen): Música da tela de morte carregada e tocando após atraso: {DEATH_SCREEN_MUSIC_PATH}")
                except pygame.error as e:
                    print(f"DEBUG(death_screen): Erro ao carregar ou tocar a música da tela de morte '{DEATH_SCREEN_MUSIC_PATH}': {e}")
            else:
                print(f"DEBUG(death_screen): Aviso: Caminho da música da tela de morte não encontrado para tocar após atraso: {DEATH_SCREEN_MUSIC_PATH}")
            
        # Atualiza a tela para mostrar as mudanças
        pygame.display.update()
        # Limita o framerate
        clock.tick(60)
