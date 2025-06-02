# Troll.py
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
    print(f"DEBUG(Troll): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    print(f"DEBUG(Troll): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    # Este é um placeholder MUITO SIMPLES. A classe base real deve ser mais completa.
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((0, 70, 0, 100)) # Placeholder verde bem escuro
            pygame.draw.rect(self.image, (0,100,0), self.image.get_rect(), 1) # Borda verde escura
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0; 
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            print(f"DEBUG(InimigoBase Placeholder para Troll): Instanciado. Sprite path (não usado): {sprite_path}")
        
        def _carregar_sprite(self, path, tamanho): # Placeholder _carregar_sprite na base
            print(f"DEBUG(InimigoBase Placeholder _carregar_sprite): Tentando carregar '{path}' (não implementado). Retornando placeholder.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((0,80,0, 128)) # Cor verde escura para placeholder do _carregar_sprite
            return img

        def receber_dano(self, dano, fonte_dano_rect=None): # Adicionado fonte_dano_rect
             self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt_ms=None): # Adicionado dt_ms
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


class Troll(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (130, 160) # Ajuste conforme o sprite real

    som_ataque_troll = None
    som_dano_troll = None
    som_morte_troll = None
    som_spawn_troll = None 
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        # Se Troll.py está em Jogo/Arquivos/Inimigos/
        # Para chegar na pasta raiz "Jogo/", subimos dois níveis.
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_troll(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Troll._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))
        
        if not os.path.exists(caminho_completo):
            print(f"DEBUG(Troll._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            print(f"DEBUG(Troll._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            print(f"DEBUG(Troll._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Troll._obter_pasta_raiz_jogo()
        print(f"DEBUG(Troll._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {pasta_raiz_jogo}")
        
        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            print(f"DEBUG(Troll._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                    print(f"DEBUG(Troll._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    print(f"DEBUG(Troll._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder (verde escuro).")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((0, 80, 0, 180)) # Cor verde escuro para placeholder
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                print(f"DEBUG(Troll._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder (verde escuro).")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((0, 80, 0, 180))
                lista_destino_existente.append(placeholder)
        
        if not lista_destino_existente: 
            print(f"DEBUG(Troll._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final (verde bem escuro).")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((0, 50, 0, 200))
            lista_destino_existente.append(placeholder)

    @staticmethod
    def carregar_recursos_troll():
        if Troll.sprites_andar_carregados is None: 
            Troll.sprites_andar_carregados = []
            caminhos_andar = [
                "Sprites/Inimigos/Troll/Troll_Andar1.png", 
                "Sprites/Inimigos/Troll/Troll_Andar2.png",
                "Sprites/Inimigos/Troll/Troll_Andar3.png",
                "Sprites/Inimigos/Troll/Troll_Andar4.png",
            ]
            Troll._carregar_lista_sprites_estatico(
                caminhos_andar, 
                Troll.sprites_andar_carregados, 
                Troll.tamanho_sprite_definido, 
                "Andar"
            )

        if Troll.sprites_atacar_carregados is None:
            Troll.sprites_atacar_carregados = []
            caminhos_atacar = [ 
                "Sprites/Inimigos/Troll/Troll_Atacar1.png", 
                "Sprites/Inimigos/Troll/Troll_Atacar2.png",
                "Sprites/Inimigos/Troll/Troll_Atacar3.png",
            ]
            pasta_raiz_temp = Troll._obter_pasta_raiz_jogo()
            primeiro_sprite_ataque_existe = False
            if caminhos_atacar:
                caminho_primeiro_ataque = os.path.join(pasta_raiz_temp, caminhos_atacar[0].replace("\\", "/"))
                if os.path.exists(caminho_primeiro_ataque):
                    primeiro_sprite_ataque_existe = True
            
            if primeiro_sprite_ataque_existe:
                Troll._carregar_lista_sprites_estatico(
                    caminhos_atacar, 
                    Troll.sprites_atacar_carregados, 
                    Troll.tamanho_sprite_definido, 
                    "Atacar"
                )
            
            if not Troll.sprites_atacar_carregados: 
                if Troll.sprites_andar_carregados and len(Troll.sprites_andar_carregados) > 0 :
                    Troll.sprites_atacar_carregados = [Troll.sprites_andar_carregados[0]] 
                    print("DEBUG(Troll.carregar_recursos): Usando primeiro sprite de andar como fallback para ataque.")
                else: 
                    placeholder_ataque = pygame.Surface(Troll.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder_ataque.fill((0,70,0, 180)) # Verde escuro
                    Troll.sprites_atacar_carregados = [placeholder_ataque]
                    print("DEBUG(Troll.carregar_recursos): Usando placeholder de cor para ataque.")
        
        if not Troll.sons_carregados:
            # Troll.som_ataque_troll = Troll._carregar_som_troll("Sons/Troll/ataque_paulada.wav") 
            # Troll.som_dano_troll = Troll._carregar_som_troll("Sons/Troll/dano_grunhido.wav")
            # Troll.som_morte_troll = Troll._carregar_som_troll("Sons/Troll/morte_queda.wav")
            # Troll.som_spawn_troll = Troll._carregar_som_troll("Sons/Troll/spawn_rugido.wav") 
            Troll.sons_carregados = True
    

    def __init__(self, x, y, velocidade=1.0): # Trolls são geralmente lentos mas fortes
        Troll.carregar_recursos_troll() 

        vida_troll = 180
        dano_contato_troll = 18
        xp_troll = 90
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Troll/Troll_Andar1.png"

        super().__init__(
            x, y,
            Troll.tamanho_sprite_definido[0], Troll.tamanho_sprite_definido[1],
            vida_troll, velocidade, dano_contato_troll,
            xp_troll, sprite_path_principal_relativo_jogo
        )

        self.sprites_andar = Troll.sprites_andar_carregados
        self.sprites_atacar = Troll.sprites_atacar_carregados
        self.sprites = self.sprites_andar 
        
        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            print("DEBUG(Troll __init__): self.image não foi definido pelo super(). Usando primeiro sprite de andar.")
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
            else: 
                placeholder_img = pygame.Surface(Troll.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((0, 70, 0, 150)) 
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.sprite_index = 0
        self.intervalo_animacao_andar = 300 
        self.intervalo_animacao_atacar = 220 
        self.intervalo_animacao = self.intervalo_animacao_andar

        self.is_attacking = False
        self.attack_duration = 1.0 # Ataque com clava pode ser mais demorado
        self.attack_timer = 0.0
        self.attack_damage_especifico = 35 
        self.attack_range = 100  # Alcance do ataque com clava
        self.attack_cooldown = 3.2 
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)

        self.attack_hitbox_largura = Troll.tamanho_sprite_definido[0] * 0.7
        self.attack_hitbox_altura = Troll.tamanho_sprite_definido[1] * 0.5
        self.attack_hitbox_offset_x = 25 
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_swing = False
        
        # if Troll.som_spawn_troll:
        #     Troll.som_spawn_troll.play()


    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0)
            return
        
        self.attack_hitbox.width = self.attack_hitbox_largura
        self.attack_hitbox.height = self.attack_hitbox_altura
        
        if self.facing_right:
            self.attack_hitbox.left = self.rect.right - self.attack_hitbox_offset_x 
            self.attack_hitbox.centery = self.rect.centery
        else:
            self.attack_hitbox.right = self.rect.left + self.attack_hitbox_offset_x
            self.attack_hitbox.centery = self.rect.centery


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
            
            # if Troll.som_ataque_troll:
            #     Troll.som_ataque_troll.play()


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
                # print(f"DEBUG(Troll): Ataque MELEE acertou jogador! Dano: {self.attack_damage_especifico}")

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
            if vida_antes > self.hp and Troll.som_dano_troll:
                Troll.som_dano_troll.play()
        elif vida_antes > 0 and Troll.som_morte_troll: 
            Troll.som_morte_troll.play()

    # O método desenhar é herdado da InimigoBase.
    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y)
    #     if self.is_attacking and self.attack_hitbox.width > 0: # Debug hitbox
    #         debug_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
    #         pygame.draw.rect(surface, (0, 100, 0, 100), debug_rect_onscreen, 1)

