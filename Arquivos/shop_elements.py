# shop_elements.py
import pygame
import random
import time
import os
import math

# Constants for the shop
SHOP_SPRITE_PATH = "Sprites\\Loja\\Loja.png" # Path to the shop sprite image
SHOP_PLACEHOLDER_SIZE = (150, 150) # Size for the placeholder if image fails to load

# Global variables to manage the shop on the map
current_shop_rect = None # Pygame Rect object for the shop's collision and position
shop_sprite_image = None # Pygame Surface object for the shop's image
last_shop_spawn_time = 0 # Time (in seconds) of the last successful shop spawn

# Global variables for the shop pop-up and arrow
shop_spawn_popup_message = "" # Message displayed in the pop-up
shop_popup_display_time = 0 # Remaining time (in milliseconds) to display the pop-up
shop_arrow_visible = False # Boolean to control arrow visibility
shop_arrow_display_time = 0 # Remaining time (in milliseconds) to display the arrow
shop_arrow_target_pos = (0, 0) # Target position (center of the shop) for the arrow to point to

# Import shop spawn probability and minimum interval
try:
    from Spawn_Loja import PROBABILIDADE_SPAWN_LOJA, INTERVALO_MINIMO_SPAWN_LOJA
except ImportError:
    print("DEBUG(shop_elements): Warning: Module 'Spawn_Loja.py' or variables 'PROBABILIDADE_SPAWN_LOJA', 'INTERVALO_MINIMO_SPAWN_LOJA' not found.")
    PROBABILIDADE_SPAWN_LOJA = 0.0 # Set probability to zero if file not found
    INTERVALO_MINIMO_SPAWN_LOJA = 0 # Set interval to zero if file not found


def spawn_shop_if_possible(jogador, est, blocos_gerados):
    """
    Attempts to spawn the shop in a new map block around the player,
    if time and probability conditions are met.
    Updates the global shop and pop-up/arrow variables.
    """
    global current_shop_rect, shop_sprite_image, last_shop_spawn_time
    global shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time, shop_arrow_target_pos
    global SHOP_SPRITE_PATH, SHOP_PLACEHOLDER_SIZE, PROBABILIDADE_SPAWN_LOJA, INTERVALO_MINIMO_SPAWN_LOJA

    # If the shop already exists, do not attempt to spawn a new one
    if current_shop_rect is not None:
        return

    # Check if player and Estacoes object exist before calculating the block
    if jogador is None or not hasattr(jogador, 'rect') or est is None:
        print("DEBUG(shop_elements): Warning: Player or Estacoes object missing. Could not attempt to spawn the shop.")
        return

    bloco_tamanho = 1080 # Block size used to avoid re-generating
    jogador_bloco_x = int(jogador.rect.centerx // bloco_tamanho)
    jogador_bloco_y = int(jogador.rect.centery // bloco_tamanho)

    current_time = time.time()

    # Explore around the player (9 blocks)
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            bloco_coord = (jogador_bloco_x + dx, jogador_bloco_y + dy)

            if bloco_coord not in blocos_gerados:
                # This is where a new block would be added and processed
                # For shop spawning, it's enough that the block hasn't been generated
                # The logic of adding to blocos_gerados MUST remain in Game.py for grass/tree management
                # This function only cares about trying to spawn THE SHOP in this block.

                if PROBABILIDADE_SPAWN_LOJA > 0 and (current_time - last_shop_spawn_time) >= INTERVALO_MINIMO_SPAWN_LOJA:
                    if random.random() < PROBABILIDADE_SPAWN_LOJA:
                        print(f"DEBUG(shop_elements): Shop spawn probability ({PROBABILIDADE_SPAWN_LOJA*100:.1f}%) successful in block {bloco_coord} and minimum interval passed!")

                        base_x = (jogador_bloco_x + dx) * bloco_tamanho
                        base_y = (jogador_bloco_y + dy) * bloco_tamanho

                        shop_x = base_x + random.randint(50, bloco_tamanho - SHOP_PLACEHOLDER_SIZE[0] - 50) # Ensure margin
                        shop_y = base_y + random.randint(50, bloco_tamanho - SHOP_PLACEHOLDER_SIZE[1] - 50) # Ensure margin
                        shop_world_pos = (shop_x, shop_y)

                        # Try to load the shop image
                        try:
                            if os.path.exists(SHOP_SPRITE_PATH):
                                shop_sprite_image = pygame.image.load(SHOP_SPRITE_PATH).convert_alpha()
                                print(f"DEBUG(shop_elements): Shop image loaded for spawn: {SHOP_SPRITE_PATH}")
                            else:
                                print(f"DEBUG(shop_elements): Warning: Shop image not found for spawn: {SHOP_SPRITE_PATH}. Using placeholder.")
                                # Create a placeholder if the image is not found
                                shop_sprite_image = pygame.Surface(SHOP_PLACEHOLDER_SIZE, pygame.SRCALPHA)
                                pygame.draw.rect(shop_sprite_image, (100, 50, 0), (0, 0, SHOP_PLACEHOLDER_SIZE[0], SHOP_PLACEHOLDER_SIZE[1])) # Brown placeholder
                        except pygame.error as e:
                            print(f"DEBUG(shop_elements): Error loading shop image for spawn: {e}. Using placeholder.")
                            # Create a placeholder in case of loading error
                            shop_sprite_image = pygame.Surface(SHOP_PLACEHOLDER_SIZE, pygame.SRCALPHA)
                            pygame.draw.rect(shop_sprite_image, (100, 50, 0), (0, 0, SHOP_PLACEHOLDER_SIZE[0], SHOP_PLACEHOLDER_SIZE[1])) # Brown placeholder

                        # Create the shop's collision rectangle at the calculated position
                        if shop_sprite_image is not None:
                            current_shop_rect = shop_sprite_image.get_rect(topleft=shop_world_pos)
                            print(f"DEBUG(shop_elements): Shop spawned at ({shop_world_pos[0]}, {shop_world_pos[1]}).") # Debug spawn position
                            last_shop_spawn_time = current_time # Update the time of the last successful spawn

                            # Activate the pop-up and arrow
                            shop_spawn_popup_message = "Uma loja apareceu!"
                            shop_popup_display_time = 3000 # Display pop-up for 3 seconds (in milliseconds)
                            shop_arrow_visible = True
                            shop_arrow_display_time = 10000 # Display arrow for 10 seconds (in milliseconds)
                            # The arrow points to the center of the shop's rectangle
                            shop_arrow_target_pos = current_shop_rect.center
                            #print("DEBUG(shop_elements): Shop pop-up and arrow activated.") # Debug visual activation



def draw_shop_elements(janela, camera_x, camera_y, current_ticks):
    """
    Draws the shop sprite, pop-up, and directional arrow.
    Updates the pop-up and arrow timers.
    """
    global shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time, shop_arrow_target_pos
    global current_shop_rect, shop_sprite_image

    # Draw the shop sprite in the game world (if it exists)
    if shop_sprite_image is not None and current_shop_rect is not None:
        shop_screen_pos = (current_shop_rect.x - camera_x, current_shop_rect.y - camera_y)
        janela.blit(shop_sprite_image, shop_screen_pos)

    # Update the pop-up and arrow timers
    # We use Pygame's real time for decrementing
    # This assumes current_ticks is the result of pygame.time.get_ticks() at the start of the frame
    # and that this function is called once per frame.
    # The time_delta should be passed from the main loop's clock.get_rawtime()
    # For simplicity here, we'll assume a fixed decrement or that the caller handles dt.
    # Let's adjust to receive dt directly for accuracy.

    # If draw_shop_elements is called from main loop, it should receive dt (delta time)
    # For now, let's assume current_ticks is the current time in ms and we calculate delta
    # If this function is called inside the main game loop, the `dt` from `clock.tick()` should be passed.
    # For this standalone module, we'll simulate it by using `pygame.time.get_ticks()`
    # but the ideal would be to pass `dt` from the main game loop.
    
    # To fix the timer update, we need the actual delta time.
    # Let's assume the caller passes the `dt` from `clock.tick()` or `clock.get_rawtime()`.
    # For now, I'll modify the signature to accept `dt_ms` (delta time in milliseconds).
    # And the `Game.py` will need to pass `clock.get_rawtime()` to this function.

    # Re-evaluating: The original Game.py was using clock.get_rawtime() to decrement.
    # Let's keep that logic but make sure this function gets the correct delta time.
    # The `current_ticks` parameter is a bit misleading if it's just `pygame.time.get_ticks()`.
    # It's better to pass the `dt` (delta time) directly.
    # For now, I will keep `current_ticks` as a placeholder and assume `dt` is derived from it or passed implicitly.
    # However, the most robust way is `draw_shop_elements(janela, camera_x, camera_y, dt_ms)`.
    # I will update the `Game.py` call to pass `dt` from `clock.get_rawtime()`.

    # For now, let's use a simple decrement based on `clock.get_rawtime()` if called from main loop,
    # or assume `dt_ms` is the delta time.
    # Since this function is called from `desenhar_cena` which doesn't have `dt`,
    # we'll need to pass `dt` from `main` to `desenhar_cena` and then here.
    # Or, we can make this function calculate `dt` from a global `last_frame_time` if it's truly standalone.
    # Given the current structure, let's assume `dt` is the time elapsed since the last frame.
    # The original `Game.py` was decrementing `shop_popup_display_time` by `clock.get_rawtime()`.
    # So, `draw_shop_elements` needs `dt` (delta time) as an argument.

    # Let's adjust the timer logic to use a passed `dt_ms`
    # The `current_ticks` parameter should be `dt_ms` (delta time in milliseconds)
    dt_ms = current_ticks # Renaming for clarity, assuming `dt` is passed here

    if shop_popup_display_time > 0:
        shop_popup_display_time -= dt_ms
        if shop_popup_display_time <= 0:
            shop_spawn_popup_message = ""
            print("DEBUG(shop_elements): Shop pop-up timer expired.")

    if shop_arrow_display_time > 0:
        shop_arrow_display_time -= dt_ms
        if shop_arrow_display_time <= 0:
            shop_arrow_visible = False
            print("DEBUG(shop_elements): Shop arrow timer expired.")

    # Draw the shop pop-up (if active)
    if shop_popup_display_time > 0 and shop_spawn_popup_message:
            popup_font = pygame.font.Font(None, 40)
            popup_text_surface = popup_font.render(shop_spawn_popup_message, True, (255, 255, 255))
            popup_rect = popup_text_surface.get_rect(center=(janela.get_width() // 2, 80))
            popup_bg = pygame.Surface((popup_rect.width + 20, popup_rect.height + 10), pygame.SRCALPHA)
            popup_bg.fill((0, 0, 0, 180)) # Semi-transparent black background
            janela.blit(popup_bg, (popup_rect.x - 10, popup_rect.y - 5))
            janela.blit(popup_text_surface, popup_rect)


    # Draw the arrow pointing to the shop (if active)
    if shop_arrow_visible and current_shop_rect is not None:
        screen_center_x = janela.get_width() // 2
        screen_center_y = janela.get_height() // 2
        
        shop_screen_center_x = current_shop_rect.centerx - camera_x
        shop_screen_center_y = current_shop_rect.centery - camera_y
        
        direction_vector = (shop_screen_center_x - screen_center_x, shop_screen_center_y - screen_center_y)
        distance_to_shop_on_screen = math.hypot(direction_vector[0], direction_vector[1])

        arrow_start_distance = 100 # Distance from screen center where arrow starts
        arrow_length = 30 # Length of the arrow line

        # Draw the arrow only if the shop is outside the central visible area
        if distance_to_shop_on_screen > arrow_start_distance and distance_to_shop_on_screen > 0:
            direction_norm = (direction_vector[0] / distance_to_shop_on_screen,
                              direction_vector[1] / distance_to_shop_on_screen)
            
            
            arrow_start_x = screen_center_x + direction_norm[0] * arrow_start_distance
            arrow_start_y = screen_center_y + direction_norm[1] * arrow_start_distance
            arrow_start_pos = (arrow_start_x, arrow_start_y)

            arrow_end_x = arrow_start_x + direction_norm[0] * arrow_length
            arrow_end_y = arrow_start_y + direction_norm[1] * arrow_length
            arrow_end_pos = (arrow_end_x, arrow_end_y)

            pygame.draw.line(janela, (255, 255, 0), arrow_start_pos, arrow_end_pos, 3) # Yellow arrow

            # Draw the arrow tips (triangle)
            angle = math.atan2(direction_norm[1], direction_norm[0])
            head_size = 10
            point1 = (arrow_end_x - head_size * math.cos(angle - math.pi / 6),
                      arrow_end_y - head_size * math.sin(angle - math.pi / 6))
            point2 = (arrow_end_x - head_size * math.cos(angle + math.pi / 6),
                      arrow_end_y - head_size * math.sin(angle + math.pi / 6))
            pygame.draw.polygon(janela, (255, 255, 0), [arrow_end_pos, point1, point2]) # Yellow arrow

def get_current_shop_rect():
    """Returns the current shop's Rect object."""
    return current_shop_rect

def reset_shop_spawn():
    """Resets the shop's state to allow a new spawn."""
    global current_shop_rect, shop_sprite_image, last_shop_spawn_time
    global shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time
    current_shop_rect = None
    shop_sprite_image = None
    last_shop_spawn_time = time.time() # Reset the timer to the current time
    shop_spawn_popup_message = ""
    shop_popup_display_time = 0
    shop_arrow_visible = False
    shop_arrow_display_time = 0
    print("DEBUG(shop_elements): Shop spawn state reset.")

