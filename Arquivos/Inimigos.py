# Inimigos.py
import pygame
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()

class Inimigo(pygame.sprite.Sprite):
    """
    Classe base para inimigos no jogo.
    Herda de pygame.sprite.Sprite para facilitar o manuseio de grupos de sprites.
    Recebe uma Surface do Pygame já carregada.
    """
    def __init__(self, x, y, image_surface, velocidade=1):
        """
        Inicializa um novo objeto Inimigo com uma Surface de imagem.

        Args:
            x (int): A posição inicial x do inimigo.
            y (int): A posição inicial y do inimigo.
            image_surface (pygame.Surface): A Surface do Pygame já carregada para o sprite.
            velocidade (float): A velocidade de movimento base do inimigo.
        """
        super().__init__() # Inicializa a classe base Sprite

        self.image = image_surface # Usa a Surface passada diretamente
        self.rect = self.image.get_rect(topleft=(x, y)) # Obtém o retângulo do sprite e define a posição inicial
        self.velocidade = velocidade # Define a velocidade de movimento base do inimigo

        # >>> Define a hitbox de colisão reduzida para o inimigo <<<
        # Esta hitbox será usada para colisões com elementos do mundo, como árvores.
        # Ajuste o tamanho e a posição conforme necessário para cada tipo de inimigo
        # nas classes derivadas, se a hitbox padrão não for adequada.
        collision_width = int(self.rect.width * 0.6) # Exemplo: 60% da largura do sprite
        collision_height = int(self.rect.height * 0.3) # Exemplo: 30% da altura do sprite

        # Garante que a hitbox tenha um tamanho mínimo
        collision_width = max(collision_width, 10) # Mínimo de 10 pixels de largura
        collision_height = max(collision_height, 10) # Mínimo de 10 pixels de altura


        # Cria o retângulo de colisão
        self.collision_rect = pygame.Rect(0, 0, collision_width, collision_height)
        # Posiciona a hitbox no centro inferior do retângulo principal do sprite
        self.collision_rect.centerx = self.rect.centerx
        self.collision_rect.bottom = self.rect.bottom

        # print(f"DEBUG(Inimigo Base): Inimigo criado em ({x}, {y}), rect: {self.rect}, collision_rect: {self.collision_rect}") # Debug removido


        # Atributos de combate comuns (podem ser sobrescritos nas classes derivadas)
        self.hp = 100 # Pontos de vida padrão
        self.is_attacking = False # Flag para indicar si o inimigo está atacando
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Retângulo para a hitbox de ataque (inicialmente vazio)
        self.hit_by_player_this_attack = False # Flag para controle de hit por ataque do jogador
        self.contact_damage = 5 # Dano por contato padrão
        self.contact_cooldown = 1000 # Cooldown de dano de contato padrão (em milissegundos)
        self.last_contact_time = pygame.time.get_ticks() # Tempo do último contato (em milissegundos)

        # Atributos para o empurrão no jogador
        self.push_force = 10 # Força do empurrão aplicado ao jogador
        self.push_duration = 200 # Duração do empurrão (em milissegundos)

        # Atributos para detecção de estar preso e lógica de desvio
        self._previous_pos = (self.rect.x, self.rect.y)
        self.is_stuck = False
        self._stuck_timer = 0 # Tempo em que ficou preso pela última vez
        self._stuck_duration_threshold = 500 # Tempo em milissegundos para considerar que está preso
        self._evade_direction = None # Direção de desvio (ex: "left", "right")
        self._evade_timer = 0 # Tempo em que começou a desviar
        self._evade_duration = 500 # Duração da tentativa de desvio em milissegundos


    # Modificado: Adicionado 'arvores' como argumento e lógica de detecção de estar preso
    def mover_em_direcao(self, alvo_x, alvo_y, arvores):
        """
        Move o inimigo na direção de um ponto alvo, verificando colisão com árvores
        usando a hitbox de colisão reduzida do inimigo e da árvore.

        Args:
            alvo_x (int): A coordenada x do ponto alvo.
            alvo_y (int): A coordenada y do ponto alvo.
            arvores (list): Uma lista de objetos Arvore para verificar colisão.
        """
        # Armazena a posição antes de tentar mover
        current_pos = (self.rect.x, self.rect.y)
        self._previous_pos = current_pos # Atualiza a posição anterior

        # Só move si estiver vivo e tiver velocidade
        if self.esta_vivo() and self.velocidade > 0:
            dx = alvo_x - self.rect.centerx # Diferença no eixo x
            dy = alvo_y - self.rect.centery # Diferença no eixo y
            distancia = math.hypot(dx, dy) # Calcula a distância usando a hipotenusa

            # Define uma pequena margem para evitar tremer quando muito perto
            if distancia > self.velocidade / 2: # Move apenas si a distância for maior que metade da velocidade
                # Normaliza o vetor direção para obter apenas a direção
                if distancia > 0: # Evita divisão por zero
                    dx_norm = dx / distancia
                    dy_norm = dy / distancia
                else:
                    dx_norm = 0
                    dy_norm = 0

                # Calcula a potencial nova posição
                new_x = self.rect.x + dx_norm * self.velocidade
                new_y = self.rect.y + dy_norm * self.velocidade

                # Cria um retângulo TEMPORÁRIO para a hitbox de colisão do inimigo na nova posição
                # para verificar colisão com as hitboxes de colisão das árvores.
                if hasattr(self, 'collision_rect'): # Verifica si a hitbox de colisão do inimigo existe
                     temp_collision_rect = self.collision_rect.copy()
                     # Atualiza a posição do centro inferior da hitbox temporária com base na nova posição do rect principal
                     temp_collision_rect.centerx = new_x + self.rect.width // 2 # Calcula o centro X da nova posição do rect
                     temp_collision_rect.bottom = new_y + self.rect.height # Calcula a base Y da nova posição do rect
                else:
                     # Se a hitbox de colisão do inimigo não existir, usa o rect principal temporário
                     temp_collision_rect = self.rect.copy()
                     temp_collision_rect.x = new_x
                     temp_collision_rect.y = new_y
                     # print("AVISO(Inimigo Base): self.collision_rect não existe. Usando self.rect para colisão com árvores.") # Debug removido


                # Verifica colisão com cada árvore usando as hitboxes de colisão
                can_move = True
                if arvores is not None: # Verifica si a lista de árvores não é None
                    for arvore in arvores:
                         # Verifica si a árvore existe e tem a hitbox de colisão reduzida
                         if arvore is not None and hasattr(arvore, 'collision_rect'):
                              # >>> Usa a hitbox de colisão do inimigo (temporária) e da árvore para a detecção <<<
                              if temp_collision_rect.colliderect(arvore.collision_rect):
                                   can_move = False
                                   break # Para de verificar assim que encontrar uma colisão
                         # Si a árvore não tiver collision_rect, verifica com o rect principal como fallback
                         elif arvore is not None and hasattr(arvore, 'rect'):
                              if temp_collision_rect.colliderect(arvore.rect):
                                   can_move = False
                                   break
                         # else:
                              # print("AVISO(Inimigo Base): Objeto na lista de árvores é None ou não tem rect/collision_rect.") # Debug removido


                # Si não houver colisão com árvores, aplica o movimento ao rect principal
                if can_move:
                    self.rect.x = new_x
                    self.rect.y = new_y
                    # Atualiza a posição da hitbox de colisão do inimigo para a nova posição
                    if hasattr(self, 'collision_rect'):
                         self.collision_rect.centerx = self.rect.centerx
                         self.collision_rect.bottom = self.rect.bottom
                # else:
                    # Se não puder mover, a posição não mudará, e isso será detectado no update
                    # print(f"DEBUG(Inimigo Base): Colisão detectada com árvore. Não moveu.") # Debug removido


            else:
                 # Si a distância for menor ou igual à metade da velocidade, move diretamente para o alvo
                 self.rect.centerx = alvo_x
                 self.rect.centery = alvo_y
                 # Atualiza a posição da hitbox de colisão do inimigo para a nova posição
                 if hasattr(self, 'collision_rect'):
                      self.collision_rect.centerx = self.rect.centerx
                      self.collision_rect.bottom = self.rect.bottom


        # Após tentar mover, verifica se a posição mudou para detectar se está preso
        # Compara a posição ATUAL do rect principal com a posição ANTERIOR
        if (self.rect.x, self.rect.y) == current_pos:
            # Se a posição não mudou, o inimigo está preso
            if not self.is_stuck:
                self.is_stuck = True
                self._stuck_timer = pygame.time.get_ticks() # Inicia o temporizador de estar preso
                # print(f"DEBUG(Inimigo Base): {type(self).__name__} ficou preso em ({self.rect.x}, {self.rect.y}).") # Debug removido
        else:
            # Se a posição mudou, o inimigo não está mais preso
            self.is_stuck = False
            self._stuck_timer = 0 # Reseta o temporizador


    # Modificado: Adicionado 'arvores' como argumento e lógica de detecção de estar preso
    def update(self, player, arvores):
        """
        Método placeholder para atualização do inimigo.
        As classes derivadas devem sobrescrever este método para implementar
        movimento, ataque, animação, etc. Deve receber o objeto player e a lista de árvores.

        As classes derivadas devem implementar a lógica de IA aqui,
        incluindo como o inimigo decide se mover (por exemplo, para desviar de árvores)
        e então chamar self.mover_em_direcao(player.rect.centerx, player.rect.centery, arvores)
        ou uma lógica de movimento específica.

        Este método base inclui a lógica de colisão com o jogador e empurrão.
        """
        # Lógica de colisão com o jogador e dano de contato/empurrão
        self.check_player_collision(player)

        # >>> Implemente a lógica de IA específica do inimigo nas classes derivadas aqui. <<<
        # As classes derivadas devem chamar self.mover_em_direcao(player.rect.centerx, player.rect.centery, arvores)
        # ou uma lógica de movimento específica.
        # Use self.is_stuck e self._stuck_timer para implementar o desvio.

        # Exemplo BÁSICO de como uma classe derivada PODE usar a detecção de estar preso:
        # No método update da CLASSE DERIVADA:
        # if self.esta_vivo() and player is not None and hasattr(player, 'esta_vivo') and player.esta_vivo():
        #    current_ticks = pygame.time.get_ticks()
        #
        #    # Se estiver preso por tempo suficiente e não estiver tentando desviar
        #    if self.is_stuck and current_ticks - self._stuck_timer > self._stuck_duration_threshold and self._evade_direction is None:
        #       # Inicia uma tentativa de desvio
        #       self._evade_direction = random.choice(["left", "right", "up", "down"]) # Escolhe uma direção aleatória para tentar desviar
        #       self._evade_timer = current_ticks
        #       # print(f"{type(self).__name__} preso! Tentando desviar para {self._evade_direction}") # Debug de desvio
        #
        #    # Se estiver tentando desviar
        #    if self._evade_direction is not None:
        #       # Calcula o movimento de desvio
        #       evade_speed = self.velocidade * 1.5 # Pode desviar mais rápido
        #       evade_dx, evade_dy = 0, 0
        #       if self._evade_direction == "left":
        #          evade_dx = -evade_speed
        #       elif self._evade_direction == "right":
        #          evade_dx = evade_speed
        #       elif self._evade_direction == "up":
        #          evade_dy = -evade_speed
        #       elif self._evade_direction == "down":
        #          evade_dy = evade_speed
        #
        #       # Aplica o movimento de desvio (sem verificar colisão com árvores durante o desvio simples)
        #       # É importante atualizar a posição do rect principal aqui
        #       self.rect.x += evade_dx
        #       self.rect.y += evade_dy
        #       # Atualiza a posição da hitbox de colisão do inimigo também
        #       if hasattr(self, 'collision_rect'):
        #            self.collision_rect.centerx = self.rect.centerx
        #            self.collision_rect.bottom = self.rect.bottom
        #
        #       # Verifica se a duração do desvio terminou
        #       if current_ticks - self._evade_timer > self._evade_duration:
        #          self._evade_direction = None # Termina a tentativa de desvio
        #          self.is_stuck = False # Considera que não está mais preso (pode ser reavaliado no próximo frame)
        #          # print(f"{type(self).__name__} terminou tentativa de desvio.") # Debug de desvio
        #
        #    else:
        #       # Se não estiver tentando desviar, move normalmente em direção ao jogador (com verificação de colisão da base)
        #       target_x, target_y = player.rect.centerx, player.rect.centery
        #       self.mover_em_direcao(target_x, target_y, arvores) # Chama o método da base com a lista de árvores
        #
        #    # Lógica de ataque (chame o método atacar se o inimigo tiver um)
        #    if hasattr(self, 'atacar'):
        #        self.atacar(player)
        #
        #    # Lógica de animação (chame o método atualizar_animacao se o inimigo tiver um)
        #    if hasattr(self, 'atualizar_animacao'):
        #        self.atualizar_animacao()
        #
        # else:
        #     # print(f"DEBUG(Inimigo Base Update): {type(self).__name__} ou player não está vivo. Não atualizando IA.") # Debug removido
        #     pass # Não atualiza a IA se o inimigo ou jogador não estiver vivo


        pass # Implementação real da IA deve estar nas classes derivadas


    def check_player_collision(self, player):
        """
        Verifica colisão com o jogador, aplica dano de contato e empurra o jogador.

        Args:
            player (Player): O objeto jogador.
        """
        # Verifica se o inimigo está vivo e se o jogador existe e tem um rect e vida
        if self.esta_vivo() and player is not None and hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo():
            # Obtém o retângulo de colisão do jogador (preferindo rect_colisao si existir)
            player_rect_colisao = getattr(player, 'rect_colisao', getattr(player, 'rect', None))

            # Verifica colisão entre o rect principal do inimigo e o retângulo de colisão do jogador
            # Usamos o rect principal do inimigo para colisão com o jogador,
            # a menos que você defina uma hitbox específica para colisão inimigo-jogador.
            if player_rect_colisao is not None and self.rect.colliderect(player_rect_colisao):
                agora = pygame.time.get_ticks()
                # Verifica si o cooldown de contato passou
                if agora - self.last_contact_time >= self.contact_cooldown:
                    # Aplica dano de contato ao jogador (se o jogador tiver o método receber_dano)
                    if hasattr(player, 'receber_dano'):
                         player.receber_dano(self.contact_damage)

                    # Calcula o vetor de empurrão do inimigo para o jogador
                    push_vector_x = player_rect_colisao.centerx - self.rect.centerx
                    push_vector_y = player_rect_colisao.centery - self.rect.centery
                    distance = math.hypot(push_vector_x, push_vector_y)

                    if distance > 0: # Evita divisão por zero
                        push_dir_x = push_vector_x / distance
                        push_dir_y = push_vector_y / distance

                        # Aplica o empurrão ao jogador (se o jogador tiver o método aplicar_empurrao)
                        if hasattr(player, 'aplicar_empurrao'):
                             player.aplicar_empurrao(push_dir_x * self.push_force, push_dir_y * self.push_force, self.push_duration)

                    self.last_contact_time = agora # Atualiza o tempo do último contato
            # else:
                 # print("AVISO(Inimigo Base - Colisão Player): Objeto player_rect_colisao é None ou inimigo/player não está vivo.") # Debug removido


    def desenhar(self, janela, camera_x, camera_y):
        """
        Desenha o inimigo na janela, aplicando o offset da câmera.
        Opcional: Desenha a hitbox de colisão para debug.

        Args:
            janela (pygame.Surface): A superfície onde desenhar.
            camera_x (int): O offset x da câmera.
            camera_y (int): O offset y da câmera.
        """
        # Desenha a imagem do inimigo na posição corrigida pela câmera
        janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

        # >>> Opcional: Desenhar a hitbox de colisão reduzida para visualização <<<
        # Verifica si a hitbox de colisão do inimigo existe
        # if hasattr(self, 'collision_rect'):
        #     # Cria um retângulo visual com o offset da câmera
        #     collision_rect_on_screen = pygame.Rect(self.collision_rect.x - camera_x, self.collision_rect.y - camera_y, self.collision_rect.width, self.collision_rect.height)
        #     # Desenha o retângulo azul (ou outra cor para distinguir)
        #     pygame.draw.rect(janela, (0, 0, 255), collision_rect_on_screen, 1) # Desenha um retângulo azul de 1 pixel de largura


    def esta_vivo(self):
        """Retorna True se o inimigo estiver vivo."""
        # Verifica si o inimigo tem o atributo hp antes de verificar
        if hasattr(self, 'hp'):
             return self.hp > 0 # Assume que o inimigo está vivo se HP > 0
        return False # Retorna False si o atributo hp não existir

    def receber_dano(self, dano):
        """
        Método para receber dano.
        As classes derivadas podem sobrescrever este método para adicionar efeitos (animação de dano, etc.).
        """
        if self.esta_vivo(): # Só recebe dano si estiver vivo
            self.hp -= dano
            # print(f"DEBUG(Inimigo Base): {type(self).__name__} recebeu {dano} de dano. HP restante: {self.hp}") # Debug removido
            if self.hp <= 0:
                self.hp = 0 # Garante que HP não seja negativo
                # print(f"DEBUG(Inimigo Base): {type(self).__name__} morreu.") # Debug removido
                self.kill() # Remove o sprite de todos os grupos (se estiver em grupos)
                # A remoção da lista no gerenciador de inimigos é feita no GerenciadorDeInimigos.update_inimigos.


# No seu loop principal do jogo (Game.py), você precisará:
# 1. Passar a lista de árvores para o método update_inimigos do GerenciadorDeInimigos.
# 2. No método update_inimigos, passar a lista de árvores para o método update de cada inimigo.
# 3. Certificar-se de que a classe Player tem um método 'aplicar_empurrao(push_x, push_y, duration_ms)'.
# 4. Implementar a lógica de desvio específica no método update de cada classe de inimigo derivada,
#    usando os atributos self.is_stuck, self._stuck_timer, self._stuck_duration_threshold,
#    self._evade_direction, self._evade_timer, self._evade_duration.
