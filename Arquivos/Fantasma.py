# Fantasma.py
import time
import pygame
import random
import math
import os # Importa os para verificar a existência de arquivos

# --- Placeholder para a classe base Inimigo se o arquivo Inimigos.py não for fornecido ---
try:
    from Inimigos import Inimigo
except ImportError:
    print("DEBUG(Fantasma): Aviso: Módulo 'Inimigos.py' não encontrado. Usando classe base Inimigo placeholder.")
    class Inimigo(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path):
            super().__init__()
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 255), (0, 0, largura, altura)) 
            self.rect = self.image.get_rect(topleft=(x, y))
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

            self.is_attacking = False
            self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
            self.hit_by_player_this_attack = False
            self.contact_cooldown = 1000
            self.last_contact_time = pygame.time.get_ticks()
            
            self.last_hit_time = 0
            self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.facing_right = True
            self.sprites = [self.image]
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.intervalo_animacao = 200

        def _carregar_sprite(self, path, tamanho):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            game_dir = os.path.dirname(base_dir)
            full_path = os.path.join(game_dir, path.replace("/", os.sep))
            if not os.path.exists(full_path):
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (255, 0, 255), (0, 0, tamanho[0], tamanho[1]))
                return img
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.scale(img, tamanho)
                return img
            except pygame.error:
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (255, 0, 255), (0, 0, tamanho[0], tamanho[1]))
                return img

        def receber_dano(self, dano):
            self.hp -= dano
            self.last_hit_time = pygame.time.get_ticks()
            if self.hp <= 0:
                self.hp = 0

        def esta_vivo(self):
            return self.hp > 0

        def mover_em_direcao(self, alvo_x, alvo_y):
            if self.esta_vivo() and self.velocidade > 0:
                dx = alvo_x - self.rect.centerx
                dy = alvo_y - self.rect.centery
                distancia = math.hypot(dx, dy)
                if distancia > 0:
                    dx_norm = dx / distancia
                    dy_norm = dy / distancia
                    self.rect.x += dx_norm * self.velocidade
                    self.rect.y += dy_norm * self.velocidade
                    if dx > 0: self.facing_right = True
                    elif dx < 0: self.facing_right = False
        
        def atualizar_animacao(self):
            agora = pygame.time.get_ticks()
            if self.sprites and len(self.sprites) > 1 and self.esta_vivo():
                if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                    self.tempo_ultimo_update_animacao = agora
                    self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            
            if self.sprites:
                idx = int(self.sprite_index % len(self.sprites)) if len(self.sprites) > 0 else 0
                if idx < len(self.sprites):
                    base_image = self.sprites[idx]
                    if hasattr(self, 'facing_right') and not self.facing_right:
                        self.image = pygame.transform.flip(base_image, True, False)
                    else:
                        self.image = base_image
                elif len(self.sprites) > 0:
                     self.image = self.sprites[0]
            elif not hasattr(self, 'image') or self.image is None:
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (255,0,255), (0,0,self.largura,self.altura))

        # CORREÇÃO APLICADA AQUI na assinatura do método update do placeholder
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None):
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
            if not hasattr(self, 'image') or self.image is None:
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (255,0,255), (0,0,self.largura,self.altura))
                if not hasattr(self, 'rect'):
                     self.rect = self.image.get_rect(topleft=(self.x,self.y))

            screen_x = self.rect.x - camera_x
            screen_y = self.rect.y - camera_y
            janela.blit(self.image, (screen_x, screen_y))
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time < self.hit_flash_duration:
                flash_surface = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                flash_surface.fill(self.hit_flash_color)
                janela.blit(flash_surface, (screen_x, screen_y))
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
# --- Fim do Placeholder para Inimigo ---


"""
Classe para o inimigo Fantasma.
Herda da classe base Inimigo.
"""
class Fantasma(Inimigo):
    sprites_carregados = None
    tamanho_sprite_definido = (60, 80) 

    def __init__(self, x, y, velocidade=1.5): 
        fantasma_vida_maxima = 50
        fantasma_contact_damage = 3
        fantasma_xp_value = 20
        caminho_sprite_principal_fantasma = "Sprites/Inimigos/Fantasma/Fantasma1.png" 

        if Fantasma.sprites_carregados is None:
            caminhos = [
                caminho_sprite_principal_fantasma, 
                "Sprites/Inimigos/Fantasma/Fantasma2.png",
                "Sprites/Inimigos/Fantasma/Fantasma3.png",
                "Sprites/Inimigos/Fantasma/Fantasma4.png",
                "Sprites/Inimigos/Fantasma/Fantasma5.png",
                "Sprites/Inimigos/Fantasma/Fantasma6.png",
                "Sprites/Inimigos/Fantasma/Fantasma8.png", 
                "Sprites/Inimigos/Fantasma/Fantasma9.png",
            ]
            Fantasma.sprites_carregados = []
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            game_root_dir = os.path.dirname(current_file_dir) 

            for path in caminhos:
                full_path = os.path.join(game_root_dir, path.replace("/", os.sep))
                try:
                    if os.path.exists(full_path):
                        sprite = pygame.image.load(full_path).convert_alpha()
                        sprite = pygame.transform.scale(sprite, Fantasma.tamanho_sprite_definido)
                        Fantasma.sprites_carregados.append(sprite)
                    else:
                        print(f"DEBUG(Fantasma): Erro: Sprite do Fantasma não encontrado: {full_path}")
                        placeholder = pygame.Surface(Fantasma.tamanho_sprite_definido, pygame.SRCALPHA)
                        pygame.draw.rect(placeholder, (0, 0, 255), (0, 0, Fantasma.tamanho_sprite_definido[0], Fantasma.tamanho_sprite_definido[1]))
                        Fantasma.sprites_carregados.append(placeholder)
                except pygame.error as e:
                    print(f"DEBUG(Fantasma): Erro ao carregar o sprite do Fantasma: {full_path} - {e}")
                    placeholder = pygame.Surface(Fantasma.tamanho_sprite_definido, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (0, 0, 255), (0, 0, Fantasma.tamanho_sprite_definido[0], Fantasma.tamanho_sprite_definido[1]))
                    Fantasma.sprites_carregados.append(placeholder)
            
            if not Fantasma.sprites_carregados:
                print("DEBUG(Fantasma): Aviso: Nenhum sprite do Fantasma carregado. Usando placeholder padrão.")
                placeholder = pygame.Surface(Fantasma.tamanho_sprite_definido, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (0, 0, 255), (0, 0, Fantasma.tamanho_sprite_definido[0], Fantasma.tamanho_sprite_definido[1]))
                Fantasma.sprites_carregados.append(placeholder)

        largura_fantasma = Fantasma.tamanho_sprite_definido[0]
        altura_fantasma = Fantasma.tamanho_sprite_definido[1]

        super().__init__(x, y, 
                         largura_fantasma, altura_fantasma, 
                         fantasma_vida_maxima, 
                         velocidade, 
                         fantasma_contact_damage, 
                         fantasma_xp_value, 
                         caminho_sprite_principal_fantasma)

        self.sprites = Fantasma.sprites_carregados 
        self.sprite_index = 0 
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() 
        self.intervalo_animacao = 150 

        self.is_attacking = False 
        self.attack_duration = 0.8 
        self.attack_timer = 0.0 
        self.attack_damage = 10 
        self.attack_range = 80 
        self.attack_cooldown = 3.0 
        self.last_attack_time = time.time() - self.attack_cooldown 
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.hit_by_player_this_attack = False

        if self.sprites: # Garante que self.sprites não está vazio
             idx = int(self.sprite_index % len(self.sprites)) if len(self.sprites) > 0 else 0
             if idx < len(self.sprites): # Verificação adicional de segurança
                self.image = self.sprites[idx]
             elif len(self.sprites) > 0: # Fallback para o primeiro sprite
                self.image = self.sprites[0]

    def receber_dano(self, dano):
        super().receber_dano(dano) 

    def atualizar_animacao(self):
        super().atualizar_animacao() 

    def atacar(self, player):
        if not hasattr(player, 'rect'):
            return

        current_time = time.time()
        if self.esta_vivo() and not self.is_attacking and (current_time - self.last_attack_time >= self.attack_cooldown):
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                              self.rect.centery - player.rect.centery)

            if distancia_ao_jogador <= self.attack_range:
                self.is_attacking = True
                self.attack_timer = current_time 
                self.last_attack_time = current_time 
                self.hit_by_player_this_attack = False 
                
                attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0]
                attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1]
                
                # Posicionamento da hitbox de ataque
                if hasattr(self, 'facing_right'): 
                    if self.facing_right:
                        # Hitbox à direita do fantasma, um pouco à frente
                        hitbox_x = self.rect.centerx 
                        hitbox_y = self.rect.centery - attack_hitbox_height // 2
                        self.attack_hitbox = pygame.Rect(hitbox_x, hitbox_y, attack_hitbox_width, attack_hitbox_height)
                    else:
                        # Hitbox à esquerda do fantasma, um pouco à frente
                        hitbox_x = self.rect.centerx - attack_hitbox_width
                        hitbox_y = self.rect.centery - attack_hitbox_height // 2
                        self.attack_hitbox = pygame.Rect(hitbox_x, hitbox_y, attack_hitbox_width, attack_hitbox_height)
                else: 
                    self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                    self.attack_hitbox.center = self.rect.center


    # CORREÇÃO APLICADA AQUI na assinatura do método update
    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None):
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            return

        # Chama o update da classe base primeiro.
        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela)

        if self.esta_vivo():
            current_time_ataque = time.time()

            if self.is_attacking:
                # Atualiza a posição da hitbox se o fantasma se move durante o ataque
                attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0]
                attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1]
                if hasattr(self, 'facing_right'):
                    if self.facing_right:
                        hitbox_x = self.rect.centerx
                        hitbox_y = self.rect.centery - attack_hitbox_height // 2
                        self.attack_hitbox.topleft = (hitbox_x, hitbox_y) # Atualiza a posição
                    else:
                        hitbox_x = self.rect.centerx - attack_hitbox_width
                        hitbox_y = self.rect.centery - attack_hitbox_height // 2
                        self.attack_hitbox.topleft = (hitbox_x, hitbox_y) # Atualiza a posição
                else:
                    self.attack_hitbox.center = self.rect.center


                if current_time_ataque - self.attack_timer >= self.attack_duration:
                    self.is_attacking = False
                    self.hit_by_player_this_attack = False
                else:
                    if not self.hit_by_player_this_attack and \
                       hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0 and \
                       self.attack_hitbox.colliderect(player.rect):
                        if hasattr(player, 'receber_dano') and player.vida.esta_vivo():
                            dano_inimigo = getattr(self, 'attack_damage', 0)
                            player.receber_dano(dano_inimigo)
                            self.hit_by_player_this_attack = True
            
            if not self.is_attacking: # Só tenta iniciar um novo ataque se não estiver no meio de um
                self.atacar(player)

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y)
        # Opcional: Desenhar a hitbox de ataque para debug
        # if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0:
        #     debug_hitbox_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
        #     pygame.draw.rect(surface, (255, 0, 0, 100), debug_hitbox_rect_onscreen, 1)
