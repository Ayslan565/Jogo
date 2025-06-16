# Fenix.py
import pygame
import os
import math
import time

from Arquivos.Inimigos.score import score_manager  # <-- INTEGRAÇÃO DO SCORE

# --- Importação da Classe Base Inimigo ---
# Assume que existe um arquivo 'Inimigos.py' na MESMA PASTA que este
# (Jogo/Arquivos/Inimigos/Inimigos.py) e que ele define a classe 'Inimigo' base.
# Essa classe base é referenciada como 'InimigoBase' aqui.
try:
    from .Inimigos import Inimigo as InimigoBase
    # print(f"DEBUG(Fenix): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Fenix): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    # Este é um placeholder MUITO SIMPLES. A classe base real deve ser mais completa.
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((180, 100, 50, 100)) # Placeholder laranja escuro
            pygame.draw.rect(self.image, (255,140,0), self.image.get_rect(), 1) # Borda laranja escura
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            # print(f"DEBUG(InimigoBase Placeholder para Fenix): Instanciado. Sprite path (não usado): {sprite_path}")

        def _carregar_sprite(self, path, tamanho): # Placeholder _carregar_sprite
            # print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{path}' (não implementado). Retornando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((255,165,0, 128)) # Cor laranja para placeholder do _carregar_sprite
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
        def kill(self): # Placeholder kill
            super().kill()


class Fenix(InimigoBase):
    sprites_voo_carregados = None # Renomeado de sprites_andar_carregados
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (100, 100) # Ajuste conforme necessário

    som_ataque_fenix = None
    som_dano_fenix = None
    som_morte_fenix = None
    som_voo_fenix = None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_fenix(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Fenix._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))

        if not os.path.exists(caminho_completo):
            # print(f"DEBUG(Fenix._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            # print(f"DEBUG(Fenix._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            # print(f"DEBUG(Fenix._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Fenix._obter_pasta_raiz_jogo()
        # print(f"DEBUG(Fenix._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {pasta_raiz_jogo}")

        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            # print(f"DEBUG(Fenix._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                    # print(f"DEBUG(Fenix._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    # print(f"DEBUG(Fenix._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder (laranja).")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((255, 165, 0, 180)) # Cor laranja para placeholder
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                # print(f"DEBUG(Fenix._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder (laranja).")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((255, 165, 0, 180))
                lista_destino_existente.append(placeholder)

        if not lista_destino_existente:
            # print(f"DEBUG(Fenix._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final (laranja escuro).")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((200, 100, 0, 200))
            lista_destino_existente.append(placeholder)

    @staticmethod
    def carregar_recursos_fenix():
        if Fenix.sprites_voo_carregados is None:
            Fenix.sprites_voo_carregados = []
            caminhos_voo = [
                "Sprites/Inimigos/Fenix/Fenix 1.png",
                "Sprites/Inimigos/Fenix/Fenix 2.png",
                "Sprites/Inimigos/Fenix/Fenix 3.png",
                "Sprites/Inimigos/Fenix/Fenix 4.png",
            ]
            Fenix._carregar_lista_sprites_estatico(
                caminhos_voo,
                Fenix.sprites_voo_carregados,
                Fenix.tamanho_sprite_definido,
                "Voo/Idle"
            )

            # Fenix.sprites_atacar_carregados = []
            # caminhos_atacar = ["Sprites/Inimigos/Fenix/Fenix_Atk1.png", ...]
            # Fenix._carregar_lista_sprites_estatico(
            #     caminhos_atacar,
            #     Fenix.sprites_atacar_carregados,
            #     Fenix.tamanho_sprite_definido,
            #     "Atacar"
            # )
            if not Fenix.sprites_atacar_carregados and Fenix.sprites_voo_carregados:
                 Fenix.sprites_atacar_carregados = [Fenix.sprites_voo_carregados[0]] # Fallback

        if not Fenix.sons_carregados:
            # Fenix.som_ataque_fenix = Fenix._carregar_som_fenix("Sons/Fenix/ataque_fogo.wav")
            # Fenix.som_dano_fenix = Fenix._carregar_som_fenix("Sons/Fenix/dano_grito.wav")
            # Fenix.som_morte_fenix = Fenix._carregar_som_fenix("Sons/Fenix/morte_cinzas.wav")
            # Fenix.som_voo_fenix = Fenix._carregar_som_fenix("Sons/Fenix/voo_loop.wav")
            Fenix.sons_carregados = True


    def __init__(self, x, y, velocidade=2.8): 
        Fenix.carregar_recursos_fenix()

        vida_fenix = 110 
        dano_contato_fenix = 6 
        xp_fenix = 70
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Fenix/Fenix 1.png" 
        # moedas_dropadas = 20

        super().__init__(
            x, y, 
            Fenix.tamanho_sprite_definido[0], Fenix.tamanho_sprite_definido[1], 
            vida_fenix, velocidade, dano_contato_fenix, 
            xp_fenix, sprite_path_principal_relativo_jogo
        )

        self.sprites_voo = Fenix.sprites_voo_carregados
        self.sprites_atacar = Fenix.sprites_atacar_carregados if Fenix.sprites_atacar_carregados else self.sprites_voo
        self.sprites = self.sprites_voo

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            # print("DEBUG(Fenix __init__): self.image não foi definido pelo super(). Usando primeiro sprite de animação.")
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
            else:
                placeholder_img = pygame.Surface(Fenix.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((200, 100, 0, 150))
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.sprite_index = 0
        self.intervalo_animacao_voo = 100
        self.intervalo_animacao_atacar = 80
        self.intervalo_animacao = self.intervalo_animacao_voo

        self.is_attacking = False
        self.attack_duration = 0.7 # Duração da baforada de fogo ou animação de ataque
        self.attack_timer = 0.0
        self.attack_damage_especifico = 18
        self.attack_hitbox_size = (self.rect.width * 1.5, self.rect.height * 0.5) # Ex: baforada à frente
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.attack_range = 150
        self.attack_cooldown = 2.5
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)
        self.hit_player_this_attack_burst = False # Para dano de baforada

        self.canal_voo = None
        # if Fenix.som_voo_fenix:
        #     try:
        #         self.canal_voo = pygame.mixer.find_channel(True)
        #         if self.canal_voo:
        #             self.canal_voo.play(Fenix.som_voo_fenix, loops=-1)
        #     except pygame.error as e:
        #         print(f"DEBUG(Fenix): Não foi possível tocar som de voo: {e}")
        #         self.canal_voo = None

    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0)
            return

        atk_w, atk_h = self.attack_hitbox_size
        self.attack_hitbox.height = atk_h # Largura pode variar com a direção
        
        if self.facing_right:
            self.attack_hitbox.width = atk_w
            self.attack_hitbox.midleft = self.rect.midright
        else:
            self.attack_hitbox.width = atk_w
            self.attack_hitbox.midright = self.rect.midleft

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
            self.hit_player_this_attack_burst = False

            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0
            # if Fenix.som_ataque_fenix: Fenix.som_ataque_fenix.play()

    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        # --- INTEGRAÇÃO DO SCORE ---
        if not self.esta_vivo():
            if not hasattr(self, "ouro_concedido") or not self.ouro_concedido:
                if hasattr(player, "dinheiro") and hasattr(self, "money_value"):
                    player.dinheiro += self.money_value
                if hasattr(self, "xp_value"):
                    score_manager.adicionar_xp(self.xp_value)
                self.ouro_concedido = True
            if self.canal_voo:
                self.canal_voo.stop()
                self.canal_voo = None
            return

        agora = pygame.time.get_ticks()
        jogador_valido = (hasattr(player, 'rect') and
                          hasattr(player, 'vida') and
                          hasattr(player.vida, 'esta_vivo') and
                          hasattr(player, 'receber_dano'))

        if self.is_attacking:
            self.atualizar_animacao()
            self._atualizar_hitbox_ataque()

            if jogador_valido and not self.hit_player_this_attack_burst and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico)
                self.hit_player_this_attack_burst = True

            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_voo
                self.intervalo_animacao = self.intervalo_animacao_voo
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
            if vida_antes > self.hp and Fenix.som_dano_fenix:
                Fenix.som_dano_fenix.play()
        elif vida_antes > 0:
            if Fenix.som_morte_fenix:
                Fenix.som_morte_fenix.play()
            if self.canal_voo:
                self.canal_voo.stop()
                self.canal_voo = None

    def kill(self): # Sobrescreve kill para parar o som de voo
        if self.canal_voo:
            self.canal_voo.stop()
            self.canal_voo = None
        super().kill()

    # O método desenhar é herdado da InimigoBase.
    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y)
    #     if self.is_attacking and self.attack_hitbox.width > 0: # Debug hitbox
    #         debug_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
    #         pygame.draw.rect(surface, (255, 100, 0, 100), debug_rect_onscreen, 1)

