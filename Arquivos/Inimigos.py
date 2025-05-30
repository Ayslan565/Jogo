# Inimigos.py
import pygame
import os
import time 
import math 
import random # Adicionado para o fallback de _resolver_colisao

class Inimigo(pygame.sprite.Sprite): 
    """
    Classe base para todos os inimigos no jogo.
    Define atributos comuns como vida, velocidade, dano de contato,
    valor de XP, carregamento de sprite, animação de flash de dano,
    e métodos básicos de movimento e desenho.
    """
    def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path):
        super().__init__()
        
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.hp = vida_maxima 
        self.max_hp = vida_maxima 
        self.velocidade = velocidade
        self.contact_damage = dano_contato
        self.xp_value = xp_value 
        self.sprite_path_base = sprite_path 

        # print(f"DEBUG INIT: Criando {type(self).__name__} em ({x},{y}) com vel: {self.velocidade}, sprite_path: {sprite_path}")

        self.image = self._carregar_sprite(sprite_path, (largura, altura))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.last_hit_time = 0 
        self.hit_flash_duration = 150 
        self.hit_flash_color = (255, 255, 255, 128) 
        
        self.facing_right = True 

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
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        game_root_dir = os.path.dirname(base_dir) 
        # Se Inimigos.py e a pasta 'Sprites' estiverem na mesma pasta (raiz do projeto), use:
        # game_root_dir = base_dir 
        
        full_path = os.path.join(game_root_dir, path.replace("\\", "/")) 

        # print(f"--- DEBUG INIMIGO BASE TENTANDO CARREGAR: {full_path}") 
        if not os.path.exists(full_path):
            print(f"DEBUG(Inimigo - _carregar_sprite): Aviso: Arquivo de sprite não encontrado: {full_path}. Usando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(img, (255, 0, 255), (0, 0, tamanho[0], tamanho[1])) 
            return img
        try:
            img = pygame.image.load(full_path).convert_alpha()
            img = pygame.transform.scale(img, tamanho)
            return img
        except pygame.error as e:
            print(f"DEBUG(Inimigo - _carregar_sprite): Erro ao carregar sprite '{full_path}': {e}. Usando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(img, (255, 0, 255), (0, 0, tamanho[0], tamanho[1]))
            return img

    def receber_dano(self, dano, fonte_dano_rect=None):
        """Reduz a vida do inimigo e ativa o efeito de flash."""
        self.hp -= dano
        self.last_hit_time = pygame.time.get_ticks() 
        if self.hp <= 0:
            self.hp = 0

    def esta_vivo(self):
        """Verifica se o inimigo ainda está vivo."""
        return self.hp > 0

    def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None): 
        """Move o inimigo na direção de um ponto alvo e atualiza a direção horizontal."""
        if self.esta_vivo() and self.velocidade > 0:
            # print(f"DEBUG MOVENDO: {type(self).__name__} (ID: {id(self)}) com vel: {self.velocidade}, dt_ms: {dt_ms}")
            
            dx = alvo_x - self.rect.centerx
            dy = alvo_y - self.rect.centery
            distancia = math.hypot(dx, dy)

            fator_tempo = 1.0 
            if dt_ms is not None and dt_ms > 0:
                fator_tempo = (dt_ms / (1000.0 / 60.0)) 
            # else:
                # print(f"DEBUG MOVENDO: {type(self).__name__} (ID: {id(self)}) usando fator_tempo 1.0 (frame-dependent ou dt_ms inválido)")


            if distancia > 0: 
                mov_x = (dx / distancia) * self.velocidade * fator_tempo
                mov_y = (dy / distancia) * self.velocidade * fator_tempo
                
                self.rect.x += mov_x
                self.rect.y += mov_y

                if dx > 0:
                    self.facing_right = True
                elif dx < 0:
                    self.facing_right = False
        elif self.esta_vivo() and self.velocidade <= 0:
            pass # print(f"DEBUG NÃO MOVENDO: {type(self).__name__} (ID: {id(self)}) está vivo mas velocidade é {self.velocidade}")


    def atualizar_animacao(self):
        """Atualiza o índice do sprite para a animação e aplica o flip horizontal."""
        agora = pygame.time.get_ticks()
        if self.sprites and len(self.sprites) > 1 and self.esta_vivo(): 
            if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                self.tempo_ultimo_update_animacao = agora
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
        
        if self.sprites and len(self.sprites) > 0:
            current_sprite_index = int(self.sprite_index % len(self.sprites))
            
            base_image = None
            if current_sprite_index < len(self.sprites) and isinstance(self.sprites[current_sprite_index], pygame.Surface):
                base_image = self.sprites[current_sprite_index]
            elif len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface): 
                base_image = self.sprites[0]
            
            if base_image:
                if hasattr(self, 'facing_right') and not self.facing_right:
                    self.image = pygame.transform.flip(base_image, True, False)
                else:
                    self.image = base_image
            elif not hasattr(self, 'image') or not isinstance(self.image, pygame.Surface): 
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (255, 0, 255), (0,0,self.largura,self.altura))
        elif not hasattr(self, 'image') or not isinstance(self.image, pygame.Surface): 
            self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 255), (0, 0, self.largura, self.altura))


    def _resolver_colisao_com_outro_inimigo(self, outro_inimigo):
        """Lógica para empurrar este inimigo para fora da colisão com outro, mantendo uma distância mínima."""
        dx = self.rect.centerx - outro_inimigo.rect.centerx
        dy = self.rect.centery - outro_inimigo.rect.centery
        
        dist_centers_current = math.hypot(dx, dy)

        if dist_centers_current == 0: 
            self.rect.x += random.choice([-1, 1, -2, 2]) 
            self.rect.y += random.choice([-1, 1, -2, 2])
            return

        radius_self = (self.rect.width + self.rect.height) / 4.0
        radius_other = (outro_inimigo.rect.width + outro_inimigo.rect.height) / 4.0
        
        min_gap = 10.0 
        desired_dist_centers = radius_self + radius_other + min_gap
        
        if dist_centers_current < desired_dist_centers:
            needed_separation = desired_dist_centers - dist_centers_current
            
            max_push_this_frame = 2.0  
            
            actual_push_magnitude = min(needed_separation, max_push_this_frame)
            
            norm_dx = dx / dist_centers_current
            norm_dy = dy / dist_centers_current
            
            self.rect.x += norm_dx * actual_push_magnitude
            self.rect.y += norm_dy * actual_push_magnitude


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        """
        Atualiza o estado do inimigo (movimento, animação, colisão entre inimigos e comportamento de contato).
        """
        # print(f"DEBUG UPDATE BASE: Chamado para {type(self).__name__} (ID: {id(self)})")

        if self.esta_vivo():
            pos_antes_movimento = self.rect.topleft 

            if hasattr(player, 'rect'):
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
            
            self.atualizar_animacao()
            
            if outros_inimigos: 
                for outro_inimigo in outros_inimigos:
                    if outro_inimigo != self and self.rect.colliderect(outro_inimigo.rect):
                        self._resolver_colisao_com_outro_inimigo(outro_inimigo)
            
            current_ticks = pygame.time.get_ticks()
            if hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo():
                if self.rect.colliderect(player.rect):
                    if (current_ticks - self.last_contact_time >= self.contact_cooldown):
                        if hasattr(player, 'receber_dano'):
                            player.receber_dano(self.contact_damage)
                            self.last_contact_time = current_ticks


    def desenhar(self, janela, camera_x, camera_y):
        """
        Desenha o inimigo na tela, aplicando o efeito de flash se estiver ativo,
        e desenha a barra de vida.
        """
        if not hasattr(self, 'image') or self.image is None or not isinstance(self.image, pygame.Surface): 
            self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255,0,255, 128), (0,0,self.largura, self.altura))
            if not hasattr(self, 'rect'): 
                self.rect = self.image.get_rect(topleft=(self.x, self.y))

        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y - camera_y

        janela.blit(self.image, (screen_x, screen_y))

        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time < self.hit_flash_duration and hasattr(self, 'image') and self.image:
            flash_image_overlay = self.image.copy()
            flash_image_overlay.fill(self.hit_flash_color[:3] + (0,), special_flags=pygame.BLEND_RGB_ADD) 
            flash_image_overlay.set_alpha(self.hit_flash_color[3]) 
            janela.blit(flash_image_overlay, (screen_x, screen_y))

        if self.hp < self.max_hp and self.hp > 0: 
            bar_width = self.largura
            bar_height = 5
            health_percentage = self.hp / self.max_hp
            current_bar_width = int(bar_width * health_percentage)
            
            bar_x = screen_x
            bar_y = screen_y - bar_height - 5 

            pygame.draw.rect(janela, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=2) 
            pygame.draw.rect(janela, (0, 255, 0), (bar_x, bar_y, current_bar_width, bar_height), border_radius=2) 
            pygame.draw.rect(janela, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=2) 


    def verificar_colisao(self, outro_objeto):
        """
        Verifica a colisão entre o inimigo e outro objeto.
        Assume que o outro objeto tem um atributo 'rect_colisao' ou 'rect'.
        """
        outro_rect = getattr(outro_objeto, 'rect_colisao', getattr(outro_objeto, 'rect', None))
        if outro_rect:
            return self.rect.colliderect(outro_rect)
        return False
