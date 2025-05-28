# Vampiro.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()
import os # Importa os para verificar a existência de arquivos

# Certifique-se de que Inimigo está acessível
try:
    from Inimigos import Inimigo # Tenta importar a classe base real
    print("DEBUG(Vampiro): Classe base Inimigo importada com sucesso.")
except ImportError:
    print("DEBUG(Vampiro): ERRO: Módulo 'Inimigos.py' não encontrado. Usando classe Inimigo placeholder.")
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

            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (100, 100, 100), (0, 0, largura, altura)) # Cor cinza escuro para placeholder de Vampiro
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
            # Pathing para o placeholder: Assume que este script (Vampiro.py) está na raiz do projeto
            # ou que os caminhos para os sprites são relativos à sua localização.
            base_dir = os.path.dirname(os.path.abspath(__file__)) # Diretório do Vampiro.py
            game_root_dir = base_dir # Assume que a pasta 'Sprites' está na raiz ou o path é completo/relativo daqui
            # Se Vampiro.py estiver numa subpasta e 'Sprites' na raiz:
            # game_root_dir = os.path.dirname(base_dir)

            full_path = os.path.join(game_root_dir, path.replace("/", os.sep))

            if not os.path.exists(full_path):
                print(f"DEBUG(InimigoPlaceholder): Sprite não encontrado em '{full_path}'. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (100,100,100), (0, 0, tamanho[0], tamanho[1]))
                return img
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.scale(img, tamanho)
                return img
            except pygame.error as e:
                print(f"DEBUG(InimigoPlaceholder): Erro ao carregar sprite '{full_path}': {e}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (100,100,100), (0, 0, tamanho[0], tamanho[1]))
                return img

        def receber_dano(self, dano):
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
                pygame.draw.rect(self.image, (100,100,100), (0,0,self.largura,self.altura))


        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
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
                pygame.draw.rect(self.image, (100,100,100), (0,0,self.largura,self.altura))
                if not hasattr(self, 'rect'): 
                       self.rect = self.image.get_rect(topleft=(self.x, self.y))

            screen_x = self.rect.x - camera_x
            screen_y = self.rect.y - camera_y
            
            janela.blit(self.image, (screen_x, screen_y))

            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time < self.hit_flash_duration:
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


"""
Classe para o inimigo Vampiro.
Herda da classe base Inimigo.
"""
class Vampiro(Inimigo):
    sprites_originais = None # Deveria ser uma lista de listas para diferentes animações (idle, walk, attack)
    sprites_andar = None
    sprites_atacar = None
    sprites_idle = None # Opcional
    tamanho_sprite_definido = (80, 90) 

    som_ataque_vampiro = None
    som_dano_vampiro = None
    som_morte_vampiro = None
    som_spawn_vampiro = None 
    som_teleporte_vampiro = None 
    sons_carregados = False

    @staticmethod
    def _carregar_som_vampiro(caminho_relativo):
        current_file_dir = os.path.dirname(os.path.abspath(__file__)) 
        project_root = current_file_dir 
        full_path = os.path.join(project_root, caminho_relativo.replace("/", os.sep))
        
        if not os.path.exists(full_path):
            print(f"DEBUG(Vampiro): Arquivo de som não encontrado: {full_path}")
            return None
        try:
            som = pygame.mixer.Sound(full_path)
            return som
        except pygame.error as e:
            print(f"DEBUG(Vampiro): Erro ao carregar som '{full_path}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho, tipo_animacao):
        """Método auxiliar estático para carregar uma lista de sprites."""
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        game_root_dir = current_file_dir # Assume que Vampiro.py está na raiz do projeto
        
        for path_relativo in caminhos:
            full_path = os.path.join(game_root_dir, path_relativo.replace("/", os.sep))
            try:
                if os.path.exists(full_path):
                    sprite = pygame.image.load(full_path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                else:
                    print(f"DEBUG(Vampiro): Sprite {tipo_animacao} não encontrado: {full_path}. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (100, 100, 120), placeholder.get_rect()) 
                    lista_destino.append(placeholder)
            except pygame.error as e:
                print(f"DEBUG(Vampiro): Erro ao carregar sprite {tipo_animacao} '{full_path}': {e}")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (100, 100, 120), placeholder.get_rect())
                lista_destino.append(placeholder)
        
        if not lista_destino:
            print(f"DEBUG(Vampiro): Nenhum sprite de {tipo_animacao} carregado. Usando placeholder final.")
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (80, 80, 100), placeholder.get_rect()) 
            lista_destino.append(placeholder)

    @staticmethod
    def carregar_recursos_vampiro():
        if Vampiro.sprites_andar is None: # Usando sprites_andar como flag principal
            base_sprite_path = "Sprites/Inimigos/Vampiro/" 
            
            nomes_sprites_andar = [ "Vampiro_Walk_1.png", "Vampiro_Walk_2.png", "Vampiro_Walk_3.png", "Vampiro_Walk_4.png"] # CRIE ESTES
            Vampiro.sprites_andar = []
            Vampiro._carregar_lista_sprites_estatico(
                [base_sprite_path + nome for nome in nomes_sprites_andar], 
                Vampiro.sprites_andar, Vampiro.tamanho_sprite_definido, "Andar"
            )

            nomes_sprites_atacar = ["Vampiro_Attack_1.png", "Vampiro_Attack_2.png", "Vampiro_Attack_3.png"] # CRIE ESTES
            Vampiro.sprites_atacar = []
            Vampiro._carregar_lista_sprites_estatico(
                [base_sprite_path + nome for nome in nomes_sprites_atacar],
                Vampiro.sprites_atacar, Vampiro.tamanho_sprite_definido, "Atacar"
            )
            # Se não houver sprites de ataque, use o primeiro de andar
            if not Vampiro.sprites_atacar and Vampiro.sprites_andar:
                Vampiro.sprites_atacar = [Vampiro.sprites_andar[0]]


            # Opcional: Sprites Idle
            # nomes_sprites_idle = ["Vampiro_Idle_1.png", "Vampiro_Idle_2.png"]
            # Vampiro.sprites_idle = []
            # Vampiro._carregar_lista_sprites_estatico(
            # [base_sprite_path + nome for nome in nomes_sprites_idle],
            # Vampiro.sprites_idle, Vampiro.tamanho_sprite_definido, "Idle"
            # )
            # if not Vampiro.sprites_idle and Vampiro.sprites_andar: # Fallback para idle
            # Vampiro.sprites_idle = [Vampiro.sprites_andar[0]]


        if not Vampiro.sons_carregados:
            Vampiro.som_ataque_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/ataque_mordida.wav") 
            Vampiro.som_dano_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/dano.wav")
            Vampiro.som_morte_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/morte_poeira.wav")
            Vampiro.som_spawn_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/spawn_risada.wav") 
            Vampiro.som_teleporte_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/teleporte_fumaca.wav")
            Vampiro.sons_carregados = True


    def __init__(self, x, y, velocidade=3.5): 
        Vampiro.carregar_recursos_vampiro() 

        vampiro_hp = 90
        vampiro_contact_damage = 8 
        vampiro_xp_value = 60
        sprite_path_ref = "Sprites/Inimigos/Vampiro/Vampiro_Walk_1.png" if Vampiro.sprites_andar else "placeholder_vampiro.png"

        super().__init__(x, y,
                         Vampiro.tamanho_sprite_definido[0], Vampiro.tamanho_sprite_definido[1],
                         vampiro_hp, velocidade, vampiro_contact_damage,
                         vampiro_xp_value, sprite_path_ref)

        self.sprites = Vampiro.sprites_andar # Começa com animação de andar
        self.sprite_index = 0
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
        self.intervalo_animacao_andar = 120 
        self.intervalo_animacao_atacar = 90 # Ataque mais rápido
        self.intervalo_animacao = self.intervalo_animacao_andar

        self.is_attacking = False 
        self.attack_duration = 0.4 
        self.attack_timer = 0.0    
        self.attack_damage = 25    
        self.life_steal_percent = 0.3 
        self.attack_hitbox_size = (50, 50) 
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) 
        self.attack_range = 80    
        self.attack_cooldown = 1.8 
        self.last_attack_time = time.time() - self.attack_cooldown 

        self.can_dash = True
        self.dash_cooldown = 5.0 
        self.last_dash_time = time.time() - self.dash_cooldown
        self.dash_range = 200 
        self.is_dashing = False
        self.dash_duration = 0.2 
        self.dash_timer = 0.0
        self.dash_target_pos = None # Para onde o dash está indo

        if self.sprites and len(self.sprites) > 0:
            idx = int(self.sprite_index % len(self.sprites))
            self.image = self.sprites[idx]
        elif hasattr(super(), 'image') and super().image is not None: 
            self.image = super().image
        else: 
            self.image = pygame.Surface(Vampiro.tamanho_sprite_definido, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (100,100,120), (0,0,self.largura,self.altura))
            if not hasattr(self, 'rect'): 
                 self.rect = self.image.get_rect(topleft=(self.x, self.y))

        if Vampiro.som_spawn_vampiro:
            Vampiro.som_spawn_vampiro.play()

    def receber_dano(self, dano):
        vida_antes = self.hp
        super().receber_dano(dano) 
        if self.esta_vivo():
            if vida_antes > self.hp : 
                if Vampiro.som_dano_vampiro:
                    Vampiro.som_dano_vampiro.play()
        else: 
            if vida_antes > 0: 
                if Vampiro.som_morte_vampiro:
                    Vampiro.som_morte_vampiro.play()

    def _perform_dash(self, player_x, player_y):
        self.is_dashing = True
        self.dash_timer = time.time()
        self.last_dash_time = self.dash_timer
        self.can_dash = False 

        if Vampiro.som_teleporte_vampiro:
            Vampiro.som_teleporte_vampiro.play()

        dx = player_x - self.rect.centerx
        dy = player_y - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist > 0:
            # Tenta se posicionar um pouco atrás do jogador após o dash
            # Ou numa posição estratégica perto dele
            # Aqui, move-se para uma posição na direção do jogador, mas pode passar um pouco
            self.dash_target_pos = (
                self.rect.centerx + (dx / dist) * self.dash_range,
                self.rect.centery + (dy / dist) * self.dash_range
            )
            # O movimento real para dash_target_pos acontecerá no update durante is_dashing
        else: # Se já estiver no jogador, dash para uma posição aleatória próxima
            angle = random.uniform(0, 2 * math.pi)
            self.dash_target_pos = (
                self.rect.centerx + self.dash_range * 0.5 * math.cos(angle),
                self.rect.centery + self.dash_range * 0.5 * math.sin(angle)
            )
        
        # print(f"DEBUG(Vampiro): Vampiro iniciando dash para {self.dash_target_pos}")


    def atacar(self, player):
        if not hasattr(player, 'rect'):
            return

        current_time = time.time()
        if self.esta_vivo() and not self.is_attacking and not self.is_dashing and \
           (current_time - self.last_attack_time >= self.attack_cooldown):
            
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                             self.rect.centery - player.rect.centery)

            if distancia_ao_jogador <= self.attack_range:
                self.is_attacking = True
                self.attack_timer = current_time 
                self.last_attack_time = current_time 
                self.hit_by_player_this_attack = False 

                self.sprites = Vampiro.sprites_atacar # Muda para animação de ataque
                self.intervalo_animacao = self.intervalo_animacao_atacar
                self.sprite_index = 0

                attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0]
                attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1]
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                # A hitbox será posicionada no update do ataque
                
                if Vampiro.som_ataque_vampiro:
                    Vampiro.som_ataque_vampiro.play()

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or \
           not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            if self.esta_vivo(): self.atualizar_animacao() 
            return

        current_time = time.time()

        if not self.can_dash and (current_time - self.last_dash_time >= self.dash_cooldown):
            self.can_dash = True

        if self.is_dashing:
            if self.dash_target_pos:
                # Movimento suave para o alvo do dash
                target_x, target_y = self.dash_target_pos
                dx = target_x - self.rect.centerx
                dy = target_y - self.rect.centery
                dist_to_target = math.hypot(dx, dy)
                
                # Velocidade de dash muito alta para parecer teleporte
                dash_speed_factor = 15 # Ajuste para quão rápido o dash "completa"
                
                if dist_to_target > self.velocidade * dash_speed_factor * (dt_ms / 1000.0 if dt_ms else 0.016): # 0.016s = 1/60fps
                    self.rect.x += (dx / dist_to_target) * self.velocidade * dash_speed_factor * (dt_ms / 1000.0 if dt_ms else 0.016)
                    self.rect.y += (dy / dist_to_target) * self.velocidade * dash_speed_factor * (dt_ms / 1000.0 if dt_ms else 0.016)
                else:
                    self.rect.centerx = target_x
                    self.rect.centery = target_y
                    self.is_dashing = False
                    self.dash_target_pos = None
                    self.sprites = Vampiro.sprites_andar # Volta para sprites de andar
                    self.intervalo_animacao = self.intervalo_animacao_andar


            if current_time - self.dash_timer >= self.dash_duration: # Tempo máximo para o estado de dash
                self.is_dashing = False
                self.dash_target_pos = None
                self.sprites = Vampiro.sprites_andar 
                self.intervalo_animacao = self.intervalo_animacao_andar
            
            self.atualizar_animacao() # Animação de dash ou transição
            return # Não faz mais nada durante o dash

        # Se não estiver em dash, comportamento normal
        if not self.is_attacking:
            try:
                super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)
            except TypeError:
                super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela)
        else:
            self.atualizar_animacao() # Animação de ataque


        if self.esta_vivo():
            dist_to_player = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
            if self.can_dash and not self.is_attacking and dist_to_player > self.attack_range * 2 and dist_to_player < self.dash_range * 1.5:
                if random.random() < (0.02 if dt_ms is None else (0.02 * (dt_ms / 16.66))): # Chance ajustada por dt_ms
                    self._perform_dash(player.rect.centerx, player.rect.centery)
                    return 

            if self.is_attacking:
                # Posiciona a hitbox de ataque à frente do vampiro
                offset_x_hitbox = self.attack_hitbox_size[0] / 2 + 10 # Ajuste conforme necessário
                if self.facing_right:
                    self.attack_hitbox.centerx = self.rect.centerx + offset_x_hitbox
                else:
                    self.attack_hitbox.centerx = self.rect.centerx - offset_x_hitbox
                self.attack_hitbox.centery = self.rect.centery

                if current_time - self.attack_timer >= self.attack_duration:
                    self.is_attacking = False
                    self.hit_by_player_this_attack = False
                    self.sprites = Vampiro.sprites_andar # Volta para sprites de andar
                    self.intervalo_animacao = self.intervalo_animacao_andar
                else:
                    if not self.hit_by_player_this_attack and \
                       self.attack_hitbox.colliderect(player.rect):
                        if player.vida.esta_vivo():
                            player.receber_dano(self.attack_damage)
                            vida_roubada = int(self.attack_damage * self.life_steal_percent)
                            self.hp = min(self.max_hp, self.hp + vida_roubada)
                            self.hit_by_player_this_attack = True 
            
            if not self.is_attacking:
                if self.sprites != Vampiro.sprites_andar and self.sprites != Vampiro.sprites_idle : # Se não estiver idle
                    self.sprites = Vampiro.sprites_andar
                    self.intervalo_animacao = self.intervalo_animacao_andar
                self.atacar(player)

    def desenhar(self, surface, camera_x, camera_y):
        # Efeito visual para dash (ex: rastro, ou sprite diferente)
        # if self.is_dashing:
        #     # Desenhar um efeito de "rastro" ou mudar a transparência
        #     # Esta é uma implementação simples, pode ser melhorada
        #     temp_image = self.image.copy()
        #     alpha_value = 255 - int((time.time() - self.dash_timer) / self.dash_duration * 200) # Fade out
        #     alpha_value = max(50, min(255, alpha_value))
        #     temp_image.set_alpha(alpha_value) 
        #     surface.blit(temp_image, (self.rect.x - camera_x, self.rect.y - camera_y))
        # else:
        #     super().desenhar(surface, camera_x, camera_y) # Desenho normal
        
        super().desenhar(surface, camera_x, camera_y)
        
        # Opcional: Desenhar a hitbox de ataque para debug
        # if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0:
        #     debug_hitbox_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
        #     s = pygame.Surface((self.attack_hitbox.width, self.attack_hitbox.height), pygame.SRCALPHA)
        #     s.fill((180, 0, 0, 100))  
        #     surface.blit(s, (debug_hitbox_rect_onscreen.x, debug_hitbox_rect_onscreen.y))

