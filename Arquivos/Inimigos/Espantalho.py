# Espantalho.py
import pygame
import os
import math
import time

# Removido: importação do score_manager, pois a lógica de recompensa é tratada pelo GerenciadorDeInimigos

# --- Importação da Classe Base Inimigo ---
try:
    # Correção: Importação relativa para a classe base Inimigo dentro do mesmo pacote 'Inimigos'
    from .Inimigos import Inimigo as InimigoBase
    # print(f"DEBUG(Espantalho): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Espantalho): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((100, 100, 100, 100))
            pygame.draw.rect(self.image, (255,165,0), self.image.get_rect(), 1)
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            self.moedas_drop = 0 # Adicionado para compatibilidade, mesmo que a lógica seja externa

        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt=None): pass
        def atualizar_animacao(self):
            if self.sprites: self.image = self.sprites[0]
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            # Placeholder de update, a lógica real estará nas classes filhas
            if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self): super().kill()


class Espantalho(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (120, 160)
    som_ataque_espantalho, som_dano_espantalho, som_morte_espantalho = None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_espantalho = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_espantalho, "..", ".."))

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho, nome_anim):
        pasta_raiz = Espantalho._obter_pasta_raiz_jogo()
        if lista_destino is None: lista_destino = []
        for path_relativo in caminhos:
            caminho_completo = os.path.join(pasta_raiz, path_relativo.replace("\\", "/"))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                else:
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((139, 69, 19, 180)); lista_destino.append(placeholder)
            except pygame.error:
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((139, 69, 19, 180)); lista_destino.append(placeholder)
        if not lista_destino:
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((100, 50, 10, 200)); lista_destino.append(placeholder)
        return lista_destino

    @staticmethod
    def carregar_recursos_espantalho():
        if Espantalho.sprites_andar_carregados is None:
            caminhos_andar = ["Sprites/Inimigos/Espantalho/Espantalho.png", "Sprites/Inimigos/Espantalho/Espantalho 2.png", "Sprites/Inimigos/Espantalho/Espantalho 3.png"]
            Espantalho.sprites_andar_carregados = Espantalho._carregar_lista_sprites_estatico(caminhos_andar, [], Espantalho.tamanho_sprite_definido, "Andar/Idle")
            if not Espantalho.sprites_atacar_carregados:
                Espantalho.sprites_atacar_carregados = [Espantalho.sprites_andar_carregados[0]]
        if not Espantalho.sons_carregados:
            # Carregar sons aqui
            Espantalho.sons_carregados = True

    def __init__(self, x, y, velocidade=1.3): 
        Espantalho.carregar_recursos_espantalho()

        vida_espantalho = 40 
        dano_contato_espantalho = 5 
        xp_espantalho = 20
        self.moedas_drop = 11

        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Espantalho/Espantalho.png" 

        super().__init__(
            x, y,
            Espantalho.tamanho_sprite_definido[0], Espantalho.tamanho_sprite_definido[1],
            vida_espantalho, velocidade, dano_contato_espantalho,
            xp_espantalho, sprite_path_principal_relativo_jogo
        )
        
        # Removido: Flag self.recursos_concedidos, pois a lógica de recompensa é externa

        self.sprites_andar = Espantalho.sprites_andar_carregados
        self.sprites_atacar = Espantalho.sprites_atacar_carregados
        self.sprites = self.sprites_andar
        
        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            if self.sprites: self.image = self.sprites[0]
            else:
                self.image = pygame.Surface(Espantalho.tamanho_sprite_definido, pygame.SRCALPHA); self.image.fill((100, 50, 10, 150))
                if not self.sprites: self.sprites = [self.image]

        self.rect = self.image.get_rect(topleft=(x, y))

        self.sprite_index = 0 
        self.intervalo_animacao_andar = 220 
        self.intervalo_animacao_atacar = 150 
        self.intervalo_animacao = self.intervalo_animacao_andar

        self.is_attacking = False 
        self.attack_duration = 0.6
        self.attack_timer = 0.0 
        self.attack_damage_especifico = 10
        self.attack_hitbox_size = (Espantalho.tamanho_sprite_definido[0] * 0.6, Espantalho.tamanho_sprite_definido[1] * 0.5)
        self.attack_hitbox_offset_x = Espantalho.tamanho_sprite_definido[0] * 0.4
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) 
        self.attack_range = 80
        self.attack_cooldown = 2.0
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000) 
        self.hit_player_this_swing = False

    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0)
            return
        w, h = self.attack_hitbox_size
        self.attack_hitbox.size = (w,h)
        if self.facing_right:
            self.attack_hitbox.midleft = (self.rect.right, self.rect.centery)
        else:
            self.attack_hitbox.midright = (self.rect.left, self.rect.centery)

    def atacar(self, player):
        if not (hasattr(player, 'rect') and self.esta_vivo()): return
        agora = pygame.time.get_ticks()
        distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
        if not self.is_attacking and distancia_ao_jogador <= self.attack_range and (agora - self.last_attack_time >= self.attack_cooldown * 1000):
            self.is_attacking = True
            self.attack_timer = agora
            self.last_attack_time = agora
            self.hit_player_this_swing = False
            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        # Lógica de recompensa ao morrer foi movida para GerenciadorDeInimigos.py
        if not self.esta_vivo():
            self.kill() # O GerenciadorDeInimigos.py cuidará das recompensas e remoção
            return

        agora = pygame.time.get_ticks()
        jogador_valido = (player and hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo'))

        # Chama o update da classe base para movimento e animação
        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)

        if self.is_attacking:
            if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()
            self._atualizar_hitbox_ataque()
            if jogador_valido and not self.hit_player_this_swing and self.attack_hitbox.colliderect(player.rect):
                if hasattr(player, 'receber_dano'): player.receber_dano(self.attack_damage_especifico)
                self.hit_player_this_swing = True
            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_andar
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.sprite_index = 0
                self.attack_hitbox.size = (0,0)
        else:
            if jogador_valido: self.atacar(player)
            # A chamada super().update já cuida do mover_em_direcao e atualizar_animacao para o estado normal.
            # Verifique se a linha abaixo ainda é necessária após a chamada a super().update
            # if not self.is_attacking and jogador_valido and hasattr(self, 'mover_em_direcao'):
            #     self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
            # if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao() # Já chamado na super.update

        # Lógica de dano de contato com o jogador (movida aqui para não ser afetada pelo estado de ataque direto)
        if jogador_valido and self.rect.colliderect(player.rect) and (agora - self.last_contact_time >= self.contact_cooldown):
            if hasattr(player, 'receber_dano'): player.receber_dano(self.contact_damage)
            self.last_contact_time = agora
