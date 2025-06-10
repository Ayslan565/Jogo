# Planta_Carnivora.py
import pygame
import os
import math
import time
import random

from score import score_manager  # <-- INTEGRAÇÃO DO SCORE

# --- Importação da Classe Base Inimigo ---
try:
    from .Inimigos import Inimigo as InimigoBase
    # print(f"DEBUG(Planta_Carnivora): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    print(f"DEBUG(Planta_Carnivora): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    # Este é um placeholder MUITO SIMPLES. A classe base real deve ser mais completa.
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((10, 120, 30, 100)) # Placeholder verde escuro para planta
            pygame.draw.rect(self.image, (50,150,50), self.image.get_rect(), 1) # Borda verde mais clara
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            # Adicionando atributos faltantes para compatibilidade com Planta_Carnivora __init__
            self.x = x 
            self.y = y
            print(f"DEBUG(InimigoBase Placeholder para Planta_Carnivora): Instanciado. Sprite path (não usado): {sprite_path}")

        def _carregar_sprite(self, path, tamanho): # Placeholder _carregar_sprite na base
            print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{path}' (não implementado). Retornando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((40,150,60, 128))
            return img

        def receber_dano(self, dano, fonte_dano_rect=None):
            self.hp = max(0, self.hp - dano)
            self.last_hit_time = pygame.time.get_ticks()
            # print(f"DEBUG(InimigoBase Placeholder): Inimigo recebeu {dano} de dano. HP atual: {self.hp}")

        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt_ms=None):
            # Implementação básica de movimento para o placeholder, se necessário
            if dt_ms is None: dt_ms = 16 # fallback
            dx = ax - self.rect.centerx
            dy = ay - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0 and self.velocidade > 0:
                dx, dy = dx / dist, dy / dist
                mov_x = dx * self.velocidade * (dt_ms / 1000.0) * 50 # Ajuste o multiplicador de velocidade conforme necessário
                mov_y = dy * self.velocidade * (dt_ms / 1000.0) * 50
                self.rect.x += mov_x
                self.rect.y += mov_y
                self.x = float(self.rect.x) # Atualiza x e y flutuantes
                self.y = float(self.rect.y)
                if dx > 0 : self.facing_right = True
                elif dx < 0: self.facing_right = False

        def atualizar_animacao(self):
            agora = pygame.time.get_ticks()
            if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                self.tempo_ultimo_update_animacao = agora
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
                self.image = self.sprites[self.sprite_index]
                if hasattr(self, 'facing_right') and not self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)
            # Flash de dano simples
            if hasattr(self, 'last_hit_time') and agora - self.last_hit_time < self.hit_flash_duration:
                if hasattr(self, 'image') and self.image: # Checa se image existe
                    flash_surface = self.image.copy()
                    flash_surface.fill(self.hit_flash_color, special_flags=pygame.BLEND_RGBA_MULT)
                    self.image.blit(flash_surface, (0,0))


        def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self):
            super().kill()


class Planta_Carnivora(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (60, 60)

    som_ataque_planta = None
    som_dano_planta = None
    som_morte_planta = None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_planta_carnivora(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Planta_Carnivora._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))
        if not os.path.exists(caminho_completo):
            # print(f"DEBUG(Planta_Carnivora._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            # print(f"DEBUG(Planta_Carnivora._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            # print(f"DEBUG(Planta_Carnivora._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Planta_Carnivora._obter_pasta_raiz_jogo()
        # print(f"DEBUG(Planta_Carnivora._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {pasta_raiz_jogo}")
        if lista_destino_existente is None: lista_destino_existente = []

        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            # print(f"DEBUG(Planta_Carnivora._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                    # print(f"DEBUG(Planta_Carnivora._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    # print(f"DEBUG(Planta_Carnivora._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder (verde escuro).")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((20, 100, 20, 180))
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                # print(f"DEBUG(Planta_Carnivora._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder (verde escuro).")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((20, 100, 20, 180))
                lista_destino_existente.append(placeholder)

        if not lista_destino_existente:
            # print(f"DEBUG(Planta_Carnivora._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final (verde muito escuro).")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((10, 70, 10, 200))
            lista_destino_existente.append(placeholder)

    @staticmethod
    def carregar_recursos_planta_carnivora():
        if Planta_Carnivora.sprites_andar_carregados is None:
            Planta_Carnivora.sprites_andar_carregados = []
            caminhos_andar = [
                "Sprites/Inimigos/Planta Carnivora/Planta carnivora 1.png",
                "Sprites/Inimigos/Planta Carnivora/Planta_Carnivora2.png",
            ]
            Planta_Carnivora._carregar_lista_sprites_estatico(
                caminhos_andar,
                Planta_Carnivora.sprites_andar_carregados,
                Planta_Carnivora.tamanho_sprite_definido,
                "Andar/Idle"
            )

        if Planta_Carnivora.sprites_atacar_carregados is None:
            Planta_Carnivora.sprites_atacar_carregados = []
            caminhos_atacar = [
                "Sprites/Inimigos/Planta Carnivora/Planta carnivora 1.png", # Usar os mesmos de andar como placeholder
                "Sprites/Inimigos/Planta Carnivora/Planta_Carnivora2.png",
            ]
            pasta_raiz_temp = Planta_Carnivora._obter_pasta_raiz_jogo()
            primeiro_sprite_ataque_existe = False
            if caminhos_atacar:
                caminho_primeiro_ataque = os.path.join(pasta_raiz_temp, caminhos_atacar[0].replace("\\", "/"))
                if os.path.exists(caminho_primeiro_ataque):
                    primeiro_sprite_ataque_existe = True

            if primeiro_sprite_ataque_existe:
                Planta_Carnivora._carregar_lista_sprites_estatico(
                    caminhos_atacar,
                    Planta_Carnivora.sprites_atacar_carregados,
                    Planta_Carnivora.tamanho_sprite_definido,
                    "Atacar"
                )

            if not Planta_Carnivora.sprites_atacar_carregados:
                if Planta_Carnivora.sprites_andar_carregados and len(Planta_Carnivora.sprites_andar_carregados) > 0 :
                    Planta_Carnivora.sprites_atacar_carregados = [Planta_Carnivora.sprites_andar_carregados[0]]
                    # print("DEBUG(Planta_Carnivora.carregar_recursos): Usando primeiro sprite de andar como fallback para ataque.")
                else:
                    placeholder_ataque = pygame.Surface(Planta_Carnivora.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder_ataque.fill((10,70,10, 180))
                    Planta_Carnivora.sprites_atacar_carregados = [placeholder_ataque]
                    # print("DEBUG(Planta_Carnivora.carregar_recursos): Usando placeholder de cor para ataque.")

        if not Planta_Carnivora.sons_carregados:
            # Planta_Carnivora.som_ataque_planta = Planta_Carnivora._carregar_som_planta_carnivora("Sons/Inimigos/Planta_Carnivora/mordida.wav")
            # Planta_Carnivora.som_dano_planta = Planta_Carnivora._carregar_som_planta_carnivora("Sons/Inimigos/Planta_Carnivora/dano_planta.wav")
            # Planta_Carnivora.som_morte_planta = Planta_Carnivora._carregar_som_planta_carnivora("Sons/Inimigos/Planta_Carnivora/morte_planta.wav")
            Planta_Carnivora.sons_carregados = True

    def __init__(self, x, y, velocidade=0.5):
        Planta_Carnivora.carregar_recursos_planta_carnivora()

        vida_planta = 90
        dano_contato_planta = 8
        xp_planta = 50
        # --- CAMINHO MODIFICADO ---
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Planta Carnivora/Planta carnivora 1.png"
        #moedas_dropas = 15

        super().__init__(
            x, y,
            Planta_Carnivora.tamanho_sprite_definido[0], Planta_Carnivora.tamanho_sprite_definido[1],
            vida_planta, velocidade, dano_contato_planta,
            xp_planta, sprite_path_principal_relativo_jogo
        )
        # Asignar x, y após super() se não forem definidos pela base ou forem necessários para o rect
        self.x = x
        self.y = y

        self.sprites_andar = Planta_Carnivora.sprites_andar_carregados
        self.sprites_atacar = Planta_Carnivora.sprites_atacar_carregados
        self.sprites = self.sprites_andar

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)) or \
           (self.sprites and len(self.sprites) > 0 and self.image is self.sprites[0] and self.sprites[0].get_size() != Planta_Carnivora.tamanho_sprite_definido): # Se a imagem base é placeholder e temos sprites carregados
            print("DEBUG(Planta_Carnivora __init__): self.image do super() não é adequado ou não definido. Usando primeiro sprite de andar.")
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0].copy()
            else:
                placeholder_img = pygame.Surface(Planta_Carnivora.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((10, 70, 10, 150))
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image] # Garante que self.sprites não seja None
        
        # Assegurar que self.rect exista e esteja correto.
        # O super().__init__() do placeholder já cria self.rect. Se o real não, descomentar/ajustar.
        # self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # No placeholder, self.rect já é criado, mas vamos garantir a posição inicial:
        self.rect.topleft = (self.x, self.y)


        self.sprite_index = 0
        self.intervalo_animacao_andar = 350
        self.intervalo_animacao_atacar = 250
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()

        self.is_attacking = False
        self.attack_duration = 0.8
        self.attack_timer = 0.0
        self.attack_damage_especifico = 20
        self.attack_range = 80  # Alcance da mordida/vinhas
        self.attack_cooldown = 2.8 # Em segundos
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000) # Permite atacar quase imediatamente

        self.attack_hitbox_size = (Planta_Carnivora.tamanho_sprite_definido[0] * 0.7, Planta_Carnivora.tamanho_sprite_definido[1] * 0.5)
        self.attack_hitbox_offset_y = -Planta_Carnivora.tamanho_sprite_definido[1] * 0.2 # Hitbox um pouco acima do centro para mordida
        self.attack_hitbox = pygame.Rect(0,0,0,0) # Será atualizado em _atualizar_hitbox_ataque
        self.hit_player_this_attack_swing = False

    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0)
            return

        w, h = self.attack_hitbox_size
        self.attack_hitbox.size = (w,h)

        # Hitbox de mordida à frente e um pouco acima
        if self.facing_right:
            self.attack_hitbox.left = self.rect.centerx
        else:
            self.attack_hitbox.right = self.rect.centerx
        self.attack_hitbox.centery = self.rect.centery + self.attack_hitbox_offset_y

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
            self.hit_player_this_attack_swing = False

            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = agora # Resetar timer da animação de ataque

            # if Planta_Carnivora.som_ataque_planta:
            #     Planta_Carnivora.som_ataque_planta.play()
            # print(f"DEBUG(Planta_Carnivora): Iniciando ataque. Sprites: {len(self.sprites_atacar)}")


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        # --- INTEGRAÇÃO DO SCORE ---
        if not self.esta_vivo():
            if not hasattr(self, "ouro_concedido") or not self.ouro_concedido:
                if hasattr(player, "dinheiro") and hasattr(self, "money_value"):
                    player.dinheiro += self.money_value
                if hasattr(self, "xp_value"):
                    score_manager.adicionar_xp(self.xp_value)
                self.ouro_concedido = True
            return

        agora = pygame.time.get_ticks()
        if dt_ms is None: # Delta time em milissegundos
            dt_ms = pygame.time.get_ticks() - getattr(self, '_last_update_time', agora)
            self._last_update_time = agora
            if dt_ms == 0 : dt_ms = 16 # Evitar dt_ms zero na primeira chamada ou se o tempo não avançou

        jogador_valido = (player is not None and hasattr(player, 'rect') and
                          hasattr(player, 'receber_dano')) # Simplificado, ajuste se 'vida' e 'esta_vivo' do jogador forem complexos

        if jogador_valido: # Virar para o jogador
            if player.rect.centerx < self.rect.centerx:
                self.facing_right = False
            else:
                self.facing_right = True

        if self.is_attacking:
            self.atualizar_animacao()
            self._atualizar_hitbox_ataque()

            if jogador_valido and not self.hit_player_this_attack_swing and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico, self.rect)
                self.hit_player_this_attack_swing = True

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
            # print(f"DEBUG(Planta_Carnivora): Dano de contato aplicado: {self.contact_damage}")

        # Lógica de flash de dano (se não estiver na base)
        if hasattr(self, 'last_hit_time') and (agora - self.last_hit_time < self.hit_flash_duration):
            # O flash em si é aplicado em atualizar_animacao se estiver usando o placeholder
            pass
        else:
            # Se o flash não estiver ativo, garantir que a imagem seja a correta (sem flash)
            # Isso é mais relevante se o flash for aplicado diretamente no self.image sem cópia
            if self.sprites and len(self.sprites) > self.sprite_index:
                 current_sprite_image = self.sprites[self.sprite_index]
                 if not self.facing_right:
                     current_sprite_image = pygame.transform.flip(current_sprite_image, True, False)
                 self.image = current_sprite_image

    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if self.esta_vivo():
            if vida_antes > self.hp and Planta_Carnivora.som_dano_planta:
                Planta_Carnivora.som_dano_planta.play()
        elif vida_antes > 0 and Planta_Carnivora.som_morte_planta:
            Planta_Carnivora.som_morte_planta.play()
            # print(f"DEBUG(Planta_Carnivora): Planta morreu. HP: {self.hp}")
            # self.kill() # A morte (remoção dos grupos) geralmente é gerenciada pelo loop principal do jogo


    # O método desenhar é herdado da InimigoBase.
    # Se precisar de debug visual para a hitbox de ataque, pode descomentar/modificar aqui ou na InimigoBase.
    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y) # Chama o desenhar da InimigoBase
        # --- DEBUG HITBOX DE ATAQUE (DESCOMENTE SE NECESSÁRIO) ---
        # if self.is_attacking and self.attack_hitbox.width > 0:
        #     debug_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
        #     pygame.draw.rect(surface, (0, 255, 0, 100), debug_rect_onscreen, 1) # Verde para hitbox de ataque
        # --- DEBUG RECT DO INIMIGO (DESCOMENTE SE NECESSÁRIO) ---
        # debug_enemy_rect_onscreen = self.rect.move(-camera_x, -camera_y)
        # pygame.draw.rect(surface, (255, 0, 0, 100), debug_enemy_rect_onscreen, 1) # Vermelho para rect principal