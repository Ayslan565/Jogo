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
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((150, 0, 150, 100))
            pygame.draw.rect(self.image, (200, 0, 200), self.image.get_rect(), 1)
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
            self.last_contact_time = pygame.time.get_ticks() - 1000
            self.sprites = [self.image.copy()]
            self.sprite_index = 0
            self.intervalo_animacao = 200
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.moedas_drop = 0
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
                dx_norm, dy_norm = dx / dist, dy / dist
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
                if len(self.sprites) > 0: self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
                self.tempo_ultimo_update_animacao = tempo_atual
            if len(self.sprites) > 0:
                current_sprite = self.sprites[self.sprite_index]
                if not self.facing_right: self.image = pygame.transform.flip(current_sprite, True, False)
                else: self.image = current_sprite
            else:
                self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA); self.image.fill((150, 0, 150, 100))
            if tempo_atual - self.last_hit_time < self.hit_flash_duration:
                flash_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA); flash_surface.fill(self.hit_flash_color); self.image.blit(flash_surface, (0, 0))
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            self.atualizar_animacao()
            if player and hasattr(player, 'rect') and player.esta_vivo(): self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect: janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self): super().kill()


class Morte(InimigoBase):
    """
    Representa a Morte, um inimigo com habilidades específicas de ataque.
    Possui animações de andar e atacar.
    """
    sprites_andar, sprites_atacar = None, None
    # --- ALTERAÇÃO APLICADA AQUI: Aumentei o tamanho da Morte ---
    tamanho_sprite_definido = (144, 144) # Original: (96, 96)
    som_ataque_Morte, som_dano_Morte, som_morte_Morte, som_spawn_Morte = None, None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_Morte(caminho_relativo_a_raiz_jogo):
        """
        Carrega um arquivo de som para a Morte, verificando se existe e tratando erros.
        """
        pasta_raiz_jogo = Morte._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("/", os.sep))
        if not os.path.exists(caminho_completo): return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            return som
        except pygame.error as e:
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino, tamanho_sprite, nome_animacao):
        """
        Carrega uma lista de sprites para uma animação específica da Morte.
        """
        pasta_raiz_jogo = Morte._obter_pasta_raiz_jogo()
        if lista_destino is None: lista_destino = []
        else: lista_destino.clear() 
        
        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("/", os.sep))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino.append(sprite)
                else:
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA); placeholder.fill((200, 0, 200, 180)); lista_destino.append(placeholder)
            except pygame.error as e:
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA); placeholder.fill((200, 0, 200, 180)); lista_destino.append(placeholder)

        if not lista_destino:
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA); placeholder.fill((150, 0, 150, 200)); lista_destino.append(placeholder)
        
        return lista_destino

    @staticmethod
    def carregar_recursos_Morte():
        """
        Carrega todos os sprites e sons para a classe Morte.
        """
        if Morte.sprites_andar is None:
            caminhos_andar = [ f"Sprites/Inimigos/Morte/Andar{i}.png" for i in range(1, 4) ] # Exemplo
            Morte.sprites_andar = Morte._carregar_lista_sprites_estatico(caminhos_andar, [], Morte.tamanho_sprite_definido, "Andar")

        if Morte.sprites_atacar is None:
            caminhos_atacar = [ f"Sprites/Inimigos/Morte/Ataque{i}.png" for i in range(1, 4) ]
            Morte.sprites_atacar = Morte._carregar_lista_sprites_estatico(caminhos_atacar, [], Morte.tamanho_sprite_definido, "Atacar")

            if not Morte.sprites_atacar and Morte.sprites_andar:
                Morte.sprites_atacar = [Morte.sprites_andar[0]]
            elif not Morte.sprites_atacar:
                placeholder = pygame.Surface(Morte.tamanho_sprite_definido, pygame.SRCALPHA); placeholder.fill((150, 0, 150, 200)); Morte.sprites_atacar = [placeholder]

        if not Morte.sons_carregados:
            Morte.sons_carregados = True

    def __init__(self, x, y, velocidade=2.5):
        """
        Inicializa uma nova instância da Morte.
        """
        Morte.carregar_recursos_Morte()

        vida_morte, dano_contato_morte, xp_morte, moedas_dropadas = 90, 10, 75, 12
        sprite_path_ref = "Sprites/Inimigos/Morte/Ataque1.png"

        super().__init__(x, y,
                         Morte.tamanho_sprite_definido[0], Morte.tamanho_sprite_definido[1],
                         vida_morte, velocidade, dano_contato_morte,
                         xp_morte, sprite_path_ref)

        self.moedas_drop = moedas_dropadas
        self.sprites_andar_anim = Morte.sprites_andar
        self.sprites_atacar_anim = Morte.sprites_atacar
        self.sprites = self.sprites_andar_anim if self.sprites_andar_anim else [self.image]
        
        self.sprite_index = 0
        self.intervalo_animacao_andar, self.intervalo_animacao_atacar = 120, 100
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()

        self.is_attacking = False
        self.attack_duration, self.attack_timer = 0.6, 0.0
        self.attack_damage = 20
        self.attack_hitbox_size = (int(Morte.tamanho_sprite_definido[0] * 0.8), int(Morte.tamanho_sprite_definido[1] * 0.8)) # Ajusta a hitbox com o novo tamanho
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.attack_range = 140 # Aumenta o alcance do ataque
        self.attack_cooldown = 2.5
        self.last_attack_time = time.time() - self.attack_cooldown
        self.hit_player_this_attack = False

        if self.sprites: self.image = self.sprites[0]
        else:
            self.image = pygame.Surface(Morte.tamanho_sprite_definido, pygame.SRCALPHA); self.image.fill((150, 0, 150, 100))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


    def receber_dano(self, dano, fonte_dano_rect=None):
        """
        Reduz a vida da Morte e lida com a reprodução de sons de dano/morte.
        """
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if not self.esta_vivo() and vida_antes > 0:
            if Morte.som_morte_Morte: Morte.som_morte_Morte.play()
        elif self.esta_vivo() and vida_antes > self.hp:
            if Morte.som_dano_Morte: Morte.som_dano_Morte.play()

    def atacar(self, player):
        """
        Inicia o ataque da Morte se as condições forem atendidas.
        """
        if not (hasattr(player, 'rect') and self.esta_vivo()): return

        current_time = time.time()
        if not self.is_attacking and (current_time - self.last_attack_time >= self.attack_cooldown):
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
            if distancia_ao_jogador <= self.attack_range:
                self.is_attacking = True
                self.attack_timer = current_time
                self.last_attack_time = current_time
                self.hit_player_this_attack = False
                self.sprites = self.sprites_atacar_anim 
                self.intervalo_animacao = self.intervalo_animacao_atacar
                self.sprite_index = 0
                self.attack_hitbox = pygame.Rect(0, 0, *self.attack_hitbox_size) 
                self.attack_hitbox.center = self.rect.center

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        """
        Atualiza o estado da Morte a cada frame.
        """
        if not self.esta_vivo():
            self.kill(); return

        agora_ticks = pygame.time.get_ticks()
        agora_sec = time.time()
        jogador_valido = player and hasattr(player, 'rect') and player.esta_vivo()

        if not jogador_valido:
            self.atualizar_animacao(); return

        if self.is_attacking:
            self.attack_hitbox.center = self.rect.center 
            if not self.hit_player_this_attack and self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage, self.rect)
                self.hit_player_this_attack = True
            
            if agora_sec - self.attack_timer > self.attack_duration:
                self.is_attacking = False
                self.sprites = self.sprites_andar_anim
                self.intervalo_animacao = self.intervalo_animacao_andar
        else:
            self.atacar(player)
            if not self.is_attacking:
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
        
        self.atualizar_animacao()

        if not self.is_attacking and self.rect.colliderect(player.rect) and (agora_ticks - self.last_contact_time >= self.contact_cooldown):
            player.receber_dano(self.contact_damage, self.rect)
            self.last_contact_time = agora_ticks
