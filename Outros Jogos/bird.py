import pygame
import random
import sys # Para sair do jogo

# --- Constantes ---
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
PIPE_WIDTH = 80
PIPE_GAP = 150 # Espaço entre o cano de cima e o de baixo
BIRD_X = 50
GRAVITY = 0.25
FLAP_STRENGTH = -6 # Quão forte o pássaro "pula"
PIPE_MOVEMENT_SPEED = -3

# --- Cores (RGB) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255) # Cor do céu (exemplo)
GREEN = (0, 200, 0) # Cor dos canos (exemplo)
YELLOW = (255, 255, 0) # Cor do pássaro (exemplo)

# --- Funções ---

def load_images():
    """Carrega as imagens do jogo (pássaro, cano, fundo)."""
    # Exemplo (você precisará criar ou baixar essas imagens)
    # global bird_image, pipe_image, background_image
    # bird_image = pygame.image.load('assets/bird.png').convert_alpha()
    # pipe_image = pygame.image.load('assets/pipe.png').convert_alpha()
    # background_image = pygame.image.load('assets/background.png').convert()
    pass

def create_pipe():
    """Cria um novo par de canos com altura aleatória."""
    pipe_height = random.randint(150, SCREEN_HEIGHT - PIPE_GAP - 100)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, pipe_height + PIPE_GAP / 2, PIPE_WIDTH, SCREEN_HEIGHT - pipe_height - PIPE_GAP / 2)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, pipe_height - PIPE_GAP / 2)
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    """Move os canos para a esquerda."""
    for pipe_pair in pipes:
        pipe_pair[0].x += PIPE_MOVEMENT_SPEED
        pipe_pair[1].x += PIPE_MOVEMENT_SPEED
    return [pipe for pipe in pipes if pipe[0].right > 0] # Remove canos que saíram da tela

def draw_pipes(screen, pipes):
    """Desenha os canos na tela."""
    for top_pipe, bottom_pipe in pipes:
        pygame.draw.rect(screen, GREEN, top_pipe)
        pygame.draw.rect(screen, GREEN, bottom_pipe)

def draw_bird(screen, bird_rect):
    """Desenha o pássaro na tela."""
    pygame.draw.rect(screen, YELLOW, bird_rect) # Usando um retângulo simples por enquanto

def check_collision(bird_rect, pipes):
    """Verifica colisão do pássaro com os canos ou limites da tela."""
    # Colisão com canos
    for top_pipe, bottom_pipe in pipes:
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            return True
    # Colisão com chão ou teto
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    return False

def display_score(screen, score, font):
    """Mostra a pontuação na tela."""
    score_surface = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)

def game_over_screen(screen, score, font):
    """Mostra a tela de Game Over."""
    game_over_text = font.render("Game Over!", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Pressione R para reiniciar ou Q para sair", True, WHITE)

    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    waiting = False # Reinicia o jogo

# --- Função Principal do Jogo ---
def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36) # Fonte padrão

    # load_images() # Descomente quando tiver as imagens

    # Variáveis do jogo
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    bird_rect = pygame.Rect(BIRD_X, bird_y, 30, 30) # Retângulo para o pássaro

    pipes = []
    pipe_spawn_timer = 0
    PIPE_SPAWN_INTERVAL = 120 # Controla a frequência de spawn dos canos (em frames)

    score = 0
    game_active = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_velocity = FLAP_STRENGTH
                if event.key == pygame.K_r and not game_active:
                    return # Reinicia o game_loop

        if game_active:
            # --- Lógica do Jogo ---
            # Movimento do Pássaro
            bird_velocity += GRAVITY
            bird_rect.y += bird_velocity

            # Geração de Canos
            pipe_spawn_timer += 1
            if pipe_spawn_timer >= PIPE_SPAWN_INTERVAL:
                pipes.extend(create_pipe())
                pipe_spawn_timer = 0

            pipes = move_pipes(pipes)

            # Checar Colisões
            if check_collision(bird_rect, pipes):
                game_active = False

            # Pontuação (simplificado: ganha ponto ao passar pelo "meio" da tela após um cano)
            # Uma forma mais precisa é checar se o pássaro passou o X do cano
            for top_pipe, bottom_pipe in pipes:
                # Verifica se o cano acabou de passar pelo pássaro e ainda não foi pontuado
                if top_pipe.right < bird_rect.left and not hasattr(top_pipe, 'passed'):
                    score += 1
                    top_pipe.passed = True # Marca o cano como pontuado


            # --- Desenhar na Tela ---
            screen.fill(BLUE) # Fundo azul
            # screen.blit(background_image, (0,0)) # Se tiver imagem de fundo

            draw_pipes(screen, pipes)
            draw_bird(screen, bird_rect)
            display_score(screen, score, font)

        else: # Game Over
            game_over_screen(screen, score, font)
            # O loop de game_over_screen vai esperar por R ou Q
            # Se R for pressionado, game_loop() será chamado novamente
            return # Sai desta instância do game_loop para reiniciar

        pygame.display.flip() # Atualiza a tela inteira
        clock.tick(60) # Limita a 60 FPS

# --- Iniciar o Jogo ---
if __name__ == "__main__":
    while True: # Loop para permitir reiniciar o jogo
        game_loop() 