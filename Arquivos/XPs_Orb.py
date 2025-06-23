import pygame
import math
import random

class XPOrb(pygame.sprite.Sprite):
    """
    Classe base para uma orbe de XP que pode ser coletada pelo jogador.
    Define a animação de pulsação, o tempo de vida e uma sombra para melhor visibilidade.
    """
    def __init__(self, x, y, xp_value, cor_nucleo, cor_brilho, raio):
        super().__init__()

        self.xp_value = xp_value
        self.raio = raio
        # Aumentamos um pouco a área do sprite para garantir que a sombra não seja cortada
        self.tamanho_sprite = (raio * 3, raio * 3)
        
        # Atributos para o efeito de pulsação
        self.cor_nucleo = cor_nucleo
        self.cor_brilho = cor_brilho
        self.tempo_animacao = pygame.time.get_ticks() + random.randint(0, 500) # Desfasa as animações
        self.frequencia_pulso = 0.003

        # Cria a superfície inicial e o rect
        self.image = pygame.Surface(self.tamanho_sprite, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

        # Atributos de controle
        self.duracao_maxima_ms = 20000 # Orbe dura 20 segundos antes de desaparecer
        self.tempo_criacao = pygame.time.get_ticks()

    def _desenhar_brilho(self):
        """
        Desenha a orbe com um efeito de brilho pulsante e uma sombra para contraste.
        """
        self.image.fill((0, 0, 0, 0)) # Limpa a superfície
        
        # Fator de pulsação (0 a 1)
        fator_pulso = (math.sin(self.tempo_animacao * self.frequencia_pulso) + 1) / 2
        
        raio_brilho_atual = self.raio + (self.raio * 0.5 * fator_pulso)
        alpha_brilho = 70 + (80 * fator_pulso)
        
        centro_surf = (self.tamanho_sprite[0] // 2, self.tamanho_sprite[1] // 2)

        # --- NOVO: Desenha a sombra projetada ---
        # A sombra é escura, semitransparente e ligeiramente deslocada
        cor_sombra = (0, 0, 0, 90) 
        offset_sombra = self.raio * 0.15 # O deslocamento aumenta com o tamanho do orbe
        pos_sombra = (centro_surf[0] + offset_sombra, centro_surf[1] + offset_sombra)
        
        # A sombra também pulsa junto com o brilho para um efeito mais coeso
        pygame.draw.circle(
            self.image,
            cor_sombra,
            pos_sombra,
            int(raio_brilho_atual)
        )
        # --- FIM DA ADIÇÃO DA SOMBRA ---

        # Desenha o brilho externo (agora sobre a sombra)
        pygame.draw.circle(
            self.image,
            (*self.cor_brilho, int(alpha_brilho)),
            centro_surf,
            int(raio_brilho_atual)
        )
        # Desenha o núcleo interno
        pygame.draw.circle(
            self.image,
            self.cor_nucleo,
            centro_surf,
            self.raio
        )

    def update(self, dt_ms):
        """
        Atualiza a animação da orbe e verifica seu tempo de vida.
        """
        # Verifica se o tempo de vida expirou
        if pygame.time.get_ticks() - self.tempo_criacao > self.duracao_maxima_ms:
            self.kill()
            return
        
        # Atualiza a animação de pulsação
        self.tempo_animacao += dt_ms
        self._desenhar_brilho()

    def desenhar(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))


# --- Classes Específicas para cada tipo de Orbe (com cores ajustadas) ---

class XPOrbPequeno(XPOrb):
    """Orbe de 10 XP (Comum). Cor: Amarela."""
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y, 
            xp_value=10, 
            # Cor do núcleo mais vibrante para melhor contraste
            cor_nucleo=(255, 255, 0), 
            cor_brilho=(200, 180, 50), 
            raio=6
        )

class XPOrbMedio(XPOrb):
    """Orbe de 25 XP (Incomum). Cor: Azul."""
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y, 
            xp_value=25, 
            # Cor do núcleo mais saturada
            cor_nucleo=(100, 180, 255), 
            cor_brilho=(50, 120, 200), 
            raio=8
        )

class XPOrbGrande(XPOrb):
    """Orbe de 35 XP (Rara). Cor: Roxa."""
    def __init__(self, x, y):
        super().__init__(
            x=x, y=y, 
            xp_value=35, 
            # Cor do núcleo mais intensa
            cor_nucleo=(220, 160, 255), 
            cor_brilho=(160, 80, 200), 
            raio=10
        )