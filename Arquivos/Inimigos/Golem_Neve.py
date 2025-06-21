import pygame
import os
import math
import time

# --- Importação da Classe Base Inimigo ---
# Este bloco tenta importar a classe Inimigo de um módulo 'Inimigos'
# (assumindo que Inimigos.py está no mesmo nível ou num subdiretório específico).
# Se a importação falhar (ex: módulo não encontrado), um placeholder básico
# da classe InimigoBase é definido localmente para permitir que Golem_Neve
# ainda seja testado ou analisado de forma independente.
try:
    from .Inimigos import Inimigo as InimigoBase    # print("DEBUG(Morte): Classe base Inimigo importada com sucesso.")
    # print(f"DEBUG(Golem_Neve): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError:
    # print(f"DEBUG(Golem_Neve): FALHA ao importar InimigoBase. Usando placeholder local BÁSICO.")
    class InimigoBase(pygame.sprite.Sprite):
        """
        Placeholder básico para InimigoBase caso a importação real falhe.
        Contém o mínimo necessário para Golem_Neve funcionar.
        """
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((180, 200, 230, 100)) # Placeholder azul-acinzentado claro
            pygame.draw.rect(self.image, (200,220,255), self.image.get_rect(), 1) # Borda azul muito clara

            self.hp = vida_maxima
            self.max_hp = vida_maxima
            self.velocidade = velocidade
            self.contact_damage = dano_contato
            self.xp_value = xp_value
            self.facing_right = True
            self.last_hit_time = 0 # Tempo do último acerto (para flash de dano)
            self.hit_flash_duration = 150 # Duração do flash de dano em ms
            self.hit_flash_color = (255, 255, 255, 128) # Cor do flash

            self.contact_cooldown = 1000 # Cooldown para dano de contato em ms
            self.last_contact_time = pygame.time.get_ticks() - self.contact_cooldown # Inicializa para permitir contato imediato

            self.sprites = [self.image.copy()] # Lista de sprites para animação
            self.sprite_index = 0 # Índice do sprite atual
            self.intervalo_animacao = 200 # Intervalo entre frames de animação em ms
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Tempo do último update de animação

            self.moedas_drop = 0 # Valor em moedas a dropar, se aplicável
            self.x = float(x) # Posição X como float para movimento mais suave
            self.y = float(y) # Posição Y como float

        def receber_dano(self, dano, fonte_dano_rect=None):
            """Reduz a vida do inimigo e inicia o flash de dano."""
            self.hp = max(0, self.hp - dano)
            self.last_hit_time = pygame.time.get_ticks()

        def esta_vivo(self):
            """Verifica se o inimigo ainda está vivo."""
            return self.hp > 0

        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None):
            """
            Move o inimigo em direção a um alvo.
            dt_ms (delta time em milissegundos) permite movimento independente da taxa de frames.
            """
            if dt_ms is None: # Se dt_ms não for fornecido, usa um valor fixo (para testes)
                dt_factor = 1.0
            else:
                dt_factor = dt_ms / 1000.0 # Converte ms para segundos

            dx = alvo_x - self.rect.centerx
            dy = alvo_y - self.rect.centery
            dist = math.hypot(dx, dy)

            if dist > 0:
                # Normaliza o vetor de direção
                dx_norm = dx / dist
                dy_norm = dy / dist

                # Calcula o deslocamento
                move_amount = self.velocidade * dt_factor
                
                # Garante que o inimigo não ultrapasse o alvo num único passo
                if move_amount > dist:
                    move_amount = dist

                self.x += dx_norm * move_amount
                self.y += dy_norm * move_amount

                self.rect.x = int(self.x)
                self.rect.y = int(self.y)

                # Atualiza a direção para virar o sprite
                if dx_norm > 0:
                    self.facing_right = True
                elif dx_norm < 0:
                    self.facing_right = False

        def atualizar_animacao(self):
            """
            Atualiza o frame da animação do inimigo.
            Deve ser chamada no método update do inimigo.
            """
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
                self.tempo_ultimo_update_animacao = tempo_atual
            
            # Aplica o sprite atual e inverte se necessário
            current_sprite = self.sprites[self.sprite_index]
            if not self.facing_right:
                self.image = pygame.transform.flip(current_sprite, True, False)
            else:
                self.image = current_sprite
            
            # Aplica o efeito de flash de dano
            if tempo_atual - self.last_hit_time < self.hit_flash_duration:
                flash_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                flash_surface.fill(self.hit_flash_color)
                self.image.blit(flash_surface, (0, 0))


        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            """
            Método de update genérico para o inimigo.
            Lida com movimento básico e atualização de animação.
            """
            self.atualizar_animacao() # Sempre atualiza a animação

            # Exemplo de movimento para o player (se ele for válido)
            if player and hasattr(player, 'rect') and player.esta_vivo():
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)

        def desenhar(self, janela, camera_x, camera_y):
            """Desenha o inimigo na janela, considerando a posição da câmera."""
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

        def kill(self):
            """Remove o inimigo dos grupos de sprites."""
            super().kill() # Chama o método kill da classe base pygame.sprite.Sprite


# Assumimos que 'score_manager' é um módulo importável.
# Se score.py não existir ou não contiver score_manager,
# este placeholder simples evita um erro de NameError.
try:
    from score import score_manager
except ImportError:
    # print("DEBUG(Golem_Neve): Módulo 'score_manager' não encontrado. Usando placeholder.")
    class ScoreManagerPlaceholder:
        def adicionar_xp(self, xp_value):
            # print(f"DEBUG(ScoreManagerPlaceholder): Adicionando XP (placeholder): {xp_value}")
            pass # No-op para o placeholder
    score_manager = ScoreManagerPlaceholder()


class Golem_Neve(InimigoBase):
    """
    Representa um Golem de Neve, um tipo de inimigo lento e forte.
    Possui animações de andar e atacar, e um ataque corpo a corpo específico.
    """
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (170, 160) # Tamanho dos sprites do Golem de Neve

    som_ataque_golem = None
    som_dano_golem = None
    som_morte_golem = None
    som_spawn_golem = None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        # Sobe dois níveis para ir de 'Jogo/Arquivos/Inimigos/Golem_Neve.py' para 'Jogo/'
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_golem_neve(caminho_relativo_a_raiz_jogo):
        """
        Carrega um arquivo de som, verificando se existe e tratando erros.
        Caminho_relativo_a_raiz_jogo deve ser relativo à pasta raiz do jogo.
        """
        pasta_raiz_jogo = Golem_Neve._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("/", os.sep))

        if not os.path.exists(caminho_completo):
            # print(f"DEBUG(Golem_Neve._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            # print(f"DEBUG(Golem_Neve._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            # print(f"DEBUG(Golem_Neve._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino, tamanho_sprite, nome_animacao):
        """
        Carrega uma lista de sprites para uma animação específica.
        Garante que os sprites são escalados e fornece placeholders em caso de falha.
        """
        pasta_raiz_jogo = Golem_Neve._obter_pasta_raiz_jogo()
        # print(f"DEBUG(Golem_Neve._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'.")

        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("/", os.sep))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino.append(sprite)
                    # print(f"DEBUG(Golem_Neve._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    # print(f"DEBUG(Golem_Neve._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((200, 220, 255, 180)) # Cor azul claro para placeholder
                    lista_destino.append(placeholder)
            except pygame.error as e:
                # print(f"DEBUG(Golem_Neve._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder.")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((200, 220, 255, 180))
                lista_destino.append(placeholder)

        # Fallback final se nenhuma sprite for carregada
        if not lista_destino:
            # print(f"DEBUG(Golem_Neve._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final.")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((180, 200, 230, 200)) # Azul acinzentado mais escuro
            lista_destino.append(placeholder)

    @staticmethod
    def carregar_recursos_golem_neve():
        """
        Carrega todos os sprites e sons para a classe Golem_Neve.
        Este método é chamado apenas uma vez, na primeira instanciação do Golem.
        """
        # Carregar sprites de andar
        if Golem_Neve.sprites_andar_carregados is None:
            Golem_Neve.sprites_andar_carregados = []
            caminhos_andar = [
                "Sprites/Inimigos/Golem Neve/GN1.png",
                "Sprites/Inimigos/Golem Neve/GN2.png",
                "Sprites/Inimigos/Golem Neve/GN3.png",
            ]
            Golem_Neve._carregar_lista_sprites_estatico(
                caminhos_andar,
                Golem_Neve.sprites_andar_carregados,
                Golem_Neve.tamanho_sprite_definido,
                "Andar"
            )

        # Carregar sprites de atacar
        if Golem_Neve.sprites_atacar_carregados is None:
            Golem_Neve.sprites_atacar_carregados = []
            caminhos_atacar = [
                "Sprites/Inimigos/Golem Neve/GN_Atacar1.png",
                "Sprites/Inimigos/Golem Neve/GN_Atacar2.png",
                "Sprites/Inimigos/Golem Neve/GN_Atacar3.png",
            ]
            
            # Tenta carregar os sprites de ataque
            Golem_Neve._carregar_lista_sprites_estatico(
                caminhos_atacar,
                Golem_Neve.sprites_atacar_carregados,
                Golem_Neve.tamanho_sprite_definido,
                "Atacar"
            )

            # Fallback: Se os sprites de ataque falharem, usa o primeiro sprite de andar
            if not Golem_Neve.sprites_atacar_carregados:
                if Golem_Neve.sprites_andar_carregados and len(Golem_Neve.sprites_andar_carregados) > 0:
                    Golem_Neve.sprites_atacar_carregados = [Golem_Neve.sprites_andar_carregados[0]]
                    # print("DEBUG(Golem_Neve.carregar_recursos): Usando primeiro sprite de andar como fallback para ataque.")
                else:
                    # Fallback final se nem os de andar existirem
                    placeholder_ataque = pygame.Surface(Golem_Neve.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder_ataque.fill((180,200,230, 180)) # Azul acinzentado
                    Golem_Neve.sprites_atacar_carregados = [placeholder_ataque]
                    # print("DEBUG(Golem_Neve.carregar_recursos): Usando placeholder de cor para ataque (sprites de andar também falharam).")

        # Carregar sons (linhas comentadas - descomente quando os arquivos de som estiverem disponíveis)
        if not Golem_Neve.sons_carregados:
            # Golem_Neve.som_ataque_golem = Golem_Neve._carregar_som_golem_neve("Sons/Golem_Neve/ataque_impacto_neve.wav")
            # Golem_Neve.som_dano_golem = Golem_Neve._carregar_som_golem_neve("Sons/Golem_Neve/dano_quebrar_gelo.wav")
            # Golem_Neve.som_morte_golem = Golem_Neve._carregar_som_golem_neve("Sons/Golem_Neve/morte_desmoronar.wav")
            # Golem_Neve.som_spawn_golem = Golem_Neve._carregar_som_golem_neve("Sons/Golem_Neve/spawn_passos_pesados.wav")
            Golem_Neve.sons_carregados = True


    def __init__(self, x, y, velocidade=1): # Golem é caracteristicamente lento
        """
        Inicializa uma nova instância de Golem_Neve.
        x, y: Posição inicial do Golem.
        velocidade: Velocidade de movimento do Golem.
        """
        Golem_Neve.carregar_recursos_golem_neve() # Garante que os recursos estão carregados

        # Definição das características do Golem de Neve
        vida_golem = 120
        dano_contato_golem = 120 # Dano de contato alto
        xp_golem = 600
        moedas_dropadas = 25 # Moedas que o Golem dropará ao ser derrotado
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Golem Neve/GN1.png" # Usado pela base, mas gerenciado pelos sprites carregados

        # Chama o construtor da classe base InimigoBase
        super().__init__(
            x, y,
            Golem_Neve.tamanho_sprite_definido[0], Golem_Neve.tamanho_sprite_definido[1],
            vida_golem, velocidade, dano_contato_golem,
            xp_golem, sprite_path_principal_relativo_jogo
        )

        self.moedas_drop = moedas_dropadas # Define as moedas para esta instância

        # Atribui as listas de sprites carregadas
        self.sprites_andar = Golem_Neve.sprites_andar_carregados
        self.sprites_atacar = Golem_Neve.sprites_atacar_carregados
        self.sprites = self.sprites_andar # Começa com a animação de andar

        # Garante que self.image esteja definido, mesmo que a base falhe ou se baseie em sprite_path
        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            # print("DEBUG(Golem_Neve __init__): self.image não foi definido pelo super(). Usando primeiro sprite de andar.")
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
            else:
                placeholder_img = pygame.Surface(Golem_Neve.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((150,180,210, 150)) # Placeholder de cor
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image] # Garante que self.sprites não está vazia

        self.rect = self.image.get_rect(topleft=(self.x, self.y)) # Atualiza o rect com a posição float

        self.sprite_index = 0
        self.intervalo_animacao_andar = 380 # Animação de andar mais lenta em ms
        self.intervalo_animacao_atacar = 280 # Animação de ataque mais rápida em ms
        self.intervalo_animacao = self.intervalo_animacao_andar # Intervalo inicial

        self.is_attacking = False # Flag para estado de ataque
        self.attack_duration = 1.0 # Duração total do ataque em segundos
        self.attack_timer = 0.0 # Tempo em que o ataque começou (usando pygame.time.get_ticks())
        self.attack_damage_especifico = 25 # Dano causado pelo ataque específico
        self.attack_range = 30 # Alcance máximo para iniciar o ataque (pixels)
        self.attack_cooldown = 3.8 # Cooldown entre ataques em segundos
        # Inicializa o cooldown para permitir o ataque quase imediato após o spawn
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)

        # Definições da hitbox do ataque
        self.attack_hitbox_largura = self.tamanho_sprite_definido[0] * 0.6
        self.attack_hitbox_altura = self.tamanho_sprite_definido[1] * 0.4
        self.attack_hitbox_offset_x = 25 # Deslocamento horizontal da hitbox em relação ao centro do golem
        self.attack_hitbox = pygame.Rect(0,0,0,0) # Hitbox real do ataque
        self.hit_player_this_attack_swing = False # Flag para garantir que o jogador só seja atingido uma vez por ataque

        self.ouro_concedido = False # Flag para controle de recompensa ao ser derrotado

        # Se o som de spawn for carregado, reproduz
        # if Golem_Neve.som_spawn_golem:
        #     Golem_Neve.som_spawn_golem.play()


    def _atualizar_hitbox_ataque(self):
        """
        Atualiza a posição e o tamanho da hitbox de ataque do Golem.
        A hitbox é ajustada com base na direção em que o Golem está a virar.
        """
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0) # Torna a hitbox inativa se não estiver atacando
            return

        self.attack_hitbox.width = self.attack_hitbox_largura
        self.attack_hitbox.height = self.attack_hitbox_altura

        # Posiciona a hitbox de acordo com a direção do Golem
        if self.facing_right:
            # Para a direita: midleft da hitbox alinhado com a parte direita do sprite
            self.attack_hitbox.midleft = (self.rect.right - self.attack_hitbox_offset_x, self.rect.centery)
        else:
            # Para a esquerda: midright da hitbox alinhado com a parte esquerda do sprite
            self.attack_hitbox.midright = (self.rect.left + self.attack_hitbox_offset_x, self.rect.centery)


    def atacar(self, player):
        """
        Inicia o ataque específico do Golem de Neve se as condições forem atendidas.
        Verifica a distância ao jogador e o cooldown do ataque.
        """
        # Verifica se o jogador é válido e o golem está vivo
        if not (hasattr(player, 'rect') and self.esta_vivo()):
            return

        agora = pygame.time.get_ticks()
        # Calcula a distância do centro do Golem ao centro do jogador
        distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                          self.rect.centery - player.rect.centery)

        # Condições para iniciar um ataque:
        # 1. Não está já a atacar
        # 2. Jogador dentro do alcance de ataque
        # 3. Cooldown do ataque terminou
        if not self.is_attacking and \
           distancia_ao_jogador <= self.attack_range and \
           (agora - self.last_attack_time >= self.attack_cooldown * 1000):

            self.is_attacking = True # Define o estado de ataque
            self.attack_timer = agora # Guarda o tempo de início do ataque
            self.last_attack_time = agora # Atualiza o último tempo de ataque
            self.hit_player_this_attack_swing = False # Reinicia a flag de hit para o novo ataque

            # Troca para os sprites de ataque e ajusta o intervalo da animação
            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0 # Reinicia a animação de ataque

            # Se o som de ataque for carregado, reproduz
            # if Golem_Neve.som_ataque_golem:
            #     Golem_Neve.som_ataque_golem.play()


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        """
        Atualiza o estado do Golem de Neve a cada frame.
        Lida com lógica de morte, ataque, movimento e dano de contato.
        """
        # Se o Golem não estiver vivo, processa as recompensas e remove-o.
        if not self.esta_vivo():
            # Garante que as moedas e XP são concedidas apenas uma vez
            if not self.ouro_concedido:
                if hasattr(player, "dinheiro"): # Verifica se o player tem atributo dinheiro
                    player.dinheiro += self.moedas_drop
                score_manager.adicionar_xp(self.xp_value) # Adiciona XP ao score manager
                self.ouro_concedido = True # Marca que as recompensas foram concedidas
            self.kill() # Remove o sprite
            return # Não processa mais nada se estiver morto

        agora = pygame.time.get_ticks()

        # Validação robusta do objeto player
        jogador_valido = (player and
                          hasattr(player, 'rect') and
                          hasattr(player, 'vida') and
                          hasattr(player.vida, 'esta_vivo') and
                          player.vida.esta_vivo() and # Garante que o jogador está vivo
                          hasattr(player, 'receber_dano'))

        # Lógica quando o Golem está a atacar
        if self.is_attacking:
            self.atualizar_animacao() # Continua a animação de ataque
            self._atualizar_hitbox_ataque() # Atualiza a posição da hitbox de ataque

            # Verifica colisão da hitbox de ataque com o jogador
            if jogador_valido and not self.hit_player_this_attack_swing and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico) # Causa dano ao jogador
                self.hit_player_this_attack_swing = True # Marca que o jogador foi atingido neste ataque
                # print(f"DEBUG(Golem_Neve): Ataque MELEE acertou jogador! Dano: {self.attack_damage_especifico}")

            # Verifica se a duração do ataque terminou
            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False # Termina o estado de ataque
                self.sprites = self.sprites_andar # Volta para os sprites de andar
                self.intervalo_animacao = self.intervalo_animacao_andar # Restaura o intervalo de animação
                self.sprite_index = 0 # Reinicia a animação de andar
                self.attack_hitbox.size = (0,0) # Desativa a hitbox de ataque
        else:
            # Se não estiver atacando e o jogador for válido, tenta iniciar um ataque
            if jogador_valido:
                self.atacar(player)

            # Se não estiver atacando e o jogador for válido, move-se em direção a ele
            if not self.is_attacking and jogador_valido:
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)

            self.atualizar_animacao() # Atualiza a animação de andar/idle

        # Lógica de dano de contato (se o Golem estiver a tocar no jogador)
        # É independente do ataque específico e tem seu próprio cooldown.
        if jogador_valido and self.rect.colliderect(player.rect) and \
           (agora - self.last_contact_time >= self.contact_cooldown):
            player.receber_dano(self.contact_damage) # Causa dano de contato
            self.last_contact_time = agora # Atualiza o tempo do último contato


    def receber_dano(self, dano, fonte_dano_rect=None):
        """
        Recebe dano, reduz a vida e reproduz sons de dano/morte.
        fonte_dano_rect: opcional, para determinar a direção do empurrão ou efeito.
        """
        vida_antes = self.hp # Guarda a vida antes de receber o dano
        super().receber_dano(dano, fonte_dano_rect) # Chama o método da classe base

        # Lógica para reproduzir sons
        if self.esta_vivo():
            # Se ainda estiver vivo e o dano realmente reduziu a vida
            if vida_antes > self.hp and Golem_Neve.som_dano_golem:
                # Golem_Neve.som_dano_golem.play()
                pass # Descomente para ativar o som de dano
        elif vida_antes > 0: # Golem acabou de morrer (HP > 0 antes, agora HP <= 0)
            if Golem_Neve.som_morte_golem:
                # Golem_Neve.som_morte_golem.play()
                pass # Descomente para ativar o som de morte

    # O método desenhar é herdado da InimigoBase e funciona bem.
    # Descomente o bloco abaixo para adicionar visualização da hitbox de debug.
    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y)
    #     # Desenha a hitbox de ataque para debug (apenas se estiver ativa)
    #     if self.is_attacking and self.attack_hitbox.width > 0:
    #         debug_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
    #         pygame.draw.rect(surface, (180, 200, 230, 100), debug_rect_onscreen, 1) # Retângulo semi-transparente
