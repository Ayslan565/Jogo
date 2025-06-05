# GerenciadorDeInimigos.py
import pygame
import random
import time
import math
import threading
import queue # Para fila thread-safe
import os

# Tenta importar todas as classes de inimigos de reuniaoInimigos.py
try:
    from reuniaoInimigos import * # Tenta importar ArvoreMaldita especificamente se não veio do '*' ou se reuniaoInimigos falhou
    if 'ArvoreMaldita' not in globals() or ArvoreMaldita is None:
        try:
            from Inimigos.Arvore_Maldita import ArvoreMaldita
        except ImportError:
            # print("ALERTA(GerenciadorDeInimigos): Classe ArvoreMaldita não encontrada em Inimigos/Arvore_Maldita.py")
            ArvoreMaldita = None
except ImportError:
    # print("ALERTA(GerenciadorDeInimigos): Módulo 'reuniaoInimigos.py' NÃO encontrado ou com erro na importação.")
    # print("ALERTA(GerenciadorDeInimigos): Todos os tipos de inimigos específicos (exceto ArvoreMaldita tentada separadamente) serão None.")
    Fantasma = BonecoDeNeve = Planta_Carnivora = Espantalho = Fenix = None
    Mae_Natureza = Espirito_Das_Flores = Lobo = Urso = None
    ProjetilNeve = None
    Troll = Golem_Neve = Goblin = Vampiro = Demonio = None
    if 'ArvoreMaldita' not in globals(): # Garante que ArvoreMaldita seja None se tudo falhou
        ArvoreMaldita = None


class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
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
        self.sprite_path_base = sprite_path
        self.moedas_drop = getattr(self, 'moedas_drop', 0) # Garante que o atributo exista

        if sprite_path:
            self.image = self._carregar_sprite(sprite_path, (largura, altura))
        else:
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((255, 0, 255, 100))

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.last_hit_time = 0
        self.hit_flash_duration = 150
        self.hit_flash_color = (255, 255, 255, 100)
        self.facing_right = True
        self.sprites = [self.image.copy()] if self.image and isinstance(self.image, pygame.Surface) else []
        self.sprite_index = 0
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
        self.intervalo_animacao = 200
        self.is_attacking = False
        self.attack_hitbox = pygame.Rect(0,0,0,0)
        self.hit_by_player_this_attack = False
        self.contact_cooldown = 1000
        self.last_contact_time = pygame.time.get_ticks() - self.contact_cooldown

    def _carregar_sprite(self, path, tamanho):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root_guess = os.path.dirname(base_dir)

        if os.path.isabs(path) or path.lower().startswith("sprites"):
            full_path = os.path.join(project_root_guess, path.replace("\\", "/"))
        else:
             full_path = os.path.join(base_dir, "Sprites", path.replace("\\", "/"))
             if not os.path.exists(full_path):
                  full_path = os.path.join(base_dir, path.replace("\\", "/"))


        if not os.path.exists(full_path):
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((255,0,255,100))
            return img
        try:
            img = pygame.image.load(full_path).convert_alpha()
            img = pygame.transform.scale(img, tamanho)
            return img
        except pygame.error:
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
        if self.esta_vivo() and self.velocidade > 0:
            dx = alvo_x - self.rect.centerx
            dy = alvo_y - self.rect.centery
            dist = math.hypot(dx, dy)

            fator_tempo = 1.0
            if dt_ms is not None and dt_ms > 0:
                fator_tempo = (dt_ms / (1000.0 / 60.0))

            if dist > self.velocidade * fator_tempo:
                mov_x = (dx / dist) * self.velocidade * fator_tempo
                mov_y = (dy / dist) * self.velocidade * fator_tempo
                self.rect.x += mov_x
                self.rect.y += mov_y
                self.x = float(self.rect.x)
                self.y = float(self.rect.y)
                if abs(dx) > 0.1: self.facing_right = dx > 0
            elif dist > 0 :
                 self.rect.centerx = round(alvo_x)
                 self.rect.centery = round(alvo_y)
                 self.x = float(self.rect.x)
                 self.y = float(self.rect.y)

    def atualizar_animacao(self):
        agora = pygame.time.get_ticks()
        if self.sprites and len(self.sprites) > 1 and self.esta_vivo():
            if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                self.tempo_ultimo_update_animacao = agora
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)

        if self.sprites and len(self.sprites) > 0:
            idx = int(self.sprite_index % len(self.sprites))
            if idx < len(self.sprites) and self.sprites[idx] and isinstance(self.sprites[idx], pygame.Surface):
                base_image = self.sprites[idx].copy()
                self.image = pygame.transform.flip(base_image, not self.facing_right, False)
            elif not (hasattr(self, 'image') and self.image and isinstance(self.image, pygame.Surface)):
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA); self.image.fill((255,0,255, 50))

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if self.esta_vivo():
            if hasattr(player, 'rect') and player.rect is not None:
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
            self.atualizar_animacao()

            current_ticks = pygame.time.get_ticks()
            player_valido_para_contato = (
                player and hasattr(player, 'rect') and player.rect is not None and
                hasattr(player, 'esta_vivo') and callable(player.esta_vivo) and player.esta_vivo() and
                hasattr(player, 'receber_dano') and callable(player.receber_dano)
            )
            if player_valido_para_contato and \
               self.rect.colliderect(player.rect) and \
               (current_ticks - self.last_contact_time >= self.contact_cooldown):
                player.receber_dano(self.contact_damage, self.rect)
                self.last_contact_time = current_ticks

    def desenhar(self, janela, camera_x, camera_y):
        if not (hasattr(self, 'image') and self.image and isinstance(self.image, pygame.Surface)):
            largura_img = getattr(self, 'largura', 32); altura_img = getattr(self, 'altura', 32)
            self.image = pygame.Surface((largura_img, altura_img), pygame.SRCALPHA)
            self.image.fill((255,0,255, 100))
        if not (hasattr(self, 'rect') and isinstance(self.rect, pygame.Rect)):
            self.rect = self.image.get_rect(topleft=(getattr(self, 'x',0), getattr(self, 'y',0)))

        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y - camera_y
        janela.blit(self.image, (screen_x, screen_y))

        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time < self.hit_flash_duration:
            flash_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            flash_surface.fill(self.hit_flash_color)
            janela.blit(flash_surface, (screen_x, screen_y), special_flags=pygame.BLEND_RGBA_ADD)

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
                 limite_inimigos: int = 25, fator_exponencial_spawn: float = 0.020,
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
        except Exception:
            pass

    def _spawn_inimigo_especifico_da_estacao(self, estacao_nome, jogador, dt_ms=None):
        est_nome_lower = estacao_nome.lower()
        tipos_disponiveis = []
        mapa_estacao_inimigos = {
            "inverno": ['fantasma', 'bonecodeneve', 'lobo', 'golem_neve'],
            "primavera": ['planta_carnivora', 'maenatureza', 'espiritodasflores', ],
            "outono": ['espantalho', 'troll', 'goblin','vampiro'],
            "verão": ['fenix', 'urso', 'demonio'],
            "verao": ['fenix', 'urso', 'demonio']
        }
        if est_nome_lower in mapa_estacao_inimigos:
            for tipo_str in mapa_estacao_inimigos[est_nome_lower]:
                nome_classe = tipo_str.capitalize().replace("_d", "_D").replace("_n", "_N").replace("_c", "_C")
                if nome_classe == "Bonecodeneve": nome_classe = "BonecoDeNeve"
                if nome_classe == "Maenatureza": nome_classe = "Mae_Natureza"
                if nome_classe == "Espiritodasflores": nome_classe = "Espirito_Das_Flores"
                if nome_classe == "Golem_neve": nome_classe = "Golem_Neve"

                if nome_classe in globals() and globals()[nome_classe] is not None:
                    tipos_disponiveis.append(tipo_str)

        if not tipos_disponiveis: return
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
        novo_inimigo = None; mapa_tipos = {}
        nomes_classes_map = {
            'fantasma': 'Fantasma', 'bonecodeneve': 'BonecoDeNeve', 'planta_carnivora': 'Planta_Carnivora',
            'espantalho': 'Espantalho', 'fenix': 'Fenix', 'maenatureza': 'Mae_Natureza',
            'espiritodasflores': 'Espirito_Das_Flores', 'lobo': 'Lobo', 'urso': 'Urso', 'troll': 'Troll',
            'golem_neve': 'Golem_Neve', 'goblin': 'Goblin', 'vampiro': 'Vampiro', 'demonio': 'Demonio'
        }
        for str_mapa, nome_classe_str in nomes_classes_map.items():
            if nome_classe_str in globals() and globals()[nome_classe_str] is not None:
                mapa_tipos[str_mapa] = globals()[nome_classe_str]

        ClasseInimigo = mapa_tipos.get(tipo_inimigo_str.lower())
        if ClasseInimigo:
            try: novo_inimigo = ClasseInimigo(x=x, y=y, velocidade=velocidade)
            except TypeError:
                try: novo_inimigo = ClasseInimigo(x, y)
                except Exception: pass
            except Exception: pass
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
        if self._spawn_normal_pausado: return
        remover = []
        for inimigo in list(self.inimigos):
            if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo():
                if hasattr(inimigo, 'update'):
                    try: inimigo.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela, dt_ms)
                    except TypeError:
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
        for proj in list(self.projeteis_inimigos):
            if hasattr(proj, 'update'):
                try: proj.update(jogador, self.tela_largura, self.altura_tela, dt_ms)
                except TypeError:
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
        if indice_estacao_chefe == 0: # Primavera -> ArvoreMaldita
            if ArvoreMaldita is not None:
                try:
                    temp_arvore = ArvoreMaldita(0,0)
                    chefe_x = posicao_mundo_spawn[0] - temp_arvore.rect.width // 2
                    chefe_y = posicao_mundo_spawn[1] - temp_arvore.rect.height // 2
                    chefe_spawnado = ArvoreMaldita(x=chefe_x, y=chefe_y, velocidade=0.3)
                except Exception:
                    pass
        if chefe_spawnado: self.grupo_chefe_ativo.add(chefe_spawnado)
        return chefe_spawnado

    def update_chefe(self, jogador, dt_ms=None):
        if self.grupo_chefe_ativo.sprite:
            chefe = self.grupo_chefe_ativo.sprite
            if hasattr(chefe, 'update') and callable(chefe.update):
                try:
                    chefe.update(jogador, self.inimigos, self.projeteis_inimigos, self.tela_largura, self.altura_tela, dt_ms)
                except TypeError:
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
