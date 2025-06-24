import pygame
import random
import math
import os
import time
from importacoes_Player import * # Assume que este arquivo importa Vida e Weapon, e as classes de armas
from import_Loja import *
from vida import *
from pocao import PocaoVida

# --- Importação das classes de armas para mapeamento ---
try: from Armas.EspadaBrasas import EspadaBrasas 
except ImportError: EspadaBrasas = None
try: from Armas.CajadoDaFixacaoAmetista import CajadoDaFixacaoAmetista
except ImportError: CajadoDaFixacaoAmetista = None
try: from Armas.CajadoDaSantaNatureza import CajadoDaSantaNatureza
except ImportError: CajadoDaSantaNatureza = None
try: from Armas.LivroDosImpuros import LivroDosImpuros
except ImportError: LivroDosImpuros = None
# Adicione outras importações de armas aqui conforme necessário

# --- Mapeamento de nomes de itens da loja para classes de Armas ---
# CORRIGIDO: As chaves agora correspondem exatamente aos nomes dos itens da loja
SHOP_ITEM_TO_WEAPON_CLASS_MAP = {
    "Adaga do Fogo Contudente": AdagaFogo,
    "Espada de Fogo azul Sacra Cerulea": EspadaFogoAzul,
    "Espada do Olhar Da Penitencia": EspadaPenitencia,
    "Espada Sacra Caida": EspadaCaida,
    "Espada Sacra do Lua": EspadaLua,
    "Lâmina do Céu Cintilante": LaminaDoCeuCintilante,
    "Machado Bárbaro Cravejado": MachadoBarbaro,
    "Machado Cerúleo da Estrela Cadente": MachadoCeruleo,
    "Machado da Descida Santa": MachadoDaDescidaSanta,
    "Machado do Fogo Abrasador": MachadoDoFogoAbrasador,
    "Machado do Marfim Resplendor": MachadoMarfim,
    "Machado Macabro da Gula Infinita": MachadoMacabro,

    # --- CORREÇÃO APLICADA AQUI: Nomes ajustados para corresponder aos logs de erro ---
    "Cajado da Fixacao Ametista": CajadoDaFixacaoAmetista,
    "Cajado Da santa Natureza": CajadoDaSantaNatureza, # Mantido com 'D' maiúsculo como no seu código original
    "Livro dos impuros": LivroDosImpuros,

    # Se "Espada Sacra Das Brasas" for um item da loja e usar a classe EspadaBrasas:
    # "Espada Sacra Das Brasas": EspadaBrasas, 
}

class Player(pygame.sprite.Sprite):
    """
    Classe que representa o jogador no jogo.
    Gerencia movimento, animações, vida, a arma equipada, e invencibilidade temporária.
    """
    def __init__(self, velocidade=15, vida_maxima=150):
        super().__init__()

        # Posição inicial aleatória (ajuste para posição definida se necessário)
        self.x = float(random.randint(100, 700)) # Evita spawn muito nas bordas
        self.y = float(random.randint(100, 500))

        self.velocidade = float(velocidade)
        if self.velocidade <= 0: # Garante velocidade positiva
            self.velocidade = 1.0 
        
        # --- ADICIONADO PARA EFEITOS DE COGUMELO E POÇÕES ---
        self.velocidade_original = self.velocidade
        self.tempo_fim_efeito_lentidao = 0
        self.tempo_fim_efeito_rapidez = 0
        # --- FIM DA ADIÇÃO ---

        if Vida is not None:
            self.vida = Vida(vida_maxima)
        else:
            self.vida = None # Objeto Vida não disponível
            print("DEBUG(Player): ERRO CRÍTICO: Classe Vida não disponível. Funcionalidades de vida estarão ausentes.")

        self.nivel = 1
        self.experiencia = 0
        self.experiencia_para_proximo_nivel = 100
        self.total_pontos_experiencia_acumulados = 0
        
        self.xp_manager = None 
        self.dinheiro = 0 # Dinheiro inicial do jogador
        
        # --- ADICIONADO PARA GERAR OURO PASSIVAMENTE ---
        self.tempo_ultimo_ouro = pygame.time.get_ticks()
        
        self.SHOP_ITEM_TO_WEAPON_CLASS = SHOP_ITEM_TO_WEAPON_CLASS_MAP

        # Configuração e carregamento de sprites de animação
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
        if self.sprites_idle_direita and len(self.sprites_idle_direita) > 0: self.image = self.sprites_idle_direita[0]
        elif self.sprites_idle_esquerda and len(self.sprites_idle_esquerda) > 0: self.image = self.sprites_idle_esquerda[0]
        elif self.sprites_direita and len(self.sprites_direita) > 0: self.image = self.sprites_direita[0]
        elif self.sprites_esquerda and len(self.sprites_esquerda) > 0: self.image = self.sprites_esquerda[0]
        else:
            self.image = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
            self.image.fill((255,0,255, 150))
            print("ALERTA(Player Init): Nenhum sprite carregado para o jogador. Usando placeholder.")

        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
        self.rect_colisao = self.rect.inflate(-30, -20) 

        self.tempo_animacao = 100
        self.ultimo_update = pygame.time.get_ticks()

        self.current_weapon: Weapon = None
        self.tempo_ultimo_ataque = 0.0

        if 'AdagaFogo' in globals() and AdagaFogo is not None:
            try:
                self.current_weapon = AdagaFogo()
                print(f"DEBUG(Player Init): Arma inicial '{self.current_weapon.name}' instanciada.")
            except Exception as e_init_weapon:
                self.current_weapon = None
                print(f"ERRO(Player Init): Falha ao instanciar AdagaFogo inicial: {e_init_weapon}")
        else:
            print("ALERTA(Player Init): Classe AdagaFogo não disponível para arma inicial.")
        
        self.is_attacking = False
        self.is_attacking_animation_active = False
        self.attack_duration = 0.3
        self.attack_timer = 0.0

        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_enemies_this_attack = set()
        
        self.owned_weapons = [None] * 4
        if self.current_weapon:
            self.owned_weapons[0] = self.current_weapon

        self.pode_levar_dano = True
        self.tempo_ultimo_dano_levado = 0
        self.duracao_invencibilidade_ms = 500
        self.is_invencivel_piscando = False
        self.tempo_para_proximo_pisca_dano = 0 
        self.intervalo_pisca_dano_ms = 80
        self.visivel_durante_pisca_dano = True

        self.projeteis_ativos = pygame.sprite.Group()

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
            print("ALERTA(Player.equip_weapon): Classe base Weapon não está disponível (importação falhou?).")
            return
        if isinstance(weapon_object, Weapon):
            self.current_weapon = weapon_object
            self.tempo_ultimo_ataque = time.time()
            print(f"DEBUG(Player.equip_weapon): Arma '{self.current_weapon.name}' equipada.")
        else:
            print(f"ALERTA(Player.equip_weapon): Tentativa de equipar objeto inválido: {type(weapon_object)}. Esperava-se um objeto Weapon.")

    def add_owned_weapon(self, weapon_object: Weapon) -> bool:
        if Weapon is None:
            return False

        if not isinstance(weapon_object, Weapon):
            print(f"ALERTA(Player.add_owned_weapon): Tentativa de adicionar objeto inválido: {type(weapon_object)}")
            return False

        if hasattr(weapon_object, '_base_name'):
            if any(hasattr(w, '_base_name') and w._base_name == weapon_object._base_name for w in self.owned_weapons if w is not None):
                print(f"DEBUG(Player.add_owned_weapon): Arma '{weapon_object.name}' (ou uma versão dela) já está no inventário.")
                return False
        
        try:
            index_vazio = self.owned_weapons.index(None)
            self.owned_weapons[index_vazio] = weapon_object
            print(f"DEBUG(Player.add_owned_weapon): Arma '{weapon_object.name}' adicionada ao inventário no espaço {index_vazio}.")
            
            if self.current_weapon is None:
                self.equip_weapon(weapon_object)
            
            return True
        except ValueError:
            print(f"DEBUG(Player.add_owned_weapon): Inventário de armas cheio (4/4). Não foi possível adicionar '{weapon_object.name}'.")
            return False

    def _carregar_sprites(self, caminhos, tamanho, nome_conjunto):
        sprites = []
        base_dir_script = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir_script)

        for path_relativo_ao_projeto in caminhos:
            full_path = os.path.join(project_root, path_relativo_ao_projeto.replace("/", os.sep))
            
            if not os.path.exists(full_path):
                print(f"ALERTA(Player._carregar_sprites): Sprite para '{nome_conjunto}' não encontrado: {full_path}")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((255,0,255, 100))
                sprites.append(placeholder)
                continue
            try:
                sprite = pygame.image.load(full_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, tamanho)
                sprites.append(sprite)
            except pygame.error as e:
                print(f"DEBUG(Player._carregar_sprites): Erro ao carregar sprite '{full_path}' para '{nome_conjunto}': {e}")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((255,0,255, 100))
                sprites.append(placeholder)
        
        if not sprites:
            print(f"ALERTA GRAVE(Player._carregar_sprites): Nenhum sprite carregado para '{nome_conjunto}'.")
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((255,0,0, 150))
            sprites.append(placeholder)
        return sprites

    def receber_dano(self, dano, _fonte_dano_rect=None):
        if self.vida is not None and self.pode_levar_dano: 
            self.vida.receber_dano(dano) 
            
            self.pode_levar_dano = False 
            self.tempo_ultimo_dano_levado = pygame.time.get_ticks()
            self.is_invencivel_piscando = True 
            self.visivel_durante_pisca_dano = False
            self.tempo_para_proximo_pisca_dano = self.tempo_ultimo_dano_levado + self.intervalo_pisca_dano_ms
            
            if not self.esta_vivo():
                print("DEBUG(Player): Jogador morreu.")
    
    def receber_cura(self, valor_cura):
        if self.vida is not None and hasattr(self.vida, 'curar'):
            self.vida.curar(valor_cura)
            print(f"DEBUG(Player): Jogador curado em {valor_cura} pontos. Vida atual: {self.vida.vida_atual}")
        else:
            print("ALERTA(Player.receber_cura): Objeto Vida ou método 'curar' não disponível.")
    
    def aplicar_efeito_cogumelo(self, tipo_efeito, duracao, magnitude):
        agora = time.time()
        
        if tipo_efeito == 'cura':
            self.receber_cura(magnitude)
        
        elif tipo_efeito == 'lentidao':
            self.velocidade = self.velocidade_original * (1 - magnitude)
            self.tempo_fim_efeito_lentidao = agora + duracao
            self.tempo_fim_efeito_rapidez = 0
            print(f"DEBUG(Player): Efeito de lentidão aplicado. Nova velocidade: {self.velocidade:.2f}")

        elif tipo_efeito == 'rapidez':
            self.velocidade = self.velocidade_original * (1 + magnitude)
            self.tempo_fim_efeito_rapidez = agora + duracao
            self.tempo_fim_efeito_lentidao = 0
            print(f"DEBUG(Player): Efeito de rapidez aplicado. Nova velocidade: {self.velocidade:.2f}")

    def update(self, dt_ms=None, teclas_pressionadas=None):
        agora_ticks = pygame.time.get_ticks()
        agora_time = time.time()
        
        # --- LÓGICA DE GERAÇÃO DE OURO ---
        if agora_ticks - self.tempo_ultimo_ouro > 1000: # 1000 ms = 1 segundo
            self.dinheiro += 12
            self.tempo_ultimo_ouro = agora_ticks
        # --- FIM DA LÓGICA DE GERAÇÃO DE OURO ---

        if self.tempo_fim_efeito_lentidao > 0 and agora_time >= self.tempo_fim_efeito_lentidao:
            self.velocidade = self.velocidade_original
            self.tempo_fim_efeito_lentidao = 0
            print("DEBUG(Player): Efeito de lentidão terminou.")
            
        if self.tempo_fim_efeito_rapidez > 0 and agora_time >= self.tempo_fim_efeito_rapidez:
            self.velocidade = self.velocidade_original
            self.tempo_fim_efeito_rapidez = 0
            print("DEBUG(Player): Efeito de rapidez terminou.")

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
            self.attack_hitbox.size = (0,0)
            self.hit_enemies_this_attack.clear()
            if self.current_weapon and hasattr(self.current_weapon, 'current_attack_animation_frame'):
                self.current_weapon.current_attack_animation_frame = 0

        if agora_ticks - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora_ticks
            active_sprites_list = []
            if self.parado:
                if self.direction == "left": active_sprites_list = self.sprites_idle_esquerda
                else: active_sprites_list = self.sprites_idle_direita
                
                if active_sprites_list:
                    self.frame_idle = (self.frame_idle + 1) % len(active_sprites_list)
                    self.image = active_sprites_list[self.frame_idle]
                elif self.direction == "left" and self.sprites_esquerda: self.image = self.sprites_esquerda[0]
                elif self.sprites_direita: self.image = self.sprites_direita[0]
            else: # Movendo-se
                if self.direction == "left": active_sprites_list = self.sprites_esquerda
                else: active_sprites_list = self.sprites_direita
                if active_sprites_list:
                    self.atual = (self.atual + 1) % len(active_sprites_list)
                    self.image = active_sprites_list[self.atual]
        
        if self.is_attacking_animation_active and self.current_weapon and hasattr(self.current_weapon, 'update_animation'):
            self.current_weapon.update_animation(agora_ticks)
        
        if self.image is None: 
            self.image = pygame.Surface((60,60), pygame.SRCALPHA); self.image.fill((255,0,255,100))

        self.rect.center = (round(self.x), round(self.y))
        if hasattr(self, 'rect_colisao'): 
            self.rect_colisao.center = self.rect.center

    def mover(self, teclas, arvores):
        if not hasattr(self, 'rect_colisao'): return

        current_dx, current_dy = 0.0, 0.0
        
        move_left = teclas[pygame.K_LEFT] or teclas[pygame.K_a]
        move_right = teclas[pygame.K_RIGHT] or teclas[pygame.K_d]
        move_up = teclas[pygame.K_UP] or teclas[pygame.K_w]
        move_down = teclas[pygame.K_DOWN] or teclas[pygame.K_s]

        if move_left and not move_right: current_dx = -self.velocidade; self.direction = "left"
        elif move_right and not move_left: current_dx = self.velocidade; self.direction = "right"
        
        if move_up and not move_down: current_dy = -self.velocidade
        elif move_down and not move_up: current_dy = self.velocidade
        
        if current_dx != 0.0 and current_dy != 0.0:
            inv_sqrt2 = 1.0 / math.sqrt(2)
            current_dx *= inv_sqrt2 
            current_dy *= inv_sqrt2
        
        self.parado = not (current_dx != 0.0 or current_dy != 0.0)
        
        self.x += current_dx
        self.rect_colisao.centerx = round(self.x)
        
        self.y += current_dy
        self.rect_colisao.centery = round(self.y)
        
        if hasattr(self, 'rect'): self.rect.center = (round(self.x), round(self.y))

    def atacar(self, inimigos, dt_ms=None):
        current_time = time.time()
        if self.current_weapon and not self.is_attacking_animation_active and \
           (current_time - self.tempo_ultimo_ataque >= self.cooldown_ataque):
            
            self.is_attacking = True 
            self.is_attacking_animation_active = True 
            
            self.attack_timer = current_time
            self.tempo_ultimo_ataque = current_time
            self.hit_enemies_this_attack.clear()
            
            if hasattr(self.current_weapon, 'attack_animation_sprites') and hasattr(self.current_weapon, 'attack_animation_speed'):
                num_frames = len(self.current_weapon.attack_animation_sprites)
                speed_ms = self.current_weapon.attack_animation_speed
                if num_frames > 0 and speed_ms > 0:
                    self.attack_duration = (num_frames * speed_ms) / 1000.0
                else:
                    self.attack_duration = 0.3
            else:
                self.attack_duration = 0.3

            hitbox_w = self.current_weapon.hitbox_width
            hitbox_h = self.current_weapon.hitbox_height
            offset_x_arma = self.current_weapon.hitbox_offset_x 
            offset_y_arma = self.current_weapon.hitbox_offset_y 
            
            self.attack_hitbox = pygame.Rect(0, 0, hitbox_w, hitbox_h)

            if self.direction == "right":
                hitbox_center_x = self.rect.centerx + offset_x_arma 
            else:
                hitbox_center_x = self.rect.centerx - offset_x_arma 
            
            hitbox_center_y = self.rect.centery + offset_y_arma
            self.attack_hitbox.center = (round(hitbox_center_x), round(hitbox_center_y))

            if hasattr(self.current_weapon, 'start_attack_animation'):
                self.current_weapon.start_attack_animation()

        if self.is_attacking and self.attack_hitbox.width > 0: 
            if inimigos:
                for inimigo in list(inimigos):
                    if inimigo and hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo() and hasattr(inimigo, 'rect') and inimigo.rect is not None:
                        inimigo_colisao_rect = getattr(inimigo, 'rect_colisao', inimigo.rect)
                        
                        if self.attack_hitbox.colliderect(inimigo_colisao_rect) and inimigo not in self.hit_enemies_this_attack:
                            if hasattr(inimigo, 'receber_dano'):
                                inimigo.receber_dano(self.dano, self.rect)
                                self.hit_enemies_this_attack.add(inimigo)
                                
                                if not inimigo.esta_vivo():
                                    xp_value = getattr(inimigo, 'xp_value_boss', getattr(inimigo, 'xp_value', 0))
                                    if xp_value > 0 and self.xp_manager and hasattr(self.xp_manager, 'gain_xp'):
                                        self.xp_manager.gain_xp(xp_value)

    def desenhar(self, janela, camera_x, camera_y):
        if self.image is not None and hasattr(self, 'rect'):
            if self.is_invencivel_piscando and not self.visivel_durante_pisca_dano:
                pass
            else:
                janela.blit(self.image, (round(self.rect.x - camera_x), round(self.rect.y - camera_y)))

        if self.is_attacking_animation_active and self.current_weapon and hasattr(self.current_weapon, 'get_current_attack_animation_sprite'):
            attack_sprite_visual = self.current_weapon.get_current_attack_animation_sprite()
            
            if attack_sprite_visual and isinstance(attack_sprite_visual, pygame.Surface):
                sprite_to_draw = attack_sprite_visual.copy()
                if self.direction == "left":
                    sprite_to_draw = pygame.transform.flip(sprite_to_draw, True, False)
                
                attack_sprite_rect = sprite_to_draw.get_rect(center=self.attack_hitbox.center)
                
                janela.blit(sprite_to_draw, (round(attack_sprite_rect.x - camera_x), 
                                             round(attack_sprite_rect.y - camera_y)))

    def esta_vivo(self):
        if self.vida is not None and hasattr(self.vida, 'esta_vivo'):
            return self.vida.esta_vivo()
        print("ALERTA(Player.esta_vivo): Objeto Vida não encontrado. Retornando False.")
        return False
    
    def adicionar_item_inventario(self, item_da_loja_dict) -> bool:
        if not isinstance(item_da_loja_dict, dict): return False
        nome_item = item_da_loja_dict.get("nome")
        if not nome_item: return False
        
        WeaponClass = self.SHOP_ITEM_TO_WEAPON_CLASS.get(nome_item)
        if WeaponClass is not None:
            try:
                nova_arma = WeaponClass() 
                return self.add_owned_weapon(nova_arma)
            except Exception as e: 
                print(f"ERRO(Player.adicionar_item_inventario): Erro ao instanciar '{nome_item}': {e}")
        else: 
            print(f"ALERTA(Player.adicionar_item_inventario): Nenhuma classe de arma mapeada para o item '{nome_item}'.")
        return False
            
    def evoluir_arma_atual(self, mapa_evolucoes_nivel_atual: dict) -> str | None:
        if not self.current_weapon: return None
        if not isinstance(mapa_evolucoes_nivel_atual, dict): return None

        chave_evolucao = getattr(self.current_weapon, '_base_name', self.current_weapon.name)
        NovaClasseArmaEvoluida = mapa_evolucoes_nivel_atual.get(chave_evolucao)

        if NovaClasseArmaEvoluida is not None:
            try:
                nova_arma_evoluida_inst = NovaClasseArmaEvoluida()
                arma_antiga_instancia = self.current_weapon
                self.equip_weapon(nova_arma_evoluida_inst)
                
                try:
                    idx_antiga = self.owned_weapons.index(arma_antiga_instancia)
                    self.owned_weapons[idx_antiga] = nova_arma_evoluida_inst
                except ValueError: 
                    print(f"ALERTA(Player.evoluir_arma_atual): Arma antiga não encontrada em owned_weapons para substituição.")
                    if not self.add_owned_weapon(nova_arma_evoluida_inst):
                        print(f"ALERTA(Player.evoluir_arma_atual): Não foi possível adicionar '{nova_arma_evoluida_inst.name}' a owned_weapons.")
                
                print(f"DEBUG(Player.evoluir_arma_atual): Arma '{getattr(arma_antiga_instancia, 'name', 'N/A')}' evoluiu para '{nova_arma_evoluida_inst.name}'.")
                return nova_arma_evoluida_inst.name
            except Exception as e: 
                print(f"ERRO(Player.evoluir_arma_atual): Erro ao instanciar evolução '{NovaClasseArmaEvoluida.__name__}': {e}")
        return None

    def ganhar_xp_chefe(self, xp_amount):
        if self.xp_manager and hasattr(self.xp_manager, 'gain_xp'):
            print(f"DEBUG(Player): Ganhando {xp_amount} de XP do chefe.")
            self.xp_manager.gain_xp(xp_amount)
        else:
            print(f"ALERTA(Player): xp_manager não configurado. Não foi possível adicionar {xp_amount} de XP do chefe.")
