# player.py
import pygame
import random
import math
import os
import time

from vida import Vida
from Armas.weapon import Weapon

# Tenta importar todas as classes de armas com seus novos nomes
# Certifique-se de que estes imports estão corretos para a sua estrutura de pastas
try:
    from Armas.EspadaBrasas import EspadaBrasas
except ImportError:
    print("DEBUG(Player): Aviso: Módulo 'Armas/EspadaBrasas.py' não encontrado.")
    EspadaBrasas = None
try:
    from Armas.MachadoCeruleo import MachadoCeruleo
except ImportError:
    print("DEBUG(Player): Aviso: Módulo 'Armas/MachadoCeruleo.py' não encontrado.")
    MachadoCeruleo = None
try:
    from Armas.MachadoMacabro import MachadoMacabro
except ImportError:
    print("DEBUG(Player): Aviso: Módulo 'Armas/MachadoMacabro.py' não encontrado.")
    MachadoMacabro = None
try:
    from Armas.MachadoMarfim import MachadoMarfim
except ImportError:
    print("DEBUG(Player): Aviso: Módulo 'Armas/MachadoMarfim.py' não encontrado.")
    MachadoMarfim = None
try:
    from Armas.MachadoBarbaro import MachadoBarbaro
except ImportError:
    print("DEBUG(Player): Aviso: Módulo 'Armas/MachadoBarbaro.py' não encontrado.")
    MachadoBarbaro = None
try:
    from Armas.AdagaFogo import AdagaFogo
except ImportError:
    print("DEBUG(Player): Aviso: Módulo 'Armas/AdagaFogo.py' não encontrado.")
    AdagaFogo = None
try:
    from Armas.EspadaFogoAzul import EspadaFogoAzul
except ImportError:
    print("DEBUG(Player): Aviso: Módulo 'Armas/EspadaFogoAzul.py' não encontrado.")
    EspadaFogoAzul = None
try:
    from Armas.EspadaLua import EspadaLua
except ImportError:
    print("DEBUG(Player): Aviso: Módulo 'Armas/EspadaLua.py' não encontrado.")
    EspadaLua = None
try:
    from Armas.EspadaCaida import EspadaCaida
except ImportError:
    print("DEBUG(Player): Aviso: Módulo 'Armas/EspadaCaida.py' não encontrado.")
    EspadaCaida = None
try:
    from Armas.EspadaPenitencia import EspadaPenitencia
except ImportError:
    print("DEBUG(Player): Aviso: Módulo 'Armas/EspadaPenitencia.py' não encontrado.")
    EspadaPenitencia = None


class Player(pygame.sprite.Sprite):
    """
    Classe que representa o jogador no jogo.
    Gerencia movimento, animações, vida, a arma equipada.
    O sistema de experiência e nivelamento é gerenciado pelo XPManager.
    """
    def __init__(self, velocidade=5, vida_maxima=150):
        super().__init__()

        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)

        self.velocidade = velocidade
        self.vida = Vida(vida_maxima) if Vida is not None else None
        if self.vida is None:
            print("DEBUG(Player): Erro: Classe Vida não disponível. Vida do jogador não funcionará corretamente.")

        # --- Referência ao XPManager (será definida após a criação do Player e XPManager) ---
        self.xp_manager = None 
        # --- Fim da Referência ao XPManager ---

        # --- Carregamento e Escalonamento dos Sprites ---
        tamanho_sprite_desejado = (60, 60)

        # Sprites de animação de movimento (Esquerda)
        caminhos_esquerda = [
            "Sprites/Asrahel/Esquerda/Ashael_E1.png", "Sprites/Asrahel/Esquerda/Ashael_E2.png",
            "Sprites/Asrahel/Esquerda/Ashael_E3.png", "Sprites/Asrahel/Esquerda/Ashael_E4.png",
            "Sprites/Asrahel/Esquerda/Ashael_E5.png", "Sprites/Asrahel/Esquerda/Ashael_E6.png",
        ]
        self.sprites_esquerda = self._carregar_sprites(caminhos_esquerda, tamanho_sprite_desejado, "Esquerda")

        # Sprites de animação de idle (Esquerda)
        caminhos_idle_esquerda = ["Sprites/Asrahel/Esquerda/Ashael_E1.png"]
        self.sprites_idle_esquerda = self._carregar_sprites(caminhos_idle_esquerda, tamanho_sprite_desejado, "Idle Esquerda")

        # Sprites de animação de movimento (Direita)
        caminhos_direita = [
            "Sprites/Asrahel/Direita/Ashael_D1.png", "Sprites/Asrahel/Direita/Ashael_D2.png",
            "Sprites/Asrahel/Direita/Ashael_D3.png", "Sprites/Asrahel/Direita/Ashael_D4.png",
            "Sprites/Asrahel/Direita/Ashael_D5.png", "Sprites/Asrahel/Direita/Ashael_D6.png",
        ]
        self.sprites_direita = self._carregar_sprites(caminhos_direita, tamanho_sprite_desejado, "Direita")

        # Sprites de animação de idle (Direita)
        caminhos_idle_direita = ["Sprites/Asrahel/Direita/Ashael_D1.png"]
        self.sprites_idle_direita = self._carregar_sprites(caminhos_idle_direita, tamanho_sprite_desejado, "Idle Direita")

        # NOVOS SPRITES DE ANIMAÇÃO DE ATAQUE POR NÍVEL
        # Nível 1 (e 1.5)
        caminhos_ataque_direita_nivel1 = [
            "Sprites/Asrahel/Ataque/Direita/Nivel1/Ashael_AD1.png",
            "Sprites/Asrahel/Ataque/Direita/Nivel1/Ashael_AD2.png",
            "Sprites/Asrahel/Ataque/Direita/Nivel1/Ashael_AD3.png",
            "Sprites/Asrahel/Ataque/Direita/Nivel1/Ashael_AD4.png",
        ]
        self.sprites_ataque_direita_nivel1 = self._carregar_sprites(caminhos_ataque_direita_nivel1, tamanho_sprite_desejado, "Ataque Dir Nv1")

        caminhos_ataque_esquerda_nivel1 = [
            "Sprites/Asrahel/Ataque/Esquerda/Nivel1/Ashael_AE1.png",
            "Sprites/Asrahel/Ataque/Esquerda/Nivel1/Ashael_AE2.png",
            "Sprites/Asrahel/Ataque/Esquerda/Nivel1/Ashael_AE3.png",
            "Sprites/Asrahel/Ataque/Esquerda/Nivel1/Ashael_AE4.png",
        ]
        self.sprites_ataque_esquerda_nivel1 = self._carregar_sprites(caminhos_ataque_esquerda_nivel1, tamanho_sprite_desejado, "Ataque Esq Nv1")

        # Nível 2 (e 2.5)
        caminhos_ataque_direita_nivel2 = [
            "Sprites/Asrahel/Ataque/Direita/Nivel2/Ashael_AD2_Nv2.png",
            "Sprites/Asrahel/Ataque/Direita/Nivel2/Ashael_AD2_Nv2_2.png",
            "Sprites/Asrahel/Ataque/Direita/Nivel2/Ashael_AD2_Nv2_3.png",
        ]
        self.sprites_ataque_direita_nivel2 = self._carregar_sprites(caminhos_ataque_direita_nivel2, tamanho_sprite_desejado, "Ataque Dir Nv2")

        caminhos_ataque_esquerda_nivel2 = [
            "Sprites/Asrahel/Ataque/Esquerda/Nivel2/Ashael_AE2_Nv2.png",
            "Sprites/Asrahel/Ataque/Esquerda/Nivel2/Ashael_AE2_Nv2_2.png",
            "Sprites/Asrahel/Ataque/Esquerda/Nivel2/Ashael_AE2_Nv2_3.png",
        ]
        self.sprites_ataque_esquerda_nivel2 = self._carregar_sprites(caminhos_ataque_esquerda_nivel2, tamanho_sprite_desejado, "Ataque Esq Nv2")

        # Nível 3
        caminhos_ataque_direita_nivel3 = [
            "Sprites/Asrahel/Ataque/Direita/Nivel3/Ashael_AD3_Nv3.png",
            "Sprites/Asrahel/Ataque/Direita/Nivel3/Ashael_AD3_Nv3_2.png",
            "Sprites/Asrahel/Ataque/Direita/Nivel3/Ashael_AD3_Nv3_3.png",
            "Sprites/Asrahel/Ataque/Direita/Nivel3/Ashael_AD3_Nv3_4.png",
        ]
        self.sprites_ataque_direita_nivel3 = self._carregar_sprites(caminhos_ataque_direita_nivel3, tamanho_sprite_desejado, "Ataque Dir Nv3")

        caminhos_ataque_esquerda_nivel3 = [
            "Sprites/Asrahel/Ataque/Esquerda/Nivel3/Ashael_AE3_Nv3.png",
            "Sprites/Asrahel/Ataque/Esquerda/Nivel3/Ashael_AE3_Nv3_2.png",
            "Sprites/Asrahel/Ataque/Esquerda/Nivel3/Ashael_AE3_Nv3_3.png",
            "Sprites/Asrahel/Ataque/Esquerda/Nivel3/Ashael_AE3_Nv3_4.png",
        ]
        self.sprites_ataque_esquerda_nivel3 = self._carregar_sprites(caminhos_ataque_esquerda_nivel3, tamanho_sprite_desejado, "Ataque Esq Nv3")


        # Define o sprite inicial e o retângulo de colisão
        self.atual = 0
        self.frame_idle = 0
        self.frame_ataque = 0
        self.parado = True
        self.direction = "right"

        self.image = None
        if self.sprites_idle_direita:
            self.image = self.sprites_idle_direita[self.frame_idle % len(self.sprites_idle_direita)]
        elif self.sprites_idle_esquerda:
            self.image = self.sprites_idle_esquerda[self.frame_idle % len(self.sprites_idle_esquerda)]
        elif self.sprites_direita:
            self.image = self.sprites_direita[0]
        elif self.sprites_esquerda:
            self.image = self.sprites_esquerda[0]
        else:
            tamanho_sprite_desejado_fallback = (60, 60)
            self.image = pygame.Surface(tamanho_sprite_desejado_fallback, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 255), (0, 0, tamanho_sprite_desejado_fallback[0], tamanho_sprite_desejado_fallback[1]))


        if self.image is not None:
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.rect_colisao = self.rect.inflate(-30, -20)
        else:
            self.rect = pygame.Rect(self.x, self.y, 60, 60)
            self.rect_colisao = pygame.Rect(self.x, self.y, 30, 40)
            self.rect.center = (self.x, self.y)
            self.rect_colisao.center = self.rect.center
            print("DEBUG(Player): Erro: Imagem inicial do jogador não definida. Usando rects placeholders.")


        self.tempo_animacao = 100
        self.ultimo_update = pygame.time.get_ticks()
        self.ultimo_update_ataque = pygame.time.get_ticks()

        self.current_weapon: Weapon = None
        self.tempo_ultimo_ataque = 0.0

        # Inicializa com a AdagaFogo por padrão (nome do arquivo encurtado)
        if AdagaFogo is not None:
            self.equip_weapon(AdagaFogo())
        else:
            print("DEBUG(Player): Aviso: AdagaFogo não pôde ser equipada. Verifique o import.")

        self.is_attacking = False
        self.is_attacking_animation_active = False
        self.attack_duration = 0.3
        self.attack_timer = 0

        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.attack_hitbox_size = (60, 60)

        self.hit_enemies_this_attack = set()

        # Inventário de armas (para a roda de armas)
        self.owned_weapons = [] # Lista de instâncias de armas que o jogador possui

    @property
    def dano(self) -> float:
        return self.current_weapon.damage if self.current_weapon else 0.0

    @property
    def alcance_ataque(self) -> float:
        return self.current_weapon.attack_range if self.current_weapon else 0.0

    @property
    def cooldown_ataque(self) -> float:
        return self.current_weapon.cooldown if self.current_weapon else 0.0

    # Adicionado para que o XPManager possa acessar o nível atual do jogador para sprites de ataque
    @property
    def level(self) -> int:
        # Retorna o nível do XPManager se ele existir, caso contrário, retorna 1 como padrão
        return self.xp_manager.level if self.xp_manager else 1

    def equip_weapon(self, weapon_object: Weapon):
        if isinstance(weapon_object, Weapon):
            self.current_weapon = weapon_object
            print(f"DEBUG(Player): Jogador equipou: {self.current_weapon.name}")
            self.tempo_ultimo_ataque = time.time()
        else:
            print(f"DEBUG(Player): Erro: Tentativa de equipar um objeto que não é uma arma: {type(weapon_object)}")

    def add_owned_weapon(self, weapon_object: Weapon):
        """Adiciona uma arma ao inventário do jogador, se ainda não a tiver e houver espaço."""
        if not isinstance(weapon_object, Weapon):
            print(f"DEBUG(Player): Erro: Tentativa de adicionar um objeto que não é uma arma ao inventário: {type(weapon_object)}")
            return False

        # Verifica se o jogador já possui uma arma com o mesmo nome
        if any(w.name == weapon_object.name for w in self.owned_weapons):
            print(f"DEBUG(Player): Jogador já possui a arma '{weapon_object.name}'.")
            return False

        # Limite de 3 armas no inventário
        if len(self.owned_weapons) >= 3:
            print(f"DEBUG(Player): Inventário de armas cheio. Não é possível adicionar '{weapon_object.name}'.")
            return False

        self.owned_weapons.append(weapon_object)
        print(f"DEBUG(Player): Arma '{weapon_object.name}' adicionada ao inventário.")
        return True

    def _carregar_sprites(self, caminhos, tamanho, nome_conjunto):
        sprites = []
        # Obtém o diretório base do script atual (Arquivos)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Sobe um nível para o diretório "Jogo"
        game_dir = os.path.dirname(base_dir)

        for path in caminhos:
            # Constrói o caminho completo para o sprite
            full_path = os.path.join(game_dir, path.replace("/", os.sep))

            if not os.path.exists(full_path):
                print(f"DEBUG(Player): Aviso: Arquivo de sprite não encontrado: {full_path}")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255, 0, 255), (0, 0, tamanho[0], tamanho[1]))
                sprites.append(placeholder)
                continue

            try:
                sprite = pygame.image.load(full_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, tamanho)
                sprites.append(sprite)
            except pygame.error as e:
                print(f"DEBUG(Player): Erro ao carregar o sprite '{full_path}': {e}")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255, 0, 255), (0, 0, tamanho[0], tamanho[1]))
                sprites.append(placeholder)

        if not sprites:
            print(f"DEBUG(Player): Aviso: Nenhum sprite carregado para o conjunto '{nome_conjunto}'. Usando placeholder padrão.")
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (255, 0, 255), (0, 0, tamanho[0], tamanho[1]))
            sprites.append(placeholder)

        return sprites

    def receber_dano(self, dano):
        if self.vida is not None:
            self.vida.receber_dano(dano)

    # Removido: gain_xp e level_up (agora no XPManager)

    def update(self):
        agora = pygame.time.get_ticks()

        if self.is_attacking and time.time() - self.attack_timer >= self.attack_duration:
            self.is_attacking = False
            self.is_attacking_animation_active = False
            self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
            self.hit_enemies_this_attack.clear()

        if self.is_attacking_animation_active:
            current_attack_sprites_right = []
            current_attack_sprites_left = []

            # Usa o nível do XPManager para determinar os sprites de ataque
            player_level = self.level 

            if player_level >= 3:
                current_attack_sprites_right = self.sprites_ataque_direita_nivel3
                current_attack_sprites_left = self.sprites_ataque_esquerda_nivel3
            elif player_level >= 2:
                current_attack_sprites_right = self.sprites_ataque_direita_nivel2
                current_attack_sprites_left = self.sprites_ataque_esquerda_nivel2
            else: # Nível 1 ou inferior
                current_attack_sprites_right = self.sprites_ataque_direita_nivel1
                current_attack_sprites_left = self.sprites_ataque_esquerda_nivel1
            
            # Fallback caso os sprites específicos de nível não existam
            if not current_attack_sprites_right and self.sprites_ataque_direita_nivel1:
                current_attack_sprites_right = self.sprites_ataque_direita_nivel1
            if not current_attack_sprites_left and self.sprites_ataque_esquerda_nivel1:
                current_attack_sprites_left = self.sprites_ataque_esquerda_nivel1


            if agora - self.ultimo_update_ataque > self.tempo_animacao:
                self.ultimo_update_ataque = agora
                if self.direction == "right" and current_attack_sprites_right:
                    self.frame_ataque = (self.frame_ataque + 1) % len(current_attack_sprites_right)
                    self.image = current_attack_sprites_right[self.frame_ataque]
                elif self.direction == "left" and current_attack_sprites_left:
                    self.frame_ataque = (self.frame_ataque + 1) % len(current_attack_sprites_left)
                    self.image = current_attack_sprites_left[self.frame_ataque]
                else:
                    if self.direction == "right" and self.sprites_direita:
                        self.image = self.sprites_direita[self.atual]
                    elif self.direction == "left" and self.sprites_esquerda:
                        self.image = self.sprites_esquerda[self.atual]
                    else:
                        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)

        else:
            if agora - self.ultimo_update > self.tempo_animacao:
                self.ultimo_update = agora
                if self.parado:
                    if self.direction == "left" and self.sprites_idle_esquerda:
                        self.frame_idle = (self.frame_idle + 1) % len(self.sprites_idle_esquerda)
                        self.image = self.sprites_idle_esquerda[self.frame_idle]
                    elif self.direction == "right" and self.sprites_idle_direita:
                        self.frame_idle = (self.frame_idle + 1) % len(self.sprites_idle_direita)
                        self.image = self.sprites_idle_direita[self.frame_idle]
                    elif self.sprites_idle_esquerda:
                        self.frame_idle = (self.frame_idle + 1) % len(self.sprites_idle_esquerda)
                        self.image = self.sprites_idle_esquerda[self.frame_idle]
                    elif self.sprites_idle_direita:
                        self.frame_idle = (self.frame_idle + 1) % len(self.sprites_idle_direita)
                        self.image = self.sprites_idle_direita[self.frame_idle]
                    elif self.sprites_esquerda:
                        self.image = self.sprites_esquerda[0]
                    else:
                        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)

                else:
                    if self.direction == "left" and self.sprites_esquerda:
                        self.atual = (self.atual + 1) % len(self.sprites_esquerda)
                        self.image = self.sprites_esquerda[self.atual]
                    elif self.direction == "right" and self.sprites_direita:
                        self.atual = (self.atual + 1) % len(self.sprites_direita)
                        self.image = self.sprites_direita[self.atual]
                    elif self.sprites_esquerda:
                        self.atual = (self.atual + 1) % len(self.sprites_esquerda)
                        self.image = self.sprites_esquerda[self.atual]
                    elif self.sprites_direita:
                        self.atual = (self.atual + 1) % len(self.sprites_direita)
                        self.image = self.sprites_direita[self.atual]
                    elif self.sprites_idle_esquerda:
                        self.image = self.sprites_idle_esquerda[0]
                    else:
                        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)

        if hasattr(self, 'rect'):
            self.rect.center = (self.x, self.y)
            if hasattr(self, 'rect_colisao'):
                self.rect_colisao.center = self.rect.center

    def mover(self, teclas, arvores):
        dx = dy = 0

        original_x = self.x
        original_y = self.y

        if teclas[pygame.K_LEFT]:
            dx = -self.velocidade
            self.direction = "left"
        if teclas[pygame.K_RIGHT]:
            dx = self.velocidade
            self.direction = "right"
        if teclas[pygame.K_UP]:
            dy = -self.velocidade
        if teclas[pygame.K_DOWN]:
            dy = self.velocidade

        self.x += dx
        if hasattr(self, 'rect_colisao'):
            self.rect_colisao.center = (self.x, self.y)
            if arvores is not None:
                for arvore in arvores:
                    arvore_rect = getattr(arvore, 'rect_colisao', getattr(arvore, 'rect', None))
                    if arvore is not None and arvore_rect is not None:
                        if self.rect_colisao.colliderect(arvore_rect):
                            self.x = original_x
                            if hasattr(self, 'rect_colisao'):
                                self.rect_colisao.center = (self.x, self.y)
                            break

        self.y += dy
        if hasattr(self, 'rect_colisao'):
            self.rect_colisao.center = (self.x, self.y)
            if arvores is not None:
                for arvore in arvores:
                    arvore_rect = getattr(arvore, 'rect_colisao', getattr(arvore, 'rect', None))
                    if arvore is not None and arvore_rect is not None:
                        if self.rect_colisao.colliderect(arvore_rect):
                            self.y = original_y
                            if hasattr(self, 'rect_colisao'):
                                self.rect_colisao.center = (self.x, self.y)
                            break

        self.parado = (dx == 0 and dy == 0)

    def atacar(self, inimigos):
        current_time = time.time()

        if self.current_weapon and current_time - self.tempo_ultimo_ataque >= self.cooldown_ataque:
            self.is_attacking = True
            self.is_attacking_animation_active = True
            self.frame_ataque = 0
            self.ultimo_update_ataque = pygame.time.get_ticks()

            self.attack_timer = current_time
            self.tempo_ultimo_ataque = current_time
            self.hit_enemies_this_attack.clear()
            
            attack_hitbox_width = getattr(self, 'attack_hitbox_size', (60, 60))[0]
            attack_hitbox_height = getattr(self, 'attack_hitbox_size', (60, 60))[1]
            self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)

            hitbox_center_x = self.rect.centerx
            hitbox_center_y = self.rect.centery

            if self.direction == "right":
                self.attack_hitbox.midleft = (hitbox_center_x + self.alcance_ataque, hitbox_center_y)
            elif self.direction == "left":
                self.attack_hitbox.midright = (hitbox_center_x - self.alcance_ataque, hitbox_center_y)

        if self.is_attacking:
            if inimigos is not None:
                for inimigo in list(inimigos): # Use list() para permitir remoção durante a iteração
                    if inimigo is not None and hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo() and hasattr(inimigo, 'rect'):
                        if self.attack_hitbox.colliderect(inimigo.rect) and inimigo not in self.hit_enemies_this_attack:
                            if hasattr(inimigo, 'receber_dano'):
                                inimigo.receber_dano(self.dano)
                                self.hit_enemies_this_attack.add(inimigo)
                                # Verifica se o inimigo morreu após o ataque
                                if not inimigo.esta_vivo():
                                    if hasattr(inimigo, 'xp_value') and self.xp_manager: # Verifica se xp_manager existe
                                        self.xp_manager.gain_xp(inimigo.xp_value) # Chama o método do XPManager
                                        print(f"DEBUG(Player): Inimigo {type(inimigo).__name__} derrotado. Ganhou {inimigo.xp_value} XP.")
                                    # Remova o inimigo da lista do gerenciador de inimigos aqui,
                                    # ou deixe o gerenciador de inimigos fazer isso em seu próprio update.
                                    # Por segurança, o gerenciador de inimigos deve ser o responsável por remover.
                            else:
                                print(f"DEBUG(Player): Aviso: Inimigo {type(inimigo).__name__} não tem método 'receber_dano'. Dano não aplicado.")
                    elif inimigo is not None:
                        if not hasattr(inimigo, 'esta_vivo'):
                            print(f"DEBUG(Player): Aviso: Inimigo {type(inimigo).__name__} não tem método 'esta_vivo'. Ignorando para ataque.")
                        if not hasattr(inimigo, 'rect'):
                            print(f"DEBUG(Player): Aviso: Inimigo {type(inimigo).__name__} não tem atributo 'rect'. Ignorando para ataque.")

    def empurrar_jogador(self, inimigo):
        pass

    def desenhar(self, janela, camera_x, camera_y):
        if self.image is not None and hasattr(self, 'rect'):
            janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

        # Removido: Desenho da barra de XP e texto de Nível (agora no XPManager)

        if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0 and self.attack_hitbox.height > 0:
            attack_hitbox_visual = pygame.Rect(self.attack_hitbox.x - camera_x, self.attack_hitbox.y - camera_y, self.attack_hitbox.width, self.attack_hitbox.height)
            pygame.draw.rect(janela, (0, 255, 0), attack_hitbox_visual, 2)

    def esta_vivo(self):
        if self.vida is not None:
            return self.vida.esta_vivo()
        return False

