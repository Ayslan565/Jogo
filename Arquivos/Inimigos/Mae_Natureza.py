# Mae_Natureza.py
import pygame
import os
import math
import time

# --- Importação da Classe Base Inimigo ---
# Assume que existe um arquivo 'Inimigos.py' na MESMA PASTA que este
# (Jogo/Arquivos/Inimigos/Inimigos.py) e que ele define a classe 'Inimigo' base.
# Essa classe base é referenciada como 'InimigoBase' aqui.
try:
    from .Inimigos import Inimigo as InimigoBase
    # print(f"DEBUG(Mae_Natureza): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Mae_Natureza): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    # Este é um placeholder MUITO SIMPLES. A classe base real deve ser mais completa.
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((20, 100, 20, 100)) # Placeholder verde escuro
            pygame.draw.rect(self.image, (34,139,34), self.image.get_rect(), 1) # Borda verde floresta
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            self.x = float(x) # Adicionado para consistência
            self.y = float(y) # Adicionado para consistência
            # print(f"DEBUG(InimigoBase Placeholder para Mae_Natureza): Instanciado. Sprite path (não usado): {sprite_path}")

        def _carregar_sprite(self, path, tamanho): # Placeholder _carregar_sprite na base
            # print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{path}' (não implementado). Retornando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((34,139,34, 128)) # Cor verde floresta para placeholder do _carregar_sprite
            return img

        def receber_dano(self, dano, fonte_dano_rect=None):
             self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt_ms=None):
            pass
        def atualizar_animacao(self):
            if self.sprites and len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0] # Simplesmente usa o primeiro sprite
                if hasattr(self, 'facing_right') and not self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)
        def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self):
            super().kill()


class Mae_Natureza(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (160, 180) # Ajuste conforme o sprite real

    som_ataque_mae = None
    som_dano_mae = None
    som_morte_mae = None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_mae_natureza(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Mae_Natureza._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))

        if not os.path.exists(caminho_completo):
            # print(f"DEBUG(Mae_Natureza._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            # print(f"DEBUG(Mae_Natureza._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            # print(f"DEBUG(Mae_Natureza._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Mae_Natureza._obter_pasta_raiz_jogo()
        # print(f"DEBUG(Mae_Natureza._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {pasta_raiz_jogo}")

        if lista_destino_existente is None: lista_destino_existente = []

        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            # print(f"DEBUG(Mae_Natureza._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                    # print(f"DEBUG(Mae_Natureza._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    # print(f"DEBUG(Mae_Natureza._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder (verde floresta).")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((34, 139, 34, 180)) # Cor verde floresta para placeholder
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                # print(f"DEBUG(Mae_Natureza._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder (verde floresta).")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((34, 139, 34, 180))
                lista_destino_existente.append(placeholder)

        if not lista_destino_existente:
            # print(f"DEBUG(Mae_Natureza._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final (verde escuro).")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((20, 100, 20, 200))
            lista_destino_existente.append(placeholder)

    @staticmethod
    def carregar_recursos_mae_natureza():
        if Mae_Natureza.sprites_andar_carregados is None:
            Mae_Natureza.sprites_andar_carregados = []
            caminhos_andar = [
                "Sprites/Inimigos/Mae_Natureza/Mae1.png",
                "Sprites/Inimigos/Mae_Natureza/Mae2.png",
                "Sprites/Inimigos/Mae_Natureza/Mae3.png",
            ]
            Mae_Natureza._carregar_lista_sprites_estatico(
                caminhos_andar,
                Mae_Natureza.sprites_andar_carregados,
                Mae_Natureza.tamanho_sprite_definido,
                "Andar/Idle"
            )

        if Mae_Natureza.sprites_atacar_carregados is None:
            Mae_Natureza.sprites_atacar_carregados = []
            caminhos_atacar = [
                "Sprites/Inimigos/Mae_Natureza/Mae_Atacar1.png", # Exemplo
                "Sprites/Inimigos/Mae_Natureza/Mae_Atacar2.png", # Exemplo
            ]
            pasta_raiz_temp = Mae_Natureza._obter_pasta_raiz_jogo()
            primeiro_sprite_ataque_existe = False
            if caminhos_atacar:
                caminho_primeiro_ataque = os.path.join(pasta_raiz_temp, caminhos_atacar[0].replace("\\", "/"))
                if os.path.exists(caminho_primeiro_ataque):
                    primeiro_sprite_ataque_existe = True

            if primeiro_sprite_ataque_existe:
                Mae_Natureza._carregar_lista_sprites_estatico(
                    caminhos_atacar,
                    Mae_Natureza.sprites_atacar_carregados,
                    Mae_Natureza.tamanho_sprite_definido,
                    "Atacar"
                )

            if not Mae_Natureza.sprites_atacar_carregados:
                if Mae_Natureza.sprites_andar_carregados and len(Mae_Natureza.sprites_andar_carregados) > 0 :
                    Mae_Natureza.sprites_atacar_carregados = [Mae_Natureza.sprites_andar_carregados[0]]
                    # print("DEBUG(Mae_Natureza.carregar_recursos): Usando primeiro sprite de andar como fallback para ataque.")
                else:
                    placeholder_ataque = pygame.Surface(Mae_Natureza.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder_ataque.fill((20,100,20, 180)) # Verde escuro
                    Mae_Natureza.sprites_atacar_carregados = [placeholder_ataque]
                    # print("DEBUG(Mae_Natureza.carregar_recursos): Usando placeholder de cor para ataque.")

        if not Mae_Natureza.sons_carregados:
            # Mae_Natureza.som_ataque_mae = Mae_Natureza._carregar_som_mae_natureza("Sons/Mae_Natureza/ataque_raizes.wav")
            # Mae_Natureza.som_dano_mae = Mae_Natureza._carregar_som_mae_natureza("Sons/Mae_Natureza/dano_folhas.wav")
            # Mae_Natureza.som_morte_mae = Mae_Natureza._carregar_som_mae_natureza("Sons/Mae_Natureza/morte_terra.wav")
            Mae_Natureza.sons_carregados = True


    def __init__(self, x, y, velocidade=0.7):
        Mae_Natureza.carregar_recursos_mae_natureza()

        vida_mae_natureza = 120
        dano_contato_mae_natureza = 12
        xp_mae_natureza = 120
        self.moedas_drop = 17 # Quantidade de moedas que a Mãe Natureza dropa

        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Mae_Natureza/Mae1.png"

        super().__init__(
            x, y,
            Mae_Natureza.tamanho_sprite_definido[0], Mae_Natureza.tamanho_sprite_definido[1],
            vida_mae_natureza, velocidade, dano_contato_mae_natureza,
            xp_mae_natureza, sprite_path_principal_relativo_jogo
        )
        self.x = float(x) # Garante que x e y são floats
        self.y = float(y)

        self.sprites_andar = Mae_Natureza.sprites_andar_carregados
        self.sprites_atacar = Mae_Natureza.sprites_atacar_carregados
        self.sprites = self.sprites_andar # Começa com animação de andar/idle

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)) or \
           (self.sprites and len(self.sprites) > 0 and self.image is self.sprites[0] and self.sprites[0].get_size() != Mae_Natureza.tamanho_sprite_definido):
            # print("DEBUG(Mae_Natureza __init__): self.image do super() não é adequado. Usando primeiro sprite de andar.")
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0].copy()
            else: # Fallback crítico se nem os sprites de andar carregaram
                placeholder_img = pygame.Surface(Mae_Natureza.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((20, 100, 20, 150)) # Verde escuro para erro
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.sprite_index = 0
        self.intervalo_animacao_andar = 300
        self.intervalo_animacao_atacar = 220
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()

        self.is_attacking = False
        self.attack_duration = 1.2 # Duração do ataque de área
        self.attack_timer = 0.0
        self.attack_damage_especifico = 30
        self.attack_range = 180  # Alcance para iniciar o ataque de área
        self.attack_cooldown = 4.5
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)

        self.attack_hitbox_size = (Mae_Natureza.tamanho_sprite_definido[0] * 1.5, Mae_Natureza.tamanho_sprite_definido[1] * 1.5)
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_pulse = False


    def _atualizar_hitbox_ataque(self):
        """Atualiza a hitbox de ataque para ser centrada na Mãe Natureza."""
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0)
            return

        w, h = self.attack_hitbox_size
        self.attack_hitbox.size = (w,h)
        self.attack_hitbox.center = self.rect.center


    def atacar(self, player):
        """Inicia a sequência de ataque da Mãe Natureza."""
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
            self.hit_player_this_attack_pulse = False

            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = agora

            # if Mae_Natureza.som_ataque_mae:
            #     Mae_Natureza.som_ataque_mae.play()


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            return

        agora = pygame.time.get_ticks()
        if dt_ms is None:
            dt_ms = agora - getattr(self, '_last_update_time', agora)
            self._last_update_time = agora
            if dt_ms <= 0 : dt_ms = 16

        jogador_valido = (player is not None and hasattr(player, 'rect') and player.rect is not None and
                          hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and
                          hasattr(player, 'receber_dano'))

        if jogador_valido:
            if player.rect.centerx < self.rect.centerx: self.facing_right = False
            else: self.facing_right = True

        if self.is_attacking:
            self.atualizar_animacao()
            self._atualizar_hitbox_ataque()

            if jogador_valido and not self.hit_player_this_attack_pulse and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico, self.rect)
                self.hit_player_this_attack_pulse = True
                # print(f"DEBUG(Mae_Natureza): Ataque de área acertou jogador! Dano: {self.attack_damage_especifico}")

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
        
        # Assegura que a imagem correta (com flip) é usada para desenhar
        if self.sprites and len(self.sprites) > 0:
            idx = int(self.sprite_index % len(self.sprites))
            current_sprite_image = self.sprites[idx]
            if not self.facing_right:
                self.image = pygame.transform.flip(current_sprite_image, True, False)
            else:
                self.image = current_sprite_image


    def receber_dano(self, dano, fonte_dano_rect=None): # Adicionado fonte_dano_rect
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if self.esta_vivo():
            if vida_antes > self.hp and Mae_Natureza.som_dano_mae:
                Mae_Natureza.som_dano_mae.play()
        elif vida_antes > 0 and Mae_Natureza.som_morte_mae: # Morreu e estava viva antes
            Mae_Natureza.som_morte_mae.play()

    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y)
