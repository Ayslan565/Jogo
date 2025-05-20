# BonecoDeNeve.py
import time
import random
import pygame
import math # Importe math se for usado para cooldowns ou outras lógicas de tempo
import os # Importa os para verificar a existência de arquivos

# Importa a classe base Inimigo do ficheiro Inimigos.py
# Certifique-se de que o ficheiro Inimigos.py está na mesma pasta ou num caminho acessível
from Inimigos import Inimigo


# Importa a nova classe de projétil
try:
    # Certifique-se de que o nome do arquivo e da classe estão corretos
    from Projetil_BolaNeve import ProjetilNeve
except ImportError:
    ProjetilNeve = None # Define como None se a importação falhar


"""
Classe para o inimigo Boneco de Neve.
Herda da classe base Inimigo.
"""
class BonecoDeNeve(Inimigo):
    """
    Representa um inimigo Boneco de Neve.
    Persegue o jogador quando este está vivo e dentro do alcance (se aplicável).
    Atira projéteis de neve no jogador.
    Implementa lógica de desvio quando preso.
    """
    # Variável de classe para armazenar os sprites carregados uma única vez
    sprites_carregados = None
    # Adiciona uma variável de classe para armazenar os sprites originais (não flipados)
    sprites_originais = None # Adicionado para armazenar sprites originais

    def __init__(self, x, y, velocidade=1.0): # Velocidade padrão do Boneco de Neve
        """
        Inicializa um novo objeto BonecoDeNeve.

        Args:
            x (int): A posição inicial x do boneco de neve.
            y (int): A posição inicial y do boneco de neve.
            velocidade (float): A velocidade de movimento do boneco de neve.
        """
        # Carrega os sprites apenas uma vez para todas as instâncias de BonecoDeNeve
        if BonecoDeNeve.sprites_originais is None: # Carrega na variável de sprites_originais
            caminhos = [
                # AJUSTE ESTES CAMINHOS PARA OS SEUS ARQUIVOS DE SPRITE DO BONECO DE NEVE
                "Sprites/Inimigos/Boneco de Neve/Boneco De Neve 1.png", # Corrigido a barra invertida
                "Sprites/Inimigos/Boneco de Neve/Boneco de Neve 2.png", # Corrigido a barra invertida
                "Sprites/Inimigos/Boneco de Neve/Boneco de Neve 3.png", # Corrigido a barra invertida
                # Adicione mais caminhos de sprite de animação aqui
            ]
            BonecoDeNeve.sprites_originais = [] # Inicializa a lista de sprites originais
            tamanho_sprite_desejado = (64, 64) # AJUSTE O TAMANHO DESEJADO PARA O SPRITE DO BONECO DE NEVE

            for path in caminhos:
                try:
                    if os.path.exists(path): # Verifica se o arquivo existe
                        sprite = pygame.image.load(path).convert_alpha()
                        # Redimensiona sprites para o tamanho desejado
                        sprite = pygame.transform.scale(sprite, tamanho_sprite_desejado)
                        BonecoDeNeve.sprites_originais.append(sprite) # Adiciona aos sprites originais
                    else:
                       # Se o arquivo não existir, adicione um placeholder
                       placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                       pygame.draw.rect(placeholder, (0, 255, 255), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1])) # Cyan placeholder
                       fonte = pygame.font.Font(None, 20)
                       texto_erro = fonte.render("Sprite", True, (0, 0, 0))
                       placeholder.blit(texto_erro, (5, 15))
                       texto_erro2 = fonte.render("Erro", True, (0, 0, 0))
                       placeholder.blit(texto_erro2, (10, 35))
                       BonecoDeNeve.sprites_originais.append(placeholder) # Adiciona o placeholder aos sprites originais

                except pygame.error as e:
                    # Se um sprite falhar, adicione um placeholder com o tamanho correto
                    placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (0, 255, 255), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1])) # Cyan placeholder
                    fonte = pygame.font.Font(None, 20)
                    texto_erro = fonte.render("Sprite", True, (0, 0, 0))
                    placeholder.blit(texto_erro, (5, 15))
                    texto_erro2 = fonte.render("Erro", True, (0, 0, 0))
                    placeholder.blit(texto_erro2, (10, 35))
                    BonecoDeNeve.sprites_originais.append(placeholder) # Adiciona o placeholder aos sprites originais

            # Certifique-se de que há pelo menos um sprite carregado
            if not BonecoDeNeve.sprites_originais:
                tamanho_sprite_desejado = (64, 64) # Tamanho do placeholder si nenhum sprite carregar
                placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (0, 255, 255), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1]))
                BonecoDeNeve.sprites_originais.append(placeholder) # Adiciona o placeholder aos sprites originais


        # Inicializa a classe base Inimigo PASSANDO A PRIMEIRA SURFACE CARREGADA E A VELOCIDADE.
        # Certifique-se de que BonecoDeNeve.sprites_originais não está vazio antes de acessar o índice [0]
        initial_image = BonecoDeNeve.sprites_originais[0] if BonecoDeNeve.sprites_originais else pygame.Surface((64, 64), pygame.SRCALPHA) # Usa placeholder se a lista estiver vazia
        super().__init__(x, y, initial_image, velocidade) # Passa a velocidade para a classe base


        self.hp = 100 # Pontos de vida do boneco de neve
        self.max_hp = self.hp # Define HP máximo para barra de vida
        # self.velocidade é definido na classe base agora
        self.sprites = BonecoDeNeve.sprites_originais # Referência à lista de sprites originais carregados
        self.sprite_index = 0 # Índice do sprite atual para animação
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Tempo do último update da animação
        self.intervalo_animacao = 200 # milissegundos entre frames de animação (ajuste para a velocidade da animação)


        # Atributos de Combate do Boneco de Neve
        self.is_attacking = False # Flag para indicar si o boneco de neve está atacando
        self.attack_duration = 0.5 # Duração da animação de ataque (ajuste conforme a animação)
        self.attack_timer = 0 # Tempo em que o ataque começou (usando time.time())
        self.attack_damage = 15 # Quantidade de dano causado pelo ataque (dano de ataque específico)
        # Define o tamanho da hitbox de ataque - AJUSTE ESTES VALORES PARA REDUZIR O TAMANHO
        self.attack_hitbox_size = (40, 40) # Exemplo: hitbox 40x40 pixels
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Retângulo para a hitbox de ataque (inicialmente vazio)
        self.attack_range = 200 # Alcance para iniciar o ataque (distância do centro do inimigo ao centro do jogador) - Aumentado para ataque de projétil
        self.attack_cooldown = 2 # Tempo de espera entre ataques em segundos (ajuste)
        self.last_attack_time = time.time() # Tempo em que o último ataque ocorreu (usando time.time())
        # self.hit_by_player_this_attack é herdado da classe base

        # Atributo para rastrear a direção horizontal para espelhamento
        self.facing_right = True # True si estiver virado para a direita, False para a esquerda

        # Atributo para rastrear a direção do boneco de neve (para posicionar a hitbox de ataque)
        # Inicializa com uma direção padrão, será atualizado no mover_em_direcao
        self.direction = "down"

        # Flag para rastrear si foi atingido pelo ataque do jogador neste ciclo de ataque do jogador (já na base)
        # self.hit_by_player_this_attack = False

        # Atributos para Dano por Contato
        self.contact_damage = 10 # Dano de contato (ajuste)
        self.contact_cooldown = 1000 # Cooldown de dano de contato em milissegundos (ajuste)
        self.last_contact_time = pygame.time.get_ticks() # Tempo do último contato (em milissegundos)

        # Atributos para Projéteis
        self.projectile_cooldown = 1.5 # Tempo em segundos entre lançamentos de projéteis (ajuste)
        self.last_projectile_time = time.time() # Tempo do último lançamento de projétil

        # NOVO: Atributo para rastrear a posição anterior para verificar movimento (herdado da base)
        # self._previous_pos = (self.rect.x, self.rect.y)
        # Atributos para detecção de estar preso e lógica de desvio (herdado da classe base)
        # self.is_stuck = False
        # self._stuck_timer = 0
        # self._stuck_duration_threshold = 500
        # self._evade_direction = None
        # self._evade_timer = 0
        # self._evade_duration = 500


    # Adicionado o método esta_vivo() para compatibilidade com o sistema de combate (já na base)
    # def esta_vivo(self):
    #     """Retorna True si o inimigo estiver vivo, False caso contrário."""
    #     return self.hp > 0 # Retorna o valor do atributo

    def receber_dano(self, dano):
        """
        Reduz a vida do inimigo pela quantidade de dano especificada.

        Args:
            dano (int): A quantidade de dano a ser recebida.
        """
        # Verifica si o inimigo está vivo antes de receber dano
        if self.esta_vivo(): # Chama o método esta_vivo()
            self.hp -= dano
            if self.hp <= 0:
                self.hp = 0 # Garante que a vida não fica negativa
                # A remoção da lista no gerenciador de inimigos é feita no GerenciadorDeInimigos.update_inimigos.
                # Opcional: self.kill() pode ser chamado aqui se estiver usando grupos de sprites.


    def atualizar_animacao(self):
        """Atualiza o índice do sprite para a animação e aplica o flip horizontal."""
        agora = pygame.time.get_ticks()

        # >>> Lógica de Animação Invertida: Anima apenas quando estiver a mover <<<
        # Verifica se o boneco de neve está a mover (posição atual diferente da anterior)
        is_moving = (self.rect.x != self._previous_pos[0] or self.rect.y != self._previous_pos[1])

        if self.sprites and self.esta_vivo(): # Verifica se há sprites e se está vivo
            if is_moving:
                # Se estiver a mover, atualiza o frame da animação no intervalo definido
                if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                    self.tempo_ultimo_update_animacao = agora
                    # Incrementa o índice do sprite para a animação de movimento
                    self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            else:
                # Se estiver parado, reseta o índice do sprite para o primeiro frame (idle)
                self.sprite_index = 0 # Mantém no primeiro frame quando parado

            # Define a imagem atual com base no índice
            base_image = self.sprites[int(self.sprite_index % len(self.sprites))]

            # Aplica o flip horizontal si não estiver virado para a direita
            # Assumindo que o sprite base está virado para a direita.
            if not self.facing_right:
                self.image = pygame.transform.flip(base_image, True, False)
            else:
                self.image = base_image
        else:
            # Fallback si não houver sprites ou não estiver vivo
            tamanho_sprite_desejado = (64, 64) # Tamanho do placeholder
            self.image = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (0, 255, 255), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1]))


    # Sobrescreve o método mover_em_direcao para adicionar a lógica de direção horizontal
    # CORRIGIDO: Adicionado 'arvores' como argumento para compatibilidade com a classe base
    def mover_em_direcao(self, alvo_x, alvo_y, arvores):
        """
        Move o boneco de neve em direção a um alvo e atualiza a direção horizontal,
        verificando colisão com árvores.

        Args:
            alvo_x (int): A coordenada x do alvo.
            alvo_y (int): A coordenada y do alvo.
            arvores (list): Uma lista de objetos Arvore para verificar colisão.
        """
        # Chama o método mover_em_direcao da classe base para lidar com o movimento e colisão com árvores
        # A lógica de detecção de estar preso e atualização de self.is_stuck ocorre na classe base.
        super().mover_em_direcao(alvo_x, alvo_y, arvores)

        # Atualiza a direção horizontal com base no movimento em X, apenas se o Boneco de Neve se moveu
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


    # Modificado para incluir lógica de lançamento de projéteis
    def atacar(self, player, lista_projeteis):
        """
        Implementa a lógica de ataque do boneco de neve.
        Atira um projétil de neve no jogador se o cooldown permitir e o jogador estiver no alcance.

        Args:
            player (Player): O objeto jogador para verificar o alcance de ataque e obter a posição.
            lista_projeteis (list): A lista onde os projéteis ativos são armazenados.
        """
        # Adiciona verificação para garantir que o objeto player tem o atributo rect
        if not hasattr(player, 'rect'):
            return # Sai do método para evitar o erro

        current_time = time.time()
        # Verifica se o cooldown de projétil passou e se o jogador está dentro do alcance de ataque
        # E se o boneco de neve está vivo
        if self.esta_vivo() and (current_time - self.last_projectile_time >= self.projectile_cooldown):
            # Calcula a distância até o jogador
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                             self.rect.centery - player.rect.centery)

            if distancia_ao_jogador <= self.attack_range:
                # Lança um projétil de neve
                # Verifica si a classe ProjetilNeve foi importada com sucesso
                if ProjetilNeve is not None:
                    # Cria uma nova instância de ProjetilNeve na posição do boneco de neve
                    # e mirando na posição atual do jogador
                    novo_projetil = ProjetilNeve(self.rect.centerx, self.rect.centery,
                                                 player.rect.centerx, player.rect.centery)
                    lista_projeteis.append(novo_projetil) # Adiciona o projétil à lista
                    self.last_projectile_time = current_time # Reseta o cooldown do projétil
                else:
                    pass # Aviso já é dado na importação


    # O método update agora recebe o objeto Player completo E a lista de projéteis E a lista de árvores
    # CORRIGIDO: Adicionado 'arvores' como argumento
    def update(self, player, arvores, lista_projeteis, tela_largura, tela_altura):
        """
        Atualiza o estado do boneco de neve (movimento, animação e ataque/lançamento de projétil).
        Inclui a lógica de aplicação de dano por contato e desvio.

        Args:
            player (Player): O objeto jogador para seguir, verificar o alcance de ataque e aplicar dano.
            arvores (list): Uma lista de objetos Arvore para colisão.
            lista_projeteis (list): A lista onde os projéteis ativos são armazenados (passada para o método atacar).
            tela_largura (int): Largura da tela (passada para a atualização dos projéteis).
            tela_altura (int): Altura da tela (passada para a atualização dos projéteis).
        """
        # Adiciona verificação para garantir que o objeto player tem os atributos necessários
        # Verifica si o player tem pelo menos rect e vida (para verificar si está vivo e receber dano)
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            return # Sai do método para evitar o erro

        # Só atualiza si estiver vivo
        if self.esta_vivo():
            current_time = time.time()
            current_ticks = pygame.time.get_ticks() # Usando get_ticks() para consistência com contact_cooldown

            # Lógica de colisão com o jogador e dano por contato (herdado da classe base)
            self.check_player_collision(player)

            # Lógica do temporizador de ataque específico (não usado para este inimigo, mas mantido por consistência)
            if self.is_attacking:
                 # Verifica si a duração do ataque passou
                 if time.time() - self.attack_timer >= self.attack_duration: # Usa time.time() para consistência com attack_timer
                     self.is_attacking = False
                     self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Reseta a hitbox quando o ataque termina
                     self.hit_by_player_this_attack = False # Reseta a flag de acerto ao final do ataque específico
                 else:
                      # Lógica de Dano do Ataque Específico (VERIFICADA DURANTE A ANIMAÇÃO DE ATAQUE)
                      if not self.hit_by_player_this_attack and \
                             hasattr(self, 'attack_hitbox') and \
                             hasattr(player, 'rect') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                             self.attack_hitbox.colliderect(player.rect): # >>> CORREÇÃO AQUI: Usa player.rect <<<

                           # Verifica si o jogador tem o método receber_dano e está vivo
                           if hasattr(player, 'receber_dano'):
                                # Aplica dano do ataque específico ao jogador
                                dano_inimigo = getattr(self, 'attack_damage', 0) # Pega attack_damage ou 0 si não existir
                                player.receber_dano(dano_inimigo)
                                self.hit_by_player_this_attack = True # Define a flag para não acertar novamente neste ataque específico
                                # Opcional: Adicionar um som ou efeito visual quando o inimigo acerta o jogador com ataque específico


            # >>> Lógica de Movimento e Desvio <<<
            # O boneco de neve persegue o jogador si estiver vivo e o jogador estiver vivo.
            # Implementa a lógica de desvio quando detecta que está preso.
            player_tem_rect = hasattr(player, 'rect')
            player_esta_vivo = hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo()
            boneco_esta_vivo = self.esta_vivo()
            boneco_tem_velocidade = self.velocidade > 0

            if boneco_esta_vivo and player_tem_rect and player_esta_vivo and boneco_tem_velocidade:
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


            # Tenta lançar um projétil (chamando o método atacar)
            # Passa a lista de projéteis para que o método atacar possa adicionar o novo projétil
            self.atacar(player, lista_projeteis)


            # Posicionamento da Hitbox de Ataque Específico (Mantido, mas pode não ser usado para ataque de projétil)
            # A hitbox de ataque é posicionada em relação ao centro do boneco de neve.
            # Ajuste as coordenadas conforme a sua animação e alcance desejado.
            # A hitbox é posicionada independentemente de estar atacando ou não,
            # mas só é usada para aplicar dano quando is_attacking é True.
            attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0] # Pega a largura da hitbox ou um valor padrão
            attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1] # Pega a altura da hitbox ou um valor padrão
            self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
            self.attack_hitbox.center = self.rect.center # Centraliza a hitbox no boneco de neve


            # Atualiza a animação (inclui o flip horizontal)
            self.atualizar_animacao()

            # NOVO: Atualiza a posição anterior após o movimento para o próximo frame (herdado da base)
            # self._previous_pos = (self.rect.x, self.rect.y)


    # O método desenhar() é herdado da classe base Inimigo e deve funcionar
    # se a classe base tiver um método desenhar que aceita surface, camera_x, camera_y.
    # Não precisamos sobrescrever desenhar aqui, pois o flip é aplicado no atualizar_animacao

    # O método receber_dano() é herdado da classe base Inimigo.
