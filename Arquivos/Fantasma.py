# Fantasma.py
import time
import pygame
import random
import math

# Importa a classe base Inimigo do ficheiro Inimigos.py
# Certifique-se de que o ficheiro Inimigos.py está na mesma pasta ou num caminho acessível
# Removido o bloco try-except ImportError conforme solicitado anteriormente
from Inimigos import Inimigo


"""
Classe para o inimigo Fantasma.
Herda da classe base Inimigo.
"""
class Fantasma(Inimigo):
    """
    Representa um inimigo Fantasma.
    Persegue o jogador quando este está vivo e dentro do alcance (se aplicável).
    Pode passar através de obstáculos como árvores.
    """
    # Variável de classe para armazenar os sprites carregados uma única vez
    sprites_carregados = None

    def __init__(self, x, y, velocidade=1.5): # Velocidade padrão do Fantasma
        """
        Inicializa um novo objeto Fantasma.

        Args:
            x (int): A posição inicial x do fantasma.
            y (int): A posição inicial y do fantasma.
            velocidade (float): A velocidade de movimento do fantasma.
        """
        # Carrega os sprites apenas uma vez para todas as instâncias de Fantasma
        if Fantasma.sprites_carregados is None:
            caminhos = [
                # >>> AJUSTE ESTES CAMINHOS PARA OS SEUS ARQUIVOS DE SPRITE DO FANTASMA <<<
                "Sprites/Inimigos/Fantasma/Fantasma1.png",
                "Sprites/Inimigos/Fantasma/Fantasma2.png",
                "Sprites/Inimigos/Fantasma/Fantasma3.png",
                # Adicione mais caminhos de sprite de animação aqui
            ]
            Fantasma.sprites_carregados = []
            tamanho_sprite_desejado = (60, 80) # >>> AJUSTE O TAMANHO DESEJADO PARA O SPRITE DO FANTASMA <<<

            for path in caminhos:
                try:
                    sprite = pygame.image.load(path).convert_alpha()
                    # Redimensiona o sprite para o tamanho desejado
                    sprite = pygame.transform.scale(sprite, tamanho_sprite_desejado)
                    Fantasma.sprites_carregados.append(sprite)
                except pygame.error as e:
                    # Se um sprite falhar, adicione um placeholder
                    placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (0, 0, 255), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1])) # Blue placeholder
                    fonte = pygame.font.Font(None, 20)
                    texto_erro = fonte.render("Sprite", True, (255, 255, 255))
                    placeholder.blit(texto_erro, (5, 15))
                    texto_erro2 = fonte.render("Erro", True, (255, 255, 255))
                    placeholder.blit(texto_erro2, (10, 35))
                    Fantasma.sprites_carregados.append(placeholder)

            # Certifique-se de que há pelo menos um sprite carregado
            if not Fantasma.sprites_carregados:
                tamanho_sprite_desejado = (60, 80) # Tamanho do placeholder si nenhum sprite carregar
                placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (0, 0, 255), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1]))
                Fantasma.sprites_carregados.append(placeholder)


        # Inicializa a classe base Inimigo PASSANDO A PRIMEIRA SURFACE CARREGADA E A VELOCIDADE.
        # Certifique-se de que Fantasma.sprites_carregados não está vazio antes de acessar o índice [0]
        initial_image = Fantasma.sprites_carregados[0] if Fantasma.sprites_carregados else pygame.Surface((60, 80), pygame.SRCALPHA) # Usa placeholder se a lista estiver vazia
        super().__init__(x, y, initial_image, velocidade) # >>> Passa a velocidade para a classe base <<<

        # >>> Inicializa os atributos de combate <<<
        self.is_attacking = False # Flag para indicar si o fantasma está atacando
        self.attack_duration = 0.8 # Duração da animação de ataque (ajuste)
        self.attack_timer = 0 # Tempo em que o ataque começou (usando time.time())
        self.attack_damage = 10 # Dano do ataque
        self.attack_range = 80 # Alcance do ataque do fantasma
        self.attack_cooldown = 3 # Cooldown do ataque em segundos
        self.last_attack_time = time.time() # Tempo do último ataque
        # Inicializa a hitbox de ataque (pode ser um retângulo vazio inicialmente)
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.hit_by_player_this_attack = False # Flag para controle de hit por ataque do jogador (herdado, mas bom inicializar)

        self.hp = 50 # Pontos de vida do fantasma (ajuste conforme necessário)
        # self.velocidade é definido na classe base agora
        self.sprites = Fantasma.sprites_carregados # Referência à lista de sprites carregados
        self.sprite_index = 0 # Índice do sprite atual para animação
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Tempo do último update da animação
        self.intervalo_animacao = 150 # milissegundos entre frames de animação (ajuste para a velocidade da animação)

        # Atributos para Dano por Contato (se o fantasma causar dano ao toque)
        self.contact_damage = 3 # Dano de contato (ajuste)
        self.contact_cooldown = 500 # Cooldown de dano de contato em milissegundos (ajuste)
        self.last_contact_time = pygame.time.get_ticks() # Tempo do último contato (em milissegundos)


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
                self.hp = 0
                # A remoção da lista no gerenciador de inimigos é feita no GerenciadorDeInimigos.update_inimigos.
                # Opcional: self.kill() pode ser chamado aqui se estiver usando grupos de sprites.


    def atualizar_animacao(self):
        """Atualiza o sprite para a animação."""
        agora = pygame.time.get_ticks()
        # Verifica si self.sprites não está vazio antes de calcular o módulo
        if self.sprites and self.esta_vivo() and agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao: # Só anima si estiver vivo
            self.tempo_ultimo_update_animacao = agora
            # Incrementa o índice do sprite
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            # Define a imagem atual com base no novo índice
            self.image = self.sprites[self.sprite_index] # Acessa o sprite com o índice inteiro
            # Opcional: Redimensionar a imagem atualizada se necessário (mas já redimensionamos no carregamento)
            # self.image = pygame.transform.scale(self.image, (60, 80))
        elif not self.esta_vivo() and self.sprites:
             # Si morreu, pode definir um sprite de morte ou manter o último frame
             # Por enquanto, mantém o último frame ou o primeiro si a lista estiver vazia
             if self.sprites:
                 self.image = self.sprites[int(self.sprite_index % len(self.sprites))] # Mantém o último frame (garante índice válido)
             else:
                  # Fallback si não houver sprites
                  tamanho_sprite_desejado = (60, 80) # Tamanho do placeholder
                  self.image = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                  pygame.draw.rect(self.image, (0, 0, 255), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1]))


    # Sobrescreve o método mover_em_direcao para que o fantasma ignore colisões com árvores
    # CORRIGIDO: Adicionado 'arvores' como argumento para compatibilidade com a chamada no GerenciadorDeInimigos
    def mover_em_direcao(self, alvo_x, alvo_y, arvores):
        """
        Move o fantasma na direção de um ponto alvo, IGNORANDO colisões com árvores.

        Args:
            alvo_x (int): A coordenada x do ponto alvo.
            alvo_y (int): A coordenada y do ponto alvo.
            arvores (list): Uma lista de objetos Arvore (ignorada pelo fantasma).
        """
        # Só move si estiver vivo e tiver velocidade
        if self.esta_vivo() and self.velocidade > 0:
            dx = alvo_x - self.rect.centerx
            dy = alvo_y - self.rect.centery
            distancia = math.hypot(dx, dy)

            if distancia > 0:
                dx_norm = dx / distancia
                dy_norm = dy / distancia
                self.rect.x += dx_norm * self.velocidade
                self.rect.y += dy_norm * self.velocidade

            # Não há verificação de colisão com árvores aqui, permitindo que o fantasma as transpasse.


    def atacar(self, player):
        """
        Implementa a lógica de ataque do fantasma.
        Neste exemplo, um ataque simples de contato ou projétil (se aplicável).

        Args:
            player (Player): O objeto jogador para verificar o alcance de ataque.
        """
        # Adiciona verificação para garantir que o objeto player tem o atributo rect
        if not hasattr(player, 'rect'):
            return # Sai do método para evitar o erro

        current_time = time.time()
        # Verifica se o cooldown passou e se o jogador está dentro do alcance de ataque
        # E se o fantasma está vivo
        if self.esta_vivo() and (current_time - self.last_attack_time >= self.attack_cooldown):
            # Calcula a distância até o jogador
            # >>> CORREÇÃO AQUI: Usa player.rect.centerx e player.rect.centery <<<
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                              self.rect.centery - player.rect.centery)

            if distancia_ao_jogador <= self.attack_range:
                # Inicia o ataque
                self.is_attacking = True
                self.attack_timer = current_time # Registra o tempo de início do ataque
                self.last_attack_time = current_time # Reseta o cooldown
                self.hit_by_player_this_attack = False # Reseta a flag de acerto para este novo ataque

                # Define a hitbox de ataque (exemplo: um retângulo ao redor do fantasma para ataque de contato)
                # Você precisará ajustar isso com base na animação ou tipo de ataque do seu fantasma
                attack_hitbox_width = self.rect.width # Largura da hitbox igual à do fantasma
                attack_hitbox_height = self.rect.height # Altura da hitbox igual à do fantasma

                # Posiciona a hitbox de ataque (exemplo: centralizada no fantasma)
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                self.attack_hitbox.center = self.rect.center # Centraliza a hitbox no fantasma


    # >>> CORREÇÃO: O método update agora recebe o objeto Player completo E a lista de árvores <<<
    # CORRIGIDO: Adicionado 'arvores' como argumento
    def update(self, player, arvores):
        """
        Atualiza o estado do fantasma (movimento, animação e ataque).
        Inclui a lógica de aplicação de dano por contato.

        Args:
            player (Player): O objeto jogador para seguir, verificar o alcance de ataque e aplicar dano.
            arvores (list): Uma lista de objetos Arvore (passada pelo GerenciadorDeInimigos, mas ignorada para movimento).
        """
        # >>> Adiciona verificação para garantir que o objeto player tem os atributos necessários <<<
        # Verifica se o player tem pelo menos rect e vida (para verificar se está vivo e receber dano)
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            return # Sai do método para evitar o erro

        # Só atualiza si estiver vivo
        if self.esta_vivo():
            current_time = time.time()
            current_ticks = pygame.time.get_ticks() # Usando get_ticks() para consistência com contact_cooldown

            # >>> Lógica de Dano por Contato <<<
            # Verifica si o fantasma está vivo, si colide com o rect do jogador,
            # e si o cooldown de contato passou.
            # Adiciona verificação para garantir que player.vida existe e é válido
            if self.esta_vivo() and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
               hasattr(player, 'rect') and self.rect.colliderect(player.rect) and \
               (current_ticks - self.last_contact_time >= self.contact_cooldown): # Cooldown em milissegundos

                # Aplica dano por contato ao jogador
                # Verifica si o jogador tem o método receber_dano
                if hasattr(player, 'receber_dano'):
                    player.receber_dano(self.contact_damage)
                    self.last_contact_time = current_ticks # Atualiza o tempo do último contato (em milissegundos)
                    # Opcional: Adicionar um som ou efeito visual para dano por contato


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


            # >>> Lógica de Perseguição (Movimento) <<<
            # O fantasma persegue o jogador si estiver vivo e o jogador estiver vivo.
            # Adiciona verificação para garantir que player tem rect antes de passar para mover_em_direcao
            if self.esta_vivo() and hasattr(player, 'rect') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo():
                 # Move o fantasma na direção do centro do retângulo do jogador
                 # CORRIGIDO: Passando a lista de árvores para mover_em_direcao, mas o método sobrescrito a ignora
                 self.mover_em_direcao(player.rect.centerx, player.rect.centery, arvores)
            else:
                 pass # Não move si o player não tiver rect ou não estiver vivo


            # Tenta iniciar um ataque específico (verificado após o movimento)
            # A função atacar também tem uma verificação interna agora
            self.atacar(player)

            # >>> Posicionamento da Hitbox de Ataque Específico (Atualiza mesmo se não estiver atacando ativamente) <<<
            # A hitbox de ataque é posicionada em relação ao centro do fantasma.
            # Ajuste as coordenadas conforme a sua animação e alcance desejado.
            # A hitbox é posicionada independentemente de estar atacando ou não,
            # mas só é usada para aplicar dano quando is_attacking é True.
            attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0] # Pega a largura da hitbox ou um valor padrão
            attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1] # Pega a altura da hitbox ou um valor padrão
            self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
            self.attack_hitbox.center = self.rect.center # Centraliza a hitbox no fantasma


            # Atualiza a animação
            self.atualizar_animacao()

    # O método desenhar() é herdado da classe base Inimigo e deve funcionar
    # se a classe base tiver um método desenhar que aceita surface, camera_x, camera_y.

    # O método receber_dano() é herdado da classe base Inimigo.
