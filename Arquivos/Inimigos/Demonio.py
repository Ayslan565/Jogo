# Demonio.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()
import os # Importa os para verificar a existência de arquivos
from Inimigos import Inimigo # Tenta importar a classe base real

# Certifique-se de que Inimigo está acessível

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
            self.moedas_drop = getattr(self, 'moedas_drop', 0) # Garante que o atributo exista

            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 255), (0, 0, largura, altura)) # Cor magenta para placeholder
            self.rect = self.image.get_rect(topleft=(x, y))

            self.last_hit_time = 0
            self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)

            self.is_attacking = False
            self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
            self.hit_by_player_this_attack = False
            self.contact_cooldown = 1000
            self.last_contact_time = pygame.time.get_ticks() - self.contact_cooldown # Para permitir dano de contato logo
            self.facing_right = True

            self.sprites = [self.image.copy()] if self.image and isinstance(self.image, pygame.Surface) else []
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.intervalo_animacao = 200

        def _carregar_sprite(self, path, tamanho):
            # Este é um placeholder de carregamento, a classe real deve ter uma implementação melhor
            # print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{path}'.")
            try:
                if os.path.exists(path):
                    img = pygame.image.load(path).convert_alpha()
                    return pygame.transform.scale(img, tamanho)
                else:
                    # print(f"AVISO(InimigoBase Placeholder _carregar_sprite): Sprite '{path}' não encontrado. Usando placeholder visual.")
                    img = pygame.Surface(tamanho, pygame.SRCALPHA)
                    img.fill((255, 0, 255, 100)) # Magenta para placeholder
                    return img
            except pygame.error as e:
                # print(f"ERRO(InimigoBase Placeholder _carregar_sprite): Falha ao carregar '{path}': {e}. Usando placeholder visual.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                img.fill((255, 0, 255, 100))
                return img

        def receber_dano(self, dano, fonte_dano_rect=None): # Adicionado fonte_dano_rect
            if not self.esta_vivo(): return
            self.hp -= dano
            self.last_hit_time = pygame.time.get_ticks()
            self.hp = max(0, self.hp)

        def esta_vivo(self):
            return self.hp > 0

        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None):
            if self.esta_vivo() and self.velocidade > 0:
                dx = alvo_x - self.rect.centerx
                dy = alvo_y - self.rect.centery
                dist = math.hypot(dx, dy)

                fator_tempo = 1.0 # Se dt_ms não for usado, movimento é por frame
                if dt_ms is not None and dt_ms > 0:
                     # Converte velocidade para pixels por segundo se dt_ms for usado
                     # Assume que self.velocidade é pixels por frame se dt_ms não for usado,
                     # ou pixels por segundo se dt_ms for usado consistentemente.
                     # Para simplificar, vamos assumir que self.velocidade é uma magnitude.
                     # Se dt_ms é fornecido, ajustamos o movimento.
                     # Se velocidade é px/frame @60fps, então velocidade_px_s = self.velocidade * 60
                     # movimento = (direcao * velocidade_px_s) * (dt_ms / 1000.0)
                     # Se self.velocidade já é px/s: movimento = direcao * self.velocidade * (dt_ms / 1000.0)
                     # Vamos assumir que a classe base Inimigo tem uma velocidade definida em px/frame
                     # e que o dt_ms é para ajustar isso a uma taxa de atualização variável.
                     # Se o jogo roda a 60FPS, dt_ms seria ~16.66ms.
                     # movimento_por_frame = self.velocidade
                     # movimento_ajustado = self.velocidade * (dt_ms / (1000.0/60.0)) # Ajusta baseado em 60 FPS
                     fator_tempo = (dt_ms / (1000.0 / 60.0)) if dt_ms else 1.0


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

            if self.sprites and len(self.sprites) > 0: # Garante que há sprites
                idx = int(self.sprite_index % len(self.sprites)) # Evita IndexError
                base_image = self.sprites[idx]
                if hasattr(self, 'facing_right') and not self.facing_right:
                    self.image = pygame.transform.flip(base_image, True, False)
                else:
                    self.image = base_image.copy() # Usa cópia para não alterar o original na lista de sprites
            elif not hasattr(self, 'image') or self.image is None : # Fallback extremo
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA); self.image.fill((255,0,255,100))

        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            if self.esta_vivo():
                if hasattr(player, 'rect') and player.rect is not None:
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
                self.atualizar_animacao()

                current_ticks = pygame.time.get_ticks()
                if hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                   self.rect.colliderect(player.rect) and \
                   (current_ticks - self.last_contact_time >= self.contact_cooldown):
                    if hasattr(player, 'receber_dano'):
                        player.receber_dano(self.contact_damage, self.rect) # Passa o rect do inimigo como fonte do dano
                        self.last_contact_time = current_ticks

        def desenhar(self, janela, camera_x, camera_y):
            if not hasattr(self, 'image') or self.image is None:
                self.image = pygame.Surface((getattr(self,'largura',32), getattr(self,'altura',32)), pygame.SRCALPHA)
                self.image.fill((255,0,255,100))
            if not hasattr(self, 'rect'):
                self.rect = self.image.get_rect(topleft=(getattr(self,'x',0), getattr(self,'y',0)))

            screen_x = self.rect.x - camera_x
            screen_y = self.rect.y - camera_y
            janela.blit(self.image, (screen_x, screen_y))

            current_time = pygame.time.get_ticks()
            if hasattr(self, 'last_hit_time') and current_time - self.last_hit_time < self.hit_flash_duration:
                flash_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                flash_surface.fill(self.hit_flash_color)
                janela.blit(flash_surface, (screen_x, screen_y), special_flags=pygame.BLEND_RGBA_ADD)


            if self.hp < self.max_hp and self.hp > 0:
                bar_width = self.rect.width
                bar_height = 5
                health_percentage = self.hp / self.max_hp
                current_bar_width = int(bar_width * health_percentage)
                bar_x = screen_x
                bar_y = screen_y - bar_height - 5
                pygame.draw.rect(janela, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=2)
                pygame.draw.rect(janela, (0, 255, 0), (bar_x, bar_y, current_bar_width, bar_height), border_radius=2)
                pygame.draw.rect(janela, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=2)


class Demonio(Inimigo):
    sprites_originais = None
    tamanho_sprite_definido = (96, 96)

    som_ataque_demonio = None
    som_dano_demonio = None
    som_morte_demonio = None
    som_spawn_demonio = None
    sons_carregados = False

    @staticmethod
    def _carregar_som_demonio(caminho_relativo):
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_file_dir)) # Assume Jogo/Arquivos/Inimigos/Demonio.py
        if not os.path.isdir(os.path.join(project_root, "Sons")): # Tenta Jogo/Sons
            project_root = os.path.dirname(project_root) # Tenta Jogo/
            if not os.path.isdir(os.path.join(project_root, "Sons")):
                 project_root = os.path.dirname(os.path.abspath(__file__)) # Fallback para diretório do script se não encontrar "Sons"

        full_path = os.path.join(project_root, caminho_relativo.replace("/", os.sep))

        if not os.path.exists(full_path):
            # print(f"DEBUG(Demonio): Arquivo de som não encontrado: {full_path}")
            return None
        try:
            som = pygame.mixer.Sound(full_path)
            return som
        except pygame.error as e:
            # print(f"DEBUG(Demonio): Erro ao carregar som '{full_path}': {e}")
            return None

    @staticmethod
    def carregar_recursos_demonio():
        if Demonio.sprites_originais is None:
            base_sprite_path = "Sprites/Inimigos/Demonio/"
            nomes_sprites = [
                "20250521_1111_Demônio Pixel Art_simple_compose_01jvsjxvc7f8ca6npqkjaftsrv (1).png",
                "Demonio_Sprite_2.png",
                "Demonio_Sprite_3.png",
                "Demonio_Sprite_4.png"
            ]
            caminhos_sprites_completos = [base_sprite_path + nome for nome in nomes_sprites]
            Demonio.sprites_originais = []

            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            game_root_dir = os.path.dirname(os.path.dirname(current_file_dir)) # Assume Jogo/Arquivos/Inimigos/Demonio.py
            if not os.path.isdir(os.path.join(game_root_dir, "Sprites")): # Tenta Jogo/Sprites
                 game_root_dir = os.path.dirname(game_root_dir) # Tenta Jogo/
                 if not os.path.isdir(os.path.join(game_root_dir, "Sprites")):
                     game_root_dir = current_file_dir # Fallback

            for path_relativo_ao_jogo in caminhos_sprites_completos:
                full_path = os.path.join(game_root_dir, path_relativo_ao_jogo.replace("/", os.sep))
                try:
                    if os.path.exists(full_path):
                        sprite_img = pygame.image.load(full_path).convert_alpha()
                        sprite_scaled = pygame.transform.scale(sprite_img, Demonio.tamanho_sprite_definido)
                        Demonio.sprites_originais.append(sprite_scaled)
                    else:
                        # print(f"DEBUG(Demonio): Sprite não encontrado {full_path}, usando placeholder vermelho.")
                        placeholder = pygame.Surface(Demonio.tamanho_sprite_definido, pygame.SRCALPHA)
                        pygame.draw.rect(placeholder, (200, 0, 0), placeholder.get_rect())
                        Demonio.sprites_originais.append(placeholder)
                except pygame.error as e:
                    # print(f"DEBUG(Demonio): Erro ao carregar o sprite do Demônio: {full_path} - {e}")
                    placeholder = pygame.Surface(Demonio.tamanho_sprite_definido, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (200, 0, 0), placeholder.get_rect())
                    Demonio.sprites_originais.append(placeholder)

            if not Demonio.sprites_originais:
                # print("DEBUG(Demonio): Nenhum sprite carregado para Demonio, usando placeholder final.")
                placeholder = pygame.Surface(Demonio.tamanho_sprite_definido, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (150, 0, 0), placeholder.get_rect())
                Demonio.sprites_originais.append(placeholder)

        if not Demonio.sons_carregados:
            Demonio.som_ataque_demonio = Demonio._carregar_som_demonio("Sons/Demonio/ataque.wav")
            Demonio.som_dano_demonio = Demonio._carregar_som_demonio("Sons/Demonio/dano.wav")
            Demonio.som_morte_demonio = Demonio._carregar_som_demonio("Sons/Demonio/morte.wav")
            Demonio.som_spawn_demonio = Demonio._carregar_som_demonio("Sons/Demonio/spawn.wav")
            Demonio.sons_carregados = True


    def __init__(self, x, y, velocidade=2.5): # Velocidade ajustada para o Demônio
        Demonio.carregar_recursos_demonio() # Garante que sprites e sons sejam carregados uma vez

        demonio_hp = 90
        demonio_contact_damage = 10
        demonio_xp_value = 75
        # moedas_dropadas = 12

        
        # O sprite_path_principal é usado pela classe base, mas Demonio usa sua lista de sprites.
        # Podemos passar o caminho do primeiro frame como referência.
        sprite_path_ref = "Sprites/Inimigos/Demonio/" + Demonio.sprites_originais[0].get_at((0,0)) if Demonio.sprites_originais and Demonio.sprites_originais[0] else "Sprites/Inimigos/Demonio/placeholder_demonio.png"


        super().__init__(x, y,
                         Demonio.tamanho_sprite_definido[0], Demonio.tamanho_sprite_definido[1],
                         demonio_hp, velocidade, demonio_contact_damage,
                         self.xp_value, sprite_path_ref)

        self.sprites = Demonio.sprites_originais
        self.sprite_index = 0
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
        self.intervalo_animacao = 120

        self.is_attacking = False
        self.attack_duration = 0.6
        self.attack_timer = 0.0
        self.attack_damage = 20
        self.attack_hitbox_size = (70, 70)
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.attack_range = 120
        self.attack_cooldown = 2.5
        self.last_attack_time = time.time() - self.attack_cooldown

        if self.sprites and len(self.sprites) > 0:
            idx = int(self.sprite_index % len(self.sprites))
            self.image = self.sprites[idx]
        elif hasattr(super(), 'image') and super().image is not None:
            self.image = super().image
        else:
            self.image = pygame.Surface(Demonio.tamanho_sprite_definido, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (200,0,0), (0,0,self.largura,self.altura))
            if not hasattr(self, 'rect'):
                 self.rect = self.image.get_rect(topleft=(self.x, self.y))

        if Demonio.som_spawn_demonio:
            Demonio.som_spawn_demonio.play()


    def receber_dano(self, dano):
        vida_antes = self.hp
        super().receber_dano(dano) # Chama o método da classe base

        if self.esta_vivo():
            if vida_antes > self.hp :
                if Demonio.som_dano_demonio:
                    Demonio.som_dano_demonio.play()
        else:
            if vida_antes > 0:
                if Demonio.som_morte_demonio:
                    Demonio.som_morte_demonio.play()
                # self.kill() # O GerenciadorDeInimigos deve cuidar de remover o sprite dos grupos

    # atualizar_animacao e mover_em_direcao são herdados da classe base Inimigo
    # e já devem funcionar corretamente com self.sprites, self.velocidade, etc.

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
                self.attack_timer = current_time # Inicia o timer da duração do ataque
                self.last_attack_time = current_time # Reseta o cooldown
                self.hit_by_player_this_attack = False # Reseta flag de dano para este ataque

                # Configura a hitbox de ataque (pode ser um golpe físico, baforada, etc.)
                # A posição será atualizada no update se o Demônio se mover
                attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0]
                attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1]
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                self.attack_hitbox.center = self.rect.center

                if Demonio.som_ataque_demonio:
                    Demonio.som_ataque_demonio.play()

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        # Validação básica do jogador
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or \
           not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            if self.esta_vivo(): self.atualizar_animacao()
            return

        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)

        if self.esta_vivo():
            current_time_ataque = time.time()

            if self.is_attacking:
                self.attack_hitbox.center = self.rect.center

                if current_time_ataque - self.attack_timer >= self.attack_duration:
                    self.is_attacking = False
                    self.hit_by_player_this_attack = False
                    # print(f"DEBUG(Demonio): Demônio terminou ciclo de ataque.")
                else:
                    if not self.hit_by_player_this_attack and \
                       hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0 and \
                       self.attack_hitbox.colliderect(player.rect):
                        if player.vida.esta_vivo():
                            player.receber_dano(self.attack_damage)
                            self.hit_by_player_this_attack = True # Garante dano uma vez por ataque
                            # print(f"DEBUG(Demonio): Demônio atingiu jogador com ataque especial.")
            
            # Se não estiver atacando, tenta iniciar um novo ataque
            if not self.is_attacking:
                self.atacar(player)
        # else: self.kill() # Se morrer, o gerenciador deve cuidar da remoção.

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y) # Chama o desenhar da classe base (imagem, flash, barra de vida)
        
        # Opcional: Desenhar a hitbox de ataque para debug
        # if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0:
        #     debug_hitbox_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
        #     # Cria uma surface semi-transparente para a hitbox
        #     s = pygame.Surface((self.attack_hitbox.width, self.attack_hitbox.height), pygame.SRCALPHA)
        #     s.fill((255, 100, 0, 100))  # Cor laranja semi-transparente
        #     surface.blit(s, (debug_hitbox_rect_onscreen.x, debug_hitbox_rect_onscreen.y))
        #     # pygame.draw.rect(surface, (255, 100, 0, 100), debug_hitbox_rect_onscreen, 1) # Borda
