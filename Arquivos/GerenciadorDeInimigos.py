import pygame
import random
import time
import math
import threading
import queue # Para fila thread-safe
import os
import sys

# --- Configuração do sys.path ---
# Garante que os módulos do projeto possam ser encontrados
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    sys.path.insert(0, os.path.join(project_root, "Arquivos"))

# Tenta importar todas as classes de inimigos de reuniaoInimigos.py
try:
    from reuniaoInimigos import *
except ImportError as e:
    print(f"AVISO(GerenciadorDeInimigos): Módulo 'reuniaoInimigos.py' não encontrado: {e}. As classes serão carregadas dinamicamente.")
    pass

# Garante que a classe base Inimigo seja importada ou definida para evitar erros
try:
    from Inimigos.Inimigos import Inimigo
except ImportError:
    print("ERRO CRÍTICO(GerenciadorDeInimigos): Classe base 'Inimigo' não encontrada. Usando placeholder.")
    class Inimigo(pygame.sprite.Sprite): # type: ignore
        def __init__(self, x, y, **kwargs):
            super().__init__()
            self.rect = pygame.Rect(x,y,32,32); self.image = pygame.Surface((32,32)); self.image.fill((255,0,0,100))
            self.hp = 1; self.max_hp = 1; self.xp_value = 0; self.moedas_drop = 0; self.contact_damage = 1
            self.x = float(x); self.y = float(y) # Garante que x e y sejam floats
        def esta_vivo(self): return self.hp > 0
        def update(self, *args, **kwargs): pass
        def desenhar(self, *args, **kwargs): pass
        def kill(self): super().kill()


class GerenciadorDeInimigos:
    def __init__(self, estacoes_obj, tela_largura: int, altura_tela: int,
                 gerenciador_moedas_ref=None,
                 intervalo_spawn_inicial: float = 3.0, spawns_iniciais: int = 20,
                 limite_inimigos: int = 500, fator_exponencial_spawn: float = 0.020,
                 intervalo_spawn_minimo: float = 0.5, atraso_spawn_estacao_seg: float = 2.0):

        self.estacoes = estacoes_obj
        self.inimigos = pygame.sprite.Group()
        self.projeteis_inimigos = pygame.sprite.Group()
        self.grupo_chefe_ativo = pygame.sprite.GroupSingle()
        self.gerenciador_moedas = gerenciador_moedas_ref

        self.intervalo_spawn_inicial = intervalo_spawn_inicial
        self.spawns_iniciais = spawns_iniciais
        self.limite_inimigos = limite_inimigos
        self.tempo_inicio_estacao_para_spawn = time.time()
        self.fator_exponencial_spawn = fator_exponencial_spawn
        self.intervalo_spawn_minimo = intervalo_spawn_minimo
        self.tela_largura, self.altura_tela = tela_largura, altura_tela

        self.spawn_request_queue = queue.Queue()
        self.stop_spawn_thread_event = threading.Event()
        self.ultimo_spawn_controlado_pelo_thread = time.time()
        self.atraso_configurado_estacao = atraso_spawn_estacao_seg
        self.tempo_fim_atraso_spawn_continuo = 0
        self.atraso_spawn_continuo_ativo = False
        self._spawn_normal_pausado = False

        ### LÓGICA DA HORDA: INÍCIO ###
        self.distancia_ativacao_horda = 1500  # Distância em pixels para ativar a horda
        self.tamanho_horda = 10              # Quantidade de inimigos na horda
        self.cooldown_horda_s = 15.0         # Cooldown de 15s entre hordas
        self.tempo_ultima_horda = 0
        self.ultima_posicao_jogador = None   # Para rastrear a direção de movimento do jogador
        ### LÓGICA DA HORDA: FIM ###

        # Mapeamento de nomes para o caminho do módulo
        self.enemy_module_map = {
            "arvoremaldita": "Inimigos.Arvore_Maldita", "fantasma": "Inimigos.Fantasma",
            "bonecodeneve": "Inimigos.BonecoDeNeve", "planta_carnivora": "Inimigos.Planta_Carnivora",
            "espantalho": "Inimigos.Espantalho", "fenix": "Inimigos.Fenix",
            "maenatureza": "Inimigos.Mae_Natureza", "espiritodasflores": "Inimigos.Espirito_Das_Flores",
            "lobo": "Inimigos.Lobo", "urso": "Inimigos.Urso", "troll": "Inimigos.Troll",
            "golem_neve": "Inimigos.Golem_Neve", "goblin": "Inimigos.Goblin",
            "vampiro": "Inimigos.Vampiro", "demonio": "Inimigos.Demonio", "morte": "Inimigos.Morte",
            "maga": "Inimigos.Maga", "cavaleiro": "Inimigos.Cavaleiro"
        }
        self.enemy_class_map = self._load_enemy_classes()
        
        # Dicionário de chefes por estação, usando as classes carregadas
        self.chefes_por_estacao = {
            0: self.enemy_class_map.get("arvoremaldita"),
            1: self.enemy_class_map.get("fenix"),
            2: self.enemy_class_map.get("morte"),
            3: self.enemy_class_map.get("golem_neve")
        }

        self.spawn_controller_thread = threading.Thread(target=self._spawn_controller_task, daemon=True)
        self.spawn_controller_thread.start()

    def _load_enemy_classes(self):
        """Carrega dinamicamente as classes de inimigos para evitar importações diretas e erros."""
        loaded_classes = {}
        for name, module_path in self.enemy_module_map.items():
            try:
                class_name = module_path.split('.')[-1]
                module = __import__(module_path, fromlist=[class_name])
                loaded_classes[name] = getattr(module, class_name)
            except (ImportError, AttributeError) as e:
                print(f"AVISO(GerenciadorInimigos): Não foi possível carregar a classe para '{name}' de '{module_path}': {e}")
        return loaded_classes

    def pausar_spawn_normal(self, pausar: bool):
        self._spawn_normal_pausado = pausar

    def resetar_temporizador_spawn_estacao(self):
        agora = time.time()
        self.tempo_inicio_estacao_para_spawn = agora
        self.tempo_fim_atraso_spawn_continuo = agora + self.atraso_configurado_estacao
        self.atraso_spawn_continuo_ativo = True
        with self.spawn_request_queue.mutex:
            self.spawn_request_queue.queue.clear()
    
    def _spawn_controller_task(self):
        while not self.stop_spawn_thread_event.is_set():
            time.sleep(0.1)
            agora = time.time()
            if self._spawn_normal_pausado or (self.atraso_spawn_continuo_ativo and agora < self.tempo_fim_atraso_spawn_continuo):
                continue
            
            self.atraso_spawn_continuo_ativo = False
            
            tempo_decorrido = agora - self.tempo_inicio_estacao_para_spawn
            intervalo_atual = max(self.intervalo_spawn_minimo, self.intervalo_spawn_inicial * math.exp(-self.fator_exponencial_spawn * tempo_decorrido))

            if agora - self.ultimo_spawn_controlado_pelo_thread >= intervalo_atual:
                if len(self.inimigos) < self.limite_inimigos and self.estacoes:
                    self.spawn_request_queue.put(True)
                    self.ultimo_spawn_controlado_pelo_thread = agora

    def process_spawn_requests(self, jogador, dt_ms=None):
        try:
            while not self.spawn_request_queue.empty():
                self.spawn_request_queue.get_nowait()
                if len(self.inimigos) < self.limite_inimigos and jogador:
                    self._spawn_inimigo_especifico_da_estacao(jogador)
                self.spawn_request_queue.task_done()
        except queue.Empty:
            pass

    def _get_enemy_types_for_current_season(self):
        """Retorna uma lista de nomes de inimigos para a estação atual."""
        mapa_estacao_inimigos = {
            "Inverno": ['fantasma', 'bonecodeneve', 'lobo'],
            "Primavera": ['planta_carnivora', 'goblin', 'espiritodasflores', 'maenatureza'],
            "Outono": ['espantalho', 'troll', 'vampiro'],
            "Verão": ['urso', 'cavaleiro', 'maga']
        }
        est_nome = self.estacoes.nome_estacao_atual()
        return [tipo for tipo in mapa_estacao_inimigos.get(est_nome, []) if tipo in self.enemy_class_map]

    def _spawn_inimigo_em_posicao(self, x, y):
        """Spawna um inimigo da estação atual em uma posição específica."""
        tipos_disponiveis = self._get_enemy_types_for_current_season()
        if not tipos_disponiveis:
            return

        tipo_escolhido = random.choice(tipos_disponiveis)
        ClasseInimigo = self.enemy_class_map.get(tipo_escolhido)
        if ClasseInimigo and len(self.inimigos) < self.limite_inimigos:
            self.inimigos.add(ClasseInimigo(x=x, y=y))

    def _spawn_inimigo_especifico_da_estacao(self, jogador):
        """Spawna um inimigo da estação atual em um ângulo aleatório ao redor do jogador."""
        distancia_do_canto = math.hypot(self.tela_largura / 2, self.altura_tela / 2)
        raio_spawn = distancia_do_canto + 200
        angulo = random.uniform(0, 2 * math.pi)
        x = jogador.rect.centerx + raio_spawn * math.cos(angulo)
        y = jogador.rect.centery + raio_spawn * math.sin(angulo)
        self._spawn_inimigo_em_posicao(x, y)

    def spawn_inimigos_iniciais(self, jogador):
        if self._spawn_normal_pausado: return
        for _ in range(self.spawns_iniciais):
            if len(self.inimigos) < self.limite_inimigos:
                self._spawn_inimigo_especifico_da_estacao(jogador)

    ### LÓGICA DA HORDA: INÍCIO ###
    def _spawn_horda(self, jogador, direcao_horda):
        """Spawna uma onda de inimigos na frente do jogador."""
        print("DEBUG: Ativando horda!")
        # Distância à frente do jogador para spawnar a horda
        distancia_spawn_frente = math.hypot(self.tela_largura / 2, self.altura_tela / 2) + 100

        # Ponto central para o spawn da horda
        ponto_central_spawn = pygame.math.Vector2(jogador.rect.center) + direcao_horda * distancia_spawn_frente

        for _ in range(self.tamanho_horda):
            # Adiciona uma pequena variação aleatória para espalhar a horda
            offset_x = random.uniform(-150, 150)
            offset_y = random.uniform(-150, 150)
            self._spawn_inimigo_em_posicao(ponto_central_spawn.x + offset_x, ponto_central_spawn.y + offset_y)

    def _verificar_e_ativar_horda(self, jogador, vetor_movimento_jogador):
        """Verifica se as condições para uma horda são atendidas e a ativa."""
        # 1. Verificar se a horda está em cooldown
        if time.time() - self.tempo_ultima_horda < self.cooldown_horda_s:
            return

        # 2. Verificar se há inimigos na tela para calcular a distância
        if not self.inimigos:
            return

        # 3. Calcular o ponto central dos inimigos
        soma_x, soma_y = 0, 0
        for inimigo in self.inimigos:
            soma_x += inimigo.rect.centerx
            soma_y += inimigo.rect.centery
        centro_massa_inimigos = pygame.math.Vector2(soma_x / len(self.inimigos), soma_y / len(self.inimigos))

        # --- CORREÇÃO DO ERRO ---
        # Converte o 'center' (tupla) do jogador para um Vetor2D antes de calcular a distância.
        posicao_jogador_vetor = pygame.math.Vector2(jogador.rect.center)
        distancia_jogador_horda = posicao_jogador_vetor.distance_to(centro_massa_inimigos)

        # 5. Ativar se a distância for maior que o limite
        if distancia_jogador_horda > self.distancia_ativacao_horda:
            self.tempo_ultima_horda = time.time()  # Ativa o cooldown
            direcao_normalizada = vetor_movimento_jogador.normalize()
            self._spawn_horda(jogador, direcao_normalizada)
    ### LÓGICA DA HORDA: FIM ###

    def _resolver_colisoes_entre_inimigos(self):
        """Verifica e resolve colisões entre inimigos para evitar sobreposição."""
        inimigos = self.inimigos.sprites()
        forca_repulsao = 1.0
        forcas_totais = {inimigo: pygame.math.Vector2(0, 0) for inimigo in inimigos}

        for i, inimigo_a in enumerate(inimigos):
            if inimigo_a in self.grupo_chefe_ativo: continue
            for j in range(i + 1, len(inimigos)):
                inimigo_b = inimigos[j]
                if inimigo_b in self.grupo_chefe_ativo: continue

                if inimigo_a.rect.colliderect(inimigo_b.rect):
                    vetor_colisao = pygame.math.Vector2(inimigo_a.rect.center) - pygame.math.Vector2(inimigo_b.rect.center)
                    if vetor_colisao.length() > 0:
                        direcao = vetor_colisao.normalize()
                        forcas_totais[inimigo_a] += direcao
                        forcas_totais[inimigo_b] -= direcao

        for inimigo, forca_total in forcas_totais.items():
            if forca_total.length() > 0:
                direcao_final = forca_total.normalize() * forca_repulsao
                inimigo.x += direcao_final.x
                inimigo.y += direcao_final.y
                inimigo.rect.topleft = (inimigo.x, inimigo.y)

    def update_inimigos(self, jogador, dt_ms):
        """Atualiza a lógica dos inimigos, incluindo movimento, colisões e a nova lógica de horda."""
        ### LÓGICA DA HORDA: INÍCIO ###
        if self.ultima_posicao_jogador is not None and jogador is not None:
            # Calcula o vetor de movimento do jogador desde o último frame
            vetor_movimento = pygame.math.Vector2(jogador.rect.center) - self.ultima_posicao_jogador
            # Só verifica a horda se o jogador estiver se movendo
            if vetor_movimento.length() > 1:
                self._verificar_e_ativar_horda(jogador, vetor_movimento)
        
        # Atualiza a última posição do jogador para o próximo frame
        if jogador is not None:
            self.ultima_posicao_jogador = pygame.math.Vector2(jogador.rect.center)
        ### LÓGICA DA HORDA: FIM ###
        
        # 1. Atualiza a lógica individual de cada inimigo (movimento, ataque, etc.)
        self.inimigos.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela, dt_ms)
        
        # 2. Resolve as colisões entre os inimigos para o efeito de horda
        self._resolver_colisoes_entre_inimigos()
        
        # 3. Remove inimigos mortos e concede recompensas
        for inimigo in list(self.inimigos):
            if not inimigo.esta_vivo():
                if self.gerenciador_moedas and hasattr(inimigo, 'moedas_drop'): self.gerenciador_moedas.create_coins_from_enemy(inimigo)
                if hasattr(jogador, 'xp_manager') and hasattr(inimigo, 'xp_value'): jogador.xp_manager.gain_xp(inimigo.xp_value)
                inimigo.kill()

    def update_projeteis_inimigos(self, jogador, dt_ms):
        self.projeteis_inimigos.update(dt_ms)
        colisoes = pygame.sprite.spritecollide(jogador, self.projeteis_inimigos, True, pygame.sprite.collide_mask)
        for projetil in colisoes:
            if hasattr(jogador, 'pode_levar_dano') and jogador.pode_levar_dano:
                jogador.receber_dano(projetil.dano, projetil.rect)
    
    def spawn_chefe_estacao(self, indice_estacao_chefe, posicao_mundo_spawn):
        self.grupo_chefe_ativo.empty()
        ClasseChefe = self.chefes_por_estacao.get(indice_estacao_chefe)
        if not ClasseChefe:
            print(f"ERRO CRÍTICO: Classe do chefe para o índice {indice_estacao_chefe} não foi carregada.")
            return None
        try:
            chefe_spawnado = ClasseChefe(x=posicao_mundo_spawn[0], y=posicao_mundo_spawn[1])
            self.grupo_chefe_ativo.add(chefe_spawnado)
            self.inimigos.add(chefe_spawnado)
            print(f"DEBUG(GerenciadorInimigos): Chefe '{type(chefe_spawnado).__name__}' spawnado.")
            return chefe_spawnado
        except Exception as e:
            print(f"ERRO CRÍTICO ao instanciar chefe {ClasseChefe.__name__}: {e}")
            return None

    def update_chefe(self, jogador, dt_ms):
        if self.grupo_chefe_ativo.sprite:
            self.grupo_chefe_ativo.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela, dt_ms)

    def desenhar_inimigos(self, janela, camera_x, camera_y):
        for inimigo in self.inimigos:
            inimigo.desenhar(janela, camera_x, camera_y)
            
    def desenhar_chefe(self, janela, camera_x, camera_y):
        if self.grupo_chefe_ativo.sprite:
            self.grupo_chefe_ativo.sprite.desenhar(janela, camera_x, camera_y)

    def desenhar_projeteis_inimigos(self, surface, camera_x, camera_y):
        for proj in self.projeteis_inimigos:
            proj.desenhar(surface, camera_x, camera_y)

    def limpar_todos_inimigos_normais(self):
        for inimigo in list(self.inimigos):
            if inimigo not in self.grupo_chefe_ativo:
                inimigo.kill()
        self.projeteis_inimigos.empty()
    
    def stop_threads(self):
        self.stop_spawn_thread_event.set()
        if self.spawn_controller_thread.is_alive():
            self.spawn_controller_thread.join(timeout=1)
