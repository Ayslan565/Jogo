# Urso.py
import pygame
import os
import math
import time

# Removido: importação do score_manager, pois a lógica de recompensa é tratada pelo GerenciadorDeInimigos

# --- Importação da Classe Base Inimigo ---
try:
    # Correção: Importação relativa para a classe base Inimigo dentro do mesmo pacote 'Inimigos'
    from .Inimigos import Inimigo as InimigoBase
except ImportError as e:
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((100, 70, 30, 100))
            pygame.draw.rect(self.image, (139,69,19), self.image.get_rect(), 1)
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            self.x = float(x); self.y = float(y)
            self.moedas_drop = 0

        def _carregar_sprite(self, path, tamanho):
            img = pygame.Surface(tamanho, pygame.SRCALPHA); img.fill((139,69,19, 128)); return img
        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt_ms=None): pass
        def atualizar_animacao(self):
            if self.sprites: self.image = self.sprites[0]
            if hasattr(self, 'facing_right') and not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self): super().kill()


class Urso(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (130, 110)
    som_ataque_urso, som_dano_urso, som_morte_urso, som_rugido_urso = None, None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho, nome_anim):
        pasta_raiz = Urso._obter_pasta_raiz_jogo()
        if lista_destino is None: lista_destino = []
        for path_relativo in caminhos:
            caminho_completo = os.path.join(pasta_raiz, path_relativo.replace("\\", "/"))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                else:
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((139, 69, 19, 180)); lista_destino.append(placeholder)
            except pygame.error:
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((139, 69, 19, 180)); lista_destino.append(placeholder)
        if not lista_destino:
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((100, 70, 30, 200)); lista_destino.append(placeholder)
        return lista_destino

    @staticmethod
    def carregar_recursos_urso():
        if Urso.sprites_andar_carregados is None:
            # --- CORREÇÃO APLICADA AQUI ---
            # Lista manual para carregar todos os 4 sprites corretamente
            caminhos_andar = [
                "Sprites/Inimigos/Urso/Urso.png",
                "Sprites/Inimigos/Urso/Urso 2.png",
                "Sprites/Inimigos/Urso/Urso 3.png",
                "Sprites/Inimigos/Urso/Urso 4.png"
            ]
            Urso.sprites_andar_carregados = []
            Urso._carregar_lista_sprites_estatico(caminhos_andar, Urso.sprites_andar_carregados, Urso.tamanho_sprite_definido, "Andar")
        
        if Urso.sprites_atacar_carregados is None:
            # --- CORREÇÃO APLICADA AQUI ---
            # Define que os sprites de ataque são os mesmos de andar
            Urso.sprites_atacar_carregados = Urso.sprites_andar_carregados

        if not Urso.sons_carregados:
            # Carregar sons aqui
            Urso.sons_carregados = True

    def __init__(self, x, y, velocidade=1.3):
        Urso.carregar_recursos_urso()

        vida_urso = 60
        dano_contato_urso = 25
        xp_urso = 130
        self.moedas_drop = 18
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Urso/Urso.png"

        super().__init__(
            x, y,
            Urso.tamanho_sprite_definido[0], Urso.tamanho_sprite_definido[1],
            vida_urso, velocidade, dano_contato_urso,
            xp_urso, sprite_path_principal_relativo_jogo
        )

        self.sprites_andar = Urso.sprites_andar_carregados
        self.sprites_atacar = Urso.sprites_atacar_carregados
        self.sprites = self.sprites_andar

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            if self.sprites: self.image = self.sprites[0]
            else:
                self.image = pygame.Surface(Urso.tamanho_sprite_definido, pygame.SRCALPHA); self.image.fill((100, 70, 30, 150))
                if not self.sprites: self.sprites = [self.image]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.sprite_index = 0
        self.intervalo_animacao_andar = 220 # Ajustado para 4 frames
        self.intervalo_animacao_atacar = 180 # Um pouco mais rápido para o ataque
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.is_attacking = False
        self.attack_duration = 0.9
        self.attack_timer = 0.0
        self.attack_damage_especifico = 40
        self.attack_range = 90
        self.attack_cooldown = 3.0
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)
        self.attack_hitbox_largura = Urso.tamanho_sprite_definido[0] * 0.6
        self.attack_hitbox_altura = Urso.tamanho_sprite_definido[1] * 0.4
        self.attack_hitbox_offset_x = 30
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_swing = False

    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0); return
        self.attack_hitbox.size = (self.attack_hitbox_largura, self.attack_hitbox_altura)
        if self.facing_right:
            self.attack_hitbox.left = self.rect.right - self.attack_hitbox_offset_x / 2
            self.attack_hitbox.centery = self.rect.centery
        else:
            self.attack_hitbox.right = self.rect.left + self.attack_hitbox_offset_x / 2
            self.attack_hitbox.centery = self.rect.centery

    def atacar(self, player):
        if not (hasattr(player, 'rect') and self.esta_vivo()): return
        agora = pygame.time.get_ticks()
        distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
        if not self.is_attacking and distancia_ao_jogador <= self.attack_range and (agora - self.last_attack_time >= self.attack_cooldown * 1000):
            self.is_attacking = True
            self.attack_timer = agora
            self.last_attack_time = agora
            self.hit_player_this_attack_swing = False
            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            self.kill()
            return

        agora = pygame.time.get_ticks()
        jogador_valido = (player and hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo'))

        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)

        if self.is_attacking:
            if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()
            self._atualizar_hitbox_ataque()
            if jogador_valido and not self.hit_player_this_attack_swing and self.attack_hitbox.colliderect(player.rect):
                if hasattr(player, 'receber_dano'): player.receber_dano(self.attack_damage_especifico)
                self.hit_player_this_attack_swing = True
            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_andar
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.sprite_index = 0
                self.attack_hitbox.size = (0,0)
        else:
            if jogador_valido: self.atacar(player)
            
        if jogador_valido and self.rect.colliderect(player.rect) and (agora - self.last_contact_time >= self.contact_cooldown):
            if hasattr(player, 'receber_dano'): player.receber_dano(self.contact_damage)
            self.last_contact_time = agora

    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if not self.esta_vivo() and vida_antes > 0 and Urso.som_morte_urso:
            Urso.som_morte_urso.play()
        elif self.esta_vivo() and vida_antes > self.hp and Urso.som_dano_urso:
            Urso.som_dano_urso.play()