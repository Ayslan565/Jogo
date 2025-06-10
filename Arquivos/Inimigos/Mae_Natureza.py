# Lobo.py
import pygame
import os
import math
import time

from score import score_manager  # <-- INTEGRAÇÃO DO SCORE

# --- Importação da Classe Base Inimigo ---
try:
    from .Inimigos import Inimigo as InimigoBase
    print(f"DEBUG(Mae_Natureza): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    print(f"DEBUG(Mae_Natureza): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
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
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            print(f"DEBUG(InimigoBase Placeholder para Mae_Natureza): Instanciado. Sprite path (não usado): {sprite_path}")
        
        def _carregar_sprite(self, path, tamanho): # Placeholder _carregar_sprite na base
            # A implementação real deste método na sua classe InimigoBase
            # deve ser capaz de encontrar a pasta raiz do jogo.
            print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{path}' (não implementado). Retornando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((100,100,100, 128))
            return img

        def receber_dano(self, dano, fonte_dano_rect=None):
             self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt_ms=None): 
            pass 
        def atualizar_animacao(self): 
            if self.sprites and len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
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

    som_ataque_lobo = None
    som_dano_lobo = None
    som_morte_lobo = None
    som_uivo_lobo = None 
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_lobo(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Lobo._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))
        
        if not os.path.exists(caminho_completo):
            print(f"DEBUG(Mae_Natureza._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            print(f"DEBUG(Mae_Natureza._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            print(f"DEBUG(Mae_Natureza._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Mae_Natureza._obter_pasta_raiz_jogo()
        print(f"DEBUG(Mae_Natureza._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {pasta_raiz_jogo}")
        
        # A lista_destino_existente já deve ser uma lista inicializada antes de chamar esta função.
        
        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            print(f"DEBUG(Mae_Natureza._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                    print(f"DEBUG(Mae_Natureza._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    print(f"DEBUG(Mae_Natureza._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder (verde floresta).")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((100, 100, 100, 180))
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                print(f"DEBUG(Mae_Natureza._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder (verde floresta).")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((100, 100, 100, 180))
                lista_destino_existente.append(placeholder)
        
        if not lista_destino_existente: 
            print(f"DEBUG(Mae_Natureza._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final (verde escuro).")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((80, 80, 80, 200))
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
            pasta_raiz_temp = Lobo._obter_pasta_raiz_jogo()
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
                    print("DEBUG(Mae_Natureza.carregar_recursos): Usando primeiro sprite de andar como fallback para ataque.")
                else: 
                    placeholder_ataque = pygame.Surface(Mae_Natureza.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder_ataque.fill((20,100,20, 180)) # Verde escuro
                    Mae_Natureza.sprites_atacar_carregados = [placeholder_ataque]
                    print("DEBUG(Mae_Natureza.carregar_recursos): Usando placeholder de cor para ataque.")
        
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
        #moedas_dropadas = 17
        
        # O _carregar_sprite da InimigoBase (herdada) será usado para esta imagem principal.
        # O caminho DEVE SER RELATIVO À PASTA RAIZ DO JOGO.
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Mae_Natureza/Mae1.png"

        super().__init__(
            x, y,
            Lobo.tamanho_sprite_definido[0], Lobo.tamanho_sprite_definido[1],
            vida_lobo, velocidade, dano_contato_lobo,
            self.xp_value, sprite_path_principal_relativo_jogo
        )
        self.x = float(x) # Garante que x e y são floats
        self.y = float(y)

        self.sprites_andar = Mae_Natureza.sprites_andar_carregados
        self.sprites_atacar = Mae_Natureza.sprites_atacar_carregados
        self.sprites = self.sprites_andar # Começa com animação de andar/idle
        
        # Garante que self.image e self.sprites[0] são válidos após o super().__init__
        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            print("DEBUG(Mae_Natureza __init__): self.image não foi definido corretamente pelo super(). Usando primeiro sprite de andar.")
            if self.sprites and len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
            else: # Fallback crítico se nem os sprites de andar carregaram
                placeholder_img = pygame.Surface(Mae_Natureza.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((20, 100, 20, 150)) # Verde escuro para erro
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.sprite_index = 0
        self.intervalo_animacao_andar = 300 
        self.intervalo_animacao_atacar = 220 
        self.intervalo_animacao = self.intervalo_animacao_andar # Começa com o intervalo de andar

        # Atributos específicos de ataque da Mãe Natureza (ex: ataque de área)
        self.is_attacking = False 
        self.attack_duration = 1.2 # Duração do ataque de área
        self.attack_timer = 0.0
        self.attack_damage_especifico = 30 
        self.attack_range = 180  # Alcance para iniciar o ataque de área
        self.attack_cooldown = 4.5 
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000) # Permite atacar logo

        # Hitbox para ataque de área (pode ser o próprio rect ou maior)
        self.attack_hitbox_size = (Mae_Natureza.tamanho_sprite_definido[0] * 1.5, Mae_Natureza.tamanho_sprite_definido[1] * 1.5) 
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_pulse = False # Para dano de área/pulso
        
    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0)
            return
        
        w, h = self.attack_hitbox_size
        self.attack_hitbox.size = (w,h)
        self.attack_hitbox.center = self.rect.center # Ataque de área centrado nela


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
            self.hit_player_this_attack_pulse = False
            
            self.sprites = self.sprites_atacar # Muda para sprites de ataque (se houver)
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0 
            
            # if Mae_Natureza.som_ataque_mae:
            #     Mae_Natureza.som_ataque_mae.play()


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): 
        if not self.esta_vivo():
            if not hasattr(self, "ouro_concedido") or not self.ouro_concedido:
                if hasattr(player, "dinheiro") and hasattr(self, "money_value"):
                    player.dinheiro += self.money_value
                if hasattr(self, "xp_value"):
                    score_manager.adicionar_xp(self.xp_value)
                self.ouro_concedido = True
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
            self.atualizar_animacao() # Continua a animação de ataque
            self._atualizar_hitbox_ataque()

            # Verifica colisão do ataque de área com o jogador
            if jogador_valido and not self.hit_player_this_attack_pulse and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico)
                self.hit_player_this_attack_pulse = True 
                # print(f"DEBUG(Mae_Natureza): Ataque de área acertou jogador! Dano: {self.attack_damage_especifico}")

            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False 
                self.sprites = self.sprites_andar # Volta para sprites de andar/idle
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.sprite_index = 0 
                self.attack_hitbox.size = (0,0) # Desativa a hitbox
        else: 
            # Se não está atacando, tenta iniciar um ataque ou se move
            if jogador_valido:
                self.atacar(player) # Tenta iniciar um ataque
            
            if not self.is_attacking and jogador_valido: # Se não iniciou um ataque, move-se
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
            
            self.atualizar_animacao() # Animação de andar/idle

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
    #     if self.is_attacking and self.attack_hitbox.width > 0: # Debug hitbox
    #         debug_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
    #         pygame.draw.ellipse(surface, (34, 139, 34, 100), debug_rect_onscreen, 2) # Elipse verde para área

