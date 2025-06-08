# Jogo/Arquivos/Inimigos/BonecoDeNeve.py
import pygame
import os
import math
import time 

try:
    from .Inimigos import Inimigo as InimigoBase
except ImportError:
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((180, 200, 230, 100)) 
            pygame.draw.rect(self.image, (200,220,255), self.image.get_rect(), 1)
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0

        def receber_dano(self, dano, fonte_dano_rect=None):
             self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt=None): pass
        def atualizar_animacao(self):
            if self.sprites and len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
        def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self):
            super().kill()

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
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", os.sep))
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

    def __init__(self, x, y, velocidade=1.2):
        BonecoDeNeve.carregar_recursos()

        vida_boneco = 70
        dano_contato_boneco = 7
        xp_boneco = 30
        self.moedas_drop = 10
        sprite_path_principal_relativo_ao_jogo = "Sprites/Inimigos/Boneco de Neve/Boneco De Neve 1.png"

        super().__init__(
            x, y,
            BonecoDeNeve.tamanho_sprite_definido[0], BonecoDeNeve.tamanho_sprite_definido[1],
            vida_boneco, velocidade, dano_contato_boneco, xp_boneco,
            sprite_path_principal_relativo_ao_jogo
        )

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
        self.velocidade_projetil = 6
        self.attack_prepare_duration = 500
        self.is_preparing_attack = False
        self.attack_prepare_start_time = 0

    def update(self, player, projeteis_inimigos_ref, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            return

        agora = pygame.time.get_ticks()
        distancia_ao_jogador = float('inf')

        jogador_valido = (hasattr(player, 'rect') and
                          hasattr(player, 'vida') and
                          hasattr(player.vida, 'esta_vivo') and
                          player.vida.esta_vivo())

        if jogador_valido:
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                             self.rect.centery - player.rect.centery)

        if self.is_preparing_attack:
            if agora - self.attack_prepare_start_time >= self.attack_prepare_duration:
                if jogador_valido and ProjetilNeve is not None:
                    novo_projetil = ProjetilNeve(
                        self.rect.centerx, self.rect.centery,
                        player.rect.centerx, player.rect.centery,
                        self.attack_damage, self.velocidade_projetil
                    )
                    # CORREÇÃO CRÍTICA: Adiciona o projétil ao grupo de projéteis dos inimigos.
                    if projeteis_inimigos_ref is not None:
                        projeteis_inimigos_ref.add(novo_projetil)
                self.is_preparing_attack = False
                self.last_attack_time = agora

        elif jogador_valido and distancia_ao_jogador <= self.attack_range and \
             (agora - self.last_attack_time >= self.attack_cooldown * 1000):
            self.is_preparing_attack = True
            self.attack_prepare_start_time = agora

        if not self.is_preparing_attack and jogador_valido:
            self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)

        self.atualizar_animacao()

        if jogador_valido and self.rect.colliderect(player.rect) and \
           (agora - self.last_contact_time >= self.contact_cooldown):
            if hasattr(player, 'receber_dano'):
                player.receber_dano(self.contact_damage)
                self.last_contact_time = agora


if ProjetilNeve is None:
    class ProjetilNeve(pygame.sprite.Sprite):
        def __init__(self, x_origem, y_origem, x_alvo, y_alvo, dano, velocidade=5, tamanho=10, cor=(200, 200, 255)):
            super().__init__()
            self.image = pygame.Surface((tamanho*2,tamanho*2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, cor, (tamanho, tamanho), tamanho)
            self.rect = self.image.get_rect(center=(x_origem,y_origem))
            self.dano = dano

            dx = x_alvo - x_origem
            dy = y_alvo - y_origem
            dist = math.hypot(dx,dy)

            if dist > 0:
                self.vel_x = (dx/dist) * velocidade
                self.vel_y = (dy/dist) * velocidade
            else:
                self.vel_x = 0
                self.vel_y = -velocidade

            self.alive = True

        def update(self, player, tela_largura, tela_altura, dt_ms=None):
            if not self.alive:
                return

            fator_tempo = 1.0
            if dt_ms is not None and dt_ms > 0:
                fator_tempo = (dt_ms / (1000.0 / 60.0))

            self.rect.x += self.vel_x * fator_tempo
            self.rect.y += self.vel_y * fator_tempo

            if hasattr(player, 'rect') and hasattr(player, 'vida') and \
               hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
               self.rect.colliderect(player.rect):
                if hasattr(player, 'receber_dano'):
                    player.receber_dano(self.dano)
                self.kill()
                self.alive = False
                return

            margem_tela = 100
            if not (-margem_tela < self.rect.centerx < tela_largura + margem_tela and \
                    -margem_tela < self.rect.centery < tela_altura + margem_tela):
                self.kill()
                self.alive = False

        def desenhar(self, surface, camera_x, camera_y):
            if self.alive:
                surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))