# GerenciadorDeInimigos.py
import pygame
import random
import time
import math
import threading
import queue # Para fila thread-safe
import os 

# Importa a classe base Inimigo
try:
    from Inimigos import Inimigo
    print("DEBUG(GerenciadorDeInimigos): Classe base Inimigo importada com sucesso.")
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): ERRO: Módulo 'Inimigos.py' ou classe 'Inimigo' NÃO encontrado. Usando placeholder MAIS COMPLETO.")
    class Inimigo(pygame.sprite.Sprite): # Placeholder MAIS COMPLETO
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.x = x; self.y = y; self.largura = largura; self.altura = altura
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.sprite_path_base = sprite_path 

            if sprite_path: 
                self.image = self._carregar_sprite(sprite_path, (largura, altura))
            else:
                self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (255, 0, 255, 128), (0, 0, largura, altura)) 
            
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
            
            self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128); self.facing_right = True
            self.sprites = [self.image] if self.image else []
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.intervalo_animacao = 200; self.is_attacking = False 
            self.attack_hitbox = pygame.Rect(0,0,0,0); self.hit_by_player_this_attack = False
            self.contact_cooldown = 1000; self.last_contact_time = pygame.time.get_ticks()

        def _carregar_sprite(self, path, tamanho):
            base_dir = os.path.dirname(os.path.abspath(__file__)) 
            game_root_dir = base_dir # Assume que GerenciadorDeInimigos.py está na raiz com Sprites/
            
            full_path = os.path.join(game_root_dir, path.replace("\\", "/"))
            if not os.path.exists(full_path):
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (255,0,255,128), (0,0,tamanho[0],tamanho[1]))
                return img
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.scale(img, tamanho)
                return img
            except pygame.error as e:
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (255,0,255,128), (0,0,tamanho[0],tamanho[1]))
                return img

        def receber_dano(self, dano, fonte_dano_rect=None): 
            self.hp -= dano
            self.last_hit_time = pygame.time.get_ticks()
            self.hp = max(0, self.hp)

        def esta_vivo(self): return self.hp > 0

        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None):
            if self.esta_vivo() and self.velocidade > 0:
                dx = alvo_x - self.rect.centerx
                dy = alvo_y - self.rect.centery
                dist = math.hypot(dx, dy)
                fator_tempo = 1.0 # CORRIGIDO: Valor padrão para fator_tempo
                if dt_ms is not None and dt_ms > 0:
                    fator_tempo = (dt_ms / (1000.0 / 60.0)) 
                
                if dist > 0:
                    mov_x = (dx / dist) * self.velocidade * fator_tempo
                    mov_y = (dy / dist) * self.velocidade * fator_tempo
                    self.rect.x += mov_x
                    self.rect.y += mov_y
                    self.facing_right = dx > 0
        
        def atualizar_animacao(self):
            agora = pygame.time.get_ticks()
            if self.sprites and len(self.sprites) > 1 and self.esta_vivo():
                if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                    self.tempo_ultimo_update_animacao = agora
                    self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            
            if self.sprites and len(self.sprites) > 0:
                idx = int(self.sprite_index % len(self.sprites))
                if idx < len(self.sprites) and isinstance(self.sprites[idx], pygame.Surface):
                    base_image = self.sprites[idx]
                    self.image = pygame.transform.flip(base_image, not self.facing_right, False)
                elif len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface): 
                    self.image = pygame.transform.flip(self.sprites[0], not self.facing_right, False)
                # Se não, self.image mantém o placeholder do __init__ ou o último sprite válido

        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            if self.esta_vivo():
                if hasattr(player, 'rect'):
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
                self.atualizar_animacao()
                
                current_ticks = pygame.time.get_ticks()
                if hasattr(player, 'rect') and hasattr(player, 'vida') and \
                   hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                   self.rect.colliderect(player.rect) and \
                   (current_ticks - self.last_contact_time >= self.contact_cooldown):
                    if hasattr(player, 'receber_dano'):
                        player.receber_dano(self.contact_damage)
                        self.last_contact_time = current_ticks
        
        def desenhar(self, janela, camera_x, camera_y):
            if not hasattr(self, 'image') or self.image is None or not isinstance(self.image, pygame.Surface):
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (255,0,255, 128), (0,0,self.largura,self.altura))
                if not hasattr(self, 'rect'): self.rect = self.image.get_rect(topleft=(self.x,self.y))

            screen_x = self.rect.x - camera_x
            screen_y = self.rect.y - camera_y
            janela.blit(self.image, (screen_x, screen_y))

            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time < self.hit_flash_duration and hasattr(self, 'image') and self.image:
                flash_overlay = self.image.copy()
                flash_overlay.fill(self.hit_flash_color[:3] + (0,), special_flags=pygame.BLEND_RGB_ADD)
                flash_overlay.set_alpha(self.hit_flash_color[3])
                janela.blit(flash_overlay, (screen_x, screen_y))

            if self.hp < self.max_hp and self.hp > 0:
                bar_w = self.largura; bar_h = 5
                health_p = self.hp / self.max_hp
                curr_bar_w = int(bar_w * health_p)
                bar_x = screen_x; bar_y = screen_y - bar_h - 5
                pygame.draw.rect(janela, (255,0,0), (bar_x, bar_y, bar_w, bar_h),0,2)
                pygame.draw.rect(janela, (0,255,0), (bar_x, bar_y, curr_bar_w, bar_h),0,2)
                pygame.draw.rect(janela, (255,255,255), (bar_x, bar_y, bar_w, bar_h),1,2)

# Imports de inimigos (mantidos)
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
                 limite_inimigos: int = 3000, 
                 fator_exponencial_spawn: float = 0.025, 
                 intervalo_spawn_minimo: float = 0.3,
                 atraso_spawn_estacao_seg: float = 0.0): 

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

        self.atraso_configurado_estacao = atraso_spawn_estacao_seg
        self.tempo_fim_atraso_spawn_continuo = 0 
        self.atraso_spawn_continuo_ativo = False

        self.spawn_controller_thread = threading.Thread(
            target=self._spawn_controller_task,
            daemon=True 
        )
        self.spawn_controller_thread.start()
        print("DEBUG(GerenciadorDeInimigos): Gerenciador de Inimigos e Thread de Spawn inicializados.")

    def resetar_temporizador_spawn_estacao(self):
        print(f"DEBUG(GerenciadorDeInimigos): Resetando temporizador de spawn para nova estação.")
        agora = time.time()
        self.tempo_inicio_estacao_para_spawn = agora 
        
        if self.atraso_configurado_estacao > 0:
            self.tempo_fim_atraso_spawn_continuo = agora + self.atraso_configurado_estacao
            self.atraso_spawn_continuo_ativo = True
            print(f"DEBUG(GerenciadorDeInimigos): Atraso de spawn contínuo de {self.atraso_configurado_estacao}s ATIVADO.")
        else:
            self.atraso_spawn_continuo_ativo = False

        self.ultimo_spawn_controlado_pelo_thread = agora 

        while not self.spawn_request_queue.empty():
            try:
                self.spawn_request_queue.get_nowait() 
                self.spawn_request_queue.task_done() 
            except queue.Empty:
                break 
        print("DEBUG(GerenciadorDeInimigos): Fila de pedidos de spawn limpa para nova estação.")


    def _spawn_controller_task(self):
        while not self.stop_spawn_thread_event.is_set(): 
            agora = time.time()

            if self.atraso_spawn_continuo_ativo:
                if agora >= self.tempo_fim_atraso_spawn_continuo:
                    self.atraso_spawn_continuo_ativo = False
                    self.tempo_inicio_estacao_para_spawn = agora 
                    self.ultimo_spawn_controlado_pelo_thread = agora 
                    print(f"DEBUG(GerenciadorDeInimigos): Atraso de spawn da estação concluído. Spawn contínuo habilitado.")
                else:
                    self.stop_spawn_thread_event.wait(timeout=0.1) 
                    continue 
            
            tempo_decorrido_na_estacao_para_calculo_exponencial = agora - self.tempo_inicio_estacao_para_spawn
            
            intervalo_atual = max(
                self.intervalo_spawn_minimo, 
                self.intervalo_spawn_inicial * math.exp(-self.fator_exponencial_spawn * tempo_decorrido_na_estacao_para_calculo_exponencial)
            )
            
            if agora - self.ultimo_spawn_controlado_pelo_thread >= intervalo_atual:
                if len(self.inimigos) < self.limite_inimigos:
                    if self.estacoes and hasattr(self.estacoes, 'nome_estacao'):
                        estacao_atual_nome = self.estacoes.nome_estacao()
                        self.spawn_request_queue.put({"estacao": estacao_atual_nome, "timestamp": agora})
                        self.ultimo_spawn_controlado_pelo_thread = agora 
            
            self.stop_spawn_thread_event.wait(timeout=0.05) 
        print("DEBUG(GerenciadorDeInimigos): Thread de controle de spawn finalizado.")

    def process_spawn_requests(self, jogador, dt_ms=None): 
        try:
            while not self.spawn_request_queue.empty(): 
                if len(self.inimigos) >= self.limite_inimigos:
                    self.spawn_request_queue.get_nowait()
                    self.spawn_request_queue.task_done()
                    continue 

                request_data = self.spawn_request_queue.get_nowait() 
                estacao_nome = request_data.get("estacao")

                if jogador and estacao_nome: 
                    self._spawn_inimigo_especifico_da_estacao(estacao_nome, jogador, dt_ms=dt_ms)

                self.spawn_request_queue.task_done() 
        except queue.Empty:
            pass 
        except Exception as e:
            print(f"DEBUG(GerenciadorDeInimigos): Erro ao processar fila de spawn: {e}")


    def _spawn_inimigo_especifico_da_estacao(self, estacao_nome, jogador, dt_ms=None): 
        est_nome_lower = estacao_nome.lower()
        tipos_disponiveis = [] 

        if est_nome_lower == "inverno":
            if Fantasma: tipos_disponiveis.append('fantasma')
            if BonecoDeNeve: tipos_disponiveis.append('bonecodeneve')
            if Lobo: tipos_disponiveis.append('lobo')
            if Golem_Neve: tipos_disponiveis.append('golem_neve') 
        elif est_nome_lower == "primavera":
            if Planta_Carnivora: tipos_disponiveis.append('planta_carnivora')
            if Mae_Natureza: tipos_disponiveis.append('maenatureza')
            if Espirito_Das_Flores: tipos_disponiveis.append('espiritodasflores')
            if Vampiro: tipos_disponiveis.append('vampiro') 
        elif est_nome_lower == "outono":
            if Espantalho: tipos_disponiveis.append('espantalho')
            if Troll: tipos_disponiveis.append('troll') 
            if Goblin: tipos_disponiveis.append('goblin') 
        elif est_nome_lower == "verão" or est_nome_lower == "verao": 
            if Fenix: tipos_disponiveis.append('fenix')
            if Urso: tipos_disponiveis.append('urso')
            if Demonio: tipos_disponiveis.append('demonio') 

        if not tipos_disponiveis: 
            return

        tipo_escolhido = random.choice(tipos_disponiveis) 
        
        # --- NOVA LÓGICA DE SPAWN NOS LIMITES DA TELA ---
        x, y = 0, 0
        spawn_margin = 50 # Distância fora da tela para spawnar

        # Coordenadas do mundo para as bordas da tela (assumindo que a câmera está centralizada no jogador)
        screen_left_world = jogador.rect.centerx - (self.tela_largura / 2)
        screen_right_world = jogador.rect.centerx + (self.tela_largura / 2)
        screen_top_world = jogador.rect.centery - (self.altura_tela / 2)
        screen_bottom_world = jogador.rect.centery + (self.altura_tela / 2)

        edge = random.choice(["top", "bottom", "left", "right"])

        if edge == "top":
            x = random.uniform(screen_left_world, screen_right_world)
            y = screen_top_world - spawn_margin
        elif edge == "bottom":
            x = random.uniform(screen_left_world, screen_right_world)
            y = screen_bottom_world + spawn_margin
        elif edge == "left":
            x = screen_left_world - spawn_margin
            y = random.uniform(screen_top_world, screen_bottom_world)
        elif edge == "right":
            x = screen_right_world + spawn_margin
            y = random.uniform(screen_top_world, screen_bottom_world)
        
        # print(f"DEBUG: Spawning {tipo_escolhido} at edge '{edge}': ({x:.0f}, {y:.0f})")
        # --- FIM DA NOVA LÓGICA DE SPAWN ---

        self.criar_inimigo_aleatorio(tipo_escolhido, x, y, velocidade=1.0, dt_ms_para_init=dt_ms)


    def adicionar_inimigo(self, inimigo):
        if inimigo:
            self.inimigos.add(inimigo)

    def remover_inimigo(self, inimigo):
        self.inimigos.remove(inimigo) 
        if hasattr(inimigo, 'kill'): 
            inimigo.kill() 


    def criar_inimigo_aleatorio(self, tipo_inimigo_str, x, y, velocidade=1.0, dt_ms_para_init=None): 
        novo_inimigo = None
        mapa_tipos = {
            'fantasma': Fantasma, 'bonecodeneve': BonecoDeNeve,
            'planta_carnivora': Planta_Carnivora, 'espantalho': Espantalho,
            'fenix': Fenix, 'maenatureza': Mae_Natureza,
            'espiritodasflores': Espirito_Das_Flores, 'lobo': Lobo, 'urso': Urso,
            'troll': Troll, 
            'golem_neve': Golem_Neve, 
            'goblin': Goblin, 
            'vampiro': Vampiro, 
            'demonio': Demonio 
        }

        ClasseInimigo = mapa_tipos.get(tipo_inimigo_str.lower())

        if ClasseInimigo is not None:
            try:
                novo_inimigo = ClasseInimigo(x, y, velocidade=velocidade)
            except TypeError as e_construtor:
                try:
                    novo_inimigo = ClasseInimigo(x, y)
                except TypeError as e_construtor_simples:
                    print(f"DEBUG(GerenciadorDeInimigos): Erro de TypeError ao criar {tipo_inimigo_str}: {e_construtor_simples}. "
                          f"Tentativa original: {e_construtor}. Verifique os args do construtor.")
            except Exception as e:
                print(f"DEBUG(GerenciadorDeInimigos): Erro desconhecido ao criar {tipo_inimigo_str}: {e}")
        else:
            print(f"DEBUG(GerenciadorDeInimigos): Classe para tipo '{tipo_inimigo_str}' não encontrada ou não importada.")

        if novo_inimigo:
            self.adicionar_inimigo(novo_inimigo)
        return novo_inimigo

    def spawn_inimigos_iniciais(self, jogador, dt_ms=None): 
        if self.estacoes is None or not hasattr(self.estacoes, 'nome_estacao'):
            print("DEBUG(GerenciadorDeInimigos): Aviso: Objeto Estacoes não disponível para spawn inicial.")
            return

        est_nome = self.estacoes.nome_estacao()
        print(f"DEBUG(GerenciadorDeInimigos): Realizando spawn inicial de {self.spawns_iniciais} inimigos para estação '{est_nome}'.")
        for _ in range(self.spawns_iniciais):
            if len(self.inimigos) < self.limite_inimigos:
                self._spawn_inimigo_especifico_da_estacao(est_nome, jogador, dt_ms=dt_ms)
            else:
                print("DEBUG(GerenciadorDeInimigos): Limite de inimigos atingido durante spawn inicial.")
                break
        # self.ultimo_spawn_controlado_pelo_thread = time.time() # Redundante se resetar_temporizador_spawn_estacao for chamado


    def update_inimigos(self, jogador, dt_ms=None):
        inimigos_para_remover = []
        for inimigo in self.inimigos:
            if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo():
                if hasattr(inimigo, 'update'):
                    try:
                        inimigo.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela, dt_ms)
                    except TypeError: 
                        try:
                            inimigo.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela)
                        except TypeError:
                            try:
                                inimigo.update(jogador, self.projeteis_inimigos)
                            except TypeError:
                                try:
                                    inimigo.update(jogador) 
                                except Exception as e_final:
                                     print(f"DEBUG(GerenciadorInimigos): Erro ao chamar update de {type(inimigo).__name__}: {e_final}. Args não correspondem.")
            else: 
                inimigos_para_remover.append(inimigo)

        for inimigo_removido in inimigos_para_remover:
            self.remover_inimigo(inimigo_removido) 

    def update_projeteis_inimigos(self, jogador, dt_ms=None):
        for projetil in list(self.projeteis_inimigos): 
            if hasattr(projetil, 'update'):
                try:
                    projetil.update(jogador, self.tela_largura, self.altura_tela, dt_ms)
                except TypeError: 
                    try:
                        projetil.update(jogador, self.tela_largura, self.altura_tela)
                    except TypeError: 
                        try:
                            projetil.update(jogador)
                        except Exception as e_final_proj:
                            print(f"DEBUG(GerenciadorInimigos): Erro ao chamar update de projétil {type(projetil).__name__}: {e_final_proj}.")

            deve_remover = False
            if hasattr(projetil, 'alive'):
                if isinstance(projetil.alive, bool) and not projetil.alive:
                    deve_remover = True
                elif callable(projetil.alive) and not projetil.alive(): 
                    deve_remover = True
            elif not self.projeteis_inimigos.has(projetil): 
                continue 

            if deve_remover:
                self.projeteis_inimigos.remove(projetil) 


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
