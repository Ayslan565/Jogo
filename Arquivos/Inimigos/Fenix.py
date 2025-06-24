# Fenix.py
import pygame
import os
import math
import time

# Removido: importação do score_manager, pois a lógica de recompensa é tratada pelo GerenciadorDeInimigos

# --- Importação da Classe Base Inimigo ---
try:
    from .Inimigos import Inimigo as InimigoBase
    # print(f"DEBUG(Fenix): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Fenix): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((180, 100, 50, 100))
            pygame.draw.rect(self.image, (255,140,0), self.image.get_rect(), 1)
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            self.x = float(x); self.y = float(y)
            self.moedas_drop = 250 # Adicionado para compatibilidade, mesmo que a lógica seja externa

        def _carregar_sprite(self, path, tamanho):
            img = pygame.Surface(tamanho, pygame.SRCALPHA); img.fill((255,165,0, 128)); return img
        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt=None): pass
        def atualizar_animacao(self):
            if self.sprites: self.image = self.sprites[0]
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            # Placeholder de update, a lógica real estará nas classes filhas
            if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self): super().kill()


class Fenix(InimigoBase):
    sprites_voo_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (100, 100)
    som_ataque_fenix, som_dano_fenix, som_morte_fenix, som_voo_fenix = None, None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho, nome_anim):
        pasta_raiz = Fenix._obter_pasta_raiz_jogo()
        for path_relativo in caminhos:
            caminho_completo = os.path.join(pasta_raiz, path_relativo.replace("\\", "/"))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                else:
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((255, 165, 0, 180)); lista_destino.append(placeholder)
            except pygame.error:
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((255, 165, 0, 180)); lista_destino.append(placeholder)
        if not lista_destino:
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((200, 100, 0, 200)); lista_destino.append(placeholder)

    @staticmethod
    def carregar_recursos_fenix():
        if Fenix.sprites_voo_carregados is None:
            Fenix.sprites_voo_carregados = []
            caminhos = ["Sprites/Inimigos/Fenix/Fenix {}.png".format(i) for i in range(1, 5)]
            Fenix._carregar_lista_sprites_estatico(caminhos, Fenix.sprites_voo_carregados, Fenix.tamanho_sprite_definido, "Voo/Idle")
            if not Fenix.sprites_atacar_carregados and Fenix.sprites_voo_carregados:
                Fenix.sprites_atacar_carregados = [Fenix.sprites_voo_carregados[0]]
        if not Fenix.sons_carregados:
            # Carregar sons aqui
            Fenix.sons_carregados = True

    def __init__(self, x, y, velocidade=1.8):
        Fenix.carregar_recursos_fenix()

        vida_fenix = 350
        dano_contato_fenix = 6
        xp_fenix = 70
        self.moedas_drop = 20
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Fenix/Fenix 1.png"

        super().__init__(
            x, y,
            Fenix.tamanho_sprite_definido[0], Fenix.tamanho_sprite_definido[1],
            vida_fenix, velocidade, dano_contato_fenix,
            xp_fenix, sprite_path_principal_relativo_jogo
        )

        # Removido: Flag self.recursos_concedidos, pois a lógica de recompensa é externa

        self.sprites_voo = Fenix.sprites_voo_carregados
        self.sprites_atacar = Fenix.sprites_atacar_carregados if Fenix.sprites_atacar_carregados else self.sprites_voo
        self.sprites = self.sprites_voo

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            if self.sprites: self.image = self.sprites[0]
            else:
                self.image = pygame.Surface(Fenix.tamanho_sprite_definido, pygame.SRCALPHA); self.image.fill((200, 100, 0, 150))
                if not self.sprites: self.sprites = [self.image]
        self.rect = self.image.get_rect(topleft=(x,y))

        self.sprite_index = 0
        self.intervalo_animacao_voo = 100
        self.intervalo_animacao_atacar = 80
        self.intervalo_animacao = self.intervalo_animacao_voo

        self.is_attacking = False
        self.attack_duration = 0.7
        self.attack_timer = 0.0
        self.attack_damage_especifico = 18
        self.attack_hitbox_size = (self.rect.width * 1.5, self.rect.height * 0.5)
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.attack_range = 100
        self.attack_cooldown = 3.5
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)
        self.hit_player_this_attack_burst = False
        self.canal_voo = None

    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0); return
        atk_w, atk_h = self.attack_hitbox_size
        self.attack_hitbox.height = atk_h
        if self.facing_right:
            self.attack_hitbox.width = atk_w; self.attack_hitbox.midleft = self.rect.midright
        else:
            self.attack_hitbox.width = atk_w; self.attack_hitbox.midright = self.rect.midleft

    def atacar(self, player):
        if not (hasattr(player, 'rect') and self.esta_vivo()): return
        agora = pygame.time.get_ticks()
        distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
        if not self.is_attacking and distancia_ao_jogador <= self.attack_range and (agora - self.last_attack_time >= self.attack_cooldown * 1000):
            self.is_attacking = True
            self.attack_timer = agora
            self.last_attack_time = agora
            self.hit_player_this_attack_burst = False
            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        # Lógica de recompensa ao morrer foi movida para GerenciadorDeInimigos.py
        if not self.esta_vivo():
            self.kill() # O GerenciadorDeInimigos.py cuidará das recompensas e remoção
            return

        agora = pygame.time.get_ticks()
        jogador_valido = (player and hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo'))

        # Chama o update da classe base para movimento e animação
        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)

        if self.is_attacking:
            if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()
            self._atualizar_hitbox_ataque()
            if jogador_valido and not self.hit_player_this_attack_burst and self.attack_hitbox.colliderect(player.rect):
                if hasattr(player, 'receber_dano'): player.receber_dano(self.attack_damage_especifico)
                self.hit_player_this_attack_burst = True
            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_voo
                self.intervalo_animacao = self.intervalo_animacao_voo
                self.sprite_index = 0
                self.attack_hitbox.size = (0,0)
        else:
            if jogador_valido: self.atacar(player)
            # A chamada super().update já cuida do mover_em_direcao e atualizar_animacao para o estado normal.
            # Essas linhas foram comentadas porque a chamada super().update já as executa.
            # if not self.is_attacking and jogador_valido and hasattr(self, 'mover_em_direcao'):
            #     self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
            # if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()

        if jogador_valido and self.rect.colliderect(player.rect) and (agora - self.last_contact_time >= self.contact_cooldown):
            if hasattr(player, 'receber_dano'): player.receber_dano(self.contact_damage)
            self.last_contact_time = agora

    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if not self.esta_vivo() and vida_antes > 0:
            if self.canal_voo: self.canal_voo.stop(); self.canal_voo = None
            if Fenix.som_morte_fenix: Fenix.som_morte_fenix.play()
        elif self.esta_vivo() and vida_antes > self.hp and Fenix.som_dano_fenix:
            Fenix.som_dano_fenix.play()

    def kill(self):
        if self.canal_voo:
            self.canal_voo.stop() # Corrigido typo de 'canal_voe' para 'canal_voo'
            self.canal_voo = None
        super().kill()
