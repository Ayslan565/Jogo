# Fenix.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()
import os # Importa os para verificar a existência de arquivos

# Certifique-se de que Inimigo está acessível
# Importa a classe base Inimigo do ficheiro Inimigos.py
from Inimigos import Inimigo


"""
Classe para o inimigo Fênix.
Herda da classe base Inimigo.
"""
class Fenix(Inimigo): # Nome da classe alterado para Fenix
    """
    Representa um inimigo Fênix.
    Persegue o jogador quando este está vivo e dentro do alcance (se aplicável).
    Implementa lógica de desvio quando presa.
    """
    # Variável de classe para armazenar os sprites carregados uma única vez
    sprites_carregados = None

    def __init__(self, x, y, velocidade=3.0): # Velocidade padrão da Fênix (mais rápida)
        """
        Inicializa um novo objeto Fênix.

        Args:
            x (int): A posição inicial x da Fênix.
            y (int): A posição inicial y da Fênix.
            velocidade (float): A velocidade de movimento da Fênix.
        """
        # Carrega os sprites apenas uma vez para todas as instâncias de Fênix
        if Fenix.sprites_carregados is None:
            caminhos = [
                # >>> CAMINHOS DOS SPRITES DA FÊNIX - AJUSTE CONFORME SEUS ARQUIVOS <<<
                "Sprites/Inimigos/Fenix/Fenix 1.png",
                "Sprites/Inimigos/Fenix/Fenix 2.png",
                "Sprites/Inimigos/Fenix/Fenix 3.png",
                "Sprites/Inimigos/Fenix/Fenix 4.png",
                # Adicione mais caminhos de sprite de animação aqui
            ]
            Fenix.sprites_carregados = []
            tamanho_sprite_desejado = (90, 90) # >>> TAMANHO DESEJADO PARA O SPRITE DA FÊNIX - AJUSTE <<<

            for path in caminhos:
                try:
                    # Verifica se o arquivo existe antes de tentar carregar
                    if os.path.exists(path):
                        sprite = pygame.image.load(path).convert_alpha()
                        # Redimensiona sprites para o tamanho desejado
                        sprite = pygame.transform.scale(sprite, tamanho_sprite_desejado)
                        Fenix.sprites_carregados.append(sprite)
                    else:
                       # Se o arquivo não existir, adicione um placeholder
                       placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                       pygame.draw.rect(placeholder, (255, 165, 0), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1])) # Orange placeholder
                       fonte = pygame.font.Font(None, 20)
                       texto_erro = fonte.render("Sprite", True, (255, 255, 255))
                       placeholder.blit(texto_erro, (5, 15))
                       texto_erro2 = fonte.render("Erro", True, (255, 255, 255))
                       placeholder.blit(texto_erro2, (10, 35))
                       Fenix.sprites_carregados.append(placeholder)

                except pygame.error as e:
                    # Se um sprite falhar, adicione um placeholder com o tamanho correto
                    placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (255, 165, 0), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1])) # Orange placeholder
                    fonte = pygame.font.Font(None, 20)
                    texto_erro = fonte.render("Sprite", True, (255, 255, 255))
                    placeholder.blit(texto_erro, (5, 15))
                    texto_erro2 = fonte.render("Erro", True, (255, 255, 255))
                    placeholder.blit(texto_erro2, (10, 35))
                    Fenix.sprites_carregados.append(placeholder)

            # Certifique-se de que há pelo menos um sprite carregado, mesmo que seja um placeholder
            if not Fenix.sprites_carregados:
                tamanho_sprite_desejado = (70, 70) # Tamanho do placeholder si nenhum sprite carregar
                placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255, 165, 0), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1]))
                Fenix.sprites_carregados.append(placeholder) # Adiciona o placeholder aos sprites originais


        # Inicializa a classe base Inimigo PASSANDO A PRIMEIRA SURFACE CARREGADA E A VELOCIDADE.
        # Certifique-se de que Fenix.sprites_carregados não está vazio antes de acessar o índice [0]
        initial_image = Fenix.sprites_carregados[0] if Fenix.sprites_carregados else pygame.Surface((70, 70), pygame.SRCALPHA) # Usa placeholder se a lista estiver vazia
        super().__init__(x, y, initial_image, velocidade) # >>> Passa a velocidade para a classe base <<<


        self.hp = 70 # Pontos de vida da Fênix (ajuste conforme necessário)
        self.max_hp = self.hp # Define HP máximo para barra de vida
        # self.velocidade é definido na classe base agora
        self.sprites = Fenix.sprites_carregados # Referência à lista de sprites carregados
        self.sprite_index = 0 # Índice do sprite atual para animação
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Tempo do último update da animação
        self.intervalo_animacao = 100 # milissegundos entre frames de animação (mais rápido para Fênix)


        # >>> Atributos de Combate da Fênix <<<
        self.is_attacking = False # Flag para indicar si a Fênix está atacando
        self.attack_duration = 0.5 # Duração da animação de ataque (mais rápido)
        self.attack_timer = 0 # Tempo em que o ataque começou (usando time.time())
        self.attack_damage = 15 # Quantidade de dano causado pelo ataque (dano de ataque específico)
        # Define o tamanho da hitbox de ataque - AJUSTE ESTES VALORES
        self.attack_hitbox_size = (60, 60) # Exemplo: hitbox 60x60 pixels (maior para Fênix)
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Retângulo para a hitbox de ataque (inicialmente vazio)
        self.attack_range = 100 # Alcance para iniciar o ataque (maior para Fênix)
        self.attack_cooldown = 2 # Tempo de espera entre ataques em segundos (mais rápido)
        self.last_attack_time = time.time() # Tempo em que o último ataque ocorreu (usando time.time())
        # self.hit_by_player_this_attack é herdado da classe base


        # Atributo para rastrear a direção horizontal para espelhamento
        self.facing_right = True # True si estiver virado para a direita, False para a esquerda


        # >>> Atributos para Dano por Contato <<<
        self.contact_damage = 5 # Dano de contato (ajuste)
        self.contact_cooldown = 300 # Cooldown de dano de contato em milissegundos (mais rápido)
        self.last_contact_time = pygame.time.get_ticks() # Tempo do último contato (em milissegundos)

        # Atributos para detecção de estar preso e lógica de desvio (herdado da classe base)
        # self._previous_pos = (self.rect.x, self.rect.y)
        # self.is_stuck = False
        # self._stuck_timer = 0
        # self._stuck_duration_threshold = 500
        # self._evade_direction = None
        # self._evade_timer = 0
        # self._evade_duration = 500


    # O método esta_vivo() é herdado da classe base Inimigo.

    def receber_dano(self, dano):
        """
        Reduz a vida do inimigo pela quantidade de dano especificada.

        Args:
            dano (int): A quantidade de dano a ser recebida.
        """
        # Verifica si o inimigo está vivo antes de receber dano
        if self.esta_vivo(): # Chama o método esta_vivo() herdado
            self.hp -= dano
            if self.hp <= 0:
                self.hp = 0
                # A remoção da lista no gerenciador de inimigos é feita no GerenciadorDeInimigos.update_inimigos.
                # Opcional: self.kill() pode ser chamado aqui si estiver usando grupos de sprites.


    def atualizar_animacao(self):
        """Atualiza o índice do sprite para a animação."""
        agora = pygame.time.get_ticks()
        # Verifica si self.sprites não está vazio antes de calcular o módulo
        if self.sprites and self.esta_vivo() and agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao: # Só anima si estiver vivo
            self.tempo_ultimo_update_animacao = agora
            # Incrementa o índice do sprite lentamente para a animação
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            # Define a imagem atual com base no índice (sem aplicar o flip ainda)
            self.image = self.sprites[int(self.sprite_index)]
            # Opcional: Redimensionar a imagem atualizada si necessário (mas já redimensionamos no carregamento)
            # self.image = pygame.transform.scale(self.image, (70, 70)) # Ajuste o tamanho se redimensionar aqui
        elif not self.esta_vivo() and self.sprites:
             # Si morreu, pode definir um sprite de morte ou manter o último frame
             # Por enquanto, mantém o último frame ou o primeiro si a lista estiver vazia
             if self.sprites:
                 self.image = self.sprites[int(self.sprite_index % len(self.sprites))] # Mantém o último frame (garante índice válido)
             else:
                 # Fallback si não houver sprites
                 tamanho_sprite_desejado = (70, 70) # Tamanho do placeholder
                 self.image = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                 pygame.draw.rect(self.image, (255, 165, 0), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1]))


    # Sobrescreve o método mover_em_direcao para atualizar a direção horizontal
    # CORRIGIDO: Adicionado 'arvores' como argumento para compatibilidade com a classe base
    def mover_em_direcao(self, alvo_x, alvo_y, arvores):
        """
        Move a Fênix na direção de um ponto alvo e atualiza a direção horizontal,
        verificando colisão com árvores.

        Args:
            alvo_x (int): A coordenada x do ponto alvo.
            alvo_y (int): A coordenada y do ponto alvo.
            arvores (list): Uma lista de objetos Arvore para verificar colisão.
        """
        # Chama o método mover_em_direcao da classe base para lidar com o movimento e colisão com árvores
        # A lógica de detecção de estar preso e atualização de self.is_stuck ocorre na classe base.
        super().mover_em_direcao(alvo_x, alvo_y, arvores)

        # Atualiza a direção horizontal com base no movimento em X, apenas se a Fênix se moveu
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
        Implementa a lógica de ataque da Fênix.
        Pode ser um ataque de mergulho, projétil de fogo, etc.

        Args:
            player (Player): O objeto jogador para verificar o alcance de ataque.
        """
        # Adiciona verificação para garantir que o objeto player tem o atributo rect
        if not hasattr(player, 'rect'):
            return # Sai do método para evitar o erro

        current_time = time.time()
        # Verifica se o cooldown passou e se o jogador está dentro do alcance de ataque
        # E se a Fênix está viva
        if self.esta_vivo() and (current_time - self.last_attack_time >= self.attack_cooldown):
            # Calcula a distância até o jogador
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                             self.rect.centery - player.rect.centery)

            if distancia_ao_jogador <= self.attack_range:
                # Inicia o ataque
                self.is_attacking = True
                self.attack_timer = current_time # Registra o tempo de início do ataque
                self.last_attack_time = current_time # Reseta o cooldown
                self.hit_by_player_this_attack = False # Reseta a flag de acerto para este novo ataque

                # Define a hitbox de ataque (exemplo: uma área de dano de fogo ao redor da Fênix)
                # Você precisará ajustar isso com base na animação ou tipo de ataque da sua Fênix
                attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0] # Pega a largura da hitbox ou um valor padrão
                attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1] # Pega a altura da hitbox ou um valor padrão

                # Posiciona a hitbox de ataque (exemplo: centralizada na Fênix durante o ataque)
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                self.attack_hitbox.center = self.rect.center # Centraliza a hitbox na Fênix


    # O método update é herdado e sobrescrito aqui para incluir a lógica específica da Fênix
    # CORRIGIDO: Adicionado 'arvores' como argumento
    def update(self, player, arvores):
        """
        Atualiza o estado da Fênix (movimento, animação e ataque).
        Inclui a lógica de aplicação de dano por contato e desvio.

        Args:
            player (Player): O objeto jogador para seguir, verificar o alcance de ataque e aplicar dano.
            arvores (list): Uma lista de objetos Arvore para colisão.
        """
        # >>> Adiciona verificação para garantir que o objeto player tem os atributos necessários <<<
        # Verifica si o player tem pelo menos rect e vida (para verificar si está vivo e receber dano)
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            return # Sai do método para evitar o erro

        # Só atualiza si estiver vivo
        if self.esta_vivo():
            current_time = time.time()
            current_ticks = pygame.time.get_ticks() # Usando get_ticks() para consistência com contact_cooldown

            # Lógica de colisão com o jogador e dano por contato (herdado da classe base)
            self.check_player_collision(player)

            # Lógica do temporizador de ataque específico
            if self.is_attacking:
                 # Verifica si a duração do ataque passou
                 if time.time() - self.attack_timer >= self.attack_duration: # Usa time.time() para consistência com attack_timer
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
            # A Fênix persegue o jogador si estiver vivo e o jogador estiver vivo.
            # Implementa a lógica de desvio quando detecta que está presa.
            player_tem_rect = hasattr(player, 'rect')
            player_esta_vivo = hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo()
            fenix_esta_viva = self.esta_vivo()
            fenix_tem_velocidade = self.velocidade > 0

            if fenix_esta_viva and player_tem_rect and player_esta_vivo and fenix_tem_velocidade:
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


            # Tenta iniciar um ataque específico (verificado após o movimento)
            # A função atacar também tem uma verificação interna agora
            self.atacar(player)

            # >>> Posicionamento da Hitbox de Ataque Específico (Atualiza mesmo si não estiver atacando ativamente) <<<
            # A hitbox de ataque é posicionada em relação ao centro da Fênix.
            # Ajuste as coordenadas conforme a sua animação e alcance desejado.
            # A hitbox é posicionada independentemente de estar atacando ou não,
            # mas só é usada para aplicar dano quando is_attacking é True.
            attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0] # Pega a largura da hitbox ou um valor padrão
            attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1] # Pega a altura da hitbox ou um valor padrão
            self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
            self.attack_hitbox.center = self.rect.center # Centraliza a hitbox na Fênix


            # Atualiza a animação
            self.atualizar_animacao()


    # Sobrescreve o método desenhar para aplicar o espelhamento
    def desenhar(self, surface, camera_x, camera_y):
        """Desenha a Fênix, aplicando espelhamento horizontal se necessário."""
        # Verifica se o inimigo está vivo antes de desenhar
        if self.esta_vivo():
            # Obtém a imagem atual (já atualizada pela animação)
            imagem_para_desenhar = self.image

            # Aplica o espelhamento horizontal si estiver virado para a esquerda
            if not self.facing_right:
                imagem_para_desenhar = pygame.transform.flip(imagem_para_desenhar, True, False) # Flip horizontalmente, não verticalmente

            # Desenha a imagem (espelhada ou não) com o offset da câmera
            surface.blit(imagem_para_desenhar, (self.rect.x - camera_x, self.rect.y - camera_y))

        # Lógica de desenho da barra de vida removida

    # O método receber_dano() é herdado da classe base Inimigo e sobrescrito aqui.
