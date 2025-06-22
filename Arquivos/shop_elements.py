# shop_elements.py
import pygame
import random
import time
import os
import math

# Tenta importar a função para saber se a luta está ativa.
try:
    from Luta_boss import esta_luta_ativa
except ImportError:
    # Se a importação falhar, cria uma função placeholder que sempre retorna False.
    def esta_luta_ativa(): return False
    print("AVISO (shop_elements.py): Não foi possível importar 'esta_luta_ativa'. A loja pode aparecer durante a luta de chefe.")


# --- Configurações e Variáveis Globais ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOP_SPRITE_PATH = os.path.join(project_root, "Sprites", "Loja", "Loja.png")
FONTE_RETRO_PATH = os.path.join(project_root, "Fontes", "Retro Gaming.ttf")
SHOP_PLACEHOLDER_SIZE = (150, 150)

# --- ALTERAÇÃO 1: Constantes para o pop-up ---
POPUP_TOTAL_DURATION = 3000.0  # Duração total do pop-up em milissegundos
FADE_IN_DURATION = 500.0   # Duração do fade-in em milissegundos
FADE_OUT_DURATION = 750.0  # Duração do fade-out em milissegundos

# Variáveis de estado da loja
current_shop_rect = None
shop_sprite_image = None
last_shop_spawn_time = 0

# Variáveis para os avisos visuais (pop-up e seta)
shop_spawn_popup_message = ""
shop_popup_display_time = 0
shop_arrow_visible = False
shop_arrow_display_time = 0
shop_arrow_target_pos = (0, 0)
popup_font_retro = None # Variável para carregar a fonte uma vez

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

    # Impede o spawn durante a luta
    if esta_luta_ativa():
        return

    if current_shop_rect is not None:
        return

    if jogador is None or not hasattr(jogador, 'rect') or est is None:
        return

    bloco_tamanho = 1080
    jogador_bloco_x = int(jogador.rect.centerx // bloco_tamanho)
    jogador_bloco_y = int(jogador.rect.centery // bloco_tamanho)
    current_time = time.time()

    if (current_time - last_shop_spawn_time) < INTERVALO_MINIMO_SPAWN_LOJA:
        return

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            bloco_coord = (jogador_bloco_x + dx, jogador_bloco_y + dy)
            if bloco_coord not in blocos_gerados:
                if random.random() < PROBABILIDADE_SPAWN_LOJA:
                    base_x = (jogador_bloco_x + dx) * bloco_tamanho
                    base_y = (jogador_bloco_y + dy) * bloco_tamanho
                    shop_x = base_x + random.randint(100, bloco_tamanho - SHOP_PLACEHOLDER_SIZE[0] - 100)
                    shop_y = base_y + random.randint(100, bloco_tamanho - SHOP_PLACEHOLDER_SIZE[1] - 100)
                    
                    try:
                        if os.path.exists(SHOP_SPRITE_PATH):
                            shop_sprite_image = pygame.image.load(SHOP_SPRITE_PATH).convert_alpha()
                        else:
                            shop_sprite_image = pygame.Surface(SHOP_PLACEHOLDER_SIZE, pygame.SRCALPHA)
                            shop_sprite_image.fill((100, 50, 0))
                    except pygame.error:
                        shop_sprite_image = pygame.Surface(SHOP_PLACEHOLDER_SIZE, pygame.SRCALPHA)
                        shop_sprite_image.fill((100, 50, 0))
                    
                    current_shop_rect = shop_sprite_image.get_rect(topleft=(shop_x, shop_y))
                    last_shop_spawn_time = current_time
                    
                    shop_spawn_popup_message = "Uma loja apareceu!"
                    shop_popup_display_time = POPUP_TOTAL_DURATION
                    shop_arrow_visible = True
                    shop_arrow_display_time = 10000
                    shop_arrow_target_pos = current_shop_rect.center
                    
                    return

def despawn_loja_imediatamente():
    """Força a remoção da loja do mapa e reseta seu estado."""
    global current_shop_rect, shop_sprite_image, last_shop_spawn_time, shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time

    if current_shop_rect is not None:
        print("INFO(shop_elements): Loja removida do mapa para o início da luta de chefe.")
        current_shop_rect = None
        shop_sprite_image = None
        last_shop_spawn_time = time.time()
        shop_spawn_popup_message = ""
        shop_popup_display_time = 0
        shop_arrow_visible = False
        shop_arrow_display_time = 0

def draw_shop_elements(janela, camera_x, camera_y, dt_ms):
    """
    Desenha os elementos da loja (sprite, pop-up e seta) e atualiza seus timers.
    """
    global shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time, popup_font_retro

    if shop_sprite_image and current_shop_rect:
        shop_screen_pos = (current_shop_rect.x - camera_x, current_shop_rect.y - camera_y)
        janela.blit(shop_sprite_image, shop_screen_pos)

    # Lógica de desenho do pop-up
    if shop_popup_display_time > 0:
        shop_popup_display_time -= dt_ms
        if shop_popup_display_time > 0:
            
            # Tenta carregar a fonte customizada uma única vez
            if popup_font_retro is None:
                try:
                    popup_font_retro = pygame.font.Font(FONTE_RETRO_PATH, 40)
                except pygame.error:
                    print(f"AVISO: Fonte '{FONTE_RETRO_PATH}' não encontrada. Usando fonte padrão.")
                    popup_font_retro = pygame.font.Font(None, 48)

            # Configurações do novo design
            text_color = (255, 255, 255)
            bg_color = (50, 50, 50) # Cor de fundo sólida para o polígono
            
            text_surface = popup_font_retro.render(shop_spawn_popup_message, True, text_color)
            text_rect = text_surface.get_rect()

            rect_width = text_rect.width + 80
            rect_height = text_rect.height + 40
            triangle_width = 30

            popup_center_x = janela.get_width() // 2
            popup_center_y = janela.get_height() // 2
            
            rect_left = popup_center_x - rect_width / 2
            rect_right = popup_center_x + rect_width / 2
            rect_top = popup_center_y - rect_height / 2
            rect_bottom = popup_center_y + rect_height / 2
            
            left_tri_point = (rect_left - triangle_width, popup_center_y)
            right_tri_point = (rect_right + triangle_width, popup_center_y)

            polygon_points = [
                (rect_left, rect_top), (rect_right, rect_top),
                right_tri_point, (rect_right, rect_bottom),
                (rect_left, rect_bottom), left_tri_point
            ]

            # Cria uma superfície temporária para o pop-up completo
            total_width = rect_width + 2 * triangle_width
            shape_surface = pygame.Surface((total_width, rect_height), pygame.SRCALPHA)
            
            local_polygon_points = [(p[0] - (rect_left - triangle_width), p[1] - rect_top) for p in polygon_points]
            pygame.draw.polygon(shape_surface, bg_color, local_polygon_points)
            
            text_pos_x = (total_width - text_rect.width) // 2
            text_pos_y = (rect_height - text_rect.height) // 2
            shape_surface.blit(text_surface, (text_pos_x, text_pos_y))
            
            # --- ALTERAÇÃO 2: Lógica de esmaecimento (fade-in e fade-out) ---
            time_from_start = POPUP_TOTAL_DURATION - shop_popup_display_time
            alpha = 255 # Opacidade total por padrão

            if time_from_start < FADE_IN_DURATION:
                # Fade-in no início
                alpha = max(0, 255 * (time_from_start / FADE_IN_DURATION))
            elif shop_popup_display_time < FADE_OUT_DURATION:
                # Fade-out no final
                alpha = max(0, 255 * (shop_popup_display_time / FADE_OUT_DURATION))
            
            shape_surface.set_alpha(alpha)
            
            final_pos_x = rect_left - triangle_width
            final_pos_y = rect_top
            janela.blit(shape_surface, (final_pos_x, final_pos_y))
            
        else:
            shop_spawn_popup_message = ""

    # Lógica da seta direcional
    if shop_arrow_display_time > 0:
        shop_arrow_display_time -= dt_ms
        if shop_arrow_display_time <= 0:
            shop_arrow_visible = False
    
    if shop_arrow_visible and current_shop_rect:
        screen_center = (janela.get_width() // 2, janela.get_height() // 2)
        shop_screen_center = (current_shop_rect.centerx - camera_x, current_shop_rect.centery - camera_y)
        
        direction_vector = (shop_screen_center[0] - screen_center[0], shop_screen_center[1] - screen_center[1])
        distance = math.hypot(*direction_vector)
        
        if distance > 150:
            norm_vec = (direction_vector[0] / distance, direction_vector[1] / distance)
            
            arrow_start_pos = (screen_center[0] + norm_vec[0] * 120, screen_center[1] + norm_vec[1] * 120)
            arrow_end_pos = (arrow_start_pos[0] + norm_vec[0] * 30, arrow_start_pos[1] + norm_vec[1] * 30)
            
            pygame.draw.line(janela, (255, 255, 0), arrow_start_pos, arrow_end_pos, 4)
            angle = math.atan2(norm_vec[1], norm_vec[0])
            p1 = (arrow_end_pos[0] - 12 * math.cos(angle - math.pi / 6), arrow_end_pos[1] - 12 * math.sin(angle - math.pi / 6))
            p2 = (arrow_end_pos[0] - 12 * math.cos(angle + math.pi / 6), arrow_end_pos[1] - 12 * math.sin(angle + math.pi / 6))
            pygame.draw.polygon(janela, (255, 255, 0), [arrow_end_pos, p1, p2])

def get_current_shop_rect():
    """Retorna o retângulo de colisão da loja atual."""
    return current_shop_rect

def reset_shop_spawn():
    """Reseta o estado da loja para permitir um novo spawn."""
    global current_shop_rect, shop_sprite_image, last_shop_spawn_time, shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time
    current_shop_rect = None
    shop_sprite_image = None
    last_shop_spawn_time = time.time()
    shop_spawn_popup_message = ""
    shop_popup_display_time = 0
    shop_arrow_visible = False
    shop_arrow_display_time = 0
