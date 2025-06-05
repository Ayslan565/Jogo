# Goblin.py
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
    # print(f"DEBUG(Goblin): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Goblin): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    # Este é um placeholder MUITO SIMPLES. A classe base real deve ser mais completa.
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((0, 80, 0, 100)) # Placeholder verde escuro
            pygame.draw.rect(self.image, (0,150,0), self.image.get_rect(), 1) # Borda verde mais clara
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            # print(f"DEBUG(InimigoBase Placeholder para Goblin): Instanciado. Sprite path (não usado): {sprite_path}")

        def _carregar_sprite(self, path, tamanho): # Placeholder _carregar_sprite
            # print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{path}' (não implementado). Retornando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((0,100,0, 128)) # Cor verde para placeholder do _carregar_sprite
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


class Goblin(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (55, 65) # Ajuste conforme necessário

    som_ataque_goblin = None
    som_dano_goblin = None
    som_morte_goblin = None
    som_spawn_goblin = None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        # Se Goblin.py está em Jogo/Arquivos/Inimigos/
        # Para chegar na pasta raiz "Jogo/", subimos dois níveis.
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_goblin(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Goblin._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))

        if not os.path.exists(caminho_completo):
            # print(f"DEBUG(Goblin._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            # print(f"DEBUG(Goblin._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            # print(f"DEBUG(Goblin._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Goblin._obter_pasta_raiz_jogo()
        # print(f"DEBUG(Goblin._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {pasta_raiz_jogo}")

        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            # print(f"DEBUG(Goblin._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                    # print(f"DEBUG(Goblin._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    # print(f"DEBUG(Goblin._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder (verde).")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((0, 100, 0, 180)) # Cor verde para placeholder
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                # print(f"DEBUG(Goblin._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder (verde).")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((0, 100, 0, 180))
                lista_destino_existente.append(placeholder)

        if not lista_destino_existente:
            # print(f"DEBUG(Goblin._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final (verde escuro).")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((0, 70, 0, 200))
            lista_destino_existente.append(placeholder)

    @staticmethod
    def carregar_recursos_goblin():
        if Goblin.sprites_andar_carregados is None:
            Goblin.sprites_andar_carregados = []
            caminhos_andar = [
                "Sprites/Inimigos/Goblin/goblin1.png",
                "Sprites/Inimigos/Goblin/goblin2.png",
                "Sprites/Inimigos/Goblin/goblin3.png",
                "Sprites/Inimigos/Goblin/goblin4.png",
            ]
            Goblin._carregar_lista_sprites_estatico(
                caminhos_andar,
                Goblin.sprites_andar_carregados,
                Goblin.tamanho_sprite_definido,
                "Andar"
            )

        if Goblin.sprites_atacar_carregados is None:
            Goblin.sprites_atacar_carregados = []
            caminhos_atacar = [
                "Sprites/Inimigos/Goblin/goblin_atacar1.png",
                "Sprites/Inimigos/Goblin/goblin_atacar2.png",
                "Sprites/Inimigos/Goblin/goblin_atacar3.png",
            ]
            pasta_raiz_temp = Goblin._obter_pasta_raiz_jogo()
            primeiro_sprite_ataque_existe = False
            if caminhos_atacar:
                caminho_primeiro_ataque = os.path.join(pasta_raiz_temp, caminhos_atacar[0].replace("\\", "/"))
                if os.path.exists(caminho_primeiro_ataque):
                    primeiro_sprite_ataque_existe = True

            if primeiro_sprite_ataque_existe:
                Goblin._carregar_lista_sprites_estatico(
                    caminhos_atacar,
                    Goblin.sprites_atacar_carregados,
                    Goblin.tamanho_sprite_definido,
                    "Atacar"
                )

            if not Goblin.sprites_atacar_carregados:
                if Goblin.sprites_andar_carregados and len(Goblin.sprites_andar_carregados) > 0 :
                    Goblin.sprites_atacar_carregados = [Goblin.sprites_andar_carregados[0]]
                    # print("DEBUG(Goblin.carregar_recursos): Usando primeiro sprite de andar como fallback para ataque.")
                else:
                    placeholder_ataque = pygame.Surface(Goblin.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder_ataque.fill((0,80,0, 180)) # Verde escuro
                    Goblin.sprites_atacar_carregados = [placeholder_ataque]
                    # print("DEBUG(Goblin.carregar_recursos): Usando placeholder de cor para ataque (sprites de andar também falharam).")

        if not Goblin.sons_carregados:
            # Goblin.som_ataque_goblin = Goblin._carregar_som_goblin("Sons/Goblin/ataque_adaga.wav")
            # Goblin.som_dano_goblin = Goblin._carregar_som_goblin("Sons/Goblin/dano_guincho.wav")
            # Goblin.som_morte_goblin = Goblin._carregar_som_goblin("Sons/Goblin/morte_rapida.wav")
            # Goblin.som_spawn_goblin = Goblin._carregar_som_goblin("Sons/Goblin/spawn_risada_curta.wav")
            Goblin.sons_carregados = True


    def __init__(self, x, y, velocidade=2.2):
        Goblin.carregar_recursos_goblin()

        vida_goblin = 50
        dano_contato_goblin = 7
        xp_goblin = 18
        self.moedas_drop = 5 # Quantidade de moedas que o Goblin dropa
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Goblin/goblin1.png"


        super().__init__(
            x, y,
            Goblin.tamanho_sprite_definido[0], Goblin.tamanho_sprite_definido[1],
            vida_goblin, velocidade, dano_contato_goblin,
            xp_goblin, sprite_path_principal_relativo_jogo
        )

        self.sprites_andar = Goblin.sprites_andar_carregados
        self.sprites_atacar = Goblin.sprites_atacar_carregados
        self.sprites = self.sprites_andar # Começa com animação de andar

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            # print("DEBUG(Goblin __init__): self.image não foi definido pelo super(). Usando primeiro sprite de andar.")
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
            else:
                placeholder_img = pygame.Surface(Goblin.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((0, 70, 0, 150))
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.sprite_index = 0
        self.intervalo_animacao_andar = 140
        self.intervalo_animacao_atacar = 90
        self.intervalo_animacao = self.intervalo_animacao_andar

        self.is_attacking = False
        self.attack_duration = 0.4 # Ataque rápido
        self.attack_timer = 0.0
        self.attack_damage_especifico = 12
        self.attack_range = 60  # Curto alcance para ataque corpo a corpo
        self.attack_cooldown = 1.5
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)

        self.attack_hitbox_largura = Goblin.tamanho_sprite_definido[0] * 0.7
        self.attack_hitbox_altura = Goblin.tamanho_sprite_definido[1] * 0.6
        self.attack_hitbox_offset_x = 10 # Quão à frente a hitbox aparece
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_swing = False

        # if Goblin.som_spawn_goblin:
        #     Goblin.som_spawn_goblin.play()


    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0)
            return

        self.attack_hitbox.width = self.attack_hitbox_largura
        self.attack_hitbox.height = self.attack_hitbox_altura

        if self.facing_right:
            self.attack_hitbox.midleft = (self.rect.right - self.attack_hitbox_offset_x / 2, self.rect.centery)
        else:
            self.attack_hitbox.midright = (self.rect.left + self.attack_hitbox_offset_x / 2, self.rect.centery)


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

            # if Goblin.som_ataque_goblin:
            #     Goblin.som_ataque_goblin.play()


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            return

        agora = pygame.time.get_ticks()
        jogador_valido = (hasattr(player, 'rect') and
                          hasattr(player, 'vida') and
                          hasattr(player.vida, 'esta_vivo') and
                          hasattr(player, 'receber_dano'))

        if self.is_attacking:
            self.atualizar_animacao() # Animação de ataque
            self._atualizar_hitbox_ataque()

            if jogador_valido and not self.hit_player_this_attack_swing and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico)
                self.hit_player_this_attack_swing = True
                # print(f"DEBUG(Goblin): Ataque MELEE acertou jogador! Dano: {self.attack_damage_especifico}")

            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_andar
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.sprite_index = 0
                self.attack_hitbox.size = (0,0) # Desativa hitbox
        else:
            if jogador_valido:
                self.atacar(player) # Tenta iniciar um ataque

            if not self.is_attacking and jogador_valido: # Se não começou a atacar, move-se
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)

            self.atualizar_animacao() # Animação de andar

        # Dano de contato (da InimigoBase, mas precisa ser chamado se não estiver no update da base)
        if jogador_valido and self.rect.colliderect(player.rect) and \
           (agora - self.last_contact_time >= self.contact_cooldown):
            player.receber_dano(self.contact_damage)
            self.last_contact_time = agora

    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if self.esta_vivo():
            if vida_antes > self.hp and Goblin.som_dano_goblin:
                Goblin.som_dano_goblin.play()
        elif vida_antes > 0 and Goblin.som_morte_goblin:
            Goblin.som_morte_goblin.play()

    # O método desenhar é herdado da InimigoBase.
    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y)
    #     if self.is_attacking and self.attack_hitbox.width > 0: # Debug hitbox
    #         debug_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
    #         pygame.draw.rect(surface, (0, 150, 0, 100), debug_rect_onscreen, 1)
