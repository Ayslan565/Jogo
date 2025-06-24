# Arvore_Maldita.py
import pygame
import os
import math
import random

# A importação do score_manager foi removida daqui, pois a lógica de recompensa agora é centralizada.

# --- Importação da Classe Base Inimigo ---
try:
    # CORREÇÃO: Importação absoluta e qualificada para a classe base.
    from Inimigos.Inimigos import Inimigo as InimigoBase
except ImportError as e:
    # O placeholder é mantido para segurança, caso a importação principal falhe.
    class InimigoBase(pygame.sprite.Sprite): # Placeholder
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((80, 40, 20, 150))
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128); self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.x = float(x); self.y = float(y)
        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano); self.last_hit_time = pygame.time.get_ticks()
        def esta_vivo(self): return self.hp > 0
        def update(self, player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms): pass
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect: janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self): super().kill()


class Arvore_Maldita(InimigoBase):
    sprites_idle_arvore_carregados = None
    sprites_ataque_principal_arvore_carregados = None
    tamanho_sprite_definido = (250, 300)

    som_ataque_arvore, som_dano_arvore, som_morte_arvore = None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))

    # ... (métodos estáticos de carregamento permanecem os mesmos) ...
    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos, lista_destino, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Arvore_Maldita._obter_pasta_raiz_jogo()
        if lista_destino is None: lista_destino = []
        for path_relativo in caminhos_relativos:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", os.sep))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino.append(sprite)
                else:
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA); placeholder.fill((60, 30, 10, 180)); lista_destino.append(placeholder)
            except pygame.error:
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA); placeholder.fill((60, 30, 10, 180)); lista_destino.append(placeholder)
        if not lista_destino:
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA); placeholder.fill((40, 20, 5, 200)); lista_destino.append(placeholder)

    @staticmethod
    def carregar_recursos_arvore_maldita():
        if Arvore_Maldita.sprites_idle_arvore_carregados is None:
            Arvore_Maldita.sprites_idle_arvore_carregados = []
            caminhos_idle = [f"Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita{i}.png" for i in range(1, 4)]
            Arvore_Maldita._carregar_lista_sprites_estatico(caminhos_idle, Arvore_Maldita.sprites_idle_arvore_carregados, Arvore_Maldita.tamanho_sprite_definido, "ArvoreMaldita_Idle")
        if Arvore_Maldita.sprites_ataque_principal_arvore_carregados is None:
            Arvore_Maldita.sprites_ataque_principal_arvore_carregados = []
            caminhos_ataque_principal = [f"Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita{i}.png" for i in range(1, 4)]
            Arvore_Maldita._carregar_lista_sprites_estatico(caminhos_ataque_principal, Arvore_Maldita.sprites_ataque_principal_arvore_carregados, Arvore_Maldita.tamanho_sprite_definido, "ArvoreMaldita_AtaquePrincipal")
        if not Arvore_Maldita.sons_carregados:
            Arvore_Maldita.sons_carregados = True

    def __init__(self, x, y, velocidade=1.0):
        Arvore_Maldita.carregar_recursos_arvore_maldita()

        vida_arvore = 250
        dano_contato_arvore = 25
        xp_arvore = 1000
        self.moedas_drop = 1500
        self.xp_value_boss = xp_arvore # Usado pela lógica de chefe em luta_boss.py
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Arvore Maldita/Arvore Maldita1.png"

        super().__init__(
            x, y,
            Arvore_Maldita.tamanho_sprite_definido[0], Arvore_Maldita.tamanho_sprite_definido[1],
            vida_arvore, velocidade, dano_contato_arvore,
            xp_arvore, sprite_path_principal_relativo_jogo
        )
        
        # O atributo 'recursos_concedidos' foi removido.
        self.x = float(x)
        self.y = float(y)
        self.sprites_idle = Arvore_Maldita.sprites_idle_arvore_carregados
        self.sprites_ataque_principal = Arvore_Maldita.sprites_ataque_principal_arvore_carregados
        self.sprites = self.sprites_idle

        if self.sprites_idle:
            self.image = self.sprites_idle[0].copy()
        else:
            self.image = pygame.Surface(Arvore_Maldita.tamanho_sprite_definido, pygame.SRCALPHA); self.image.fill((40, 20, 5, 150))
            if not self.sprites: self.sprites = [self.image]
        
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.sprite_index = 0
        self.intervalo_animacao_idle = 450
        self.intervalo_animacao_ataque_principal = 150
        self.intervalo_animacao = self.intervalo_animacao_idle
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
        self.is_attacking_principal = False
        self.attack_principal_duration = 1.8
        self.attack_principal_timer = 0.0
        self.attack_principal_damage = 50
        self.attack_principal_range = Arvore_Maldita.tamanho_sprite_definido[0] * 0.8
        self.attack_principal_cooldown = 4.0
        self.last_attack_principal_time = pygame.time.get_ticks() - int(self.attack_principal_cooldown * 1000 * 0.75)
        self.attack_principal_hitbox_size = (Arvore_Maldita.tamanho_sprite_definido[0] * 0.7, Arvore_Maldita.tamanho_sprite_definido[1] * 0.6)
        self.attack_principal_hitbox_offset_y = -Arvore_Maldita.tamanho_sprite_definido[1] * 0.1
        self.attack_principal_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_swing = False

    # (Funções de ataque e hitbox permanecem as mesmas)
    def _atualizar_hitbox_ataque_principal(self):
        if not self.is_attacking_principal:
            self.attack_principal_hitbox.size = (0,0); return
        w, h = self.attack_principal_hitbox_size
        self.attack_principal_hitbox.size = (w,h)
        if self.facing_right:
            self.attack_principal_hitbox.left = self.rect.centerx
        else:
            self.attack_principal_hitbox.right = self.rect.centerx
        self.attack_principal_hitbox.centery = self.rect.centery + self.attack_principal_hitbox_offset_y

    def iniciar_ataque_principal(self, player):
        if not (hasattr(player, 'rect') and self.esta_vivo()): return
        agora = pygame.time.get_ticks()
        distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
        if not self.is_attacking_principal and \
           distancia_ao_jogador <= self.attack_principal_range and \
           (agora - self.last_attack_principal_time >= self.attack_principal_cooldown * 1000):
            self.is_attacking_principal = True
            self.attack_principal_timer = agora
            self.last_attack_principal_time = agora
            self.hit_player_this_attack_swing = False
            self.sprites = self.sprites_ataque_principal
            self.intervalo_animacao = self.intervalo_animacao_ataque_principal
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = agora
            if Arvore_Maldita.som_ataque_arvore: Arvore_Maldita.som_ataque_arvore.play()

    # --- MÉTODO UPDATE TOTALMENTE CORRIGIDO ---
    def update(self, player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms):
        # A verificação de 'esta_vivo' e a concessão de recompensas foram removidas.
        # O GerenciadorDeInimigos é agora o único responsável por essa lógica.
        if not self.esta_vivo():
            return # Apenas para de se atualizar, o gerenciador fará o resto.

        agora = pygame.time.get_ticks()
        
        jogador_valido = (player and hasattr(player, 'rect') and hasattr(player, 'receber_dano'))

        if jogador_valido:
            if player.rect.centerx < self.rect.centerx: self.facing_right = False
            else: self.facing_right = True
        
        # --- Lógica de Ataque ---
        if self.is_attacking_principal:
            self._atualizar_hitbox_ataque_principal()
            
            if jogador_valido and not self.hit_player_this_attack_swing and \
               self.attack_principal_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_principal_damage, self.rect)
                self.hit_player_this_attack_swing = True
            
            if agora - self.attack_principal_timer >= self.attack_principal_duration * 1000:
                self.is_attacking_principal = False
                self.sprites = self.sprites_idle
                self.intervalo_animacao = self.intervalo_animacao_idle
                self.sprite_index = 0
                self.tempo_ultimo_update_animacao = agora
                self.attack_principal_hitbox.size = (0,0)
        else:
            if jogador_valido: self.iniciar_ataque_principal(player)
            
            # Movimento só ocorre se não estiver atacando
            if not self.is_attacking_principal and self.velocidade > 0:
                if jogador_valido and hasattr(self, 'mover_em_direcao'):
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
        
        # A atualização de animação é chamada pela classe base Inimigo
        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)
    
    # (O resto dos métodos como receber_dano e desenhar permanecem)
    def receber_dano(self, dano, fonte_dano_rect=None):
        if not self.esta_vivo(): return
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if self.esta_vivo():
            if vida_antes > self.hp:
                if Arvore_Maldita.som_dano_arvore: Arvore_Maldita.som_dano_arvore.play()
                self.last_hit_time = pygame.time.get_ticks()
        elif vida_antes > 0:
            if Arvore_Maldita.som_morte_arvore: Arvore_Maldita.som_morte_arvore.play()

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y)