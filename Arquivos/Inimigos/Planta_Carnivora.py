# Planta_Carnivora.py
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
    print(f"DEBUG(Planta_Carnivora): Classe InimigoBase importada com sucesso de .Inimigos.")
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
            print(f"DEBUG(InimigoBase Placeholder para Planta_Carnivora): Instanciado. Sprite path (não usado): {sprite_path}")
        
        def _carregar_sprite(self, path, tamanho): # Placeholder _carregar_sprite na base
            print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{path}' (não implementado). Retornando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((40,150,60, 128)) # Cor verde para placeholder do _carregar_sprite
            return img

        def receber_dano(self, dano, fonte_dano_rect=None): 
             self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt_ms=None): 
            pass 
        def atualizar_animacao(self): 
            if self.sprites and len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
                if hasattr(self, 'facing_right') and not self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)
        def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y): 
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self): 
            super().kill()


class Planta_Carnivora(InimigoBase):
    sprites_andar_carregados = None 
    sprites_atacar_carregados = None 
    tamanho_sprite_definido = (100, 120) # Ajuste conforme o sprite real

    som_ataque_planta = None
    som_dano_planta = None
    som_morte_planta = None
    # som_spawn_planta = None # Opcional
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        # Se Planta_Carnivora.py está em Jogo/Arquivos/Inimigos/
        # Para chegar na pasta raiz "Jogo/", subimos dois níveis.
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_planta_carnivora(caminho_relativo_a_raiz_jogo): # Renomeado
        pasta_raiz_jogo = Planta_Carnivora._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))
        
        if not os.path.exists(caminho_completo):
            print(f"DEBUG(Planta_Carnivora._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            print(f"DEBUG(Planta_Carnivora._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            print(f"DEBUG(Planta_Carnivora._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Planta_Carnivora._obter_pasta_raiz_jogo()
        print(f"DEBUG(Planta_Carnivora._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {pasta_raiz_jogo}")
        
        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            print(f"DEBUG(Planta_Carnivora._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                    print(f"DEBUG(Planta_Carnivora._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    print(f"DEBUG(Planta_Carnivora._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder (verde escuro).")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((20, 100, 20, 180)) # Cor verde escuro para placeholder
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                print(f"DEBUG(Planta_Carnivora._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder (verde escuro).")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((20, 100, 20, 180))
                lista_destino_existente.append(placeholder)
        
        if not lista_destino_existente: 
            print(f"DEBUG(Planta_Carnivora._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final (verde muito escuro).")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((10, 70, 10, 200))
            lista_destino_existente.append(placeholder)

    @staticmethod
    def carregar_recursos_planta_carnivora(): # Renomeado
        if Planta_Carnivora.sprites_andar_carregados is None: 
            Planta_Carnivora.sprites_andar_carregados = []
            caminhos_andar = [ # Ajuste os caminhos para os sprites da Planta Carnívora
                "Sprites/Inimigos/Planta_Carnivora/Planta_carnivora_1.png", 
                "Sprites/Inimigos/Planta_Carnivora/Planta_Carnivora_2.png",

            ]
            Planta_Carnivora._carregar_lista_sprites_estatico(
                caminhos_andar, 
                Planta_Carnivora.sprites_andar_carregados, 
                Planta_Carnivora.tamanho_sprite_definido, 
                "Andar/Idle"
            )

        if Planta_Carnivora.sprites_atacar_carregados is None:
            Planta_Carnivora.sprites_atacar_carregados = []
            caminhos_atacar = [ # Ajuste os caminhos para os sprites de ataque da Planta Carnívora
                "Sprites/Inimigos/Planta_Carnivora/Planta_carnivora_1.png", 
                "Sprites/Inimigos/Planta_Carnivora/Planta_Carnivora_2.png",
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
                    print("DEBUG(Planta_Carnivora.carregar_recursos): Usando primeiro sprite de andar como fallback para ataque.")
                else: 
                    placeholder_ataque = pygame.Surface(Planta_Carnivora.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder_ataque.fill((10,70,10, 180)) # Verde bem escuro
                    Planta_Carnivora.sprites_atacar_carregados = [placeholder_ataque]
                    print("DEBUG(Planta_Carnivora.carregar_recursos): Usando placeholder de cor para ataque.")
        
        if not Planta_Carnivora.sons_carregados:
            # Planta_Carnivora.som_ataque_planta = Planta_Carnivora._carregar_som_planta_carnivora("Sons/Planta_Carnivora/mordida.wav")
            # Planta_Carnivora.som_dano_planta = Planta_Carnivora._carregar_som_planta_carnivora("Sons/Planta_Carnivora/dano_planta.wav")
            # Planta_Carnivora.som_morte_planta = Planta_Carnivora._carregar_som_planta_carnivora("Sons/Planta_Carnivora/morte_planta.wav")
            Planta_Carnivora.sons_carregados = True
    

    def __init__(self, x, y, velocidade=0.5): # Plantas carnívoras podem ser lentas ou imóveis
        Planta_Carnivora.carregar_recursos_planta_carnivora() 

        vida_planta = 90
        dano_contato_planta = 8 
        xp_planta = 50
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Planta_Carnivora/Planta1.png"
        #moedas_dropas = 15

        super().__init__(
            x, y,
            Planta_Carnivora.tamanho_sprite_definido[0], Planta_Carnivora.tamanho_sprite_definido[1],
            vida_planta, velocidade, dano_contato_planta,
            xp_planta, sprite_path_principal_relativo_jogo
        )

        self.sprites_andar = Planta_Carnivora.sprites_andar_carregados
        self.sprites_atacar = Planta_Carnivora.sprites_atacar_carregados
        self.sprites = self.sprites_andar 
        
        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            print("DEBUG(Planta_Carnivora __init__): self.image não foi definido pelo super(). Usando primeiro sprite de andar.")
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
            else: 
                placeholder_img = pygame.Surface(Planta_Carnivora.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((10, 70, 10, 150)) 
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.sprite_index = 0
        self.intervalo_animacao_andar = 350 # Animação lenta
        self.intervalo_animacao_atacar = 250 
        self.intervalo_animacao = self.intervalo_animacao_andar

        self.is_attacking = False
        self.attack_duration = 0.8 # Duração da mordida/ataque
        self.attack_timer = 0.0
        self.attack_damage_especifico = 20 
        self.attack_range = 80  # Alcance da mordida/vinhas
        self.attack_cooldown = 2.8 
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)

        self.attack_hitbox_size = (Planta_Carnivora.tamanho_sprite_definido[0] * 0.7, Planta_Carnivora.tamanho_sprite_definido[1] * 0.5) 
        self.attack_hitbox_offset_y = -Planta_Carnivora.tamanho_sprite_definido[1] * 0.2 # Hitbox um pouco acima do centro para mordida
        self.attack_hitbox = pygame.Rect(0,0,0,0)
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
            
            # if Planta_Carnivora.som_ataque_planta:
            #     Planta_Carnivora.som_ataque_planta.play()


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): 
        if not self.esta_vivo():
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
                # print(f"DEBUG(Planta_Carnivora): Mordida acertou jogador! Dano: {self.attack_damage_especifico}")

            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False 
                self.sprites = self.sprites_andar 
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.sprite_index = 0 
                self.attack_hitbox.size = (0,0) 
        else: 
            if jogador_valido:
                self.atacar(player) 
            
            if not self.is_attacking and jogador_valido and self.velocidade > 0: # Só se move se tiver velocidade
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
            if vida_antes > self.hp and Planta_Carnivora.som_dano_planta:
                Planta_Carnivora.som_dano_planta.play()
        elif vida_antes > 0 and Planta_Carnivora.som_morte_planta: 
            Planta_Carnivora.som_morte_planta.play()

    # O método desenhar é herdado da InimigoBase.
    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y)
    #     if self.is_attacking and self.attack_hitbox.width > 0: # Debug hitbox
    #         debug_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
    #         pygame.draw.rect(surface, (0, 150, 0, 100), debug_rect_onscreen, 1)

