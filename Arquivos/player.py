import pygame
import random
import math
import os
import time

from vida import Vida 
from Armas.weapon import Weapon 

try: from Armas.EspadaBrasas import EspadaBrasas
except ImportError: EspadaBrasas = None
try: from Armas.MachadoCeruleo import MachadoCeruleo
except ImportError: MachadoCeruleo = None
try: from Armas.MachadoMacabro import MachadoMacabro
except ImportError: MachadoMacabro = None
try: from Armas.MachadoMarfim import MachadoMarfim
except ImportError: MachadoMarfim = None
try: from Armas.MachadoBarbaro import MachadoBarbaro
except ImportError: MachadoBarbaro = None
try: from Armas.AdagaFogo import AdagaFogo
except ImportError: AdagaFogo = None
try: from Armas.EspadaFogoAzul import EspadaFogoAzul
except ImportError: EspadaFogoAzul = None
try: from Armas.EspadaLua import EspadaLua
except ImportError: EspadaLua = None
try: from Armas.EspadaCaida import EspadaCaida
except ImportError: EspadaCaida = None
try: from Armas.EspadaPenitencia import EspadaPenitencia
except ImportError: EspadaPenitencia = None

# --- Mapeamento de nomes de itens da loja para classes de Armas (Exemplo) ---
SHOP_ITEM_TO_WEAPON_CLASS = {
    "Adaga Básica": AdagaFogo, 
    "Espada Média": EspadaBrasas, 
    "Espada dos Corrompidos": EspadaCaida,
    "Espada dos Deuses Caidos": EspadaFogoAzul, 
    "Espada Demoniaca": EspadaPenitencia, 
    "Machado Comum": MachadoBarbaro,
    "Machado Dos Heréges": MachadoMacabro, 
    "Machado de Batalha": MachadoCeruleo,
    "Machado Duplo": MachadoMarfim,
    # Adicione mais itens conforme necessário
}

class Player(pygame.sprite.Sprite):
    """
    Classe que representa o jogador no jogo.
    Gerencia movimento, animações, vida, a arma equipada, e invencibilidade temporária.
    """
    def __init__(self, velocidade=5, vida_maxima=150):
        super().__init__()

        self.x = float(random.randint(0, 800))
        self.y = float(random.randint(0, 600))

        self.velocidade = float(velocidade)
        if self.velocidade <= 0:
            self.velocidade = 1.0

        if Vida is not None:
            self.vida = Vida(vida_maxima)
        else:
            self.vida = None
            print("DEBUG(Player): Erro: Classe Vida não disponível.")

        self.xp_manager = None 
        self.dinheiro = 1000 

        tamanho_sprite_desejado = (60, 60)
        caminhos_esquerda = ["Sprites/Asrahel/Esquerda/Ashael_E1.png", "Sprites/Asrahel/Esquerda/Ashael_E2.png", "Sprites/Asrahel/Esquerda/Ashael_E3.png", "Sprites/Asrahel/Esquerda/Ashael_E4.png", "Sprites/Asrahel/Esquerda/Ashael_E5.png", "Sprites/Asrahel/Esquerda/Ashael_E6.png"]
        self.sprites_esquerda = self._carregar_sprites(caminhos_esquerda, tamanho_sprite_desejado, "Esquerda")
        caminhos_idle_esquerda = ["Sprites/Asrahel/Esquerda/Ashael_E1.png"]
        self.sprites_idle_esquerda = self._carregar_sprites(caminhos_idle_esquerda, tamanho_sprite_desejado, "Idle Esquerda")
        caminhos_direita = ["Sprites/Asrahel/Direita/Ashael_D1.png", "Sprites/Asrahel/Direita/Ashael_D2.png", "Sprites/Asrahel/Direita/Ashael_D3.png", "Sprites/Asrahel/Direita/Ashael_D4.png", "Sprites/Asrahel/Direita/Ashael_D5.png", "Sprites/Asrahel/Direita/Ashael_D6.png"]
        self.sprites_direita = self._carregar_sprites(caminhos_direita, tamanho_sprite_desejado, "Direita")
        caminhos_idle_direita = ["Sprites/Asrahel/Direita/Ashael_D1.png"]
        self.sprites_idle_direita = self._carregar_sprites(caminhos_idle_direita, tamanho_sprite_desejado, "Idle Direita")

        self.atual = 0
        self.frame_idle = 0
        
        self.parado = True
        self.direction = "right"

        self.image = None
        if self.sprites_idle_direita: self.image = self.sprites_idle_direita[0]
        elif self.sprites_idle_esquerda: self.image = self.sprites_idle_esquerda[0]
        elif self.sprites_direita: self.image = self.sprites_direita[0]
        elif self.sprites_esquerda: self.image = self.sprites_esquerda[0]
        else:
            self.image = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255,0,255), self.image.get_rect())

        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
        self.rect_colisao = self.rect.inflate(-30, -20) # Reduzido para melhor colisão

        self.tempo_animacao = 100
        self.ultimo_update = pygame.time.get_ticks()

        self.current_weapon: Weapon = None
        self.tempo_ultimo_ataque = 0.0

        if AdagaFogo is not None: # Equipar uma arma inicial
            self.equip_weapon(AdagaFogo())
        
        self.is_attacking = False 
        self.is_attacking_animation_active = False
        self.attack_duration = 0.3 
        self.attack_timer = 0.0

        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_enemies_this_attack = set()
        self.owned_weapons = []

        # --- Atributos para I-Frames (Invencibilidade Temporária) ---
        self.pode_levar_dano = True
        self.tempo_ultimo_dano_levado = 0  # Timestamp do último dano (pygame.time.get_ticks())
        self.duracao_invencibilidade_ms = 1500  # Duração da invencibilidade em milissegundos (ex: 1.5 segundos)
        self.is_invencivel_piscando = False # Controla se o jogador está no estado de piscar por dano
        self.tempo_para_proximo_pisca_dano = 0 # Timestamp para o próximo toggle de visibilidade
        self.intervalo_pisca_dano_ms = 100 # Intervalo entre os "piscas" (em ms)
        self.visivel_durante_pisca_dano = True # Controla se o sprite é desenhado durante o piscar

    @property
    def dano(self) -> float:
        return self.current_weapon.damage if self.current_weapon else 0.0

    @property
    def alcance_ataque(self) -> float:
        return self.current_weapon.attack_range if self.current_weapon else 0.0

    @property
    def cooldown_ataque(self) -> float:
        return self.current_weapon.cooldown if self.current_weapon else 0.0

    @property
    def level(self) -> int:
        return self.xp_manager.level if self.xp_manager else 1

    def equip_weapon(self, weapon_object: Weapon):
        if Weapon is None: return
        if isinstance(weapon_object, Weapon):
            self.current_weapon = weapon_object
            self.tempo_ultimo_ataque = time.time() 

    def add_owned_weapon(self, weapon_object: Weapon):
        if Weapon is None: return False
        if not isinstance(weapon_object, Weapon): return False
        if any(w.name == weapon_object.name for w in self.owned_weapons): return False
        if len(self.owned_weapons) >= 3: return False # Limite de 3 armas possuídas
        self.owned_weapons.append(weapon_object)
        if not self.current_weapon: self.equip_weapon(weapon_object)
        return True

    def _carregar_sprites(self, caminhos, tamanho, nome_conjunto):
        sprites = []
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        game_dir = os.path.dirname(base_dir) 
        for path in caminhos:
            full_path = os.path.join(game_dir, path.replace("/", os.sep))
            if not os.path.exists(full_path):
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255,0,255), (0,0,tamanho[0],tamanho[1]))
                sprites.append(placeholder); continue
            try:
                sprite = pygame.image.load(full_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, tamanho)
                sprites.append(sprite)
            except pygame.error as e:
                print(f"DEBUG(Player): Erro ao carregar sprite '{full_path}': {e}")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255,0,255), (0,0,tamanho[0],tamanho[1]))
                sprites.append(placeholder)
        if not sprites: # Garante que há pelo menos um sprite (placeholder)
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (255,0,255), (0,0,tamanho[0],tamanho[1]))
            sprites.append(placeholder)
        return sprites

    def receber_dano(self, dano): 
        if self.vida is not None and self.pode_levar_dano: # Verifica se pode levar dano
            self.vida.receber_dano(dano) # Reduz a vida através da classe Vida
            
            self.pode_levar_dano = False # Ativa a invencibilidade
            self.tempo_ultimo_dano_levado = pygame.time.get_ticks()
            self.is_invencivel_piscando = True # Ativa o feedback visual de piscar
            self.visivel_durante_pisca_dano = False # Começa "invisível" para o primeiro pisca
            self.tempo_para_proximo_pisca_dano = self.tempo_ultimo_dano_levado + self.intervalo_pisca_dano_ms
            
            if not self.esta_vivo():
                print("DEBUG(Player): Jogador morreu.")
            else:
                print(f"DEBUG(Player): Jogador recebeu {dano} de dano. Invencibilidade ativada por {self.duracao_invencibilidade_ms / 1000.0}s.")
        # else:
            # print("DEBUG(Player): Tentativa de dano enquanto invencível ou sem vida.")


    def update(self):
        agora_ticks = pygame.time.get_ticks()
        agora_time = time.time()

        # --- Lógica de Invencibilidade e Piscar ---
        if self.is_invencivel_piscando:
            # Controla o efeito de piscar
            if agora_ticks >= self.tempo_para_proximo_pisca_dano:
                self.visivel_durante_pisca_dano = not self.visivel_durante_pisca_dano # Alterna
                self.tempo_para_proximo_pisca_dano = agora_ticks + self.intervalo_pisca_dano_ms
            
            # Verifica se o tempo de invencibilidade acabou
            if agora_ticks - self.tempo_ultimo_dano_levado > self.duracao_invencibilidade_ms:
                self.pode_levar_dano = True
                self.is_invencivel_piscando = False
                self.visivel_durante_pisca_dano = True # Garante que o jogador fique visível ao final
                print("DEBUG(Player.update): Invencibilidade terminada.")
        # --- Fim da Lógica de Invencibilidade ---

        if self.is_attacking_animation_active and (agora_time - self.attack_timer >= self.attack_duration):
            self.is_attacking = False 
            self.is_attacking_animation_active = False 
            self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
            self.hit_enemies_this_attack.clear()
            if self.current_weapon and hasattr(self.current_weapon, 'current_attack_animation_frame'):
                self.current_weapon.current_attack_animation_frame = 0

        if agora_ticks - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora_ticks
            if self.parado:
                sprites_to_use_idle = []
                if self.direction == "left" and self.sprites_idle_esquerda: sprites_to_use_idle = self.sprites_idle_esquerda
                elif self.direction == "right" and self.sprites_idle_direita: sprites_to_use_idle = self.sprites_idle_direita
                elif self.sprites_idle_direita: sprites_to_use_idle = self.sprites_idle_direita 
                elif self.sprites_idle_esquerda: sprites_to_use_idle = self.sprites_idle_esquerda
                
                if sprites_to_use_idle:
                    self.frame_idle = (self.frame_idle + 1) % len(sprites_to_use_idle)
                    self.image = sprites_to_use_idle[self.frame_idle]
                elif self.sprites_direita and len(self.sprites_direita) > 0 : self.image = self.sprites_direita[0] 
                elif self.sprites_esquerda and len(self.sprites_esquerda) > 0: self.image = self.sprites_esquerda[0]
            else: 
                sprites_to_use_move = []
                if self.direction == "left" and self.sprites_esquerda: sprites_to_use_move = self.sprites_esquerda
                elif self.direction == "right" and self.sprites_direita: sprites_to_use_move = self.sprites_direita
                elif self.sprites_direita: sprites_to_use_move = self.sprites_direita
                elif self.sprites_esquerda: sprites_to_use_move = self.sprites_esquerda

                if sprites_to_use_move:
                    self.atual = (self.atual + 1) % len(sprites_to_use_move)
                    self.image = sprites_to_use_move[self.atual]
        
        if self.is_attacking_animation_active and self.current_weapon and \
           hasattr(self.current_weapon, 'attack_animation_sprites') and self.current_weapon.attack_animation_sprites and \
           hasattr(self.current_weapon, 'attack_animation_speed') and hasattr(self.current_weapon, 'last_attack_animation_update'):
            
            if agora_ticks - self.current_weapon.last_attack_animation_update > self.current_weapon.attack_animation_speed:
                self.current_weapon.last_attack_animation_update = agora_ticks
                num_frames_arma = len(self.current_weapon.attack_animation_sprites)
                if num_frames_arma > 0 : 
                    self.current_weapon.current_attack_animation_frame = (self.current_weapon.current_attack_animation_frame + 1) % num_frames_arma
        
        if self.image is None: 
                 self.image = pygame.Surface((60,60), pygame.SRCALPHA); pygame.draw.circle(self.image, (255,0,255), (30,30), 30)

        self.rect.center = (round(self.x), round(self.y))
        if hasattr(self, 'rect_colisao'): 
            self.rect_colisao.center = self.rect.center

    def mover(self, teclas, arvores):
        if not hasattr(self, 'rect_colisao'):
            return

        current_dx, current_dy = 0.0, 0.0
        
        move_left = teclas[pygame.K_LEFT] or teclas[pygame.K_a]
        move_right = teclas[pygame.K_RIGHT] or teclas[pygame.K_d]
        move_up = teclas[pygame.K_UP] or teclas[pygame.K_w]
        move_down = teclas[pygame.K_DOWN] or teclas[pygame.K_s]

        if move_left and not move_right:
            current_dx = -self.velocidade
            self.direction = "left"
        elif move_right and not move_left:
            current_dx = self.velocidade
            self.direction = "right"
        
        if move_up and not move_down:
            current_dy = -self.velocidade
        elif move_down and not move_up:
            current_dy = self.velocidade
        
        if current_dx != 0.0 and current_dy != 0.0:
            inv_sqrt2 = 1.0 / math.sqrt(2)
            current_dx *= inv_sqrt2 
            current_dy *= inv_sqrt2
        
        self.parado = not (current_dx != 0.0 or current_dy != 0.0)
        
        original_x_colisao = self.x 
        self.x += current_dx
        if hasattr(self, 'rect_colisao'): 
            self.rect_colisao.centerx = round(self.x)
            if arvores and current_dx != 0:
                for arvore in arvores:
                    arvore_rect = getattr(arvore, 'rect_colisao', getattr(arvore, 'rect', None))
                    if arvore_rect and self.rect_colisao.colliderect(arvore_rect):
                        if current_dx > 0: self.rect_colisao.right = arvore_rect.left
                        elif current_dx < 0: self.rect_colisao.left = arvore_rect.right
                        self.x = float(self.rect_colisao.centerx) 
                        break 
        
        original_y_colisao = self.y 
        self.y += current_dy
        if hasattr(self, 'rect_colisao'): 
            self.rect_colisao.centery = round(self.y)
            if arvores and current_dy != 0:
                for arvore in arvores:
                    arvore_rect = getattr(arvore, 'rect_colisao', getattr(arvore, 'rect', None))
                    if arvore_rect and self.rect_colisao.colliderect(arvore_rect):
                        if current_dy > 0: self.rect_colisao.bottom = arvore_rect.top
                        elif current_dy < 0: self.rect_colisao.top = arvore_rect.bottom
                        self.y = float(self.rect_colisao.centery) 
                        break
        
        if hasattr(self, 'rect'): self.rect.center = (round(self.x), round(self.y))

    def atacar(self, inimigos):
        current_time = time.time()
        if self.current_weapon and not self.is_attacking_animation_active and \
           current_time - self.tempo_ultimo_ataque >= self.cooldown_ataque:
            
            self.is_attacking = True 
            self.is_attacking_animation_active = True 
            
            self.attack_timer = current_time 
            self.tempo_ultimo_ataque = current_time 
            self.hit_enemies_this_attack.clear()
            
            hitbox_w = self.current_weapon.hitbox_width
            hitbox_h = self.current_weapon.hitbox_height
            offset_x_arma = self.current_weapon.hitbox_offset_x 
            offset_y_arma = self.current_weapon.hitbox_offset_y 
            
            self.attack_hitbox = pygame.Rect(0, 0, hitbox_w, hitbox_h)

            base_attack_point_x = self.rect.centerx
            if self.direction == "right":
                base_attack_point_x += self.alcance_ataque 
                hitbox_center_x = base_attack_point_x + offset_x_arma 
            else: # "left"
                base_attack_point_x -= self.alcance_ataque
                hitbox_center_x = base_attack_point_x - offset_x_arma
            
            hitbox_center_y = self.rect.centery + offset_y_arma
            self.attack_hitbox.center = (round(hitbox_center_x), round(hitbox_center_y))

            if hasattr(self.current_weapon, 'attack_animation_sprites') and self.current_weapon.attack_animation_sprites:
                if not hasattr(self.current_weapon, 'current_attack_animation_frame'): 
                    self.current_weapon.current_attack_animation_frame = 0
                if not hasattr(self.current_weapon, 'last_attack_animation_update'): 
                    self.current_weapon.last_attack_animation_update = 0
                    
                self.current_weapon.current_attack_animation_frame = 0
                self.current_weapon.last_attack_animation_update = pygame.time.get_ticks()

        if self.is_attacking and self.attack_hitbox.width > 0: 
            if inimigos:
                for inimigo in list(inimigos): 
                    if inimigo and hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo() and \
                       hasattr(inimigo, 'rect') and inimigo.rect is not None:
                        inimigo_colisao_rect = getattr(inimigo, 'rect_colisao', inimigo.rect)
                        if self.attack_hitbox.colliderect(inimigo_colisao_rect) and \
                           inimigo not in self.hit_enemies_this_attack:
                            if hasattr(inimigo, 'receber_dano'):
                                inimigo.receber_dano(self.dano) 
                                self.hit_enemies_this_attack.add(inimigo)
                                if not inimigo.esta_vivo():
                                    if hasattr(inimigo, 'xp_value') and self.xp_manager:
                                        self.xp_manager.gain_xp(inimigo.xp_value)

    def empurrar_jogador(self, obstaculo_rect):
        pass 

    def desenhar(self, janela, camera_x, camera_y):
        # Desenha o jogador, considerando o efeito de piscar da invencibilidade
        if self.image is not None and hasattr(self, 'rect'):
            if self.is_invencivel_piscando and not self.visivel_durante_pisca_dano:
                pass # Não desenha o jogador para criar o efeito de piscar
            else:
                # Se não estiver piscando ou se for para ser visível durante o pisca, desenha normal
                janela.blit(self.image, (round(self.rect.x - camera_x), round(self.rect.y - camera_y)))

        # Desenha o sprite de animação de ataque da arma, se ativo
        if self.is_attacking_animation_active and self.current_weapon and \
           hasattr(self.current_weapon, 'get_current_attack_animation_sprite'):
            
            attack_sprite_visual = self.current_weapon.get_current_attack_animation_sprite()
            
            if attack_sprite_visual:
                sprite_to_draw = attack_sprite_visual.copy()
                if self.direction == "left":
                    sprite_to_draw = pygame.transform.flip(sprite_to_draw, True, False)
                
                attack_sprite_rect = sprite_to_draw.get_rect(center=self.attack_hitbox.center)
                
                janela.blit(sprite_to_draw, (round(attack_sprite_rect.x - camera_x), 
                                             round(attack_sprite_rect.y - camera_y)))
        
        # Opcional: Desenhar a hitbox LÓGICA para depuração
        # if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0:
        #     debug_hitbox_rect_on_screen = pygame.Rect(
        #         round(self.attack_hitbox.x - camera_x), 
        #         round(self.attack_hitbox.y - camera_y),
        #         self.attack_hitbox.width, 
        #         self.attack_hitbox.height
        #     )
        #     pygame.draw.rect(janela, (255, 0, 0, 100), debug_hitbox_rect_on_screen, 1) 


    def esta_vivo(self):
        if self.vida is not None:
            return self.vida.esta_vivo()
        return False
    
    def adicionar_item_inventario(self, item_da_loja_dict):
        nome_item = item_da_loja_dict.get("nome")
        if not nome_item: return False
        WeaponClass = SHOP_ITEM_TO_WEAPON_CLASS.get(nome_item)
        if WeaponClass:
            try:
                nova_arma = WeaponClass() 
                return self.add_owned_weapon(nova_arma)
            except Exception as e: print(f"DEBUG(Player): Erro ao instanciar '{nome_item}': {e}")
        else: print(f"DEBUG(Player): Classe não mapeada para '{nome_item}'")
        return False
            
    def evoluir_arma_atual(self, mapa_evolucoes_nivel_atual) -> str | None:
        if not self.current_weapon: return None
        arma_atual_nome = self.current_weapon.name
        if arma_atual_nome in mapa_evolucoes_nivel_atual:
            NovaClasseArma = mapa_evolucoes_nivel_atual[arma_atual_nome]
            try:
                nova_arma = NovaClasseArma()
                self.equip_weapon(nova_arma) 
                for i, owned_weapon in enumerate(self.owned_weapons):
                    if owned_weapon.name == arma_atual_nome:
                        self.owned_weapons[i] = nova_arma; break
                return nova_arma.name
            except Exception as e: print(f"DEBUG(Player): Erro ao evoluir '{NovaClasseArma.__name__}': {e}")
        return None

