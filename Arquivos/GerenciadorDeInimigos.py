import pygame
import random
import time
import math
import threading
import queue # Para fila thread-safe
import os

# Tenta importar todas as classes de inimigos de reuniaoInimigos.py
# Este módulo deve ser responsável por importar todas as classes de inimigos
# e defini-las no escopo global para que GerenciadorDeInimigos.py possa acessá-las.
try:
    from reuniaoInimigos import *
except ImportError as e:
    # Em caso de falha na importação de reuniaoInimigos, tenta importar classes individuais.
    # Esta seção é um fallback e deve ser mantida consistente com reuniaoInimigos.py.
    print(f"ALERTA(GerenciadorDeInimigos): Módulo 'reuniaoInimigos.py' NÃO encontrado ou com erro na importação: {e}")
    print("ALERTA(GerenciadorDeInimigos): Tentando importar classes de inimigos individualmente.")
    inimigo_classes_para_importar = [
        "ArvoreMaldita", "Fantasma", "BonecoDeNeve", "Planta_Carnivora", "Espantalho",
        "Fenix", "Mae_Natureza", "Espirito_Das_Flores", "Lobo", "Urso",
        "Troll", "Golem_Neve", "Goblin", "Vampiro", "Demonio", "ProjetilNeve",
        "Maga", # Adicionado: Maga
        "Cavaleiro" # Adicionado: Cavaleiro
    ]
    for cls_name in inimigo_classes_para_importar:
        try:
            # Assume que os arquivos estão em Jogo/Arquivos/Inimigos/
            module_name = f"Inimigos.{cls_name.replace('De', 'De').replace('_d', '_D').replace('_n', '_N').replace('_c', '_C')}"
            # Lidar com casos especiais de nomes de arquivo vs. nomes de classe se necessário
            if cls_name == "BonecoDeNeve": module_name = "Inimigos.BonecoDeNeve"
            elif cls_name == "Mae_Natureza": module_name = "Inimigos.Mae_Natureza"
            elif cls_name == "Espirito_Das_Flores": module_name = "Inimigos.Espirito_Das_Flores"
            elif cls_name == "Golem_Neve": module_name = "Inimigos.Golem_Neve"
            elif cls_name == "Planta_Carnivora": module_name = "Inimigos.Planta_Carnivora"
            elif cls_name == "ArvoreMaldita": module_name = "Inimigos.Arvore_Maldita"
            elif cls_name == "ProjetilNeve": module_name = "Inimigos.Projetil_BolaNeve"
            elif cls_name == "Maga": module_name = "Inimigos.Maga" # Adicionado: Importação específica para Maga
            elif cls_name == "Cavaleiro": module_name = "Inimigos.Cavaleiro" # Adicionado: Importação específica para Cavaleiro


            # Importa dinamicamente a classe
            imported_module = __import__(module_name, fromlist=[cls_name])
            globals()[cls_name] = getattr(imported_module, cls_name, None)
            if globals()[cls_name] is None:
                print(f"ALERTA(GerenciadorDeInimigos): Classe {cls_name} não encontrada em {module_name}. Definindo como None.")
        except (ImportError, AttributeError) as inner_e:
            globals()[cls_name] = None
            print(f"ALERTA(GerenciadorDeInimigos): Falha ao importar {cls_name} de {module_name}: {inner_e}. Definido como None.")

# Garante que a classe base Inimigo seja importada ou definida para evitar erros
try:
    from Inimigos.Inimigos import Inimigo
except ImportError:
    # Se a classe base Inimigo não puder ser importada, define um placeholder.
    # Isso é crucial para que o resto do código que depende de Inimigo não quebre.
    print("ERRO CRÍTICO(GerenciadorDeInimigos): Classe base 'Inimigo' não encontrada. Usando placeholder básico.")
    class Inimigo(pygame.sprite.Sprite): # type: ignore
        def __init__(self, x, y, largura=32, altura=32, vida_maxima=100, velocidade=1, dano_contato=10, xp_value=10, sprite_path=""):
            super().__init__()
            self.x = float(x)
            self.y = float(y)
            self.largura = largura
            self.altura = altura
            self.hp = vida_maxima
            self.max_hp = vida_maxima
            self.velocidade = velocidade
            self.contact_damage = dano_contato
            self.xp_value = xp_value
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((255, 0, 0, 100)) # Placeholder vermelho semi-transparente
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
            self.last_hit_time = 0
            self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 100)
            self.facing_right = True
            self.sprites = [self.image.copy()]
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.intervalo_animacao = 200
            self.contact_cooldown = 1000
            self.last_contact_time = pygame.time.get_ticks() - self.contact_cooldown
            self.moedas_drop = 0 # Adiciona o atributo moedas_drop ao placeholder

        def _carregar_sprite(self, path, tamanho):
            # Implementação de placeholder para carregar sprite
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((255,0,255,100))
            return img

        def receber_dano(self, dano, fonte_dano_rect=None):
            if not self.esta_vivo(): return
            self.hp -= dano
            self.last_hit_time = pygame.time.get_ticks()
            self.hp = max(0, self.hp)

        def esta_vivo(self):
            return self.hp > 0

        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None):
            # Lógica de movimento de placeholder
            pass

        def atualizar_animacao(self):
            # Lógica de animação de placeholder
            pass

        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            # Lógica de atualização de placeholder
            if self.esta_vivo():
                if hasattr(player, 'rect') and player.rect is not None:
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
                self.atualizar_animacao()
                current_ticks = pygame.time.get_ticks()
                if self.rect.colliderect(player.rect) and (current_ticks - self.last_contact_time >= self.contact_cooldown):
                    if hasattr(player, 'receber_dano'):
                        player.receber_dano(self.contact_damage, self.rect)
                        self.last_contact_time = current_ticks

        def desenhar(self, janela, camera_x, camera_y):
            screen_x = self.rect.x - camera_x
            screen_y = self.rect.y - camera_y
            janela.blit(self.image, (screen_x, screen_y))
            if self.hp < self.max_hp and self.hp > 0:
                bar_w, bar_h = self.rect.width, 5
                health_p = self.hp / self.max_hp
                curr_bar_w = int(bar_w * health_p)
                bar_x, bar_y = screen_x, screen_y - bar_h - 5
                pygame.draw.rect(janela, (200,0,0), (bar_x, bar_y, bar_w, bar_h), border_radius=2)
                if curr_bar_w > 0: pygame.draw.rect(janela, (0,200,0), (bar_x, bar_y, curr_bar_w, bar_h), border_radius=2)
                pygame.draw.rect(janela, (220,220,220), (bar_x, bar_y, bar_w, bar_h), 1, border_radius=2)


class GerenciadorDeInimigos:
    def __init__(self, estacoes_obj, tela_largura: int, altura_tela: int,
                     gerenciador_moedas_ref=None, # Parâmetro adicionado
                     intervalo_spawn_inicial: float = 3.0, spawns_iniciais: int = 5,
                     limite_inimigos: int = 5000, fator_exponencial_spawn: float = 0.020,
                     intervalo_spawn_minimo: float = 0.5, atraso_spawn_estacao_seg: float = 2.0):

        self.estacoes = estacoes_obj
        self.inimigos = pygame.sprite.Group()
        self.projeteis_inimigos = pygame.sprite.Group()
        self.grupo_chefe_ativo = pygame.sprite.GroupSingle()
        self.gerenciador_moedas = gerenciador_moedas_ref # Referência armazenada

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

        self.spawn_controller_thread = threading.Thread(target=self._spawn_controller_task, daemon=True)
        self.spawn_controller_thread.start()

        # Mapeamento de nomes de string para classes de inimigos
        self.enemy_class_map = {
            "arvoremaldita": globals().get("ArvoreMaldita"),
            "fantasma": globals().get("Fantasma"),
            "bonecodeneve": globals().get("BonecoDeNeve"),
            "planta_carnivora": globals().get("Planta_Carnivora"),
            "espantalho": globals().get("Espantalho"),
            "fenix": globals().get("Fenix"),
            "maenatureza": globals().get("Mae_Natureza"),
            "espiritodasflores": globals().get("Espirito_Das_Flores"),
            "lobo": globals().get("Lobo"),
            "urso": globals().get("Urso"),
            "troll": globals().get("Troll"),
            "golem_neve": globals().get("Golem_Neve"),
            "goblin": globals().get("Goblin"),
            "vampiro": globals().get("Vampiro"),
            "demonio": globals().get("Demonio"),
            "maga": globals().get("Maga"),  # Adicionado: Maga
            "cavaleiro": globals().get("Cavaleiro") # Adicionado: Cavaleiro
        }
        # Filtra entradas None, caso alguma classe não tenha sido importada
        self.enemy_class_map = {k: v for k, v in self.enemy_class_map.items() if v is not None}


    def pausar_spawn_normal(self, pausar: bool):
        self._spawn_normal_pausado = pausar
        if not pausar:
            self.ultimo_spawn_controlado_pelo_thread = time.time()

    def resetar_temporizador_spawn_estacao(self):
        agora = time.time()
        self.tempo_inicio_estacao_para_spawn = agora
        if self.atraso_configurado_estacao > 0:
            self.tempo_fim_atraso_spawn_continuo = agora + self.atraso_configurado_estacao
            self.atraso_spawn_continuo_ativo = True
        else: self.atraso_spawn_continuo_ativo = False
        self.ultimo_spawn_controlado_pelo_thread = agora
        while not self.spawn_request_queue.empty():
            try: self.spawn_request_queue.get_nowait(); self.spawn_request_queue.task_done()
            except queue.Empty: break

    def _spawn_controller_task(self):
        while not self.stop_spawn_thread_event.is_set():
            agora = time.time()
            if self._spawn_normal_pausado:
                self.stop_spawn_thread_event.wait(timeout=0.2)
                continue

            if self.atraso_spawn_continuo_ativo:
                if agora >= self.tempo_fim_atraso_spawn_continuo:
                    self.atraso_spawn_continuo_ativo = False
                    self.tempo_inicio_estacao_para_spawn = agora
                    self.ultimo_spawn_controlado_pelo_thread = agora
                else:
                    tempo_restante = self.tempo_fim_atraso_spawn_continuo - agora
                    self.stop_spawn_thread_event.wait(timeout=min(0.1, tempo_restante if tempo_restante > 0 else 0.1))
                    continue

            tempo_decorrido = agora - self.tempo_inicio_estacao_para_spawn
            intervalo_atual = max(self.intervalo_spawn_minimo,
                                  self.intervalo_spawn_inicial * math.exp(-self.fator_exponencial_spawn * tempo_decorrido))

            if agora - self.ultimo_spawn_controlado_pelo_thread >= intervalo_atual:
                if len(self.inimigos) < self.limite_inimigos:
                    if self.estacoes and hasattr(self.estacoes, 'nome_estacao_atual'):
                        try:
                            est_nome = self.estacoes.nome_estacao_atual()
                            if est_nome:
                                self.spawn_request_queue.put({"estacao": est_nome, "timestamp": agora})
                                self.ultimo_spawn_controlado_pelo_thread = agora
                        except Exception: pass

            self.stop_spawn_thread_event.wait(timeout=0.05)

    def process_spawn_requests(self, jogador, dt_ms=None):
        try:
            while not self.spawn_request_queue.empty():
                if len(self.inimigos) >= self.limite_inimigos:
                    try: self.spawn_request_queue.get_nowait(); self.spawn_request_queue.task_done()
                    except queue.Empty: break
                    continue
                request = self.spawn_request_queue.get_nowait()
                if jogador and hasattr(jogador, 'rect') and request.get("estacao"):
                    self._spawn_inimigo_especifico_da_estacao(request["estacao"], jogador, dt_ms=dt_ms)
                self.spawn_request_queue.task_done()
        except queue.Empty: pass
        except Exception as e:
            # print(f"ERRO ao processar requisição de spawn: {e}")
            pass

    def _spawn_inimigo_especifico_da_estacao(self, estacao_nome, jogador, dt_ms=None):
        est_nome_lower = estacao_nome.lower()
        
        # Mapeamento de estações para tipos de inimigos (strings de chaves no enemy_class_map)
        mapa_estacao_inimigos = {
            "inverno": ['fantasma', 'bonecodeneve', 'lobo', 'golem_neve'],
            "primavera": ['planta_carnivora', 'maenatureza', 'espiritodasflores'],
            "outono": ['espantalho', 'troll', 'goblin', 'vampiro'],
            "verão": ['urso', 'demonio', 'cavaleiro', 'maga'], # Maga e Cavaleiro adicionados, Fenix removida
            "verao": ['urso', 'demonio', 'cavaleiro', 'maga']  # Adicionado para consistência, se houver variação
        }

        # Filtra os tipos de inimigos disponíveis com base no que realmente foi importado
        tipos_disponiveis = [
            tipo for tipo in mapa_estacao_inimigos.get(est_nome_lower, [])
            if self.enemy_class_map.get(tipo) is not None
        ]
        
        if not tipos_disponiveis:
            # print(f"AVISO: Nenhum tipo de inimigo disponível para spawn na estação '{estacao_nome}'.")
            return
        
        tipo_escolhido = random.choice(tipos_disponiveis)

        x, y = 0.0, 0.0; spawn_margin = 60
        if not (jogador and hasattr(jogador, 'rect') and jogador.rect is not None): return

        cam_cx, cam_cy = jogador.rect.centerx, jogador.rect.centery
        s_left = cam_cx - (self.tela_largura / 2); s_right = cam_cx + (self.tela_largura / 2)
        s_top = cam_cy - (self.altura_tela / 2); s_bottom = cam_cy + (self.altura_tela / 2)
        edge = random.choice(["top", "bottom", "left", "right"])

        if edge == "top": x,y = random.uniform(s_left - spawn_margin, s_right + spawn_margin), s_top - spawn_margin
        elif edge == "bottom": x,y = random.uniform(s_left - spawn_margin, s_right + spawn_margin), s_bottom + spawn_margin
        elif edge == "left": x,y = s_left - spawn_margin, random.uniform(s_top - spawn_margin, s_bottom + spawn_margin)
        elif edge == "right": x,y = s_right + spawn_margin, random.uniform(s_top - spawn_margin, s_bottom + spawn_margin)

        self.criar_inimigo_aleatorio(tipo_escolhido, x, y, velocidade=random.uniform(0.7,1.3), dt_ms_para_init=dt_ms)

    def adicionar_inimigo(self, inimigo):
        if inimigo and isinstance(inimigo, pygame.sprite.Sprite): self.inimigos.add(inimigo)

    def remover_inimigo(self, inimigo):
        if inimigo in self.inimigos: self.inimigos.remove(inimigo)
        if hasattr(inimigo, 'kill') and callable(inimigo.kill): inimigo.kill()

    def criar_inimigo_aleatorio(self, tipo_inimigo_str, x, y, velocidade=1.0, dt_ms_para_init=None):
        novo_inimigo = None
        ClasseInimigo = self.enemy_class_map.get(tipo_inimigo_str.lower())
        if ClasseInimigo:
            try:
                # Tenta instanciar com os parâmetros esperados pela maioria dos inimigos
                novo_inimigo = ClasseInimigo(x=x, y=y, velocidade=velocidade)
            except TypeError as e:
                # Fallback para construtores que esperam apenas x, y ou outros.
                # É fortemente recomendado padronizar os construtores dos inimigos.
                # print(f"AVISO: Construtor de {ClasseInimigo.__name__} não aceitou 'velocidade' ou args nomeados. Tentando com (x, y). Erro: {e}")
                try:
                    novo_inimigo = ClasseInimigo(x, y)
                except Exception as inner_e:
                    # print(f"ERRO: Falha ao instanciar {ClasseInimigo.__name__} com (x, y): {inner_e}")
                    pass
            except Exception as e:
                # print(f"ERRO inesperado ao instanciar {ClasseInimigo.__name__}: {e}")
                pass
        if novo_inimigo: self.adicionar_inimigo(novo_inimigo)
        return novo_inimigo


    def spawn_inimigos_iniciais(self, jogador, dt_ms=None):
        if self._spawn_normal_pausado: return
        if not (self.estacoes and hasattr(self.estacoes, 'nome_estacao_atual')): return
        try:
            est_nome = self.estacoes.nome_estacao_atual()
            if not est_nome: return
        except Exception: return
        for _ in range(self.spawns_iniciais):
            if len(self.inimigos) < self.limite_inimigos:
                self._spawn_inimigo_especifico_da_estacao(est_nome, jogador, dt_ms=dt_ms)
            else: break

    def update_inimigos(self, jogador, dt_ms=None):
        """
        Atualiza todos os inimigos ativos.
        Todas as classes de inimigos devem implementar o método update com a assinatura:
        `update(self, player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)`
        para garantir compatibilidade e evitar erros de TypeError.
        """
        if self._spawn_normal_pausado: return
        remover = []
        for inimigo in list(self.inimigos):
            if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo():
                if hasattr(inimigo, 'update'):
                    try:
                        # Chamada padronizada para o método update dos inimigos
                        inimigo.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela, dt_ms)
                    except TypeError as e:
                        # Loga o erro para depuração, mas tenta chamar com menos argumentos como fallback.
                        # É altamente recomendado corrigir as assinaturas dos métodos update dos inimigos.
                        # print(f"AVISO: TypeError no update de inimigo {type(inimigo).__name__}: {e}. Tentando fallback.")
                        try: inimigo.update(jogador, self.projeteis_inimigos, dt_ms)
                        except TypeError:
                            try: inimigo.update(jogador, dt_ms)
                            except TypeError:
                                try: inimigo.update(jogador)
                                except Exception: pass
            elif hasattr(inimigo, 'esta_vivo') and not inimigo.esta_vivo(): remover.append(inimigo)
        for ini_rem in remover:
            if hasattr(jogador, 'xp_manager') and jogador.xp_manager and \
               hasattr(jogador.xp_manager, 'gain_xp') and callable(jogador.xp_manager.gain_xp) and \
               hasattr(ini_rem, 'xp_value'):
                jogador.xp_manager.gain_xp(ini_rem.xp_value)

            # Adiciona moedas ao jogador se o inimigo tiver o atributo moedas_drop
            if hasattr(ini_rem, 'moedas_drop') and self.gerenciador_moedas and \
               hasattr(self.gerenciador_moedas, 'adicionar_moedas'):
                self.gerenciador_moedas.adicionar_moedas(ini_rem.moedas_drop)

            self.remover_inimigo(ini_rem)

    def update_projeteis_inimigos(self, jogador, dt_ms=None):
        """
        Atualiza todos os projéteis inimigos ativos.
        Todas as classes de projéteis inimigos devem implementar o método update com a assinatura:
        `update(self, player, tela_largura, altura_tela, dt_ms)`
        para garantir compatibilidade e evitar erros de TypeError.
        """
        for proj in list(self.projeteis_inimigos):
            if hasattr(proj, 'update'):
                try:
                    # Chamada padronizada para o método update dos projéteis
                    proj.update(jogador, self.tela_largura, self.altura_tela, dt_ms)
                except TypeError as e:
                    # Loga o erro para depuração, mas tenta chamar com menos argumentos como fallback.
                    # É altamente recomendado corrigir as assinaturas dos métodos update dos projéteis.
                    # print(f"AVISO: TypeError no update de projétil {type(proj).__name__}: {e}. Tentando fallback.")
                    try: proj.update(jogador, dt_ms)
                    except TypeError:
                        try: proj.update(jogador)
                        except Exception: pass
            remover_proj = False
            if hasattr(proj, 'alive'):
                if callable(proj.alive) and not proj.alive(): remover_proj = True
                elif isinstance(proj.alive, bool) and not proj.alive: remover_proj = True
            elif not hasattr(proj, 'rect'): remover_proj = True
            if remover_proj and proj in self.projeteis_inimigos:
                self.projeteis_inimigos.remove(proj)
                if hasattr(proj, 'kill'): proj.kill()

    def desenhar_inimigos(self, janela, camera_x: int, camera_y: int):
        for inimigo in self.inimigos:
            if hasattr(inimigo, 'desenhar'): inimigo.desenhar(janela, camera_x, camera_y)
            elif isinstance(inimigo, pygame.sprite.Sprite) and hasattr(inimigo, 'image') and hasattr(inimigo, 'rect'):
                if inimigo.image and inimigo.rect: janela.blit(inimigo.image, (inimigo.rect.x - camera_x, inimigo.rect.y - camera_y))

    def desenhar_projeteis_inimigos(self, surface, camera_x, camera_y):
        for proj in self.projeteis_inimigos:
            if hasattr(proj, 'desenhar'): proj.desenhar(surface, camera_x, camera_y)
            elif isinstance(proj, pygame.sprite.Sprite) and hasattr(proj, 'image') and hasattr(proj, 'rect'):
                if proj.image and proj.rect: surface.blit(proj.image, (proj.rect.x - camera_x, proj.rect.y - camera_y))

    def get_inimigos_vivos(self): return self.inimigos

    def limpar_todos_inimigos_normais(self):
        for inimigo_obj in list(self.inimigos): self.remover_inimigo(inimigo_obj)
        for proj in list(self.projeteis_inimigos):
            if hasattr(proj, 'kill'): proj.kill()
        self.projeteis_inimigos.empty()

    def spawn_chefe_estacao(self, indice_estacao_chefe, posicao_mundo_spawn):
        self.grupo_chefe_ativo.empty()
        chefe_spawnado = None
        # Mapeamento do índice da estação para o tipo de chefe
        boss_map = {
            0: "ArvoreMaldita", # Primavera
            # Adicione outros chefes aqui para outras estações, ex:
            # 1: "NomeDoChefeVerao",
            # 2: "NomeDoChefeOutono",
            # 3: "NomeDoChefeInverno",
        }
        
        chefe_tipo_str = boss_map.get(indice_estacao_chefe)
        if chefe_tipo_str and self.enemy_class_map.get(chefe_tipo_str.lower()):
            ClasseChefe = self.enemy_class_map[chefe_tipo_str.lower()]
            try:
                # Instancia o chefe e posiciona centralizado
                temp_chefe_for_size = ClasseChefe(0,0) # Cria uma instância temporária para pegar as dimensões
                chefe_x = posicao_mundo_spawn[0] - temp_chefe_for_size.rect.width // 2
                chefe_y = posicao_mundo_spawn[1] - temp_chefe_for_size.rect.height // 2
                chefe_spawnado = ClasseChefe(x=chefe_x, y=chefe_y, velocidade=0.3)
            except Exception as e:
                # print(f"ERRO ao instanciar chefe {chefe_tipo_str}: {e}")
                pass

        if chefe_spawnado: self.grupo_chefe_ativo.add(chefe_spawnado)
        return chefe_spawnado

    def update_chefe(self, jogador, dt_ms=None):
        if self.grupo_chefe_ativo.sprite:
            chefe = self.grupo_chefe_ativo.sprite
            if hasattr(chefe, 'update') and callable(chefe.update):
                try:
                    # Chamada padronizada para o método update do chefe
                    chefe.update(jogador, self.inimigos, self.projeteis_inimigos, self.tela_largura, self.altura_tela, dt_ms)
                except TypeError as e:
                    # Loga o erro para depuração, mas tenta chamar com menos argumentos como fallback.
                    # É altamente recomendado corrigir as assinaturas dos métodos update dos chefes.
                    # print(f"AVISO: TypeError no update do chefe {type(chefe).__name__}: {e}. Tentando fallback.")
                    try: chefe.update(jogador, dt_ms)
                    except TypeError:
                        try: chefe.update(jogador)
                        except Exception: pass

    def desenhar_chefe(self, janela, camera_x, camera_y):
        if self.grupo_chefe_ativo.sprite:
            chefe = self.grupo_chefe_ativo.sprite
            if hasattr(chefe, 'desenhar') and callable(chefe.desenhar):
                chefe.desenhar(janela, camera_x, camera_y)
            elif isinstance(chefe, pygame.sprite.Sprite) and hasattr(chefe, 'image') and hasattr(chefe, 'rect'):
                if chefe.image and chefe.rect:
                    janela.blit(chefe.image, (chefe.rect.x - camera_x, chefe.rect.y - camera_y))

    def limpar_chefe_ativo(self):
        if self.grupo_chefe_ativo.sprite:
            chefe = self.grupo_chefe_ativo.sprite
            if hasattr(chefe, 'kill'): chefe.kill()
            self.grupo_chefe_ativo.empty()

    def stop_threads(self):
        self.stop_spawn_thread_event.set()
        if self.spawn_controller_thread and self.spawn_controller_thread.is_alive():
            self.spawn_controller_thread.join(timeout=0.5)
