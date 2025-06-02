# GerenciadorDeInimigos.py
import pygame
import random
import time
import math
import threading
import queue # Para fila thread-safe
import os 

# Tenta importar todas as classes de inimigos de reuniaoInimigos.py
# Se reuniaoInimigos.py não for encontrado, ou se ele mesmo tiver problemas
# ao importar classes específicas, este bloco tenta lidar com isso graciosamente.
try:
    from reuniaoInimigos import * # Importa nomes como Fantasma, BonecoDeNeve, etc.
    print("DEBUG(GerenciadorDeInimigos): Classes de 'reuniaoInimigos' importadas (ou definidas como None lá).")
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): ERRO CRÍTICO: Módulo 'reuniaoInimigos.py' NÃO encontrado.")
    print("DEBUG(GerenciadorDeInimigos): Todos os tipos de inimigos específicos serão definidos como None.")
    # Fallback: Define todos os nomes de classes de inimigos esperados como None
    # para que o resto do script não falhe com NameError imediatamente.
    # A lógica subsequente que usa essas classes (ex: `if Fantasma:`) deve
    # verificar se elas não são None antes de tentar usá-las.
    Fantasma = BonecoDeNeve = Planta_Carnivora = Espantalho = Fenix = None
    Mae_Natureza = Espirito_Das_Flores = Lobo = Urso = None
    # ProjetilNeve não estava na lista de fallback anterior, adicionando se necessário
    ProjetilNeve = None 
    Troll = Golem_Neve = Goblin = Vampiro = Demonio = None


class Inimigo(pygame.sprite.Sprite): # Classe base Inimigo (placeholder ou real)
    def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
        super().__init__()
        self.x = x # Posição inicial x
        self.y = y # Posição inicial y
        self.largura = largura # Largura do inimigo
        self.altura = altura   # Altura do inimigo
        self.hp = vida_maxima # Pontos de vida atuais
        self.max_hp = vida_maxima # Pontos de vida máximos
        self.velocidade = velocidade # Velocidade de movimento
        self.contact_damage = dano_contato # Dano causado ao tocar no jogador
        self.xp_value = xp_value # Valor de XP concedido ao ser derrotado
        self.sprite_path_base = sprite_path # Caminho base para o sprite

        # Carrega o sprite ou cria um placeholder visual
        if sprite_path: 
            self.image = self._carregar_sprite(sprite_path, (largura, altura))
        else:
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA) # Cria superfície transparente
            pygame.draw.rect(self.image, (255, 0, 255, 128), (0, 0, largura, altura)) # Desenha um retângulo magenta semi-transparente
        
        self.rect = self.image.get_rect(topleft=(self.x, self.y)) # Define o retângulo de colisão
        
        # Atributos para controle de animação e estado
        self.last_hit_time = 0 # Tempo do último golpe recebido (para efeito de flash)
        self.hit_flash_duration = 150 # Duração do flash ao ser atingido (ms)
        self.hit_flash_color = (255, 255, 255, 128) # Cor do flash (branco semi-transparente)
        self.facing_right = True # Direção para a qual o inimigo está virado
        self.sprites = [self.image] if self.image else [] # Lista de frames da animação
        self.sprite_index = 0 # Índice do frame atual da animação
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Controle de tempo da animação
        self.intervalo_animacao = 200 # Intervalo entre frames da animação (ms)
        self.is_attacking = False # Estado de ataque
        self.attack_hitbox = pygame.Rect(0,0,0,0) # Hitbox para ataques (se aplicável)
        self.hit_by_player_this_attack = False # Flag para ataques do jogador
        self.contact_cooldown = 1000 # Cooldown para dano de contato (ms)
        self.last_contact_time = pygame.time.get_ticks() - self.contact_cooldown # Garante que pode dar dano no primeiro contato

    def _carregar_sprite(self, path, tamanho):
        # Determina o diretório base do script atual
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        
        # Constrói o caminho completo para o arquivo de sprite
        # Assume que 'path' é relativo a 'base_dir' ou já é um caminho que faz sentido a partir dele.
        # Por exemplo, se 'path' é "Sprites/inimigo.png", espera-se que a pasta "Sprites"
        # esteja no mesmo nível que o 'GerenciadorDeInimigos.py' ou que o 'path' seja ajustado.
        full_path = os.path.join(base_dir, path.replace("\\", "/"))

        # Verifica se o arquivo de sprite existe
        if not os.path.exists(full_path):
            print(f"DEBUG(Inimigo._carregar_sprite): Sprite não encontrado em '{full_path}'. Criando placeholder visual.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(img, (255,0,255,128), (0,0,tamanho[0],tamanho[1])) # Retângulo magenta
            return img
        try:
            # Tenta carregar a imagem e convertê-la com canal alfa
            img = pygame.image.load(full_path).convert_alpha()
            # Redimensiona a imagem para o tamanho especificado
            img = pygame.transform.scale(img, tamanho)
            return img
        except pygame.error as e:
            print(f"DEBUG(Inimigo._carregar_sprite): Pygame error ao carregar sprite '{full_path}': {e}. Criando placeholder visual.")
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(img, (255,0,255,128), (0,0,tamanho[0],tamanho[1])) # Retângulo magenta
            return img

    def receber_dano(self, dano, fonte_dano_rect=None): 
        # Reduz os pontos de vida do inimigo
        self.hp -= dano
        # Registra o tempo do último golpe para o efeito de flash
        self.last_hit_time = pygame.time.get_ticks()
        # Garante que os pontos de vida não fiquem abaixo de zero
        self.hp = max(0, self.hp)
        # print(f"DEBUG({type(self).__name__}): Recebeu {dano} de dano. HP: {self.hp}/{self.max_hp}")

    def esta_vivo(self): 
        # Verifica se o inimigo ainda tem pontos de vida
        return self.hp > 0

    def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None):
        # Move o inimigo em direção a um ponto alvo (alvo_x, alvo_y)
        if self.esta_vivo() and self.velocidade > 0:
            dx = alvo_x - self.rect.centerx # Diferença em x
            dy = alvo_y - self.rect.centery # Diferença em y
            dist = math.hypot(dx, dy) # Distância até o alvo
            
            # Fator de tempo para movimento consistente independente de framerate
            fator_tempo = 1.0 
            if dt_ms is not None and dt_ms > 0:
                # Normaliza o movimento com base em um framerate alvo (ex: 60 FPS)
                fator_tempo = (dt_ms / (1000.0 / 60.0)) 
            
            if dist > 0: # Evita divisão por zero se já estiver no alvo
                # Calcula o movimento normalizado e aplica a velocidade e fator de tempo
                mov_x = (dx / dist) * self.velocidade * fator_tempo
                mov_y = (dy / dist) * self.velocidade * fator_tempo
                self.rect.x += mov_x
                self.rect.y += mov_y
                # Atualiza a direção para a qual o inimigo está virado
                self.facing_right = dx > 0
    
    def atualizar_animacao(self):
        # Atualiza o frame da animação do inimigo
        agora = pygame.time.get_ticks()
        if self.sprites and len(self.sprites) > 1 and self.esta_vivo():
            # Avança para o próximo frame se o intervalo de animação tiver passado
            if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                self.tempo_ultimo_update_animacao = agora
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites) # Loop pela lista de sprites
        
        # Define a imagem atual do inimigo com base no frame e direção
        if self.sprites and len(self.sprites) > 0:
            idx = int(self.sprite_index % len(self.sprites))
            # Garante que o índice é válido e o sprite é uma Surface
            if idx < len(self.sprites) and self.sprites[idx] and isinstance(self.sprites[idx], pygame.Surface):
                base_image = self.sprites[idx]
                # Inverte a imagem horizontalmente se não estiver virado para a direita
                self.image = pygame.transform.flip(base_image, not self.facing_right, False)
            elif len(self.sprites) > 0 and self.sprites[0] and isinstance(self.sprites[0], pygame.Surface): 
                # Fallback para o primeiro sprite
                self.image = pygame.transform.flip(self.sprites[0], not self.facing_right, False)

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        # Método de atualização principal do inimigo
        if self.esta_vivo():
            # Move em direção ao jogador, se o jogador existir e tiver um rect
            if hasattr(player, 'rect'):
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
            
            self.atualizar_animacao() # Atualiza a animação
            
            # Lógica de dano de contato com o jogador
            current_ticks = pygame.time.get_ticks()
            if (hasattr(player, 'rect') and hasattr(player, 'vida') and 
                hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and 
                self.rect.colliderect(player.rect) and 
                (current_ticks - self.last_contact_time >= self.contact_cooldown)):
                
                if hasattr(player, 'receber_dano'):
                    player.receber_dano(self.contact_damage) # Aplica dano ao jogador
                    self.last_contact_time = current_ticks # Reseta o cooldown do dano de contato
    
    def desenhar(self, janela, camera_x, camera_y):
        # Desenha o inimigo na tela
        # Garante que self.image é uma Surface válida
        if not hasattr(self, 'image') or self.image is None or not isinstance(self.image, pygame.Surface):
            largura_img = self.largura if hasattr(self, 'largura') else 32
            altura_img = self.altura if hasattr(self, 'altura') else 32
            self.image = pygame.Surface((largura_img, altura_img), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255,0,255, 128), (0,0,self.image.get_width(),self.image.get_height()))
            # Garante que self.rect é um Rect válido
            if not hasattr(self, 'rect') or not isinstance(self.rect, pygame.Rect): 
                current_x = self.x if hasattr(self, 'x') else 0
                current_y = self.y if hasattr(self, 'y') else 0
                self.rect = self.image.get_rect(topleft=(current_x, current_y))

        # Calcula a posição de desenho na tela com base na câmera
        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y - camera_y
        janela.blit(self.image, (screen_x, screen_y)) # Desenha a imagem do inimigo

        # Efeito de flash ao ser atingido
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time < self.hit_flash_duration and hasattr(self, 'image') and self.image:
            flash_overlay = self.image.copy()
            if len(self.hit_flash_color) == 4: # RGBA
                flash_overlay.fill(self.hit_flash_color[:3] + (0,), special_flags=pygame.BLEND_RGB_ADD)
                flash_overlay.set_alpha(self.hit_flash_color[3])
            elif len(self.hit_flash_color) == 3: # RGB
                flash_overlay.fill(self.hit_flash_color + (0,), special_flags=pygame.BLEND_RGB_ADD)
                flash_overlay.set_alpha(128) # Alpha padrão para o flash
            janela.blit(flash_overlay, (screen_x, screen_y))

        # Desenha a barra de vida
        if self.hp < self.max_hp and self.hp > 0: # Só desenha se não estiver com vida cheia e estiver vivo
            bar_w = self.rect.width # Largura da barra de vida igual à largura do inimigo
            bar_h = 5 # Altura da barra de vida
            health_p = self.hp / self.max_hp # Percentual de vida
            curr_bar_w = int(bar_w * health_p) # Largura atual da parte verde da barra
            
            bar_x = screen_x # Posição x da barra
            bar_y = screen_y - bar_h - 5 # Posição y da barra (acima do inimigo)
            
            pygame.draw.rect(janela, (255,0,0), (bar_x, bar_y, bar_w, bar_h),0,2) # Fundo vermelho
            pygame.draw.rect(janela, (0,255,0), (bar_x, bar_y, curr_bar_w, bar_h),0,2) # Barra verde (vida atual)
            pygame.draw.rect(janela, (255,255,255), (bar_x, bar_y, bar_w, bar_h),1,2) # Contorno branco


class GerenciadorDeInimigos:
    def __init__(self, estacoes_obj, tela_largura: int, altura_tela: int,
                 intervalo_spawn_inicial: float = 3.0,
                 spawns_iniciais: int = 10,
                 limite_inimigos: int = 3000, 
                 fator_exponencial_spawn: float = 0.025, 
                 intervalo_spawn_minimo: float = 0.3,
                 atraso_spawn_estacao_seg: float = 0.0): 

        self.estacoes = estacoes_obj # Objeto que gerencia as estações do ano
        self.inimigos = pygame.sprite.Group() # Grupo para armazenar os inimigos ativos
        self.projeteis_inimigos = pygame.sprite.Group() # Grupo para projéteis disparados por inimigos

        # Configurações de spawn
        self.intervalo_spawn_inicial = intervalo_spawn_inicial # Intervalo inicial entre spawns (s)
        self.spawns_iniciais = spawns_iniciais # Número de inimigos a spawnar no início de uma estação
        self.limite_inimigos = limite_inimigos # Limite máximo de inimigos na tela

        self.tempo_inicio_estacao_para_spawn = time.time() # Registra o tempo de início da estação atual

        self.fator_exponencial_spawn = fator_exponencial_spawn # Fator para diminuir o intervalo de spawn exponencialmente
        self.intervalo_spawn_minimo = intervalo_spawn_minimo # Intervalo mínimo de spawn (s)

        self.tela_largura = tela_largura # Largura da tela do jogo
        self.altura_tela = altura_tela   # Altura da tela do jogo

        # Fila e thread para controle de spawn assíncrono
        self.spawn_request_queue = queue.Queue() # Fila para requisições de spawn
        self.stop_spawn_thread_event = threading.Event() # Evento para sinalizar parada da thread
        self.ultimo_spawn_controlado_pelo_thread = time.time() # Tempo do último spawn realizado pela thread

        # Atraso de spawn no início de uma estação
        self.atraso_configurado_estacao = atraso_spawn_estacao_seg # Duração do atraso (s)
        self.tempo_fim_atraso_spawn_continuo = 0 # Tempo em que o atraso termina
        self.atraso_spawn_continuo_ativo = False # Flag se o atraso está ativo

        # Inicializa e inicia a thread de controle de spawn
        self.spawn_controller_thread = threading.Thread(
            target=self._spawn_controller_task,
            daemon=True # Permite que o programa principal termine mesmo se a thread estiver rodando
        )
        self.spawn_controller_thread.start()
        print("DEBUG(GerenciadorDeInimigos): Gerenciador de Inimigos e Thread de Spawn inicializados.")

    def resetar_temporizador_spawn_estacao(self):
        # Reseta os temporizadores e a fila de spawn para uma nova estação
        print(f"DEBUG(GerenciadorDeInimigos): Resetando temporizador de spawn para nova estação.")
        agora = time.time()
        self.tempo_inicio_estacao_para_spawn = agora 
        
        # Ativa o atraso de spawn se configurado
        if self.atraso_configurado_estacao > 0:
            self.tempo_fim_atraso_spawn_continuo = agora + self.atraso_configurado_estacao
            self.atraso_spawn_continuo_ativo = True
            print(f"DEBUG(GerenciadorDeInimigos): Atraso de spawn contínuo de {self.atraso_configurado_estacao}s ATIVADO até {time.ctime(self.tempo_fim_atraso_spawn_continuo)}.")
        else:
            self.atraso_spawn_continuo_ativo = False

        self.ultimo_spawn_controlado_pelo_thread = agora 

        # Limpa a fila de requisições de spawn pendentes
        while not self.spawn_request_queue.empty():
            try:
                self.spawn_request_queue.get_nowait() 
                self.spawn_request_queue.task_done() 
            except queue.Empty:
                break 
        print("DEBUG(GerenciadorDeInimigos): Fila de pedidos de spawn limpa para nova estação.")


    def _spawn_controller_task(self):
        # Tarefa executada pela thread de controle de spawn
        while not self.stop_spawn_thread_event.is_set(): 
            agora = time.time()

            # Lida com o atraso de spawn no início da estação
            if self.atraso_spawn_continuo_ativo:
                if agora >= self.tempo_fim_atraso_spawn_continuo:
                    # Atraso concluído, permite spawn contínuo
                    self.atraso_spawn_continuo_ativo = False
                    self.tempo_inicio_estacao_para_spawn = agora # Reseta o tempo base para cálculo exponencial
                    self.ultimo_spawn_controlado_pelo_thread = agora 
                    print(f"DEBUG(GerenciadorDeInimigos): Atraso de spawn da estação concluído. Spawn contínuo habilitado.")
                else:
                    # Ainda em atraso, espera um pouco
                    tempo_restante_atraso = self.tempo_fim_atraso_spawn_continuo - agora
                    self.stop_spawn_thread_event.wait(timeout=min(0.1, tempo_restante_atraso if tempo_restante_atraso > 0 else 0.1)) 
                    continue # Volta ao início do loop da thread
            
            # Calcula o intervalo de spawn atual com base no tempo decorrido na estação
            tempo_decorrido_na_estacao_para_calculo_exponencial = agora - self.tempo_inicio_estacao_para_spawn
            
            intervalo_atual = max(
                self.intervalo_spawn_minimo, 
                self.intervalo_spawn_inicial * math.exp(-self.fator_exponencial_spawn * tempo_decorrido_na_estacao_para_calculo_exponencial)
            )
            
            # Verifica se é hora de solicitar um novo spawn
            if agora - self.ultimo_spawn_controlado_pelo_thread >= intervalo_atual:
                if len(self.inimigos) < self.limite_inimigos: # Verifica o limite de inimigos
                    if self.estacoes and hasattr(self.estacoes, 'nome_estacao'):
                        try:
                            estacao_atual_nome = self.estacoes.nome_estacao()
                            if estacao_atual_nome: # Garante que o nome da estação é válido
                                # Adiciona uma requisição de spawn à fila
                                self.spawn_request_queue.put({"estacao": estacao_atual_nome, "timestamp": agora})
                                self.ultimo_spawn_controlado_pelo_thread = agora 
                            # else:
                                # print("DEBUG(GerenciadorDeInimigos_Thread): Nome da estação vazio, não solicitando spawn.")
                        except Exception as e:
                            print(f"DEBUG(GerenciadorDeInimigos_Thread): Erro ao obter nome da estação: {e}")
            
            self.stop_spawn_thread_event.wait(timeout=0.05) # Pequena pausa para não sobrecarregar a CPU
        print("DEBUG(GerenciadorDeInimigos): Thread de controle de spawn finalizado.")

    def process_spawn_requests(self, jogador, dt_ms=None): 
        # Processa as requisições de spawn da fila (chamado no loop principal do jogo)
        try:
            while not self.spawn_request_queue.empty(): 
                if len(self.inimigos) >= self.limite_inimigos:
                    # Limite atingido, descarta a requisição para evitar acúmulo na fila
                    try:
                        self.spawn_request_queue.get_nowait()
                        self.spawn_request_queue.task_done()
                    except queue.Empty: # Fila pode ter esvaziado entre o empty() e o get_nowait()
                        break
                    continue 

                request_data = self.spawn_request_queue.get_nowait() 
                estacao_nome = request_data.get("estacao")

                # Garante que o jogador e seu rect existem antes de tentar spawnar
                if jogador and hasattr(jogador, 'rect') and estacao_nome: 
                    self._spawn_inimigo_especifico_da_estacao(estacao_nome, jogador, dt_ms=dt_ms)

                self.spawn_request_queue.task_done() # Indica que a requisição foi processada
        except queue.Empty:
            pass # Normal se a fila estiver vazia
        except Exception as e:
            print(f"DEBUG(GerenciadorDeInimigos): Erro ao processar fila de spawn: {e}")


    def _spawn_inimigo_especifico_da_estacao(self, estacao_nome, jogador, dt_ms=None): 
        # Lógica para escolher e spawnar um inimigo com base na estação atual
        est_nome_lower = estacao_nome.lower()
        tipos_disponiveis = [] # Lista de tipos de inimigos que podem spawnar

        # Define os tipos de inimigos disponíveis para cada estação
        # Verifica se a variável da classe do inimigo existe globalmente E não é None
        if est_nome_lower == "inverno":
            if 'Fantasma' in globals() and Fantasma: tipos_disponiveis.append('fantasma')
            if 'BonecoDeNeve' in globals() and BonecoDeNeve: tipos_disponiveis.append('bonecodeneve')
            if 'Lobo' in globals() and Lobo: tipos_disponiveis.append('lobo')
            if 'Golem_Neve' in globals() and Golem_Neve: tipos_disponiveis.append('golem_neve') 
        elif est_nome_lower == "primavera":
            if 'Planta_Carnivora' in globals() and Planta_Carnivora: tipos_disponiveis.append('planta_carnivora')
            if 'Mae_Natureza' in globals() and Mae_Natureza: tipos_disponiveis.append('maenatureza')
            if 'Espirito_Das_Flores' in globals() and Espirito_Das_Flores: tipos_disponiveis.append('espiritodasflores')
            if 'Vampiro' in globals() and Vampiro: tipos_disponiveis.append('vampiro') 
        elif est_nome_lower == "outono":
            if 'Espantalho' in globals() and Espantalho: tipos_disponiveis.append('espantalho')
            if 'Troll' in globals() and Troll: tipos_disponiveis.append('troll') 
            if 'Goblin' in globals() and Goblin: tipos_disponiveis.append('goblin') 
        elif est_nome_lower == "verão" or est_nome_lower == "verao": 
            if 'Fenix' in globals() and Fenix: tipos_disponiveis.append('fenix')
            if 'Urso' in globals() and Urso: tipos_disponiveis.append('urso')
            if 'Demonio' in globals() and Demonio: tipos_disponiveis.append('demonio') 

        if not tipos_disponiveis: 
            # print(f"DEBUG(GerenciadorDeInimigos): Nenhum tipo de inimigo disponível para spawn na estação '{estacao_nome}'.")
            return

        tipo_escolhido = random.choice(tipos_disponiveis) # Escolhe aleatoriamente um tipo de inimigo
        
        # Lógica para determinar a posição de spawn (fora da tela)
        x, y = 0, 0
        spawn_margin = 50 # Margem para spawnar fora da visão do jogador

        if not (jogador and hasattr(jogador, 'rect')):
            print("DEBUG(GerenciadorDeInimigos): Jogador ou jogador.rect não disponível para _spawn_inimigo_especifico_da_estacao.")
            return

        # Calcula as bordas da tela no sistema de coordenadas do mundo
        screen_left_world = jogador.rect.centerx - (self.tela_largura / 2)
        screen_right_world = jogador.rect.centerx + (self.tela_largura / 2)
        screen_top_world = jogador.rect.centery - (self.altura_tela / 2)
        screen_bottom_world = jogador.rect.centery + (self.altura_tela / 2)

        edge = random.choice(["top", "bottom", "left", "right"]) # Escolhe uma borda aleatória

        # Define as coordenadas x, y com base na borda escolhida
        if edge == "top":
            x = random.uniform(screen_left_world - spawn_margin, screen_right_world + spawn_margin) # Varia um pouco mais para evitar concentração
            y = screen_top_world - spawn_margin
        elif edge == "bottom":
            x = random.uniform(screen_left_world - spawn_margin, screen_right_world + spawn_margin)
            y = screen_bottom_world + spawn_margin
        elif edge == "left":
            x = screen_left_world - spawn_margin
            y = random.uniform(screen_top_world - spawn_margin, screen_bottom_world + spawn_margin)
        elif edge == "right":
            x = screen_right_world + spawn_margin
            y = random.uniform(screen_top_world - spawn_margin, screen_bottom_world + spawn_margin)
        
        self.criar_inimigo_aleatorio(tipo_escolhido, x, y, velocidade=1.0, dt_ms_para_init=dt_ms)


    def adicionar_inimigo(self, inimigo):
        # Adiciona um inimigo ao grupo, se for um sprite válido
        if inimigo and isinstance(inimigo, pygame.sprite.Sprite):
            self.inimigos.add(inimigo)
        # else:
            # print(f"DEBUG(GerenciadorDeInimigos): Tentativa de adicionar objeto inválido ({type(inimigo)}) ao grupo de inimigos.")

    def remover_inimigo(self, inimigo):
        # Remove um inimigo do grupo
        if inimigo in self.inimigos: 
            self.inimigos.remove(inimigo) 
        if hasattr(inimigo, 'kill'): # Chama o método kill() do sprite, se existir
            inimigo.kill() # kill() também remove de todos os grupos aos quais o sprite pertence


    def criar_inimigo_aleatorio(self, tipo_inimigo_str, x, y, velocidade=1.0, dt_ms_para_init=None): 
        # Cria uma instância de um inimigo específico
        novo_inimigo = None
        mapa_tipos = {} # Mapa de strings para classes de inimigos

        # Nomes das classes e suas strings correspondentes para o mapa
        nomes_classes_map = {
            'fantasma': 'Fantasma', 'bonecodeneve': 'BonecoDeNeve',
            'planta_carnivora': 'Planta_Carnivora', 'espantalho': 'Espantalho',
            'fenix': 'Fenix', 'maenatureza': 'Mae_Natureza',
            'espiritodasflores': 'Espirito_Das_Flores', 'lobo': 'Lobo', 'urso': 'Urso',
            'troll': 'Troll', 'golem_neve': 'Golem_Neve', 'goblin': 'Goblin',
            'vampiro': 'Vampiro', 'demonio': 'Demonio'
        }

        # Preenche o mapa_tipos apenas com classes que foram importadas com sucesso
        for str_mapa, nome_classe_str in nomes_classes_map.items():
            if nome_classe_str in globals() and globals()[nome_classe_str] is not None:
                mapa_tipos[str_mapa] = globals()[nome_classe_str]
        
        ClasseInimigo = mapa_tipos.get(tipo_inimigo_str.lower()) # Obtém a classe do mapa

        if ClasseInimigo is not None:
            try:
                # Tenta instanciar o inimigo.
                # As classes de inimigos específicas (Fantasma, BonecoDeNeve, etc.)
                # DEVEM ser capazes de serem instanciadas com, no mínimo, (x, y).
                # Idealmente, elas devem herdar da classe Inimigo definida neste arquivo
                # e chamar super().__init__(...) com todos os parâmetros necessários,
                # ou ter seus próprios construtores que aceitem pelo menos (x,y) e
                # configurem os atributos esperados pela classe base Inimigo.
                
                # Tentativa de construtor mais comum para inimigos que podem ter velocidade variável.
                # Se as classes específicas não usam 'velocidade' no construtor, isso pode dar TypeError.
                novo_inimigo = ClasseInimigo(x=x, y=y, velocidade=velocidade)
                
            except TypeError as e_construtor_kwargs:
                 try:
                    # Fallback para um construtor mais simples (x, y)
                    novo_inimigo = ClasseInimigo(x, y)
                 except TypeError as e_construtor_simples:
                    print(f"DEBUG(GerenciadorDeInimigos): Erro de TypeError ao criar {tipo_inimigo_str} (classe {ClasseInimigo.__name__}). "
                          f"Tentativa com (x,y,velocidade): {e_construtor_kwargs}. "
                          f"Tentativa com (x,y): {e_construtor_simples}. "
                          f"Verifique os parâmetros do construtor de {ClasseInimigo.__name__}. "
                          f"A classe Inimigo base espera: (x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path). "
                          f"As classes específicas devem chamar super() adequadamente ou ter construtores compatíveis.")
                 except Exception as e_geral_xy:
                    print(f"DEBUG(GerenciadorDeInimigos): Erro geral (não TypeError) ao criar {tipo_inimigo_str} com (x,y): {e_geral_xy}")
            except Exception as e:
                print(f"DEBUG(GerenciadorDeInimigos): Erro desconhecido ao criar {tipo_inimigo_str} (classe {ClasseInimigo.__name__}): {e}")
        else:
            print(f"DEBUG(GerenciadorDeInimigos): Classe para tipo '{tipo_inimigo_str}' não encontrada no mapa_tipos (valor é None).")

        if novo_inimigo:
            self.adicionar_inimigo(novo_inimigo)
        # else:
            # print(f"DEBUG(GerenciadorDeInimigos): Falha ao criar instância de '{tipo_inimigo_str}'.")
        return novo_inimigo


    def spawn_inimigos_iniciais(self, jogador, dt_ms=None): 
        # Spawna um número inicial de inimigos no início de uma estação
        if self.estacoes is None or not hasattr(self.estacoes, 'nome_estacao'):
            print("DEBUG(GerenciadorDeInimigos): Aviso: Objeto Estacoes não disponível para spawn inicial.")
            return
        
        try:
            est_nome = self.estacoes.nome_estacao()
            if not est_nome: # Verifica se o nome da estação é válido
                print("DEBUG(GerenciadorDeInimigos): Aviso: nome_estacao() retornou vazio/None para spawn inicial.")
                return
        except Exception as e:
            print(f"DEBUG(GerenciadorDeInimigos): Erro ao obter nome da estação para spawn inicial: {e}")
            return

        print(f"DEBUG(GerenciadorDeInimigos): Realizando spawn inicial de {self.spawns_iniciais} inimigos para estação '{est_nome}'.")
        for _ in range(self.spawns_iniciais):
            if len(self.inimigos) < self.limite_inimigos:
                self._spawn_inimigo_especifico_da_estacao(est_nome, jogador, dt_ms=dt_ms)
            else:
                print("DEBUG(GerenciadorDeInimigos): Limite de inimigos atingido durante spawn inicial.")
                break


    def update_inimigos(self, jogador, dt_ms=None):
        # Atualiza todos os inimigos ativos
        inimigos_para_remover = []
        for inimigo_obj in list(self.inimigos): # Itera sobre uma cópia da lista de inimigos
            if hasattr(inimigo_obj, 'esta_vivo') and inimigo_obj.esta_vivo():
                if hasattr(inimigo_obj, 'update'):
                    try:
                        # Tenta chamar update com a assinatura mais completa
                        inimigo_obj.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela, dt_ms)
                    except TypeError: # Se falhar, tenta assinaturas mais simples (fallback)
                        try:
                            inimigo_obj.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela)
                        except TypeError:
                            try:
                                inimigo_obj.update(jogador, self.projeteis_inimigos)
                            except TypeError:
                                try:
                                    inimigo_obj.update(jogador) 
                                except Exception as e_final:
                                    # Para evitar spam, pode-se logar o erro uma vez por tipo de inimigo
                                    # if not hasattr(inimigo_obj, '_update_error_logged_'):
                                    # print(f"DEBUG(GerenciadorInimigos): Erro ao chamar update de {type(inimigo_obj).__name__}: {e_final}. Args não correspondem.")
                                    # inimigo_obj._update_error_logged_ = True 
                                    pass 
            elif hasattr(inimigo_obj, 'esta_vivo') and not inimigo_obj.esta_vivo(): 
                # Se o inimigo não está mais vivo, marca para remoção
                inimigos_para_remover.append(inimigo_obj)
            # else: # Caso onde o inimigo não tem 'esta_vivo' ou o atributo é inválido
                # print(f"DEBUG(GerenciadorDeInimigos): Inimigo {type(inimigo_obj).__name__} sem método 'esta_vivo' ou estado inesperado.")

        # Remove os inimigos marcados e concede XP
        for inimigo_removido in inimigos_para_remover:
            if hasattr(jogador, 'ganhar_xp') and hasattr(inimigo_removido, 'xp_value'):
                jogador.ganhar_xp(inimigo_removido.xp_value) # Concede XP ao jogador
            self.remover_inimigo(inimigo_removido) # Remove o inimigo

    def update_projeteis_inimigos(self, jogador, dt_ms=None):
        # Atualiza todos os projéteis disparados por inimigos
        for projetil in list(self.projeteis_inimigos): 
            if hasattr(projetil, 'update'):
                try: # Assinatura completa
                    projetil.update(jogador, self.tela_largura, self.altura_tela, dt_ms)
                except TypeError: # Fallbacks
                    try:
                        projetil.update(jogador, self.tela_largura, self.altura_tela)
                    except TypeError: 
                        try:
                            projetil.update(jogador)
                        except Exception as e_final_proj:
                            # print(f"DEBUG(GerenciadorInimigos): Erro ao chamar update de projétil {type(projetil).__name__}: {e_final_proj}.")
                            pass

            deve_remover = False
            # Verifica se o projétil deve ser removido (ex: saiu da tela, colidiu, tempo de vida expirou)
            # O próprio projétil deve ter uma lógica para se marcar como "não vivo"
            if hasattr(projetil, 'alive'): # Sprites do Pygame têm o método alive()
                if callable(projetil.alive) and not projetil.alive(): 
                    deve_remover = True
                elif isinstance(projetil.alive, bool) and not projetil.alive: # Se 'alive' for um atributo booleano
                    deve_remover = True
            elif not hasattr(projetil, 'rect'): # Se não tem rect, provavelmente não é um sprite válido
                deve_remover = True

            if deve_remover:
                if projetil in self.projeteis_inimigos: # Garante que ainda está no grupo
                    self.projeteis_inimigos.remove(projetil)
                    if hasattr(projetil, 'kill'):
                        projetil.kill() # Chama kill() para remover de todos os grupos


    def desenhar_inimigos(self, janela, camera_x: int, camera_y: int):
        # Desenha todos os inimigos ativos
        for inimigo in self.inimigos:
            if hasattr(inimigo, 'desenhar'):
                inimigo.desenhar(janela, camera_x, camera_y)
            # Fallback se o método 'desenhar' não existir, mas for um sprite padrão
            # elif isinstance(inimigo, pygame.sprite.Sprite) and hasattr(inimigo, 'image') and hasattr(inimigo, 'rect'):
                # if inimigo.image and inimigo.rect: # Garante que image e rect são válidos
                    # janela.blit(inimigo.image, (inimigo.rect.x - camera_x, inimigo.rect.y - camera_y))

    def desenhar_projeteis_inimigos(self, surface, camera_x, camera_y):
        # Desenha todos os projéteis ativos
        for projetil in self.projeteis_inimigos:
            if hasattr(projetil, 'desenhar'):
                projetil.desenhar(surface, camera_x, camera_y)
            # Fallback
            # elif isinstance(projetil, pygame.sprite.Sprite) and hasattr(projetil, 'image') and hasattr(projetil, 'rect'):
                # if projetil.image and projetil.rect:
                    # surface.blit(projetil.image, (projetil.rect.x - camera_x, projetil.rect.y - camera_y))

    def get_inimigos_vivos(self):
        # Retorna o grupo de inimigos (pygame.sprite.Group já é uma coleção de sprites "vivos")
        return self.inimigos

    def limpar_inimigos(self):
        # Remove todos os inimigos e projéteis
        # Usar kill() é preferível pois remove dos grupos e pode limpar outros recursos
        for inimigo_obj in list(self.inimigos): 
            if hasattr(inimigo_obj, 'kill'):
                inimigo_obj.kill()
            elif inimigo_obj in self.inimigos: # Fallback se não tiver kill
                 self.inimigos.remove(inimigo_obj)

        for projetil in list(self.projeteis_inimigos):
            if hasattr(projetil, 'kill'):
                projetil.kill()
            elif projetil in self.projeteis_inimigos:
                self.projeteis_inimigos.remove(projetil)
        
        # Alternativamente, se todos os sprites implementam kill() corretamente:
        # self.inimigos.empty()
        # self.projeteis_inimigos.empty()
        print("DEBUG(GerenciadorDeInimigos): Todos os inimigos e projéteis limpos.")

    def stop_threads(self):
        # Para a thread de controle de spawn de forma segura
        print("DEBUG(GerenciadorDeInimigos): Sinalizando para parar thread de spawn...")
        self.stop_spawn_thread_event.set() # Sinaliza para a thread terminar
        if self.spawn_controller_thread and self.spawn_controller_thread.is_alive():
            self.spawn_controller_thread.join(timeout=1.0) # Espera a thread terminar (com timeout)
            if self.spawn_controller_thread.is_alive():
                print("DEBUG(GerenciadorDeInimigos): AVISO: Thread de spawn não terminou a tempo.")
            else:
                print("DEBUG(GerenciadorDeInimigos): Thread de spawn finalizado com sucesso.")
        else:
            print("DEBUG(GerenciadorDeInimigos): Thread de spawn não estava ativa ou não existe.")

