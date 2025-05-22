# Troll.py
import pygame
import random
import math 
import time 
import os 

# Importa a classe base Inimigo do ficheiro Inimigos.py
try:
    from Inimigos import Inimigo
except ImportError:
    print("DEBUG(Troll): ERRO: Módulo 'Inimigos.py' ou classe 'Inimigo' NÃO encontrado. Usando classe Inimigo placeholder.")
    class Inimigo(pygame.sprite.Sprite): # Placeholder
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
            pygame.draw.rect(self.image, (0, 80, 0), (0, 0, largura, altura)) # Placeholder verde mais escuro para Troll
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
                print(f"DEBUG(InimigoPlaceholder): Aviso: Arquivo de sprite não encontrado: {full_path}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (0,80,0), (0, 0, tamanho[0], tamanho[1])) # Placeholder verde escuro
                return img
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.scale(img, tamanho)
                return img
            except pygame.error as e:
                print(f"DEBUG(InimigoPlaceholder): Erro ao carregar sprite '{full_path}': {e}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (0,80,0), (0, 0, tamanho[0], tamanho[1])) # Placeholder verde escuro
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
                pygame.draw.rect(self.image, (0,80,0), (0,0,self.largura,self.altura)) # Placeholder verde escuro


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
                pygame.draw.rect(self.image, (0,80,0), (0,0,self.largura,self.altura)) # Placeholder verde escuro
            if not hasattr(self, 'rect'):
                 self.rect = self.image.get_rect(topleft=(self.x,self.y))

            screen_x = self.rect.x - camera_x
            screen_y = self.rect.y - camera_y
            janela.blit(self.image, (screen_x, screen_y))

            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time < self.hit_flash_duration:
                flash_image_overlay = self.image.copy()
                flash_image_overlay.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGB_MAX) 
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

class Troll(Inimigo):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None 
    tamanho_sprite_definido = (120, 150) # Trolls são maiores

    def __init__(self, x, y, velocidade=1.2): # Trolls são mais lentos
        print(f"DEBUG(Troll): Inicializando Troll em ({x}, {y}) com velocidade {velocidade}.")

        troll_hp = 150 # Mais HP
        troll_contact_damage = 15 # Mais dano de contato
        troll_xp_value = 75 # Mais XP
        sprite_path_principal_andar = "Sprites/Inimigos/Troll/Troll_Andar1.png" 
        # sprite_path_principal_atacar = "Sprites/Inimigos/Troll/Troll_Atacar1.png" # Se tiver animação de ataque

        # Carrega sprites de andar
        if Troll.sprites_andar_carregados is None:
            caminhos_andar = [
                sprite_path_principal_andar,
                "Sprites/Inimigos/Troll/Troll_Andar2.png",
                "Sprites/Inimigos/Troll/Troll_Andar3.png",
                "Sprites/Inimigos/Troll/Troll_Andar4.png",
            ]
            Troll.sprites_andar_carregados = []
            self._carregar_lista_sprites(caminhos_andar, Troll.sprites_andar_carregados, Troll.tamanho_sprite_definido, "Andar")

        # Carrega sprites de atacar (opcional)
        if Troll.sprites_atacar_carregados is None:
            caminhos_atacar = [
                # "Sprites/Inimigos/Troll/Troll_Atacar1.png",
                # "Sprites/Inimigos/Troll/Troll_Atacar2.png",
                # "Sprites/Inimigos/Troll/Troll_Atacar3.png",
            ]
            Troll.sprites_atacar_carregados = []
            if caminhos_atacar: 
                 self._carregar_lista_sprites(caminhos_atacar, Troll.sprites_atacar_carregados, Troll.tamanho_sprite_definido, "Atacar")
            else: 
                if Troll.sprites_andar_carregados: # Usa o primeiro frame de andar se não houver sprites de ataque
                    Troll.sprites_atacar_carregados = [Troll.sprites_andar_carregados[0]] 
                else: # Fallback extremo
                    placeholder_ataque = pygame.Surface(Troll.tamanho_sprite_definido, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder_ataque, (0,70,0), (0,0,Troll.tamanho_sprite_definido[0],Troll.tamanho_sprite_definido[1]))
                    Troll.sprites_atacar_carregados = [placeholder_ataque]

        super().__init__(x, y, 
                         Troll.tamanho_sprite_definido[0], Troll.tamanho_sprite_definido[1], 
                         troll_hp, velocidade, troll_contact_damage,
                         troll_xp_value, sprite_path_principal_andar)

        self.sprites = Troll.sprites_andar_carregados 
        self.sprite_index = 0 
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() 
        self.intervalo_animacao_andar = 250 # Animação mais lenta para o Troll
        self.intervalo_animacao_atacar = 180 
        self.intervalo_animacao = self.intervalo_animacao_andar 

        self.is_attacking = False 
        self.attack_duration = 0.8 # Duração da animação de ataque do Troll
        self.attack_timer = 0.0 
        self.attack_damage = 25 # Dano do ataque do Troll (ex: paulada)
        self.attack_range = 80  # Alcance um pouco maior para um porrete
        self.attack_cooldown = 2.5 
        self.last_attack_time = time.time() - self.attack_cooldown 

        self.attack_hitbox_largura = 60 # Hitbox de ataque maior
        self.attack_hitbox_altura = 80
        
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
        
        print(f"DEBUG(Troll): Troll inicializado. HP: {self.hp}, Vel: {self.velocidade}")

    def _carregar_lista_sprites(self, caminhos, lista_destino, tamanho, tipo_animacao):
        """Método auxiliar para carregar uma lista de sprites."""
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        game_root_dir = os.path.dirname(current_file_dir)
        
        for path in caminhos:
            full_path = os.path.join(game_root_dir, path.replace("/", os.sep))
            try:
                if os.path.exists(full_path):
                    sprite = pygame.image.load(full_path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                else:
                    print(f"DEBUG(Troll): Aviso: Sprite {tipo_animacao} do Troll não encontrado: {full_path}. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (0, 70, 0), (0, 0, tamanho[0], tamanho[1])) # Verde escuro para placeholder
                    lista_destino.append(placeholder)
            except pygame.error as e:
                print(f"DEBUG(Troll): Erro ao carregar o sprite {tipo_animacao} do Troll: {full_path} - {e}")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (0, 70, 0), (0, 0, tamanho[0], tamanho[1]))
                lista_destino.append(placeholder)
        
        if not lista_destino: 
            print(f"DEBUG(Troll): Aviso: Nenhum sprite de {tipo_animacao} do Troll carregado. Usando placeholder padrão.")
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (0, 70, 0), (0, 0, tamanho[0], tamanho[1]))
            lista_destino.append(placeholder)

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
                self.sprites = Troll.sprites_atacar_carregados 
                self.intervalo_animacao = self.intervalo_animacao_atacar
                self.sprite_index = 0 
                print(f"DEBUG(Troll): Troll iniciando ataque! Dist: {distancia_ao_jogador:.0f}")
                
                if self.facing_right:
                    hitbox_x = self.rect.right 
                else:
                    hitbox_x = self.rect.left - self.attack_hitbox_largura                
                hitbox_y = self.rect.centery - (self.attack_hitbox_altura / 2)
                self.attack_hitbox = pygame.Rect(hitbox_x, hitbox_y, self.attack_hitbox_largura, self.attack_hitbox_altura)

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None):
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            return

        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela) 

        if self.esta_vivo():
            current_time_ataque = time.time()

            if self.is_attacking:
                if self.facing_right:
                    hitbox_x = self.rect.right
                else:
                    hitbox_x = self.rect.left - self.attack_hitbox_largura
                hitbox_y = self.rect.centery - (self.attack_hitbox_altura / 2)
                self.attack_hitbox.topleft = (hitbox_x, hitbox_y)

                if current_time_ataque - self.attack_timer >= self.attack_duration:
                    self.is_attacking = False 
                    self.hit_by_player_this_attack = False 
                    self.sprites = Troll.sprites_andar_carregados 
                    self.intervalo_animacao = self.intervalo_animacao_andar
                    self.sprite_index = 0 
                else:
                    if not self.hit_by_player_this_attack and \
                       self.attack_hitbox.colliderect(player.rect):
                        if player.vida.esta_vivo(): 
                            player.receber_dano(self.attack_damage)
                            self.hit_by_player_this_attack = True 
                            print(f"DEBUG(Troll): Troll atacou o jogador! Dano: {self.attack_damage}")
            
            if not self.is_attacking:
                self.sprites = Troll.sprites_andar_carregados 
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.atacar(player)
        
    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y) 
    #     # Opcional: Desenhar a hitbox de ataque para debug
    #     if self.is_attacking and hasattr(self, 'attack_hitbox'):
    #         debug_hitbox_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
    #         pygame.draw.rect(surface, (0, 100, 0, 100), debug_hitbox_rect_onscreen, 1) # Verde escuro para hitbox do Troll
