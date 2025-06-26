# BonecoDeNeve.py
import pygame
import os
import math
import time # Usado para cooldowns de ataque

# --- Importação da Classe Base Inimigo ---
try:
    # Correção: Importação relativa para a classe base Inimigo dentro do mesmo pacote 'Inimigos'
    from .Inimigos import Inimigo as InimigoBase
except ImportError as e:
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((128, 128, 128, 100)) # Placeholder cinza
            pygame.draw.rect(self.image, (255,0,0), self.image.get_rect(), 1) # Borda vermelha
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            self.moedas_drop = 0
            self.x = float(x)
            self.y = float(y)

        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt=None): pass
        def atualizar_animacao(self): pass
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            pass
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self): super().kill()


# --- Importação do Projétil ---
ProjetilNeve = None
try:
    from .Projetil_BolaNeve import ProjetilNeve as ProjetilNeveReal
    ProjetilNeve = ProjetilNeveReal
except ImportError:
    pass
except Exception:
    pass


class BonecoDeNeve(InimigoBase):
    sprites_animacao = None
    tamanho_sprite_definido = (70, 90)

    @staticmethod
    def carregar_recursos():
        if BonecoDeNeve.sprites_animacao is not None:
            return

        BonecoDeNeve.sprites_animacao = []
        caminhos_relativos_sprites = [
            "Sprites/Inimigos/Boneco de Neve/Boneco De Neve 1.png",
            "Sprites/Inimigos/Boneco de Neve/Boneco de Neve 2.png",
            "Sprites/Inimigos/Boneco de Neve/Boneco de Neve 3.png",
        ]
        diretorio_script_boneco = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_boneco, "..", ".."))

        for path_relativo in caminhos_relativos_sprites:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, BonecoDeNeve.tamanho_sprite_definido)
                    BonecoDeNeve.sprites_animacao.append(sprite)
                else:
                    placeholder = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder.fill((50, 50, 200, 180))
                    BonecoDeNeve.sprites_animacao.append(placeholder)
            except pygame.error:
                placeholder = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder.fill((50, 50, 200, 180))
                BonecoDeNeve.sprites_animacao.append(placeholder)

        if not BonecoDeNeve.sprites_animacao:
            placeholder = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA)
            placeholder.fill((0, 0, 150, 200))
            BonecoDeNeve.sprites_animacao.append(placeholder)

    def __init__(self, x, y, velocidade=60):
        BonecoDeNeve.carregar_recursos()

        vida_boneco = 40
        dano_contato_boneco = 7
        xp_boneco = 30
        self.moedas_drop = 1500

        sprite_path_principal_relativo_ao_jogo = "Sprites/Inimigos/Boneco de Neve/Boneco De Neve 1.png"

        super().__init__(
            x, y,
            BonecoDeNeve.tamanho_sprite_definido[0], BonecoDeNeve.tamanho_sprite_definido[1],
            vida_boneco, velocidade, dano_contato_boneco, xp_boneco,
            sprite_path_principal_relativo_ao_jogo
        )
        
        self.x = float(x)
        self.y = float(y)
        
        self.sprites = BonecoDeNeve.sprites_animacao
        if not self.sprites or not isinstance(self.sprites[0], pygame.Surface):
            if hasattr(self, 'image') and isinstance(self.image, pygame.Surface):
                   self.sprites = [self.image]
            else:
                   placeholder_img = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA)
                   placeholder_img.fill((100,0,0,100))
                   self.image = placeholder_img
                   self.sprites = [self.image]


        self.sprite_index = 0
        self.intervalo_animacao = 250
        self.attack_damage = 12
        self.attack_range = 350
        self.attack_cooldown = 2.5
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)
        self.velocidade_projetil = 250 
        self.attack_prepare_duration = 500
        self.is_preparing_attack = False
        self.attack_prepare_start_time = 0

    def mover_em_direcao(self, ax, ay, dt_ms):
        if dt_ms is None or dt_ms <= 0:
            return
            
        direcao_x = ax - self.x
        direcao_y = ay - self.y
        distancia = math.hypot(direcao_x, direcao_y)

        if distancia > 0:
            direcao_x /= distancia
            direcao_y /= distancia
            
            fator_tempo = dt_ms / 1000.0
            movimento_x = direcao_x * self.velocidade * fator_tempo
            movimento_y = direcao_y * self.velocidade * fator_tempo
            
            self.x += movimento_x
            self.y += movimento_y
            self.rect.center = (int(self.x), int(self.y))

    def update(self, player, projeteis_inimigos_ref, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            self.kill()
            return

        agora = pygame.time.get_ticks()
        distancia_ao_jogador = float('inf')

        jogador_valido = (player and hasattr(player, 'esta_vivo') and player.esta_vivo())

        if jogador_valido:
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                              self.rect.centery - player.rect.centery)

        if self.is_preparing_attack:
            if agora - self.attack_prepare_start_time >= self.attack_prepare_duration:
                if jogador_valido and ProjetilNeve is not None:
                    novo_projetil = ProjetilNeve(
                        x_origem=self.rect.centerx, 
                        y_origem=self.rect.centery,
                        x_alvo=player.rect.centerx,
                        y_alvo=player.rect.centery,
                        dano=self.attack_damage, 
                        velocidade=self.velocidade_projetil
                    )
                    if hasattr(projeteis_inimigos_ref, 'add'):
                        projeteis_inimigos_ref.add(novo_projetil)

                self.is_preparing_attack = False
                self.last_attack_time = agora

        elif jogador_valido and distancia_ao_jogador <= self.attack_range and \
             (agora - self.last_attack_time >= self.attack_cooldown * 1000):
            self.is_preparing_attack = True
            self.attack_prepare_start_time = agora

        # --- LÓGICA DE MOVIMENTO CORRIGIDA ---
        if not self.is_preparing_attack and jogador_valido:
            # Se estiver muito perto, foge do jogador
            if distancia_ao_jogador < 150:
                # Calcula o vetor de fuga (direção oposta ao jogador)
                fuga_x = self.rect.centerx - player.rect.centerx
                fuga_y = self.rect.centery - player.rect.centery
                # Move na direção de fuga
                self.mover_em_direcao(self.rect.centerx + fuga_x, self.rect.centery + fuga_y, dt_ms)
            # Se estiver longe, se aproxima
            elif distancia_ao_jogador > self.attack_range:
                 self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)

        if hasattr(self, 'atualizar_animacao'):
            self.atualizar_animacao()

if ProjetilNeve is None:
    pass
