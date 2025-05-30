# Mae_Natureza.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()
import os # Importa os para verificar a existência de arquivos

# Importa a classe base Inimigo do ficheiro Inimigos.py
try:
    from Inimigos import Inimigo # Tenta importar a classe base real
    print("DEBUG(Mae_Natureza): Classe base Inimigo importada com sucesso.")
except ImportError:
    print("DEBUG(Mae_Natureza): ERRO: Módulo 'Inimigos.py' ou classe 'Inimigo' NÃO encontrado. Usando classe Inimigo placeholder.")
    # Define uma classe Inimigo placeholder mais completa
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

            self.image = self._carregar_sprite(sprite_path, (largura, altura))
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
            
            self.sprites = [self.image] if self.image and isinstance(self.image, pygame.Surface) else []
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.intervalo_animacao = 200

        def _carregar_sprite(self, path, tamanho): 
            base_dir = os.path.dirname(os.path.abspath(__file__)) 
            game_root_dir = os.path.dirname(base_dir) 
            # Se este script e a pasta 'Sprites' estiverem na mesma pasta (raiz do projeto):
            # game_root_dir = base_dir
            
            full_path = os.path.join(game_root_dir, path.replace("\\", "/"))
            # print(f"--- DEBUG PLACEHOLDER TENTANDO CARREGAR (Mae_Natureza): {full_path}")

            if not os.path.exists(full_path):
                print(f"DEBUG(InimigoPlaceholder - Mae_Natureza): Sprite não encontrado: {full_path}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (34,139,34), (0, 0, tamanho[0], tamanho[1])) # Verde floresta para placeholder
                return img
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.scale(img, tamanho)
                return img
            except pygame.error as e:
                print(f"DEBUG(InimigoPlaceholder - Mae_Natureza): Erro ao carregar sprite '{full_path}': {e}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (34,139,34), (0, 0, tamanho[0], tamanho[1]))
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
                dist = math.hypot(dx, dy)
                fator_tempo = 1.0
                if dt_ms is not None and dt_ms > 0:
                     fator_tempo = (dt_ms / (1000.0 / 60.0)) 
                
                if dist > 0:
                    dx_norm = dx / dist
                    dy_norm = dy / dist
                    self.rect.x += dx_norm * self.velocidade * fator_tempo
                    self.rect.y += dy_norm * self.velocidade * fator_tempo
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
            
            if self.sprites and len(self.sprites) > 0: 
                idx = int(self.sprite_index % len(self.sprites))
                if idx < len(self.sprites) and isinstance(self.sprites[idx], pygame.Surface): 
                    base_image = self.sprites[idx]
                    self.image = pygame.transform.flip(base_image, not self.facing_right, False)
                elif len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface): 
                    self.image = pygame.transform.flip(self.sprites[0], not self.facing_right, False)
            elif not hasattr(self, 'image') or not isinstance(self.image, pygame.Surface): 
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (34,139,34), (0,0,self.largura,self.altura))


        def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): 
            if self.esta_vivo():
                if hasattr(player, 'rect'):
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
                self.atualizar_animacao() 
                
                if outros_inimigos: 
                    for outro_inimigo in outros_inimigos:
                        if outro_inimigo != self and self.rect.colliderect(outro_inimigo.rect):
                            if hasattr(self, '_resolver_colisao_com_outro_inimigo'): 
                                self._resolver_colisao_com_outro_inimigo(outro_inimigo)
                            break 

                current_ticks = pygame.time.get_ticks()
                if hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                   self.rect.colliderect(player.rect) and \
                   (current_ticks - self.last_contact_time >= self.contact_cooldown):
                    if hasattr(player, 'receber_dano'):
                        player.receber_dano(self.contact_damage)
                        self.last_contact_time = current_ticks

        def desenhar(self, janela, camera_x, camera_y):
            if not hasattr(self, 'image') or self.image is None or not isinstance(self.image, pygame.Surface):
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (34,139,34), (0,0,self.largura,self.altura))
                if not hasattr(self, 'rect'): self.rect = self.image.get_rect(topleft=(self.x,self.y))

            screen_x = self.rect.x - camera_x
            screen_y = self.rect.y - camera_y
            janela.blit(self.image, (screen_x, screen_y))

            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time < self.hit_flash_duration and hasattr(self, 'image') and self.image:
                flash_overlay = self.image.copy()
                flash_overlay.fill(self.hit_flash_color[:3] + (0,), special_flags=pygame.BLEND_RGB_ADD) 
                flash_overlay.set_alpha(self.hit_flash_color[3]) 
                janela.blit(flash_overlay, (screen_x, screen_y))

            if self.hp < self.max_hp and self.hp > 0:
                bar_width = self.largura
                bar_height = 7 # Barra de vida um pouco maior para Mae Natureza
                health_percentage = self.hp / self.max_hp
                current_bar_width = int(bar_width * health_percentage)
                bar_x = screen_x
                bar_y = screen_y - bar_height - 7 
                pygame.draw.rect(janela, (139,0,0), (bar_x, bar_y, bar_width, bar_height), border_radius=3) # Fundo vermelho escuro
                pygame.draw.rect(janela, (34,139,34), (bar_x, bar_y, current_bar_width, bar_height), border_radius=3) # Vida verde floresta
                pygame.draw.rect(janela, (220,220,200), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=3) # Borda


class Mae_Natureza(Inimigo):
    sprites_andar_carregados = None # Para animação de andar/idle
    sprites_atacar_carregados = None # Para animação de ataque, se houver
    tamanho_sprite_definido = (150, 150)

    # Sons
    som_ataque_mae = None
    som_dano_mae = None
    som_morte_mae = None
    sons_carregados = False

    @staticmethod
    def _carregar_som_mae_natureza(caminho_relativo):
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_file_dir)
        full_path = os.path.join(project_root, caminho_relativo.replace("\\", "/"))
        if not os.path.exists(full_path):
            print(f"DEBUG(Mae_Natureza): Arquivo de som não encontrado: {full_path}")
            return None
        try:
            return pygame.mixer.Sound(full_path)
        except pygame.error as e:
            print(f"DEBUG(Mae_Natureza): Erro ao carregar som '{full_path}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho, tipo_animacao):
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        game_root_dir = os.path.dirname(current_file_dir)
        
        print(f"--- Carregando sprites de {tipo_animacao} para Mae_Natureza. Raiz para assets: {game_root_dir} ---")
        for path_relativo in caminhos:
            path_corrigido = path_relativo.replace("\\", "/")
            full_path = os.path.join(game_root_dir, path_corrigido)
            print(f"--- TENTANDO CARREGAR MAE_NATUREZA SPRITE ({tipo_animacao}): {full_path}")
            try:
                if os.path.exists(full_path):
                    sprite = pygame.image.load(full_path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                    print(f"--- SUCESSO: Sprite '{full_path}' carregado.")
                else:
                    print(f"!!! ARQUIVO NÃO EXISTE (Mae_Natureza - {tipo_animacao}): {full_path}. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (34,139,34), placeholder.get_rect()) # Verde floresta
                    lista_destino.append(placeholder)
            except pygame.error as e:
                print(f"!!! ERRO PYGAME (Mae_Natureza - {tipo_animacao}) ao carregar '{full_path}': {e}. Usando placeholder.")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (34,139,34), placeholder.get_rect())
                lista_destino.append(placeholder)
        
        if not lista_destino:
            print(f"!!! FALHA TOTAL (Mae_Natureza - {tipo_animacao}): Nenhum sprite carregado. Usando placeholder final.")
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (20,100,20), placeholder.get_rect()) # Verde mais escuro
            lista_destino.append(placeholder)

    @staticmethod
    def carregar_recursos_mae_natureza():
        """Carrega todos os recursos estáticos da Mãe Natureza."""
        if Mae_Natureza.sprites_andar_carregados is None:
            caminhos_andar = [
                "Sprites/Inimigos/Mae_Natureza/Mae1.png", 
                "Sprites/Inimigos/Mae_Natureza/Mae2.png",
                "Sprites/Inimigos/Mae_Natureza/Mae3.png",
                # Adicione mais frames se tiver
            ]
            Mae_Natureza.sprites_andar_carregados = []
            Mae_Natureza._carregar_lista_sprites_estatico(caminhos_andar, Mae_Natureza.sprites_andar_carregados, Mae_Natureza.tamanho_sprite_definido, "Andar/Idle")

            # Se tiver sprites de ataque separados:
            # caminhos_atacar = ["Sprites/Inimigos/Mae_Natureza/Mae_Atacar1.png", ...]
            # Mae_Natureza.sprites_atacar_carregados = []
            # Mae_Natureza._carregar_lista_sprites_estatico(caminhos_atacar, Mae_Natureza.sprites_atacar_carregados, Mae_Natureza.tamanho_sprite_definido, "Atacar")
            # if not Mae_Natureza.sprites_atacar_carregados and Mae_Natureza.sprites_andar_carregados:
            #     Mae_Natureza.sprites_atacar_carregados = [Mae_Natureza.sprites_andar_carregados[0]]

        if not Mae_Natureza.sons_carregados:
            # Mae_Natureza.som_ataque_mae = Mae_Natureza._carregar_som_mae_natureza("Sons/Mae_Natureza/ataque_raizes.wav")
            # Mae_Natureza.som_dano_mae = Mae_Natureza._carregar_som_mae_natureza("Sons/Mae_Natureza/dano_folhas.wav")
            # Mae_Natureza.som_morte_mae = Mae_Natureza._carregar_som_mae_natureza("Sons/Mae_Natureza/morte_terra.wav")
            Mae_Natureza.sons_carregados = True


    def __init__(self, x, y, velocidade=0.8): 
        Mae_Natureza.carregar_recursos_mae_natureza()
        # print(f"DEBUG(Mae_Natureza): Inicializando em ({x}, {y}) com velocidade {velocidade}.")

        mae_natureza_hp = 200 
        mae_natureza_contact_damage = 10 
        mae_natureza_xp_value = 100 
        sprite_path_principal = "Sprites/Inimigos/Mae_Natureza/Mae1.png"

        super().__init__(x, y, 
                         Mae_Natureza.tamanho_sprite_definido[0], Mae_Natureza.tamanho_sprite_definido[1], 
                         mae_natureza_hp, velocidade, mae_natureza_contact_damage, 
                         mae_natureza_xp_value, sprite_path_principal)

        self.sprites = Mae_Natureza.sprites_andar_carregados 
        if not self.sprites: 
             placeholder_img = pygame.Surface(Mae_Natureza.tamanho_sprite_definido, pygame.SRCALPHA)
             pygame.draw.rect(placeholder_img, (34,139,34), placeholder_img.get_rect())
             self.sprites = [placeholder_img]
        
        self.sprite_index = 0 
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() 
        self.intervalo_animacao_andar = 280 # Animação mais lenta para um ser imponente
        # self.intervalo_animacao_atacar = 200 
        self.intervalo_animacao = self.intervalo_animacao_andar

        self.is_attacking = False 
        self.attack_duration = 1.5 
        self.attack_timer = 0.0 
        self.attack_damage = 25 
        self.attack_hitbox_size = (120, 120) # Área de efeito maior
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) 
        self.attack_range = 160 # Alcance maior para ataques de área
        self.attack_cooldown = 4.0 
        self.last_attack_time = time.time() - self.attack_cooldown
        
        if self.sprites and len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface):
            self.image = self.sprites[0]
        elif hasattr(super(), 'image') and isinstance(super().image, pygame.Surface):
            self.image = super().image
        else:
            self.image = pygame.Surface(Mae_Natureza.tamanho_sprite_definido, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (34,139,34), self.image.get_rect())
        
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        # print(f"DEBUG(Mae_Natureza): Inicializada. HP: {self.hp}, Vel: {self.velocidade}")

    def receber_dano(self, dano, fonte_dano_rect=None):
        super().receber_dano(dano) 
        # if Mae_Natureza.som_dano_mae: Mae_Natureza.som_dano_mae.play()
        # if not self.esta_vivo() and Mae_Natureza.som_morte_mae: Mae_Natureza.som_morte_mae.play()

    def atualizar_animacao(self):
        # if self.is_attacking and Mae_Natureza.sprites_atacar_carregados:
        #     self.sprites = Mae_Natureza.sprites_atacar_carregados
        #     self.intervalo_animacao = self.intervalo_animacao_atacar
        # elif Mae_Natureza.sprites_andar_carregados:
        #     self.sprites = Mae_Natureza.sprites_andar_carregados
        #     self.intervalo_animacao = self.intervalo_animacao_andar
        super().atualizar_animacao()

    def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None):
        if not self.is_attacking: # Mãe Natureza pode parar para conjurar ataques
            super().mover_em_direcao(alvo_x, alvo_y, dt_ms)

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
                # print(f"DEBUG(Mae_Natureza): Iniciando ataque! Dist: {distancia_ao_jogador:.0f}")

                # if Mae_Natureza.sprites_atacar_carregados:
                #     self.sprites = Mae_Natureza.sprites_atacar_carregados
                #     self.intervalo_animacao = self.intervalo_animacao_atacar
                #     self.sprite_index = 0
                # if Mae_Natureza.som_ataque_mae: Mae_Natureza.som_ataque_mae.play()
                
                attack_hitbox_width, attack_hitbox_height = self.attack_hitbox_size
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                self.attack_hitbox.center = self.rect.center # Ataque de área centrado nela


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            if self.esta_vivo(): self.atualizar_animacao()
            return

        if not self.is_attacking:
            try:
                super().update(player, outros_inimigos, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)
            except TypeError: 
                try:
                    super().update(player, outros_inimigos, projeteis_inimigos_ref, tela_largura, altura_tela)
                except TypeError: 
                    super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)
        else:
            self.atualizar_animacao() 

        if self.esta_vivo():
            current_time_ataque = time.time() 

            if self.is_attacking:
                self.attack_hitbox.center = self.rect.center 

                if current_time_ataque - self.attack_timer >= self.attack_duration:
                    self.is_attacking = False
                    self.hit_by_player_this_attack = False 
                    # if Mae_Natureza.sprites_andar_carregados: 
                    #     self.sprites = Mae_Natureza.sprites_andar_carregados
                    #     self.intervalo_animacao = self.intervalo_animacao_andar
                    #     self.sprite_index = 0
                else:
                    if not self.hit_by_player_this_attack and \
                       hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0 and \
                       self.attack_hitbox.colliderect(player.rect):
                        if player.vida.esta_vivo(): 
                            player.receber_dano(self.attack_damage)
                            self.hit_by_player_this_attack = True
                            # print(f"DEBUG(Mae_Natureza): Ataque acertou o jogador! Dano: {self.attack_damage}")
            
            if not self.is_attacking:
                # if self.sprites != Mae_Natureza.sprites_andar_carregados and Mae_Natureza.sprites_andar_carregados:
                #     self.sprites = Mae_Natureza.sprites_andar_carregados
                #     self.intervalo_animacao = self.intervalo_animacao_andar
                #     self.sprite_index = 0
                self.atacar(player)
        

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y) 
        # Opcional: Desenhar a hitbox de ataque para debug
        # if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0:
        #     debug_hitbox_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
        #     s = pygame.Surface((self.attack_hitbox.width, self.attack_hitbox.height), pygame.SRCALPHA)
        #     s.fill((34, 139, 34, 100)) # Verde para hitbox
        #     surface.blit(s, (debug_hitbox_rect_onscreen.x, debug_hitbox_rect_onscreen.y))
