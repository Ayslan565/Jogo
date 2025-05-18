# Mae_Natureza.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()
import os # Importa os para verificar a existência de arquivos

# Importa a classe base Inimigo do ficheiro Inimigos.py
# Certifique-se de que o ficheiro Inimigos.py está na mesma pasta ou num caminho acessível
try:
    from Inimigos import Inimigo
except ImportError:
    print("DEBUG(Mae_Natureza): Aviso: Módulo 'Inimigos.py' ou classe 'Inimigo' não encontrado. Usando placeholder.")
    # Define uma classe Inimigo placeholder para evitar NameError se a importação falhar
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
                # A remoção do inimigo da lista/grupo deve ser feita no GerenciadorDeInimigos
                # self.kill() # Pode ser chamado aqui se estiver usando grupos de sprites

        def update(self, player):
            pass # Update placeholder

        def desenhar(self, janela, camera_x, camera_y):
            # Desenho placeholder
            janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
            # Lógica de desenho da barra de vida removida

        def esta_vivo(self):
            return self.hp > 0

        def mover_em_direcao(self, alvo_x, alvo_y):
            # Lógica de movimento placeholder
            dx = alvo_x - self.rect.centerx
            dy = alvo_y - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                dx_norm = dx / dist
                dy_norm = dy / dist
                self.rect.x += dx_norm * self.velocidade
                self.rect.y += dy_norm * self.velocidade

        # Método desenhar_barra_vida removido do placeholder


"""
Classe para o inimigo Mãe Natureza.
Herda da classe base Inimigo.
"""
class Mae_Natureza(Inimigo):
    """
    Representa um inimigo Mãe Natureza.
    Pode ter comportamentos únicos relacionados a natureza.
    """
    # Variável de classe para armazenar os sprites carregados uma única vez
    sprites_carregados = None
    # Adiciona uma variável de classe para armazenar os sprites originais (não flipados)
    sprites_originais = None # Adicionado para armazenar sprites originais

    def __init__(self, x, y, velocidade=1.8): # Velocidade padrão da Mãe Natureza (ajustada)
        """
        Inicializa um novo objeto Mae_Natureza.

        Args:
            x (int): A posição inicial x da Mãe Natureza.
            y (int): A posição inicial y da Mãe Natureza.
            velocidade (float): A velocidade de movimento da Mãe Natureza.
        """
        print(f"DEBUG(Mae_Natureza): Inicializando Mãe Natureza em ({x}, {y}) com velocidade {velocidade}.") # Debug inicialização

        # Carrega os sprites apenas uma vez para todas as instâncias de Mae_Natureza
        if Mae_Natureza.sprites_originais is None: # Carrega na variável de sprites_originais
            caminhos = [
                # >>> AJUSTE ESTES CAMINHOS PARA OS SEUS ARQUIVOS DE SPRITE DA MÃE NATUREZA <<<
                "Sprites/Inimigos/Mae_Natureza/Mae1.png", # Corrigido a barra invertida
                "Sprites/Inimigos/Mae_Natureza/Mae2.png", # Corrigido a barra invertida
                "Sprites/Inimigos/Mae_Natureza/Mae3.png", # Corrigido a barra invertida

                # Adicione mais caminhos de sprite de animação aqui
            ]
            Mae_Natureza.sprites_originais = [] # Inicializa a lista de sprites originais
            tamanho_sprite_desejado = (70, 70) # >>> AJUSTE O TAMANHO DESEJADO PARA O SPRITE DA MÃE NATUREZA <<<

            for path in caminhos:
                try:
                    if os.path.exists(path): # Verifica se o arquivo existe
                        sprite = pygame.image.load(path).convert_alpha()
                        # Redimensiona sprites para o tamanho desejado
                        sprite = pygame.transform.scale(sprite, tamanho_sprite_desejado)
                        Mae_Natureza.sprites_originais.append(sprite) # CORRIGIDO: Adiciona aos sprites originais
                    else:
                         print(f"DEBUG(Mae_Natureza): Aviso: Sprite da Mãe Natureza não encontrado: {path}") # Nome atualizado
                         # Se o arquivo não existir, adicione um placeholder
                         placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                         pygame.draw.rect(placeholder, (255, 105, 180), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1])) # Pink placeholder
                         Mae_Natureza.sprites_originais.append(placeholder) # Referência à nova classe

                except pygame.error as e:
                    print(f"DEBUG(Mae_Natureza): Erro ao carregar o sprite da Mãe Natureza: {path}") # Nome atualizado
                    print(f"DEBUG(Mae_Natureza): Detalhes do erro: {e}")
                    # Se um sprite falhar, adicione um placeholder com o tamanho correto
                    placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (255, 105, 180), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1])) # Pink placeholder
                    Mae_Natureza.sprites_originais.append(placeholder) # Referência à nova classe

            # Certifique-se de que há pelo menos um sprite carregado, mesmo que seja um placeholder
            if not Mae_Natureza.sprites_originais: # Referência à nova classe
                print("DEBUG(Mae_Natureza): Aviso: Nenhum sprite da Mãe Natureza carregado. Usando placeholder padrão.") # Nome atualizado
                tamanho_sprite_desejado = (70, 70) # Tamanho do placeholder si nenhum sprite carregar
                placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255, 105, 180), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1]))
                Mae_Natureza.sprites_originais.append(placeholder) # Referência à nova classe


        # Inicializa a classe base Inimigo PASSANDO A PRIMEIRA SURFACE CARREGADA E A VELOCIDADE.
        # Certifique-se de que Mae_Natureza.sprites_carregados não está vazio antes de acessar o índice [0]
        initial_image = Mae_Natureza.sprites_originais[0] if Mae_Natureza.sprites_originais else pygame.Surface((70, 70), pygame.SRCALPHA) # Usa placeholder se a lista estiver vazia (Referência à nova classe)
        super().__init__(x, y, initial_image, velocidade) # >>> Passa a velocidade para a classe base <<<


        self.hp = 75 # Pontos de vida da Mãe Natureza (ajustado)
        self.max_hp = self.hp # Define HP máximo para barra de vida
        # self.velocidade é definido na classe base agora
        self.sprites = Mae_Natureza.sprites_originais # Referência à lista de sprites carregados (Referência à nova classe)
        self.sprite_index = 0 # Índice do sprite atual para animação
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Tempo do último update da animação
        self.intervalo_animacao = 180 # milissegundos entre frames de animação (ajustado)


        # >>> Atributos de Combate da Mãe Natureza <<<
        self.is_attacking = False # Flag para indicar si a Mãe Natureza está atacando
        self.attack_duration = 0.6 # Duração da animação de ataque (ajustado)
        self.attack_timer = 0 # Tempo em que o ataque começou (usando time.time())
        self.attack_damage = 12 # Quantidade de dano causado pelo ataque (dano de ataque específico, ajustado)
        # Define o tamanho da hitbox de ataque - AJUSTE ESTES VALORES
        self.attack_hitbox_size = (50, 50) # Exemplo: hitbox 50x50 pixels (ajustado)
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Retângulo para a hitbox de ataque (inicialmente vazio)
        self.attack_range = 70 # Alcance para iniciar o ataque (ajustado)
        self.attack_cooldown = 2.5 # Tempo de espera entre ataques em segundos (ajustado)
        self.last_attack_time = time.time() # Tempo em que o último ataque ocorreu (usando time.time())
        # self.hit_by_player_this_attack é herdado da classe base

        # Atributo para rastrear a direção horizontal para espelhamento
        # Assume que o sprite original está virado para a esquerda ou para baixo.
        # Vamos flipar quando facing_right for True.
        self.facing_right = False # Inicializa como False (virado para a esquerda ou padrão)


        # Atributo para rastrear a direção da Mãe Natureza (para posicionar a hitbox de ataque)
        # Inicializa com uma direção padrão, será atualizado no mover_em_direcao
        self.direction = "down"


        # >>> Atributos para Dano por Contato <<<
        self.contact_damage = 8 # Dano de contato (ajustado)
        self.contact_cooldown = 800 # Cooldown de dano de contato em milissegundos (ajustado)
        self.last_contact_time = pygame.time.get_ticks() # Tempo do último contato (em milissegundos)


        # >>> Atributos Específicos da Mãe Natureza (Cura, etc.) <<<
        # Adicione atributos únicos aqui, como:
        # self.chance_de_curar_aliado = 0.1 # Exemplo: 10% de chance de curar um inimigo próximo
        # self.raio_cura = 150 # Exemplo: raio de busca por aliados para curar
        # self.quantidade_cura = 10 # Exemplo: quanto de HP cura


    # O método esta_vivo() é herdado da classe base Inimigo.

    def receber_dano(self, dano):
        """
        Reduz a vida da Mãe Natureza pela quantidade de dano especificada.

        Args:
            dano (int): A quantidade de dano a ser recebida.
        """
        # Verifica si o inimigo está vivo antes de receber dano
        if self.esta_vivo(): # Chama o método esta_vivo() herdado
            self.hp -= dano
            print(f"DEBUG(Mae_Natureza): Recebeu {dano} de dano. HP restante: {self.hp}") # Debug: Mostra dano recebido e HP restante (Nome atualizado)
            if self.hp <= 0:
                self.hp = 0
                print(f"DEBUG(Mae_Natureza): Mãe Natureza morreu.") # Debug: Mostra que morreu (Nome atualizado)
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
            # Aplica o flip horizontal si estiver virado para a direita
            if self.facing_right:
                self.image = pygame.transform.flip(base_image, True, False)
            else:
                self.image = base_image
        else:
            # Fallback si não houver sprites
            tamanho_sprite_desejado = (70, 70) # Tamanho do placeholder
            self.image = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 105, 180), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1]))


    # Sobrescreve o método mover_em_direcao para adicionar a lógica de direção horizontal
    def mover_em_direcao(self, alvo_x, alvo_y):
        """
        Move a Mãe Natureza em direção a um alvo e atualiza a direção horizontal.

        Args:
            alvo_x (int): A coordenada x do alvo.
            alvo_y (int): A coordenada y do alvo.
        """
        dx = alvo_x - self.rect.centerx
        dy = alvo_y - self.rect.centery
        dist = math.hypot(dx, dy)

        # Atualiza a direção horizontal com base em dx apenas se houver movimento horizontal significativo
        if abs(dx) > 0.1: # Adiciona uma pequena tolerância para evitar flipar por micro-movimentos
            if dx > 0:
                self.facing_right = True
            elif dx < 0:
                self.facing_right = False

        if dist > 0:
            dx_norm = dx / dist
            dy_norm = dy / dist
            self.rect.x += dx_norm * self.velocidade
            self.rect.y += dy_norm * self.velocidade


    def atacar(self, player):
        """
        Implementa a lógica de ataque da Mãe Natureza.
        Pode ser um ataque de projétil floral, aura de dano, etc.

        Args:
            player (Player): O objeto jogador para verificar o alcance de ataque.
        """
        # Adiciona verificação para garantir que o objeto player tem o atributo rect
        if not hasattr(player, 'rect'):
            # print("DEBUG(Mae_Natureza): Objeto player passado para Mae_Natureza.atacar não tem atributo 'rect'.") # Debug (Nome atualizado)
            return # Sai do método para evitar o erro

        current_time = time.time()
        # Verifica se o cooldown passou e se o jogador está dentro do alcance de ataque
        # E se a Mãe Natureza está viva
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
                print("DEBUG(Mae_Natureza): Mãe Natureza iniciou ataque!") # Debug (Nome atualizado)

                # Define a hitbox de ataque (exemplo: uma área de dano ao redor do espírito)
                # Você precisará ajustar isso com base na animação ou tipo de ataque do seu espírito
                attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0] # Pega a largura da hitbox ou um valor padrão
                attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1] # Pega a altura da hitbox ou um valor padrão

                # Posiciona a hitbox de ataque (exemplo: centralizada na Mãe Natureza)
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                self.attack_hitbox.center = self.rect.center # Centraliza a hitbox na Mãe Natureza

                # >>> Lógica de Aplicação de Dano do Ataque Específico (PODE SER AQUI OU NO UPDATE) <<<
                # Para um ataque instantâneo (não baseado em duração), a lógica de dano pode vir aqui.
                # Para ataques com duração (animação), a lógica de dano geralmente fica no update,
                # verificando a colisão da hitbox de ataque enquanto is_attacking é True.
                # Exemplo de ataque instantâneo:
                # if hasattr(player, 'receber_dano'):
                #     dano_inimigo = getattr(self, 'attack_damage', 0)
                #     player.receber_dano(dano_inimigo)
                #     self.hit_by_player_this_attack = True # Marca como atingido para evitar múltiplos hits no mesmo ataque instantâneo


    # O método update é herdado e sobrescrito aqui para incluir a lógica específica da Mãe Natureza
    def update(self, player):
        """
        Atualiza o estado da Mãe Natureza (movimento, animação e ataque).
        Inclui a lógica de aplicação de dano por contato e ataque específico.

        Args:
            player (Player): O objeto jogador para seguir, verificar o alcance de ataque e aplicar dano.
        """
        # print("DEBUG(Mae_Natureza): Update da Mãe Natureza chamado.") # Debug geral (Nome atualizado)
        # >>> Adiciona verificação para garantir que o objeto player tem os atributos necessários <<<
        # Verifica si o player tem pelo menos rect e vida (para verificar si está vivo e receber dano)
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            # print("DEBUG(Mae_Natureza): Objeto player passado para Mae_Natureza.update não tem todos os atributos necessários.") # Debug (Nome atualizado)
            return # Sai do método para evitar o erro

        # Só atualiza si estiver vivo
        if self.esta_vivo():
            current_time = time.time()
            current_ticks = pygame.time.get_ticks() # Usando get_ticks() para consistência com contact_cooldown

            # >>> Lógica de Dano por Contato <<<
            # Verifica si a Mãe Natureza está viva, si colide com o rect do jogador,
            # e si o cooldown de contato passou.
            # Adiciona verificação para garantir que player.vida existe e é válido
            if self.esta_vivo() and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
               hasattr(player, 'rect') and self.rect.colliderect(player.rect) and \
               (current_ticks - self.last_contact_time >= self.contact_cooldown): # Cooldown em milissegundos

                # Aplica dano por contato ao jogador
                # Verifica si o jogador tem o método receber_dano
                if hasattr(player, 'receber_dano'):
                    print(f"DEBUG(Mae_Natureza): Colisão de contato! Mãe Natureza tocou no jogador. Aplicando {self.contact_damage} de dano.") # Debug (Nome atualizado)
                    player.receber_dano(self.contact_damage)
                    self.last_contact_time = current_ticks # Atualiza o tempo do último contato (em milissegundos)
                    # Opcional: Adicionar um som ou efeito visual para dano por contato


            # Lógica do temporizador de ataque específico
            if self.is_attacking:
                 # print("DEBUG(Mae_Natureza): Mãe Natureza está atacando (ataque específico).") # Debug (Nome atualizado)
                 # Verifica si a duração do ataque passou
                 if time.time() - self.attack_timer >= self.attack_duration: # Usa time.time() para consistência com attack_timer
                     self.is_attacking = False
                     self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Reseta a hitbox quando o ataque termina
                     self.hit_by_player_this_attack = False # Reseta a flag de acerto ao final do ataque específico
                     # print("DEBUG(Mae_Natureza): Ataque específico da Mãe Natureza terminou.") # Debug (Nome atualizado)
                 else:
                      # >>> Lógica de Dano do Ataque Específico (VERIFICADA DURANTE A ANIMAÇÃO DE ATAQUE) <<<
                      # Verifica si o inimigo está atacando (ataque específico), si ainda não acertou neste ataque,
                      # si tem hitbox de ataque e si colide com o rect do jogador.
                      # Esta lógica é para ataques que duram um tempo (animação).
                      if not self.hit_by_player_this_attack and \
                           hasattr(self, 'attack_hitbox') and \
                           hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                           self.attack_hitbox.colliderect(player.rect): # >>> CORREÇÃO AQUI: Usa player.rect <<<

                           # Verifica si o jogador tem o método receber_dano e está vivo
                           if hasattr(player, 'receber_dano'):
                                # Aplica dano do ataque específico ao jogador
                                dano_inimigo = getattr(self, 'attack_damage', 0) # Pega attack_damage ou 0 si não existir
                                print(f"DEBUG(Mae_Natureza): Ataque específico acertou o jogador! Causou {dano_inimigo} de dano.") # Debug (Nome atualizado)
                                player.receber_dano(dano_inimigo)
                                self.hit_by_player_this_attack = True # Define a flag para não acertar novamente neste ataque específico
                                # Opcional: Adicionar um som ou efeito visual quando o inimigo acerta o jogador com ataque específico


            # >>> Lógica de Perseguição (Movimento) <<<
            # A Mãe Natureza persegue o jogador si estiver vivo e o jogador estiver vivo.
            # Adiciona verificação para garantir que player tem rect antes de passar para mover_em_direcao
            player_tem_rect = hasattr(player, 'rect')
            player_esta_vivo = hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo()
            mae_natureza_esta_vivo = self.esta_vivo() # Referência à nova classe
            mae_natureza_tem_velocidade = self.velocidade > 0 # Referência à nova classe

            # print(f"DEBUG(Mae_Natureza): Player tem rect: {player_tem_rect}") # Debug: Verifica rect do player (Nome atualizado)
            # print(f"DEBUG(Mae_Natureza): Player está vivo: {player_esta_vivo}") # Debug: Verifica vida do player (Nome atualizado)
            # print(f"DEBUG(Mae_Natureza): Mãe Natureza está vivo: {mae_natureza_esta_vivo}") # Debug: Verifica vida da Mãe Natureza (Nome atualizado)
            # print(f"DEBUG(Mae_Natureza): Mãe Natureza tem velocidade > 0: {mae_natureza_tem_velocidade}") # Debug: Verifica velocidade (Nome atualizado)

            if mae_natureza_esta_vivo and player_tem_rect and player_esta_vivo and mae_natureza_tem_velocidade:
                 # print("DEBUG(Mae_Natureza): Condições de movimento atendidas. Chamando mover_em_direcao.") # Debug: Condições atendidas (Nome atualizado)
                 # Move a Mãe Natureza na direção do centro do retângulo do jogador
                 # Acessa centerx e centery do rect do player
                 self.mover_em_direcao(player.rect.centerx, player.rect.centery)
            else:
                 # print("DEBUG(Mae_Natureza): Condições de movimento NÃO atendidas. Não movendo.") # Debug: Condições não atendidas (Nome atualizado)
                 pass # Não move si o player não tiver rect ou não estiver vivo


            # Tenta iniciar um ataque específico (verificado após o movimento)
            # A função atacar também tem uma verificação interna agora
            self.atacar(player)

            # >>> Lógica Específica da Mãe Natureza (Cura, etc.) <<<
            # Implemente aqui lógicas únicas para a Mãe Natureza, como curar aliados próximos.
            # Exemplo (usando atributos definidos no __init__):
            # if self.esta_vivo() and random.random() < self.chance_de_curar_aliado: # Verifica a chance de curar
            #     # Encontra aliados próximos (precisa de acesso à lista de todos os inimigos)
            #     # Esta lógica geralmente seria melhor no GerenciadorDeInimigos ou em um sistema de buff/debuff
            #     print("DEBUG(Mae_Natureza): Tentando curar aliados próximos.") # Debug (Nome atualizado)
            #     # Exemplo BÁSICO: Cura a si mesmo (apenas para demonstração)
            #     # self.hp = min(self.max_hp, self.hp + self.quantidade_cura)
            #     # print(f"DEBUG(Mae_Natureza): Curou a si mesmo. HP atual: {self.hp}") # Debug (Nome atualizado)


            # >>> Posicionamento da Hitbox de Ataque Específico (Atualiza mesmo si não estiver atacando ativamente) <<<
            # A hitbox de ataque é posicionada em relação ao centro da Mãe Natureza.
            # Ajuste as coordenadas conforme a sua animação e alcance desejado.
            # A hitbox é posicionada independentemente de estar atacando ou não,
            # mas só é usada para aplicar dano quando is_attacking é True.
            attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0] # Pega a largura da hitbox ou um valor padrão
            attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1] # Pega a altura da hitbox ou um valor padrão
            self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
            self.attack_hitbox.center = self.rect.center # Centraliza a hitbox na Mãe Natureza


            # Atualiza a animação
            self.atualizar_animacao()

    # O método desenhar() é herdado da classe base Inimigo e deve funcionar
    # se a classe base tiver um método desenhar que aceita surface, camera_x, camera_y.
    # Sobrescrevendo desenhar para remover a barra de vida
    def desenhar(self, surface, camera_x, camera_y):
        """Desenha a Mãe Natureza.""" # Nome atualizado
        # Desenha o sprite da Mãe Natureza com o offset da câmera
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        # Lógica de desenho da barra de vida removida

    # O método receber_dano() é herdado da classe base Inimigo e sobrescrito aqui.
