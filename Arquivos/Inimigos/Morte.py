import pygame
import random
import math
import time
import os

# --- Importação da Classe Base Inimigo ---
# Este bloco tenta importar a classe Inimigo de um módulo 'Inimigos'
# (assumindo que Inimigos.py está no mesmo nível ou num subdiretório específico).
# Se a importação falhar (ex: módulo não encontrado), um placeholder básico
# da classe InimigoBase é definido localmente para permitir que Morte
# ainda seja testado ou analisado de forma independente.
try:
    from .Inimigos import Inimigo as InimigoBase    # print("DEBUG(Morte): Classe base Inimigo importada com sucesso.")
except ImportError as e:
    # print(f"DEBUG(Morte): ERRO: Módulo 'Inimigos.py' não encontrado. Usando classe Inimigo placeholder: {e}.")
    class InimigoBase(pygame.sprite.Sprite):
        """
        Placeholder básico para InimigoBase caso a importação real falhe.
        Contém o mínimo necessário para a classe Morte funcionar.
        """
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((150, 0, 150, 100)) # Placeholder roxo claro
            pygame.draw.rect(self.image, (200, 0, 200), self.image.get_rect(), 1) # Borda

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
            self.last_contact_time = pygame.time.get_ticks() - 1000 # Inicializa para permitir contato imediato

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
                # Garante que len(self.sprites) não é zero antes de calcular o módulo
                if len(self.sprites) > 0:
                    self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
                self.tempo_ultimo_update_animacao = tempo_atual
            
            # Aplica o sprite atual e inverte se necessário
            if len(self.sprites) > 0: # Garante que há sprites para exibir
                current_sprite = self.sprites[self.sprite_index]
                if not self.facing_right:
                    self.image = pygame.transform.flip(current_sprite, True, False)
                else:
                    self.image = current_sprite
            else: # Fallback se a lista de sprites estiver vazia
                self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                self.image.fill((150, 0, 150, 100)) # Placeholder roxo

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


class Morte(InimigoBase):
    """
    Representa a Morte, um inimigo com habilidades específicas de ataque.
    Possui animações de andar e atacar.
    """
    sprites_andar, sprites_atacar = None, None # Separado em andar e atacar
    tamanho_sprite_definido = (96, 96)
    som_ataque_Morte, som_dano_Morte, som_morte_Morte, som_spawn_Morte = None, None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        # Sobe dois níveis para ir de 'Jogo/Arquivos/Inimigos/Morte.py' para 'Jogo/'
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_Morte(caminho_relativo_a_raiz_jogo):
        """
        Carrega um arquivo de som para a Morte, verificando se existe e tratando erros.
        Caminho_relativo_a_raiz_jogo deve ser relativo à pasta raiz do jogo.
        """
        pasta_raiz_jogo = Morte._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("/", os.sep))

        if not os.path.exists(caminho_completo):
            # print(f"DEBUG(Morte._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            # print(f"DEBUG(Morte._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            # print(f"DEBUG(Morte._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino, tamanho_sprite, nome_animacao):
        """
        Carrega uma lista de sprites para uma animação específica da Morte.
        Garante que os sprites são escalados e fornece placeholders em caso de falha.
        """
        pasta_raiz_jogo = Morte._obter_pasta_raiz_jogo()
        # print(f"DEBUG(Morte._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'.")

        # Garante que lista_destino é uma lista mutável e não None (se fosse passado None)
        if lista_destino is None:
            lista_destino = []
        else:
            # Limpa a lista existente se já houver conteúdo (para evitar duplicações em recargas)
            lista_destino.clear() 
        
        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("/", os.sep))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino.append(sprite)
                    # print(f"DEBUG(Morte._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    # print(f"DEBUG(Morte._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((200, 0, 200, 180)) # Cor roxa clara para placeholder
                    lista_destino.append(placeholder)
            except pygame.error as e:
                # print(f"DEBUG(Morte._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder.")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((200, 0, 200, 180))
                lista_destino.append(placeholder)

        # Fallback final se nenhuma sprite for carregada
        if not lista_destino:
            # print(f"DEBUG(Morte._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final.")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((150, 0, 150, 200)) # Roxa mais escura
            lista_destino.append(placeholder)
        
        return lista_destino # Retorna a lista modificada (importante para atribuição direta)

    @staticmethod
    def carregar_recursos_Morte():
        """
        Carrega todos os sprites e sons para a classe Morte.
        Este método é chamado apenas uma vez, na primeira instanciação da Morte.
        """
        # Carregar sprites de andar (necessita de caminhos reais de sprites de andar/idle)
        if Morte.sprites_andar is None:
            # EXEMPLO: SUBSTITUA ESTES CAMINHOS PELOS SEUS SPRITES DE ANDAR/IDLE DA MORTE
            caminhos_andar = [
                "Sprites\\Inimigos\\Morte\\Andar1.png",
                "Sprites\\Inimigos\\Morte\\Andar2.png",
                "Sprites\\Inimigos\\Morte\\Andar3.png",
                # ... adicione mais frames conforme necessário
            ]
            Morte.sprites_andar = Morte._carregar_lista_sprites_estatico(
                caminhos_andar,
                [], # Passar uma nova lista vazia
                Morte.tamanho_sprite_definido,
                "Andar"
            )

        # Carregar sprites de atacar
        if Morte.sprites_atacar is None:
            # CORRIGIDO: Adicionado a extensão .png aos caminhos de ataque
            caminhos_atacar = [
                "Sprites\\Inimigos\\Morte\\Ataque1.png",
                "Sprites\\Inimigos\\Morte\\Ataque2.png",
                "Sprites\\Inimigos\\Morte\\Ataque3.png",
            ]
            
            Morte.sprites_atacar = Morte._carregar_lista_sprites_estatico(
                caminhos_atacar,
                [], # Passar uma nova lista vazia
                Morte.tamanho_sprite_definido,
                "Atacar"
            )

            # Fallback: Se os sprites de ataque falharem, usa o primeiro sprite de andar
            if not Morte.sprites_atacar and Morte.sprites_andar:
                Morte.sprites_atacar = [Morte.sprites_andar[0]]
                # print("DEBUG(Morte.carregar_recursos): Usando primeiro sprite de andar como fallback para ataque.")
            elif not Morte.sprites_atacar: # Fallback se nem os sprites de andar existirem
                placeholder = pygame.Surface(Morte.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder.fill((150, 0, 150, 200)) # Roxa mais escura
                Morte.sprites_atacar = [placeholder]
                # print("DEBUG(Morte.carregar_recursos): Usando placeholder de cor para ataque (sprites de andar também falharam).")

        # Carregar sons (linhas comentadas - descomente quando os arquivos de som estiverem disponíveis)
        if not Morte.sons_carregados:
            # Morte.som_ataque_Morte = Morte._carregar_som_Morte("Sons/Morte/ataque_morte.wav")
            # Morte.som_dano_Morte = Morte._carregar_som_Morte("Sons/Morte/dano_morte.wav")
            # Morte.som_morte_Morte = Morte._carregar_som_Morte("Sons/Morte/morte_morte.wav")
            # Morte.som_spawn_Morte = Morte._carregar_som_Morte("Sons/Morte/spawn_morte.wav")
            Morte.sons_carregados = True

    def __init__(self, x, y, velocidade=2.5):
        """
        Inicializa uma nova instância da Morte.
        x, y: Posição inicial da Morte.
        velocidade: Velocidade de movimento da Morte.
        """
        Morte.carregar_recursos_Morte() # Garante que os recursos estão carregados

        # Definição das características da Morte
        vida_morte = 90
        dano_contato_morte = 10
        xp_morte = 75
        moedas_dropadas = 12
        sprite_path_ref = "Sprites/Inimigos/Morte/Ataque1.png" # Caminho de referência para a classe base

        # Chama o construtor da classe base InimigoBase
        super().__init__(x, y,
                         Morte.tamanho_sprite_definido[0], Morte.tamanho_sprite_definido[1],
                         vida_morte, velocidade, dano_contato_morte,
                         xp_morte, sprite_path_ref)

        self.moedas_drop = moedas_dropadas # Define as moedas para esta instância (para uso externo)

        # Atribui as listas de sprites carregadas
        self.sprites_andar_anim = Morte.sprites_andar # Renomeado para evitar conflito com self.sprites
        self.sprites_atacar_anim = Morte.sprites_atacar # Renomeado
        
        # Começa com a animação de andar
        self.sprites = self.sprites_andar_anim if self.sprites_andar_anim else [self.image]
        
        self.sprite_index = 0
        self.intervalo_animacao_andar = 120 # Animação de andar
        self.intervalo_animacao_atacar = 100 # Animação de ataque mais rápida
        self.intervalo_animacao = self.intervalo_animacao_andar # Intervalo inicial
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()

        self.is_attacking = False
        self.attack_duration = 0.6 # Duração do ataque em segundos
        self.attack_timer = 0.0 # Tempo em que o ataque começou
        self.attack_damage = 20 # Dano causado pelo ataque
        self.attack_hitbox_size = (70, 70) # Tamanho da hitbox do ataque
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Hitbox real do ataque
        self.attack_range = 120 # Alcance para iniciar o ataque
        self.attack_cooldown = 2.5 # Cooldown entre ataques em segundos
        self.last_attack_time = time.time() - self.attack_cooldown # Inicializa para permitir ataque imediato
        self.hit_player_this_attack = False # Flag para hit único por ataque

        # Define a imagem inicial e o rect
        if self.sprites:
            self.image = self.sprites[0]
        else:
            self.image = pygame.Surface(Morte.tamanho_sprite_definido, pygame.SRCALPHA)
            self.image.fill((150, 0, 150, 100)) # Fallback se não houver sprites carregados

        self.rect = self.image.get_rect(topleft=(self.x, self.y)) # Atualiza o rect com a posição float


    def receber_dano(self, dano, fonte_dano_rect=None):
        """
        Reduz a vida da Morte e lida com a reprodução de sons de dano/morte.
        """
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect) # Chama o método da classe base

        if not self.esta_vivo() and vida_antes > 0: # Morte morreu
            if Morte.som_morte_Morte:
                # Morte.som_morte_Morte.play()
                pass # Descomente para ativar o som de morte
        elif self.esta_vivo() and vida_antes > self.hp: # Morte levou dano, mas continua viva
            if Morte.som_dano_Morte:
                # Morte.som_dano_Morte.play()
                pass # Descomente para ativar o som de dano

    def atacar(self, player):
        """
        Inicia o ataque da Morte se as condições forem atendidas.
        """
        if not (hasattr(player, 'rect') and self.esta_vivo()):
            return

        current_time = time.time()
        # Condições para atacar: não está atacando, e cooldown terminou
        if not self.is_attacking and (current_time - self.last_attack_time >= self.attack_cooldown):
            
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                              self.rect.centery - player.rect.centery)
            
            if distancia_ao_jogador <= self.attack_range:
                self.is_attacking = True
                self.attack_timer = current_time
                self.last_attack_time = current_time
                self.hit_player_this_attack = False # Resetar para permitir hit neste ataque
                
                # Troca para sprites de ataque e ajusta animação
                self.sprites = self.sprites_atacar_anim 
                self.intervalo_animacao = self.intervalo_animacao_atacar
                self.sprite_index = 0 # Reinicia a animação de ataque

                # Define a hitbox do ataque
                self.attack_hitbox = pygame.Rect(0, 0, *self.attack_hitbox_size) 
                self.attack_hitbox.center = self.rect.center # Posiciona no centro da Morte inicialmente

                # if Morte.som_ataque_Morte: Morte.som_ataque_Morte.play()


    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        """
        Atualiza o estado da Morte a cada frame.
        Lida com lógica de morte, ataque e movimento.
        """
        # A lógica de recompensa ao morrer e remoção do sprite
        # é tratada externamente pelo GerenciadorDeInimigos.py
        if not self.esta_vivo():
            self.kill() 
            return # Não processa mais nada se estiver morta

        agora = pygame.time.get_ticks()
        current_time_sec = time.time() # Usar time.time() para cooldowns

        # Validação robusta do objeto player
        jogador_valido = (player and
                          hasattr(player, 'rect') and
                          hasattr(player, 'vida') and
                          hasattr(player.vida, 'esta_vivo') and
                          player.vida.esta_vivo() and # Garante que o jogador está vivo
                          hasattr(player, 'receber_dano'))

        if not jogador_valido:
            # Se o jogador não for válido, apenas atualiza a animação e retorna.
            self.atualizar_animacao()
            return

        # Lógica de ataque e movimento
        if self.is_attacking:
            # Atualiza a posição da hitbox de ataque para seguir a Morte
            self.attack_hitbox.center = self.rect.center 

            # Verifica colisão da hitbox de ataque com o jogador
            # Usa player.rect para a colisão, como no código original
            if not self.hit_player_this_attack and self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage, self.rect) # Causa dano
                self.hit_player_this_attack = True # Marca que o jogador foi atingido
            
            # Verifica se a duração do ataque terminou
            if current_time_sec - self.attack_timer > self.attack_duration:
                self.is_attacking = False # Termina o estado de ataque
                self.sprites = self.sprites_andar_anim # Volta para os sprites de andar
                self.intervalo_animacao = self.intervalo_animacao_andar # Restaura o intervalo de animação
        else:
            # Se não estiver atacando, tenta iniciar um ataque
            self.atacar(player)
            # E se não estiver atacando, move-se em direção ao jogador
            if not self.is_attacking: # Verifica novamente caso atacar() tenha ativado is_attacking
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
        
        # Atualização da animação (agora após toda a lógica de estado)
        self.atualizar_animacao()

        # Dano de contato (independente da lógica de ataque direto)
        # Só causa dano de contato se não estiver atacando e o jogador for válido
        if jogador_valido and not self.is_attacking and self.rect.colliderect(player.rect) and \
           (agora - self.last_contact_time >= self.contact_cooldown):
            player.receber_dano(self.contact_damage, self.rect)
            self.last_contact_time = agora

    # O método desenhar é herdado da InimigoBase e funciona bem.
    # Descomente o bloco abaixo para adicionar visualização da hitbox de debug.
    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y)
    #     # Desenha a hitbox de ataque para debug (apenas se estiver ativa)
    #     if self.is_attacking and self.attack_hitbox.width > 0:
    #         debug_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
    #         pygame.draw.rect(surface, (255, 0, 0, 100), debug_rect_onscreen, 1) # Retângulo semi-transparente vermelho
    #     # Desenha a hitbox do próprio inimigo para debug
    #     # debug_morte_rect_onscreen = self.rect.move(-camera_x, -camera_y)
    #     # pygame.draw.rect(surface, (0, 255, 255, 100), debug_morte_rect_onscreen, 1)
