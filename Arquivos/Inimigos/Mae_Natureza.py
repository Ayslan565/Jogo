# Mae_Natureza.py
import pygame
import os
import math
import time

# Removido: importação do score_manager, pois a lógica de recompensa é tratada pelo GerenciadorDeInimigos

# --- Importação da Classe Base Inimigo ---
try:
    # Correção: Importação relativa para a classe base Inimigo dentro do mesmo pacote 'Inimigos'
    from .Inimigos import Inimigo as InimigoBase
    # print(f"DEBUG(Mae_Natureza): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Mae_Natureza): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((34, 139, 34, 100))
            pygame.draw.rect(self.image, (0,100,0), self.image.get_rect(), 1)
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            self.x = float(x); self.y = float(y)
            self.moedas_drop = 0 # Adicionado para compatibilidade, mesmo que a lógica seja externa

        def _carregar_sprite(self, path, tamanho):
            img = pygame.Surface(tamanho, pygame.SRCALPHA); img.fill((34, 139, 34, 128)); return img
        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt_ms=None): pass
        def atualizar_animacao(self):
            if self.sprites: self.image = self.sprites[0]
        # Padronizado a assinatura do update do placeholder para consistência
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            # Placeholder de update, a lógica real estará nas classes filhas
            self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self): super().kill()


class Mae_Natureza(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (160, 180)

    som_ataque_mae, som_dano_mae, som_morte_mae = None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))

    @staticmethod
    def _carregar_som_mae_natureza(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Mae_Natureza._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))
        if not os.path.exists(caminho_completo): return None
        try: return pygame.mixer.Sound(caminho_completo)
        except pygame.error: return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho, nome_anim):
        pasta_raiz_jogo = Mae_Natureza._obter_pasta_raiz_jogo()
        if lista_destino is None: lista_destino = [] # Garante que lista_destino é uma lista
        for path_relativo in caminhos:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                else:
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((34, 139, 34, 180)); lista_destino.append(placeholder)
            except pygame.error:
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((34, 139, 34, 180)); lista_destino.append(placeholder)
        if not lista_destino:
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((20, 100, 20, 200)); lista_destino.append(placeholder)
        return lista_destino # Retorna a lista modificada

    @staticmethod
    def carregar_recursos_mae_natureza():
        if Mae_Natureza.sprites_andar_carregados is None:
            Mae_Natureza.sprites_andar_carregados = []
            caminhos = ["Sprites/Inimigos/Mae_Natureza/Mae{}.png".format(i) for i in range(1, 4)]
            Mae_Natureza._carregar_lista_sprites_estatico(caminhos, Mae_Natureza.sprites_andar_carregados, Mae_Natureza.tamanho_sprite_definido, "Andar/Idle")
        if Mae_Natureza.sprites_atacar_carregados is None:
            Mae_Natureza.sprites_atacar_carregados = []
            caminhos_atacar = ["Sprites/Inimigos/Mae_Natureza/Mae_Atacar{}.png".format(i) for i in range(1, 3)]
            Mae_Natureza._carregar_lista_sprites_estatico(caminhos_atacar, Mae_Natureza.sprites_atacar_carregados, Mae_Natureza.tamanho_sprite_definido, "Atacar")
            if not Mae_Natureza.sprites_atacar_carregados and Mae_Natureza.sprites_andar_carregados:
                Mae_Natureza.sprites_atacar_carregados = [Mae_Natureza.sprites_andar_carregados[0]]
        if not Mae_Natureza.sons_carregados:
            # Carregar sons aqui
            Mae_Natureza.sons_carregados = True

    def __init__(self, x, y, velocidade=0.7):
        Mae_Natureza.carregar_recursos_mae_natureza()

        vida_mae_natureza = 120
        dano_contato_mae_natureza = 12
        xp_mae_natureza = 120
        self.moedas_drop = 17

        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Mae_Natureza/Mae1.png"

        super().__init__(
            x, y,
            Mae_Natureza.tamanho_sprite_definido[0], Mae_Natureza.tamanho_sprite_definido[1],
            vida_mae_natureza, velocidade, dano_contato_mae_natureza,
            xp_mae_natureza, sprite_path_principal_relativo_jogo
        )

        # Removido: Flag self.recursos_concedidos, pois a lógica de recompensa é externa

        self.x = float(x)
        self.y = float(y)
        self.sprites_andar = Mae_Natureza.sprites_andar_carregados
        self.sprites_atacar = Mae_Natureza.sprites_atacar_carregados
        self.sprites = self.sprites_andar

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            if self.sprites: self.image = self.sprites[0]
            else:
                self.image = pygame.Surface(Mae_Natureza.tamanho_sprite_definido, pygame.SRCALPHA); self.image.fill((20, 100, 20, 150))
                if not self.sprites: self.sprites = [self.image]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.sprite_index = 0
        self.intervalo_animacao_andar = 300
        self.intervalo_animacao_atacar = 220
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.is_attacking = False
        self.attack_duration = 1.2
        self.attack_timer = 0.0
        self.attack_damage_especifico = 30
        self.attack_range = 180
        self.attack_cooldown = 4.5
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)
        self.attack_hitbox_size = (Mae_Natureza.tamanho_sprite_definido[0] * 1.5, Mae_Natureza.tamanho_sprite_definido[1] * 1.5)
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_pulse = False
        
    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0); return
        self.attack_hitbox.size = self.attack_hitbox_size
        self.attack_hitbox.center = self.rect.center

    def atacar(self, player):
        if not (hasattr(player, 'rect') and self.esta_vivo()): return
        agora = pygame.time.get_ticks()
        distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
        if not self.is_attacking and distancia_ao_jogador <= self.attack_range and (agora - self.last_attack_time >= self.attack_cooldown * 1000):
            self.is_attacking = True
            self.attack_timer = agora
            self.last_attack_time = agora
            self.hit_player_this_attack_pulse = False
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

        if jogador_valido:
            if player.rect.centerx < self.rect.centerx: self.facing_right = False
            else: self.facing_right = True

        # Chama o update da classe base para movimento e animação
        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)

        if self.is_attacking:
            if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()
            self._atualizar_hitbox_ataque()
            if jogador_valido and not self.hit_player_this_attack_pulse and self.attack_hitbox.colliderect(player.rect):
                if hasattr(player, 'receber_dano'): player.receber_dano(self.attack_damage_especifico)
                self.hit_player_this_attack_pulse = True
            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_andar
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.sprite_index = 0
                self.attack_hitbox.size = (0,0)
        else:
            if jogador_valido: self.atacar(player)
            # A chamada super().update já cuida do mover_em_direcao e atualizar_animacao para o estado normal.
            # Essas linhas foram comentadas porque a chamada super().update já as executa.
            # if not self.is_attacking and jogador_valido and hasattr(self, 'mover_em_direcao'):
            #     self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
            # if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao() # Já chamado na super.update

        if jogador_valido and self.rect.colliderect(player.rect) and (agora - self.last_contact_time >= self.contact_cooldown):
            if hasattr(player, 'receber_dano'): player.receber_dano(self.contact_damage, self.rect)
            self.last_contact_time = agora
            
    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if not self.esta_vivo() and vida_antes > 0 and self.som_morte_mae:
             self.som_morte_mae.play()
        elif self.esta_vivo() and vida_antes > self.hp and self.som_dano_mae:
             self.som_dano_mae.play()
