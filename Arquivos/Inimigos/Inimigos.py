# Arquivo: Inimigos.py (Atualizado para colisão centralizada)
import pygame
import os
import time 
import math 
import random

class Inimigo(pygame.sprite.Sprite): 
    """
    Classe base para todos os inimigos no jogo.
    A lógica de colisão entre inimigos foi removida para ser gerenciada centralmente.
    """
    def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path):
        super().__init__()
        
        # --- CORREÇÃO APLICADA AQUI ---
        # Garante que as posições X e Y sejam floats para movimento e colisão suaves.
        self.x = float(x)
        self.y = float(y)
        
        self.largura = largura
        self.altura = altura
        self.hp = vida_maxima 
        self.max_hp = vida_maxima 
        self.velocidade = velocidade
        self.contact_damage = dano_contato
        self.xp_value = xp_value 
        self.sprite_path_base = sprite_path 

        self.image = self._carregar_sprite(sprite_path, (largura, altura))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.last_hit_time = 0 
        self.hit_flash_duration = 150 
        self.hit_flash_color = (255, 255, 255, 128) 
        
        self.facing_right = True 

        # Garante que a lista de sprites nunca esteja vazia
        if hasattr(self, 'image') and isinstance(self.image, pygame.Surface):
            self.sprites = [self.image]
        else: 
            placeholder_surface = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(placeholder_surface, (255,0,255), (0,0,largura,altura))
            self.sprites = [placeholder_surface]
            if not hasattr(self, 'image') or not isinstance(self.image, pygame.Surface): 
                self.image = placeholder_surface
        
        self.sprite_index = 0
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
        self.intervalo_animacao = 200 

        self.is_attacking = False 
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) 
        self.hit_by_player_this_attack = False 
        
        self.contact_cooldown = 1000 
        self.last_contact_time = pygame.time.get_ticks()

    def _carregar_sprite(self, path, tamanho):
        """Carrega e escala um sprite, com um fallback para placeholder."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(project_root, path)

        if not os.path.exists(full_path):
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(img, (255, 0, 255), (0, 0, tamanho[0], tamanho[1])) 
            return img
        try:
            img = pygame.image.load(full_path).convert_alpha()
            img = pygame.transform.scale(img, tamanho)
            return img
        except pygame.error as e:
            print(f"ERRO (Inimigo): Ao carregar sprite '{full_path}': {e}. Usando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(img, (255, 0, 255), (0, 0, tamanho[0], tamanho[1]))
            return img

    def receber_dano(self, dano, fonte_dano_rect=None):
        self.hp -= dano
        self.last_hit_time = pygame.time.get_ticks() 
        if self.hp <= 0:
            self.hp = 0

    def esta_vivo(self):
        return self.hp > 0

    def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None): 
        if self.esta_vivo() and self.velocidade > 0:
            dx = alvo_x - self.rect.centerx
            dy = alvo_y - self.rect.centery
            distancia = math.hypot(dx, dy)

            fator_tempo = (dt_ms / 1000.0) if dt_ms and dt_ms > 0 else (1/60.0)

            if distancia > 0: 
                mov_x = (dx / distancia) * self.velocidade * 60 * fator_tempo
                mov_y = (dy / distancia) * self.velocidade * 60 * fator_tempo
                
                # --- CORREÇÃO APLICADA AQUI ---
                # Atualiza as posições float para movimento suave
                self.x += mov_x
                self.y += mov_y
                
                # Atualiza o rect a partir das posições float
                self.rect.x = int(self.x)
                self.rect.y = int(self.y)

                self.facing_right = dx > 0

    def atualizar_animacao(self):
        agora = pygame.time.get_ticks()
        if self.sprites and len(self.sprites) > 1 and self.esta_vivo(): 
            if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                self.tempo_ultimo_update_animacao = agora
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
        
        if self.sprites:
            base_image = self.sprites[int(self.sprite_index % len(self.sprites))]
            self.image = pygame.transform.flip(base_image, not self.facing_right, False)
        else:
            self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 255), self.image.get_rect())

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        """Atualiza o estado do inimigo (movimento, animação, dano de contato)."""
        if not self.esta_vivo():
            return

        # 1. Mover em direção ao jogador
        if hasattr(player, 'rect'):
            self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
        
        # 2. Atualizar a animação
        self.atualizar_animacao()
        
        # 3. Lidar com dano de contato ao jogador
        current_ticks = pygame.time.get_ticks()
        if hasattr(player, 'vida') and player.esta_vivo() and self.rect.colliderect(player.rect):
            if (current_ticks - self.last_contact_time >= self.contact_cooldown):
                if hasattr(player, 'receber_dano'):
                    player.receber_dano(self.contact_damage)
                    self.last_contact_time = current_ticks

    def desenhar(self, janela, camera_x, camera_y):
        """Desenha o inimigo e sua barra de vida."""
        if not hasattr(self, 'image') or self.image is None: return

        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y - camera_y

        janela.blit(self.image, (screen_x, screen_y))

        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time < self.hit_flash_duration:
            flash_overlay = self.image.copy()
            flash_overlay.fill(self.hit_flash_color, special_flags=pygame.BLEND_RGBA_MULT)
            janela.blit(flash_overlay, (screen_x, screen_y))

        if self.hp < self.max_hp and self.hp > 0: 
            bar_width = self.largura
            bar_height = 5
            health_percentage = self.hp / self.max_hp
            current_bar_width = int(bar_width * health_percentage)
            bar_x = screen_x
            bar_y = screen_y - bar_height - 5 
            
            pygame.draw.rect(janela, (139, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=2) 
            pygame.draw.rect(janela, (60, 179, 113), (bar_x, bar_y, current_bar_width, bar_height), border_radius=2) 
            pygame.draw.rect(janela, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=2) 

    def verificar_colisao(self, outro_objeto):
        outro_rect = getattr(outro_objeto, 'rect_colisao', getattr(outro_objeto, 'rect', None))
        return self.rect.colliderect(outro_rect) if outro_rect else False
