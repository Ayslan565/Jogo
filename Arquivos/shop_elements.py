# shop_elements.py
import pygame
import random
import time
import os
import math

# --- ALTERAÇÃO 1: Importa a verificação da luta de chefe ---
# Tenta importar a função para saber se a luta está ativa.
try:
    from Luta_boss import esta_luta_ativa
except ImportError:
    # Se a importação falhar, cria uma função placeholder que sempre retorna False.
    # Isso evita que o jogo trave e assume que não há luta ativa.
    def esta_luta_ativa(): return False
    print("AVISO (shop_elements.py): Não foi possível importar 'esta_luta_ativa'. A loja pode aparecer durante a luta de chefe.")


# --- Configurações e Variáveis Globais ---

# Constantes da loja
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOP_SPRITE_PATH = os.path.join(project_root, "Sprites", "Loja", "Loja.png")
SHOP_PLACEHOLDER_SIZE = (150, 150)

# Variáveis de estado da loja (globais)
current_shop_rect = None
shop_sprite_image = None
last_shop_spawn_time = 0

# Variáveis para os avisos visuais (pop-up e seta)
shop_spawn_popup_message = ""
shop_popup_display_time = 0
shop_arrow_visible = False
shop_arrow_display_time = 0
shop_arrow_target_pos = (0, 0)

# Importa as chances de spawn do arquivo de configuração
try:
    from Spawn_Loja import PROBABILIDADE_SPAWN_LOJA, INTERVALO_MINIMO_SPAWN_LOJA
except ImportError:
    print("AVISO (shop_elements): 'Spawn_Loja.py' não encontrado. A loja não aparecerá.")
    PROBABILIDADE_SPAWN_LOJA = 0.0
    INTERVALO_MINIMO_SPAWN_LOJA = float('inf')


def spawn_shop_if_possible(jogador, est, blocos_gerados):
    """
    Tenta criar a loja, verificando as condições de tempo, probabilidade e se a luta de chefe NÃO está ativa.
    """
    global current_shop_rect, shop_sprite_image, last_shop_spawn_time, shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time, shop_arrow_target_pos

    # --- ALTERAÇÃO 2: Impede o spawn durante a luta ---
    if esta_luta_ativa():
        return

    # Se a loja já existe, não faz nada.
    if current_shop_rect is not None:
        return

    # Validação dos objetos necessários
    if jogador is None or not hasattr(jogador, 'rect') or est is None:
        return

    bloco_tamanho = 1080
    jogador_bloco_x = int(jogador.rect.centerx // bloco_tamanho)
    jogador_bloco_y = int(jogador.rect.centery // bloco_tamanho)
    current_time = time.time()

    # Verifica o cooldown para o spawn
    if (current_time - last_shop_spawn_time) < INTERVALO_MINIMO_SPAWN_LOJA:
        return

    # Procura um bloco novo ao redor do jogador para tentar criar a loja
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            bloco_coord = (jogador_bloco_x + dx, jogador_bloco_y + dy)
            if bloco_coord not in blocos_gerados:
                # Se encontrar um bloco novo, verifica a probabilidade de spawn
                if random.random() < PROBABILIDADE_SPAWN_LOJA:
                    base_x = (jogador_bloco_x + dx) * bloco_tamanho
                    base_y = (jogador_bloco_y + dy) * bloco_tamanho
                    shop_x = base_x + random.randint(100, bloco_tamanho - SHOP_PLACEHOLDER_SIZE[0] - 100)
                    shop_y = base_y + random.randint(100, bloco_tamanho - SHOP_PLACEHOLDER_SIZE[1] - 100)
                    
                    try:
                        if os.path.exists(SHOP_SPRITE_PATH):
                            shop_sprite_image = pygame.image.load(SHOP_SPRITE_PATH).convert_alpha()
                        else: # Cria um placeholder se a imagem não for encontrada
                            shop_sprite_image = pygame.Surface(SHOP_PLACEHOLDER_SIZE, pygame.SRCALPHA)
                            shop_sprite_image.fill((100, 50, 0))
                    except pygame.error:
                        shop_sprite_image = pygame.Surface(SHOP_PLACEHOLDER_SIZE, pygame.SRCALPHA)
                        shop_sprite_image.fill((100, 50, 0))
                    
                    # Define a posição da loja e atualiza as variáveis de controle
                    current_shop_rect = shop_sprite_image.get_rect(topleft=(shop_x, shop_y))
                    last_shop_spawn_time = current_time
                    
                    # Ativa os avisos visuais
                    shop_spawn_popup_message = "Uma loja apareceu!"
                    shop_popup_display_time = 3000  # 3 segundos
                    shop_arrow_visible = True
                    shop_arrow_display_time = 10000 # 10 segundos
                    shop_arrow_target_pos = current_shop_rect.center
                    
                    # Para a busca após encontrar um local e criar a loja
                    return

# --- ALTERAÇÃO 3: Nova função para forçar o desaparecimento da loja ---
def despawn_loja_imediatamente():
    """Força a remoção da loja do mapa e reseta seu estado."""
    global current_shop_rect, shop_sprite_image, last_shop_spawn_time
    global shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time

    if current_shop_rect is not None:
        print("INFO(shop_elements): Loja removida do mapa para o início da luta de chefe.")
        current_shop_rect = None
        shop_sprite_image = None
        last_shop_spawn_time = time.time() # Reseta o cooldown
        # Limpa os avisos visuais
        shop_spawn_popup_message = ""
        shop_popup_display_time = 0
        shop_arrow_visible = False
        shop_arrow_display_time = 0

def draw_shop_elements(janela, camera_x, camera_y, dt_ms):
    """
    Desenha os elementos da loja (sprite, pop-up e seta) e atualiza seus timers.
    """
    global shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time

    # Desenha a imagem da loja
    if shop_sprite_image and current_shop_rect:
        shop_screen_pos = (current_shop_rect.x - camera_x, current_shop_rect.y - camera_y)
        janela.blit(shop_sprite_image, shop_screen_pos)

    # Atualiza e desenha o pop-up de aviso
    if shop_popup_display_time > 0:
        shop_popup_display_time -= dt_ms
        if shop_popup_display_time > 0:
            popup_font = pygame.font.Font(None, 40)
            popup_text_surface = popup_font.render(shop_spawn_popup_message, True, (255, 255, 255))
            popup_rect = popup_text_surface.get_rect(center=(janela.get_width() // 2, 80))
            popup_bg = pygame.Surface((popup_rect.width + 20, popup_rect.height + 10), pygame.SRCALPHA)
            popup_bg.fill((0, 0, 0, 180))
            janela.blit(popup_bg, (popup_rect.x - 10, popup_rect.y - 5))
            janela.blit(popup_text_surface, popup_rect)
        else:
            shop_spawn_popup_message = ""

    # Atualiza e desenha a seta direcional
    if shop_arrow_display_time > 0:
        shop_arrow_display_time -= dt_ms
        if shop_arrow_display_time <= 0:
            shop_arrow_visible = False
    
    if shop_arrow_visible and current_shop_rect:
        screen_center = (janela.get_width() // 2, janela.get_height() // 2)
        shop_screen_center = (current_shop_rect.centerx - camera_x, current_shop_rect.centery - camera_y)
        
        direction_vector = (shop_screen_center[0] - screen_center[0], shop_screen_center[1] - screen_center[1])
        distance = math.hypot(*direction_vector)
        
        if distance > 100: # Só desenha a seta se a loja estiver fora do centro
            norm_vec = (direction_vector[0] / distance, direction_vector[1] / distance)
            
            arrow_start_pos = (screen_center[0] + norm_vec[0] * 100, screen_center[1] + norm_vec[1] * 100)
            arrow_end_pos = (arrow_start_pos[0] + norm_vec[0] * 30, arrow_start_pos[1] + norm_vec[1] * 30)
            
            pygame.draw.line(janela, (255, 255, 0), arrow_start_pos, arrow_end_pos, 3)
            # Ponta da seta
            angle = math.atan2(norm_vec[1], norm_vec[0])
            p1 = (arrow_end_pos[0] - 10 * math.cos(angle - math.pi / 6), arrow_end_pos[1] - 10 * math.sin(angle - math.pi / 6))
            p2 = (arrow_end_pos[0] - 10 * math.cos(angle + math.pi / 6), arrow_end_pos[1] - 10 * math.sin(angle + math.pi / 6))
            pygame.draw.polygon(janela, (255, 255, 0), [arrow_end_pos, p1, p2])

def get_current_shop_rect():
    """Retorna o retângulo de colisão da loja atual."""
    return current_shop_rect

def reset_shop_spawn():
    """Reseta o estado da loja para permitir um novo spawn."""
    global current_shop_rect, shop_sprite_image, last_shop_spawn_time
    global shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time
    current_shop_rect = None
    shop_sprite_image = None
    last_shop_spawn_time = time.time()
    shop_spawn_popup_message = ""
    shop_popup_display_time = 0
    shop_arrow_visible = False
    shop_arrow_display_time = 0
