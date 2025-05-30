# Fantasma.py
import pygame
import random
import math
import time
import os 

# Importa a classe base Inimigo do ficheiro Inimigos.py
try:
    from Inimigos import Inimigo # Tenta importar a classe base real
    print("DEBUG(Fantasma): Classe base Inimigo importada com sucesso.")
except ImportError:
    print("DEBUG(Fantasma): ERRO: Módulo 'Inimigos.py' ou classe 'Inimigo' NÃO encontrado. Usando classe Inimigo placeholder.")
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
            base_dir = os.path.dirname(os.path.abspath(__file__)) # Diretório do script atual (Fantasma.py)
            # Assumindo que a pasta 'Sprites' está um nível ACIMA do diretório deste script
            game_root_dir = os.path.dirname(base_dir) 
            # Se este script e a pasta 'Sprites' estiverem na mesma pasta (raiz do projeto):
            # game_root_dir = base_dir
            
            full_path = os.path.join(game_root_dir, path.replace("\\", "/"))
            # print(f"--- DEBUG PLACEHOLDER TENTANDO CARREGAR (Fantasma): {full_path}")

            if not os.path.exists(full_path):
                print(f"DEBUG(InimigoPlaceholder - Fantasma): Sprite não encontrado: {full_path}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (200,200,255), (0, 0, tamanho[0], tamanho[1])) # Cor azul claro para placeholder
                return img
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.scale(img, tamanho)
                return img
            except pygame.error as e:
                print(f"DEBUG(InimigoPlaceholder - Fantasma): Erro ao carregar sprite '{full_path}': {e}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (200,200,255), (0, 0, tamanho[0], tamanho[1]))
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
                pygame.draw.rect(self.image, (200,200,255), (0,0,self.largura,self.altura))


        def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): 
            if self.esta_vivo():
                if hasattr(player, 'rect'):
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
                self.atualizar_animacao() 
                
                if outros_inimigos: # Lógica de colisão entre inimigos
                    for outro_inimigo in outros_inimigos:
                        if outro_inimigo != self and self.rect.colliderect(outro_inimigo.rect):
                            if hasattr(self, '_resolver_colisao_com_outro_inimigo'): # Se o método existir
                                self._resolver_colisao_com_outro_inimigo(outro_inimigo)
                            break # Resolve uma colisão por frame para evitar instabilidade

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
                pygame.draw.rect(self.image, (200,200,255), (0,0,self.largura,self.altura))
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


class Fantasma(Inimigo):
    sprites_carregados = None # Para animação de andar/flutuar
    # sprites_atacar_carregados = None # Para animação de ataque, se houver
    tamanho_sprite_definido = (60, 80) 

    # Sons
    som_ataque_fantasma = None
    som_dano_fantasma = None
    som_morte_fantasma = None
    sons_carregados = False # Flag para sons do Fantasma

    @staticmethod
    def _carregar_som_fantasma(caminho_relativo):
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        # Assumindo que Fantasma.py está numa subpasta e 'Sons' na raiz
        project_root = os.path.dirname(current_file_dir)
        # Se Fantasma.py e 'Sons' estiverem na mesma pasta:
        # project_root = current_file_dir
        
        full_path = os.path.join(project_root, caminho_relativo.replace("\\", "/"))
        if not os.path.exists(full_path):
            print(f"DEBUG(Fantasma): Arquivo de som não encontrado: {full_path}")
            return None
        try:
            som = pygame.mixer.Sound(full_path)
            return som
        except pygame.error as e:
            print(f"DEBUG(Fantasma): Erro ao carregar som '{full_path}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho, tipo_animacao):
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        # Assumindo que Fantasma.py está numa subpasta e 'Sprites' na raiz
        game_root_dir = os.path.dirname(current_file_dir)
        # Se Fantasma.py e 'Sprites' estiverem na mesma pasta:
        # game_root_dir = current_file_dir
        
        print(f"--- Carregando sprites de {tipo_animacao} para Fantasma. Raiz para assets: {game_root_dir} ---")
        for path_relativo in caminhos:
            path_corrigido = path_relativo.replace("\\", "/")
            full_path = os.path.join(game_root_dir, path_corrigido)
            print(f"--- TENTANDO CARREGAR FANTASMA SPRITE ({tipo_animacao}): {full_path}")
            try:
                if os.path.exists(full_path):
                    sprite = pygame.image.load(full_path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                    print(f"--- SUCESSO: Sprite '{full_path}' carregado.")
                else:
                    print(f"!!! ARQUIVO NÃO EXISTE (Fantasma - {tipo_animacao}): {full_path}. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (200, 200, 255), placeholder.get_rect()) # Azul claro/branco
                    lista_destino.append(placeholder)
            except pygame.error as e:
                print(f"!!! ERRO PYGAME (Fantasma - {tipo_animacao}) ao carregar '{full_path}': {e}. Usando placeholder.")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (200, 200, 255), placeholder.get_rect())
                lista_destino.append(placeholder)
        
        if not lista_destino:
            print(f"!!! FALHA TOTAL (Fantasma - {tipo_animacao}): Nenhum sprite carregado. Usando placeholder final.")
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (180, 180, 230), placeholder.get_rect()) # Azul mais escuro
            lista_destino.append(placeholder)

    @staticmethod
    def carregar_recursos_fantasma():
        """Carrega todos os recursos estáticos do Fantasma."""
        if Fantasma.sprites_carregados is None:
            caminhos_animacao = [
                "Sprites/Inimigos/Fantasma/Fantasma1.png", 
                "Sprites/Inimigos/Fantasma/Fantasma2.png",
                "Sprites/Inimigos/Fantasma/Fantasma3.png",
                "Sprites/Inimigos/Fantasma/Fantasma4.png",
                "Sprites/Inimigos/Fantasma/Fantasma5.png",
                "Sprites/Inimigos/Fantasma/Fantasma6.png",
                "Sprites/Inimigos/Fantasma/Fantasma8.png", # Nota: Pula o 7 no seu original
                "Sprites/Inimigos/Fantasma/Fantasma9.png",
            ]
            Fantasma.sprites_carregados = [] 
            Fantasma._carregar_lista_sprites_estatico(caminhos_animacao, Fantasma.sprites_carregados, Fantasma.tamanho_sprite_definido, "Flutuar")

            # Se tiver sprites de ataque separados:
            # caminhos_atacar = ["Sprites/Inimigos/Fantasma/Fantasma_Atacar1.png", ...]
            # Fantasma.sprites_atacar_carregados = []
            # Fantasma._carregar_lista_sprites_estatico(caminhos_atacar, Fantasma.sprites_atacar_carregados, Fantasma.tamanho_sprite_definido, "Atacar")
            # if not Fantasma.sprites_atacar_carregados and Fantasma.sprites_carregados:
            #     Fantasma.sprites_atacar_carregados = [Fantasma.sprites_carregados[0]]

        if not Fantasma.sons_carregados:
            # Fantasma.som_ataque_fantasma = Fantasma._carregar_som_fantasma("Sons/Fantasma/ataque_sopro.wav")
            # Fantasma.som_dano_fantasma = Fantasma._carregar_som_fantasma("Sons/Fantasma/dano_gemido.wav")
            # Fantasma.som_morte_fantasma = Fantasma._carregar_som_fantasma("Sons/Fantasma/morte_desaparecer.wav")
            Fantasma.sons_carregados = True


    def __init__(self, x, y, velocidade=1.5): 
        Fantasma.carregar_recursos_fantasma()
        # print(f"DEBUG(Fantasma): Inicializando Fantasma em ({x}, {y}) com velocidade {velocidade}.")

        fantasma_vida_maxima = 50
        fantasma_contact_damage = 3 # Dano de contato baixo, pode ter ataque especial
        fantasma_xp_value = 20
        caminho_sprite_principal_fantasma = "Sprites/Inimigos/Fantasma/Fantasma1.png" 

        super().__init__(x, y, 
                         Fantasma.tamanho_sprite_definido[0], Fantasma.tamanho_sprite_definido[1], 
                         fantasma_vida_maxima, 
                         velocidade, 
                         fantasma_contact_damage, 
                         fantasma_xp_value, 
                         caminho_sprite_principal_fantasma)

        self.sprites = Fantasma.sprites_carregados 
        if not self.sprites: # Fallback extremo
             placeholder_img = pygame.Surface(Fantasma.tamanho_sprite_definido, pygame.SRCALPHA)
             pygame.draw.rect(placeholder_img, (200,200,255), placeholder_img.get_rect())
             self.sprites = [placeholder_img]
        
        self.sprite_index = 0 
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() 
        self.intervalo_animacao_flutuar = 150 
        # self.intervalo_animacao_atacar = 100 # Se tiver animação de ataque
        self.intervalo_animacao = self.intervalo_animacao_flutuar

        self.is_attacking = False 
        self.attack_duration = 0.8 
        self.attack_timer = 0.0 
        self.attack_damage = 10 # Dano do ataque especial do Fantasma
        self.attack_range = 80 
        self.attack_cooldown = 3.0 
        self.last_attack_time = time.time() - self.attack_cooldown 
        self.attack_hitbox_size = (40, 40) # Ajustar conforme o ataque
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.hit_by_player_this_attack = False

        if self.sprites and len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface):
            self.image = self.sprites[0]
        elif hasattr(super(), 'image') and isinstance(super().image, pygame.Surface):
            self.image = super().image
        else:
            self.image = pygame.Surface(Fantasma.tamanho_sprite_definido, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (200,200,255), self.image.get_rect())
        
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        # print(f"DEBUG(Fantasma): Fantasma inicializado. HP: {self.hp}, Vel: {self.velocidade}")

    def receber_dano(self, dano, fonte_dano_rect=None):
        super().receber_dano(dano) 
        # if Fantasma.som_dano_fantasma: Fantasma.som_dano_fantasma.play()
        # if not self.esta_vivo() and Fantasma.som_morte_fantasma: Fantasma.som_morte_fantasma.play()

    def atualizar_animacao(self):
        # if self.is_attacking and Fantasma.sprites_atacar_carregados:
        #     self.sprites = Fantasma.sprites_atacar_carregados
        #     self.intervalo_animacao = self.intervalo_animacao_atacar
        # elif Fantasma.sprites_carregados:
        #     self.sprites = Fantasma.sprites_carregados
        #     self.intervalo_animacao = self.intervalo_animacao_flutuar
        super().atualizar_animacao() 

    def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None):
        # Fantasmas podem ter movimento mais suave ou atravessar obstáculos (não implementado aqui)
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
                # print(f"DEBUG(Fantasma): Iniciando ataque! Dist: {distancia_ao_jogador:.0f}")
                
                # if Fantasma.sprites_atacar_carregados:
                #     self.sprites = Fantasma.sprites_atacar_carregados
                #     self.intervalo_animacao = self.intervalo_animacao_atacar
                #     self.sprite_index = 0
                # if Fantasma.som_ataque_fantasma: Fantasma.som_ataque_fantasma.play()
                
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
                    # if Fantasma.sprites_carregados: 
                    #     self.sprites = Fantasma.sprites_carregados
                    #     self.intervalo_animacao = self.intervalo_animacao_flutuar
                    #     self.sprite_index = 0
                else:
                    if not self.hit_by_player_this_attack and \
                       hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0 and \
                       self.attack_hitbox.colliderect(player.rect):
                        if player.vida.esta_vivo(): 
                            player.receber_dano(self.attack_damage)
                            self.hit_by_player_this_attack = True 
                            # print(f"DEBUG(Fantasma): Ataque acertou o jogador! Dano: {self.attack_damage}")
            
            if not self.is_attacking:
                # if self.sprites != Fantasma.sprites_carregados and Fantasma.sprites_carregados:
                #     self.sprites = Fantasma.sprites_carregados
                #     self.intervalo_animacao = self.intervalo_animacao_flutuar
                #     self.sprite_index = 0
                self.atacar(player)
        

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y) 
        # Opcional: Desenhar a hitbox de ataque para debug
        # if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0:
        #     debug_hitbox_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
        #     s = pygame.Surface((self.attack_hitbox.width, self.attack_hitbox.height), pygame.SRCALPHA)
        #     s.fill((220, 220, 255, 100)) # Cor azul claro/lavanda para hitbox
        #     surface.blit(s, (debug_hitbox_rect_onscreen.x, debug_hitbox_rect_onscreen.y))

