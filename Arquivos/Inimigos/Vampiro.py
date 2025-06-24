# Vampiro.py
import pygame
import random
import math
import time
import os

# --- Importação da Classe Base Inimigo ---
try:
    from .Inimigos import Inimigo as InimigoBase
except ImportError as e:
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (100, 100, 100), (0, 0, largura, altura))
            vida_maxima = 60
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.contact_cooldown = 1000; self.last_contact_time = pygame.time.get_ticks()
            self.sprites = [self.image]; self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks(); self.intervalo_animacao = 200
            self.moedas_drop = 0
            self.x = float(x)
            self.y = float(y)

        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None): pass
        def atualizar_animacao(self):
             if self.sprites and len(self.sprites) > 0: self.image = self.sprites[0]
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self): super().kill()

class Vampiro(InimigoBase):
    sprites_andar, sprites_atacar = None, None
    tamanho_sprite_definido = (80, 90)
    som_ataque_vampiro, som_dano_vampiro, som_morte_vampiro = None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho):
        pasta_raiz = Vampiro._obter_pasta_raiz_jogo()
        if lista_destino is None: lista_destino = []
        for path_relativo in caminhos:
            caminho_completo = os.path.join(pasta_raiz, path_relativo.replace("\\", "/"))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                else:
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((100, 100, 120, 180)); lista_destino.append(placeholder)
            except pygame.error:
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((100, 100, 120, 180)); lista_destino.append(placeholder)
        if not lista_destino:
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((80, 80, 100, 200)); lista_destino.append(placeholder)
        return lista_destino

    @staticmethod
    def carregar_recursos_vampiro():
        if Vampiro.sprites_andar is None:
            caminhos_andar = ["Sprites/Inimigos/Vampiro/Imagem.png", "Sprites/Inimigos/Vampiro/Imagem1.png"]
            Vampiro.sprites_andar = Vampiro._carregar_lista_sprites_estatico(caminhos_andar, [], Vampiro.tamanho_sprite_definido)
        
        if Vampiro.sprites_atacar is None:
            caminhos_atacar = [
                "Sprites/Inimigos/Vampiro/Vampiro1.png", 
                "Sprites/Inimigos/Vampiro/Vampiro2.png", 
                "Sprites/Inimigos/Vampiro/Vampiro3.png"
            ]
            Vampiro.sprites_atacar = Vampiro._carregar_lista_sprites_estatico(caminhos_atacar, [], Vampiro.tamanho_sprite_definido)
            if not Vampiro.sprites_atacar and Vampiro.sprites_andar:
                Vampiro.sprites_atacar = [Vampiro.sprites_andar[0]]
        
        if not Vampiro.sons_carregados:
            # Carregar sons aqui
            Vampiro.sons_carregados = True

    def __init__(self, x, y, velocidade=80):
        Vampiro.carregar_recursos_vampiro()

        vampiro_hp = 90
        vampiro_contact_damage = 8
        vampiro_xp_value = 60
        self.moedas_drop = 25
        sprite_path_ref = "Sprites/Inimigos/Vampiro/Imagem.png"

        super().__init__(x, y,
                         Vampiro.tamanho_sprite_definido[0], Vampiro.tamanho_sprite_definido[1],
                         vampiro_hp, velocidade, vampiro_contact_damage,
                         vampiro_xp_value, sprite_path_ref)
        
        self.x = float(x)
        self.y = float(y)

        self.sprites_andar = Vampiro.sprites_andar
        self.sprites_atacar = Vampiro.sprites_atacar
        self.sprites = self.sprites_andar
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.sprite_index = 0
        self.intervalo_animacao_andar = 150
        self.intervalo_animacao_atacar = 120
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()

        self.is_attacking = False
        self.attack_duration = 3 * self.intervalo_animacao_atacar # Duração baseada nos frames de ataque
        self.attack_timer = 0
        self.attack_damage = 25
        self.attack_range = 60 # Reduzido para um ataque corpo a corpo
        self.attack_cooldown = 1800 # Em milissegundos
        self.last_attack_time = pygame.time.get_ticks() - self.attack_cooldown
        self.attack_hitbox = None
        self.hit_player_this_attack = False

    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if not self.esta_vivo() and vida_antes > 0 and self.som_morte_vampiro:
            self.som_morte_vampiro.play()
        elif self.esta_vivo() and vida_antes > self.hp and self.som_dano_vampiro:
            self.som_dano_vampiro.play()

    def mover_em_direcao(self, alvo_x, alvo_y, dt_ms):
        if dt_ms is None or dt_ms <= 0:
            return
            
        direcao_x = alvo_x - self.x
        direcao_y = alvo_y - self.y
        distancia = math.hypot(direcao_x, direcao_y)

        if distancia > 0:
            direcao_x /= distancia
            direcao_y /= distancia
            
            fator_tempo = dt_ms / 1000.0
            movimento_x = direcao_x * self.velocidade * fator_tempo
            movimento_y = direcao_y * self.velocidade * fator_tempo
            
            self.x += movimento_x
            self.y += movimento_y
            self.rect.center = (int(self.x), int(self.y))
            
            if movimento_x > 0.1: self.facing_right = True
            elif movimento_x < -0.1: self.facing_right = False

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            return

        agora = pygame.time.get_ticks()
        jogador_valido = (player and hasattr(player, 'esta_vivo') and player.esta_vivo())
        
        if not jogador_valido:
            self.atualizar_animacao()
            return

        distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)

        # Lógica de ataque
        if self.is_attacking:
            # Termina o ataque após a duração
            if agora - self.attack_timer > self.attack_duration:
                self.is_attacking = False
                self.sprites = self.sprites_andar
                self.intervalo_animacao = self.intervalo_animacao_andar
            else:
                # Verifica a colisão durante o ataque
                if not self.hit_player_this_attack:
                    # Cria uma hitbox de ataque temporária à frente do vampiro
                    hitbox_offset_x = 30 if self.facing_right else -30
                    attack_hitbox = pygame.Rect(
                        self.rect.centerx + hitbox_offset_x - 20,
                        self.rect.centery - 25,
                        40, 50
                    )
                    if attack_hitbox.colliderect(player.rect):
                        player.receber_dano(self.attack_damage, self.rect)
                        self.hit_player_this_attack = True
        
        # Lógica de movimento e decisão de atacar
        else: 
            # Verifica se está no alcance para atacar
            if distancia_ao_jogador <= self.attack_range and agora - self.last_attack_time >= self.attack_cooldown:
                self.is_attacking = True
                self.attack_timer = agora
                self.last_attack_time = agora
                self.hit_player_this_attack = False
                self.sprites = self.sprites_atacar
                self.intervalo_animacao = self.intervalo_animacao_atacar
                self.sprite_index = 0
            
            # Se não estiver atacando, move-se em direção ao jogador
            else:
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)

        self.atualizar_animacao()

        # O dano de contato direto é gerido pelo GerenciadorDeInimigos para todos os inimigos
