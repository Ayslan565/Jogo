# Espirito_Das_Flores.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()
import os # Importa os para verificar a existência de arquivos

# Importa a classe base Inimigo do ficheiro Inimigos.py
# Certifique-se de que o ficheiro Inimigos.py está na mesma pasta ou num caminho acessível
try:
    from Inimigos import Inimigo
except ImportError:
    # Define uma classe Inimigo placeholder mais completa para evitar NameError e AttributeError
    class Inimigo(pygame.sprite.Sprite):
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

            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 255), (0, 0, largura, altura)) 
            self.rect = self.image.get_rect(topleft=(x, y))

            self.last_hit_time = 0
            self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128) 

            self.is_attacking = False
            self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
            self.hit_by_player_this_attack = False
            self.contact_cooldown = 1000 
            self.last_contact_time = pygame.time.get_ticks()
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
            except pygame.error as e:
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
                dist = math.hypot(dx, dy)
                if dist > 0:
                    dx_norm = dx / dist
                    dy_norm = dy / dist
                    self.rect.x += dx_norm * self.velocidade
                    self.rect.y += dy_norm * self.velocidade
                    if dx > 0:
                        self.facing_right = True
                    elif dx < 0:
                        self.facing_right = False
        
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
                if hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                   self.rect.colliderect(player.rect) and \
                   (current_ticks - self.last_contact_time >= self.contact_cooldown):
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

            if self.hp < self.max_hp and self.hp > 0 :
                bar_width = self.largura
                bar_height = 5
                health_percentage = self.hp / self.max_hp
                current_bar_width = int(bar_width * health_percentage)
                bar_x = screen_x
                bar_y = screen_y - bar_height - 5 
                pygame.draw.rect(janela, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=2)
                pygame.draw.rect(janela, (0, 255, 0), (bar_x, bar_y, current_bar_width, bar_height), border_radius=2)
                pygame.draw.rect(janela, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=2)


"""
Classe para o inimigo Espírito das Flores.
Herda da classe base Inimigo.
"""
class Espirito_Das_Flores(Inimigo):
    sprites_originais = None 
    tamanho_sprite_definido = (70, 70)

    def __init__(self, x, y, velocidade=1.8): 

        espirito_hp = 75 
        espirito_contact_damage = 8 
        espirito_xp_value = 40 
        sprite_path_principal = "Sprites/Inimigos/Espirito_Flores/Espirito_Flores1.png" 

        if Espirito_Das_Flores.sprites_originais is None:
            caminhos = [
                sprite_path_principal,
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores2.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores3.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores4.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores5.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores6.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores7.png",
            ]
            Espirito_Das_Flores.sprites_originais = []
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            game_root_dir = os.path.dirname(current_file_dir) 

            for path in caminhos:
                full_path = os.path.join(game_root_dir, path.replace("/", os.sep))
                try:
                    if os.path.exists(full_path): 
                        sprite = pygame.image.load(full_path).convert_alpha()
                        sprite = pygame.transform.scale(sprite, Espirito_Das_Flores.tamanho_sprite_definido)
                        Espirito_Das_Flores.sprites_originais.append(sprite)
                    else:
                        placeholder = pygame.Surface(Espirito_Das_Flores.tamanho_sprite_definido, pygame.SRCALPHA)
                        pygame.draw.rect(placeholder, (255, 105, 180), (0, 0, Espirito_Das_Flores.tamanho_sprite_definido[0], Espirito_Das_Flores.tamanho_sprite_definido[1])) 
                        Espirito_Das_Flores.sprites_originais.append(placeholder)
                except pygame.error as e:
                    placeholder = pygame.Surface(Espirito_Das_Flores.tamanho_sprite_definido, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (255, 105, 180), (0, 0, Espirito_Das_Flores.tamanho_sprite_definido[0], Espirito_Das_Flores.tamanho_sprite_definido[1])) 
                    Espirito_Das_Flores.sprites_originais.append(placeholder)
            
            if not Espirito_Das_Flores.sprites_originais:
                print("DEBUG(Espirito_Das_Flores): Aviso: Nenhum sprite do Espírito das Flores carregado. Usando placeholder padrão.")
                placeholder = pygame.Surface(Espirito_Das_Flores.tamanho_sprite_definido, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255, 105, 180), (0, 0, Espirito_Das_Flores.tamanho_sprite_definido[0], Espirito_Das_Flores.tamanho_sprite_definido[1]))
                Espirito_Das_Flores.sprites_originais.append(placeholder)

        super().__init__(x, y, 
                         Espirito_Das_Flores.tamanho_sprite_definido[0], Espirito_Das_Flores.tamanho_sprite_definido[1], 
                         espirito_hp, velocidade, espirito_contact_damage,
                         espirito_xp_value, sprite_path_principal)

        self.sprites = Espirito_Das_Flores.sprites_originais 
        self.sprite_index = 0 
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() 
        self.intervalo_animacao = 180 

        self.is_attacking = False 
        self.attack_duration = 0.6 
        self.attack_timer = 0.0 # Consistência com time.time()
        self.attack_damage = 12 
        self.attack_hitbox_size = (50, 50) 
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) 
        self.attack_range = 70 
        self.attack_cooldown = 2.5 # Segundos
        self.last_attack_time = time.time() - self.attack_cooldown # Permite atacar mais cedo
        
        # self.facing_right é herdado. Pode ser inicializado para False se o sprite base for para a esquerda
        # self.facing_right = False 

        if self.sprites: 
             idx = int(self.sprite_index % len(self.sprites)) if len(self.sprites) > 0 else 0
             if idx < len(self.sprites): 
                self.image = self.sprites[idx]
             elif len(self.sprites) > 0: 
                self.image = self.sprites[0]

    def receber_dano(self, dano):
        super().receber_dano(dano) 


    def atualizar_animacao(self):
        # A classe base Inimigo.atualizar_animacao() já lida com o flip
        super().atualizar_animacao()


    def mover_em_direcao(self, alvo_x, alvo_y):
        # A classe base Inimigo.mover_em_direcao() já lida com isso, incluindo facing_right
        super().mover_em_direcao(alvo_x, alvo_y)


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
                
                attack_hitbox_width, attack_hitbox_height = self.attack_hitbox_size
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                self.attack_hitbox.center = self.rect.center 


    # CORREÇÃO APLICADA AQUI na assinatura do método update
    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None):
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            return

        # Chama o update da classe base para movimento, animação base, dano de contato base.
        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela)

        if self.esta_vivo():
            current_time_ataque = time.time()

            if self.is_attacking:
                # Atualiza a posição da hitbox de ataque (caso o espírito se mova durante o ataque)
                self.attack_hitbox.center = self.rect.center 

                if current_time_ataque - self.attack_timer >= self.attack_duration:
                    self.is_attacking = False
                    self.hit_by_player_this_attack = False 
                else:
                    # Lógica de Dano do Ataque Específico
                    if not self.hit_by_player_this_attack and \
                       hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0 and \
                       self.attack_hitbox.colliderect(player.rect):
                        if player.vida.esta_vivo(): 
                            player.receber_dano(self.attack_damage)
                            self.hit_by_player_this_attack = True 
            
            if not self.is_attacking:
                self.atacar(player)
        
        # A animação já é chamada pelo super().update()


    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y) 
        # Opcional: Desenhar a hitbox de ataque para debug
        # if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0:
        #     debug_hitbox_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
        #     pygame.draw.rect(surface, (255, 182, 193, 150), debug_hitbox_rect_onscreen, 1) # Rosa para hitbox do Espírito

