# Vampiro.py
import pygame
import os
import math
import time

# --- Importação da Classe Base Inimigo ---
# Assume que existe um arquivo 'Inimigos.py' na MESMA PASTA que este
# (Jogo/Arquivos/Inimigos/Inimigos.py) e que ele define a classe 'Inimigo' base.
# Essa classe base é referenciada como 'InimigoBase' aqui.
try:
    from .Inimigos import Inimigo as InimigoBase
    # print(f"DEBUG(Vampiro): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Vampiro): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((50, 0, 0, 100)) # Placeholder vermelho escuro para Vampiro
            pygame.draw.rect(self.image, (100,0,0), self.image.get_rect(), 1) # Borda vermelha
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = pygame.time.get_ticks() - self.contact_cooldown
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.x = float(x)
            self.y = float(y)
            # print(f"DEBUG(InimigoBase Placeholder para Vampiro): Instanciado. Sprite path (não usado): {sprite_path}")

        def _carregar_sprite(self, path, tamanho):
            caminho_log = os.path.normpath(path)
            # print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{caminho_log}' (não implementado). Retornando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((80,0,0, 128)) # Cor vermelha escura para placeholder do _carregar_sprite
            return img

        def receber_dano(self, dano, fonte_dano_rect=None):
             self.hp = max(0, self.hp - dano)
             if hasattr(self, 'last_hit_time'):
                 self.last_hit_time = pygame.time.get_ticks()
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt_ms=None):
            if self.esta_vivo() and self.velocidade > 0:
                dx = ax - self.rect.centerx
                dy = ay - self.rect.centery
                dist = math.hypot(dx, dy)
                fator_tempo = (dt_ms / (1000.0 / 60.0)) if dt_ms and dt_ms > 0 else 1.0

                if dist > self.velocidade * fator_tempo :
                    mov_x = (dx / dist) * self.velocidade * fator_tempo
                    mov_y = (dy / dist) * self.velocidade * fator_tempo
                    self.rect.x += mov_x
                    self.rect.y += mov_y
                    self.x = float(self.rect.x)
                    self.y = float(self.rect.y)
                    if abs(dx) > 0.1 : self.facing_right = dx > 0
                elif dist > 0 : # Snap to position if very close
                    self.rect.center = (round(ax), round(ay))
                    self.x = float(self.rect.x)
                    self.y = float(self.rect.y)

        def atualizar_animacao(self):
            agora = pygame.time.get_ticks()
            if self.sprites and len(self.sprites) > 1 and self.esta_vivo():
                if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                    self.tempo_ultimo_update_animacao = agora
                    self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            
            if self.sprites and len(self.sprites) > 0:
                idx = int(self.sprite_index % len(self.sprites))
                base_image = self.sprites[idx]
                if isinstance(base_image, pygame.Surface):
                    self.image = base_image.copy() # Use a copy to avoid modifying the original in the list
                    if hasattr(self, 'facing_right') and not self.facing_right:
                        self.image = pygame.transform.flip(self.image, True, False)
                else: # Fallback if the sprite in the list is not a Surface
                    self.image = pygame.Surface((self.largura if hasattr(self, 'largura') else 32, self.altura if hasattr(self, 'altura') else 32), pygame.SRCALPHA)
                    self.image.fill((50,0,0,150)) # Original placeholder color for Vampiro

        def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            if self.esta_vivo():
                if hasattr(player, 'rect') and player.rect is not None:
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
                self.atualizar_animacao()
                # Dano de contato
                agora_contato = pygame.time.get_ticks()
                if hasattr(player, 'rect') and player.rect is not None and \
                   hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                   self.rect.colliderect(player.rect) and \
                   (agora_contato - self.last_contact_time >= self.contact_cooldown):
                    if hasattr(player, 'receber_dano'):
                        player.receber_dano(self.contact_damage, self.rect)
                        self.last_contact_time = agora_contato

        def desenhar(self, janela, camera_x, camera_y):
            if not (hasattr(self, 'image') and self.image and isinstance(self.image, pygame.Surface)):
                self.image = pygame.Surface((getattr(self,'largura',32), getattr(self,'altura',32)), pygame.SRCALPHA)
                self.image.fill((50,0,0,150)) # Original placeholder color for Vampiro
            if not (hasattr(self, 'rect') and isinstance(self.rect, pygame.Rect)):
                 self.rect = self.image.get_rect(topleft=(getattr(self,'x',0), getattr(self,'y',0)))

            screen_x = self.rect.x - camera_x
            screen_y = self.rect.y - camera_y
            janela.blit(self.image, (screen_x, screen_y))

            current_time_flash = pygame.time.get_ticks()
            if hasattr(self, 'last_hit_time') and current_time_flash - self.last_hit_time < self.hit_flash_duration:
                flash_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                flash_surface.fill(self.hit_flash_color)
                janela.blit(flash_surface, (screen_x, screen_y), special_flags=pygame.BLEND_RGBA_ADD)

            if self.hp < self.max_hp and self.hp > 0:
                bar_width = self.rect.width
                bar_height = 5
                health_percentage = self.hp / self.max_hp
                current_bar_width = int(bar_width * health_percentage)
                bar_x = screen_x
                bar_y = screen_y - bar_height - 5
                pygame.draw.rect(janela, (200,0,0), (bar_x, bar_y, bar_width, bar_height), border_radius=2)
                pygame.draw.rect(janela, (0,200,0), (bar_x, bar_y, current_bar_width, bar_height), border_radius=2)
                pygame.draw.rect(janela, (255,255,255), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=2)

        def kill(self):
            super().kill()


class Vampiro(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None # Poderia ser 'transformar_morcego', 'mordida', etc.
    tamanho_sprite_definido = (70, 100) # Ajuste para o Vampiro

    som_ataque_vampiro = None
    som_dano_vampiro = None
    som_morte_vampiro = None
    som_transformacao_vampiro = None # Exemplo de som específico
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_vampiro(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Vampiro._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))
        caminho_log = os.path.normpath(caminho_completo)

        if not os.path.exists(caminho_completo):
            # print(f"DEBUG(Vampiro._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_log}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            # print(f"DEBUG(Vampiro._carregar_som): Som '{caminho_log}' carregado.")
            return som
        except pygame.error as e:
            # print(f"DEBUG(Vampiro._carregar_som): ERRO PYGAME ao carregar som '{caminho_log}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Vampiro._obter_pasta_raiz_jogo()
        # print(f"DEBUG(Vampiro._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {os.path.normpath(pasta_raiz_jogo)}")
        if lista_destino_existente is None: lista_destino_existente = [] # Garante que a lista exista

        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", os.sep))
            caminho_log = os.path.normpath(caminho_completo)
            # print(f"DEBUG(Vampiro._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_log}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                    # print(f"DEBUG(Vampiro._carregar_lista_sprites): Sprite '{caminho_log}' carregado para '{nome_animacao}'.")
                else:
                    # print(f"DEBUG(Vampiro._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_log}. Usando placeholder vermelho escuro.")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((80, 0, 0, 180)) # Placeholder vermelho escuro
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                # print(f"DEBUG(Vampiro._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_log}': {e}. Usando placeholder vermelho escuro.")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((80, 0, 0, 180))
                lista_destino_existente.append(placeholder)

        if not lista_destino_existente:
            # print(f"DEBUG(Vampiro._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final vermelho muito escuro.")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((50, 0, 0, 200))
            lista_destino_existente.append(placeholder)
        # A lista é modificada no local, não precisa retornar se for um atributo de classe


    @staticmethod
    def carregar_recursos_vampiro():
        if Vampiro.sprites_andar_carregados is None:
            Vampiro.sprites_andar_carregados = []
            # Substitua pelos caminhos reais dos sprites do Vampiro
            caminhos_andar = [
                "Sprites\\Inimigos\\Vampiro\\Imagem.png",
                "Sprites\\Inimigos\\Vampiro\\Imagem1.png",
            ]
            Vampiro._carregar_lista_sprites_estatico(
                caminhos_andar, Vampiro.sprites_andar_carregados,
                Vampiro.tamanho_sprite_definido, "Andar"
            )

        if Vampiro.sprites_atacar_carregados is None:
            Vampiro.sprites_atacar_carregados = []
            # Substitua pelos caminhos reais dos sprites de ataque do Vampiro
            caminhos_atacar = [
                "Sprites/Inimigos/Vampiro/Vampiro1.png",
                "Sprites/Inimigos/Vampiro/Vampiro2.png",
                "Sprites/Inimigos/Vampiro/Vampiro3.png",

            ]
            pasta_raiz_temp = Vampiro._obter_pasta_raiz_jogo()
            primeiro_sprite_ataque_existe = False
            if caminhos_atacar:
                caminho_primeiro_ataque = os.path.join(pasta_raiz_temp, caminhos_atacar[0].replace("\\", "/"))
                if os.path.exists(caminho_primeiro_ataque):
                    primeiro_sprite_ataque_existe = True

            if primeiro_sprite_ataque_existe:
                Vampiro._carregar_lista_sprites_estatico(
                    caminhos_atacar, Vampiro.sprites_atacar_carregados,
                    Vampiro.tamanho_sprite_definido, "Atacar"
                )

            if not Vampiro.sprites_atacar_carregados: # Fallback
                if Vampiro.sprites_andar_carregados and len(Vampiro.sprites_andar_carregados) > 0 :
                    Vampiro.sprites_atacar_carregados = [Vampiro.sprites_andar_carregados[0]]
                else:
                    placeholder_ataque = pygame.Surface(Vampiro.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder_ataque.fill((50,0,0, 180))
                    Vampiro.sprites_atacar_carregados = [placeholder_ataque]

        if not Vampiro.sons_carregados:
            # Vampiro.som_ataque_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/mordida.wav")
            # Vampiro.som_dano_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/dano_vampiro.wav")
            # Vampiro.som_morte_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/morte_poeira.wav")
            # Vampiro.som_transformacao_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/transformacao_morcego.wav")
            Vampiro.sons_carregados = True


    def __init__(self, x, y, velocidade=2.0):
        Vampiro.carregar_recursos_vampiro()

        vida_vampiro = 100
        dano_contato_vampiro = 10 # Dano baixo se o ataque principal for mordida
        xp_vampiro = 80
        self.moedas_drop = 15 # Exemplo de valor
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Vampiro/Vampiro_Andar1.png" # Exemplo

        super().__init__(
            x, y,
            Vampiro.tamanho_sprite_definido[0], Vampiro.tamanho_sprite_definido[1],
            vida_vampiro, velocidade, dano_contato_vampiro,
            xp_vampiro, sprite_path_principal_relativo_jogo
        )
        self.x = float(x)
        self.y = float(y)

        self.sprites_andar = Vampiro.sprites_andar_carregados
        self.sprites_atacar = Vampiro.sprites_atacar_carregados
        self.sprites = self.sprites_andar

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)) or \
           (self.sprites and len(self.sprites) > 0 and self.image is self.sprites[0] and self.sprites[0].get_size() != Vampiro.tamanho_sprite_definido):
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0].copy()
            else:
                placeholder_img = pygame.Surface(Vampiro.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((50, 0, 0, 150))
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


        self.sprite_index = 0
        self.intervalo_animacao_andar = 150
        self.intervalo_animacao_atacar = 100
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()

        self.is_attacking = False
        self.attack_duration = 0.6 # Duração da mordida
        self.attack_timer = 0.0
        self.attack_damage_especifico = 25 # Dano da mordida
        self.attack_range = 60  # Curto alcance para mordida
        self.attack_cooldown = 1.8
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)

        self.attack_hitbox_largura = Vampiro.tamanho_sprite_definido[0] * 0.6
        self.attack_hitbox_altura = Vampiro.tamanho_sprite_definido[1] * 0.4
        self.attack_hitbox_offset_x = Vampiro.tamanho_sprite_definido[0] * 0.3 # Quão à frente a mordida alcança
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_swing = False

        # Comportamentos específicos do Vampiro podem ser adicionados aqui
        # Ex: self.pode_transformar_morcego = True
        # self.tempo_ultima_transformacao = 0


    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0)
            return

        self.attack_hitbox.width = self.attack_hitbox_largura
        self.attack_hitbox.height = self.attack_hitbox_altura

        if self.facing_right:
            self.attack_hitbox.left = self.rect.centerx # Ajuste para a mordida começar mais à frente
            self.attack_hitbox.centery = self.rect.centery
        else:
            self.attack_hitbox.right = self.rect.centerx
            self.attack_hitbox.centery = self.rect.centery


    def atacar(self, player):
        if not (hasattr(player, 'rect') and self.esta_vivo()):
            return

        agora = pygame.time.get_ticks()
        distancia_ao_jogador = float('inf')
        if hasattr(player, 'rect') and player.rect is not None:
             distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                             self.rect.centery - player.rect.centery)

        if not self.is_attacking and \
           distancia_ao_jogador <= self.attack_range and \
           (agora - self.last_attack_time >= self.attack_cooldown * 1000):

            self.is_attacking = True
            self.attack_timer = agora
            self.last_attack_time = agora
            self.hit_player_this_attack_swing = False

            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = agora

            # if Vampiro.som_ataque_vampiro:
            #     Vampiro.som_ataque_vampiro.play()


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            return

        agora = pygame.time.get_ticks()
        if dt_ms is None:
            dt_ms = agora - getattr(self, '_last_update_time', agora)
            self._last_update_time = agora
            if dt_ms <= 0 : dt_ms = 16

        jogador_valido = (player is not None and hasattr(player, 'rect') and player.rect is not None and
                          hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and
                          hasattr(player, 'receber_dano'))

        if jogador_valido:
            if player.rect.centerx < self.rect.centerx:
                self.facing_right = False
            else:
                self.facing_right = True

        if self.is_attacking:
            self.atualizar_animacao()
            self._atualizar_hitbox_ataque()

            if jogador_valido and not self.hit_player_this_attack_swing and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico, self.rect)
                self.hit_player_this_attack_swing = True

            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_andar
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.sprite_index = 0
                self.tempo_ultimo_update_animacao = agora
                self.attack_hitbox.size = (0,0)
        else:
            if jogador_valido:
                self.atacar(player)

            if not self.is_attacking and self.velocidade > 0:
                if jogador_valido:
                     self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)

            self.atualizar_animacao()


        if jogador_valido and self.rect.colliderect(player.rect) and \
           (agora - self.last_contact_time >= self.contact_cooldown):
            player.receber_dano(self.contact_damage, self.rect)
            self.last_contact_time = agora

        if self.sprites and len(self.sprites) > 0:
            idx = int(self.sprite_index % len(self.sprites))
            current_sprite_image = self.sprites[idx]
            if not self.facing_right:
                self.image = pygame.transform.flip(current_sprite_image, True, False)
            else:
                self.image = current_sprite_image


    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if self.esta_vivo():
            if vida_antes > self.hp and Vampiro.som_dano_vampiro:
                Vampiro.som_dano_vampiro.play()
        elif vida_antes > 0 and Vampiro.som_morte_vampiro:
            Vampiro.som_morte_vampiro.play()

    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y)
