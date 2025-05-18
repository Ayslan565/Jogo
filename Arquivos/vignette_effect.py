import pygame
import math

def create_vignette_surface(width, height, strength=150, radius_falloff=0.85):
    """
    Cria uma superfície de vinheta.

    Args:
        width (int): Largura da superfície.
        height (int): Altura da superfície.
        strength (int): A opacidade máxima da vinheta nas bordas (0-255).
                        Controla o quão escuras as bordas se tornam.
        radius_falloff (float): Controla o quão rápido a vinheta aparece a partir do centro.
                                Valores menores (ex: 0.6) significam uma área central clara menor
                                e uma transição mais abrupta para a vinheta.
                                Valores maiores (ex: 0.9) significam uma área central clara maior
                                e a vinheta fica mais restrita às bordas extremas.
    Returns:
        pygame.Surface: A superfície da vinheta, pronta para ser desenhada sobre o jogo.
    """
    # Cria uma nova superfície que suporta transparência por pixel (SRCALPHA)
    vignette_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Calcula o centro da superfície
    center_x, center_y = width / 2, height / 2
    
    # Calcula a distância máxima do centro até um dos cantos da superfície.
    # Isso é usado para normalizar a distância de cada pixel ao centro.
    max_dist = math.sqrt(center_x**2 + center_y**2)

    # Itera sobre cada pixel da superfície
    for x in range(width):
        for y in range(height):
            # Calcula a distância do pixel atual (x, y) ao centro da superfície
            dist_x = x - center_x
            dist_y = y - center_y
            distance = math.sqrt(dist_x**2 + dist_y**2)

            # Normaliza a distância:
            # - Divide a distância do pixel pelo produto da distância máxima e o 'radius_falloff'.
            #   'radius_falloff' efetivamente escala a "área clara" no centro.
            # - Garante que o valor normalizado não exceda 1.0 (usando min).
            #   Pixels dentro da área clara terão norm_dist < 1, pixels fora terão norm_dist = 1.
            norm_dist = min(distance / (max_dist * radius_falloff), 1.0)

            # Calcula a opacidade (alpha) do pixel da vinheta:
            # - A opacidade aumenta com a 'norm_dist'.
            # - 'norm_dist**1.5' (ou outro expoente) controla a curva da transição.
            #   Um expoente > 1 faz a transição ser mais suave perto do centro e mais íngreme nas bordas.
            #   Um expoente de 1.0 daria uma transição linear.
            # - Multiplica pela 'strength' para definir a escuridão máxima da vinheta.
            alpha = int(strength * (norm_dist**1.5)) 
            
            # Garante que o valor alfa calculado não exceda a 'strength' máxima definida.
            alpha = min(alpha, strength) 

            # Define a cor do pixel na superfície da vinheta.
            # A cor é preta (0, 0, 0) com a opacidade (alpha) calculada.
            vignette_surf.set_at((x, y), (0, 0, 0, alpha))
            
    return vignette_surf
