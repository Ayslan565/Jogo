# Espirito_Das_Flores.py
import pygame
import os
import math
import time
import random

# --- Importação da Classe Base Inimigo ---
# Assume que existe um arquivo 'Inimigos.py' na MESMA PASTA que este
# (Jogo/Arquivos/Inimigos/Inimigos.py) e que ele define a classe 'Inimigo' base.
# Essa classe base é referenciada como 'InimigoBase' aqui.
try:
    from .Inimigos import Inimigo as InimigoBase
    # print(f"DEBUG(Espirito_Das_Flores): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Espirito_Das_Flores): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    # Este é um placeholder MUITO SIMPLES. A classe base real deve ser mais completa
    # e ter o método _carregar_sprite principal (que também precisa encontrar a raiz do jogo).
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((120, 120, 120, 100)) # Placeholder cinza médio
            pygame.draw.rect(self.image, (255,20,147), self.image.get_rect(), 1) # Borda rosa choque
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            self.x = float(x)
            self.y = float(y)
            # print(f"DEBUG(InimigoBase Placeholder para Espirito_Das_Flores): Instanciado. Sprite path (não usado): {sprite_path}")

        def _carregar_sprite(self, path, tamanho): # Placeholder _carregar_sprite
            # print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{path}' (não implementado neste placeholder). Retornando placeholder visual.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((255,105,180, 128)) # Cor rosa para placeholder do _carregar_sprite
            return img

        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt=None): pass
        def atualizar_animacao(self):
            if self.sprites and len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
        def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))


class Espirito_Das_Flores(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (80, 80) # Ajuste conforme necessário

    som_ataque_espirito = None
    som_dano_espirito = None
    som_morte_espirito = None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_espirito(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Espirito_Das_Flores._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))

        if not os.path.exists(caminho_completo):
            # print(f"DEBUG(Espirito_Das_Flores._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            # print(f"DEBUG(Espirito_Das_Flores._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            # print(f"DEBUG(Espirito_Das_Flores._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Espirito_Das_Flores._obter_pasta_raiz_jogo()
        # print(f"DEBUG(Espirito_Das_Flores._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {pasta_raiz_jogo}")

        if lista_destino_existente is None: lista_destino_existente = []

        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            # print(f"DEBUG(Espirito_Das_Flores._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                    # print(f"DEBUG(Espirito_Das_Flores._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    # print(f"DEBUG(Espirito_Das_Flores._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder (rosa).")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((255, 105, 180, 180)) # Cor rosa para placeholder
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                # print(f"DEBUG(Espirito_Das_Flores._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder (rosa).")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((255, 105, 180, 180))
                lista_destino_existente.append(placeholder)

        if not lista_destino_existente:
            # print(f"DEBUG(Espirito_Das_Flores._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final (rosa escuro).")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((200, 80, 150, 200))
            lista_destino_existente.append(placeholder)


    @staticmethod
    def carregar_recursos_espirito():
        if Espirito_Das_Flores.sprites_andar_carregados is None:
            Espirito_Das_Flores.sprites_andar_carregados = []
            caminhos_andar = [
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores1.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores2.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores3.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores4.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores5.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores6.png",
                "Sprites/Inimigos/Espirito_Flores/Espirito_Flores7.png",
            ]
            Espirito_Das_Flores._carregar_lista_sprites_estatico(
                caminhos_andar,
                Espirito_Das_Flores.sprites_andar_carregados,
                Espirito_Das_Flores.tamanho_sprite_definido,
                "Andar/Idle"
            )

            if not Espirito_Das_Flores.sprites_atacar_carregados and Espirito_Das_Flores.sprites_andar_carregados:
                 Espirito_Das_Flores.sprites_atacar_carregados = [Espirito_Das_Flores.sprites_andar_carregados[0]]

        if not Espirito_Das_Flores.sons_carregados:
            # Espirito_Das_Flores.som_ataque_espirito = Espirito_Das_Flores._carregar_som_espirito("Sons/Espirito_Flores/ataque_magico.wav")
            # Espirito_Das_Flores.som_dano_espirito = Espirito_Das_Flores._carregar_som_espirito("Sons/Espirito_Flores/dano_brilho.wav")
            # Espirito_Das_Flores.som_morte_espirito = Espirito_Das_Flores._carregar_som_espirito("Sons/Espirito_Flores/morte_dissipar.wav")
            Espirito_Das_Flores.sons_carregados = True


    def __init__(self, x, y, velocidade=1.6):
        Espirito_Das_Flores.carregar_recursos_espirito()

        vida_espirito = 75
        dano_contato_espirito = 6
        xp_espirito = 35
        self.moedas_drop = 10 # Quantidade de moedas que o Espírito das Flores dropa

        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Espirito_Flores/Espirito_Flores1.png"

        super().__init__(
            x, y,
            Espirito_Das_Flores.tamanho_sprite_definido[0], Espirito_Das_Flores.tamanho_sprite_definido[1],
            vida_espirito, velocidade, dano_contato_espirito,
            xp_espirito, sprite_path_principal_relativo_jogo
        )
        self.x = float(x)
        self.y = float(y)

        self.sprites_andar = Espirito_Das_Flores.sprites_andar_carregados
        self.sprites_atacar = Espirito_Das_Flores.sprites_atacar_carregados if Espirito_Das_Flores.sprites_atacar_carregados else self.sprites_andar
        self.sprites = self.sprites_andar

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)) or \
           (self.sprites and len(self.sprites) > 0 and self.image is self.sprites[0] and self.sprites[0].get_size() != Espirito_Das_Flores.tamanho_sprite_definido):
            # print("DEBUG(Espirito_Das_Flores __init__): self.image do super() não é adequado ou não definido. Usando primeiro sprite de andar.")
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
            else:
                placeholder_img = pygame.Surface(Espirito_Das_Flores.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((200, 80, 150, 150))
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))


        self.sprite_index = 0
        self.intervalo_animacao_andar = 160
        self.intervalo_animacao_atacar = 130
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()

        self.is_attacking = False
        self.attack_duration = 0.7
        self.attack_timer = 0.0
        self.attack_damage_especifico = 15
        self.attack_hitbox_size = (Espirito_Das_Flores.tamanho_sprite_definido[0] * 1.2, Espirito_Das_Flores.tamanho_sprite_definido[1] * 1.2)
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.attack_range = 100
        self.attack_cooldown = 3.0
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)
        self.hit_player_this_pulse = False

    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0)
            return

        w, h = self.attack_hitbox_size
        self.attack_hitbox.size = (w,h)
        self.attack_hitbox.center = self.rect.center


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
            self.hit_player_this_pulse = False

            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = agora
            # if Espirito_Das_Flores.som_ataque_espirito: Espirito_Das_Flores.som_ataque_espirito.play()

    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            return

        agora = pygame.time.get_ticks()
        if dt_ms is None:
            dt_ms = agora - getattr(self, '_last_update_time', agora)
            self._last_update_time = agora
            if dt_ms <= 0 : dt_ms = 16

        jogador_valido = (player is not None and hasattr(player, 'rect') and player.rect is not None and
                          hasattr(player, 'receber_dano'))

        if jogador_valido:
            if player.rect.centerx < self.rect.centerx: self.facing_right = False
            else: self.facing_right = True

        if self.is_attacking:
            self.atualizar_animacao()
            self._atualizar_hitbox_ataque()

            if jogador_valido and not self.hit_player_this_pulse and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico, self.rect)
                self.hit_player_this_pulse = True

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

        if hasattr(self, 'last_hit_time') and (agora - self.last_hit_time < self.hit_flash_duration):
            pass
        else:
            if self.sprites and len(self.sprites) > self.sprite_index:
                 current_sprite_image = self.sprites[self.sprite_index]
                 if not self.facing_right:
                     current_sprite_image = pygame.transform.flip(current_sprite_image, True, False)
                 self.image = current_sprite_image


    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if self.esta_vivo():
            if vida_antes > self.hp and Espirito_Das_Flores.som_dano_espirito:
                Espirito_Das_Flores.som_dano_espirito.play()
        elif vida_antes > 0 and Espirito_Das_Flores.som_morte_espirito:
            Espirito_Das_Flores.som_morte_espirito.play()

    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y)
