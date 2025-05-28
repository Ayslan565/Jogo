# GerenciadorDeInimigos.py
import pygame
import random
import time
import math
import threading
import queue # Para fila thread-safe

# Importa a classe base Inimigo
try:
    from Inimigos import Inimigo
    print("DEBUG(GerenciadorDeInimigos): Classe base Inimigo importada com sucesso.")
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): ERRO: Módulo 'Inimigos.py' ou classe 'Inimigo' NÃO encontrado. Usando placeholder.")
    class Inimigo(pygame.sprite.Sprite): # Placeholder
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.x = x; self.y = y; self.largura = largura; self.altura = altura
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 255), (0, 0, largura, altura)) # Cor magenta para placeholder
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
            self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128); self.facing_right = True
            self.sprites = [self.image]; self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.intervalo_animacao = 200; self.is_attacking = False
            self.attack_hitbox = pygame.Rect(0,0,0,0); self.hit_by_player_this_attack = False
            self.contact_cooldown = 1000; self.last_contact_time = pygame.time.get_ticks()
        def _carregar_sprite(self, path, tamanho): return pygame.Surface(tamanho) # Placeholder simples
        def receber_dano(self, dano, fonte_dano_rect=None): self.hp -= dano; self.last_hit_time = pygame.time.get_ticks(); self.hp = max(0, self.hp)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None): pass # Placeholder
        def atualizar_animacao(self): pass # Placeholder
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): pass # Placeholder
        def desenhar(self, janela, camera_x, camera_y): # Placeholder
            if hasattr(self, 'image') and self.image:
                 janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

# Importa as classes de inimigos específicas
try: from Fantasma import Fantasma
except ImportError: Fantasma = None; print("DEBUG(GerenciadorDeInimigos): Fantasma não encontrado.")
try: from BonecoDeNeve import BonecoDeNeve
except ImportError: BonecoDeNeve = None; print("DEBUG(GerenciadorDeInimigos): BonecoDeNeve não encontrado.")
try: from Planta_Carnivora import Planta_Carnivora
except ImportError: Planta_Carnivora = None; print("DEBUG(GerenciadorDeInimigos): Planta_Carnivora não encontrada.")
try: from Espantalho import Espantalho
except ImportError: Espantalho = None; print("DEBUG(GerenciadorDeInimigos): Espantalho não encontrado.")
try: from Fenix import Fenix
except ImportError: Fenix = None; print("DEBUG(GerenciadorDeInimigos): Fenix não encontrado.")
try: from Mae_Natureza import Mae_Natureza
except ImportError: Mae_Natureza = None; print("DEBUG(GerenciadorDeInimigos): Mae_Natureza não encontrada.")
try: from Espirito_Das_Flores import Espirito_Das_Flores
except ImportError: Espirito_Das_Flores = None; print("DEBUG(GerenciadorDeInimigos): Espirito_Das_Flores não encontrado.")
try: from Lobo import Lobo
except ImportError: Lobo = None; print("DEBUG(GerenciadorDeInimigos): Lobo não encontrado.")
try: from Urso import Urso
except ImportError: Urso = None; print("DEBUG(GerenciadorDeInimigos): Urso não encontrado.")
try: from Projetil_BolaNeve import ProjetilNeve # Usado por BonecoDeNeve, por exemplo
except ImportError: ProjetilNeve = None; print("DEBUG(GerenciadorDeInimigos): ProjetilNeve não encontrado.")

# NOVOS INIMIGOS
try: from Troll import Troll
except ImportError: Troll = None; print("DEBUG(GerenciadorDeInimigos): Troll não encontrado.")
try: from Golem_Neve import Golem_Neve
except ImportError: Golem_Neve = None; print("DEBUG(GerenciadorDeInimigos): Golem_Neve não encontrado.")
try: from Goblin import Goblin
except ImportError: Goblin = None; print("DEBUG(GerenciadorDeInimigos): Goblin não encontrado.")
try: from Vampiro import Vampiro
except ImportError: Vampiro = None; print("DEBUG(GerenciadorDeInimigos): Vampiro não encontrado.")
try: from Demonio import Demonio
except ImportError: Demonio = None; print("DEBUG(GerenciadorDeInimigos): Demonio não encontrado.")


class GerenciadorDeInimigos:
    def __init__(self, estacoes_obj, tela_largura: int, altura_tela: int,
                 intervalo_spawn_inicial: float = 3.0,
                 spawns_iniciais: int = 10,
                 limite_inimigos: int = 3000, # Limite global de inimigos em jogo
                 fator_exponencial_spawn: float = 0.025, # Quão rápido o spawn acelera
                 intervalo_spawn_minimo: float = 0.3): # Intervalo mínimo entre spawns no pico

        self.estacoes = estacoes_obj
        self.inimigos = pygame.sprite.Group() # Grupo para todos os inimigos ativos
        self.projeteis_inimigos = pygame.sprite.Group() # Grupo para projéteis disparados por inimigos

        self.intervalo_spawn_inicial = intervalo_spawn_inicial
        self.spawns_iniciais = spawns_iniciais
        self.limite_inimigos = limite_inimigos

        self.tempo_inicio_estacao_para_spawn = time.time() # Usado para calcular a aceleração do spawn

        self.fator_exponencial_spawn = fator_exponencial_spawn
        self.intervalo_spawn_minimo = intervalo_spawn_minimo

        self.tela_largura = tela_largura # Para referência de limites, se necessário
        self.altura_tela = altura_tela

        # Sistema de Fila para Spawns controlados por Thread
        self.spawn_request_queue = queue.Queue() # Fila para pedidos de spawn
        self.stop_spawn_thread_event = threading.Event() # Evento para parar a thread de forma limpa
        self.ultimo_spawn_controlado_pelo_thread = time.time() # Controla o tempo do último spawn pela thread

        # Thread para controlar a taxa de spawn dinamicamente
        self.spawn_controller_thread = threading.Thread(
            target=self._spawn_controller_task,
            daemon=True # Permite que a thread principal saia mesmo se esta thread estiver rodando
        )
        self.spawn_controller_thread.start()
        print("DEBUG(GerenciadorDeInimigos): Gerenciador de Inimigos e Thread de Spawn inicializados.")

    def resetar_temporizador_spawn_estacao(self):
        """Reseta os temporizadores e limpa a fila de spawn ao mudar de estação."""
        print(f"DEBUG(GerenciadorDeInimigos): Resetando temporizador de spawn para nova estação.")
        self.tempo_inicio_estacao_para_spawn = time.time()
        self.ultimo_spawn_controlado_pelo_thread = time.time()

        # Limpa quaisquer pedidos de spawn pendentes da estação anterior
        while not self.spawn_request_queue.empty():
            try:
                self.spawn_request_queue.get_nowait() # Remove da fila sem bloquear
                self.spawn_request_queue.task_done() # Sinaliza que a tarefa foi concluída
            except queue.Empty:
                break # Sai se a fila estiver vazia
        print("DEBUG(GerenciadorDeInimigos): Fila de pedidos de spawn limpa para nova estação.")


    def _spawn_controller_task(self):
        """Tarefa executada pela thread para determinar quando solicitar um novo spawn."""
        while not self.stop_spawn_thread_event.is_set(): # Continua enquanto o evento de parada não for acionado
            agora = time.time()
            tempo_decorrido_na_estacao = agora - self.tempo_inicio_estacao_para_spawn

            # Calcula o intervalo de spawn atual, diminuindo exponencialmente com o tempo
            intervalo_atual = max(
                self.intervalo_spawn_minimo, # Não permite que o intervalo seja menor que o mínimo
                self.intervalo_spawn_inicial * math.exp(-self.fator_exponencial_spawn * tempo_decorrido_na_estacao)
            )

            # Se o tempo desde o último spawn pela thread for maior ou igual ao intervalo calculado
            if agora - self.ultimo_spawn_controlado_pelo_thread >= intervalo_atual:
                if self.estacoes and hasattr(self.estacoes, 'nome_estacao'):
                    estacao_atual_nome = self.estacoes.nome_estacao()
                    # Coloca um pedido de spawn na fila com a estação atual
                    self.spawn_request_queue.put({"estacao": estacao_atual_nome, "timestamp": agora})
                    self.ultimo_spawn_controlado_pelo_thread = agora # Atualiza o tempo do último spawn

            # Espera um curto período ou até que o evento de parada seja acionado
            # Isso evita que a thread consuma 100% da CPU em um loop apertado
            self.stop_spawn_thread_event.wait(timeout=0.05) # Verifica a cada 50ms
        print("DEBUG(GerenciadorDeInimigos): Thread de controle de spawn finalizado.")

    def process_spawn_requests(self, jogador):
        """Processa os pedidos de spawn da fila no loop principal do jogo."""
        try:
            while not self.spawn_request_queue.empty(): # Enquanto houver pedidos na fila
                if len(self.inimigos) >= self.limite_inimigos:
                    # Se o limite de inimigos for atingido, descarta o pedido para evitar sobrecarga
                    self.spawn_request_queue.get_nowait()
                    self.spawn_request_queue.task_done()
                    continue # Pula para o próximo pedido

                request_data = self.spawn_request_queue.get_nowait() # Pega o pedido da fila
                estacao_nome = request_data.get("estacao")

                if jogador and estacao_nome: # Se o jogador e a estação são válidos
                    self._spawn_inimigo_especifico_da_estacao(estacao_nome, jogador)

                self.spawn_request_queue.task_done() # Sinaliza que o pedido foi processado
        except queue.Empty:
            pass # Normal se a fila estiver vazia
        except Exception as e:
            print(f"DEBUG(GerenciadorDeInimigos): Erro ao processar fila de spawn: {e}")


    def _spawn_inimigo_especifico_da_estacao(self, estacao_nome, jogador):
        """Cria um inimigo específico com base na estação atual."""
        est_nome_lower = estacao_nome.lower()
        tipos_disponiveis = [] # Lista de tipos de inimigos que podem spawnar nesta estação

        # Define os inimigos para cada estação
        if est_nome_lower == "inverno":
            if Fantasma: tipos_disponiveis.append('fantasma')
            if BonecoDeNeve: tipos_disponiveis.append('bonecodeneve')
            if Lobo: tipos_disponiveis.append('lobo')
            if Golem_Neve: tipos_disponiveis.append('golem_neve') # NOVO
        elif est_nome_lower == "primavera":
            if Planta_Carnivora: tipos_disponiveis.append('planta_carnivora')
            if Mae_Natureza: tipos_disponiveis.append('maenatureza')
            if Espirito_Das_Flores: tipos_disponiveis.append('espiritodasflores')
            if Vampiro: tipos_disponiveis.append('vampiro') # NOVO
        elif est_nome_lower == "outono":
            if Espantalho: tipos_disponiveis.append('espantalho')
            if Troll: tipos_disponiveis.append('troll') # NOVO
            if Goblin: tipos_disponiveis.append('goblin') # NOVO
        elif est_nome_lower == "verão" or est_nome_lower == "verao": # Considera com e sem acento
            if Fenix: tipos_disponiveis.append('fenix')
            if Urso: tipos_disponiveis.append('urso')
            if Demonio: tipos_disponiveis.append('demonio') # NOVO

        if not tipos_disponiveis: # Se nenhum inimigo estiver disponível para a estação
            # print(f"DEBUG(GerenciadorDeInimigos): Nenhum tipo de inimigo disponível para spawn na estação: {estacao_nome}")
            return

        tipo_escolhido = random.choice(tipos_disponiveis) # Escolhe aleatoriamente um tipo da lista

        # Lógica para determinar a posição de spawn (fora da tela visível)
        # Define uma área de spawn ao redor do jogador, mas fora da visão imediata
        # A distância exata pode precisar de ajuste com base no tamanho da tela/câmera
        min_dist_spawn = int(min(self.tela_largura, self.altura_tela) * 0.6) # Mínimo 60% da menor dimensão da tela
        max_dist_spawn = int(min(self.tela_largura, self.altura_tela) * 1.0) # Máximo 100% da menor dimensão da tela

        # Tenta encontrar uma posição de spawn válida
        # Esta lógica assume que as coordenadas do jogador (jogador.rect.centerx/y) são coordenadas do MUNDO.
        # E que x, y calculados também serão coordenadas do MUNDO.
        # A câmera cuidará de transladar as coordenadas do mundo para a tela.
        spawn_pos_ok = False
        tentativas = 0
        max_tentativas = 10 # Evita loop infinito se for difícil encontrar posição
        x, y = 0, 0

        while not spawn_pos_ok and tentativas < max_tentativas:
            angle = random.uniform(0, 2 * math.pi) # Ângulo aleatório
            distance = random.randint(min_dist_spawn, max_dist_spawn) # Distância aleatória
            
            # Calcula a posição de spawn relativa ao jogador
            x = jogador.rect.centerx + distance * math.cos(angle)
            y = jogador.rect.centery + distance * math.sin(angle)

            # Validação simples: apenas garante que não spawne exatamente no jogador
            # Uma validação mais complexa poderia verificar se está dentro dos limites do mapa, etc.
            if math.hypot(x - jogador.rect.centerx, y - jogador.rect.centery) > 50: # Não muito perto
                spawn_pos_ok = True
            tentativas += 1
        
        if not spawn_pos_ok: # Fallback se não encontrou posição ideal
            angle = random.uniform(0, 2 * math.pi)
            distance = (min_dist_spawn + max_dist_spawn) / 2 # Usa uma distância média
            x = jogador.rect.centerx + distance * math.cos(angle)
            y = jogador.rect.centery + distance * math.sin(angle)
            # print(f"DEBUG(GerenciadorDeInimigos): Fallback de posição de spawn para {tipo_escolhido} em ({x:.0f},{y:.0f})")


        self.criar_inimigo_aleatorio(tipo_escolhido, x, y)


    def adicionar_inimigo(self, inimigo):
        """Adiciona um inimigo ao grupo de inimigos."""
        if inimigo:
            self.inimigos.add(inimigo)

    def remover_inimigo(self, inimigo):
        """Remove um inimigo e garante que seu método kill() seja chamado."""
        self.inimigos.remove(inimigo) # Remove do grupo principal
        if hasattr(inimigo, 'kill'): # Chama o método kill do sprite, se existir
            inimigo.kill() # Isso o removerá de todos os grupos aos quais pertence


    def criar_inimigo_aleatorio(self, tipo_inimigo_str, x, y, velocidade=1.0):
        """Cria uma instância de um inimigo com base no tipo fornecido."""
        novo_inimigo = None
        mapa_tipos = {
            'fantasma': Fantasma, 'bonecodeneve': BonecoDeNeve,
            'planta_carnivora': Planta_Carnivora, 'espantalho': Espantalho,
            'fenix': Fenix, 'maenatureza': Mae_Natureza,
            'espiritodasflores': Espirito_Das_Flores, 'lobo': Lobo, 'urso': Urso,
            'troll': Troll, # NOVO
            'golem_neve': Golem_Neve, # NOVO
            'goblin': Goblin, # NOVO
            'vampiro': Vampiro, # NOVO
            'demonio': Demonio # NOVO
        }

        ClasseInimigo = mapa_tipos.get(tipo_inimigo_str.lower())

        if ClasseInimigo is not None:
            try:
                # Tenta instanciar. Assume que os construtores aceitam (x, y, velocidade=...)
                # ou apenas (x, y) se 'velocidade' não for um parâmetro comum a todos.
                # É mais seguro se todos os inimigos tiverem uma assinatura de construtor consistente.
                # Se a velocidade padrão for definida dentro de cada classe de inimigo,
                # podemos chamar apenas com (x,y).
                novo_inimigo = ClasseInimigo(x, y, velocidade=velocidade)
            except TypeError as e_construtor:
                # Se falhar, tenta sem o parâmetro 'velocidade', assumindo que é opcional
                # ou que a classe inimiga não o aceita.
                try:
                    novo_inimigo = ClasseInimigo(x, y)
                    # print(f"DEBUG(GerenciadorDeInimigos): {tipo_inimigo_str} criado sem arg 'velocidade'.")
                except TypeError as e_construtor_simples:
                    print(f"DEBUG(GerenciadorDeInimigos): Erro de TypeError ao criar {tipo_inimigo_str}: {e_construtor_simples}. "
                          f"Construtor original tentado: {e_construtor}. Verifique os argumentos.")
            except Exception as e:
                print(f"DEBUG(GerenciadorDeInimigos): Erro desconhecido ao criar {tipo_inimigo_str}: {e}")
        else:
            print(f"DEBUG(GerenciadorDeInimigos): Classe para tipo '{tipo_inimigo_str}' não encontrada ou não importada.")

        if novo_inimigo:
            self.adicionar_inimigo(novo_inimigo)
        return novo_inimigo

    def spawn_inimigos_iniciais(self, jogador):
        """Faz o spawn de uma quantidade inicial de inimigos no início de uma estação."""
        if self.estacoes is None or not hasattr(self.estacoes, 'nome_estacao'):
            print("DEBUG(GerenciadorDeInimigos): Aviso: Objeto Estacoes não disponível para spawn inicial.")
            return

        est_nome = self.estacoes.nome_estacao()
        print(f"DEBUG(GerenciadorDeInimigos): Realizando spawn inicial de {self.spawns_iniciais} inimigos para estação '{est_nome}'.")
        for _ in range(self.spawns_iniciais):
            if len(self.inimigos) < self.limite_inimigos:
                self._spawn_inimigo_especifico_da_estacao(est_nome, jogador)
            else:
                print("DEBUG(GerenciadorDeInimigos): Limite de inimigos atingido durante spawn inicial.")
                break
        # Reseta os temporizadores após o spawn inicial para que a thread comece a contagem corretamente
        self.ultimo_spawn_controlado_pelo_thread = time.time()
        self.tempo_inicio_estacao_para_spawn = time.time()


    def update_inimigos(self, jogador, dt_ms=None):
        """Atualiza todos os inimigos ativos e remove os que não estão mais vivos."""
        inimigos_para_remover = []
        for inimigo in self.inimigos:
            if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo():
                if hasattr(inimigo, 'update'):
                    try:
                        # Tenta passar todos os parâmetros que o inimigo PODE precisar
                        inimigo.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela, dt_ms)
                    except TypeError: # Fallbacks para diferentes assinaturas de update
                        try:
                            inimigo.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela)
                        except TypeError:
                            try:
                                inimigo.update(jogador, self.projeteis_inimigos)
                            except TypeError:
                                try:
                                    inimigo.update(jogador) # O mais básico
                                except Exception as e_final:
                                     print(f"DEBUG(GerenciadorInimigos): Erro ao chamar update de {type(inimigo).__name__}: {e_final}. Args não correspondem.")
            else: # Se o inimigo não está mais vivo
                inimigos_para_remover.append(inimigo)

        for inimigo_removido in inimigos_para_remover:
            self.remover_inimigo(inimigo_removido) # Usa o método que também chama .kill()

    def update_projeteis_inimigos(self, jogador, dt_ms=None):
        """Atualiza todos os projéteis ativos e remove os inativos."""
        for projetil in list(self.projeteis_inimigos): # Itera sobre uma cópia para remoção segura
            if hasattr(projetil, 'update'):
                try:
                    projetil.update(jogador, self.tela_largura, self.altura_tela, dt_ms)
                except TypeError: # Fallbacks
                    try:
                        projetil.update(jogador, self.tela_largura, self.altura_tela)
                    except TypeError:
                        try:
                            projetil.update(jogador)
                        except Exception as e_final_proj:
                            print(f"DEBUG(GerenciadorInimigos): Erro ao chamar update de projétil {type(projetil).__name__}: {e_final_proj}.")

            # Verifica se o projétil deve ser removido (geralmente o próprio projétil chama self.kill())
            # Esta é uma checagem adicional.
            deve_remover = False
            if hasattr(projetil, 'alive'):
                if isinstance(projetil.alive, bool) and not projetil.alive:
                    deve_remover = True
                elif callable(projetil.alive) and not projetil.alive(): # Ex: método padrão de Sprite
                    deve_remover = True
            elif not self.projeteis_inimigos.has(projetil): # Se já foi removido (por self.kill() interno)
                continue # Já tratado, não precisa fazer nada

            if deve_remover:
                self.projeteis_inimigos.remove(projetil) # Remove do grupo
                # Não precisa chamar kill() aqui se o próprio projétil já o fez ao setar alive=False


    def desenhar_inimigos(self, janela, camera_x: int, camera_y: int):
        """Desenha todos os inimigos ativos na tela."""
        for inimigo in self.inimigos:
            if hasattr(inimigo, 'desenhar'):
                inimigo.desenhar(janela, camera_x, camera_y)

    def desenhar_projeteis_inimigos(self, surface, camera_x, camera_y):
        """Desenha todos os projéteis ativos na tela."""
        for projetil in self.projeteis_inimigos:
            if hasattr(projetil, 'desenhar'):
                projetil.desenhar(surface, camera_x, camera_y)

    def get_inimigos_vivos(self):
        """Retorna o grupo de inimigos ativos."""
        return self.inimigos

    def limpar_inimigos(self):
        """Remove todos os inimigos e projéteis, geralmente ao mudar de nível ou reiniciar."""
        self.inimigos.empty()
        self.projeteis_inimigos.empty()
        print("DEBUG(GerenciadorDeInimigos): Todos os inimigos e projéteis limpos.")

    def stop_threads(self):
        """Sinaliza para a thread de spawn parar e espera que ela termine."""
        print("DEBUG(GerenciadorDeInimigos): Sinalizando para parar thread de spawn...")
        self.stop_spawn_thread_event.set() # Aciona o evento de parada
        if self.spawn_controller_thread and self.spawn_controller_thread.is_alive():
            self.spawn_controller_thread.join(timeout=1.0) # Espera pela thread por até 1 segundo
            if self.spawn_controller_thread.is_alive():
                print("DEBUG(GerenciadorDeInimigos): AVISO: Thread de spawn não terminou a tempo.")
            else:
                print("DEBUG(GerenciadorDeInimigos): Thread de spawn finalizado com sucesso.")

