# Fenix.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()
import os # Importa os para verificar a existência de arquivos

# Certifique-se de que Inimigo está acessível
try:
    from Inimigos import Inimigo # Tenta importar a classe base real
    print("DEBUG(Fenix): Classe base Inimigo importada com sucesso.")
except ImportError:
    print("DEBUG(Fenix): ERRO: Módulo 'Inimigos.py' não encontrado. Usando classe Inimigo placeholder.")
    # Placeholder para Inimigo, caso Inimigos.py não seja encontrado
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
            # Assumindo que a pasta 'Sprites' está um nível ACIMA do diretório deste script
            game_root_dir = os.path.dirname(base_dir) 
            # Se este script e a pasta 'Sprites' estiverem na mesma pasta (raiz do projeto):
            # game_root_dir = base_dir
            
            full_path = os.path.join(game_root_dir, path.replace("\\", "/"))
            # print(f"--- DEBUG PLACEHOLDER TENTANDO CARREGAR (Fenix): {full_path}")

            if not os.path.exists(full_path):
                print(f"DEBUG(InimigoPlaceholder - Fenix): Sprite não encontrado: {full_path}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (255,165,0), (0, 0, tamanho[0], tamanho[1])) # Cor laranja para placeholder
                return img
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.scale(img, tamanho)
                return img
            except pygame.error as e:
                print(f"DEBUG(InimigoPlaceholder - Fenix): Erro ao carregar sprite '{full_path}': {e}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (255,165,0), (0, 0, tamanho[0], tamanho[1]))
                return img

        def receber_dano(self, dano, fonte_dano_rect=None): # Adicionado fonte_dano_rect
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
                pygame.draw.rect(self.image, (255,165,0), (0,0,self.largura,self.altura))


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
                pygame.draw.rect(self.image, (255,165,0), (0,0,self.largura,self.altura))
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


class Fenix(Inimigo): 
    sprites_andar_carregados = None # Para animação de voo/idle
    sprites_atacar_carregados = None # Para animação de ataque, se houver
    tamanho_sprite_definido = (90, 90) 

    # Sons
    som_ataque_fenix = None
    som_dano_fenix = None
    som_morte_fenix = None
    som_voo_fenix = None # Som de voo em loop
    sons_carregados = False

    @staticmethod
    def _carregar_som_fenix(caminho_relativo):
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_file_dir) # Assume que Fenix.py está em subpasta
        full_path = os.path.join(project_root, caminho_relativo.replace("\\", "/"))
        if not os.path.exists(full_path):
            print(f"DEBUG(Fenix): Arquivo de som não encontrado: {full_path}")
            return None
        try:
            return pygame.mixer.Sound(full_path)
        except pygame.error as e:
            print(f"DEBUG(Fenix): Erro ao carregar som '{full_path}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho, tipo_animacao):
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        game_root_dir = os.path.dirname(current_file_dir) # Assume que Fenix.py está em subpasta
        
        # print(f"--- Carregando sprites de {tipo_animacao} para Fenix. Raiz para assets: {game_root_dir} ---")
        for path_relativo in caminhos:
            path_corrigido = path_relativo.replace("\\", "/")
            full_path = os.path.join(game_root_dir, path_corrigido)
            # print(f"--- TENTANDO CARREGAR FENIX SPRITE ({tipo_animacao}): {full_path}")
            try:
                if os.path.exists(full_path):
                    sprite = pygame.image.load(full_path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                    # print(f"--- SUCESSO: Sprite '{full_path}' carregado.")
                else:
                    print(f"!!! ARQUIVO NÃO EXISTE (Fenix - {tipo_animacao}): {full_path}. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (255,165,0), placeholder.get_rect()) # Laranja para Fenix
                    lista_destino.append(placeholder)
            except pygame.error as e:
                print(f"!!! ERRO PYGAME (Fenix - {tipo_animacao}) ao carregar '{full_path}': {e}. Usando placeholder.")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255,165,0), placeholder.get_rect())
                lista_destino.append(placeholder)
        
        if not lista_destino:
            print(f"!!! FALHA TOTAL (Fenix - {tipo_animacao}): Nenhum sprite carregado. Usando placeholder final.")
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (200,100,0), placeholder.get_rect()) # Laranja escuro
            lista_destino.append(placeholder)

    @staticmethod
    def carregar_recursos_fenix():
        """Carrega todos os recursos estáticos da Fênix."""
        if Fenix.sprites_andar_carregados is None: # Usando sprites_andar_carregados como flag
            caminhos_voo = [
                "Sprites/Inimigos/Fenix/Fenix 1.png", 
                "Sprites/Inimigos/Fenix/Fenix 2.png",
                "Sprites/Inimigos/Fenix/Fenix 3.png",
                "Sprites/Inimigos/Fenix/Fenix 4.png",
            ]
            Fenix.sprites_andar_carregados = [] # Usado para animação de voo/idle
            Fenix._carregar_lista_sprites_estatico(caminhos_voo, Fenix.sprites_andar_carregados, Fenix.tamanho_sprite_definido, "Voo/Idle")

            # Se tiver sprites de ataque separados (ex: baforada de fogo)
            # caminhos_atacar = ["Sprites/Inimigos/Fenix/Fenix_Atacar1.png", ...]
            # Fenix.sprites_atacar_carregados = []
            # Fenix._carregar_lista_sprites_estatico(caminhos_atacar, Fenix.sprites_atacar_carregados, Fenix.tamanho_sprite_definido, "Atacar")
            # if not Fenix.sprites_atacar_carregados and Fenix.sprites_andar_carregados:
            #     Fenix.sprites_atacar_carregados = [Fenix.sprites_andar_carregados[0]]


        if not Fenix.sons_carregados:
            Fenix.som_ataque_fenix = Fenix._carregar_som_fenix("Sons/Fenix/ataque_fogo.wav") # CRIE ESTES ARQUIVOS
            Fenix.som_dano_fenix = Fenix._carregar_som_fenix("Sons/Fenix/dano_grito.wav")
            Fenix.som_morte_fenix = Fenix._carregar_som_fenix("Sons/Fenix/morte_cinzas.wav")
            Fenix.som_voo_fenix = Fenix._carregar_som_fenix("Sons/Fenix/voo_loop.wav") 
            Fenix.sons_carregados = True


    def __init__(self, x, y, velocidade=3.0): 
        Fenix.carregar_recursos_fenix()
        # print(f"DEBUG(Fenix): Inicializando Fenix em ({x}, {y}) com velocidade {velocidade}.")

        fenix_hp = 70 
        fenix_contact_damage = 5 
        fenix_xp_value = 50 
        sprite_path_principal = "Sprites/Inimigos/Fenix/Fenix 1.png" 

        super().__init__(x, y, 
                         Fenix.tamanho_sprite_definido[0], Fenix.tamanho_sprite_definido[1], 
                         fenix_hp, velocidade, fenix_contact_damage, 
                         fenix_xp_value, sprite_path_principal)

        self.sprites = Fenix.sprites_andar_carregados 
        if not self.sprites: 
             placeholder_img = pygame.Surface(Fenix.tamanho_sprite_definido, pygame.SRCALPHA)
             pygame.draw.rect(placeholder_img, (255,165,0), placeholder_img.get_rect())
             self.sprites = [placeholder_img]
        
        self.sprite_index = 0 
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() 
        self.intervalo_animacao_voo = 100 
        # self.intervalo_animacao_atacar = 80 # Se tiver animação de ataque
        self.intervalo_animacao = self.intervalo_animacao_voo

        self.is_attacking = False 
        self.attack_duration = 0.5 
        self.attack_timer = 0.0 
        self.attack_damage = 15 
        self.attack_hitbox_size = (self.largura, self.altura / 2) # Ex: baforada de fogo à frente
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) 
        self.attack_range = 120 # Alcance maior para ataque à distância
        self.attack_cooldown = 2.0 
        self.last_attack_time = time.time() - self.attack_cooldown 

        self.canal_voo = None # Para o som de voo em loop
        if Fenix.som_voo_fenix:
            try:
                self.canal_voo = pygame.mixer.find_channel(True) 
                if self.canal_voo:
                    self.canal_voo.play(Fenix.som_voo_fenix, loops=-1) 
            except pygame.error as e:
                print(f"DEBUG(Fenix): Não foi possível tocar som de voo: {e}")
                self.canal_voo = None
        
        if self.sprites and len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface):
            self.image = self.sprites[0]
        elif hasattr(super(), 'image') and isinstance(super().image, pygame.Surface):
            self.image = super().image
        else:
            self.image = pygame.Surface(Fenix.tamanho_sprite_definido, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255,165,0), self.image.get_rect())
        
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        # print(f"DEBUG(Fenix): Fenix inicializada. HP: {self.hp}, Vel: {self.velocidade}")

    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano) 
        if self.esta_vivo():
            if vida_antes > self.hp and Fenix.som_dano_fenix:
                Fenix.som_dano_fenix.play()
        elif vida_antes > 0: # Morreu e estava viva antes
            if Fenix.som_morte_fenix:
                Fenix.som_morte_fenix.play()
            if self.canal_voo: # Para o som de voo ao morrer
                self.canal_voo.stop()
                self.canal_voo = None # Libera o canal

    def atualizar_animacao(self):
        # if self.is_attacking and Fenix.sprites_atacar_carregados:
        #     self.sprites = Fenix.sprites_atacar_carregados
        #     self.intervalo_animacao = self.intervalo_animacao_atacar
        # elif Fenix.sprites_andar_carregados: # Renomeado para sprites_andar_carregados
        #     self.sprites = Fenix.sprites_andar_carregados
        #     self.intervalo_animacao = self.intervalo_animacao_voo
        super().atualizar_animacao()

    def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None):
        if not self.is_attacking: # Fênix pode parar para lançar ataque de fogo
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
                
                # if Fenix.sprites_atacar_carregados:
                #     self.sprites = Fenix.sprites_atacar_carregados
                #     self.intervalo_animacao = self.intervalo_animacao_atacar
                #     self.sprite_index = 0
                if Fenix.som_ataque_fenix:
                    Fenix.som_ataque_fenix.play()
                
                # Define a hitbox de ataque (ex: baforada de fogo)
                # A posição exata dependerá da direção da Fênix e da animação
                atk_w, atk_h = self.attack_hitbox_size
                if self.facing_right:
                    # Hitbox à direita da Fênix
                    self.attack_hitbox = pygame.Rect(self.rect.right, self.rect.centery - atk_h / 2, atk_w, atk_h)
                else:
                    # Hitbox à esquerda da Fênix
                    self.attack_hitbox = pygame.Rect(self.rect.left - atk_w, self.rect.centery - atk_h / 2, atk_w, atk_h)


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
                    super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms) # Tenta com outros_inimigos removido
        else:
            self.atualizar_animacao() # Só anima se estiver atacando

        if self.esta_vivo():
            current_time_ataque = time.time()

            if self.is_attacking:
                # Atualiza a posição da hitbox de ataque se necessário (se o ataque for móvel)
                # Para uma baforada, pode ser fixo em relação à Fênix no momento do ataque
                # A hitbox já foi definida em self.atacar()
                pass # A hitbox é definida em atacar e pode ser atualizada aqui se o ataque for "perseguidor"

                if current_time_ataque - self.attack_timer >= self.attack_duration:
                    self.is_attacking = False
                    self.hit_by_player_this_attack = False 
                    # if Fenix.sprites_andar_carregados: 
                    #     self.sprites = Fenix.sprites_andar_carregados
                    #     self.intervalo_animacao = self.intervalo_animacao_voo
                    #     self.sprite_index = 0
                else:
                    if not self.hit_by_player_this_attack and \
                       hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0 and \
                       self.attack_hitbox.colliderect(player.rect):
                        if player.vida.esta_vivo(): 
                            player.receber_dano(self.attack_damage)
                            self.hit_by_player_this_attack = True 
            
            if not self.is_attacking:
                # if self.sprites != Fenix.sprites_andar_carregados and Fenix.sprites_andar_carregados:
                #     self.sprites = Fenix.sprites_andar_carregados
                #     self.intervalo_animacao = self.intervalo_animacao_voo
                #     self.sprite_index = 0
                self.atacar(player)
        else: # Não está vivo
            if self.canal_voo: # Garante que o som de voo pare se a Fênix morrer por outra razão
                self.canal_voo.stop()
                self.canal_voo = None

    def kill(self): # Sobrescreve kill para parar o som de voo
        if self.canal_voo:
            self.canal_voo.stop()
            self.canal_voo = None
        super().kill() # Chama o kill da classe base Sprite

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y) 
        # Opcional: Desenhar a hitbox de ataque para debug
        # if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0:
        #     debug_hitbox_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
        #     s = pygame.Surface((self.attack_hitbox.width, self.attack_hitbox.height), pygame.SRCALPHA)
        #     s.fill((255, 100, 0, 100)) # Laranja para hitbox da Fênix
        #     surface.blit(s, (debug_hitbox_rect_onscreen.x, debug_hitbox_rect_onscreen.y))

