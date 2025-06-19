# Vampiro.py
import pygame
import random
import math
import time
import os

# Removido: importação do score_manager, pois a lógica de recompensa é tratada pelo GerenciadorDeInimigos

# --- Importação da Classe Base Inimigo ---
try:
    # Correção: Importação relativa para a classe base Inimigo dentro do mesmo pacote 'Inimigos'
    from .Inimigos import Inimigo as InimigoBase
    # print("DEBUG(Vampiro): Classe base Inimigo importada com sucesso.")
except ImportError as e:
    # print(f"DEBUG(Vampiro): ERRO: Módulo 'Inimigos.py' não encontrado. Usando classe Inimigo placeholder: {e}.")
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (100, 100, 100), (0, 0, largura, altura))
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = pygame.time.get_ticks()
            self.sprites = [self.image]; self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks(); self.intervalo_animacao = 200
            self.moedas_drop = 0 # Adicionado para compatibilidade, mesmo que a lógica seja externa

        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None): pass
        def atualizar_animacao(self):
            if self.sprites: self.image = self.sprites[0]
        # Padronizado a assinatura do update do placeholder para consistência
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            # Placeholder de update, a lógica real estará nas classes filhas
            self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self): super().kill()

class Vampiro(InimigoBase):
    sprites_andar, sprites_atacar, sprites_idle = None, None, None
    tamanho_sprite_definido = (80, 90)
    som_ataque_vampiro, som_dano_vampiro, som_morte_vampiro, som_teleporte_vampiro = None, None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho, nome_anim):
        pasta_raiz = Vampiro._obter_pasta_raiz_jogo()
        if lista_destino is None: lista_destino = [] # Garante que lista_destino é uma lista
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
        return lista_destino # Retorna a lista modificada

    @staticmethod
    def carregar_recursos_vampiro():
        if Vampiro.sprites_andar is None:
            caminhos_andar = ["Sprites/Inimigos/Vampiro/Imagem.png", "Sprites/Inimigos/Vampiro/Imagem1.png"]
            Vampiro.sprites_andar = []
            Vampiro._carregar_lista_sprites_estatico(caminhos_andar, Vampiro.sprites_andar, Vampiro.tamanho_sprite_definido, "Andar")
        if Vampiro.sprites_atacar is None:
            caminhos_atacar = [
                "Sprites/Inimigos/Vampiro/Vampiro1.png", 
                "Sprites/Inimigos/Vampiro/Vampiro2.png", 
                "Sprites/Inimigos/Vampiro/Vampiro3.png"
            ]
            Vampiro.sprites_atacar = []
            Vampiro._carregar_lista_sprites_estatico(caminhos_atacar, Vampiro.sprites_atacar, Vampiro.tamanho_sprite_definido, "Atacar")
            if not Vampiro.sprites_atacar and Vampiro.sprites_andar:
                Vampiro.sprites_atacar = [Vampiro.sprites_andar[0]]
        if not Vampiro.sons_carregados:
            # Carregar sons aqui
            Vampiro.sons_carregados = True

    def __init__(self, x, y, velocidade=3.5):
        Vampiro.carregar_recursos_vampiro()

        vampiro_hp = 90
        vampiro_contact_damage = 8
        vampiro_xp_value = 60
        self.moedas_drop = 25
        sprite_path_ref = "Sprites/Inimigos/Vampiro/Vampiro1.png"

        super().__init__(x, y,
                         Vampiro.tamanho_sprite_definido[0], Vampiro.tamanho_sprite_definido[1],
                         vampiro_hp, velocidade, vampiro_contact_damage,
                         vampiro_xp_value, sprite_path_ref)

        # Removido: Flag self.recursos_concedidos, pois a lógica de recompensa é externa

        self.sprites = Vampiro.sprites_andar if Vampiro.sprites_andar else [self.image]
        self.sprite_index = 0
        self.intervalo_animacao_andar = 150
        self.intervalo_animacao_atacar = 100
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()

        self.is_attacking = False
        self.attack_duration = 0.4
        self.attack_timer = 0.0
        self.attack_damage = 25
        self.attack_range = 80
        self.attack_cooldown = 1.8
        self.last_attack_time = time.time() - self.attack_cooldown
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.hit_player_this_attack = False

        self.can_dash = True
        self.dash_cooldown = 5.0
        self.last_dash_time = time.time() - self.dash_cooldown
        self.dash_range = 200
        self.is_dashing = False
        self.dash_duration = 0.2
        self.dash_timer = 0.0
        self.dash_target_pos = None

        if self.sprites: self.image = self.sprites[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def receber_dano(self, dano, fonte_dano_rect=None): # Assinatura Padrão
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if not self.esta_vivo() and vida_antes > 0 and self.som_morte_vampiro:
            self.som_morte_vampiro.play()
        elif self.esta_vivo() and vida_antes > self.hp and self.som_dano_vampiro:
            self.som_dano_vampiro.play()

    def atacar(self, player):
        if not (hasattr(player, 'rect') and self.esta_vivo()): return
        current_time = time.time()
        if not self.is_attacking and not self.is_dashing and (current_time - self.last_attack_time >= self.attack_cooldown):
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
            if distancia_ao_jogador <= self.attack_range:
                self.is_attacking = True
                self.attack_timer = current_time
                self.last_attack_time = current_time
                self.hit_player_this_attack = False
                self.sprites = Vampiro.sprites_atacar if Vampiro.sprites_atacar else Vampiro.sprites_andar
                self.intervalo_animacao = self.intervalo_animacao_atacar
                self.sprite_index = 0
                self.attack_hitbox = pygame.Rect(0, 0, 50, 50)

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        # Lógica de recompensa ao morrer foi movida para GerenciadorDeInimigos.py
        if not self.esta_vivo():
            self.kill() # O GerenciadorDeInimigos.py cuidará das recompensas e remoção
            return

        jogador_valido = (player and hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo'))
        if not jogador_valido:
            if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()
            return

        # Lógica de dash/teleporte
        current_time = time.time()
        if self.can_dash and not self.is_dashing and jogador_valido and \
           (current_time - self.last_dash_time >= self.dash_cooldown) and \
           math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery) > self.dash_range * 1.5:
            self.is_dashing = True
            self.dash_timer = current_time
            self.last_dash_time = current_time
            # Define um ponto alvo para o dash próximo ao jogador
            angle = math.atan2(player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)
            dash_x = player.rect.centerx - math.cos(angle) * (self.dash_range * 0.8) # Um pouco antes do jogador
            dash_y = player.rect.centery - math.sin(angle) * (self.dash_range * 0.8)
            self.dash_target_pos = (dash_x, dash_y)
            # if Vampiro.som_teleporte_vampiro: Vampiro.som_teleporte_vampiro.play()
            self.velocidade_original = self.velocidade # Salva a velocidade original
            self.velocidade *= 5 # Aumenta a velocidade durante o dash
            self.intervalo_animacao = 50 # Animação mais rápida durante o dash
            self.sprite_index = 0

        if self.is_dashing:
            if current_time - self.dash_timer < self.dash_duration:
                # Move em direção ao ponto alvo do dash
                if self.dash_target_pos:
                    self.mover_em_direcao(self.dash_target_pos[0], self.dash_target_pos[1], dt_ms)
            else:
                self.is_dashing = False
                self.velocidade = self.velocidade_original # Restaura a velocidade
                self.intervalo_animacao = self.intervalo_animacao_andar # Restaura a animação
                self.dash_target_pos = None # Reseta o alvo do dash

        # Lógica de ataque e movimento (só se não estiver em dash)
        if not self.is_dashing:
            if self.is_attacking:
                self.attack_hitbox.center = self.rect.center
                if not self.hit_player_this_attack and self.attack_hitbox.colliderect(player.rect):
                    if hasattr(player, 'receber_dano'): player.receber_dano(self.attack_damage, self.rect)
                    self.hit_player_this_attack = True
                if time.time() - self.attack_timer > self.attack_duration:
                    self.is_attacking = False
                    self.sprites = self.sprites_andar
                    self.intervalo_animacao = self.intervalo_animacao_andar
            else:
                self.atacar(player)
                if hasattr(self, 'mover_em_direcao'):
                     self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
        
        # Atualização da animação (agora após a lógica de dash e ataque)
        if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()

        # Dano de contato (fora da lógica de dash e ataque direto)
        if jogador_valido and self.rect.colliderect(player.rect) and \
           (pygame.time.get_ticks() - self.last_contact_time >= self.contact_cooldown):
            if hasattr(player, 'receber_dano'):
                player.receber_dano(self.contact_damage, self.rect)
                self.last_contact_time = pygame.time.get_ticks()
