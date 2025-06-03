import pygame
import random
import math
import os
import time
from importacoes_Player import * # Assume que este arquivo importa Vida e Weapon, e as classes de armas


# A classe EspadaBrasas é importada mas não parece corresponder diretamente a um item na lista da loja fornecida.
# Se "Espada Sacra Das Brasas" for um item da loja, adicione-o ao SHOP_ITEM_TO_WEAPON_CLASS_MAP.
try: from Armas.EspadaBrasas import EspadaBrasas 
except ImportError: EspadaBrasas = None


# --- Mapeamento de nomes de itens da loja para classes de Armas ---
# As chaves DEVEM CORRESPONDER EXATAMENTE aos nomes ("nome") dos itens em itens_data_global no loja_modulo.py
SHOP_ITEM_TO_WEAPON_CLASS_MAP = {
    "Adaga do Fogo Contudente": AdagaFogo,
    "Espada de Fogo azul Sacra Cerulea": EspadaFogoAzul,
    "Espada do Olhar Da Penitencia": EspadaPenitencia,
    "Espada Sacra Caida": EspadaCaida,
    "Espada Sacra do Lua": EspadaLua,
    "Lâmina do Ceu Centilhante": LaminaDoCeuCentilhante,
    
    "Machado Bárbaro Cravejado": MachadoBarbaro,
    "Machado Cerúleo da Estrela Cadente": MachadoCeruleo,
    "Machado da Descida Santa": MachadoDaDescidaSanta,
    "Machado do Fogo Abrasador": MachadoDoFogoAbrasador,
    "Machado do Marfim Resplendor": MachadoMarfim,
    "Machado Macabro da Gula Infinita": MachadoMacabro,

    # Adicione aqui os mapeamentos para os cajados se eles forem armas compráveis
    # Exemplo: "Cajado da Fixacao Ametista": CajadoDaFixacaoAmetista,
    # "Cajado Da santa Natureza": CajadoDaSantaNatureza,
    # "Livro dos impuros": LivroDosImpuros,

    # Se "Espada Sacra Das Brasas" for um item da loja e usar a classe EspadaBrasas:
    # "Espada Sacra Das Brasas": EspadaBrasas, 
}

class Player(pygame.sprite.Sprite):
    """
    Classe que representa o jogador no jogo.
    Gerencia movimento, animações, vida, a arma equipada, e invencibilidade temporária.
    """
    def __init__(self, velocidade=5, vida_maxima=150):
        super().__init__()

        # Posição inicial aleatória (ajuste para posição definida se necessário)
        self.x = float(random.randint(100, 700)) # Evita spawn muito nas bordas
        self.y = float(random.randint(100, 500))

        self.velocidade = float(velocidade)
        if self.velocidade <= 0: # Garante velocidade positiva
            self.velocidade = 1.0 

        if Vida is not None:
            self.vida = Vida(vida_maxima)
        else:
            self.vida = None # Objeto Vida não disponível
            print("DEBUG(Player): ERRO CRÍTICO: Classe Vida não disponível. Funcionalidades de vida estarão ausentes.")

        self.xp_manager = None 
        self.dinheiro = 1000 # Dinheiro inicial do jogador
        
        # Mapeamento para converter nomes de itens da loja em classes de armas
        self.SHOP_ITEM_TO_WEAPON_CLASS = SHOP_ITEM_TO_WEAPON_CLASS_MAP

        # Configuração e carregamento de sprites de animação
        tamanho_sprite_desejado = (60, 60) # Tamanho padrão para os sprites do jogador
        # Caminhos relativos à pasta 'Sprites' na raiz do projeto (conforme _carregar_sprites)
        caminhos_esquerda = ["Sprites/Asrahel/Esquerda/Ashael_E1.png", "Sprites/Asrahel/Esquerda/Ashael_E2.png", "Sprites/Asrahel/Esquerda/Ashael_E3.png", "Sprites/Asrahel/Esquerda/Ashael_E4.png", "Sprites/Asrahel/Esquerda/Ashael_E5.png", "Sprites/Asrahel/Esquerda/Ashael_E6.png"]
        self.sprites_esquerda = self._carregar_sprites(caminhos_esquerda, tamanho_sprite_desejado, "Esquerda")
        caminhos_idle_esquerda = ["Sprites/Asrahel/Esquerda/Ashael_E1.png"] # Frame idle
        self.sprites_idle_esquerda = self._carregar_sprites(caminhos_idle_esquerda, tamanho_sprite_desejado, "Idle Esquerda")
        caminhos_direita = ["Sprites/Asrahel/Direita/Ashael_D1.png", "Sprites/Asrahel/Direita/Ashael_D2.png", "Sprites/Asrahel/Direita/Ashael_D3.png", "Sprites/Asrahel/Direita/Ashael_D4.png", "Sprites/Asrahel/Direita/Ashael_D5.png", "Sprites/Asrahel/Direita/Ashael_D6.png"]
        self.sprites_direita = self._carregar_sprites(caminhos_direita, tamanho_sprite_desejado, "Direita")
        caminhos_idle_direita = ["Sprites/Asrahel/Direita/Ashael_D1.png"] # Frame idle
        self.sprites_idle_direita = self._carregar_sprites(caminhos_idle_direita, tamanho_sprite_desejado, "Idle Direita")

        self.atual = 0 # Índice do frame de animação de movimento
        self.frame_idle = 0 # Índice do frame de animação parado (idle)
        
        self.parado = True # Estado de movimento
        self.direction = "right" # Direção inicial

        # Define a imagem inicial do jogador
        self.image = None
        if self.sprites_idle_direita and len(self.sprites_idle_direita) > 0: self.image = self.sprites_idle_direita[0]
        elif self.sprites_idle_esquerda and len(self.sprites_idle_esquerda) > 0: self.image = self.sprites_idle_esquerda[0]
        elif self.sprites_direita and len(self.sprites_direita) > 0: self.image = self.sprites_direita[0] # Fallback para sprite de movimento
        elif self.sprites_esquerda and len(self.sprites_esquerda) > 0: self.image = self.sprites_esquerda[0]
        else: # Fallback extremo: cria um placeholder se nenhum sprite for carregado
            self.image = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
            self.image.fill((255,0,255, 150)) # Magenta semi-transparente
            print("ALERTA(Player Init): Nenhum sprite carregado para o jogador. Usando placeholder.")

        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
        # Rect de colisão menor que o rect da imagem
        self.rect_colisao = self.rect.inflate(-30, -20) 

        self.tempo_animacao = 100 # Intervalo entre frames de animação do jogador (ms)
        self.ultimo_update = pygame.time.get_ticks() # Para controle de tempo da animação

        # Gerenciamento da arma
        self.current_weapon: Weapon = None
        self.tempo_ultimo_ataque = 0.0 # Usado para cooldown do ataque (time.time())

        # Tenta equipar uma arma inicial (AdagaFogo)
        if 'AdagaFogo' in globals() and AdagaFogo is not None: # Verifica se AdagaFogo foi importada
            try:
                self.current_weapon = AdagaFogo() # Tenta instanciar
                print(f"DEBUG(Player Init): Arma inicial '{self.current_weapon.name}' instanciada.")
            except Exception as e_init_weapon:
                self.current_weapon = None
                print(f"ERRO(Player Init): Falha ao instanciar AdagaFogo inicial: {e_init_weapon}")
        else:
            print("ALERTA(Player Init): Classe AdagaFogo não disponível para arma inicial.")
        
        # Estado de ataque
        self.is_attacking = False # Flag geral se está na lógica de ataque
        self.is_attacking_animation_active = False # Flag se a animação da arma está ativa
        self.attack_duration = 0.3 # Duração da animação de ataque em segundos (pode ser da arma)
        self.attack_timer = 0.0 # Timer para controlar a duração da animação de ataque (time.time())

        self.attack_hitbox = pygame.Rect(0,0,0,0) # Hitbox do ataque atual
        self.hit_enemies_this_attack = set() # Para garantir que cada inimigo seja atingido uma vez por swing
        
        self.owned_weapons = [] # Lista de armas que o jogador possui
        if self.current_weapon: # Adiciona a arma inicial à lista de possuídas, se foi equipada
            self.owned_weapons.append(self.current_weapon)

        # Controle de invencibilidade
        self.pode_levar_dano = True # Se o jogador pode receber dano
        self.tempo_ultimo_dano_levado = 0 # pygame.time.get_ticks()
        self.duracao_invencibilidade_ms = 500 # Meio segundo de invencibilidade
        self.is_invencivel_piscando = False # Se o efeito de piscar está ativo
        self.tempo_para_proximo_pisca_dano = 0 
        self.intervalo_pisca_dano_ms = 80 # Pisca mais rápido
        self.visivel_durante_pisca_dano = True # Estado atual do pisca-pisca

    @property
    def dano(self) -> float:
        return self.current_weapon.damage if self.current_weapon else 0.0

    @property
    def alcance_ataque(self) -> float:
        return self.current_weapon.attack_range if self.current_weapon else 0.0

    @property
    def cooldown_ataque(self) -> float:
        """Retorna o cooldown da arma atual em segundos."""
        return self.current_weapon.cooldown if self.current_weapon else 0.5 # Cooldown padrão de 0.5s se sem arma

    @property
    def level(self) -> int:
        return self.xp_manager.level if self.xp_manager and hasattr(self.xp_manager, 'level') else 1

    def equip_weapon(self, weapon_object: Weapon):
        if Weapon is None: 
            print("ALERTA(Player.equip_weapon): Classe base Weapon não está disponível (importação falhou?).")
            return
        if isinstance(weapon_object, Weapon):
            self.current_weapon = weapon_object
            self.tempo_ultimo_ataque = time.time() # Reseta o timer de cooldown ao equipar
            print(f"DEBUG(Player.equip_weapon): Arma '{self.current_weapon.name}' equipada.")
        else:
            print(f"ALERTA(Player.equip_weapon): Tentativa de equipar objeto inválido: {type(weapon_object)}. Esperava-se um objeto Weapon.")

    def add_owned_weapon(self, weapon_object: Weapon) -> bool:
        """Adiciona uma arma ao inventário do jogador. Retorna True se bem sucedido."""
        if Weapon is None: return False # Classe base não carregada
        if not isinstance(weapon_object, Weapon): 
            print(f"ALERTA(Player.add_owned_weapon): Tentativa de adicionar objeto inválido: {type(weapon_object)}")
            return False
        
        # Verifica se já possui uma arma com o mesmo nome base
        # As classes de armas devem ter um atributo '_base_name' para esta verificação funcionar corretamente
        # Ex: AdagaFogo Nível 1 e AdagaFogo Nível 2 teriam o mesmo _base_name "AdagaFogo"
        if hasattr(weapon_object, '_base_name'):
            if any(hasattr(w, '_base_name') and w._base_name == weapon_object._base_name for w in self.owned_weapons if w is not None):
                print(f"DEBUG(Player.add_owned_weapon): Arma '{weapon_object.name}' (ou uma versão dela com base_name '{weapon_object._base_name}') já está no inventário.")
                return False # Já possui esta "linhagem" de arma
        elif any(type(w) is type(weapon_object) for w in self.owned_weapons if w is not None): # Fallback: verifica por tipo exato se _base_name não existir
             print(f"DEBUG(Player.add_owned_weapon): Arma do tipo '{type(weapon_object).__name__}' já está no inventário (verificação por tipo).")
             return False


        # Lógica para adicionar a arma (substitui None ou adiciona se houver espaço)
        # Mantém um máximo de 3 armas no inventário rápido (owned_weapons)
        if None in self.owned_weapons:
            idx = self.owned_weapons.index(None)
            self.owned_weapons[idx] = weapon_object
        elif len(self.owned_weapons) < 3:
            self.owned_weapons.append(weapon_object)
        else:
            print(f"DEBUG(Player.add_owned_weapon): Inventário de armas rápido cheio (3/3). Não foi possível adicionar '{weapon_object.name}'.")
            return False # Inventário cheio

        print(f"DEBUG(Player.add_owned_weapon): Arma '{weapon_object.name}' adicionada ao inventário.")
        if not self.current_weapon: # Se não tinha nenhuma arma equipada, equipa a nova
            self.equip_weapon(weapon_object)
        return True

    def _carregar_sprites(self, caminhos, tamanho, nome_conjunto):
        sprites = []
        # Assume que player.py está em uma subpasta (ex: 'Codigo') e 'Sprites' está na raiz do projeto
        base_dir_script = os.path.dirname(os.path.abspath(__file__)) # Diretório de player.py
        project_root = os.path.dirname(base_dir_script) # Sobe um nível para a raiz do projeto

        for path_relativo_ao_projeto in caminhos: # 'path' deve ser tipo "Sprites/Asrahel/Esquerda/Ashael_E1.png"
            full_path = os.path.join(project_root, path_relativo_ao_projeto.replace("/", os.sep))
            
            if not os.path.exists(full_path):
                print(f"ALERTA(Player._carregar_sprites): Sprite para '{nome_conjunto}' não encontrado: {full_path}")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                placeholder.fill((255,0,255, 100)) # Magenta placeholder
                sprites.append(placeholder)
                continue
            try:
                sprite = pygame.image.load(full_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, tamanho)
                sprites.append(sprite)
            except pygame.error as e:
                print(f"DEBUG(Player._carregar_sprites): Erro ao carregar sprite '{full_path}' para '{nome_conjunto}': {e}")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                placeholder.fill((255,0,255, 100))
                sprites.append(placeholder)
        
        if not sprites: # Se, por algum motivo, a lista estiver vazia após o loop
            print(f"ALERTA GRAVE(Player._carregar_sprites): Nenhum sprite carregado para '{nome_conjunto}'. Adicionando placeholder único.")
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            placeholder.fill((255,0,0, 150)) # Vermelho para destacar falha crítica
            sprites.append(placeholder)
        return sprites

    def receber_dano(self, dano, _fonte_dano_rect=None): # _fonte_dano_rect opcional
        if self.vida is not None and self.pode_levar_dano: 
            self.vida.receber_dano(dano) 
            
            self.pode_levar_dano = False 
            self.tempo_ultimo_dano_levado = pygame.time.get_ticks()
            self.is_invencivel_piscando = True 
            self.visivel_durante_pisca_dano = False # Começa invisível
            self.tempo_para_proximo_pisca_dano = self.tempo_ultimo_dano_levado + self.intervalo_pisca_dano_ms
            
            if not self.esta_vivo():
                print("DEBUG(Player): Jogador morreu.")
            # else:
                # print(f"DEBUG(Player): Jogador recebeu {dano} de dano. Invencibilidade ativada.") # Comentado para reduzir spam

    def update(self, dt_ms=None, teclas_pressionadas=None): # Adicionado dt_ms e teclas para uso futuro se necessário
        agora_ticks = pygame.time.get_ticks()
        agora_time = time.time() # Para cooldown de ataque baseado em time.time()

        # Lógica de invencibilidade e piscar
        if self.is_invencivel_piscando:
            if agora_ticks >= self.tempo_para_proximo_pisca_dano:
                self.visivel_durante_pisca_dano = not self.visivel_durante_pisca_dano 
                self.tempo_para_proximo_pisca_dano = agora_ticks + self.intervalo_pisca_dano_ms
            
            if agora_ticks - self.tempo_ultimo_dano_levado > self.duracao_invencibilidade_ms:
                self.pode_levar_dano = True
                self.is_invencivel_piscando = False
                self.visivel_durante_pisca_dano = True 

        # Lógica para finalizar a animação de ataque
        if self.is_attacking_animation_active and (agora_time - self.attack_timer >= self.attack_duration):
            self.is_attacking = False 
            self.is_attacking_animation_active = False 
            self.attack_hitbox.size = (0,0) # Reseta a hitbox
            self.hit_enemies_this_attack.clear()
            if self.current_weapon and hasattr(self.current_weapon, 'current_attack_animation_frame'):
                self.current_weapon.current_attack_animation_frame = 0 # Reseta frame da animação da arma

        # Animação do jogador (idle ou movimento)
        if agora_ticks - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora_ticks
            active_sprites_list = []
            if self.parado:
                if self.direction == "left": active_sprites_list = self.sprites_idle_esquerda
                else: active_sprites_list = self.sprites_idle_direita # Default para direita se não esquerda
                
                if active_sprites_list: # Garante que a lista não está vazia
                    self.frame_idle = (self.frame_idle + 1) % len(active_sprites_list)
                    self.image = active_sprites_list[self.frame_idle]
                # Fallback se listas idle específicas estiverem vazias mas as de movimento não
                elif self.direction == "left" and self.sprites_esquerda: self.image = self.sprites_esquerda[0]
                elif self.sprites_direita: self.image = self.sprites_direita[0]

            else: # Movendo-se
                if self.direction == "left": active_sprites_list = self.sprites_esquerda
                else: active_sprites_list = self.sprites_direita

                if active_sprites_list:
                    self.atual = (self.atual + 1) % len(active_sprites_list)
                    self.image = active_sprites_list[self.atual]
        
        # Animação da arma (se estiver atacando)
        if self.is_attacking_animation_active and self.current_weapon and \
           hasattr(self.current_weapon, 'attack_animation_sprites') and self.current_weapon.attack_animation_sprites and \
           hasattr(self.current_weapon, 'attack_animation_speed') and hasattr(self.current_weapon, 'last_attack_animation_update') and \
           hasattr(self.current_weapon, 'current_attack_animation_frame'):
            
            if agora_ticks - self.current_weapon.last_attack_animation_update > self.current_weapon.attack_animation_speed:
                self.current_weapon.last_attack_animation_update = agora_ticks
                num_frames_arma = len(self.current_weapon.attack_animation_sprites)
                if num_frames_arma > 0 : 
                    self.current_weapon.current_attack_animation_frame = \
                        (self.current_weapon.current_attack_animation_frame + 1) % num_frames_arma
        
        # Fallback final para self.image se ainda for None
        if self.image is None: 
            self.image = pygame.Surface((60,60), pygame.SRCALPHA); self.image.fill((255,0,255,100))

        # Atualiza rects
        self.rect.center = (round(self.x), round(self.y))
        if hasattr(self, 'rect_colisao'): 
            self.rect_colisao.center = self.rect.center

    def mover(self, teclas, arvores): # arvores é uma lista de sprites de obstáculos
        if not hasattr(self, 'rect_colisao'): # Precisa do rect de colisão para mover
            return

        current_dx, current_dy = 0.0, 0.0
        
        move_left = teclas[pygame.K_LEFT] or teclas[pygame.K_a]
        move_right = teclas[pygame.K_RIGHT] or teclas[pygame.K_d]
        move_up = teclas[pygame.K_UP] or teclas[pygame.K_w]
        move_down = teclas[pygame.K_DOWN] or teclas[pygame.K_s]

        if move_left and not move_right: current_dx = -self.velocidade; self.direction = "left"
        elif move_right and not move_left: current_dx = self.velocidade; self.direction = "right"
        
        if move_up and not move_down: current_dy = -self.velocidade
        elif move_down and not move_up: current_dy = self.velocidade
        
        # Normaliza movimento diagonal
        if current_dx != 0.0 and current_dy != 0.0:
            inv_sqrt2 = 1.0 / math.sqrt(2) # Aproximadamente 0.7071
            current_dx *= inv_sqrt2 
            current_dy *= inv_sqrt2
        
        self.parado = not (current_dx != 0.0 or current_dy != 0.0)
        
        # Movimento e Colisão no eixo X
        self.x += current_dx
        self.rect_colisao.centerx = round(self.x) # Atualiza rect_colisao para a nova posição X
        if arvores and current_dx != 0: # Só checa colisão X se houve movimento X
            for arvore in arvores:
                arvore_col_rect = getattr(arvore, 'rect_colisao', getattr(arvore, 'rect', None))
                if arvore_col_rect and self.rect_colisao.colliderect(arvore_col_rect):
                    if current_dx > 0: self.rect_colisao.right = arvore_col_rect.left # Movendo para direita, colidiu
                    elif current_dx < 0: self.rect_colisao.left = arvore_col_rect.right # Movendo para esquerda, colidiu
                    self.x = float(self.rect_colisao.centerx) # Ajusta posição x baseada na colisão
                    break 
        
        # Movimento e Colisão no eixo Y
        self.y += current_dy
        self.rect_colisao.centery = round(self.y) # Atualiza rect_colisao para a nova posição Y
        if arvores and current_dy != 0: # Só checa colisão Y se houve movimento Y
            for arvore in arvores:
                arvore_col_rect = getattr(arvore, 'rect_colisao', getattr(arvore, 'rect', None))
                if arvore_col_rect and self.rect_colisao.colliderect(arvore_col_rect):
                    if current_dy > 0: self.rect_colisao.bottom = arvore_col_rect.top # Movendo para baixo, colidiu
                    elif current_dy < 0: self.rect_colisao.top = arvore_col_rect.bottom # Movendo para cima, colidiu
                    self.y = float(self.rect_colisao.centery) # Ajusta posição y baseada na colisão
                    break
        
        # Atualiza o rect principal do jogador com base nas posições x,y finais (após colisões)
        if hasattr(self, 'rect'): self.rect.center = (round(self.x), round(self.y))


    def atacar(self, inimigos, dt_ms=None): # dt_ms opcional, pode ser usado para ataques carregados, etc.
        current_time = time.time() # Usar time.time() para cooldowns baseados em tempo real
        if self.current_weapon and not self.is_attacking_animation_active and \
           (current_time - self.tempo_ultimo_ataque >= self.cooldown_ataque):
            
            self.is_attacking = True 
            self.is_attacking_animation_active = True 
            
            self.attack_timer = current_time # Início da animação de ataque
            self.tempo_ultimo_ataque = current_time # Reseta cooldown
            self.hit_enemies_this_attack.clear() # Limpa lista de inimigos atingidos neste ataque
            
            # Define a hitbox do ataque
            hitbox_w = self.current_weapon.hitbox_width
            hitbox_h = self.current_weapon.hitbox_height
            offset_x_arma = self.current_weapon.hitbox_offset_x 
            offset_y_arma = self.current_weapon.hitbox_offset_y 
            
            self.attack_hitbox = pygame.Rect(0, 0, hitbox_w, hitbox_h)

            # Calcula o centro da hitbox baseado na direção do jogador e offsets da arma
            if self.direction == "right":
                hitbox_center_x = self.rect.centerx + offset_x_arma 
            else: # "left"
                hitbox_center_x = self.rect.centerx - offset_x_arma 
            
            hitbox_center_y = self.rect.centery + offset_y_arma
            self.attack_hitbox.center = (round(hitbox_center_x), round(hitbox_center_y))

            # Inicia a animação de ataque da arma (se houver)
            if hasattr(self.current_weapon, 'attack_animation_sprites') and self.current_weapon.attack_animation_sprites:
                # Garante que os atributos de animação da arma existem
                if not hasattr(self.current_weapon, 'current_attack_animation_frame'): 
                    self.current_weapon.current_attack_animation_frame = 0
                if not hasattr(self.current_weapon, 'last_attack_animation_update'): 
                    self.current_weapon.last_attack_animation_update = 0
                    
                self.current_weapon.current_attack_animation_frame = 0 # Começa do primeiro frame
                self.current_weapon.last_attack_animation_update = pygame.time.get_ticks() # Usa ticks para animação visual

        # Verifica colisão do ataque com inimigos (somente se o ataque foi iniciado neste frame ou ainda está ativo)
        if self.is_attacking and self.attack_hitbox.width > 0: 
            if inimigos:
                for inimigo in list(inimigos): # Itera sobre cópia se a lista puder mudar
                    if inimigo and hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo() and \
                       hasattr(inimigo, 'rect') and inimigo.rect is not None:
                        
                        inimigo_colisao_rect = getattr(inimigo, 'rect_colisao', inimigo.rect) # Usa rect_colisao se disponível
                        
                        if self.attack_hitbox.colliderect(inimigo_colisao_rect) and \
                           inimigo not in self.hit_enemies_this_attack: # Atinge cada inimigo uma vez por "swing"
                            
                            if hasattr(inimigo, 'receber_dano'):
                                inimigo.receber_dano(self.dano, self.rect) # Passa o rect do jogador como fonte
                                self.hit_enemies_this_attack.add(inimigo)
                                
                                if not inimigo.esta_vivo(): # Se o inimigo morreu
                                    if hasattr(inimigo, 'xp_value') and self.xp_manager and \
                                       hasattr(self.xp_manager, 'gain_xp'):
                                        self.xp_manager.gain_xp(inimigo.xp_value)

    def empurrar_jogador(self, obstaculo_rect):
        """Método placeholder para lógica de empurrão se necessário."""
        # Esta lógica pode ser complexa e depender da natureza do empurrão.
        # Por ora, o sistema de colisão em mover() impede a sobreposição.
        pass 

    def desenhar(self, janela, camera_x, camera_y):
        # Desenha o jogador
        if self.image is not None and hasattr(self, 'rect'):
            if self.is_invencivel_piscando and not self.visivel_durante_pisca_dano:
                pass # Não desenha o jogador se estiver na fase "invisível" do pisca-pisca
            else:
                janela.blit(self.image, (round(self.rect.x - camera_x), round(self.rect.y - camera_y)))

        # Desenha a animação de ataque da ARMA ATUAL
        if self.is_attacking_animation_active and self.current_weapon and \
           hasattr(self.current_weapon, 'get_current_attack_animation_sprite') and \
           callable(self.current_weapon.get_current_attack_animation_sprite):
            
            attack_sprite_visual = self.current_weapon.get_current_attack_animation_sprite()
            
            if attack_sprite_visual and isinstance(attack_sprite_visual, pygame.Surface):
                sprite_to_draw = attack_sprite_visual.copy() # Copia para não modificar o original da arma
                if self.direction == "left": # Espelha a animação da arma
                    sprite_to_draw = pygame.transform.flip(sprite_to_draw, True, False)
                
                # Posiciona a animação da arma. Pode precisar de ajuste fino baseado no design da arma.
                # Aqui, centraliza na attack_hitbox (que já considera a direção e offsets).
                attack_sprite_rect = sprite_to_draw.get_rect(center=self.attack_hitbox.center)
                
                janela.blit(sprite_to_draw, (round(attack_sprite_rect.x - camera_x), 
                                             round(attack_sprite_rect.y - camera_y)))
            # elif self.current_weapon: # Debug se o sprite não for válido
                # print(f"ALERTA(Player.desenhar): Arma {self.current_weapon.name} não retornou Surface válida para animação de ataque.")

    def esta_vivo(self):
        if self.vida is not None and hasattr(self.vida, 'esta_vivo'):
            return self.vida.esta_vivo()
        print("ALERTA(Player.esta_vivo): Objeto Vida não encontrado ou sem método esta_vivo(). Retornando False.")
        return False # Assume morto se não houver sistema de vida
    
    def adicionar_item_inventario(self, item_da_loja_dict) -> bool:
        """Adiciona uma arma ao inventário com base em um item comprado na loja."""
        if not isinstance(item_da_loja_dict, dict):
            print("ALERTA(Player.adicionar_item_inventario): item_da_loja_dict não é um dicionário.")
            return False

        nome_item = item_da_loja_dict.get("nome")
        if not nome_item: 
            print("ALERTA(Player.adicionar_item_inventario): Item da loja sem chave 'nome'.")
            return False
        
        WeaponClass = self.SHOP_ITEM_TO_WEAPON_CLASS.get(nome_item) # Case-sensitive
        if WeaponClass is not None: # Garante que a classe existe e não é None (importada com sucesso)
            try:
                nova_arma = WeaponClass() 
                # print(f"DEBUG(Player.adicionar_item_inventario): Instanciando '{nova_arma.name}' (Classe: {WeaponClass.__name__}) da loja.")
                return self.add_owned_weapon(nova_arma) # Usa a lógica de add_owned_weapon
            except Exception as e: 
                print(f"ERRO(Player.adicionar_item_inventario): Erro ao instanciar '{nome_item}' da classe {WeaponClass.__name__ if WeaponClass else 'N/A'}: {e}")
        else: 
            print(f"ALERTA(Player.adicionar_item_inventario): Nenhuma classe de arma mapeada para o item da loja '{nome_item}'. Verifique SHOP_ITEM_TO_WEAPON_CLASS_MAP.")
        return False
            
    def evoluir_arma_atual(self, mapa_evolucoes_nivel_atual: dict) -> str | None:
        """Evolui a arma equipada atualmente.
        mapa_evolucoes_nivel_atual: dict onde chave é nome da arma atual, valor é a Classe da arma evoluída.
        Retorna o nome da nova arma se evoluiu, None caso contrário.
        """
        if not self.current_weapon: 
            print("ALERTA(Player.evoluir_arma_atual): Nenhuma arma equipada para evoluir.")
            return None
        if not isinstance(mapa_evolucoes_nivel_atual, dict):
            print("ALERTA(Player.evoluir_arma_atual): mapa_evolucoes_nivel_atual não é um dicionário.")
            return None

        # Usa o nome base da arma para a chave do mapa de evoluções, se disponível
        # Isso permite que "Adaga Nv1" e "Adaga Nv2" usem a mesma entrada "Adaga" para encontrar a evolução.
        # As classes de arma devem definir `_base_name`.
        chave_evolucao = getattr(self.current_weapon, '_base_name', self.current_weapon.name)
        
        NovaClasseArmaEvoluida = mapa_evolucoes_nivel_atual.get(chave_evolucao)

        if NovaClasseArmaEvoluida is not None: # Garante que a classe da evolução existe e foi importada
            try:
                nova_arma_evoluida_inst = NovaClasseArmaEvoluida()
                
                arma_antiga_instancia = self.current_weapon # Guarda referência à arma antiga
                self.equip_weapon(nova_arma_evoluida_inst) # Equipa a nova arma
                
                # Tenta substituir a arma antiga na lista de armas possuídas
                try:
                    idx_antiga = self.owned_weapons.index(arma_antiga_instancia)
                    self.owned_weapons[idx_antiga] = nova_arma_evoluida_inst
                except ValueError: 
                    # Se a arma antiga não estava em owned_weapons (improvável se estava equipada),
                    # ou se a lista é gerenciada de forma diferente. Tenta adicionar a nova.
                    print(f"ALERTA(Player.evoluir_arma_atual): Arma antiga '{getattr(arma_antiga_instancia, 'name', 'N/A')}' não encontrada em owned_weapons para substituição. Tentando adicionar a nova.")
                    if not self.add_owned_weapon(nova_arma_evoluida_inst):
                         # Se não conseguiu adicionar (ex: inventário cheio), o jogador ainda tem a nova arma equipada,
                         # mas ela não estará formalmente na lista 'owned_weapons'.
                         print(f"ALERTA(Player.evoluir_arma_atual): Não foi possível adicionar '{nova_arma_evoluida_inst.name}' a owned_weapons após evolução, mas está equipada.")
                
                print(f"DEBUG(Player.evoluir_arma_atual): Arma '{getattr(arma_antiga_instancia, 'name', 'N/A')}' evoluiu para '{nova_arma_evoluida_inst.name}'.")
                return nova_arma_evoluida_inst.name
            except Exception as e: 
                print(f"ERRO(Player.evoluir_arma_atual): Erro ao instanciar evolução '{NovaClasseArmaEvoluida.__name__ if NovaClasseArmaEvoluida else 'N/A'}' para '{chave_evolucao}': {e}")
        else:
            print(f"DEBUG(Player.evoluir_arma_atual): Nenhuma evolução definida para '{chave_evolucao}' no mapa fornecido ou a classe de evolução é None.")
        return None