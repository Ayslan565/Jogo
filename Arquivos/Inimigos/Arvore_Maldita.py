# Arvore_Maldita.py
import pygame
import os
import math
import random

from Arquivos.Inimigos.score import score_manager  # <-- INTEGRAÇÃO DO SCORE

# --- Importação da Classe Base Inimigo ---
try:
    from .Inimigos import Inimigo as InimigoBase
    print(f"DEBUG(Arvore_Maldita): Classe InimigoBase importada com sucesso.")
except ImportError as e:
    print(f"DEBUG(Arvore_Maldita): FALHA ao importar InimigoBase: {e}. Usando placeholder local MUITO BÁSICO.")
    class InimigoBase(pygame.sprite.Sprite): # Placeholder
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA) # SRCALPHA para transparência
            self.image.fill((80, 40, 20, 150)) # Cor marrom translúcida para placeholder
            pygame.draw.rect(self.image, (100,60,30), self.image.get_rect(), 1) # Contorno
            self.hp = vida_maxima
            self.max_hp = vida_maxima
            self.velocidade = velocidade # Armazena a velocidade
            self.contact_damage = dano_contato
            self.xp_value = xp_value # adicione um valor de XP Aqui 
            self.facing_right = True # Direção inicial
            self.last_hit_time = 0 # Para efeito de flash ao ser atingido
            self.hit_flash_duration = 150 # Duração do flash em ms
            self.hit_flash_color = (255, 255, 255, 128) # Cor do flash (branco translúcido)
            self.contact_cooldown = 1000 # Cooldown para dano de contato em ms
            self.last_contact_time = 0
            self.sprites = [self.image] # Lista de sprites para animação (inicia com a imagem placeholder)
            self.sprite_index = 0 # Índice do sprite atual na animação
            self.intervalo_animacao = 200 # Intervalo entre frames da animação em ms
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Para controlar o tempo da animação
            self.x = float(x) # Coordenada X (float para movimento suave)
            self.y = float(y) # Coordenada Y (float para movimento suave)
            print(f"DEBUG(InimigoBase Placeholder para Arvore_Maldita): Instanciado. Velocidade: {self.velocidade}")

        def _carregar_sprite(self, path, tamanho):
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((70,30,10, 128))
            return img

        def receber_dano(self, dano, fonte_dano_rect=None):
            self.hp = max(0, self.hp - dano)
            self.last_hit_time = pygame.time.get_ticks()

        def esta_vivo(self):
            return self.hp > 0

        def mover_em_direcao(self, ax, ay, dt_ms=None):
            if not self.velocidade > 0: return
            if dt_ms is None: dt_ms = 16
            dx = ax - self.rect.centerx
            dy = ay - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                norm_dx = dx / dist
                norm_dy = dy / dist
                mov_x = norm_dx * self.velocidade * (dt_ms / 1000.0) * 50
                mov_y = norm_dy * self.velocidade * (dt_ms / 1000.0) * 50
                self.rect.x += mov_x
                self.rect.y += mov_y
                self.x = float(self.rect.centerx)
                self.y = float(self.rect.centery)
                if dx > 0 : self.facing_right = True
                elif dx < 0: self.facing_right = False

        def atualizar_animacao(self):
            agora = pygame.time.get_ticks()
            if not self.sprites or len(self.sprites) == 0: return
            if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                self.tempo_ultimo_update_animacao = agora
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
                base_image = self.sprites[self.sprite_index]
                if hasattr(self, 'facing_right') and not self.facing_right:
                    self.image = pygame.transform.flip(base_image, True, False)
                else:
                    self.image = base_image.copy()
            elif not hasattr(self, 'image') or self.image is None:
                base_image = self.sprites[self.sprite_index]
                if hasattr(self, 'facing_right') and not self.facing_right:
                    self.image = pygame.transform.flip(base_image, True, False)
                else:
                    self.image = base_image.copy()
            if hasattr(self, 'last_hit_time') and agora - self.last_hit_time < self.hit_flash_duration:
                if hasattr(self, 'image') and self.image is not None:
                    flash_overlay = self.image.copy()
                    try:
                        flash_overlay.fill(self.hit_flash_color, special_flags=pygame.BLEND_RGBA_MULT)
                        self.image.blit(flash_overlay, (0,0))
                    except pygame.error:
                        simple_flash = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                        simple_flash.fill(self.hit_flash_color)
                        self.image.blit(simple_flash, (0,0))

        def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            self.atualizar_animacao()

        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        
        def kill(self):
            super().kill()

class Arvore_Maldita(InimigoBase):
    sprites_idle_arvore_carregados = None
    sprites_ataque_principal_arvore_carregados = None
    tamanho_sprite_definido = (250, 300)
    som_ataque_arvore = None
    som_dano_arvore = None
    som_morte_arvore = None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_arvore_maldita(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Arvore_Maldita._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", os.sep))
        if not os.path.exists(caminho_completo):
            print(f"AVISO (Arvore_Maldita): Arquivo de som não encontrado: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            print(f"DEBUG (Arvore_Maldita): Som carregado: {caminho_completo}")
            return som
        except pygame.error as e:
            print(f"ERRO (Arvore_Maldita): Falha ao carregar som {caminho_completo}: {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Arvore_Maldita._obter_pasta_raiz_jogo()
        if lista_destino_existente is None: lista_destino_existente = []
        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", os.sep))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino_existente.append(sprite)
                else:
                    print(f"AVISO (Arvore_Maldita): Sprite '{nome_animacao}' não encontrado: {caminho_completo}. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((60, 30, 10, 180))
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                print(f"ERRO (Arvore_Maldita): Falha ao carregar sprite '{nome_animacao}' de {caminho_completo}: {e}. Usando placeholder.")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((60, 30, 10, 180))
                lista_destino_existente.append(placeholder)
        if not lista_destino_existente:
            print(f"AVISO (Arvore_Maldita): Nenhum sprite carregado para '{nome_animacao}'. Adicionando placeholder genérico para a animação.")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((40, 20, 5, 200))
            lista_destino_existente.append(placeholder)

    @staticmethod
    def carregar_recursos_arvore_maldita():
        if Arvore_Maldita.sprites_idle_arvore_carregados is None:
            Arvore_Maldita.sprites_idle_arvore_carregados = []
            caminhos_idle = [
                "Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita1.png",
                "Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita2.png",
                "Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita3.png",
            ]
            Arvore_Maldita._carregar_lista_sprites_estatico(caminhos_idle, Arvore_Maldita.sprites_idle_arvore_carregados, Arvore_Maldita.tamanho_sprite_definido, "ArvoreMaldita_Idle")

        if Arvore_Maldita.sprites_ataque_principal_arvore_carregados is None:
            Arvore_Maldita.sprites_ataque_principal_arvore_carregados = []
            caminhos_ataque_principal = [
                "Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita1.png",
                "Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita2.png",
                "Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita3.png",
            ]
            primeiro_sprite_path_completo = ""
            if caminhos_ataque_principal:
                primeiro_sprite_path_completo = os.path.join(Arvore_Maldita._obter_pasta_raiz_jogo(), caminhos_ataque_principal[0].replace("\\", os.sep))
            if not caminhos_ataque_principal or not os.path.exists(primeiro_sprite_path_completo):
                print(f"AVISO (Arvore_Maldita): Sprites de ataque principal não encontrados ou lista vazia. Usando sprites de idle como fallback.")
                if Arvore_Maldita.sprites_idle_arvore_carregados and len(Arvore_Maldita.sprites_idle_arvore_carregados) > 0:
                    Arvore_Maldita.sprites_ataque_principal_arvore_carregados = list(Arvore_Maldita.sprites_idle_arvore_carregados)
                else:
                    print(f"AVISO (Arvore_Maldita): Sprites de idle também vazios. Criando placeholder para ataque principal.")
                    placeholder_ataque = pygame.Surface(Arvore_Maldita.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder_ataque.fill((40,20,5, 180))
                    Arvore_Maldita.sprites_ataque_principal_arvore_carregados = [placeholder_ataque]
            else:
                Arvore_Maldita._carregar_lista_sprites_estatico(caminhos_ataque_principal, Arvore_Maldita.sprites_ataque_principal_arvore_carregados, Arvore_Maldita.tamanho_sprite_definido, "ArvoreMaldita_AtaquePrincipal")

        if not Arvore_Maldita.sons_carregados:
            # Exemplo de como carregar sons (os caminhos devem existir)
            # Arvore_Maldita.som_ataque_arvore = Arvore_Maldita._carregar_som_arvore_maldita("Sons/Chefes/Arvore_Maldita/ataque_principal.wav")
            # Arvore_Maldita.som_dano_arvore = Arvore_Maldita._carregar_som_arvore_maldita("Sons/Chefes/Arvore_Maldita/dano.wav")
            # Arvore_Maldita.som_morte_arvore = Arvore_Maldita._carregar_som_arvore_maldita("Sons/Chefes/Arvore_Maldita/morte.wav")
            # print("DEBUG (Arvore_Maldita): Tentativa de carregar sons concluída.")
            Arvore_Maldita.sons_carregados = True

    def __init__(self, x, y, velocidade=0.3):
        Arvore_Maldita.carregar_recursos_arvore_maldita()
        vida_arvore = 1000
        dano_contato_arvore = 25
        xp_arvore = 1000
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Arvore Maldita/Arvore Maldita1.png"
        super().__init__(
            x, y,
            Arvore_Maldita.tamanho_sprite_definido[0], Arvore_Maldita.tamanho_sprite_definido[1],
            vida_arvore, velocidade, dano_contato_arvore,
            xp_arvore, sprite_path_principal_relativo_jogo
        )
        self.x = float(x)
        self.y = float(y)
        self.sprites_idle = Arvore_Maldita.sprites_idle_arvore_carregados
        self.sprites_ataque_principal = Arvore_Maldita.sprites_ataque_principal_arvore_carregados
        self.sprites = self.sprites_idle
        if self.sprites_idle and len(self.sprites_idle) > 0 and isinstance(self.sprites_idle[0], pygame.Surface):
            self.image = self.sprites_idle[0].copy()
        elif not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            print(f"AVISO (Arvore_Maldita instance): Sprites de idle não disponíveis ou imagem base não definida. Usando placeholder para instância.")
            placeholder_img = pygame.Surface(Arvore_Maldita.tamanho_sprite_definido, pygame.SRCALPHA)
            placeholder_img.fill((40, 20, 5, 150))
            self.image = placeholder_img
            if not self.sprites: self.sprites = [self.image]
        if hasattr(self, 'image') and self.image is not None:
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            self.rect = pygame.Rect(self.x, self.y, Arvore_Maldita.tamanho_sprite_definido[0], Arvore_Maldita.tamanho_sprite_definido[1])
            if not hasattr(self, 'image') or self.image is None:
                 self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                 self.image.fill((30,15,3,100))
        self.sprite_index = 0
        self.intervalo_animacao_idle = 450
        self.intervalo_animacao_ataque_principal = 150
        self.intervalo_animacao = self.intervalo_animacao_idle
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
        self.is_attacking_principal = False
        self.attack_principal_duration = 1.8
        self.attack_principal_timer = 0.0
        self.attack_principal_damage = 50
        self.attack_principal_range = Arvore_Maldita.tamanho_sprite_definido[0] * 0.8
        self.attack_principal_cooldown = 4.0
        self.last_attack_principal_time = pygame.time.get_ticks() - int(self.attack_principal_cooldown * 1000 * 0.75)
        self.attack_principal_hitbox_size = (Arvore_Maldita.tamanho_sprite_definido[0] * 0.7, Arvore_Maldita.tamanho_sprite_definido[1] * 0.6)
        self.attack_principal_hitbox_offset_y = -Arvore_Maldita.tamanho_sprite_definido[1] * 0.1
        self.attack_principal_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_swing = False
        self.xp_value_boss = xp_arvore

        # --- SCORE: Flag para conceder XP apenas uma vez ---
        self.xp_concedido = False

    def _atualizar_hitbox_ataque_principal(self):
        if not self.is_attacking_principal:
            self.attack_principal_hitbox.size = (0,0)
            return
        w, h = self.attack_principal_hitbox_size
        self.attack_principal_hitbox.size = (w,h)
        if self.facing_right:
            self.attack_principal_hitbox.left = self.rect.centerx
        else:
            self.attack_principal_hitbox.right = self.rect.centerx
        self.attack_principal_hitbox.centery = self.rect.centery + self.attack_principal_hitbox_offset_y

    def iniciar_ataque_principal(self, player):
        if not (hasattr(player, 'rect') and self.esta_vivo()): return
        agora = pygame.time.get_ticks()
        distancia_ao_jogador = float('inf')
        if hasattr(player, 'rect') and player.rect is not None:
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
        if not self.is_attacking_principal and \
           distancia_ao_jogador <= self.attack_principal_range and \
           (agora - self.last_attack_principal_time >= self.attack_principal_cooldown * 1000):
            self.is_attacking_principal = True
            self.attack_principal_timer = agora
            self.last_attack_principal_time = agora
            self.hit_player_this_attack_swing = False
            self.sprites = self.sprites_ataque_principal
            self.intervalo_animacao = self.intervalo_animacao_ataque_principal
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = agora
            if Arvore_Maldita.som_ataque_arvore: Arvore_Maldita.som_ataque_arvore.play()

    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        # --- SCORE: Concede XP ao jogador ao morrer, apenas uma vez ---
        if not self.esta_vivo():
            if not self.xp_concedido:
                if hasattr(self, "xp_value"):
                    score_manager.adicionar_xp(self.xp_value)
                    print(f"DEBUG(Arvore_Maldita): Jogador recebeu {self.xp_value} de XP. Score atual: {score_manager.get_score()}")
                self.xp_concedido = True
            return

        agora = pygame.time.get_ticks()
        if dt_ms is None:
            dt_ms = agora - getattr(self, '_last_update_time', agora)
            self._last_update_time = agora
            if dt_ms <= 0 : dt_ms = 16

        jogador_valido = (player is not None and 
                          hasattr(player, 'rect') and player.rect is not None and 
                          hasattr(player, 'receber_dano'))

        if jogador_valido:
            if player.rect.centerx < self.rect.centerx: self.facing_right = False
            else: self.facing_right = True

        if self.is_attacking_principal:
            self._atualizar_hitbox_ataque_principal()
            if jogador_valido and not self.hit_player_this_attack_swing and \
               self.attack_principal_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_principal_damage, self.rect)
                self.hit_player_this_attack_swing = True
            if agora - self.attack_principal_timer >= self.attack_principal_duration * 1000:
                self.is_attacking_principal = False
                self.sprites = self.sprites_idle
                self.intervalo_animacao = self.intervalo_animacao_idle
                self.sprite_index = 0
                self.tempo_ultimo_update_animacao = agora
                self.attack_principal_hitbox.size = (0,0)
        else:
            if jogador_valido: self.iniciar_ataque_principal(player)
            if not self.is_attacking_principal and self.velocidade > 0:
                if jogador_valido:
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
        super().update(player, outros_inimigos, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

    def receber_dano(self, dano, fonte_dano_rect=None):
        if not self.esta_vivo(): return
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if self.esta_vivo():
            if vida_antes > self.hp:
                if Arvore_Maldita.som_dano_arvore: Arvore_Maldita.som_dano_arvore.play()
                self.last_hit_time = pygame.time.get_ticks()
        elif vida_antes > 0:
            if Arvore_Maldita.som_morte_arvore: Arvore_Maldita.som_morte_arvore.play()

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y)
        # DEBUG: Desenha a hitbox de ataque (descomente para visualizar)
        # if self.is_attacking_principal and self.attack_principal_hitbox.width > 0:
        #     debug_rect_onscreen = self.attack_principal_hitbox.move(-camera_x, -camera_y)
        #     temp_surface = pygame.Surface(debug_rect_onscreen.size, pygame.SRCALPHA)
        #     temp_surface.fill((0, 255, 0, 100))
        #     surface.blit(temp_surface, debug_rect_onscreen.topleft)
        #     pygame.draw.rect(surface, (0, 255, 0), debug_rect_onscreen, 2)

# O restante do código (main/teste) permanece igual...