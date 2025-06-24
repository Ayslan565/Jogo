import pygame
import os
import math
import time

# --- Importação da Classe Base Inimigo ---
try:
    from .Inimigos import Inimigo as InimigoBase
except ImportError:
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((180, 200, 230, 100)) 
            pygame.draw.rect(self.image, (200,220,255), self.image.get_rect(), 1)
            self.hp = vida_maxima
            self.max_hp = vida_maxima
            self.velocidade = velocidade
            self.contact_damage = dano_contato
            self.xp_value = xp_value
            self.facing_right = True
            self.last_hit_time = 0 
            self.hit_flash_duration = 150 
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000 
            self.last_contact_time = pygame.time.get_ticks() - self.contact_cooldown
            self.sprites = [self.image.copy()]
            self.sprite_index = 0
            self.intervalo_animacao = 200
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.moedas_drop = 50
            self.x = float(x)
            self.y = float(y)
        def receber_dano(self, dano, fonte_dano_rect=None):
            self.hp = max(0, self.hp - dano)
            self.last_hit_time = pygame.time.get_ticks()
        def esta_vivo(self):
            return self.hp > 0
        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None):
            if dt_ms is None: dt_factor = 1.0
            else: dt_factor = dt_ms / 1000.0
            dx = alvo_x - self.rect.centerx
            dy = alvo_y - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                dx_norm = dx / dist
                dy_norm = dy / dist
                move_amount = self.velocidade * dt_factor
                if move_amount > dist: move_amount = dist
                self.x += dx_norm * move_amount
                self.y += dy_norm * move_amount
                self.rect.x = int(self.x)
                self.rect.y = int(self.y)
                if dx_norm > 0: self.facing_right = True
                elif dx_norm < 0: self.facing_right = False
        def atualizar_animacao(self):
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
                self.tempo_ultimo_update_animacao = tempo_atual
            current_sprite = self.sprites[self.sprite_index]
            if not self.facing_right: self.image = pygame.transform.flip(current_sprite, True, False)
            else: self.image = current_sprite
            if tempo_atual - self.last_hit_time < self.hit_flash_duration:
                flash_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                flash_surface.fill(self.hit_flash_color)
                self.image.blit(flash_surface, (0, 0))
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            self.atualizar_animacao()
            if player and hasattr(player, 'rect') and player.esta_vivo():
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self):
            super().kill()

try:
    from score import score_manager
except ImportError:
    class ScoreManagerPlaceholder:
        def adicionar_xp(self, xp_value):
            pass
    score_manager = ScoreManagerPlaceholder()


class Golem_Neve(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (170, 160)

    som_ataque_golem = None
    som_dano_golem = None
    som_morte_golem = None
    som_spawn_golem = None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_golem_neve(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Golem_Neve._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("/", os.sep))
        if not os.path.exists(caminho_completo): return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            return som
        except pygame.error as e:
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Golem_Neve._obter_pasta_raiz_jogo()
        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("/", os.sep))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino.append(sprite)
                else:
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((200, 220, 255, 180))
                    lista_destino.append(placeholder)
            except pygame.error as e:
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((200, 220, 255, 180))
                lista_destino.append(placeholder)
        if not lista_destino:
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((180, 200, 230, 200))
            lista_destino.append(placeholder)

    @staticmethod
    def carregar_recursos_golem_neve():
        # Carregar sprites de andar
        if Golem_Neve.sprites_andar_carregados is None:
            Golem_Neve.sprites_andar_carregados = []
            caminhos_andar = [
                "Sprites/Inimigos/Golem Neve/GN1.png",
                "Sprites/Inimigos/Golem Neve/GN2.png",
                "Sprites/Inimigos/Golem Neve/GN3.png",
            ]
            Golem_Neve._carregar_lista_sprites_estatico(
                caminhos_andar,
                Golem_Neve.sprites_andar_carregados,
                Golem_Neve.tamanho_sprite_definido,
                "Andar"
            )

        # --- CORREÇÃO APLICADA AQUI ---
        # Carregar sprites de atacar (usando os mesmos de andar)
        if Golem_Neve.sprites_atacar_carregados is None:
            # Atribui a lista de sprites de andar já carregada para os de ataque
            Golem_Neve.sprites_atacar_carregados = Golem_Neve.sprites_andar_carregados

        if not Golem_Neve.sons_carregados:
            Golem_Neve.sons_carregados = True


    def __init__(self, x, y, velocidade=1):
        Golem_Neve.carregar_recursos_golem_neve()

        vida_golem = 250
        dano_contato_golem = 50
        xp_golem = 600
        moedas_dropadas = 25
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Golem Neve/GN1.png"

        super().__init__(
            x, y,
            Golem_Neve.tamanho_sprite_definido[0], Golem_Neve.tamanho_sprite_definido[1],
            vida_golem, velocidade, dano_contato_golem,
            xp_golem, sprite_path_principal_relativo_jogo
        )

        self.moedas_drop = moedas_dropadas
        self.sprites_andar = Golem_Neve.sprites_andar_carregados
        self.sprites_atacar = Golem_Neve.sprites_atacar_carregados
        self.sprites = self.sprites_andar

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
            else:
                placeholder_img = pygame.Surface(Golem_Neve.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((150,180,210, 150))
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.sprite_index = 0
        self.intervalo_animacao_andar = 380
        self.intervalo_animacao_atacar = 280
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.is_attacking = False
        self.attack_duration = 1.0
        self.attack_timer = 0.0
        self.attack_damage_especifico = 25
        self.attack_range = 80 # Aumentado para o golem atacar um pouco antes
        self.attack_cooldown = 3.8
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)
        self.attack_hitbox_largura = self.tamanho_sprite_definido[0] * 0.7
        self.attack_hitbox_altura = self.tamanho_sprite_definido[1] * 0.5
        self.attack_hitbox_offset_x = 30
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_swing = False
        self.ouro_concedido = False

    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0)
            return
        self.attack_hitbox.width = self.attack_hitbox_largura
        self.attack_hitbox.height = self.attack_hitbox_altura
        if self.facing_right:
            self.attack_hitbox.midleft = (self.rect.right - self.attack_hitbox_offset_x, self.rect.centery)
        else:
            self.attack_hitbox.midright = (self.rect.left + self.attack_hitbox_offset_x, self.rect.centery)

    def atacar(self, player):
        if not (hasattr(player, 'rect') and self.esta_vivo()):
            return
        agora = pygame.time.get_ticks()
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

    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            if not self.ouro_concedido:
                if hasattr(player, "dinheiro"):
                    player.dinheiro += self.moedas_drop
                score_manager.adicionar_xp(self.xp_value)
                self.ouro_concedido = True
            self.kill()
            return
        agora = pygame.time.get_ticks()
        jogador_valido = (player and
                          hasattr(player, 'rect') and
                          hasattr(player, 'vida') and
                          hasattr(player.vida, 'esta_vivo') and
                          player.vida.esta_vivo() and
                          hasattr(player, 'receber_dano'))
        if self.is_attacking:
            self.atualizar_animacao()
            self._atualizar_hitbox_ataque()
            if jogador_valido and not self.hit_player_this_attack_swing and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico)
                self.hit_player_this_attack_swing = True
            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_andar
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.sprite_index = 0
                self.attack_hitbox.size = (0,0)
        else:
            if jogador_valido:
                self.atacar(player)
            if not self.is_attacking and jogador_valido:
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
            self.atualizar_animacao()
        if jogador_valido and self.rect.colliderect(player.rect) and \
           (agora - self.last_contact_time >= self.contact_cooldown):
            player.receber_dano(self.contact_damage)
            self.last_contact_time = agora

    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if self.esta_vivo():
            if vida_antes > self.hp and Golem_Neve.som_dano_golem:
                pass
        elif vida_antes > 0:
            if Golem_Neve.som_morte_golem:
                pass