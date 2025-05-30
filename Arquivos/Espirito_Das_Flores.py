# Espirito_Das_Flores.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()
import os # Importa os para verificar a existência de arquivos

# Importa a classe base Inimigo do ficheiro Inimigos.py
try:
    from Inimigos import Inimigo # Tenta importar a classe base real
    print("DEBUG(Espirito_Das_Flores): Classe base Inimigo importada com sucesso.")
except ImportError:
    print("DEBUG(Espirito_Das_Flores): ERRO: Módulo 'Inimigos.py' ou classe 'Inimigo' NÃO encontrado. Usando classe Inimigo placeholder.")
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
            base_dir = os.path.dirname(os.path.abspath(__file__)) # Diretório do script atual (Espirito_Das_Flores.py)
            # Assumindo que a pasta 'Sprites' está um nível ACIMA do diretório deste script
            game_root_dir = os.path.dirname(base_dir) 
            # Se este script e a pasta 'Sprites' estiverem na mesma pasta (raiz do projeto):
            # game_root_dir = base_dir
            
            full_path = os.path.join(game_root_dir, path.replace("\\", "/"))
            # print(f"--- DEBUG PLACEHOLDER TENTANDO CARREGAR (Espirito_Das_Flores): {full_path}")

            if not os.path.exists(full_path):
                print(f"DEBUG(InimigoPlaceholder - Espirito_Das_Flores): Sprite não encontrado: {full_path}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (255,105,180), (0, 0, tamanho[0], tamanho[1])) # Cor rosa para placeholder
                return img
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.scale(img, tamanho)
                return img
            except pygame.error as e:
                print(f"DEBUG(InimigoPlaceholder - Espirito_Das_Flores): Erro ao carregar sprite '{full_path}': {e}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (255,105,180), (0, 0, tamanho[0], tamanho[1]))
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
                pygame.draw.rect(self.image, (255,105,180), (0,0,self.largura,self.altura))


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
                pygame.draw.rect(self.image, (255,105,180), (0,0,self.largura,self.altura))
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
                bar_height = 5
                health_percentage = self.hp / self.max_hp
                current_bar_width = int(bar_width * health_percentage)
                bar_x = screen_x
                bar_y = screen_y - bar_height - 5 
                pygame.draw.rect(janela, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=2)
                pygame.draw.rect(janela, (0, 255, 0), (bar_x, bar_y, current_bar_width, bar_height), border_radius=2)
                pygame.draw.rect(janela, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=2)


class Espirito_Das_Flores(Inimigo):
    sprites_andar_carregados = None # Para animação de andar/idle
    sprites_atacar_carregados = None # Para animação de ataque, se houver
    tamanho_sprite_definido = (70, 70)

    # Sons
    som_ataque_espirito = None
    som_dano_espirito = None
    som_morte_espirito = None
    sons_carregados = False # Flag para sons do Espirito_Das_Flores

    @staticmethod
    def _carregar_som_espirito(caminho_relativo):
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        # Assumindo que Espirito_Das_Flores.py está numa subpasta e 'Sons' na raiz
        project_root = os.path.dirname(current_file_dir)
        # Se Espirito_Das_Flores.py e 'Sons' estiverem na mesma pasta:
        # project_root = current_file_dir
        
        full_path = os.path.join(project_root, caminho_relativo.replace("\\", "/"))
        if not os.path.exists(full_path):
            print(f"DEBUG(Espirito_Das_Flores): Arquivo de som não encontrado: {full_path}")
            return None
        try:
            som = pygame.mixer.Sound(full_path)
            return som
        except pygame.error as e:
            print(f"DEBUG(Espirito_Das_Flores): Erro ao carregar som '{full_path}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho, tipo_animacao):
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        # Assumindo que Espirito_Das_Flores.py está numa subpasta e 'Sprites' na raiz
        game_root_dir = os.path.dirname(current_file_dir)
        # Se Espirito_Das_Flores.py e 'Sprites' estiverem na mesma pasta:
        # game_root_dir = current_file_dir
        
        print(f"--- Carregando sprites de {tipo_animacao} para Espirito_Das_Flores. Raiz para assets: {game_root_dir} ---")
        for path_relativo in caminhos:
            path_corrigido = path_relativo.replace("\\", "/")
            full_path = os.path.join(game_root_dir, path_corrigido)
            print(f"--- TENTANDO CARREGAR ESPIRITO_FLORES SPRITE ({tipo_animacao}): {full_path}")
            try:
                if os.path.exists(full_path):
                    sprite = pygame.image.load(full_path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                    print(f"--- SUCESSO: Sprite '{full_path}' carregado.")
                else:
                    print(f"!!! ARQUIVO NÃO EXISTE (Espirito_Das_Flores - {tipo_animacao}): {full_path}. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (255, 105, 180), placeholder.get_rect()) # Cor rosa
                    lista_destino.append(placeholder)
            except pygame.error as e:
                print(f"!!! ERRO PYGAME (Espirito_Das_Flores - {tipo_animacao}) ao carregar '{full_path}': {e}. Usando placeholder.")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255, 105, 180), placeholder.get_rect())
                lista_destino.append(placeholder)
        
        if not lista_destino:
            print(f"!!! FALHA TOTAL (Espirito_Das_Flores - {tipo_animacao}): Nenhum sprite carregado. Usando placeholder final.")
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (200, 80, 150), placeholder.get_rect()) # Rosa mais escuro
            lista_destino.append(placeholder)

    @staticmethod
    def carregar_recursos_espirito(): # Renomeado para clareza
        """Carrega todos os recursos estáticos do Espírito das Flores."""
        if Espirito_Das_Flores.sprites_andar_carregados is None:
            caminhos_andar = [
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores1.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores2.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores3.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores4.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores5.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores6.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores7.png",
            ]
            Espirito_Das_Flores.sprites_andar_carregados = []
            Espirito_Das_Flores._carregar_lista_sprites_estatico(caminhos_andar, Espirito_Das_Flores.sprites_andar_carregados, Espirito_Das_Flores.tamanho_sprite_definido, "Andar/Idle")

            # Se tiver sprites de ataque separados:
            # caminhos_atacar = ["Sprites/Inimigos/Espirito_Flores/Espirito_Atacar1.png", ...]
            # Espirito_Das_Flores.sprites_atacar_carregados = []
            # Espirito_Das_Flores._carregar_lista_sprites_estatico(caminhos_atacar, Espirito_Das_Flores.sprites_atacar_carregados, Espirito_Das_Flores.tamanho_sprite_definido, "Atacar")
            # if not Espirito_Das_Flores.sprites_atacar_carregados and Espirito_Das_Flores.sprites_andar_carregados:
            #     Espirito_Das_Flores.sprites_atacar_carregados = [Espirito_Das_Flores.sprites_andar_carregados[0]]


        if not Espirito_Das_Flores.sons_carregados:
            # Espirito_Das_Flores.som_ataque_espirito = Espirito_Das_Flores._carregar_som_espirito("Sons/Espirito_Flores/ataque.wav")
            # Espirito_Das_Flores.som_dano_espirito = Espirito_Das_Flores._carregar_som_espirito("Sons/Espirito_Flores/dano.wav")
            # Espirito_Das_Flores.som_morte_espirito = Espirito_Das_Flores._carregar_som_espirito("Sons/Espirito_Flores/morte.wav")
            Espirito_Das_Flores.sons_carregados = True


    def __init__(self, x, y, velocidade=1.8): 
        Espirito_Das_Flores.carregar_recursos_espirito() # Chama o carregamento de recursos
        # print(f"DEBUG(Espirito_Das_Flores): Inicializando em ({x}, {y}) com velocidade {velocidade}.")

        espirito_hp = 75 
        espirito_contact_damage = 8 
        espirito_xp_value = 40 
        sprite_path_principal = "Sprites/Inimigos/Espirito_Flores/Espirito_Flores1.png" 

        super().__init__(x, y, 
                         Espirito_Das_Flores.tamanho_sprite_definido[0], Espirito_Das_Flores.tamanho_sprite_definido[1], 
                         espirito_hp, velocidade, espirito_contact_damage,
                         espirito_xp_value, sprite_path_principal)

        self.sprites = Espirito_Das_Flores.sprites_andar_carregados 
        if not self.sprites: # Fallback extremo
             placeholder_img = pygame.Surface(Espirito_Das_Flores.tamanho_sprite_definido, pygame.SRCALPHA)
             pygame.draw.rect(placeholder_img, (255,105,180), placeholder_img.get_rect())
             self.sprites = [placeholder_img]
        
        self.sprite_index = 0 
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() 
        self.intervalo_animacao_andar = 180 
        # self.intervalo_animacao_atacar = 120 # Se tiver animação de ataque
        self.intervalo_animacao = self.intervalo_animacao_andar

        self.is_attacking = False 
        self.attack_duration = 0.6 
        self.attack_timer = 0.0 
        self.attack_damage = 12 
        self.attack_hitbox_size = (50, 50) 
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) 
        self.attack_range = 70 
        self.attack_cooldown = 2.5 
        self.last_attack_time = time.time() - self.attack_cooldown 
        
        if self.sprites and len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface):
            self.image = self.sprites[0]
        elif hasattr(super(), 'image') and isinstance(super().image, pygame.Surface):
            self.image = super().image
        else:
            self.image = pygame.Surface(Espirito_Das_Flores.tamanho_sprite_definido, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255,105,180), self.image.get_rect())
        
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        # print(f"DEBUG(Espirito_Das_Flores): Inicializado. HP: {self.hp}, Vel: {self.velocidade}")

    def receber_dano(self, dano, fonte_dano_rect=None):
        super().receber_dano(dano) 
        # if Espirito_Das_Flores.som_dano_espirito: Espirito_Das_Flores.som_dano_espirito.play()
        # if not self.esta_vivo() and Espirito_Das_Flores.som_morte_espirito: Espirito_Das_Flores.som_morte_espirito.play()

    def atualizar_animacao(self):
        # if self.is_attacking and Espirito_Das_Flores.sprites_atacar_carregados:
        #     self.sprites = Espirito_Das_Flores.sprites_atacar_carregados
        #     self.intervalo_animacao = self.intervalo_animacao_atacar
        # elif Espirito_Das_Flores.sprites_andar_carregados:
        #     self.sprites = Espirito_Das_Flores.sprites_andar_carregados
        #     self.intervalo_animacao = self.intervalo_animacao_andar
        super().atualizar_animacao()

    def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None):
        # O Espírito das Flores pode ter um movimento mais flutuante ou errático.
        # Por enquanto, usa o da classe base.
        if not self.is_attacking: # Pode parar para atacar
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
                # print(f"DEBUG(Espirito_Das_Flores): Iniciando ataque! Dist: {distancia_ao_jogador:.0f}")
                
                # if Espirito_Das_Flores.sprites_atacar_carregados:
                #     self.sprites = Espirito_Das_Flores.sprites_atacar_carregados
                #     self.intervalo_animacao = self.intervalo_animacao_atacar
                #     self.sprite_index = 0
                # if Espirito_Das_Flores.som_ataque_espirito: Espirito_Das_Flores.som_ataque_espirito.play()
                
                attack_hitbox_width, attack_hitbox_height = self.attack_hitbox_size
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                self.attack_hitbox.center = self.rect.center # Ataque pode ser um pulso ao redor


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
                except TypeError: # Fallback se a classe base Inimigo não aceitar 'outros_inimigos'
                    super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)

        else:
            self.atualizar_animacao() # Só anima se estiver atacando (e não se move)

        if self.esta_vivo():
            current_time_ataque = time.time()

            if self.is_attacking:
                self.attack_hitbox.center = self.rect.center 

                if current_time_ataque - self.attack_timer >= self.attack_duration:
                    self.is_attacking = False
                    self.hit_by_player_this_attack = False 
                    # if Espirito_Das_Flores.sprites_andar_carregados: 
                    #     self.sprites = Espirito_Das_Flores.sprites_andar_carregados
                    #     self.intervalo_animacao = self.intervalo_animacao_andar
                    #     self.sprite_index = 0
                else:
                    if not self.hit_by_player_this_attack and \
                       hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0 and \
                       self.attack_hitbox.colliderect(player.rect):
                        if player.vida.esta_vivo(): 
                            player.receber_dano(self.attack_damage)
                            self.hit_by_player_this_attack = True 
                            # print(f"DEBUG(Espirito_Das_Flores): Ataque acertou o jogador! Dano: {self.attack_damage}")
            
            if not self.is_attacking:
                # if self.sprites != Espirito_Das_Flores.sprites_andar_carregados and Espirito_Das_Flores.sprites_andar_carregados:
                #     self.sprites = Espirito_Das_Flores.sprites_andar_carregados
                #     self.intervalo_animacao = self.intervalo_animacao_andar
                #     self.sprite_index = 0
                self.atacar(player)
        

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y) 
        # Opcional: Desenhar a hitbox de ataque para debug
        # if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0:
        #     debug_hitbox_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
        #     s = pygame.Surface((self.attack_hitbox.width, self.attack_hitbox.height), pygame.SRCALPHA)
        #     s.fill((255, 182, 193, 100)) # Rosa para hitbox
        #     surface.blit(s, (debug_hitbox_rect_onscreen.x, debug_hitbox_rect_onscreen.y))
