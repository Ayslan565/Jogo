# Fenix.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()

# Importa a classe base Inimigo do ficheiro Inimigos.py
# Certifique-se de que o ficheiro Inimigos.py está na mesma pasta ou num caminho acessível
try:
    from Inimigos import Inimigo
except ImportError:
    print("DEBUG(Fenix): Aviso: Módulo 'Inimigos.py' não encontrado. Usando classe base Inimigo placeholder.")
    class Inimigo(pygame.sprite.Sprite):
        def __init__(self, x, y, image, velocidade=1):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y))
            self.hp = 100 # Vida padrão
            self.velocidade = velocidade # Velocidade padrão
            self.is_attacking = False # Flag de ataque padrão
            self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Hitbox de ataque padrão (vazia)
            self.hit_by_player_this_attack = False # Flag para controle de hit por ataque do jogador
            self.contact_damage = 5 # Dano de contato padrão
            self.contact_cooldown = 1000 # Cooldown de contato padrão (em milissegundos)
            self.last_contact_time = pygame.time.get_ticks() # Tempo do último contato
            self.max_hp = self.hp # Armazena HP máximo para barra de vida


        def receber_dano(self, dano):
            self.hp -= dano
            if self.hp <= 0:
                self.hp = 0 # Garante que a vida não fica negativa
                # print(f"DEBUG(Inimigo Base): Inimigo morreu.") # Debug
                # A remoção do inimigo da lista/grupo deve ser feita no GerenciadorDeInimigos
                # self.kill() # Pode ser chamado aqui se estiver usando grupos de sprites

        def update(self, player):
            pass

        def desenhar(self, surface, camera_x, camera_y):
            # Desenha o inimigo com o offset da câmera
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
            # Lógica de desenho da barra de vida removida

        def esta_vivo(self):
             return self.hp > 0

        def mover_em_direcao(self, alvo_x, alvo_y):
            if self.esta_vivo() and self.velocidade > 0:
                dx = alvo_x - self.rect.centerx
                dy = alvo_y - self.rect.centery
                distancia = math.hypot(dx, dy)

                if distancia > 0:
                    dx_norm = dx / distancia
                    dy_norm = dy / distancia
                    self.rect.x += dx_norm * self.velocidade
                    self.rect.y += dy_norm * self.velocidade

        # Método desenhar_barra_vida removido do placeholder

"""
Classe para o inimigo Fênix.
Herda da classe base Inimigo.
"""
class Fenix(Inimigo): # Nome da classe alterado para Fenix
    # Variável de classe para armazenar os sprites carregados uma única vez
    sprites_carregados = None

    def __init__(self, x, y, velocidade=3.0): # Velocidade padrão da Fênix (mais rápida que o Espantalho)
        """
        Inicializa um novo objeto Fênix.

        Args:
            x (int): A posição inicial x da Fênix.
            y (int): A posição inicial y da Fênix.
            velocidade (float): A velocidade de movimento da Fênix.
        """
        print(f"DEBUG(Fenix): Inicializando Fênix em ({x}, {y}) com velocidade {velocidade}.") # Debug inicialização

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
                    sprite = pygame.image.load(path).convert_alpha()
                    # Redimensiona sprites para o tamanho desejado
                    sprite = pygame.transform.scale(sprite, tamanho_sprite_desejado)
                    Fenix.sprites_carregados.append(sprite)
                except pygame.error as e:
                    print(f"DEBUG(Fenix): Erro ao carregar o sprite da Fênix: {path}")
                    print(f"DEBUG(Fenix): Detalhes do erro: {e}")
                    # Se um sprite falhar, adicione um placeholder com o tamanho correto
                    placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (255, 165, 0), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1])) # Orange placeholder
                    Fenix.sprites_carregados.append(placeholder)

            # Certifique-se de que há pelo menos um sprite carregado
            if not Fenix.sprites_carregados:
                print("DEBUG(Fenix): Aviso: Nenhum sprite da Fênix carregado. Usando placeholder padrão.")
                tamanho_sprite_desejado = (70, 70) # Tamanho do placeholder si nenhum sprite carregar
                placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255, 165, 0), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1]))
                Fenix.sprites_carregados.append(placeholder)


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


        # Atributo para rastrear a direção da Fênix (para posicionar a hitbox de ataque)
        self.direction = "down" # Pode ser útil para ataques direcionais


        # >>> Atributos para Dano por Contato <<<
        self.contact_damage = 5 # Dano de contato (ajuste)
        self.contact_cooldown = 300 # Cooldown de dano de contato em milissegundos (mais rápido)
        self.last_contact_time = pygame.time.get_ticks() # Tempo do último contato (em milissegundos)


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
            print(f"DEBUG(Fenix): Recebeu {dano} de dano. HP restante: {self.hp}") # Debug: Mostra dano recebido e HP restante
            if self.hp <= 0:
                self.hp = 0
                print(f"DEBUG(Fenix): Fênix morreu.") # Debug: Mostra que morreu
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
            # Define a imagem atual com base no índice
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


    # O método mover_em_direcao() é herdado da classe base Inimigo agora.
    # Se precisar de lógica de movimento específica para a Fênix, sobrescreva-o aqui.
    # Exemplo de sobrescrita (si necessário):
    # def mover_em_direcao(self, alvo_x, alvo_y):
    #     # Lógica de movimento específica da Fênix (talvez voando ou desviando)
    #     super().mover_em_direcao(alvo_x, alvo_y) # Chama o método da classe base


    def atacar(self, player):
        """
        Implementa a lógica de ataque da Fênix.
        Pode ser um ataque de mergulho, projétil de fogo, etc.

        Args:
            player (Player): O objeto jogador para verificar o alcance de ataque.
        """
        # Adiciona verificação para garantir que o objeto player tem o atributo rect
        if not hasattr(player, 'rect'):
            # print("DEBUG(Fenix): Objeto player passado para Fenix.atacar não tem atributo 'rect'.") # Debug
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
                print("DEBUG(Fenix): Fênix iniciou ataque!") # Debug

                # Define a hitbox de ataque (exemplo: uma área de dano de fogo ao redor da Fênix)
                # Você precisará ajustar isso com base na animação ou tipo de ataque da sua Fênix
                attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0] # Pega a largura da hitbox ou um valor padrão
                attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1] # Pega a altura da hitbox ou um valor padrão

                # Posiciona a hitbox de ataque (exemplo: centralizada na Fênix durante o ataque)
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                self.attack_hitbox.center = self.rect.center # Centraliza a hitbox na Fênix


    # O método update é herdado e sobrescrito aqui para incluir a lógica específica da Fênix
    def update(self, player):
        """
        Atualiza o estado da Fênix (movimento, animação e ataque).
        Inclui a lógica de aplicação de dano por contato.

        Args:
            player (Player): O objeto jogador para seguir, verificar o alcance de ataque e aplicar dano.
        """
        # print("DEBUG(Fenix): Update da Fênix chamado.") # Debug geral
        # >>> Adiciona verificação para garantir que o objeto player tem os atributos necessários <<<
        # Verifica si o player tem pelo menos rect e vida (para verificar si está vivo e receber dano)
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            # print("DEBUG(Fenix): Objeto player passado para Fenix.update não tem todos os atributos necessários.") # Debug
            return # Sai do método para evitar o erro

        # Só atualiza si estiver vivo
        if self.esta_vivo():
            # print(f"DEBUG(Fenix): Fênix está viva. HP: {self.hp}") # Debug
            current_time = time.time()
            current_ticks = pygame.time.get_ticks() # Usando get_ticks() para consistência com contact_cooldown

            # >>> Lógica de Dano por Contato <<<
            # Verifica si a Fênix está viva, si colide com o rect do jogador,
            # e si o cooldown de contato passou.
            # Adiciona verificação para garantir que player.vida existe e é válido
            if self.esta_vivo() and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
               hasattr(player, 'rect') and self.rect.colliderect(player.rect) and \
               (current_ticks - self.last_contact_time >= self.contact_cooldown): # Cooldown em milissegundos

                # Aplica dano por contato ao jogador
                # Verifica si o jogador tem o método receber_dano
                if hasattr(player, 'receber_dano'):
                    # print(f"DEBUG(Fenix): Colisão de contato! Fênix tocou no jogador. Aplicando {self.contact_damage} de dano.") # Debug
                    player.receber_dano(self.contact_damage)
                    self.last_contact_time = current_ticks # Atualiza o tempo do último contato (em milissegundos)
                    # Opcional: Adicionar um som ou efeito visual para dano por contato


            # Lógica do temporizador de ataque específico
            if self.is_attacking:
                 # print("DEBUG(Fenix): Fênix está atacando (ataque específico).") # Debug
                 # Verifica si a duração do ataque passou
                 if time.time() - self.attack_timer >= self.attack_duration: # Usa time.time() para consistência com attack_timer
                     self.is_attacking = False
                     self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Reseta a hitbox quando o ataque termina
                     self.hit_by_player_this_attack = False # Reseta a flag de acerto ao final do ataque específico
                     # print("DEBUG(Fenix): Ataque específico da Fênix terminou.") # Debug
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
                              # print(f"DEBUG(Fenix): Ataque específico acertou o jogador! Causou {dano_inimigo} de dano.") # Debug
                              player.receber_dano(dano_inimigo)
                              self.hit_by_player_this_attack = True # Define a flag para não acertar novamente neste ataque específico
                              # Opcional: Adicionar um som ou efeito visual quando o inimigo acerta o jogador com ataque específico


            # >>> Lógica de Perseguição (Movimento) <<<
            # A Fênix persegue o jogador si estiver vivo e o jogador estiver vivo.
            # Adiciona verificação para garantir que player tem rect antes de passar para mover_em_direcao
            player_tem_rect = hasattr(player, 'rect')
            player_esta_vivo = hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo()
            fenix_esta_viva = self.esta_vivo()
            fenix_tem_velocidade = self.velocidade > 0


            # print(f"DEBUG(Fenix): Player tem rect: {player_tem_rect}") # Debug: Verifica rect do player
            # print(f"DEBUG(Fenix): Player está vivo: {player_esta_vivo}") # Debug: Verifica vida do player
            # print(f"DEBUG(Fenix): Fênix está viva: {fenix_esta_viva}") # Debug: Verifica vida da fênix
            # print(f"DEBUG(Fenix): Fênix tem velocidade > 0: {fenix_tem_velocidade}") # Debug: Verifica velocidade


            if fenix_esta_viva and player_tem_rect and player_esta_vivo and fenix_tem_velocidade:
                 # print("DEBUG(Fenix): Condições de movimento atendidas. Chamando mover_em_direcao.") # Debug: Condições atendidas
                 # Move a Fênix na direção do centro do retângulo do jogador
                 self.mover_em_direcao(player.rect.centerx, player.rect.centery)
            else:
                 # print("DEBUG(Fenix): Condições de movimento NÃO atendidas. Não movendo.") # Debug: Condições não atendidas
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

        # else:
             # print(f"DEBUG(Fenix): Fênix não está viva. Não atualizando. HP: {self.hp}") # Debug se não estiver vivo


    # O método desenhar() é herdado da classe base Inimigo e deve funcionar
    # se a classe base tiver um método desenhar que aceita surface, camera_x, camera_y.
    # Sobrescrevendo desenhar para remover a barra de vida
    def desenhar(self, surface, camera_x, camera_y):
        """Desenha a Fênix."""
        # Desenha o sprite da Fênix com o offset da câmera
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        # Lógica de desenho da barra de vida removida

    # O método receber_dano() é herdado da classe base Inimigo e sobrescrito aqui.
