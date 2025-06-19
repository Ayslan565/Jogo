import pygame
import random
import math
import time
import os

# --- Importação da Classe Base Inimigo ---
try:
    # Importação relativa para a classe base Inimigo
    from .Inimigos import Inimigo as InimigoBase
except ImportError as e:
    # Placeholder para InimigoBase caso a importação falhe
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((255, 0, 255, 100))
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value; self.facing_right = True
            self.last_hit_time = 0; self.hit_flash_duration = 150; self.contact_cooldown = 1000
            self.last_contact_time = pygame.time.get_ticks() - self.contact_cooldown
            self.sprites = [self.image.copy()]; self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks(); self.intervalo_animacao = 200
            self.moedas_drop = 0

        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None): pass
        def atualizar_animacao(self): pass
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): pass
        def desenhar(self, janela, camera_x, camera_y):
            if hasattr(self, 'image') and self.image:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self): super().kill()


class Demonio(InimigoBase):
    sprites_originais = None
    tamanho_sprite_definido = (96, 96)
    som_ataque_demonio, som_dano_demonio, som_morte_demonio, som_spawn_demonio = None, None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))

    @staticmethod
    def _carregar_som_demonio(caminho_relativo):
        caminho_completo = os.path.join(Demonio._obter_pasta_raiz_jogo(), caminho_relativo.replace("/", os.sep))
        if not os.path.exists(caminho_completo): return None
        try: return pygame.mixer.Sound(caminho_completo)
        except pygame.error: return None

    @staticmethod
    def carregar_recursos_demonio():
        if Demonio.sprites_originais is None:
            Demonio.sprites_originais = []
            # MODIFICADO: Lista explícita com os caminhos completos relativos à raiz do projeto
            caminhos_sprites = [
                "Sprites\\Inimigos\\Demonio\\A (1).png",
                "Sprites\\Inimigos\\Demonio\\A (2).png",
                "Sprites\\Inimigos\\Demonio\\A (3).png",
                "Sprites\\Inimigos\\Demonio\\A (4).png",
                "Sprites\\Inimigos\\Demonio\\A (5).png",
            ]
            pasta_raiz = Demonio._obter_pasta_raiz_jogo()
            for caminho_relativo in caminhos_sprites:
                caminho_completo = os.path.join(pasta_raiz, caminho_relativo.replace("/", os.sep))
                try:
                    if os.path.exists(caminho_completo):
                        sprite_img = pygame.image.load(caminho_completo).convert_alpha()
                        sprite_scaled = pygame.transform.scale(sprite_img, Demonio.tamanho_sprite_definido)
                        Demonio.sprites_originais.append(sprite_scaled)
                    else:
                        placeholder = pygame.Surface(Demonio.tamanho_sprite_definido, pygame.SRCALPHA); placeholder.fill((200, 0, 0)); Demonio.sprites_originais.append(placeholder)
                except pygame.error:
                    placeholder = pygame.Surface(Demonio.tamanho_sprite_definido, pygame.SRCALPHA); placeholder.fill((200, 0, 0)); Demonio.sprites_originais.append(placeholder)
            
            if not Demonio.sprites_originais:
                placeholder = pygame.Surface(Demonio.tamanho_sprite_definido, pygame.SRCALPHA); placeholder.fill((150, 0, 0)); Demonio.sprites_originais.append(placeholder)

        if not Demonio.sons_carregados:
            # Carregar sons aqui...
            Demonio.sons_carregados = True

    def __init__(self, x, y, velocidade=2.5):
        Demonio.carregar_recursos_demonio()

        super().__init__(x, y,
                         Demonio.tamanho_sprite_definido[0], Demonio.tamanho_sprite_definido[1],
                         vida_maxima=90, 
                         velocidade=velocidade, 
                         dano_contato=10,
                         xp_value=75, 
                         sprite_path="Sprites/Inimigos/Demonio/A(1).png")
        self.moedas_drop = 12
        
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
        self.hit_player_this_attack = False

        if self.sprites: self.image = self.sprites[0]
        else: self.image = pygame.Surface(self.tamanho_sprite_definido, pygame.SRCALPHA); self.image.fill((200,0,0))
        
        self.rect = self.image.get_rect(topleft=(x, y))

    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        # ... (lógica de som)

    def atacar(self, player):
        if not hasattr(player, 'rect'): return
        current_time = time.time()
        if self.esta_vivo() and not self.is_attacking and (current_time - self.last_attack_time >= self.attack_cooldown):
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
            if distancia_ao_jogador <= self.attack_range:
                self.is_attacking = True
                self.attack_timer = current_time
                self.last_attack_time = current_time
                self.hit_player_this_attack = False
                self.attack_hitbox = pygame.Rect(0, 0, *self.attack_hitbox_size)
                self.attack_hitbox.center = self.rect.center
                # ... (lógica de som)

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            self.kill() # O GerenciadorDeInimigos cuidará das recompensas.
            return

        jogador_valido = (player and hasattr(player, 'rect') and player.esta_vivo())
        if not jogador_valido:
            if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()
            return
        
        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)

        if self.is_attacking:
            self.attack_hitbox.center = self.rect.center
            if time.time() - self.attack_timer >= self.attack_duration:
                self.is_attacking = False
                self.hit_player_this_attack = False
            elif not self.hit_player_this_attack and self.attack_hitbox.colliderect(player.rect_colisao):
                if player.esta_vivo():
                    player.receber_dano(self.attack_damage, self.rect)
                    self.hit_player_this_attack = True
        else:
            self.atacar(player)
            
    def desenhar(self, surface, camera_x, camera_y):
        # O método da classe base agora cuida de tudo
        super().desenhar(surface, camera_x, camera_y)
