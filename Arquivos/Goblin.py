# Goblin.py
import pygame
import random
import math 
import time 
import os 

# Importa a classe base Inimigo do ficheiro Inimigos.py
try:
    from Inimigos import Inimigo
    print("DEBUG(Goblin): Classe base Inimigo importada com sucesso.")
except ImportError:
    print("DEBUG(Goblin): ERRO: Módulo 'Inimigos.py' ou classe 'Inimigo' NÃO encontrado. Usando classe Inimigo placeholder.")
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
            pygame.draw.rect(self.image, (0, 100, 0), (0, 0, largura, altura)) 
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
            # Corrigido: Assume que Goblin.py está na raiz do projeto ou os caminhos são relativos a ele.
            base_dir = os.path.dirname(os.path.abspath(__file__)) # Diretório do Goblin.py
            game_root_dir = base_dir # Assume que a pasta 'Sprites' está na raiz ou o path é completo/relativo daqui
            
            full_path = os.path.join(game_root_dir, path.replace("/", os.sep))
            if not os.path.exists(full_path):
                print(f"DEBUG(InimigoPlaceholder): Aviso: Arquivo de sprite não encontrado: {full_path}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (0,100,0), (0, 0, tamanho[0], tamanho[1]))
                return img
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.scale(img, tamanho)
                return img
            except pygame.error as e:
                print(f"DEBUG(InimigoPlaceholder): Erro ao carregar sprite '{full_path}': {e}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (0,100,0), (0, 0, tamanho[0], tamanho[1]))
                return img

        def receber_dano(self, dano):
            self.hp -= dano
            self.last_hit_time = pygame.time.get_ticks()
            if self.hp <= 0:
                self.hp = 0

        def esta_vivo(self):
            return self.hp > 0

        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None): 
            # Este placeholder Inimigo.mover_em_direcao USA dt_ms se fornecido.
            # Se o Inimigos.py real não usar, o movimento será diferente.
            if self.esta_vivo() and self.velocidade > 0:
                dx = alvo_x - self.rect.centerx
                dy = alvo_y - self.rect.centery
                dist = math.hypot(dx, dy)
                fator_tempo = 1.0
                if dt_ms is not None and dt_ms > 0:
                     fator_tempo = (dt_ms / (1000.0 / 60.0)) # Assume velocidade em px/frame @60FPS

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
                pygame.draw.rect(self.image, (0,100,0), (0,0,self.largura,self.altura))


        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): 
            # Este placeholder Inimigo.update USA dt_ms.
            if self.esta_vivo():
                if hasattr(player, 'rect'):
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
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
                pygame.draw.rect(self.image, (0,100,0), (0,0,self.largura,self.altura))
            if not hasattr(self, 'rect'):
                   self.rect = self.image.get_rect(topleft=(self.x,self.y))

            screen_x = self.rect.x - camera_x
            screen_y = self.rect.y - camera_y
            janela.blit(self.image, (screen_x, screen_y))

            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time < self.hit_flash_duration:
                flash_image_overlay = self.image.copy()
                # Usando BLEND_RGB_ADD para um efeito de clareamento mais sutil que BLEND_RGB_MAX
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
                pygame.draw.rect(janela, (150, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=2) 
                pygame.draw.rect(janela, (0, 150, 0), (bar_x, bar_y, current_bar_width, bar_height), border_radius=2) 
                pygame.draw.rect(janela, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=2) 

class Goblin(Inimigo):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None 
    tamanho_sprite_definido = (50, 60) 

    som_ataque_goblin = None
    som_dano_goblin = None
    som_morte_goblin = None
    som_spawn_goblin = None 
    sons_carregados = False

    @staticmethod
    def _carregar_som_goblin(caminho_relativo):
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = current_file_dir 
        full_path = os.path.join(project_root, caminho_relativo.replace("/", os.sep))
        if not os.path.exists(full_path):
            print(f"DEBUG(Goblin): Arquivo de som não encontrado: {full_path}")
            return None
        try:
            som = pygame.mixer.Sound(full_path)
            return som
        except pygame.error as e:
            print(f"DEBUG(Goblin): Erro ao carregar som '{full_path}': {e}")
            return None

    @staticmethod
    def carregar_recursos_goblin():
        if Goblin.sprites_andar_carregados is None:
            caminhos_andar = [
                "Sprites/Inimigos/Goblin/Goblin_Andar1.png", 
                "Sprites/Inimigos/Goblin/Goblin_Andar2.png",
                "Sprites/Inimigos/Goblin/Goblin_Andar3.png",
                "Sprites/Inimigos/Goblin/Goblin_Andar4.png",
            ]
            Goblin.sprites_andar_carregados = []
            Goblin._carregar_lista_sprites_estatico(caminhos_andar, Goblin.sprites_andar_carregados, Goblin.tamanho_sprite_definido, "Andar")

        if Goblin.sprites_atacar_carregados is None:
            caminhos_atacar = [
                "Sprites/Inimigos/Goblin/Goblin_Atacar1.png", 
                "Sprites/Inimigos/Goblin/Goblin_Atacar2.png",
                "Sprites/Inimigos/Goblin/Goblin_Atacar3.png",
            ]
            Goblin.sprites_atacar_carregados = []
            if caminhos_atacar: 
                Goblin._carregar_lista_sprites_estatico(caminhos_atacar, Goblin.sprites_atacar_carregados, Goblin.tamanho_sprite_definido, "Atacar")
            
            if not Goblin.sprites_atacar_carregados: 
                if Goblin.sprites_andar_carregados:
                    Goblin.sprites_atacar_carregados = [Goblin.sprites_andar_carregados[0]] 
                else: 
                    placeholder_ataque = pygame.Surface(Goblin.tamanho_sprite_definido, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder_ataque, (0,80,0), placeholder_ataque.get_rect())
                    Goblin.sprites_atacar_carregados = [placeholder_ataque]
        
        if not Goblin.sons_carregados:
            Goblin.som_ataque_goblin = Goblin._carregar_som_goblin("Sons/Goblin/ataque_adaga.wav") 
            Goblin.som_dano_goblin = Goblin._carregar_som_goblin("Sons/Goblin/dano_guincho.wav")
            Goblin.som_morte_goblin = Goblin._carregar_som_goblin("Sons/Goblin/morte_rapida.wav")
            Goblin.som_spawn_goblin = Goblin._carregar_som_goblin("Sons/Goblin/spawn_risada_curta.wav") 
            Goblin.sons_carregados = True
    
    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho, tipo_animacao):
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        game_root_dir = current_file_dir # Assumindo que Goblin.py está na raiz do projeto
        
        for path_relativo in caminhos:
            full_path = os.path.join(game_root_dir, path_relativo.replace("/", os.sep))
            try:
                if os.path.exists(full_path):
                    sprite = pygame.image.load(full_path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                else:
                    print(f"DEBUG(Goblin): Sprite {tipo_animacao} não encontrado: {full_path}. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (0, 100, 0), placeholder.get_rect()) 
                    lista_destino.append(placeholder)
            except pygame.error as e:
                print(f"DEBUG(Goblin): Erro ao carregar sprite {tipo_animacao} '{full_path}': {e}")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (0, 100, 0), placeholder.get_rect())
                lista_destino.append(placeholder)
        
        if not lista_destino:
            print(f"DEBUG(Goblin): Nenhum sprite de {tipo_animacao} carregado. Usando placeholder final.")
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (0, 70, 0), placeholder.get_rect()) 
            lista_destino.append(placeholder)


    def __init__(self, x, y, velocidade=2.0): 
        Goblin.carregar_recursos_goblin() 

        goblin_hp = 40
        goblin_contact_damage = 6
        goblin_xp_value = 15
        sprite_path_ref = "Sprites/Inimigos/Goblin/Goblin_Andar1.png" if Goblin.sprites_andar_carregados else "placeholder_goblin.png"

        super().__init__(x, y,
                         Goblin.tamanho_sprite_definido[0], Goblin.tamanho_sprite_definido[1],
                         goblin_hp, velocidade, goblin_contact_damage,
                         goblin_xp_value, sprite_path_ref)

        self.sprites = Goblin.sprites_andar_carregados
        self.sprite_index = 0
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
        self.intervalo_animacao_andar = 150 
        self.intervalo_animacao_atacar = 100 
        self.intervalo_animacao = self.intervalo_animacao_andar

        self.is_attacking = False
        self.attack_duration = 0.5 
        self.attack_timer = 0.0
        self.attack_damage = 10 
        self.attack_range = 50  
        self.attack_cooldown = 1.8 
        self.last_attack_time = time.time() - self.attack_cooldown

        self.attack_hitbox_largura = 30
        self.attack_hitbox_altura = 40
        self.attack_hitbox_offset_x = 5 

        if self.sprites and len(self.sprites) > 0:
            idx = int(self.sprite_index % len(self.sprites))
            self.image = self.sprites[idx]
        elif hasattr(super(), 'image') and super().image is not None:
            self.image = super().image
        else:
            self.image = pygame.Surface(Goblin.tamanho_sprite_definido, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (0,100,0), self.image.get_rect())
            if not hasattr(self, 'rect'):
                 self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        if Goblin.som_spawn_goblin:
            Goblin.som_spawn_goblin.play()
        
        # print(f"DEBUG(Goblin): Goblin inicializado. HP: {self.hp}, Vel: {self.velocidade}")


    def receber_dano(self, dano):
        vida_antes = self.hp
        super().receber_dano(dano)
        if self.esta_vivo():
            if vida_antes > self.hp and Goblin.som_dano_goblin:
                Goblin.som_dano_goblin.play()
        elif vida_antes > 0 and Goblin.som_morte_goblin: 
            Goblin.som_morte_goblin.play()


    def atacar(self, player):
        if not hasattr(player, 'rect'):
            return

        current_time = time.time()
        if self.esta_vivo() and not self.is_attacking and \
           (current_time - self.last_attack_time >= self.attack_cooldown):
            
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                             self.rect.centery - player.rect.centery)

            if distancia_ao_jogador <= self.attack_range:
                self.is_attacking = True
                self.attack_timer = current_time
                self.last_attack_time = current_time
                self.hit_by_player_this_attack = False
                
                self.sprites = Goblin.sprites_atacar_carregados 
                self.intervalo_animacao = self.intervalo_animacao_atacar
                self.sprite_index = 0 
                
                if Goblin.som_ataque_goblin:
                    Goblin.som_ataque_goblin.play()
                
                if self.facing_right:
                    hitbox_x = self.rect.right - self.attack_hitbox_offset_x 
                else:
                    hitbox_x = self.rect.left - self.attack_hitbox_largura + self.attack_hitbox_offset_x
                
                hitbox_y = self.rect.centery - (self.attack_hitbox_altura / 2)
                self.attack_hitbox = pygame.Rect(hitbox_x, hitbox_y, self.attack_hitbox_largura, self.attack_hitbox_altura)

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): 
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or \
           not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            if self.esta_vivo(): self.atualizar_animacao() 
            return

        if not self.is_attacking:
            # --- CORREÇÃO PRINCIPAL ---
            # Chama super().update() sem dt_ms para ser compatível com a assinatura de Inimigos.py
            # que você forneceu (ID: inimigo_base_py), que não aceita dt_ms em seu update.
            # Se o seu Inimigos.py REAL aceitar dt_ms no update, você pode passar dt_ms aqui.
            # Se o seu Inimigos.py REAL NÃO usar dt_ms para mover, então o movimento será frame-dependente.
            # O placeholder Inimigo DENTRO DESTE ARQUIVO Goblin.py USA dt_ms,
            # então se Inimigos.py falhar ao importar, o movimento será ajustado por dt_ms.
            try:
                # Tenta chamar com dt_ms primeiro, caso o Inimigo base real o suporte
                super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)
            except TypeError:
                # Se der TypeError (provavelmente porque o Inimigo.update não aceita dt_ms),
                # chama sem dt_ms.
                super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela)
        else: 
            self.atualizar_animacao()


        if self.esta_vivo():
            current_time_ataque = time.time()

            if self.is_attacking:
                if self.facing_right:
                    hitbox_x = self.rect.right - self.attack_hitbox_offset_x
                else:
                    hitbox_x = self.rect.left - self.attack_hitbox_largura + self.attack_hitbox_offset_x
                hitbox_y = self.rect.centery - (self.attack_hitbox_altura / 2)
                self.attack_hitbox.topleft = (hitbox_x, hitbox_y)

                if current_time_ataque - self.attack_timer >= self.attack_duration:
                    self.is_attacking = False 
                    self.hit_by_player_this_attack = False 
                    self.sprites = Goblin.sprites_andar_carregados 
                    self.intervalo_animacao = self.intervalo_animacao_andar
                    self.sprite_index = 0 
                else:
                    if not self.hit_by_player_this_attack and \
                       self.attack_hitbox.colliderect(player.rect):
                        if player.vida.esta_vivo(): 
                            player.receber_dano(self.attack_damage)
                            self.hit_by_player_this_attack = True 
            
            if not self.is_attacking:
                if self.sprites != Goblin.sprites_andar_carregados:
                    self.sprites = Goblin.sprites_andar_carregados
                    self.intervalo_animacao = self.intervalo_animacao_andar
                    self.sprite_index = 0 
                self.atacar(player) 

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y)
        
        # Opcional: Desenhar a hitbox de ataque para debug
        # if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0:
        #     debug_hitbox_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
        #     s = pygame.Surface((self.attack_hitbox.width, self.attack_hitbox.height), pygame.SRCALPHA)
        #     s.fill((0, 150, 0, 100)) 
        #     surface.blit(s, (debug_hitbox_rect_onscreen.x, debug_hitbox_rect_onscreen.y))
