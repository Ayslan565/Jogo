# Planta_Carnivora.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()
import os # Importa os para verificar a existência de arquivos

# Importa a classe base Inimigo do ficheiro Inimigos.py
# Certifique-se de que o ficheiro Inimigos.py está na mesma pasta ou num caminho acessível
from Inimigos import Inimigo


class Planta_Carnivora(Inimigo):
    """
    Representa um inimigo Planta Carnívora.
    Persegue o jogador quando este está vivo e dentro do alcance (se aplicável).
    Implementa lógica de desvio quando presa.
    """
    # Variável de classe para armazenar os sprites carregados uma única vez
    _sprites_originais = None
    _tamanho_sprite_desejado = (64, 64) # Tamanho padrão para sprites

    def __init__(self, x, y, velocidade=1.0): # Velocidade padrão do Planta Carnivora
        """
        Inicializa um novo objeto Planta_Carnivora.

        Args:
            x (int): A posição inicial x da planta.
            y (int): A posição inicial y da planta.
            velocidade (float): A velocidade de movimento da planta.
        """
        # Carrega os sprites apenas uma vez para todas as instâncias de Planta_Carnivora
        if Planta_Carnivora._sprites_originais is None: # Carrega na variável de sprites_originais
            Planta_Carnivora._carregar_sprites()

        # Inicializa a classe base Inimigo PASSANDO A PRIMEIRA SURFACE CARREGADA E A VELOCIDADE.
        # Certifique-se de que Planta_Carnivora._sprites_originais não está vazio antes de acessar o índice [0]
        initial_image = Planta_Carnivora._sprites_originais[0] if Planta_Carnivora._sprites_originais else self._criar_placeholder_sprite() # Usa placeholder se a lista estiver vazia
        super().__init__(x, y, initial_image, velocidade) # >>> Passa a velocidade para a classe base <<<


        self.hp = 25 # Pontos de vida do Planta Carnivora
        self.max_hp = self.hp # Define HP máximo para barra de vida
        # self.velocidade é definido na classe base agora
        self.sprites = Planta_Carnivora._sprites_originais # Referência à lista de sprites originais carregados
        self.sprite_index = 0 # Índice do sprite atual para animação
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Tempo do último update da animação
        self.intervalo_animacao = 200 # milissegundos entre frames de animação (ajuste para a velocidade da animação)


        # >>> Atributos de Combate do Planta Carnivora <<<
        self.is_attacking = False # Flag para indicar si o Planta Carnivora está atacando
        self.attack_duration = 500 # Duração da animação de ataque (ajuste conforme a animação) em ms
        self.attack_timer = 0 # Tempo em que o ataque começou (usando pygame.time.get_ticks())
        self.attack_damage = 15 # Quantidade de dano causado pelo ataque (dano de ataque específico)
        # Define o tamanho da hitbox de ataque - AJUSTE ESTES VALORES PARA REDUZIR O TAMANHO
        self.attack_hitbox_size = (40, 40) # Exemplo: hitbox 40x40 pixels
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Retângulo para a hitbox de ataque (inicialmente vazio)
        self.attack_range = 60 # Alcance para iniciar o ataque (distância do centro do inimigo ao centro do jogador)
        self.attack_cooldown = 3000 # Tempo de espera entre ataques em milissegundos
        self.last_attack_time = pygame.time.get_ticks() # Tempo em que o último ataque ocorreu (usando pygame.time.get_ticks())
        # self.hit_by_player_this_attack é herdado da classe base


        # Atributo para rastrear a direção do Planta Carnivora (para posicionar a hitbox de ataque e flipar o sprite)
        # Inicializa com uma direção padrão, será atualizado no mover_em_direcao
        self.direction = "down"
        self.facing_right = True # Adiciona atributo para controlar a direção horizontal

        # Atributos para detecção de estar preso e lógica de desvio (herdado da classe base)
        # self._previous_pos = (self.rect.x, self.rect.y)
        # self.is_stuck = False
        # self._stuck_timer = 0
        # self._stuck_duration_threshold = 500
        # self._evade_direction = None
        # self._evade_timer = 0
        # self._evade_duration = 500


        # >>> Atributos para Dano por Contato <<<
        self.contact_damage = 10 # Dano de contato (ajuste)
        self.contact_cooldown = 1000 # Cooldown de dano de contato em milissegundos (ajuste)
        self.last_contact_time = pygame.time.get_ticks() # Tempo do último contato (em milissegundos)

    @classmethod
    def _carregar_sprites(cls):
        """Carrega os sprites da Planta Carnívora e os armazena na variável de classe."""
        caminhos = [
            "Sprites/Inimigos/Planta Carnivora/Planta carnivora 1.png",
            "Sprites/Inimigos/Planta Carnivora/Planta_Carnivora2.png", # Corrigido a barra invertida
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
                   pygame.draw.rect(placeholder, (0, 255, 255), (0, 0, cls._tamanho_sprite_desejado[0], cls._tamanho_sprite_desejado[1])) # Cyan placeholder
                   fonte = pygame.font.Font(None, 20)
                   texto_erro = fonte.render("Sprite", True, (0, 0, 0))
                   placeholder.blit(texto_erro, (5, 15))
                   texto_erro2 = fonte.render("Erro", True, (0, 0, 0))
                   placeholder.blit(texto_erro2, (10, 35))
                   cls._sprites_originais.append(placeholder)

            except pygame.error as e:
                # Se um sprite falhar, adicione um placeholder com o tamanho correto
                placeholder = pygame.Surface(cls._tamanho_sprite_desejado, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (0, 255, 255), (0, 0, cls._tamanho_sprite_desejado[0], cls._tamanho_sprite_desejado[1])) # Cyan placeholder
                fonte = pygame.font.Font(None, 20)
                texto_erro = fonte.render("Sprite", True, (0, 0, 0))
                placeholder.blit(texto_erro, (5, 15))
                texto_erro2 = fonte.render("Erro", True, (0, 0, 0))
                placeholder.blit(texto_erro2, (10, 35))
                cls._sprites_originais.append(placeholder)

        if not cls._sprites_originais:
            # Certifique-se de que há pelo menos um sprite carregado, mesmo que seja um placeholder
            placeholder = pygame.Surface(cls._tamanho_sprite_desejado, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (0, 255, 255), (0, 0, cls._tamanho_sprite_desejado[0], cls._tamanho_sprite_desejado[1]))
            cls._sprites_originais.append(placeholder)

    @staticmethod
    def _criar_placeholder_sprite():
        """Cria e retorna uma superfície de placeholder ciano."""
        placeholder = pygame.Surface(Planta_Carnivora._tamanho_sprite_desejado, pygame.SRCALPHA)
        pygame.draw.rect(placeholder, (0, 255, 255), (0, 0, Planta_Carnivora._tamanho_sprite_desejado[0], Planta_Carnivora._tamanho_sprite_desejado[1]))
        fonte = pygame.font.Font(None, 20)
        texto_erro = fonte.render("Sprite", True, (0, 0, 0))
        placeholder.blit(texto_erro, (5, 15))
        texto_erro2 = fonte.render("Erro", True, (0, 0, 0))
        placeholder.blit(texto_erro2, (10, 35))
        return placeholder


    # O método esta_vivo() é herdado da classe base Inimigo.

    def receber_dano(self, dano):
        """
        Reduz a vida do inimigo pela quantidade de dano especificada.
        """
        if self.esta_vivo(): # Chama o método esta_vivo() herdado
            self.hp -= dano
            if self.hp <= 0:
                self.hp = 0
                # A remoção da lista no gerenciador de inimigos é feita no GerenciadorDeInimigos.update_inimigos.
                # Opcional: self.kill() pode ser chamado aqui si estiver usando grupos de sprites.


    def atualizar_animacao(self):
        """Atualiza o índice do sprite para a animação e aplica o flip horizontal."""
        agora = pygame.time.get_ticks()
        # Verifica si self.sprites (sprites originais) não está vazio antes de calcular o módulo
        if self.sprites and self.esta_vivo() and agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao: # Só anima si estiver vivo
            self.tempo_ultimo_update_animacao = agora
            # Incrementa o índice do sprite lentamente para a animação
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)

        # Define a imagem atual com base no índice, usando os sprites originais
        if self.sprites:
            base_image = self.sprites[int(self.sprite_index % len(self.sprites))]
            # Invertendo a lógica: aplica o flip horizontal si estiver virado para a direita
            # Assumindo que o sprite base está virado para a esquerda.
            if self.facing_right: # <-- Lógica invertida aqui
                self.image = pygame.transform.flip(base_image, True, False)
            else:
                self.image = base_image
        else:
            # Fallback si não houver sprites
            self.image = self._criar_placeholder_sprite()


    # Sobrescreve o método mover_em_direcao para adicionar a lógica de direção horizontal
    # CORRIGIDO: Adicionado 'arvores' como argumento para compatibilidade com a classe base
    def mover_em_direcao(self, alvo_x, alvo_y, arvores):
        """
        Move a planta carnívora em direção a um alvo e atualiza a direção horizontal,
        verificando colisão com árvores.

        Args:
            alvo_x (int): A coordenada x do alvo.
            alvo_y (int): A coordenada y do alvo.
            arvores (list): Uma lista de objetos Arvore para verificar colisão.
        """
        # Chama o método mover_em_direcao da classe base para lidar com o movimento e colisão com árvores
        # A lógica de detecção de estar preso e atualização de self.is_stuck ocorre na classe base.
        super().mover_em_direcao(alvo_x, alvo_y, arvores)

        # Atualiza a direção horizontal com base no movimento em X, apenas se a Planta Carnívora se moveu
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
        Implementa a lógica de ataque do Planta Carnivora.
        Neste exemplo, um ataque simples de contato ou projétil (si aplicável).

        Args:
            player (Player): O objeto jogador para verificar o alcance de ataque.
        """
        # Adiciona verificação para garantir que o objeto player tem o atributo rect
        if not hasattr(player, 'rect'):
            return # Sai do método para evitar o erro

        current_ticks = pygame.time.get_ticks()
        # Verifica si o cooldown passou e se o jogador está dentro do alcance de ataque
        # E se o Planta Carnivora está vivo
        if self.esta_vivo() and (current_ticks - self.last_attack_time >= self.attack_cooldown):
            # Calcula a distância até o jogador
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                             self.rect.centery - player.rect.centery)

            if distancia_ao_jogador <= self.attack_range:
                # Inicia o ataque
                self.is_attacking = True
                self.attack_timer = current_ticks # Registra o tempo de início do ataque
                self.last_attack_time = current_ticks # Reseta o cooldown
                self.hit_by_player_this_attack = False # Reseta a flag de acerto para este novo ataque

                # Define a hitbox de ataque (exemplo: um retângulo ao redor do Planta Carnivora para ataque de contato)
                # Você precisará ajustar isso com base na animação ou tipo de ataque do seu Planta Carnivora
                attack_hitbox_width = self.attack_hitbox_size[0] # Pega a largura da hitbox ou um valor padrão
                attack_hitbox_height = self.attack_hitbox_size[1] # Pega a altura da hitbox ou um valor padrão

                # Posiciona a hitbox de ataque (exemplo: centralizada no Planta Carnivora)
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                self.attack_hitbox.center = self.rect.center # Centraliza a hitbox no Planta Carnivora

                # >>> Lógica de Aplicação de Dano do Ataque Específico (PODE SER AQUI OU NO UPDATE) <<<
                # Para um ataque instantâneo (não baseado em duração), a lógica de dano pode vir aqui.
                # Para ataques com duração (animação), a lógica de dano geralmente fica no update,
                # verificando a colisão da hitbox de ataque enquanto is_attacking é True.
                # Exemplo de ataque instantâneo:
                # if hasattr(player, 'receber_dano'):
                #     dano_inimigo = getattr(self, 'attack_damage', 0)
                #     player.receber_dano(dano_inimigo)
                #     self.hit_by_player_this_attack = True # Marca como atingido para evitar múltiplos hits no mesmo ataque instantâneo


    # O método update é herdado e sobrescrito aqui para incluir a lógica específica da Planta Carnivora
    # CORRIGIDO: Adicionado 'arvores' como argumento
    def update(self, player, arvores):
        """
        Atualiza o estado do Planta Carnivora (movimento, animação e ataque).
        Inclui a lógica de aplicação de dano por contato e desvio.

        Args:
            player (Player): O objeto jogador para seguir, verificar o alcance de ataque e aplicar dano.
            arvores (list): Uma lista de objetos Arvore para colisão.
        """
        # >>> Adiciona verificação para garantir que o objeto player tem os atributos necessários <<<
        # Verifica si o player tem pelo menos rect e vida (para verificar si está vivo e receber dano)
        if not (hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and hasattr(player, 'receber_dano')):
            return # Sai do método para evitar o erro

        # Só atualiza si estiver vivo
        if self.esta_vivo():
            current_ticks = pygame.time.get_ticks() # Usando get_ticks() para consistência com contact_cooldown

            # Lógica de colisão com o jogador e dano por contato (herdado da classe base)
            self.check_player_collision(player)

            # Lógica do temporizador de ataque específico
            if self.is_attacking:
                 # Verifica si a duração do ataque passou
                 if current_ticks - self.attack_timer >= self.attack_duration: # Usa pygame.time.get_ticks() para consistência com attack_timer
                     self.is_attacking = False
                     self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Reseta a hitbox quando o ataque termina
                     self.hit_by_player_this_attack = False # Reseta a flag de acerto ao final do ataque específico
                 else:
                      # >>> Lógica de Dano do Ataque Específico (VERIFICADA DURANTE A ANIMAÇÃO DE ATAQUE) <<<
                      # Verifica si o inimigo está atacando (ataque específico), si ainda não acertou neste ataque,
                      # si tem hitbox de ataque e si colide com o rect do jogador.
                      if not self.hit_by_player_this_attack and \
                             hasattr(self, 'attack_hitbox') and \
                             hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                             self.attack_hitbox.colliderect(player.rect): # >>> CORREÇÃO AQUI: Usa player.rect <<<

                           # Verifica si o jogador tem o método receber_dano e está vivo
                           if hasattr(player, 'receber_dano'):
                                # Aplica dano do ataque específico ao jogador
                                dano_inimigo = getattr(self, 'attack_damage', 0) # Pega attack_damage ou 0 si não existir
                                player.receber_dano(dano_inimigo)
                                self.hit_by_player_this_attack = True # Define a flag para não acertar novamente neste ataque específico
                                # Opcional: Adicionar um som ou efeito visual quando o inimigo acerta o jogador com ataque específico


            # >>> Lógica de Movimento e Desvio <<<
            # O Planta Carnivora persegue o jogador si estiver vivo e o jogador estiver vivo.
            # Implementa a lógica de desvio quando detecta que está preso.
            player_tem_rect = hasattr(player, 'rect')
            player_esta_vivo = hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo()
            planta_esta_viva = self.esta_vivo()
            planta_tem_velocidade = self.velocidade > 0

            if planta_esta_viva and player_tem_rect and player_esta_vivo and planta_tem_velocidade:
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

    # O método desenhar() é herdado da classe base Inimigo.
    # Não precisamos sobrescrever desenhar aqui, pois o flip é aplicado no atualizar_animacao

    # O método receber_dano() é herdado da classe base Inimigo.
