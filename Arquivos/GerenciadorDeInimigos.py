# GerenciadorDeInimigos.py
import pygame
import random
import time
import math 
import os 
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
            pygame.draw.rect(self.image, (255, 0, 255), (0, 0, largura, altura)) 
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
            self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128); self.facing_right = True
            self.sprites = [self.image]; self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.intervalo_animacao = 200; self.is_attacking = False
            self.attack_hitbox = pygame.Rect(0,0,0,0); self.hit_by_player_this_attack = False
            self.contact_cooldown = 1000; self.last_contact_time = pygame.time.get_ticks()
        def _carregar_sprite(self, path, tamanho): return pygame.Surface(tamanho) 
        def receber_dano(self, dano, fonte_dano_rect=None): self.hp -= dano; self.last_hit_time = pygame.time.get_ticks(); self.hp = max(0, self.hp)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, alvo_x, alvo_y): pass
        def atualizar_animacao(self): pass
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None): pass
        def desenhar(self, janela, camera_x, camera_y): janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

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
try: from Projetil_BolaNeve import ProjetilNeve 
except ImportError: ProjetilNeve = None; print("DEBUG(GerenciadorDeInimigos): ProjetilNeve não encontrado.")


class GerenciadorDeInimigos:
    def __init__(self, estacoes_obj, tela_largura: int, altura_tela: int, 
                 intervalo_spawn_inicial: float = 3.0, # REDUZIDO: Inimigos aparecem mais rápido no início
                 spawns_iniciais: int = 10, 
                 limite_inimigos: int = 3000, # Aumentado um pouco o limite para mais ação
                 fator_exponencial_spawn: float = 0.025, # Ligeiramente aumentado para acelerar mais rápido
                 intervalo_spawn_minimo: float = 0.3): # REDUZIDO: Permite spawns muito mais frequentes no pico
        
        self.estacoes = estacoes_obj
        self.inimigos = pygame.sprite.Group() 
        self.projeteis_inimigos = pygame.sprite.Group()
        
        self.intervalo_spawn_inicial = intervalo_spawn_inicial 
        self.spawns_iniciais = spawns_iniciais 
        self.limite_inimigos = limite_inimigos 
        
        self.tempo_inicio_estacao_para_spawn = time.time() 
        
        self.fator_exponencial_spawn = fator_exponencial_spawn 
        self.intervalo_spawn_minimo = intervalo_spawn_minimo 
        
        self.tela_largura = tela_largura
        self.altura_tela = altura_tela

        self.spawn_request_queue = queue.Queue()
        self.stop_spawn_thread_event = threading.Event()
        self.ultimo_spawn_controlado_pelo_thread = time.time() 
        
        self.spawn_controller_thread = threading.Thread(
            target=self._spawn_controller_task, 
            daemon=True 
        )
        self.spawn_controller_thread.start()
        print("DEBUG(GerenciadorDeInimigos): Gerenciador de Inimigos e Thread de Spawn inicializados (Spawn mais rápido).")

    def resetar_temporizador_spawn_estacao(self):
        print(f"DEBUG(GerenciadorDeInimigos): Resetando temporizador de spawn para nova estação.")
        self.tempo_inicio_estacao_para_spawn = time.time()
        self.ultimo_spawn_controlado_pelo_thread = time.time() 
        
        while not self.spawn_request_queue.empty():
            try:
                self.spawn_request_queue.get_nowait()
                self.spawn_request_queue.task_done()
            except queue.Empty:
                break
        print("DEBUG(GerenciadorDeInimigos): Fila de pedidos de spawn limpa para nova estação.")


    def _spawn_controller_task(self):
        # print("DEBUG(GerenciadorDeInimigos): Thread de controle de spawn iniciado.") # Log menos frequente
        while not self.stop_spawn_thread_event.is_set():
            agora = time.time()
            tempo_decorrido_na_estacao = agora - self.tempo_inicio_estacao_para_spawn
            
            intervalo_atual = max(
                self.intervalo_spawn_minimo, 
                self.intervalo_spawn_inicial * math.exp(-self.fator_exponencial_spawn * tempo_decorrido_na_estacao)
            )
            
            if agora - self.ultimo_spawn_controlado_pelo_thread >= intervalo_atual:
                if self.estacoes and hasattr(self.estacoes, 'nome_estacao'):
                    estacao_atual_nome = self.estacoes.nome_estacao()
                    self.spawn_request_queue.put({"estacao": estacao_atual_nome, "timestamp": agora})
                    # print(f"DEBUG(GerenciadorDeInimigos Thread): Pedido de spawn. Intervalo: {intervalo_atual:.2f}s") # Log menos frequente
                    self.ultimo_spawn_controlado_pelo_thread = agora 
            
            self.stop_spawn_thread_event.wait(timeout=0.05) # Verifica mais frequentemente
        print("DEBUG(GerenciadorDeInimigos): Thread de controle de spawn finalizado.")

    def process_spawn_requests(self, jogador):
        try:
            while not self.spawn_request_queue.empty():
                if len(self.inimigos) >= self.limite_inimigos:
                    self.spawn_request_queue.get_nowait() 
                    self.spawn_request_queue.task_done()
                    continue

                request_data = self.spawn_request_queue.get_nowait()
                estacao_nome = request_data.get("estacao")
                
                if jogador and estacao_nome: 
                    self._spawn_inimigo_especifico_da_estacao(estacao_nome, jogador)
                
                self.spawn_request_queue.task_done()
        except queue.Empty:
            pass 
        except Exception as e:
            print(f"DEBUG(GerenciadorDeInimigos): Erro ao processar fila de spawn: {e}")


    def _spawn_inimigo_especifico_da_estacao(self, estacao_nome, jogador):
        est_nome_lower = estacao_nome.lower()
        tipos_disponiveis = []
        
        if est_nome_lower == "inverno":
            if Fantasma: tipos_disponiveis.append('fantasma')
            if BonecoDeNeve: tipos_disponiveis.append('bonecodeneve')
            if Lobo: tipos_disponiveis.append('lobo') 
        elif est_nome_lower == "primavera":
            if Planta_Carnivora: tipos_disponiveis.append('planta_carnivora')
            if Mae_Natureza: tipos_disponiveis.append('maenatureza')
            if Espirito_Das_Flores: tipos_disponiveis.append('espiritodasflores')
        elif est_nome_lower == "outono":
            if Espantalho: tipos_disponiveis.append('espantalho')
        elif est_nome_lower == "verão": 
            if Fenix: tipos_disponiveis.append('fenix')
            if Urso: tipos_disponiveis.append('urso') 
        
        if tipos_disponiveis:
            tipo_escolhido = random.choice(tipos_disponiveis)
            
            player_screen_rect = jogador.rect.inflate(self.tela_largura, self.altura_tela) 
            
            spawn_pos_ok = False
            tentativas_spawn = 0
            max_tentativas_spawn = 20
            x, y = 0, 0

            while not spawn_pos_ok and tentativas_spawn < max_tentativas_spawn:
                spawn_distance_from_player = random.randint(int(self.tela_largura * 0.6), int(self.tela_largura * 0.9)) 
                angle = random.uniform(0, 2 * math.pi)
                
                x = jogador.rect.centerx + spawn_distance_from_player * math.cos(angle)
                y = jogador.rect.centery + spawn_distance_from_player * math.sin(angle)
                
                ponto_spawn_teste = pygame.Rect(x,y,1,1)
                if not player_screen_rect.colliderect(ponto_spawn_teste):
                     spawn_pos_ok = True
                tentativas_spawn +=1

            if not spawn_pos_ok: 
                spawn_distance = random.randint(400, 700)
                angle = random.uniform(0, 2 * math.pi)
                x = jogador.rect.centerx + spawn_distance * math.cos(angle)
                y = jogador.rect.centery + spawn_distance * math.sin(angle)

            self.criar_inimigo_aleatorio(tipo_escolhido, x, y)


    def adicionar_inimigo(self, inimigo):
        if inimigo: 
            self.inimigos.add(inimigo) 

    def remover_inimigo(self, inimigo):
        self.inimigos.remove(inimigo) 
        if hasattr(inimigo, 'kill'): 
            inimigo.kill()


    def criar_inimigo_aleatorio(self, tipo_inimigo_str, x, y, velocidade=1.0):
        novo_inimigo = None
        mapa_tipos = {
            'fantasma': Fantasma, 'bonecodeneve': BonecoDeNeve, 
            'planta_carnivora': Planta_Carnivora, 'espantalho': Espantalho,
            'fenix': Fenix, 'maenatureza': Mae_Natureza,
            'espiritodasflores': Espirito_Das_Flores, 'lobo': Lobo, 'urso': Urso
        }
        
        ClasseInimigo = mapa_tipos.get(tipo_inimigo_str.lower())
        
        if ClasseInimigo is not None:
            try:
                novo_inimigo = ClasseInimigo(x, y, velocidade=velocidade) 
            except TypeError as e:
                print(f"DEBUG(GerenciadorDeInimigos): Erro de TypeError ao criar {tipo_inimigo_str}: {e}. Verifique os argumentos do construtor.")
            except Exception as e:
                print(f"DEBUG(GerenciadorDeInimigos): Erro desconhecido ao criar {tipo_inimigo_str}: {e}")
        else:
            print(f"DEBUG(GerenciadorDeInimigos): Classe para tipo '{tipo_inimigo_str}' não encontrada ou não importada.")

        if novo_inimigo:
            self.adicionar_inimigo(novo_inimigo)
        return novo_inimigo

    def spawn_inimigos_iniciais(self, jogador): 
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
        self.ultimo_spawn_controlado_pelo_thread = time.time() 
        self.tempo_inicio_estacao_para_spawn = time.time() 


    def update_inimigos(self, jogador): 
        inimigos_para_remover = []
        for inimigo in self.inimigos: 
            if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo():
                if hasattr(inimigo, 'update'):
                    inimigo.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela)
            else: 
                inimigos_para_remover.append(inimigo)
        
        for inimigo in inimigos_para_remover:
            self.remover_inimigo(inimigo)

    def update_projeteis_inimigos(self, jogador): 
        for projetil in list(self.projeteis_inimigos):  
            if hasattr(projetil, 'update'):
                projetil.update(jogador, self.tela_largura, self.altura_tela) 
            
            if hasattr(projetil, 'alive') and not projetil.alive(): 
                self.projeteis_inimigos.remove(projetil)
                if hasattr(projetil, 'kill'): projetil.kill()
            elif not hasattr(projetil, 'alive'): 
                 self.projeteis_inimigos.remove(projetil)
                 if hasattr(projetil, 'kill'): projetil.kill()


    def desenhar_inimigos(self, janela, camera_x: int, camera_y: int):
        for inimigo in self.inimigos: 
            if hasattr(inimigo, 'desenhar'):
                inimigo.desenhar(janela, camera_x, camera_y)

    def desenhar_projeteis_inimigos(self, surface, camera_x, camera_y):
        for projetil in self.projeteis_inimigos: 
            if hasattr(projetil, 'desenhar'):
                projetil.desenhar(surface, camera_x, camera_y)

    def get_inimigos_vivos(self): 
        return self.inimigos 

    def limpar_inimigos(self):
        self.inimigos.empty() 
        self.projeteis_inimigos.empty() 
        print("DEBUG(GerenciadorDeInimigos): Todos os inimigos e projéteis limpos.")

    def stop_threads(self):
        print("DEBUG(GerenciadorDeInimigos): Sinalizando para parar thread de spawn...")
        self.stop_spawn_thread_event.set()
        if self.spawn_controller_thread and self.spawn_controller_thread.is_alive():
            self.spawn_controller_thread.join(timeout=1.0) 
            if self.spawn_controller_thread.is_alive():
                print("DEBUG(GerenciadorDeInimigos): AVISO: Thread de spawn não terminou a tempo.")
            else:
                print("DEBUG(GerenciadorDeInimigos): Thread de spawn finalizado com sucesso.")
