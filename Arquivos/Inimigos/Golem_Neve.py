# Golem_Neve.py
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
    from Inimigos import Inimigo as InimigoBase
    # print(f"DEBUG(Golem_Neve): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Golem_Neve): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    # Este é um placeholder MUITO SIMPLES. A classe base real deve ser mais completa.
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((180, 200, 230, 100)) # Placeholder azul-acinzentado claro
            pygame.draw.rect(self.image, (200,220,255), self.image.get_rect(), 1) # Borda azul muito clara
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            # print(f"DEBUG(InimigoBase Placeholder para Golem_Neve): Instanciado. Sprite path (não usado): {sprite_path}")

        def _carregar_sprite(self, path, tamanho): # Placeholder _carregar_sprite na base
            # print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{path}' (não implementado). Retornando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((200,220,255, 128)) # Cor azul claro para placeholder do _carregar_sprite
            return img

        def receber_dano(self, dano, fonte_dano_rect=None): # Adicionado fonte_dano_rect para consistência
             self.hp = max(0, self.hp - dano)
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


class Golem_Neve(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (170, 160)

    som_ataque_golem = None
    som_dano_golem = None
    som_morte_golem = None
    som_spawn_golem = None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_golem_neve(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Golem_Neve._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))

        if not os.path.exists(caminho_completo):
            # print(f"DEBUG(Golem_Neve._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            # print(f"DEBUG(Golem_Neve._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            # print(f"DEBUG(Golem_Neve._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Golem_Neve._obter_pasta_raiz_jogo()
        # print(f"DEBUG(Golem_Neve._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {pasta_raiz_jogo}")

        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            # print(f"DEBUG(Golem_Neve._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                    # print(f"DEBUG(Golem_Neve._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    # print(f"DEBUG(Golem_Neve._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder (azul claro).")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((200, 220, 255, 180)) # Cor azul claro para placeholder
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                # print(f"DEBUG(Golem_Neve._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder (azul claro).")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((200, 220, 255, 180))
                lista_destino_existente.append(placeholder)

        if not lista_destino_existente:
            # print(f"DEBUG(Golem_Neve._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final (azul acinzentado).")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((180, 200, 230, 200))
            lista_destino_existente.append(placeholder)

    @staticmethod
    def carregar_recursos_golem_neve():
        if Golem_Neve.sprites_andar_carregados is None:
            Golem_Neve.sprites_andar_carregados = []
            caminhos_andar = [
                "Sprites/Inimigos/Golem Neve/GN1.png",
                "Sprites/Inimigos/Golem Neve/GN2.png",
                "Sprites/Inimigos/Golem Neve/GN3.png",
            ]
            Golem_Neve._carregar_lista_sprites_estatico(
                caminhos_andar,
                Golem_Neve.sprites_andar_carregados,
                Golem_Neve.tamanho_sprite_definido,
                "Andar"
            )

        if Golem_Neve.sprites_atacar_carregados is None:
            Golem_Neve.sprites_atacar_carregados = []
            caminhos_atacar = [
                "Sprites/Inimigos/Golem Neve/GN_Atacar1.png",
                "Sprites/Inimigos/Golem Neve/GN_Atacar2.png",
                "Sprites/Inimigos/Golem Neve/GN_Atacar3.png",
            ]
            pasta_raiz_temp = Golem_Neve._obter_pasta_raiz_jogo()
            primeiro_sprite_ataque_existe = False
            if caminhos_atacar: # Verifica se a lista de caminhos de ataque não está vazia
                caminho_primeiro_ataque = os.path.join(pasta_raiz_temp, caminhos_atacar[0].replace("\\", "/"))
                if os.path.exists(caminho_primeiro_ataque):
                    primeiro_sprite_ataque_existe = True

            if primeiro_sprite_ataque_existe:
                Golem_Neve._carregar_lista_sprites_estatico(
                    caminhos_atacar,
                    Golem_Neve.sprites_atacar_carregados,
                    Golem_Neve.tamanho_sprite_definido,
                    "Atacar"
                )

            if not Golem_Neve.sprites_atacar_carregados:
                if Golem_Neve.sprites_andar_carregados and len(Golem_Neve.sprites_andar_carregados) > 0 :
                    Golem_Neve.sprites_atacar_carregados = [Golem_Neve.sprites_andar_carregados[0]]
                    # print("DEBUG(Golem_Neve.carregar_recursos): Usando primeiro sprite de andar como fallback para ataque.")
                else:
                    placeholder_ataque = pygame.Surface(Golem_Neve.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder_ataque.fill((180,200,230, 180)) # Azul acinzentado
                    Golem_Neve.sprites_atacar_carregados = [placeholder_ataque]
                    # print("DEBUG(Golem_Neve.carregar_recursos): Usando placeholder de cor para ataque (sprites de andar também falharam).")

        if not Golem_Neve.sons_carregados:
            # Golem_Neve.som_ataque_golem = Golem_Neve._carregar_som_golem_neve("Sons/Golem_Neve/ataque_impacto_neve.wav")
            # Golem_Neve.som_dano_golem = Golem_Neve._carregar_som_golem_neve("Sons/Golem_Neve/dano_quebrar_gelo.wav")
            # Golem_Neve.som_morte_golem = Golem_Neve._carregar_som_golem_neve("Sons/Golem_Neve/morte_desmoronar.wav")
            # Golem_Neve.som_spawn_golem = Golem_Neve._carregar_som_golem_neve("Sons/Golem_Neve/spawn_passos_pesados.wav")
            Golem_Neve.sons_carregados = True


    def __init__(self, x, y, velocidade=0.5): # Golem é lento
        Golem_Neve.carregar_recursos_golem_neve()

        vida_golem = 120
        dano_contato_golem = 120 # Dano de contato alto
        xp_golem = 600
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Golem Neve/GN1.png"
        #moedas_dropadas = 25

        super().__init__(
            x, y,
            Golem_Neve.tamanho_sprite_definido[0], Golem_Neve.tamanho_sprite_definido[1],
            vida_golem, velocidade, dano_contato_golem,
            xp_golem, sprite_path_principal_relativo_jogo
        )

        self.sprites_andar = Golem_Neve.sprites_andar_carregados
        self.sprites_atacar = Golem_Neve.sprites_atacar_carregados
        self.sprites = self.sprites_andar

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            # print("DEBUG(Golem_Neve __init__): self.image não foi definido pelo super(). Usando primeiro sprite de andar.")
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
            else:
                placeholder_img = pygame.Surface(Golem_Neve.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((150,180,210, 150))
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.sprite_index = 0
        self.intervalo_animacao_andar = 380 # Animação lenta
        self.intervalo_animacao_atacar = 280
        self.intervalo_animacao = self.intervalo_animacao_andar

        self.is_attacking = False
        self.attack_duration = 1.0 # Ataque mais demorado
        self.attack_timer = 0.0
        self.attack_damage_especifico = 45
        self.attack_range = 110  # Alcance um pouco maior para o soco
        self.attack_cooldown = 3.8
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)

        self.attack_hitbox_largura = Golem_Neve.tamanho_sprite_definido[0] * 0.6
        self.attack_hitbox_altura = Golem_Neve.tamanho_sprite_definido[1] * 0.4
        self.attack_hitbox_offset_x = 25
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_swing = False

        # if Golem_Neve.som_spawn_golem:
        #     Golem_Neve.som_spawn_golem.play()


    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0)
            return

        self.attack_hitbox.width = self.attack_hitbox_largura
        self.attack_hitbox.height = self.attack_hitbox_altura

        if self.facing_right:
            self.attack_hitbox.midleft = (self.rect.right - self.attack_hitbox_offset_x / 3, self.rect.centery)
        else:
            self.attack_hitbox.midright = (self.rect.left + self.attack_hitbox_offset_x / 3, self.rect.centery)


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
            self.hit_player_this_attack_swing = False

            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0

            # if Golem_Neve.som_ataque_golem:
            #     Golem_Neve.som_ataque_golem.play()


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): 
        if not self.esta_vivo():
            if not hasattr(self, "ouro_concedido") or not self.ouro_concedido:
                if hasattr(player, "dinheiro") and hasattr(self, "money_value"):
                    player.dinheiro += self.money_value
                score_manager.adicionar_xp(self.xp_value)
                self.ouro_concedido = True
            return

        agora = pygame.time.get_ticks()
        jogador_valido = (hasattr(player, 'rect') and
                          hasattr(player, 'vida') and
                          hasattr(player.vida, 'esta_vivo') and
                          hasattr(player, 'receber_dano'))

        if self.is_attacking:
            self.atualizar_animacao()
            self._atualizar_hitbox_ataque()

            if jogador_valido and not self.hit_player_this_attack_swing and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico)
                self.hit_player_this_attack_swing = True 
                # print(f"DEBUG(Golem_Neve): Ataque MELEE acertou jogador! Dano: {self.attack_damage_especifico}")

            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_andar
                self.intervalo_animacao = self.intervalo_animacao_andar
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

    def receber_dano(self, dano, fonte_dano_rect=None): # Adicionado fonte_dano_rect
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if self.esta_vivo():
            if vida_antes > self.hp and Golem_Neve.som_dano_golem:
                Golem_Neve.som_dano_golem.play()
        elif vida_antes > 0 and Golem_Neve.som_morte_golem:
            Golem_Neve.som_morte_golem.play()

    # O método desenhar é herdado da InimigoBase.
    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y)
    #     if self.is_attacking and self.attack_hitbox.width > 0: # Debug hitbox
    #         debug_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
    #         pygame.draw.rect(surface, (180, 200, 230, 100), debug_rect_onscreen, 1)

