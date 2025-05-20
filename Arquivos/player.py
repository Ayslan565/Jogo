# player.py
import pygame
import random
from vida import Vida
from arvores import Arvore # Importado mas não usado diretamente no código fornecido, mantido por compatibilidade
from grama import Grama # Importado mas não usado diretamente no código fornecido, mantido por compatibilidade
import math
import os # Importa os para verificar a existência de arquivos
import time # Importa time para usar time.time()

# Importa a classe base Inimigo se o jogador interagir diretamente com ela (ex: para ataque)
try:
    from Inimigos import Inimigo
except ImportError:
    # print("AVISO(Player): Módulo 'Inimigos.py' ou classe 'Inimigo' não encontrado.") # Debug removido
    # Define uma classe Inimigo placeholder si a importação falhar e for necessária
    class Inimigo:
        def __init__(self):
            self.rect = pygame.Rect(0, 0, 0, 0) # Rect vazio
            self.hp = 0
        def receber_dano(self, dano):
            pass
        def esta_vivo(self):
            return False


# Importa a classe Arvore para verificar colisões
try:
    from arvores import Arvore
except ImportError:
    print("AVISO(Player): Módulo 'arvores.py' ou classe 'Arvore' não encontrado.")
    Arvore = None # Define como None para evitar NameError

# Importa a classe Vida se o jogador tiver uma referência direta a ela
try:
    from vida import Vida
except ImportError:
    print("AVISO(Player): Módulo 'vida.py' ou classe 'Vida' não encontrado.")
    Vida = None # Define como None para evitar NameError


class Player(pygame.sprite.Sprite):
    """Representa o jogador no jogo."""

    def __init__(self, velocidade=5, vida_maxima=100):
        """Inicializa o objeto jogador."""
        super().__init__()

        self.x = random.randint(0, 800) # Posição inicial aleatória (pode ser ajustada)
        self.y = random.randint(0, 600) # Posição inicial aleatória (pode ser ajustada)

        self.velocidade = velocidade
        # Inicializa o objeto Vida (verifica si a classe Vida foi importada)
        self.vida = Vida(vida_maxima) if Vida is not None else None
        if self.vida is None:
            print("AVISO(Player): Erro: Classe Vida não disponível. Vida do jogador não funcionará corretamente.")


        # --- Carregamento e Escalonamento dos Sprites ---
        tamanho_sprite_desejado = (60, 60) # Tamanho desejado para todos os sprites

        # Sprites de animação de movimento (Esquerda)
        caminhos_esquerda = [
            "Sprites/Asrahel/Esquerda/Ashael_E1.png",
            "Sprites/Asrahel/Esquerda/Ashael_E2.png",
            "Sprites/Asrahel/Esquerda/Ashael_E3.png",
            "Sprites/Asrahel/Esquerda/Ashael_E4.png",
            "Sprites/Asrahel/Esquerda/Ashael_E5.png",
            "Sprites/Asrahel/Esquerda/Ashael_E6.png",
        ]
        self.sprites_esquerda = self._carregar_sprites(caminhos_esquerda, tamanho_sprite_desejado, "Esquerda")

        # Sprites de animação de idle (Esquerda)
        caminhos_idle_esquerda = [
            "Sprites/Asrahel/Esquerda/Ashael_E1.png",
        ]
        self.sprites_idle_esquerda = self._carregar_sprites(caminhos_idle_esquerda, tamanho_sprite_desejado, "Idle Esquerda")

        # Sprites de animação de movimento (Direita) - Assumindo que você terá esses arquivos
        # >>> AJUSTE ESTES CAMINHOS PARA OS SEUS SPRITES DE DIREITA <<<
        caminhos_direita = [
            "Sprites/Asrahel/Direita/Ashael_D1.png",
            "Sprites/Asrahel/Direita/Ashael_D2.png",
            "Sprites/Asrahel/Direita/Ashael_D3.png",
            "Sprites/Asrahel/Direita/Ashael_D4.png",
            "Sprites/Asrahel/Direita/Ashael_D5.png",
            "Sprites/Asrahel/Direita/Ashael_D6.png",
        ]
        self.sprites_direita = self._carregar_sprites(caminhos_direita, tamanho_sprite_desejado, "Direita")

        # Sprites de animação de idle (Direita) - Assumindo que você terá esses arquivos
        # >>> AJUSTE ESTES CAMINHOS PARA OS SEUS SPRITES DE IDLE DIREITA <<<
        caminhos_idle_direita = [
            "Sprites/Asrahel/Direita/Ashael_D1.png",
        ]
        self.sprites_idle_direita = self._carregar_sprites(caminhos_idle_direita, tamanho_sprite_desejado, "Idle Direita")


        # Define o sprite inicial e o retângulo de colisão
        self.atual = 0 # Índice do sprite de movimento atual
        self.frame_idle = 0 # Índice do sprite de idle atual
        self.parado = True # Estado de movimento
        self.direction = "right" # Direção inicial (pode ser "left" ou "right")

        # Define a imagem inicial (começa virado para a direita por padrão)
        # Adiciona verificações antes de acessar as listas de sprites
        self.image = None
        if self.sprites_idle_direita:
             self.image = self.sprites_idle_direita[self.frame_idle % len(self.sprites_idle_direita)]
        elif self.sprites_idle_esquerda:
             self.image = self.sprites_idle_esquerda[self.frame_idle % len(self.sprites_idle_esquerda)]
        elif self.sprites_direita: # Fallback para primeiro sprite de movimento direita
             self.image = self.sprites_direita[0]
        elif self.sprites_esquerda: # Fallback para primeiro sprite de movimento esquerda
             self.image = self.sprites_esquerda[0]
        else: # Fallback para um placeholder si nenhuma lista de sprites existir
             tamanho_sprite_desejado_fallback = (60, 60)
             self.image = pygame.Surface(tamanho_sprite_desejado_fallback, pygame.SRCALPHA)
             pygame.draw.rect(self.image, (255, 0, 255), (0, 0, tamanho_sprite_desejado_fallback[0], tamanho_sprite_desejado_fallback[1]))


        # Garante que self.image não é None antes de criar self.rect
        if self.image is not None:
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            # Ajusta o tamanho do retângulo de colisão (hitbox)
            self.rect_colisao = self.rect.inflate(-30, -20) # Exemplo: reduz a hitbox em 30px na largura e 20px na altura
        else:
            # Define rects placeholders se a imagem falhou
            self.rect = pygame.Rect(self.x, self.y, 60, 60)
            self.rect_colisao = pygame.Rect(self.x, self.y, 30, 40)
            self.rect.center = (self.x, self.y)
            self.rect_colisao.center = self.rect.center
            print("AVISO(Player): Erro: Imagem inicial do jogador não definida. Usando rects placeholders.")


        # Controle de tempo de animação
        self.tempo_animacao = 100  # milissegundos entre frames
        self.ultimo_update = pygame.time.get_ticks() # >>> Inicialização de ultimo_update <<<

        # --- Atributos de Combate ---
        self.is_attacking = False
        self.attack_range = 80 # Distância do centro do jogador para a borda da hitbox de ataque
        self.attack_damage = 20 # Dano por ataque
        self.attack_cooldown = 1.0 # Cooldown em segundos
        self.last_attack_time = time.time() # Tempo do último ataque (em segundos)
        self.attack_duration = 0.3 # Duração da animação/estado de ataque (em segundos) - Ajuste!
        self.attack_timer = 0 # Tempo de início do ataque atual (em segundos)

        # Hitbox de ataque (será definida dinamicamente durante o ataque)
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.attack_hitbox_size = (60, 60) # Tamanho da hitbox de ataque (ajuste!)

        # Lista para rastrear inimigos já atingidos em um único ataque para evitar múltiplos hits
        self.hit_enemies_this_attack = set()


    def _carregar_sprites(self, caminhos, tamanho, nome_conjunto):
        """Carrega e escala uma lista de sprites, com tratamento de erro e placeholder."""
        sprites = []
        for path in caminhos:
            if not os.path.exists(path):
                # print(f"AVISO(Player): Arquivo de sprite não encontrado: {path}") # Debug removido
                # Cria um placeholder se o arquivo não existir
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255, 0, 255), (0, 0, tamanho[0], tamanho[1])) # Placeholder Magenta
                sprites.append(placeholder)
                continue # Pula para o próximo caminho

            try:
                sprite = pygame.image.load(path).convert_alpha()
                sprite = pygame.transform.scale(sprite, tamanho)
                sprites.append(sprite)
            except pygame.error as e:
                print(f"ERRO(Player): Erro ao carregar o sprite '{path}': {e}")
                # Cria um placeholder si houver erro de carregamento
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (255, 0, 255), (0, 0, tamanho[0], tamanho[1])) # Placeholder Magenta
                sprites.append(placeholder)

        if not sprites:
            print(f"AVISO(Player): Nenhum sprite carregado para o conjunto '{nome_conjunto}'. Usando placeholder padrão.")
            # Adiciona um placeholder si a lista de sprites estiver vazia
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(placeholder, (255, 0, 255), (0, 0, tamanho[0], tamanho[1])) # Placeholder Magenta
            sprites.append(placeholder) # Garante que a lista não está vazia

        return sprites


    # Removido o método handle_input, pois o ataque será automático


    def receber_dano(self, dano):
        """Reduz a vida do jogador."""
        # Verifica si o objeto vida existe antes de chamar o método
        if self.vida is not None:
            self.vida.receber_dano(dano)
            # A lógica de "Você morreu!" e fim de jogo está no Game.py, verificando self.vida.esta_vivo()
        # else:
             # print("AVISO(Player): Objeto vida não disponível. Jogador não pode receber dano.") # Debug removido


    def update(self):
        """Atualiza o estado do jogador (animação e posição do retângulo de colisão)."""
        agora = pygame.time.get_ticks()

        # Lógica de animação
        # >>> Verifica si self.ultimo_update e self.tempo_animacao existem antes de usar <<<
        if hasattr(self, 'ultimo_update') and hasattr(self, 'tempo_animacao') and agora - self.ultimo_update > self.tempo_animacao:
            self.ultimo_update = agora
            if self.parado:
                # Verifica si a lista de sprites de idle esquerda não está vazia antes de usar
                if self.sprites_idle_esquerda:
                     self.frame_idle = (self.frame_idle + 1) % len(self.sprites_idle_esquerda)
                     # Seleciona o sprite de idle correto com base na direção
                     if self.direction == "left" and self.sprites_idle_esquerda:
                          self.image = self.sprites_idle_esquerda[self.frame_idle]
                     elif self.direction == "right" and self.sprites_idle_direita:
                          self.image = self.sprites_idle_direita[self.frame_idle]
                     else: # Fallback para esquerda si direita não existir
                          self.image = self.sprites_idle_esquerda[self.frame_idle]
                elif self.sprites_idle_direita: # Fallback para direita si esquerda estiver vazia
                     self.frame_idle = (self.frame_idle + 1) % len(self.sprites_idle_direita)
                     self.image = self.sprites_idle_direita[self.frame_idle]
                elif self.sprites_esquerda: # Fallback para primeiro sprite de movimento esquerdo
                     self.image = self.sprites_esquerda[0]
                else: # Fallback para um placeholder si nenhuma lista de sprites de idle ou movimento existir
                     self.image = pygame.Surface((60, 60), pygame.SRCALPHA) # Placeholder

            else: # Si não estiver parado (a mover)
                 # Verifica si a lista de sprites de movimento esquerda não está vazia antes de usar
                 if self.sprites_esquerda:
                      self.atual = (self.atual + 1) % len(self.sprites_esquerda)
                      # Seleciona o sprite de movimento correto com base na direção
                      if self.direction == "left" and self.sprites_esquerda:
                           self.image = self.sprites_esquerda[self.atual]
                      elif self.direction == "right" and self.sprites_direita:
                           self.image = self.sprites_direita[self.atual]
                      else: # Fallback para esquerda si direita não existir
                           self.image = self.sprites_esquerda[self.atual]
                 elif self.sprites_direita: # Fallback para direita si esquerda estiver vazia
                      self.atual = (self.atual + 1) % len(self.sprites_direita)
                      self.image = self.sprites_direita[self.atual]
                 elif self.sprites_idle_esquerda: # Fallback para primeiro sprite de idle esquerdo
                      self.image = self.sprites_idle_esquerda[0]
                 else: # Fallback para um placeholder si nenhuma lista de sprites de movimento ou idle existir
                      self.image = pygame.Surface((60, 60), pygame.SRCALPHA) # Placeholder

        # Lógica de temporizador de ataque para resetar o estado is_attacking
        if self.is_attacking and time.time() - self.attack_timer >= self.attack_duration:
            self.is_attacking = False
            self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Reseta a hitbox quando o ataque termina
            self.hit_enemies_this_attack.clear() # Limpa a lista de inimigos atingidos

        # Atualiza a posição do retângulo de colisão (rect) para a posição atual do jogador
        if hasattr(self, 'rect'): # Verifica si self.rect existe
            self.rect.center = (self.x, self.y)
            # Atualiza a posição do retângulo de colisão secundário (rect_colisao)
            if hasattr(self, 'rect_colisao'): # Verifica si self.rect_colisao existe
                 self.rect_colisao.center = self.rect.center
        # else:
             # print("AVISO(Player): self.rect ou self.rect_colisao não existem. Não foi possível atualizar a posição.") # Debug removido


    def mover(self, teclas, arvores):
        """Move o jogador e atualiza a direção, verificando colisões com árvores."""
        dx = dy = 0

        # >>> Armazena a posição original antes do movimento <<<
        original_x = self.x
        original_y = self.y

        if teclas[pygame.K_LEFT]:
            dx = -self.velocidade
            self.direction = "left" # Atualiza a direção para esquerda
        if teclas[pygame.K_RIGHT]:
            dx = self.velocidade
            self.direction = "right" # Atualiza a direção para direita
        if teclas[pygame.K_UP]:
            dy = -self.velocidade
            # Não muda a direção horizontal para cima/baixo, mantém a última horizontal
        if teclas[pygame.K_DOWN]:
            dy = self.velocidade
            # Não muda a direção horizontal para cima/baixo, mantém a última horizontal

        # >>> Verifica movimento no eixo X <<<
        self.x += dx
        # Atualiza a posição do retângulo de colisão para o check de colisão X
        if hasattr(self, 'rect_colisao'):
             self.rect_colisao.center = (self.x, self.y)
             # Verifica colisões com as árvores após mover no X
             if arvores is not None: # Verifica si a lista de árvores não é None
                 for arvore in arvores:
                     # Verifica si a árvore existe e tem a hitbox de colisão reduzida
                     if arvore is not None and hasattr(arvore, 'collision_rect'):
                          # >>> Usa a hitbox de colisão da árvore para a detecção <<<
                          if self.rect_colisao.colliderect(arvore.collision_rect):
                               # Si houver colisão no X, reverte o movimento no X
                               self.x = original_x
                               if hasattr(self, 'rect_colisao'): # Atualiza a hitbox após reverter
                                    self.rect_colisao.center = (self.x, self.y)
                               break # Sai do loop de árvores após encontrar uma colisão
                     # Adicione lógica para outros tipos de obstáculos si necessário
                     # elif isinstance(arvore, OutroObstaculo) and hasattr(arvore, 'rect'):
                     #     if self.rect_colisao.colliderect(arvore.rect):
                     #         # Lógica de resposta à colisão para OutroObstaculo
                     #         self.x = original_x # Exemplo simples de reverter movimento
                     #         if hasattr(self, 'rect_colisao'):
                     #              self.rect_colisao.center = (self.x, self.y)
                     #         break


        # else:
             # print("AVISO(Player): self.rect_colisao não existe. Colisão com árvores no X não verificada.") # Debug removido


        # >>> Verifica movimento no eixo Y <<<
        self.y += dy
        # Atualiza a posição do retângulo de colisão para o check de colisão Y
        if hasattr(self, 'rect_colisao'):
             self.rect_colisao.center = (self.x, self.y)
             # Verifica colisões com as árvores após mover no Y
             if arvores is not None: # Verifica si a lista de árvores não é None
                 for arvore in arvores:
                      # Verifica si a árvore existe e tem a hitbox de colisão reduzida
                      if arvore is not None and hasattr(arvore, 'collision_rect'):
                           # >>> Usa a hitbox de colisão da árvore para a detecção <<<
                           if self.rect_colisao.colliderect(arvore.collision_rect):
                                # Si houver colisão no Y, reverte o movimento no Y
                                self.y = original_y
                                if hasattr(self, 'rect_colisao'): # Atualiza a hitbox após reverter
                                     self.rect_colisao.center = (self.x, self.y)
                                break # Sai do loop de árvores após encontrar uma colisão
                      # Adicione lógica para outros tipos de obstáculos si necessário
                      # elif isinstance(arvore, OutroObstaculo) and hasattr(arvore, 'rect'):
                      #     if self.rect_colisao.colliderect(arvore.rect):
                      #         # Lógica de resposta à colisão para OutroObstaculo
                      #         self.y = original_y # Exemplo simples de reverter movimento
                      #         if hasattr(self, 'rect_colisao'):
                      #              self.rect_colisao.center = (self.x, self.y)
                      #         break
        # else:
             # print("AVISO(Player): self.rect_colisao não existe. Colisão com árvores no Y não verificada.") # Debug removido


        # Atualiza o estado de parado
        self.parado = (dx == 0 and dy == 0)

        # A posição final do self.rect é atualizada no método update()


    # Removido o método trocar_arma, pois não é relevante para o ataque automático básico

    # Removido o método usar_arma, pois a lógica de ataque está no método atacar

    # >>> Implementação do método atacar (agora automático) <<<
    def atacar(self, inimigos):
        """
        Lógica de ataque automático do jogador.
        Verifica o cooldown e ataca inimigos dentro do alcance.
        """
        current_time = time.time()

        # Verifica si o cooldown passou
        if current_time - self.last_attack_time >= self.attack_cooldown:
            # print("DEBUG(Player): Tentando atacar...") # Debug removido
            self.last_attack_time = current_time # Reseta o cooldown
            self.is_attacking = True # Ativa a flag de ataque (para animação, etc.)
            self.attack_timer = current_time # Registra o tempo de início do ataque
            self.hit_enemies_this_attack.clear() # Limpa a lista de inimigos atingidos para o novo ataque
            # print("DEBUG(Player): Jogador iniciou ataque automático!") # Debug removido

            # Define a posição da hitbox de ataque baseada na direção do jogador e alcance
            attack_hitbox_width = getattr(self, 'attack_hitbox_size', (60, 60))[0]
            attack_hitbox_height = getattr(self, 'attack_hitbox_size', (60, 60))[1]
            self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)

            # Posiciona a hitbox de ataque (ajuste conforme a sua animação de ataque e alcance)
            # A hitbox é posicionada em relação ao centro do jogador
            hitbox_center_x = self.rect.centerx
            hitbox_center_y = self.rect.centery

            # Calcula a posição da hitbox com base na direção e alcance
            # Ajuste os offsets (ex: + self.attack_range) para posicionar a hitbox
            if self.direction == "right":
                # Exemplo: hitbox à direita do jogador
                self.attack_hitbox.midleft = (hitbox_center_x + self.attack_range, hitbox_center_y)
            elif self.direction == "left":
                # Exemplo: hitbox à esquerda do jogador
                self.attack_hitbox.midright = (hitbox_center_x - self.attack_range, hitbox_center_y)
            # Adicione outras direções (cima, baixo) si necessário, ajustando o offset
            # Exemplo para cima: self.attack_hitbox.midbottom = (hitbox_center_x, hitbox_center_y - self.attack_range)
            # Exemplo para baixo: self.attack_hitbox.midtop = (hitbox_center_x, hitbox_center_y + self.attack_range)


        # Verifica si o jogador está no estado de ataque para aplicar dano
        if self.is_attacking:
             # print("DEBUG(Player): Jogador está atacando. Verificando colisões com inimigos.") # Debug removido
             # Verifica si a lista de inimigos não é None e é iterável
             if inimigos is not None:
                 for inimigo in list(inimigos): # Itera sobre uma cópia para permitir remoção
                      # Verifica si o inimigo existe, está vivo e tem um retângulo de colisão
                      # É CRUCIAL QUE SEUS OBJETOS INIMIGOS TENHAM:
                      # 1. Um método esta_vivo() que retorna True ou False
                      # 2. Um atributo rect (pygame.Rect) para colisão
                      # 3. Um método receber_dano(dano)
                      if inimigo is not None and hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo() and hasattr(inimigo, 'rect'):
                           # Verifica colisão da hitbox de ataque do jogador com o inimigo
                           # E si o inimigo ainda não foi atingido neste ataque
                           if self.attack_hitbox.colliderect(inimigo.rect) and inimigo not in self.hit_enemies_this_attack:
                                # Aplica dano ao inimigo
                                if hasattr(inimigo, 'receber_dano'): # Verifica si o inimigo pode receber dano
                                     # print(f"DEBUG(Player): Acertou {type(inimigo).__name__}! Causando {self.attack_damage} de dano.") # Debug removido
                                     inimigo.receber_dano(self.attack_damage)
                                     self.hit_enemies_this_attack.add(inimigo) # Adiciona o inimigo à lista de atingidos
                                     # Opcional: Adicionar som ou efeito visual de hit
                                else:
                                     print(f"AVISO(Player): Aviso: Inimigo {type(inimigo).__name__} não tem método 'receber_dano'. Dano não aplicado.")
                      elif inimigo is not None:
                           if not hasattr(inimigo, 'esta_vivo'):
                                print(f"AVISO(Player): Aviso: Inimigo {type(inimigo).__name__} não tem método 'esta_vivo'. Ignorando para ataque.")
                           if not hasattr(inimigo, 'rect'):
                                print(f"AVISO(Player): Aviso: Inimigo {type(inimigo).__name__} não tem atributo 'rect'. Ignorando para ataque.")

        # Não há necessidade de resetar a flag do botão de ataque, pois ela foi removida


    def empurrar_jogador(self, inimigo):
        """Lógica para empurrar o jogador (se aplicável). Implementado pelos inimigos."""
        # Esta lógica geralmente é implementada no lado do inimigo
        pass # Placeholder

    # >>> Adicionado método desenhar para desenhar o jogador e a hitbox de ataque <<<
    def desenhar(self, janela, camera_x, camera_y):
        """Desenha o jogador e, si estiver atacando, a hitbox de ataque."""
        # Desenha o sprite do jogador
        if self.image is not None and hasattr(self, 'rect'):
            # Desenha o jogador com o offset da câmera
            janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        # else:
             # print("AVISO(Player): Imagem ou rect do jogador ausente. Não foi possível desenhar o jogador.") # Debug removido


        # Opcional: Desenhar a hitbox de colisão (para depuração)
        # Verifica si a hitbox de colisão existe
        # if hasattr(self, 'rect_colisao'):
        #     # Cria um retângulo visual com o offset da câmera
        #     colisao_visual = pygame.Rect(self.rect_colisao.x - camera_x, self.rect_colisao.y - camera_y, self.rect_colisao.width, self.rect_colisao.height)
        #     # Desenha o retângulo vermelho
        #     pygame.draw.rect(janela, (255, 0, 0), colisao_visual, 1) # Desenha um retângulo vermelho


        # Desenha a hitbox de ataque si estiver atacando (para depuração)
        # Verifica si a hitbox de ataque existe e tem um tamanho > 0 (si foi definida)
        if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0 and self.attack_hitbox.height > 0:
             # Cria um retângulo visual com o offset da câmera
             attack_hitbox_visual = pygame.Rect(self.attack_hitbox.x - camera_x, self.attack_hitbox.y - camera_y, self.attack_hitbox.width, self.attack_hitbox.height)
             # Desenha o retângulo verde
             pygame.draw.rect(janela, (0, 255, 0), attack_hitbox_visual, 2) # Desenha um retângulo verde


    def esta_vivo(self):
        """Retorna True si o jogador está vivo."""
        # Verifica si o objeto vida existe antes de chamar o método
        if self.vida is not None:
            return self.vida.esta_vivo()
        return False # Retorna False si o objeto vida não estiver disponível
