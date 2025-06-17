# Planta_Carnivora.py
import pygame
import os
import math
import time
import random

# Removido: importação do score_manager, pois a lógica de recompensa é tratada pelo GerenciadorDeInimigos

# --- Importação da Classe Base Inimigo ---
try:
    # Correção: Importação relativa para a classe base Inimigo dentro do mesmo pacote 'Inimigos'
    from .Inimigos import Inimigo as InimigoBase
    # print(f"DEBUG(Planta_Carnivora): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Planta_Carnivora): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((10, 120, 30, 100))
            pygame.draw.rect(self.image, (50,150,50), self.image.get_rect(), 1)
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
            img = pygame.Surface(tamanho, pygame.SRCALPHA); img.fill((40,150,60, 128)); return img
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


class Planta_Carnivora(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (60, 60)
    som_ataque_planta, som_dano_planta, som_morte_planta = None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho, nome_anim):
        pasta_raiz = Planta_Carnivora._obter_pasta_raiz_jogo()
        if lista_destino is None: lista_destino = [] # Garante que lista_destino é uma lista
        for path_relativo in caminhos:
            caminho_completo = os.path.join(pasta_raiz, path_relativo.replace("\\", "/"))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                else:
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((20, 100, 20, 180)); lista_destino.append(placeholder)
            except pygame.error:
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((20, 100, 20, 180)); lista_destino.append(placeholder)
        if not lista_destino:
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((10, 70, 10, 200)); lista_destino.append(placeholder)
        return lista_destino # Retorna a lista modificada

    @staticmethod
    def carregar_recursos_planta_carnivora():
        if Planta_Carnivora.sprites_andar_carregados is None:
            caminhos_andar = ["Sprites/Inimigos/Planta Carnivora/Planta carnivora 1.png", "Sprites/Inimigos/Planta Carnivora/Planta_Carnivora2.png"]
            Planta_Carnivora.sprites_andar_carregados = []
            Planta_Carnivora._carregar_lista_sprites_estatico(caminhos_andar, Planta_Carnivora.sprites_andar_carregados, Planta_Carnivora.tamanho_sprite_definido, "Andar/Idle")
        if Planta_Carnivora.sprites_atacar_carregados is None:
            caminhos_atacar = ["Sprites/Inimigos/Planta Carnivora/Planta carnivora 1.png", "Sprites/Inimigos/Planta Carnivora/Planta_Carnivora2.png"] # Se os sprites de ataque são os mesmos do andar
            Planta_Carnivora.sprites_atacar_carregados = []
            Planta_Carnivora._carregar_lista_sprites_estatico(caminhos_atacar, Planta_Carnivora.sprites_atacar_carregados, Planta_Carnivora.tamanho_sprite_definido, "Atacar")
            if not Planta_Carnivora.sprites_atacar_carregados and Planta_Carnivora.sprites_andar_carregados: # Fallback se os sprites de ataque estiverem faltando
                Planta_Carnivora.sprites_atacar_carregados = [Planta_Carnivora.sprites_andar_carregados[0]]
        if not Planta_Carnivora.sons_carregados:
            # Carregar sons aqui
            Planta_Carnivora.sons_carregados = True

    def __init__(self, x, y, velocidade=0.5):
        Planta_Carnivora.carregar_recursos_planta_carnivora()

        vida_planta = 90
        dano_contato_planta = 8
        xp_planta = 50
        self.moedas_drop = 15
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Planta Carnivora/Planta carnivora 1.png"

        super().__init__(
            x, y,
            Planta_Carnivora.tamanho_sprite_definido[0], Planta_Carnivora.tamanho_sprite_definido[1],
            vida_planta, velocidade, dano_contato_planta,
            xp_planta, sprite_path_principal_relativo_jogo
        )
        
        # Removido: Flag self.recursos_concedidos, pois a lógica de recompensa é externa

        self.x = float(x)
        self.y = float(y)
        self.sprites_andar = Planta_Carnivora.sprites_andar_carregados
        self.sprites_atacar = Planta_Carnivora.sprites_atacar_carregados
        self.sprites = self.sprites_andar

        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            if self.sprites: self.image = self.sprites[0].copy()
            else:
                self.image = pygame.Surface(Planta_Carnivora.tamanho_sprite_definido, pygame.SRCALPHA); self.image.fill((10, 70, 10, 150))
                if not self.sprites: self.sprites = [self.image]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.sprite_index = 0
        self.intervalo_animacao_andar = 350
        self.intervalo_animacao_atacar = 250
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()

        self.is_attacking = False
        self.attack_duration = 0.8
        self.attack_timer = 0.0
        self.attack_damage_especifico = 20
        self.attack_range = 80
        self.attack_cooldown = 2.8
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)
        self.attack_hitbox_size = (Planta_Carnivora.tamanho_sprite_definido[0] * 0.7, Planta_Carnivora.tamanho_sprite_definido[1] * 0.5)
        self.attack_hitbox_offset_y = -Planta_Carnivora.tamanho_sprite_definido[1] * 0.2
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_player_this_attack_swing = False

    def _atualizar_hitbox_ataque(self):
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0); return
        w, h = self.attack_hitbox_size
        self.attack_hitbox.size = (w,h)
        if self.facing_right:
            self.attack_hitbox.left = self.rect.centerx
        else:
            self.attack_hitbox.right = self.rect.centerx
        self.attack_hitbox.centery = self.rect.centery + self.attack_hitbox_offset_y

    def atacar(self, player):
        if not (hasattr(player, 'rect') and self.esta_vivo()): return
        agora = pygame.time.get_ticks()
        distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
        if not self.is_attacking and distancia_ao_jogador <= self.attack_range and (agora - self.last_attack_time >= self.attack_cooldown * 1000):
            self.is_attacking = True
            self.attack_timer = agora
            self.last_attack_time = agora
            self.hit_player_this_attack_swing = False
            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = agora

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        # Lógica de recompensa ao morrer foi movida para GerenciadorDeInimigos.py
        if not self.esta_vivo():
            self.kill() # O GerenciadorDeInimigos.py cuidará das recompensas e remoção
            return

        agora = pygame.time.get_ticks()
        jogador_valido = (player and hasattr(player, 'rect') and hasattr(player, 'receber_dano'))

        if jogador_valido:
            if player.rect.centerx < self.rect.centerx: self.facing_right = False
            else: self.facing_right = True

        # Chama o update da classe base para movimento e animação
        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)

        if self.is_attacking:
            if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()
            self._atualizar_hitbox_ataque()
            if jogador_valido and not self.hit_player_this_attack_swing and self.attack_hitbox.colliderect(player.rect):
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
            if jogador_valido: self.atacar(player)
            # As chamadas a mover_em_direcao e atualizar_animacao são cobertas pela super().update()
            # que é chamada no início deste método update. Remover estas linhas duplicadas.
            # if not self.is_attacking and self.velocidade > 0:
            #     if jogador_valido and hasattr(self, 'mover_em_direcao'):
            #         self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
            # if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()

        if jogador_valido and self.rect.colliderect(player.rect) and (agora - self.last_contact_time >= self.contact_cooldown):
            player.receber_dano(self.contact_damage, self.rect)
            self.last_contact_time = agora

    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if not self.esta_vivo() and vida_antes > 0 and Planta_Carnivora.som_morte_planta:
            Planta_Carnivora.som_morte_planta.play()
        elif self.esta_vivo() and vida_antes > self.hp and Planta_Carnivora.som_dano_planta:
            Planta_Carnivora.som_dano_planta.play()

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y)
