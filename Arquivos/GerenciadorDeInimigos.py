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
        def esta_vivo(self): return self.hp > 0
        def update(self, *args, **kwargs): pass
        def desenhar(self, *args, **kwargs): pass
        def kill(self): super().kill()


class GerenciadorDeInimigos:
    def __init__(self, estacoes_obj, tela_largura: int, altura_tela: int,
                 gerenciador_moedas_ref=None,
                 intervalo_spawn_inicial: float = 3.0, spawns_iniciais: int = 5,
                 limite_inimigos: int = 50, fator_exponencial_spawn: float = 0.020,
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

    def _spawn_inimigo_especifico_da_estacao(self, jogador):
        mapa_estacao_inimigos = {
            "Inverno": ['fantasma', 'bonecodeneve', 'lobo'],
            "Primavera": ['planta_carnivora', 'goblin', 'espiritodasflores', 'maenatureza'],
            "Outono": ['espantalho', 'troll', 'vampiro'],
            "Verão": ['urso', 'cavaleiro', 'maga']
        }
        est_nome = self.estacoes.nome_estacao_atual()
        tipos_disponiveis = [tipo for tipo in mapa_estacao_inimigos.get(est_nome, []) if tipo in self.enemy_class_map]
        
        if not tipos_disponiveis: return
        tipo_escolhido = random.choice(tipos_disponiveis)
        ClasseInimigo = self.enemy_class_map.get(tipo_escolhido)
        if not ClasseInimigo: return

        cam_rect = pygame.Rect(jogador.rect.centerx - self.tela_largura / 2, jogador.rect.centery - self.altura_tela / 2, self.tela_largura, self.altura_tela)
        spawn_margin = 100
        edge = random.choice(["top", "bottom", "left", "right"])

        if edge == "top": x, y = random.uniform(cam_rect.left, cam_rect.right), cam_rect.top - spawn_margin
        elif edge == "bottom": x, y = random.uniform(cam_rect.left, cam_rect.right), cam_rect.bottom + spawn_margin
        elif edge == "left": x, y = cam_rect.left - spawn_margin, random.uniform(cam_rect.top, cam_rect.bottom)
        else: x, y = cam_rect.right + spawn_margin, random.uniform(cam_rect.top, cam_rect.bottom)
        
        self.inimigos.add(ClasseInimigo(x=x, y=y))

    def spawn_inimigos_iniciais(self, jogador):
        if self._spawn_normal_pausado: return
        for _ in range(self.spawns_iniciais):
            if len(self.inimigos) < self.limite_inimigos:
                self._spawn_inimigo_especifico_da_estacao(jogador)

    def update_inimigos(self, jogador, dt_ms):
        self.inimigos.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela, dt_ms)
        
        for inimigo in list(self.inimigos):
            if not inimigo.esta_vivo():
                if self.gerenciador_moedas and hasattr(inimigo, 'moedas_drop'): self.gerenciador_moedas.create_coins_from_enemy(inimigo)
                if hasattr(jogador, 'xp_manager') and hasattr(inimigo, 'xp_value'): jogador.xp_manager.gain_xp(inimigo.xp_value)
                inimigo.kill()

    def update_projeteis_inimigos(self, jogador, dt_ms):
        # --- CORREÇÃO APLICADA AQUI ---
        # A chamada de update para o grupo de projéteis agora passa
        # apenas o 'dt_ms', que é o único argumento que o ProjetilMaga.update() espera.
        self.projeteis_inimigos.update(dt_ms)

        # O resto da lógica, como a verificação de colisão, permanece o mesmo
        colisoes = pygame.sprite.spritecollide(jogador, self.projeteis_inimigos, True, pygame.sprite.collide_mask)
        for projetil in colisoes:
            if jogador.pode_levar_dano:
                jogador.receber_dano(projetil.dano, projetil.rect)
    
    def spawn_chefe_estacao(self, indice_estacao_chefe, posicao_mundo_spawn):
        self.grupo_chefe_ativo.empty()
        
        ClasseChefe = self.chefes_por_estacao.get(indice_estacao_chefe)
        
        if not ClasseChefe:
            print(f"ERRO CRÍTICO: Classe do chefe para o índice {indice_estacao_chefe} não foi carregada ou não existe. Verifique o __init__.")
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
