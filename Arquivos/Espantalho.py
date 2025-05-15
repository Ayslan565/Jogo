# Espantalho.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()

# Importa a classe base Inimigo do ficheiro Inimigos.py
# Certifique-se de que o ficheiro Inimigos.py está na mesma pasta ou num caminho acessível
from Inimigos import Inimigo

"""
Classe para o inimigo Espantalho.
Herda da classe base Inimigo.
"""
class Espantalho(Inimigo):
    # Variável de classe para armazenar os sprites carregados uma única vez
    sprites_carregados = None

    def __init__(self, x, y, velocidade=1.5): # Velocidade padrão do Espantalho
        """
        Inicializa um novo objeto Espantalho.

        Args:
            x (int): A posição inicial x do Espantalho.
            y (int): A posição inicial y do Espantalho.
            velocidade (float): A velocidade de movimento do Espantalho.
        """
        print(f"DEBUG(Espantalho): Inicializando Espantalho em ({x}, {y}) com velocidade {velocidade}.") # Debug inicialização

        # Carrega os sprites apenas uma vez para todas as instâncias de Espantalho
        if Espantalho.sprites_carregados is None:
            caminhos = [
                # >>> CAMINHOS DOS SPRITES DO Espantalho <<<
                "Sprites\\Inimigos\\Espantalho\\Espantalho.png",
                "Sprites\\Inimigos\\Espantalho\\Espantalho 2.png",
                "Sprites\\Inimigos\\Espantalho\\Espantalho 3.png",
                # Adicione mais caminhos de sprite de animação aqui
            ]
            Espantalho.sprites_carregados = []
            tamanho_sprite_desejado = (110, 110) # >>> TAMANHO DESEJADO PARA O SPRITE DO Espantalho <<<

            for path in caminhos:
                try:
                    sprite = pygame.image.load(path).convert_alpha()
                    # Redimensiona sprites para o tamanho desejado
                    sprite = pygame.transform.scale(sprite, tamanho_sprite_desejado)
                    Espantalho.sprites_carregados.append(sprite)
                except pygame.error as e:
                    print(f"DEBUG(Espantalho): Erro ao carregar o sprite do Espantalho: {path}")
                    print(f"DEBUG(Espantalho): Detalhes do erro: {e}")
                    # Se um sprite falhar, adicione um placeholder com o tamanho correto
                    placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (0, 0, 255), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1])) # Blue placeholder
                    fonte = pygame.font.Font(None, 20)
                    texto_erro = fonte.render("Sprite", True, (255, 255, 255))
                    placeholder.blit(texto_erro, (5, 15))
                    texto_erro2 = fonte.render("Erro", True, (255, 255, 255))
                    placeholder.blit(texto_erro2, (10, 35))
                    Espantalho.sprites_carregados.append(placeholder)

            # Certifique-se de que há pelo menos um sprite carregado
            if not Espantalho.sprites_carregados:
                print("DEBUG(Espantalho): Aviso: Nenhum sprite do Espantalho carregado. Usando placeholder padrão.")
                tamanho_sprite_desejado = (60, 80) # Tamanho do placeholder si nenhum sprite carregar
                placeholder = pygame.Surface(tamanho_sprite_desejado, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (0, 0, 255), (0, 0, tamanho_sprite_desejado[0], tamanho_sprite_desejado[1]))
                Espantalho.sprites_carregados.append(placeholder)


        # Inicializa a classe base Inimigo PASSANDO A PRIMEIRA SURFACE CARREGADA E A VELOCIDADE.
        # Certifique-se de que Espantalho.sprites_carregados não está vazio antes de acessar o índice [0]
        initial_image = Espantalho.sprites_carregados[0] if Espantalho.sprites_carregados else pygame.Surface((60, 80), pygame.SRCALPHA) # Usa placeholder se a lista estiver vazia
        super().__init__(x, y, initial_image, velocidade) # >>> Passa a velocidade para a classe base <<<


        self.hp = 50 # Pontos de vida do Espantalho (ajuste conforme necessário)
        # self.velocidade é definido na classe base agora
        self.sprites = Espantalho.sprites_carregados # Referência à lista de sprites carregados
        self.sprite_index = 0 # Índice do sprite atual para animação
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Tempo do último update da animação
        self.intervalo_animacao = 150 # milissegundos entre frames de animação (ajuste para a velocidade da animação)


        # >>> Atributos de Combate do Espantalho <<<
        self.is_attacking = False # Flag para indicar si o Espantalho está atacando
        self.attack_duration = 0.8 # Duração da animação de ataque (ajuste conforme a animação)
        self.attack_timer = 0 # Tempo em que o ataque começou (usando time.time())
        self.attack_damage = 10 # Quantidade de dano causado pelo ataque (dano de ataque específico)
        # Define o tamanho da hitbox de ataque - AJUSTE ESTES VALORES
        self.attack_hitbox_size = (40, 40) # Exemplo: hitbox 40x40 pixels
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Retângulo para a hitbox de ataque (inicialmente vazio)
        self.attack_range = 80 # Alcance para iniciar o ataque (distância do centro do inimigo ao centro do jogador)
        self.attack_cooldown = 3 # Tempo de espera entre ataques em segundos
        self.last_attack_time = time.time() # Tempo em que o último ataque ocorreu (usando time.time())
        # self.hit_player_this_attack = False # Já na classe base

        # Atributo para rastrear a direção do Espantalho (para posicionar a hitbox de ataque)
        # Inicializa com uma direção padrão, será atualizado no mover_em_direcao se o espantalho se mover
        self.direction = "down" # Pode não ser tão relevante para um espantalho, mas mantido por consistência

        # Flag para rastrear si foi atingido pelo ataque do jogador neste ciclo de ataque do jogador (já na base)
        # self.hit_by_player_this_attack = False

        # >>> Atributos para Dano por Contato <<<
        self.contact_damage = 3 # Dano de contato (ajuste)
        self.contact_cooldown = 500 # Cooldown de dano de contato em milissegundos (ajuste)
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
            print(f"DEBUG(Espantalho): Recebeu {dano} de dano. HP restante: {self.hp}") # Debug
            if self.hp <= 0:
                self.hp = 0
                print(f"DEBUG(Espantalho): Espantalho morreu.") # Debug morte
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


    # O método mover_em_direcao() é herdado da classe base Inimigo agora.
    # Se precisar de lógica de movimento específica para o Espantalho, sobrescreva-o aqui.
    # Exemplo de sobrescrita (si necessário):
    # def mover_em_direcao(self, alvo_x, alvo_y):
    #     # Lógica de movimento específica do Espantalho
    #     super().mover_em_direcao(alvo_x, alvo_y) # Chama o método da classe base


    def atacar(self, player):
        """
        Implementa a lógica de ataque do Espantalho.
        Neste exemplo, um ataque simples de contato ou projétil (si aplicável).

        Args:
            player (Player): O objeto jogador para verificar o alcance de ataque.
        """
        # Adiciona verificação para garantir que o objeto player tem o atributo rect
        if not hasattr(player, 'rect'):
            # print("DEBUG(Espantalho): Objeto player passado para Espantalho.atacar não tem atributo 'rect'.") # Debug
            return # Sai do método para evitar o erro

        current_time = time.time()
        # Verifica se o cooldown passou e se o jogador está dentro do alcance de ataque
        # E se o Espantalho está vivo
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
                print("DEBUG(Espantalho): Espantalho iniciou ataque!") # Debug

                # Define a hitbox de ataque (exemplo: um retângulo ao redor do Espantalho para ataque de contato)
                # Você precisará ajustar isso com base na animação ou tipo de ataque do seu Espantalho
                attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0] # Pega a largura da hitbox ou um valor padrão
                attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1] # Pega a altura da hitbox ou um valor padrão

                # Posiciona a hitbox de ataque (exemplo: centralizada no Espantalho)
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                self.attack_hitbox.center = self.rect.center # Centraliza a hitbox no Espantalho


    # >>> O método update recebe o objeto Player completo <<<
    def update(self, player):
        """
        Atualiza o estado do Espantalho (movimento, animação e ataque).
        Inclui a lógica de aplicação de dano por contato.

        Args:
            player (Player): O objeto jogador para seguir, verificar o alcance de ataque e aplicar dano.
        """
        print("DEBUG(Espantalho): Update do Espantalho chamado.") # Debug geral
        # >>> Adiciona verificação para garantir que o objeto player tem os atributos necessários <<<
        # Verifica se o player tem pelo menos rect e vida (para verificar si está vivo e receber dano)
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            print("DEBUG(Espantalho): Objeto player passado para Espantalho.update não tem todos os atributos necessários.") # Debug
            return # Sai do método para evitar o erro

        # Só atualiza si estiver vivo
        if self.esta_vivo():
            print(f"DEBUG(Espantalho): Espantalho está vivo. HP: {self.hp}") # Debug
            current_time = time.time()
            current_ticks = pygame.time.get_ticks() # Usando get_ticks() para consistência com contact_cooldown

            # >>> Lógica de Dano por Contato <<<
            # Verifica si o Espantalho está vivo, si colide com o rect do jogador,
            # e si o cooldown de contato passou.
            # Adiciona verificação para garantir que player.vida existe e é válido
            if self.esta_vivo() and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
               hasattr(player, 'rect') and self.rect.colliderect(player.rect) and \
               (current_ticks - self.last_contact_time >= self.contact_cooldown): # Cooldown em milissegundos

                # Aplica dano por contato ao jogador
                # Verifica si o jogador tem o método receber_dano
                if hasattr(player, 'receber_dano'):
                    print(f"DEBUG(Espantalho): Colisão de contato! Espantalho tocou no jogador. Aplicando {self.contact_damage} de dano.") # Debug
                    player.receber_dano(self.contact_damage)
                    self.last_contact_time = current_ticks # Atualiza o tempo do último contato (em milissegundos)
                    # Opcional: Adicionar um som ou efeito visual para dano por contato


            # Lógica do temporizador de ataque específico
            if self.is_attacking:
                 print("DEBUG(Espantalho): Espantalho está atacando (ataque específico).") # Debug
                 # Verifica si a duração do ataque passou
                 if time.time() - self.attack_timer >= self.attack_duration: # Usa time.time() para consistência com attack_timer
                     self.is_attacking = False
                     self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Reseta a hitbox quando o ataque termina
                     self.hit_by_player_this_attack = False # Reseta a flag de acerto ao final do ataque específico
                     print("DEBUG(Espantalho): Ataque específico do Espantalho terminou.") # Debug
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
                              print(f"DEBUG(Espantalho): Ataque específico acertou o jogador! Causou {dano_inimigo} de dano.") # Debug
                              player.receber_dano(dano_inimigo)
                              self.hit_by_player_this_attack = True # Define a flag para não acertar novamente neste ataque específico
                              # Opcional: Adicionar um som ou efeito visual quando o inimigo acerta o jogador com ataque específico


            # >>> Lógica de Perseguição (Movimento) <<<
            # O Espantalho persegue o jogador si estiver vivo e o jogador estiver vivo.
            # Adiciona verificação para garantir que player tem rect antes de passar para mover_em_direcao
            player_tem_rect = hasattr(player, 'rect')
            player_esta_vivo = hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo()
            espantalho_esta_vivo = self.esta_vivo()
            espantalho_tem_velocidade = self.velocidade > 0


            print(f"DEBUG(Espantalho): Player tem rect: {player_tem_rect}") # Debug: Verifica rect do player
            print(f"DEBUG(Espantalho): Player está vivo: {player_esta_vivo}") # Debug: Verifica vida do player
            print(f"DEBUG(Espantalho): Espantalho está vivo: {espantalho_esta_vivo}") # Debug: Verifica vida do espantalho
            print(f"DEBUG(Espantalho): Espantalho tem velocidade > 0: {espantalho_tem_velocidade}") # Debug: Verifica velocidade


            if espantalho_esta_vivo and player_tem_rect and player_esta_vivo and espantalho_tem_velocidade:
                 print("DEBUG(Espantalho): Condições de movimento atendidas. Chamando mover_em_direcao.") # Debug: Condições atendidas
                 # Move o Espantalho na direção do centro do retângulo do jogador
                 self.mover_em_direcao(player.rect.centerx, player.rect.centery)
            else:
                 print("DEBUG(Espantalho): Condições de movimento NÃO atendidas. Não movendo.") # Debug: Condições não atendidas
                 pass # Não move si o player não tiver rect ou não estiver vivo


            # Tenta iniciar um ataque específico (verificado após o movimento)
            # A função atacar também tem uma verificação interna agora
            self.atacar(player)

            # >>> Posicionamento da Hitbox de Ataque Específico (Atualiza mesmo si não estiver atacando ativamente) <<<
            # A hitbox de ataque é posicionada em relação ao centro do Espantalho.
            # Ajuste as coordenadas conforme a sua animação e alcance desejado.
            # A hitbox é posicionada independentemente de estar atacando ou não,
            # mas só é usada para aplicar dano quando is_attacking é True.
            attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0] # Pega a largura da hitbox ou um valor padrão
            attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1] # Pega a altura da hitbox ou um valor padrão
            self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
            self.attack_hitbox.center = self.rect.center # Centraliza a hitbox no Espantalho


            # Atualiza a animação
            self.atualizar_animacao()

        else:
             print(f"DEBUG(Espantalho): Espantalho não está vivo. Não atualizando. HP: {self.hp}") # Debug se não estiver vivo


    # O método desenhar() é herdado da classe base Inimigo e deve funcionar
    # se a classe base tiver um método desenhar que aceita surface, camera_x, camera_y.

    # O método receber_dano() é herdado da classe base Inimigo.
