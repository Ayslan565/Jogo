# Lobo.py
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
    # print(f"DEBUG(Lobo): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Lobo): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    # Este é um placeholder MUITO SIMPLES. A classe base real deve ser mais completa.
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((100, 100, 100, 100)) # Placeholder cinza
            pygame.draw.rect(self.image, (150,150,150), self.image.get_rect(), 1) # Borda cinza clara
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0 # Ajustado para 200ms como nos outros
            self.x = float(x) # Adicionado para consistência
            self.y = float(y) # Adicionado para consistência
            # print(f"DEBUG(InimigoBase Placeholder para Lobo): Instanciado. Sprite path (não usado): {sprite_path}")

        def _carregar_sprite(self, path, tamanho): # Placeholder _carregar_sprite na base
            # print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{path}' (não implementado). Retornando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((100,100,100, 128)) # Cor cinza para placeholder do _carregar_sprite
            return img

        def receber_dano(self, dano, fonte_dano_rect=None):
             self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt_ms=None): # Adicionado dt_ms
            pass
        def atualizar_animacao(self):
            if self.sprites and len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0] # Usa o primeiro sprite
                if hasattr(self, 'facing_right') and not self.facing_right: # Adiciona flip se necessário
                    self.image = pygame.transform.flip(self.image, True, False)
        def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self):
            super().kill()


class Lobo(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (150, 100) # Ajuste conforme o sprite real do lobo

    som_ataque_lobo = None
    som_dano_lobo = None
    som_morte_lobo = None
    som_uivo_lobo = None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_lobo(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Lobo._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))

        if not os.path.exists(caminho_completo):
            # print(f"DEBUG(Lobo._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            # print(f"DEBUG(Lobo._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            # print(f"DEBUG(Lobo._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Lobo._obter_pasta_raiz_jogo()
        # print(f"DEBUG(Lobo._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {pasta_raiz_jogo}")

        if lista_destino_existente is None: lista_destino_existente = []

        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            # print(f"DEBUG(Lobo._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                    # print(f"DEBUG(Lobo._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    # print(f"DEBUG(Lobo._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder (cinza).")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((100, 100, 100, 180)) # Cor cinza para placeholder
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                # print(f"DEBUG(Lobo._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder (cinza).")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((100, 100, 100, 180))
                lista_destino_existente.append(placeholder)

        if not lista_destino_existente:
            # print(f"DEBUG(Lobo._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final (cinza escuro).")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((80, 80, 80, 200))
            lista_destino_existente.append(placeholder)


    @staticmethod
    def carregar_recursos_lobo():
        if Lobo.sprites_andar_carregados is None:
            Lobo.sprites_andar_carregados = []
            caminhos_andar = [
                "Sprites/Inimigos/Lobo/Lobo4.png",
                "Sprites/Inimigos/Lobo/Lobo5.png",
                "Sprites/Inimigos/Lobo/Lobo6.png",
            ]
            Lobo._carregar_lista_sprites_estatico(
                caminhos_andar,
                Lobo.sprites_andar_carregados,
                Lobo.tamanho_sprite_definido,
                "Andar/Correr"
            )

        if Lobo.sprites_atacar_carregados is None:
            Lobo.sprites_atacar_carregados = []
            caminhos_atacar = [
                "Sprites/Inimigos/Lobo/Lobo4.png", # Usando os mesmos de andar como placeholder para ataque
                "Sprites/Inimigos/Lobo/Lobo5.png",
                "Sprites/Inimigos/Lobo/Lobo6.png",
            ]
            pasta_raiz_temp = Lobo._obter_pasta_raiz_jogo()
            primeiro_sprite_ataque_existe = False
            if caminhos_atacar:
                caminho_primeiro_ataque = os.path.join(pasta_raiz_temp, caminhos_atacar[0].replace("\\", "/"))
                if os.path.exists(caminho_primeiro_ataque):
                    primeiro_sprite_ataque_existe = True

            if primeiro_sprite_ataque_existe:
                Lobo._carregar_lista_sprites_estatico(
                    caminhos_atacar,
                    Lobo.sprites_atacar_carregados,
                    Lobo.tamanho_sprite_definido,
                    "Atacar"
                )

            if not Lobo.sprites_atacar_carregados:
                if Lobo.sprites_andar_carregados and len(Lobo.sprites_andar_carregados) > 0 :
                    Lobo.sprites_atacar_carregados = [Lobo.sprites_andar_carregados[0]]
                    # print("DEBUG(Lobo.carregar_recursos): Usando primeiro sprite de andar como fallback para ataque.")
                else:
                    placeholder_ataque = pygame.Surface(Lobo.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder_ataque.fill((80,80,80, 180)) # Cinza escuro
                    Lobo.sprites_atacar_carregados = [placeholder_ataque]
                    # print("DEBUG(Lobo.carregar_recursos): Usando placeholder de cor para ataque.")

        if not Lobo.sons_carregados:
            # Lobo.som_ataque_lobo = Lobo._carregar_som_lobo("Sons/Lobo/mordida_lobo.wav")
            # Lobo.som_dano_lobo = Lobo._carregar_som_lobo("Sons/Lobo/ganido_lobo.wav")
            # Lobo.som_morte_lobo = Lobo._carregar_som_lobo("Sons/Lobo/morte_lobo.wav")
            # Lobo.som_uivo_lobo = Lobo._carregar_som_lobo("Sons/Lobo/uivo_lobo.wav")
            Lobo.sons_carregados = True


    def __init__(self, x, y, velocidade=2.5): # Lobos são geralmente rápidos
        Lobo.carregar_recursos_lobo()

        vida_lobo = 55
        dano_contato_lobo = 9 # Ajustado para um valor mais razoável para contato
        xp_lobo = 45
        self.moedas_drop = 6 # Quantidade de moedas que o Lobo dropa
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Lobo/Lobo1.png" # Usar um sprite válido ou o primeiro da lista de andar


        super().__init__(
            x, y,
            Lobo.tamanho_sprite_definido[0], Lobo.tamanho_sprite_definido[1],
            vida_lobo, velocidade, dano_contato_lobo,
            xp_lobo, sprite_path_principal_relativo_jogo
        )
        self.x = float(x) # Garante que x e y são floats
        self.y = float(y)

        self.sprites_andar = Lobo.sprites_andar_carregados
        self.sprites_atacar = Lobo.sprites_atacar_carregados
        self.sprites = self.sprites_andar

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)) or \
           (self.sprites and len(self.sprites) > 0 and self.image is self.sprites[0] and self.sprites[0].get_size() != Lobo.tamanho_sprite_definido): # Checa se a imagem do super é a default ou não escalada
            # print("DEBUG(Lobo __init__): self.image do super() não é adequado. Usando primeiro sprite de andar.")
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0].copy() # Usa uma cópia
            else:
                placeholder_img = pygame.Surface(Lobo.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((80, 80, 80, 150))
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))


        self.sprite_index = 0
        self.intervalo_animacao_andar = 120 # Animação de corrida/andar mais rápida
        self.intervalo_animacao_atacar = 100
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Inicializa o timer da animação

        self.is_attacking = False
        self.attack_duration = 0.5 # Mordida rápida
        self.attack_timer = 0.0
        self.attack_damage_especifico = 15 # Dano da mordida
        self.attack_range = 70  # Alcance da mordida
        self.attack_cooldown = 1.2
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)

        self.attack_hitbox_largura = Lobo.tamanho_sprite_definido[0] * 0.5 # Ajustar para a mordida
        self.attack_hitbox_altura = Lobo.tamanho_sprite_definido[1] * 0.4
        self.attack_hitbox_offset_x = Lobo.tamanho_sprite_definido[0] * 0.3 # Quão à frente a mordida alcança
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_swing = False

        # if Lobo.som_uivo_lobo and random.random() < 0.1: # Chance de uivar ao spawnar
        #     Lobo.som_uivo_lobo.play()


    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0)
            return

        self.attack_hitbox.width = self.attack_hitbox_largura
        self.attack_hitbox.height = self.attack_hitbox_altura

        if self.facing_right:
            # A hitbox deve estar à frente do lobo quando ele ataca para a direita
            self.attack_hitbox.left = self.rect.centerx # Começa no centro do lobo
            self.attack_hitbox.centery = self.rect.centery
        else:
            # A hitbox deve estar à frente do lobo quando ele ataca para a esquerda
            self.attack_hitbox.right = self.rect.centerx # Começa no centro do lobo
            self.attack_hitbox.centery = self.rect.centery


    def atacar(self, player):
        if not (hasattr(player, 'rect') and self.esta_vivo()):
            return

        agora = pygame.time.get_ticks()
        distancia_ao_jogador = float('inf') # Inicializa com infinito
        if hasattr(player, 'rect') and player.rect is not None: # Checa se player.rect existe
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
            self.tempo_ultimo_update_animacao = agora # Reseta o timer da animação de ataque

            # if Lobo.som_ataque_lobo:
            #     Lobo.som_ataque_lobo.play()


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            return

        agora = pygame.time.get_ticks()
        # Adiciona verificação de dt_ms e inicializa _last_update_time se não existir
        if dt_ms is None:
            dt_ms = agora - getattr(self, '_last_update_time', agora) # Usa getattr para segurança
            self._last_update_time = agora
            if dt_ms <= 0 : dt_ms = 16 # Evita dt_ms zero ou negativo

        jogador_valido = (player is not None and hasattr(player, 'rect') and player.rect is not None and
                          hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and
                          hasattr(player, 'receber_dano'))

        if jogador_valido: # Define a direção do lobo antes de qualquer outra lógica
            if player.rect.centerx < self.rect.centerx: self.facing_right = False
            else: self.facing_right = True

        if self.is_attacking:
            self.atualizar_animacao()
            self._atualizar_hitbox_ataque()

            if jogador_valido and not self.hit_player_this_attack_swing and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico, self.rect) # Passa o rect do lobo como fonte
                self.hit_player_this_attack_swing = True
                # print(f"DEBUG(Lobo): Mordida acertou jogador! Dano: {self.attack_damage_especifico}")

            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_andar
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.sprite_index = 0
                self.tempo_ultimo_update_animacao = agora # Reseta timer da animação de andar
                self.attack_hitbox.size = (0,0)
        else:
            if jogador_valido:
                self.atacar(player)

            if not self.is_attacking and self.velocidade > 0 : # Só se move se não estiver atacando e tiver velocidade
                if jogador_valido: # Garante que o jogador é válido para mover_em_direcao
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)

            self.atualizar_animacao()


        if jogador_valido and self.rect.colliderect(player.rect) and \
           (agora - self.last_contact_time >= self.contact_cooldown):
            player.receber_dano(self.contact_damage, self.rect) # Passa rect do lobo
            self.last_contact_time = agora
        
        # Aplica o flip da imagem baseado na direção APÓS todas as atualizações de estado e animação
        if self.sprites and len(self.sprites) > 0: # Verifica se há sprites
            idx = int(self.sprite_index % len(self.sprites))
            current_sprite_image = self.sprites[idx]
            if not self.facing_right:
                self.image = pygame.transform.flip(current_sprite_image, True, False)
            else:
                self.image = current_sprite_image # Já deve ser a versão virada para a direita


    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if self.esta_vivo():
            if vida_antes > self.hp and Lobo.som_dano_lobo:
                Lobo.som_dano_lobo.play()
        elif vida_antes > 0 and Lobo.som_morte_lobo:
            Lobo.som_morte_lobo.play()

    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y)
