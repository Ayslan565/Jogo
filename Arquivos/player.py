# Jogo/Arquivos/player.py
import pygame
import random
import math
import os
import time
from importacoes_Player import *
from import_Loja import *

# Garante que o diretório de trabalho seja o do arquivo para consistência nos caminhos
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except Exception as e:
    print(f"AVISO: Não foi possível mudar o diretório de trabalho: {e}")

try:
    from Armas.EspadaBrasas import EspadaBrasas
except ImportError:
    EspadaBrasas = None

# Mapeamento de nomes de itens da loja para classes de Armas
SHOP_ITEM_TO_WEAPON_CLASS_MAP = {
    "Adaga do Fogo Contudente": AdagaFogo,
    "Espada de Fogo azul Sacra Cerulea": EspadaFogoAzul,
    "Espada do Olhar Da Penitencia": EspadaPenitencia,
    "Espada Sacra Caida": EspadaCaida,
    "Espada Sacra do Lua": EspadaLua,
    "Lâmina do Ceu Centilhante": LaminaDoCeuCentilhante,
    "Espada Sacra Das Brasas": EspadaSacraDasBrasas,
    "Machado Bárbaro Cravejado": MachadoBarbaro,
    "Machado Cerúleo da Estrela Cadente": MachadoCeruleo,
    "Machado da Descida Santa": MachadoDaDescidaSanta,
    "Machado do Fogo Abrasador": MachadoDoFogoAbrasador,
    "Machado do Marfim Resplendor": MachadoMarfim,
    "Machado Macabro da Gula Infinita": MachadoMacabro,
    "Cajado da Fixacao Ametista": CajadoDaFixacaoAmetista,
    "Cajado Da santa Natureza": CajadoDaSantaNatureza,
    "Livro dos impuros": LivroDosImpuros,
}

class Player(pygame.sprite.Sprite):
    """
    Classe que representa o jogador no jogo.
    Gerencia movimento, animações, vida, a arma equipada, e invencibilidade temporária.
    """
    def __init__(self, velocidade=5, vida_maxima=150):
        super().__init__()
        self.x = float(random.randint(100, 700))
        self.y = float(random.randint(100, 500))
        self.velocidade = float(velocidade)
        if self.velocidade <= 0: self.velocidade = 1.0

        if Vida is not None:
            self.vida = Vida(vida_maxima)
        else:
            self.vida = None
            print("ERRO CRÍTICO(Player): Classe Vida não disponível.")

        self.xp_manager = None
        self.dinheiro = 1000
        self.SHOP_ITEM_TO_WEAPON_CLASS = SHOP_ITEM_TO_WEAPON_CLASS_MAP

        tamanho_sprite_desejado = (60, 60)
        self.sprites_esquerda = self._carregar_sprites_diretorio("Asrahel/Esquerda", tamanho_sprite_desejado)
        self.sprites_idle_esquerda = self._carregar_sprites_diretorio("Asrahel/Esquerda", tamanho_sprite_desejado, single_frame=True)
        self.sprites_direita = self._carregar_sprites_diretorio("Asrahel/Direita", tamanho_sprite_desejado)
        self.sprites_idle_direita = self._carregar_sprites_diretorio("Asrahel/Direita", tamanho_sprite_desejado, single_frame=True)

        self.atual = 0
        self.frame_idle = 0
        self.parado = True
        self.direction = "right"

        self.image = self.sprites_idle_direita[0] if self.sprites_idle_direita else None
        if not self.image:
            self.image = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
            self.image.fill((255, 0, 255, 150))
            print("ALERTA(Player): Nenhum sprite carregado para o jogador. Usando placeholder.")

        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
        self.rect_colisao = self.rect.inflate(-30, -20)

        self.tempo_animacao = 100
        self.ultimo_update = pygame.time.get_ticks()

        self.current_weapon: Weapon | None = None
        self.tempo_ultimo_ataque = 0.0
        self.max_owned_weapons = 4
        self.owned_weapons: list[Weapon | None] = [None] * self.max_owned_weapons

        if 'AdagaFogo' in globals() and AdagaFogo is not None:
            try:
                arma_inicial = AdagaFogo()
                self.add_owned_weapon(arma_inicial)
                self.equip_weapon(arma_inicial)
            except Exception as e:
                print(f"ERRO(Player Init): Falha ao instanciar AdagaFogo: {e}")

        self.is_attacking = False
        self.is_attacking_animation_active = False
        self.attack_duration = 0.3
        self.attack_timer = 0.0
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.hit_enemies_this_attack = set()

        self.pode_levar_dano = True
        self.tempo_ultimo_dano_levado = 0
        self.duracao_invencibilidade_ms = 500
        self.is_invencivel_piscando = False
        self.tempo_para_proximo_pisca_dano = 0
        self.intervalo_pisca_dano_ms = 80
        self.visivel_durante_pisca_dano = True

    def _get_project_root(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def _carregar_sprites_diretorio(self, subpasta_relativa, tamanho, single_frame=False):
        sprites = []
        project_root = self._get_project_root()
        caminho_completo_dir = os.path.join(project_root, "Sprites", subpasta_relativa.replace("/", os.sep))

        if not os.path.isdir(caminho_completo_dir):
            print(f"ALERTA(Player): Diretório de sprites não encontrado: {caminho_completo_dir}")
            return [pygame.Surface(tamanho, pygame.SRCALPHA)]

        arquivos_imagem = sorted([f for f in os.listdir(caminho_completo_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        if single_frame and arquivos_imagem:
            arquivos_imagem = [arquivos_imagem[0]]

        for nome_arquivo in arquivos_imagem:
            caminho_arquivo = os.path.join(caminho_completo_dir, nome_arquivo)
            try:
                sprite = pygame.image.load(caminho_arquivo).convert_alpha()
                sprite = pygame.transform.scale(sprite, tamanho)
                sprites.append(sprite)
            except pygame.error as e:
                print(f"ERRO(Player): Falha ao carregar sprite '{caminho_arquivo}': {e}")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                placeholder.fill((255, 0, 255, 100))
                sprites.append(placeholder)

        if not sprites:
            print(f"ALERTA(Player): Nenhum sprite carregado de '{caminho_completo_dir}'.")
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            placeholder.fill((255, 0, 0, 150))
            sprites.append(placeholder)
        return sprites
    
    # ... (restante das propriedades como dano, alcance_ataque, etc.)

    @property
    def dano(self) -> float:
        return self.current_weapon.damage if self.current_weapon else 0.0

    @property
    def alcance_ataque(self) -> float:
        return self.current_weapon.attack_range if self.current_weapon else 0.0

    @property
    def cooldown_ataque(self) -> float:
        return self.current_weapon.cooldown if self.current_weapon else 0.5

    @property
    def level(self) -> int:
        return self.xp_manager.level if self.xp_manager and hasattr(self.xp_manager, 'level') else 1

    def equip_weapon(self, weapon_object: Weapon):
        if Weapon is None:
            return
        if isinstance(weapon_object, Weapon):
            self.current_weapon = weapon_object
            self.tempo_ultimo_ataque = time.time()
        else:
            print(f"ALERTA(Player.equip_weapon): Tentativa de equipar objeto inválido: {type(weapon_object)}.")

    def add_owned_weapon(self, weapon_object: Weapon) -> bool:
        if Weapon is None or not isinstance(weapon_object, Weapon):
            return False
        
        base_name_to_add = getattr(weapon_object, '_base_name', weapon_object.name)
        if any(hasattr(w, '_base_name') and w._base_name == base_name_to_add for w in self.owned_weapons if w):
            return False

        if None in self.owned_weapons:
            idx = self.owned_weapons.index(None)
            self.owned_weapons[idx] = weapon_object
            if not self.current_weapon:
                self.equip_weapon(weapon_object)
            return True
        return False

    def receber_dano(self, dano, _fonte_dano_rect=None):
        if self.vida and self.pode_levar_dano:
            self.vida.receber_dano(dano)
            self.pode_levar_dano = False
            self.tempo_ultimo_dano_levado = pygame.time.get_ticks()
            self.is_invencivel_piscando = True
            self.visivel_durante_pisca_dano = False
            self.tempo_para_proximo_pisca_dano = self.tempo_ultimo_dano_levado + self.intervalo_pisca_dano_ms

    def update(self, dt_ms=None, teclas_pressionadas=None):
        agora_ticks = pygame.time.get_ticks()
        agora_time = time.time()

        if self.is_invencivel_piscando:
            if agora_ticks >= self.tempo_para_proximo_pisca_dano:
                self.visivel_durante_pisca_dano = not self.visivel_durante_pisca_dano
                self.tempo_para_proximo_pisca_dano = agora_ticks + self.intervalo_pisca_dano_ms
            if agora_ticks - self.tempo_ultimo_dano_levado > self.duracao_invencibilidade_ms:
                self.pode_levar_dano = True
                self.is_invencivel_piscando = False
                self.visivel_durante_pisca_dano = True

        if self.is_attacking_animation_active and (agora_time - self.attack_timer >= self.attack_duration):
            self.is_attacking = False
            self.is_attacking_animation_active = False
            self.attack_hitbox.size = (0, 0)
            self.hit_enemies_this_attack.clear()
            if self.current_weapon and hasattr(self.current_weapon, 'current_attack_animation_frame'):
                self.current_weapon.current_attack_animation_frame = 0

        if agora_ticks - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora_ticks
            if self.parado:
                sprites_atuais = self.sprites_idle_direita if self.direction == "right" else self.sprites_idle_esquerda
                if sprites_atuais:
                    self.frame_idle = (self.frame_idle + 1) % len(sprites_atuais)
                    self.image = sprites_atuais[self.frame_idle]
            else:
                sprites_atuais = self.sprites_direita if self.direction == "right" else self.sprites_esquerda
                if sprites_atuais:
                    self.atual = (self.atual + 1) % len(sprites_atuais)
                    self.image = sprites_atuais[self.atual]
        
        if self.is_attacking_animation_active and self.current_weapon and hasattr(self.current_weapon, 'attack_animation_sprites') and self.current_weapon.attack_animation_sprites:
            if agora_ticks - self.current_weapon.last_attack_animation_update > self.current_weapon.attack_animation_speed:
                self.current_weapon.last_attack_animation_update = agora_ticks
                num_frames_arma = len(self.current_weapon.attack_animation_sprites)
                if num_frames_arma > 0:
                    self.current_weapon.current_attack_animation_frame = (self.current_weapon.current_attack_animation_frame + 1) % num_frames_arma
        
        self.rect.center = (round(self.x), round(self.y))
        if hasattr(self, 'rect_colisao'):
            self.rect_colisao.center = self.rect.center

    def mover(self, teclas, arvores):
        if not hasattr(self, 'rect_colisao'): return

        dx, dy = 0.0, 0.0
        move_left = teclas[pygame.K_LEFT] or teclas[pygame.K_a]
        move_right = teclas[pygame.K_RIGHT] or teclas[pygame.K_d]
        move_up = teclas[pygame.K_UP] or teclas[pygame.K_w]
        move_down = teclas[pygame.K_DOWN] or teclas[pygame.K_s]

        if move_left != move_right:
            dx = -self.velocidade if move_left else self.velocidade
            self.direction = "left" if move_left else "right"
        if move_up != move_down:
            dy = -self.velocidade if move_up else self.velocidade
        
        self.parado = not (dx or dy)

        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071
        
        self.x += dx
        self.rect_colisao.centerx = round(self.x)
        if arvores and dx:
            for arvore in arvores:
                arvore_col_rect = getattr(arvore, 'rect_colisao', arvore.rect)
                if arvore_col_rect and self.rect_colisao.colliderect(arvore_col_rect):
                    if dx > 0: self.rect_colisao.right = arvore_col_rect.left
                    else: self.rect_colisao.left = arvore_col_rect.right
                    self.x = float(self.rect_colisao.centerx)
                    break
        
        self.y += dy
        self.rect_colisao.centery = round(self.y)
        if arvores and dy:
            for arvore in arvores:
                arvore_col_rect = getattr(arvore, 'rect_colisao', arvore.rect)
                if arvore_col_rect and self.rect_colisao.colliderect(arvore_col_rect):
                    if dy > 0: self.rect_colisao.bottom = arvore_col_rect.top
                    else: self.rect_colisao.top = arvore_col_rect.bottom
                    self.y = float(self.rect_colisao.centery)
                    break
        
        self.rect.center = (round(self.x), round(self.y))

    def atacar(self, inimigos_group, projeteis_group, dt_ms=None):
        current_time = time.time()
        if not self.current_weapon or self.is_attacking_animation_active or \
           (current_time - self.tempo_ultimo_ataque < self.cooldown_ataque):
            return

        if hasattr(self.current_weapon, 'attack_style') and self.current_weapon.attack_style == 'ranged':
            if not hasattr(self.current_weapon, 'projectile_class') or self.current_weapon.projectile_class is None:
                return

            inimigo_mais_proximo = None
            distancia_minima = float('inf')

            for inimigo in inimigos_group:
                if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo():
                    distancia = math.hypot(self.rect.centerx - inimigo.rect.centerx, self.rect.centery - inimigo.rect.centery)
                    if distancia < self.alcance_ataque and distancia < distancia_minima:
                        distancia_minima = distancia
                        inimigo_mais_proximo = inimigo

            if inimigo_mais_proximo:
                self.is_attacking = True
                self.is_attacking_animation_active = True
                self.attack_timer = time.time()
                self.tempo_ultimo_ataque = time.time()

                novo_projetil = self.current_weapon.projectile_class(
                    start_pos=self.rect.center,
                    target_enemy=inimigo_mais_proximo,
                    speed=getattr(self.current_weapon, 'projectile_speed', 5),
                    damage=self.dano,
                    lifetime=getattr(self.current_weapon, 'projectile_lifetime', 3.0),
                    scale=getattr(self.current_weapon, 'projectile_scale', 1.0)
                )
                if projeteis_group is not None:
                    projeteis_group.add(novo_projetil)
                else:
                    print("ERRO(Player.atacar): Grupo de projéteis é None.")

        else: # Melee
            self.is_attacking = True
            self.is_attacking_animation_active = True
            self.attack_timer = current_time
            self.tempo_ultimo_ataque = current_time
            self.hit_enemies_this_attack.clear()

            hitbox_w = self.current_weapon.hitbox_width
            hitbox_h = self.current_weapon.hitbox_height
            offset_x = self.current_weapon.hitbox_offset_x
            offset_y = self.current_weapon.hitbox_offset_y
            
            self.attack_hitbox = pygame.Rect(0, 0, hitbox_w, hitbox_h)
            hitbox_center_x = self.rect.centerx + (offset_x if self.direction == "right" else -offset_x)
            hitbox_center_y = self.rect.centery + offset_y
            self.attack_hitbox.center = (round(hitbox_center_x), round(hitbox_center_y))

            if hasattr(self.current_weapon, 'attack_animation_sprites') and self.current_weapon.attack_animation_sprites:
                self.current_weapon.current_attack_animation_frame = 0
                self.current_weapon.last_attack_animation_update = pygame.time.get_ticks()

            if self.is_attacking and self.attack_hitbox.width > 0:
                for inimigo in list(inimigos_group):
                    if inimigo and hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo() and hasattr(inimigo, 'rect'):
                        if self.attack_hitbox.colliderect(getattr(inimigo, 'rect_colisao', inimigo.rect)):
                            if inimigo not in self.hit_enemies_this_attack:
                                inimigo.receber_dano(self.dano, self.rect)
                                self.hit_enemies_this_attack.add(inimigo)

    def desenhar(self, janela, camera_x, camera_y):
        if self.image and hasattr(self, 'rect'):
            if not (self.is_invencivel_piscando and not self.visivel_durante_pisca_dano):
                janela.blit(self.image, (round(self.rect.x - camera_x), round(self.rect.y - camera_y)))

        if self.is_attacking_animation_active and self.current_weapon and hasattr(self.current_weapon, 'get_current_attack_animation_sprite'):
            attack_sprite = self.current_weapon.get_current_attack_animation_sprite()
            if attack_sprite:
                sprite_to_draw = pygame.transform.flip(attack_sprite, self.direction == "left", False)
                attack_sprite_rect = sprite_to_draw.get_rect(center=self.attack_hitbox.center)
                janela.blit(sprite_to_draw, (round(attack_sprite_rect.x - camera_x), round(attack_sprite_rect.y - camera_y)))

    def esta_vivo(self):
        return self.vida.esta_vivo() if self.vida else False

    def adicionar_item_inventario(self, item_da_loja_dict: dict) -> bool:
        if not isinstance(item_da_loja_dict, dict):
            return False
        nome_item = item_da_loja_dict.get("nome")
        if not nome_item:
            return False
        
        WeaponClass = self.SHOP_ITEM_TO_WEAPON_CLASS.get(nome_item)
        if WeaponClass:
            try:
                return self.add_owned_weapon(WeaponClass())
            except Exception as e:
                print(f"ERRO(Player.adicionar_item): Falha ao instanciar '{nome_item}': {e}")
        return False
            
    def evoluir_arma_atual(self, mapa_evolucoes_nivel_atual: dict) -> str | None:
        if not self.current_weapon or not isinstance(mapa_evolucoes_nivel_atual, dict):
            return None

        chave_evolucao = getattr(self.current_weapon, '_base_name', self.current_weapon.name)
        NovaClasseArmaEvoluida = mapa_evolucoes_nivel_atual.get(chave_evolucao)

        if NovaClasseArmaEvoluida:
            try:
                nova_arma = NovaClasseArmaEvoluida()
                arma_antiga = self.current_weapon
                self.equip_weapon(nova_arma)
                
                try:
                    idx = self.owned_weapons.index(arma_antiga)
                    self.owned_weapons[idx] = nova_arma
                except (ValueError, IndexError):
                    if not self.add_owned_weapon(nova_arma):
                        print(f"ALERTA(Player.evoluir): Não foi possível adicionar '{nova_arma.name}' ao inventário.")
                
                return nova_arma.name
            except Exception as e:
                print(f"ERRO(Player.evoluir): Falha ao instanciar evolução '{NovaClasseArmaEvoluida.__name__}': {e}")
        return None 