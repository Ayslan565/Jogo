# Demonio.py
import pygame
import random
import math
import time
import os

# Removido: importação do score_manager, pois a lógica de recompensa é tratada pelo GerenciadorDeInimigos

# --- Importação da Classe Base Inimigo ---
try:
    # Correção: Importação relativa para a classe base Inimigo dentro do mesmo pacote 'Inimigos'
    from .Inimigos import Inimigo as InimigoBase
    # print(f"DEBUG(Demonio): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Demonio): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    class InimigoBase(pygame.sprite.Sprite): # Placeholder
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((255, 0, 255, 100))
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value; self.facing_right = True
            self.last_hit_time = 0; self.hit_flash_duration = 150; self.contact_cooldown = 1000
            self.last_contact_time = pygame.time.get_ticks() - self.contact_cooldown
            self.sprites = [self.image.copy()]; self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks(); self.intervalo_animacao = 200
            self.moedas_drop = 0 # Adicionado para compatibilidade, mesmo que a lógica seja externa

        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None): pass
        def atualizar_animacao(self): pass
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            # Placeholder de update, a lógica real estará nas classes filhas
            pass
        def desenhar(self, janela, camera_x, camera_y):
            if hasattr(self, 'image') and self.image:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        def kill(self): super().kill()


class Demonio(InimigoBase):
    sprites_originais = None
    tamanho_sprite_definido = (96, 96)
    som_ataque_demonio, som_dano_demonio, som_morte_demonio, som_spawn_demonio = None, None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))

    @staticmethod
    def _carregar_som_demonio(caminho_relativo):
        caminho_completo = os.path.join(Demonio._obter_pasta_raiz_jogo(), caminho_relativo.replace("/", os.sep))
        if not os.path.exists(caminho_completo): return None
        try: return pygame.mixer.Sound(caminho_completo)
        except pygame.error: return None

    @staticmethod
    def carregar_recursos_demonio():
        if Demonio.sprites_originais is None:
            Demonio.sprites_originais = []
            base_sprite_path = "Sprites/Inimigos/Demonio/"
            nomes_sprites = [
                "20250521_1111_Demônio Pixel Art_simple_compose_01jvsjxvc7f8ca6npqkjaftsrv (1).png",
                "Demonio_Sprite_2.png", "Demonio_Sprite_3.png", "Demonio_Sprite_4.png"
            ]
            pasta_raiz = Demonio._obter_pasta_raiz_jogo()
            for nome in nomes_sprites:
                caminho_completo = os.path.join(pasta_raiz, base_sprite_path, nome)
                try:
                    if os.path.exists(caminho_completo):
                        sprite_img = pygame.image.load(caminho_completo).convert_alpha()
                        sprite_scaled = pygame.transform.scale(sprite_img, Demonio.tamanho_sprite_definido)
                        Demonio.sprites_originais.append(sprite_scaled)
                    else:
                        placeholder = pygame.Surface(Demonio.tamanho_sprite_definido, pygame.SRCALPHA); placeholder.fill((200, 0, 0)); Demonio.sprites_originais.append(placeholder)
                except pygame.error:
                    placeholder = pygame.Surface(Demonio.tamanho_sprite_definido, pygame.SRCALPHA); placeholder.fill((200, 0, 0)); Demonio.sprites_originais.append(placeholder)
            if not Demonio.sprites_originais:
                placeholder = pygame.Surface(Demonio.tamanho_sprite_definido, pygame.SRCALPHA); placeholder.fill((150, 0, 0)); Demonio.sprites_originais.append(placeholder)

        if not Demonio.sons_carregados:
            # Carregar sons aqui...
            Demonio.sons_carregados = True

    def __init__(self, x, y, velocidade=2.5):
        Demonio.carregar_recursos_demonio()

        demonio_hp = 90
        demonio_contact_damage = 10
        demonio_xp_value = 75
        self.moedas_drop = 12

        sprite_path_ref = "Sprites/Inimigos/Demonio/placeholder.png"
        if Demonio.sprites_originais:
            # Apenas uma referência, não usado para carregar a imagem principal aqui
            sprite_path_ref = "Sprites/Inimigos/Demonio/Demonio_Sprite_1.png"

        super().__init__(x, y,
                         Demonio.tamanho_sprite_definido[0], Demonio.tamanho_sprite_definido[1],
                         demonio_hp, velocidade, demonio_contact_damage,
                         demonio_xp_value, sprite_path_ref)

        # Removido: Flag self.recursos_concedidos, pois a lógica de recompensa é externa

        self.sprites = Demonio.sprites_originais
        self.sprite_index = 0
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
        self.intervalo_animacao = 120

        self.is_attacking = False
        self.attack_duration = 0.6
        self.attack_timer = 0.0
        self.attack_damage = 20
        self.attack_hitbox_size = (70, 70)
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.attack_range = 120
        self.attack_cooldown = 2.5
        self.last_attack_time = time.time() - self.attack_cooldown
        self.hit_player_this_attack = False # Renomeado para clareza

        if self.sprites: self.image = self.sprites[0]
        else: self.image = pygame.Surface(self.tamanho_sprite_definido, pygame.SRCALPHA); self.image.fill((200,0,0))
        
        self.rect = self.image.get_rect(topleft=(x, y))

    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        # ... (lógica de som)

    def atacar(self, player):
        if not hasattr(player, 'rect'): return
        current_time = time.time()
        if self.esta_vivo() and not self.is_attacking and (current_time - self.last_attack_time >= self.attack_cooldown):
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
            if distancia_ao_jogador <= self.attack_range:
                self.is_attacking = True
                self.attack_timer = current_time
                self.last_attack_time = current_time
                self.hit_player_this_attack = False
                self.attack_hitbox = pygame.Rect(0, 0, *self.attack_hitbox_size)
                self.attack_hitbox.center = self.rect.center
                # ... (lógica de som)

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        # Lógica de recompensa ao morrer foi movida para GerenciadorDeInimigos.py
        if not self.esta_vivo():
            self.kill() # O GerenciadorDeInimigos.py cuidará das recompensas e remoção
            return

        jogador_valido = (player and hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo'))
        if not jogador_valido:
            if hasattr(self, 'atualizar_animacao'): self.atualizar_animacao()
            return
        
        # Chama o update da classe base para movimento e animação
        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)

        if self.is_attacking:
            self.attack_hitbox.center = self.rect.center
            if time.time() - self.attack_timer >= self.attack_duration:
                self.is_attacking = False
                self.hit_player_this_attack = False
            elif not self.hit_player_this_attack and self.attack_hitbox.colliderect(player.rect):
                if player.vida.esta_vivo() and hasattr(player, 'receber_dano'):
                    player.receber_dano(self.attack_damage, self.rect)
                    self.hit_player_this_attack = True
        else:
            self.atacar(player)
            
    def desenhar(self, surface, camera_x, camera_y):
        # O método da classe base agora cuida de tudo (imagem, flash, barra de vida)
        super().desenhar(surface, camera_x, camera_y)
