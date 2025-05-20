# Espirito_Das_Flores.py
import pygame
import random
import math
import os

# Importa a classe base Inimigo do ficheiro Inimigos.py
# Certifique-se de que o ficheiro Inimigos.py está na mesma pasta ou num caminho acessível
# Removido o bloco try-except ImportError conforme solicitado anteriormente
from Inimigos import Inimigo


"""
Classe para o inimigo Espírito das Flores.
Herda da classe base Inimigo.
"""
class Espirito_Das_Flores(Inimigo):
    """
    Representa um inimigo Espírito das Flores.
    Pode ter comportamentos únicos relacionados a flores ou natureza.
    Implementa lógica de desvio quando presa.
    """
    # Variável de classe para armazenar os sprites originais carregados uma única vez
    _sprites_originais = None
    _tamanho_sprite_desejado = (70, 70) # Tamanho padrão para sprites

    def __init__(self, x, y, velocidade=1.8):
        # Carrega os sprites apenas uma vez para todas as instâncias de Espirito_Das_Flores
        if Espirito_Das_Flores._sprites_originais is None:
            Espirito_Das_Flores._carregar_sprites()

        # Inicializa a classe base Inimigo passando a primeira surface carregada e a velocidade.
        initial_image = Espirito_Das_Flores._sprites_originais[0] if Espirito_Das_Flores._sprites_originais else self._criar_placeholder_sprite()
        super().__init__(x, y, initial_image, velocidade)

        self.hp = 75
        self.max_hp = self.hp
        self.sprites = Espirito_Das_Flores._sprites_originais
        self.sprite_index = 0
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
        self.intervalo_animacao = 180

        # Atributos de Combate do Espírito das Flores
        self.is_attacking = False
        self.attack_duration = 600 # milissegundos
        self.attack_timer = 0 # Usando pygame.time.get_ticks()
        self.attack_damage = 12
        self.attack_hitbox_size = (50, 50)
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.attack_range = 70
        self.attack_cooldown = 2500 # milissegundos
        self.last_attack_time = pygame.time.get_ticks() # Usando pygame.time.get_ticks()
        self.facing_right = False
        self.direction = "down" # Usado para posicionar a hitbox, não necessariamente para flipar o sprite

        # Atributos para Dano por Contato
        self.contact_damage = 8
        self.contact_cooldown = 800
        self.last_contact_time = pygame.time.get_ticks()

        # Atributos para detecção de estar preso e lógica de desvio (herdado da classe base)
        # self._previous_pos = (self.rect.x, self.rect.y)
        # self.is_stuck = False
        # self._stuck_timer = 0
        # self._stuck_duration_threshold = 500
        # self._evade_direction = None
        # self._evade_timer = 0
        # self._evade_duration = 500

    @classmethod
    def _carregar_sprites(cls):
        """Carrega os sprites do Espírito das Flores e os armazena na variável de classe."""
        caminhos = [
            "Sprites/Inimigos/Espirito_Flores/Espirito_Flores1.png",
            "Sprites/Inimigos/Espirito_Flores/Espirito_Flores2.png",
            "Sprites/Inimigos/Espirito_Flores/Espirito_Flores3.png",
            "Sprites/Inimigos/Espirito_Flores/Espirito_Flores4.png",
            "Sprites/Inimigos/Espirito_Flores/Espirito_Flores5.png",
            "Sprites/Inimigos/Espirito_Flores/Espirito_Flores6.png",
            "Sprites/Inimigos/Espirito_Flores/Espirito_Flores7.png",
        ]
        cls._sprites_originais = []

        for path in caminhos:
            try:
                if os.path.exists(path):
                    sprite = pygame.image.load(path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, cls._tamanho_sprite_desejado)
                    cls._sprites_originais.append(sprite)
                else:
                    # Se o arquivo não existir, adicione um placeholder
                    placeholder = pygame.Surface(cls._tamanho_sprite_desejado, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (255, 105, 180), (0, 0, cls._tamanho_sprite_desejado[0], cls._tamanho_sprite_desejado[1])) # Pink placeholder
                    fonte = pygame.font.Font(None, 20)
                    texto_erro = fonte.render("Sprite", True, (255, 255, 255))
                    placeholder.blit(texto_erro, (5, 15))
                    texto_erro2 = fonte.render("Erro", True, (255, 255, 255))
                    placeholder.blit(texto_erro2, (10, 35))
                    cls._sprites_originais.append(placeholder)
            except pygame.error as e:
                # Se um sprite falhar, adicione um placeholder com o tamanho correto
                placeholder = pygame.Surface(cls._tamanho_sprite_desejado, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255, 105, 180), (0, 0, cls._tamanho_sprite_desejado[0], cls._tamanho_sprite_desejado[1])) # Pink placeholder
                fonte = pygame.font.Font(None, 20)
                texto_erro = fonte.render("Sprite", True, (255, 255, 255))
                placeholder.blit(texto_erro, (5, 15))
                texto_erro2 = fonte.render("Erro", True, (255, 255, 255))
                placeholder.blit(texto_erro2, (10, 35))
                cls._sprites_originais.append(placeholder)

        if not cls._sprites_originais:
            # Certifique-se de que há pelo menos um sprite carregado, mesmo que seja um placeholder
            placeholder = pygame.Surface(cls._tamanho_sprite_desejado, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (255, 105, 180), (0, 0, cls._tamanho_sprite_desejado[0], cls._tamanho_sprite_desejado[1]))
            cls._sprites_originais.append(placeholder)

    @staticmethod
    def _criar_placeholder_sprite():
        """Cria e retorna uma superfície de placeholder rosa."""
        placeholder = pygame.Surface(Espirito_Das_Flores._tamanho_sprite_desejado, pygame.SRCALPHA)
        pygame.draw.rect(placeholder, (255, 105, 180), (0, 0, Espirito_Das_Flores._tamanho_sprite_desejado[0], Espirito_Das_Flores._tamanho_sprite_desejado[1]))
        fonte = pygame.font.Font(None, 20)
        texto_erro = fonte.render("Sprite", True, (255, 255, 255))
        placeholder.blit(texto_erro, (5, 15))
        texto_erro2 = fonte.render("Erro", True, (255, 255, 255))
        placeholder.blit(texto_erro2, (10, 35))
        return placeholder


    def receber_dano(self, dano):
        """Reduz a vida do Espírito das Flores pela quantidade de dano especificada."""
        if self.esta_vivo():
            self.hp -= dano
            if self.hp <= 0:
                self.hp = 0


    def atualizar_animacao(self):
        """Atualiza o índice do sprite para a animação e aplica o flip horizontal."""
        agora = pygame.time.get_ticks()
        if self.sprites and self.esta_vivo() and agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
            self.tempo_ultimo_update_animacao = agora
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)

        if self.sprites:
            base_image = self.sprites[int(self.sprite_index % len(self.sprites))]
            if self.facing_right:
                self.image = pygame.transform.flip(base_image, True, False)
            else:
                self.image = base_image
        else:
            self.image = self._criar_placeholder_sprite()


    # Sobrescreve o método mover_em_direcao para adicionar a lógica de direção horizontal
    # CORRIGIDO: Adicionado 'arvores' como argumento para compatibilidade com a classe base
    def mover_em_direcao(self, alvo_x, alvo_y, arvores):
        """
        Move o Espírito das Flores em direção a um alvo e atualiza a direção horizontal,
        verificando colisão com árvores.

        Args:
            alvo_x (int): A coordenada x do alvo.
            alvo_y (int): A coordenada y do alvo.
            arvores (list): Uma lista de objetos Arvore para verificar colisão.
        """
        # Chama o método mover_em_direcao da classe base para lidar com o movimento e colisão com árvores
        # A lógica de detecção de estar preso e atualização de self.is_stuck ocorre na classe base.
        super().mover_em_direcao(alvo_x, alvo_y, arvores)

        # Atualiza a direção horizontal com base no movimento em X, apenas se o Espírito das Flores se moveu
        # A detecção de movimento agora está na classe base através de self.is_stuck
        # Podemos inferir a direção horizontal do movimento se não estiver preso
        if not self.is_stuck:
             # Calcula a diferença de posição para determinar a direção horizontal do movimento
             dx = self.rect.x - self._previous_pos[0]
             if abs(dx) > 0.1: # Verifica se houve movimento horizontal significativo
                 if dx > 0:
                     self.facing_right = True
                 elif dx < 0:
                     self.facing_right = False


    def atacar(self, player):
        """
        Implementa a lógica de ataque do Espírito das Flores.
        """
        if not hasattr(player, 'rect'):
            return

        current_ticks = pygame.time.get_ticks()
        if self.esta_vivo() and (current_ticks - self.last_attack_time >= self.attack_cooldown):
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                               self.rect.centery - player.rect.centery)

            if distancia_ao_jogador <= self.attack_range:
                self.is_attacking = True
                self.attack_timer = current_ticks
                self.last_attack_time = current_ticks
                self.hit_by_player_this_attack = False

                attack_hitbox_width = self.attack_hitbox_size[0]
                attack_hitbox_height = self.attack_hitbox_size[1]
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                self.attack_hitbox.center = self.rect.center


    # O método update é herdado e sobrescrito aqui para incluir a lógica específica do Espírito das Flores
    # CORRIGIDO: Adicionado 'arvores' como argumento
    def update(self, player, arvores):
        """
        Atualiza o estado do Espírito das Flores (movimento, animação e ataque).
        Inclui a lógica de aplicação de dano por contato e desvio.

        Args:
            player (Player): O objeto jogador para seguir, verificar o alcance de ataque e aplicar dano.
            arvores (list): Uma lista de objetos Arvore para colisão.
        """
        # Adiciona verificação para garantir que o objeto player tem os atributos necessários
        # Verifica si o player tem pelo menos rect e vida (para verificar si está vivo e receber dano)
        if not (hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and hasattr(player, 'receber_dano')):
            return # Sai do método para evitar o erro

        # Só atualiza si estiver vivo
        if self.esta_vivo():
            current_ticks = pygame.time.get_ticks()

            # Lógica de colisão com o jogador e dano por contato (herdado da classe base)
            self.check_player_collision(player)

            # Lógica do temporizador de ataque específico
            if self.is_attacking:
                if current_ticks - self.attack_timer >= self.attack_duration:
                    self.is_attacking = False
                    self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
                    self.hit_by_player_this_attack = False
                else:
                    if not self.hit_by_player_this_attack and \
                       hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                       self.attack_hitbox.colliderect(player.rect):
                        dano_inimigo = self.attack_damage
                        player.receber_dano(dano_inimigo)
                        self.hit_by_player_this_attack = True


            # >>> Lógica de Movimento e Desvio <<<
            # O Espírito das Flores persegue o jogador si estiver vivo e o jogador estiver vivo.
            # Implementa a lógica de desvio quando detecta que está preso.
            player_tem_rect = hasattr(player, 'rect')
            player_esta_vivo = hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo()
            espirito_esta_vivo = self.esta_vivo()
            espirito_tem_velocidade = self.velocidade > 0

            if espirito_esta_vivo and player_tem_rect and player_esta_vivo and espirito_tem_velocidade:
                # Verifica se está preso por tempo suficiente e não está tentando desviar
                if self.is_stuck and current_ticks - self._stuck_timer > self._stuck_duration_threshold and self._evade_direction is None:
                    # Inicia uma tentativa de desvio
                    # Escolhe uma direção aleatória para tentar desviar (horizontal ou vertical)
                    self._evade_direction = random.choice(["left", "right", "up", "down"])
                    self._evade_timer = current_ticks

                # Se estiver tentando desviar
                if self._evade_direction is not None:
                    # Calcula o movimento de desvio
                    evade_speed = self.velocidade * 1.2 # Pode desviar um pouco mais rápido
                    evade_dx, evade_dy = 0, 0
                    if self._evade_direction == "left":
                        evade_dx = -evade_speed
                    elif self._evade_direction == "right":
                        evade_dx = evade_speed
                    elif self._evade_direction == "up":
                        evade_dy = -evade_speed
                    elif self._evade_direction == "down":
                        evade_dy = evade_speed

                    # Aplica o movimento de desvio (sem verificar colisão com árvores durante o desvio simples)
                    # Uma lógica de desvio mais avançada verificaria colisões também aqui.
                    self.rect.x += evade_dx
                    self.rect.y += evade_dy

                    # Verifica se a duração do desvio terminou
                    if current_ticks - self._evade_timer > self._evade_duration:
                        self._evade_direction = None # Termina a tentativa de desvio
                        self.is_stuck = False # Considera que não está mais preso (será reavaliado no próximo frame)
                else:
                    # Se não estiver tentando desviar, move normalmente em direção ao jogador (com verificação de colisão da base)
                    target_x, target_y = player.rect.centerx, player.rect.centery
                    self.mover_em_direcao(target_x, target_y, arvores) # Chama o método da base com a lista de árvores
            else:
                 pass # Não move si o player não tiver rect ou não estiver vivo


            # Tenta iniciar um ataque específico
            self.atacar(player)

            # Posicionamento da Hitbox de Ataque Específico
            self.attack_hitbox.center = self.rect.center

            # Atualiza a animação
            self.atualizar_animacao()

    def desenhar(self, surface, camera_x, camera_y):
        """Desenha o Espírito das Flores."""
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
