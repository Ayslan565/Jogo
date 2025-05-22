# Inimigos.py
# (Anteriormente referenciado como C:\Users\aysla\Documents\Jogo_Asrahel\Jogo\Arquivos\Inimigo.py pelo usuário)

import pygame
import os
import time # Para usar time.time() ou pygame.time.get_ticks()
import math # Para a função math.hypot

class Inimigo(pygame.sprite.Sprite): # Herda de pygame.sprite.Sprite
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
        self.hp = vida_maxima # Vida atual do inimigo
        self.max_hp = vida_maxima # Vida máxima do inimigo
        self.velocidade = velocidade
        self.contact_damage = dano_contato
        self.xp_value = xp_value # XP que o jogador ganha ao derrotar este inimigo

        # Carrega o sprite do inimigo
        self.image = self._carregar_sprite(sprite_path, (largura, altura))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # --- Atributos para o efeito de flash de dano ---
        self.last_hit_time = 0 # Tempo (em milissegundos) do último hit
        self.hit_flash_duration = 150 # Duração do flash em ms (0.15 segundos)
        # A cor do flash. O valor alfa (último componente) controla a intensidade do flash.
        self.hit_flash_color = (255, 255, 255, 128) # Branco com 50% de transparência (RGBA)
        
        self.facing_right = True 

        # Atributos de animação (básicos para a classe base)
        self.sprites = [self.image] if hasattr(self, 'image') and self.image is not None else []
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
        game_dir = os.path.dirname(base_dir) 
        full_path = os.path.join(game_dir, path.replace("/", os.sep))

        if not os.path.exists(full_path):
            print(f"DEBUG(Inimigo): Aviso: Arquivo de sprite não encontrado: {full_path}. Usando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(img, (255, 0, 255), (0, 0, tamanho[0], tamanho[1])) 
            return img
        try:
            img = pygame.image.load(full_path).convert_alpha()
            img = pygame.transform.scale(img, tamanho)
            return img
        except pygame.error as e:
            print(f"DEBUG(Inimigo): Erro ao carregar sprite '{full_path}': {e}. Usando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(img, (255, 0, 255), (0, 0, tamanho[0], tamanho[1]))
            return img

    def receber_dano(self, dano):
        """Reduz a vida do inimigo e ativa o efeito de flash."""
        self.hp -= dano
        self.last_hit_time = pygame.time.get_ticks() 
        if self.hp <= 0:
            self.hp = 0

    def esta_vivo(self):
        """Verifica se o inimigo ainda está vivo."""
        return self.hp > 0

    def mover_em_direcao(self, alvo_x, alvo_y):
        """Move o inimigo na direção de um ponto alvo e atualiza a direção horizontal."""
        if self.esta_vivo() and self.velocidade > 0:
            dx = alvo_x - self.rect.centerx
            dy = alvo_y - self.rect.centery
            distancia = math.hypot(dx, dy)

            if distancia > 0: 
                dx_norm = dx / distancia
                dy_norm = dy / distancia
                self.rect.x += dx_norm * self.velocidade
                self.rect.y += dy_norm * self.velocidade

                if dx > 0:
                    self.facing_right = True
                elif dx < 0:
                    self.facing_right = False

    def atualizar_animacao(self):
        """Atualiza o índice do sprite para a animação e aplica o flip horizontal."""
        agora = pygame.time.get_ticks()
        if self.sprites and len(self.sprites) > 1 and self.esta_vivo(): 
            if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                self.tempo_ultimo_update_animacao = agora
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
        
        if self.sprites:
            current_sprite_index = int(self.sprite_index % len(self.sprites)) if len(self.sprites) > 0 else 0
            if current_sprite_index < len(self.sprites):
                 base_image = self.sprites[current_sprite_index]
            else: 
                 base_image = self.sprites[0]

            if hasattr(self, 'facing_right') and not self.facing_right:
                self.image = pygame.transform.flip(base_image, True, False)
            else:
                self.image = base_image
        elif not hasattr(self, 'image') or self.image is None: 
            self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 255), (0, 0, self.largura, self.altura))

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None):
        """
        Atualiza o estado do inimigo (movimento, animação e comportamento de contato).
        """
        if self.esta_vivo():
            if hasattr(player, 'rect'):
                self.mover_em_direcao(player.rect.centerx, player.rect.centery)
            
            self.atualizar_animacao()
            
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
        if not hasattr(self, 'image') or self.image is None: 
            self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255,0,255), (0,0,self.largura, self.altura))
            if not hasattr(self, 'rect'): 
                 self.rect = self.image.get_rect(topleft=(self.x, self.y))

        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y - camera_y

        # Desenha o sprite normal do inimigo
        janela.blit(self.image, (screen_x, screen_y))

        # --- Lógica do flash de dano MODIFICADA ---
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time < self.hit_flash_duration:
            # Cria uma cópia da imagem atual do inimigo para o efeito de flash
            flash_image_overlay = self.image.copy()
            
            # Preenche as partes visíveis da cópia com branco.
            # BLEND_RGB_MAX (ou BLEND_RGBA_MAX) pega o valor máximo de cor, 
            # efetivamente tornando as partes coloridas do sprite brancas, 
            # respeitando a transparência original.
            flash_image_overlay.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGB_MAX) 
            # O alfa na cor de fill é ignorado por BLEND_RGB_MAX, mas é bom ter para RGBA_MAX.
            
            # Define o alfa da superfície de flash para a intensidade desejada
            # self.hit_flash_color é (R, G, B, Alpha_intensidade)
            flash_image_overlay.set_alpha(self.hit_flash_color[3]) # Usa o alfa de hit_flash_color (ex: 128)
            
            # Desenha a imagem com flash sobre a posição do inimigo
            janela.blit(flash_image_overlay, (screen_x, screen_y))
        # --- Fim da lógica do flash ---

        # Desenhar barra de vida do inimigo
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

