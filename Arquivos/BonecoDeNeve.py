# BonecoDeNeve.py
import time
import random
import pygame
import math # Importe math se for usado para cooldowns ou outras lógicas de tempo
import os # Importa os para verificar a existência de arquivos

# Inclui a classe base Inimigo aqui para garantir que BonecoDeNeve funcione mesmo sem Inimigos.py
# Se você tiver um arquivo Inimigos.py separado, este bloco será substituído pela importação real.
try:
    from Inimigos import Inimigo
except ImportError:
    print("DEBUG(BonecoDeNeve): Aviso: Módulo 'Inimigos.py' ou classe 'Inimigo' não encontrado. Usando placeholder.")
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
                self.kill() # Remove o sprite do grupo

        def update(self, player):
            # Lógica de atualização padrão (pode ser sobrescrita)
            pass

        def desenhar(self, surface, camera_x, camera_y):
            # Desenha o inimigo com o offset da câmera
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
            # Opcional: Desenhar barra de vida do inimigo aqui

        def esta_vivo(self):
             """Verifica se o inimigo está vivo."""
             return self.hp > 0

        def mover_em_direcao(self, alvo_x, alvo_y):
            """
            Move o inimigo na direção de um ponto alvo.
            Este é um método base que pode ser sobrescrito por subclasses.

            Args:
                alvo_x (int): A coordenada x do ponto alvo.
                alvo_y (int): A coordenada y do ponto alvo.
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
                    # Retorna a componente X normalizada para que a subclasse possa usar
                    return dx_norm
                return 0 # Retorna 0 si não houver movimento
            return 0 # Retorna 0 si não estiver vivo ou não tiver velocidade

        # Adicione outros métodos base comuns a todos os inimigos aqui
# --- Fim do Placeholder para Inimigo ---


# Importa a nova classe de projétil
try:
    # Certifique-se de que o nome do arquivo e da classe estão corretos
    from Projetil_BolaNeve import ProjetilNeve
except ImportError:
    print("DEBUG(BonecoDeNeve): Aviso: Módulo 'Projetil_BolaNeve.py' ou classe 'ProjetilNeve' não encontrado.")
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
        # print(f"DEBUG(BonecoDeNeve): Inicializando Boneco de Neve em ({x}, {y}) com velocidade {velocidade}.") # Debug inicialização

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
                         print(f"DEBUG(BonecoDeNeve): Aviso: Sprite do Boneco de Neve não encontrado: {path}")
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
                    print(f"DEBUG(BonecoDeNeve): Erro ao carregar o sprite do Boneco de Neve: {path}")
                    print(f"DEBUG(BonecoDeNeve): Detalhes do erro: {e}")
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
                print("DEBUG(BonecoDeNeve): Aviso: Nenhum sprite do Boneco de Neve carregado. Usando placeholder padrão.")
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

        # NOVO: Atributo para rastrear a posição anterior para verificar movimento
        self._previous_pos = (self.rect.x, self.rect.y)


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
            # print(f"DEBUG(BonecoDeNeve): Recebeu {dano} de dano. HP restante: {self.hp}") # Debug
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
    def mover_em_direcao(self, alvo_x, alvo_y):
        """
        Move o boneco de neve em direção a um alvo e atualiza a direção horizontal.

        Args:
            alvo_x (int): A coordenada x do alvo.
            alvo_y (int): A coordenada y do alvo.
        """
        # Armazena a posição antes de mover
        self._previous_pos = (self.rect.x, self.rect.y) # Atualiza a posição anterior

        dx = alvo_x - self.rect.centerx
        dy = alvo_y - self.rect.centery
        dist = math.hypot(dx, dy)

        # Atualiza a direção horizontal com base em dx apenas se houver movimento horizontal significativo
        if abs(dx) > 0.1: # Adiciona uma pequena tolerância para evitar flipar por micro-movimentos
            if dx > 0:
                self.facing_right = True
                # print(f"DEBUG(BonecoDeNeve): Movendo para a direita (dx={dx:.2f}). facing_right = True") # Debug direção
            elif dx < 0:
                self.facing_right = False
                # print(f"DEBUG(BonecoDeNeve): Movendo para a esquerda (dx={dx:.2f}). facing_right = False") # Debug direção

        if dist > 0:
            dx_norm = dx / dist
            dy_norm = dy / dist
            self.rect.x += dx_norm * self.velocidade
            self.rect.y += dy_norm * self.velocidade


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
            # print("DEBUG(BonecoDeNeve): Objeto player passado para BonecoDeNeve.atacar não tem atributo 'rect'.") # Debug
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
                    # print("DEBUG(BonecoDeNeve): Boneco de Neve lançou um projétil!") # Debug
                else:
                    print("DEBUG(BonecoDeNeve): Aviso: Classe 'ProjetilNeve' não disponível. Não foi possível lançar projétil.") # Debug aviso


    # O método update agora recebe o objeto Player completo E a lista de projéteis
    def update(self, player, lista_projeteis, tela_largura, tela_altura):
        """
        Atualiza o estado do boneco de neve (movimento, animação e ataque/lançamento de projétil).
        Inclui a lógica de aplicação de dano por contato.

        Args:
            player (Player): O objeto jogador para seguir, verificar o alcance de ataque e aplicar dano.
            lista_projeteis (list): A lista onde os projéteis ativos são armazenados (passada para o método atacar).
            tela_largura (int): Largura da tela (passada para a atualização dos projéteis).
            tela_altura (int): Altura da tela (passada para a atualização dos projéteis).
        """
        # print("DEBUG(BonecoDeNeve): Update do BonecoDeNeve chamado.") # Debug geral
        # Adiciona verificação para garantir que o objeto player tem os atributos necessários
        # Verifica se o player tem pelo menos rect e vida (para verificar se está vivo e receber dano)
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            # print("DEBUG(BonecoDeNeve): Objeto player passado para BonecoDeNeve.update não tem todos os atributos necessários.") # Debug
            return # Sai do método para evitar o erro

        # Só atualiza si estiver vivo
        if self.esta_vivo():
            current_time = time.time()
            current_ticks = pygame.time.get_ticks() # Usando get_ticks() para consistência com contact_cooldown

            # Lógica de Dano por Contato
            # Verifica si o boneco de neve está vivo, si colide com o rect do jogador,
            # e si o cooldown de contato passou.
            # Adiciona verificação para garantir que player.vida existe e é válido
            if self.esta_vivo() and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
               hasattr(player, 'rect') and self.rect.colliderect(player.rect) and \
               (current_ticks - self.last_contact_time >= self.contact_cooldown): # Cooldown em milissegundos

                # Aplica dano por contato ao jogador
                # Verifica si o jogador tem o método receber_dano
                if hasattr(player, 'receber_dano'):
                    # print(f"DEBUG(BonecoDeNeve): Colisão de contato! Boneco de Neve tocou no jogador. Aplicando {self.contact_damage} de dano.") # Debug
                    player.receber_dano(self.contact_damage)
                    self.last_contact_time = current_ticks # Atualiza o tempo do último contato (em milissegundos)
                    # Opcional: Adicionar um som ou efeito visual para dano por contato


            # Lógica de Perseguição (Movimento)
            # O boneco de neve persegue o jogador si estiver vivo e o jogador estiver vivo.
            # Adiciona verificação para garantir que player tem rect antes de passar para mover_em_direcao
            if self.esta_vivo() and hasattr(player, 'rect') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo():
                 # Move o boneco de neve na direção do centro do retângulo do jogador
                 # Acessa centerx e centery do rect do player
                 self.mover_em_direcao(player.rect.centerx, player.rect.centery)
            else:
                 # print("DEBUG(BonecoDeNeve): Objeto player não tem atributos necessários para perseguição ou boneco de neve/jogador não está vivo.") # Debug
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

            # NOVO: Atualiza a posição anterior após o movimento para o próximo frame
            self._previous_pos = (self.rect.x, self.rect.y)


    # O método desenhar() é herdado da classe base Inimigo e deve funcionar
    # se a classe base tiver um método desenhar que aceita surface, camera_x, camera_y.
    # Não precisamos sobrescrever desenhar aqui, pois o flip é aplicado no atualizar_animacao

    # O método receber_dano() é herdado da classe base Inimigo.
