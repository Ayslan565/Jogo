# Fantasma.py
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
    # print(f"DEBUG(Fantasma): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Fantasma): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    # Este é um placeholder MUITO SIMPLES. A classe base real deve ser mais completa.
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((150, 150, 180, 100)) # Placeholder cinza-azulado
            pygame.draw.rect(self.image, (220,220,250), self.image.get_rect(), 1) # Borda azul clara
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            # print(f"DEBUG(InimigoBase Placeholder para Fantasma): Instanciado. Sprite path (não usado): {sprite_path}")

        def _carregar_sprite(self, path, tamanho): # Placeholder _carregar_sprite
            # print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{path}' (não implementado). Retornando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((200,200,255, 128)) # Cor azul claro para placeholder do _carregar_sprite
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


class Fantasma(InimigoBase):
    sprites_animacao_carregados = None # Renomeado de sprites_carregados para clareza
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (70, 90) # Ajuste conforme necessário

    som_ataque_fantasma = None
    som_dano_fantasma = None
    som_morte_fantasma = None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        # Se Fantasma.py está em Jogo/Arquivos/Inimigos/
        # Para chegar na pasta raiz "Jogo/", subimos dois níveis.
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_fantasma(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Fantasma._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))

        if not os.path.exists(caminho_completo):
            # print(f"DEBUG(Fantasma._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            # print(f"DEBUG(Fantasma._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            # print(f"DEBUG(Fantasma._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Fantasma._obter_pasta_raiz_jogo()
        # print(f"DEBUG(Fantasma._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {pasta_raiz_jogo}")

        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            # print(f"DEBUG(Fantasma._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                    # print(f"DEBUG(Fantasma._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    # print(f"DEBUG(Fantasma._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder (azul claro).")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((200, 200, 255, 180)) # Cor azul claro para placeholder
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                # print(f"DEBUG(Fantasma._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder (azul claro).")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((200, 200, 255, 180))
                lista_destino_existente.append(placeholder)

        if not lista_destino_existente:
            # print(f"DEBUG(Fantasma._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final (azul escuro).")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((180, 180, 230, 200))
            lista_destino_existente.append(placeholder)
        # A lista é modificada no local, não precisa retornar.

    @staticmethod
    def carregar_recursos_fantasma():
        if Fantasma.sprites_animacao_carregados is None:
            Fantasma.sprites_animacao_carregados = [] # Inicializa a lista
            caminhos_animacao = [
                "Sprites/Inimigos/Fantasma/Fantasma1.png",
                "Sprites/Inimigos/Fantasma/Fantasma2.png",
                "Sprites/Inimigos/Fantasma/Fantasma3.png",
                "Sprites/Inimigos/Fantasma/Fantasma4.png",
                "Sprites/Inimigos/Fantasma/Fantasma5.png",
                "Sprites/Inimigos/Fantasma/Fantasma6.png",
                # "Sprites/Inimigos/Fantasma/Fantasma7.png", # Se existir
                "Sprites/Inimigos/Fantasma/Fantasma8.png",
                "Sprites/Inimigos/Fantasma/Fantasma9.png",
            ]
            Fantasma._carregar_lista_sprites_estatico(
                caminhos_animacao,
                Fantasma.sprites_animacao_carregados,
                Fantasma.tamanho_sprite_definido,
                "Flutuar"
            )

            # Fantasma.sprites_atacar_carregados = [] # Inicializa se for usar
            # caminhos_atacar = ["Sprites/Inimigos/Fantasma/Fantasma_Atk1.png", ...]
            # Fantasma._carregar_lista_sprites_estatico(
            #     caminhos_atacar,
            #     Fantasma.sprites_atacar_carregados,
            #     Fantasma.tamanho_sprite_definido,
            #     "Atacar"
            # )
            if not Fantasma.sprites_atacar_carregados and Fantasma.sprites_animacao_carregados:
                 Fantasma.sprites_atacar_carregados = [Fantasma.sprites_animacao_carregados[0]] # Fallback

        if not Fantasma.sons_carregados:
            # Fantasma.som_ataque_fantasma = Fantasma._carregar_som_fantasma("Sons/Fantasma/sopro_fantasma.wav")
            # Fantasma.som_dano_fantasma = Fantasma._carregar_som_fantasma("Sons/Fantasma/gemido_fantasma.wav")
            # Fantasma.som_morte_fantasma = Fantasma._carregar_som_fantasma("Sons/Fantasma/desaparecer_fantasma.wav")
            Fantasma.sons_carregados = True


    def __init__(self, x, y, velocidade=1.7): # Velocidade um pouco maior para fantasma
        Fantasma.carregar_recursos_fantasma()

        vida_fantasma = 40
        dano_contato_fantasma = 4
        xp_fantasma = 25
        self.moedas_drop = 11 # Quantidade de moedas que o Fantasma dropa

        # O _carregar_sprite da InimigoBase será usado para esta imagem principal.
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Fantasma/Fantasma1.png"

        super().__init__(
            x, y,
            Fantasma.tamanho_sprite_definido[0], Fantasma.tamanho_sprite_definido[1],
            vida_fantasma, velocidade, dano_contato_fantasma,
            xp_fantasma, sprite_path_principal_relativo_jogo
        )

        self.sprites_flutuar = Fantasma.sprites_animacao_carregados
        self.sprites_atacar = Fantasma.sprites_atacar_carregados if Fantasma.sprites_atacar_carregados else self.sprites_flutuar
        self.sprites = self.sprites_flutuar # Começa com animação de flutuar

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            # print("DEBUG(Fantasma __init__): self.image não foi definido pelo super(). Usando primeiro sprite de animação.")
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
            else:
                placeholder_img = pygame.Surface(Fantasma.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((180, 180, 230, 150))
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.sprite_index = random.randint(0, len(self.sprites) -1 if self.sprites else 0) # Começa em frame aleatório
        self.intervalo_animacao_flutuar = 130
        self.intervalo_animacao_atacar = 100
        self.intervalo_animacao = self.intervalo_animacao_flutuar

        # Atributos específicos de ataque do Fantasma (ex: um ataque de toque rápido ou um debuff)
        self.is_attacking = False
        self.attack_duration = 0.5 # Duração do estado de ataque (s)
        self.attack_timer = 0.0
        self.attack_damage_especifico = 8
        self.attack_hitbox_size = (Fantasma.tamanho_sprite_definido[0] * 0.8, Fantasma.tamanho_sprite_definido[1] * 0.8)
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.attack_range = 60 # Fantasmas atacam de perto
        self.attack_cooldown = 2.2
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)
        self.hit_player_this_attack_swing = False # Renomeado para clareza

        # Comportamento de flutuação/transparência (opcional)
        self.alpha = 255
        self.fading_in = False
        self.fade_speed = 5 # Quão rápido ele desaparece/reaparece
        self.min_alpha = 80
        self.max_alpha = 255


    def _atualizar_hitbox_ataque(self):
        """Atualiza a hitbox de ataque para estar centrada no fantasma."""
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
        distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                         self.rect.centery - player.rect.centery)

        if not self.is_attacking and \
           distancia_ao_jogador <= self.attack_range and \
           (agora - self.last_attack_time >= self.attack_cooldown * 1000):

            self.is_attacking = True
            self.attack_timer = agora
            self.last_attack_time = agora
            self.hit_player_this_attack_swing = False

            self.sprites = self.sprites_atacar # Muda para sprites de ataque (se houver)
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0
            # if Fantasma.som_ataque_fantasma: Fantasma.som_ataque_fantasma.play()


    def _atualizar_flutuacao_alpha(self):
        """Faz o fantasma piscar ou mudar sua transparência."""
        if self.fading_in:
            self.alpha += self.fade_speed
            if self.alpha >= self.max_alpha:
                self.alpha = self.max_alpha
                self.fading_in = False
        else:
            self.alpha -= self.fade_speed
            if self.alpha <= self.min_alpha:
                self.alpha = self.min_alpha
                self.fading_in = True

        if hasattr(self, 'image') and self.image is not None:
            try:
                self.image.set_alpha(int(self.alpha))
            except pygame.error: # Pode acontecer se a surface não suportar alpha por pixel
                pass


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            return

        agora = pygame.time.get_ticks()
        jogador_valido = (hasattr(player, 'rect') and
                          hasattr(player, 'vida') and
                          hasattr(player.vida, 'esta_vivo') and
                          hasattr(player, 'receber_dano'))

        self._atualizar_flutuacao_alpha() # Aplica efeito de transparência

        if self.is_attacking:
            self.atualizar_animacao()
            self._atualizar_hitbox_ataque()

            if jogador_valido and not self.hit_player_this_attack_swing and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico)
                self.hit_player_this_attack_swing = True

            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_flutuar
                self.intervalo_animacao = self.intervalo_animacao_flutuar
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

    # O método desenhar é herdado da InimigoBase.
    # A transparência já é aplicada à self.image em _atualizar_flutuacao_alpha.
