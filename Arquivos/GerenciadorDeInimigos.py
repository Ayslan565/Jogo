# GerenciadorDeInimigos.py
import pygame
import random
import time
import math # Importa math para a função hypot e exp
import os # Importa os para verificar a existência de arquivos

# Importa a classe base Inimigo do ficheiro Inimigos.py
try:
    from Inimigos import Inimigo
    print("DEBUG(GerenciadorDeInimigos): Classe base Inimigo importada com sucesso.")
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): ERRO: Módulo 'Inimigos.py' ou classe 'Inimigo' NÃO encontrado. Usando classe base Inimigo placeholder para evitar crash.")
    class Inimigo(pygame.sprite.Sprite): # Placeholder
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.x = x
            self.y = y
            self.largura = largura
            self.altura = altura
            self.hp = vida_maxima
            self.max_hp = vida_maxima
            self.velocidade = velocidade
            self.contact_damage = dano_contato
            self.xp_value = xp_value
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 255), (0, 0, largura, altura)) 
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
            self.last_hit_time = 0
            self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128) 
            self.facing_right = True
            self.sprites = [self.image]
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.intervalo_animacao = 200
            self.is_attacking = False
            self.attack_hitbox = pygame.Rect(0,0,0,0)
            self.hit_by_player_this_attack = False
            self.contact_cooldown = 1000
            self.last_contact_time = pygame.time.get_ticks()

        def _carregar_sprite(self, path, tamanho):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            game_dir = os.path.dirname(base_dir)
            full_path = os.path.join(game_dir, path.replace("/", os.sep))
            if not os.path.exists(full_path):
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (255,0,255), (0,0,tamanho[0],tamanho[1]))
                return img
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.scale(img, tamanho)
                return img
            except pygame.error:
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (255,0,255), (0,0,tamanho[0],tamanho[1]))
                return img

        def receber_dano(self, dano):
            self.hp -= dano
            self.last_hit_time = pygame.time.get_ticks()
            if self.hp <= 0:
                self.hp = 0

        def esta_vivo(self):
            return self.hp > 0

        def mover_em_direcao(self, alvo_x, alvo_y):
            if self.esta_vivo() and self.velocidade > 0:
                dx = alvo_x - self.rect.centerx
                dy = alvo_y - self.rect.centery
                dist = math.hypot(dx, dy)
                if dist > 0:
                    dx_norm = dx / dist
                    dy_norm = dy / dist
                    self.rect.x += dx_norm * self.velocidade
                    self.rect.y += dy_norm * self.velocidade
                    if dx > 0: self.facing_right = True
                    elif dx < 0: self.facing_right = False
        
        def atualizar_animacao(self):
            agora = pygame.time.get_ticks()
            if self.sprites and len(self.sprites) > 1 and self.esta_vivo():
                if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                    self.tempo_ultimo_update_animacao = agora
                    self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            if self.sprites:
                idx = int(self.sprite_index % len(self.sprites)) if len(self.sprites) > 0 else 0
                if idx < len(self.sprites):
                    base_image = self.sprites[idx]
                    if hasattr(self, 'facing_right') and not self.facing_right:
                        self.image = pygame.transform.flip(base_image, True, False)
                    else:
                        self.image = base_image
                elif len(self.sprites) > 0:
                     self.image = self.sprites[0]
            elif not hasattr(self, 'image') or self.image is None:
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (255,0,255), (0,0,self.largura,self.altura))

        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None):
            if self.esta_vivo():
                if hasattr(player, 'rect'):
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery)
                self.atualizar_animacao()
                current_ticks = pygame.time.get_ticks()
                if hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo():
                    if self.rect.colliderect(player.rect):
                        if (current_ticks - self.last_contact_time >= self.contact_cooldown):
                            if hasattr(player, 'receber_dano'):
                                player.receber_dano(self.contact_damage)
                                self.last_contact_time = current_ticks

        def desenhar(self, janela, camera_x, camera_y):
            if not hasattr(self, 'image') or self.image is None:
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (255,0,255), (0,0,self.largura,self.altura))
                if not hasattr(self, 'rect'):
                     self.rect = self.image.get_rect(topleft=(self.x,self.y))
            screen_x = self.rect.x - camera_x
            screen_y = self.rect.y - camera_y
            janela.blit(self.image, (screen_x, screen_y))
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time < self.hit_flash_duration:
                flash_surface = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                flash_surface.fill(self.hit_flash_color)
                janela.blit(flash_surface, (screen_x, screen_y))
            if self.hp < self.max_hp and self.hp > 0:
                bar_width = self.largura
                bar_height = 5
                health_percentage = self.hp / self.max_hp
                current_bar_width = int(bar_width * health_percentage)
                bar_x = screen_x
                bar_y = screen_y - bar_height - 5 
                pygame.draw.rect(janela, (255,0,0), (bar_x,bar_y,bar_width,bar_height), border_radius=2)
                pygame.draw.rect(janela, (0,255,0), (bar_x,bar_y,current_bar_width,bar_height), border_radius=2)
                pygame.draw.rect(janela, (255,255,255), (bar_x,bar_y,bar_width,bar_height), 1, border_radius=2)

# Importa as classes de inimigos específicas
try:
    from Fantasma import Fantasma
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Fantasma.py' ou classe 'Fantasma' não encontrado.")
    Fantasma = None
try:
    from BonecoDeNeve import BonecoDeNeve
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'BonecoDeNeve.py' ou classe 'BonecoDeNeve' não encontrado.")
    BonecoDeNeve = None
try:
    from Planta_Carnivora import Planta_Carnivora
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Planta_Carnivora.py' ou classe 'Planta_Carnivora' não encontrado.")
    Planta_Carnivora = None
try:
    from Espantalho import Espantalho
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Espantalho.py' ou classe 'Espantalho' não encontrado.")
    Espantalho = None
try:
    from Fenix import Fenix
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Fenix.py' ou classe 'Fenix' não encontrado.")
    Fenix = None
try:
    from Mae_Natureza import Mae_Natureza
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Mae_Natureza.py' ou classe 'Mae_Natureza' não encontrado.")
    Mae_Natureza = None
try:
    from Espirito_Das_Flores import Espirito_Das_Flores
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Espirito_Das_Flores.py' ou classe 'Espirito_Das_Flores' não encontrado.")
    Espirito_Das_Flores = None
try:
    from Lobo import Lobo 
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Lobo.py' ou classe 'Lobo' não encontrado.")
    Lobo = None
try:
    from Urso import Urso # IMPORTANDO A NOVA CLASSE URSO
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Urso.py' ou classe 'Urso' não encontrado.")
    Urso = None
try:
    from Projetil_BolaNeve import ProjetilNeve
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Projetil_BolaNeve.py' ou classe 'ProjetilNeve' não encontrado.")
    ProjetilNeve = None


class GerenciadorDeInimigos:
    def __init__(self, estacoes_obj, tela_largura: int, altura_tela: int, intervalo_spawn_inicial: float = 3.0, spawns_iniciais: int = 5, limite_inimigos: int = 150, fator_exponencial_spawn: float = 0.02, intervalo_spawn_minimo: float = 0.5):
        self.estacoes = estacoes_obj
        self.inimigos = [] 
        self.projeteis_inimigos = [] 
        self.ultimo_spawn = time.time() 
        self.intervalo_spawn_inicial = intervalo_spawn_inicial 
        self.spawns_iniciais = spawns_iniciais 
        self.limite_inimigos = limite_inimigos 
        self.tempo_inicial_jogo = time.time() 
        self.fator_exponencial_spawn = fator_exponencial_spawn 
        self.intervalo_spawn_minimo = intervalo_spawn_minimo 
        self.tela_largura = tela_largura
        self.altura_tela = altura_tela
        print("DEBUG(GerenciadorDeInimigos): Gerenciador de Inimigos inicializado.")

    def adicionar_inimigo(self, inimigo):
        self.inimigos.append(inimigo)

    def remover_inimigo(self, inimigo):
        if inimigo in self.inimigos:
            self.inimigos.remove(inimigo)

    def criar_inimigo_aleatorio(self, tipo_inimigo, x, y, velocidade=1.0):
        novo_inimigo = None
        if tipo_inimigo.lower() == 'fantasma' and Fantasma is not None:
            novo_inimigo = Fantasma(x, y, velocidade=velocidade)
        elif tipo_inimigo.lower() == 'bonecodeneve' and BonecoDeNeve is not None:
            novo_inimigo = BonecoDeNeve(x, y, velocidade=velocidade)
        elif tipo_inimigo.lower() == 'planta_carnivora' and Planta_Carnivora is not None:
            novo_inimigo = Planta_Carnivora(x, y, velocidade=velocidade)
        elif tipo_inimigo.lower() == 'espantalho' and Espantalho is not None:
            novo_inimigo = Espantalho(x, y, velocidade=velocidade)
        elif tipo_inimigo.lower() == 'fenix' and Fenix is not None:
            novo_inimigo = Fenix(x, y, velocidade=velocidade)
        elif tipo_inimigo.lower() == 'maenatureza' and Mae_Natureza is not None:
            novo_inimigo = Mae_Natureza(x, y, velocidade=velocidade)
        elif tipo_inimigo.lower() == 'espiritodasflores' and Espirito_Das_Flores is not None:
            novo_inimigo = Espirito_Das_Flores(x, y, velocidade=velocidade)
        elif tipo_inimigo.lower() == 'lobo' and Lobo is not None: 
            novo_inimigo = Lobo(x, y, velocidade=velocidade)
        elif tipo_inimigo.lower() == 'urso' and Urso is not None: # ADICIONADO CASO PARA URSO
            novo_inimigo = Urso(x, y, velocidade=velocidade)
        else:
            print(f"DEBUG(GerenciadorDeInimigos): Tipo de inimigo desconhecido ou classe não importada: {tipo_inimigo}")

        if novo_inimigo:
            self.adicionar_inimigo(novo_inimigo)
        return novo_inimigo

    def spawn_inimigos(self, jogador):
        if self.estacoes is None or not hasattr(self.estacoes, 'nome_estacao'):
            print("DEBUG(GerenciadorDeInimigos): Aviso: Objeto Estacoes não disponível. Não foi possível spawnar inimigos.")
            return

        est_nome = self.estacoes.nome_estacao().lower()
        tipos_disponiveis = []

        if est_nome == "inverno":
            if Fantasma: tipos_disponiveis.append('fantasma')
            if BonecoDeNeve: tipos_disponiveis.append('bonecodeneve')
            if Lobo: tipos_disponiveis.append('lobo') 
        elif est_nome == "primavera":
            if Planta_Carnivora: tipos_disponiveis.append('planta_carnivora')
            if Mae_Natureza: tipos_disponiveis.append('maenatureza')
            if Espirito_Das_Flores: tipos_disponiveis.append('espiritodasflores')
            # Lobo não spawna na primavera por padrão
        elif est_nome == "outono":
            if Espantalho: tipos_disponiveis.append('espantalho')
            # Lobo não spawna no outono por padrão
        elif est_nome == "verão":
            if Fenix: tipos_disponiveis.append('fenix')
            if Urso: tipos_disponiveis.append('urso') 
        

        if tipos_disponiveis and len(self.inimigos) < self.limite_inimigos:
            num_to_spawn = min(self.spawns_iniciais, self.limite_inimigos - len(self.inimigos))
            print(f"DEBUG(GerenciadorDeInimigos): Tentando spawnar {num_to_spawn} inimigos para '{est_nome}'. Tipos: {tipos_disponiveis}")
            for _ in range(num_to_spawn):
                if not tipos_disponiveis: break 
                tipo = random.choice(tipos_disponiveis)
                spawn_distance = random.randint(400, 700) 
                angle = random.uniform(0, 2 * math.pi)
                if hasattr(jogador, 'rect'):
                    x = jogador.rect.centerx + spawn_distance * math.cos(angle)
                    y = jogador.rect.centery + spawn_distance * math.sin(angle)
                    self.criar_inimigo_aleatorio(tipo, x, y)
                else:
                    print("DEBUG(GerenciadorDeInimigos): Jogador sem 'rect' no spawn_inimigos.")
        elif not tipos_disponiveis:
            print(f"DEBUG(GerenciadorDeInimigos): Nenhum tipo de inimigo disponível para spawn inicial na estação '{est_nome}'.")

    def tentar_spawnar(self, jogador):
        agora = time.time()
        tempo_decorrido = agora - self.tempo_inicial_jogo
        intervalo_atual = max(self.intervalo_spawn_minimo, self.intervalo_spawn_inicial * math.exp(-self.fator_exponencial_spawn * tempo_decorrido))

        if agora - self.ultimo_spawn >= intervalo_atual and len(self.inimigos) < self.limite_inimigos:
            if self.estacoes is not None and hasattr(self.estacoes, 'nome_estacao'):
                self.spawn_inimigo_periodico(self.estacoes.nome_estacao(), jogador)
                self.ultimo_spawn = agora
            else:
                print("DEBUG(GerenciadorDeInimigos): Objeto Estacoes não disponível para spawn periódico.")

    def spawn_inimigo_periodico(self, estacao_nome, jogador):
        est_nome = estacao_nome.lower()
        tipos_disponiveis = []
        
        if est_nome == "inverno":
            if Fantasma: tipos_disponiveis.append('fantasma')
            if BonecoDeNeve: tipos_disponiveis.append('bonecodeneve')
            if Lobo: tipos_disponiveis.append('lobo') 
        elif est_nome == "primavera":
            if Planta_Carnivora: tipos_disponiveis.append('planta_carnivora')
            if Mae_Natureza: tipos_disponiveis.append('maenatureza')
            if Espirito_Das_Flores: tipos_disponiveis.append('espiritodasflores')
        elif est_nome == "outono":
            if Espantalho: tipos_disponiveis.append('espantalho')
        elif est_nome == "verão":
            if Fenix: tipos_disponiveis.append('fenix')
            if Urso: tipos_disponiveis.append('urso') 
        

        if tipos_disponiveis and len(self.inimigos) < self.limite_inimigos:
            tipo = random.choice(tipos_disponiveis)
            spawn_distance = random.randint(400, 700)
            angle = random.uniform(0, 2 * math.pi)
            if hasattr(jogador, 'rect'):
                x = jogador.rect.centerx + spawn_distance * math.cos(angle)
                y = jogador.rect.centery + spawn_distance * math.sin(angle)
                self.criar_inimigo_aleatorio(tipo, x, y)
            else:
                 print("DEBUG(GerenciadorDeInimigos): Jogador sem 'rect' no spawn_inimigo_periodico.")
        elif not tipos_disponiveis:
            print(f"DEBUG(GerenciadorDeInimigos): Nenhum tipo de inimigo para spawn periódico na estação '{est_nome}'.")

    def update_inimigos(self, jogador):
        inimigos_para_remover = []
        for inimigo in self.inimigos:
            if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo():
                if hasattr(inimigo, 'update'):
                    inimigo.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela)
                else:
                    print(f"DEBUG(GerenciadorDeInimigos): Inimigo {type(inimigo).__name__} sem método 'update'.")
            else: 
                if hasattr(jogador, 'xp_manager') and jogador.xp_manager is not None and hasattr(inimigo, 'xp_value'):
                    if hasattr(jogador.xp_manager, 'ganhar_xp') and callable(getattr(jogador.xp_manager, 'ganhar_xp')):
                        print(f"DEBUG(GerenciadorDeInimigos): Concedendo {inimigo.xp_value} XP pela derrota de {type(inimigo).__name__}")
                        jogador.xp_manager.ganhar_xp(inimigo.xp_value)
                    else:
                        print(f"DEBUG(GerenciadorDeInimigos): ERRO: jogador.xp_manager ({type(jogador.xp_manager).__name__}) não possui o método 'ganhar_xp'. XP não concedido por {type(inimigo).__name__}.")
                else:
                    if not hasattr(jogador, 'xp_manager') or jogador.xp_manager is None:
                        print(f"DEBUG(GerenciadorDeInimigos): Jogador sem xp_manager, XP não concedido por {type(inimigo).__name__}")
                    if not hasattr(inimigo, 'xp_value'):
                         print(f"DEBUG(GerenciadorDeInimigos): Inimigo {type(inimigo).__name__} sem xp_value, XP não concedido.")

                inimigos_para_remover.append(inimigo)
        
        for inimigo in inimigos_para_remover:
            self.remover_inimigo(inimigo)
            print(f"DEBUG(GerenciadorDeInimigos): Inimigo {type(inimigo).__name__} removido por não estar vivo.")


    def update_projeteis_inimigos(self, jogador):
        projeteis_ativos = []
        for projetil in list(self.projeteis_inimigos): 
            if hasattr(projetil, 'update'):
                projetil.update(jogador, self.tela_largura, self.altura_tela)
                
                if hasattr(projetil, 'alive') and projetil.alive: 
                    projeteis_ativos.append(projetil)
                elif not hasattr(projetil, 'alive'): 
                     print(f"DEBUG(GerenciadorDeInimigos): Projétil {type(projetil).__name__} sem atributo 'alive'. Removendo por precaução.")
            else:
                print(f"DEBUG(GerenciadorDeInimigos): Objeto na lista de projéteis ({type(projetil).__name__}) não tem método 'update'. Removido.")
        self.projeteis_inimigos = projeteis_ativos

    def desenhar_inimigos(self, janela, camera_x: int, camera_y: int):
        for inimigo in self.inimigos: 
            if hasattr(inimigo, 'desenhar'):
                inimigo.desenhar(janela, camera_x, camera_y)
            else:
                print(f"DEBUG(GerenciadorDeInimigos): Inimigo {type(inimigo).__name__} sem método 'desenhar'.")

    def desenhar_projeteis_inimigos(self, surface, camera_x, camera_y):
        for projetil in self.projeteis_inimigos: 
            if hasattr(projetil, 'desenhar'):
                projetil.desenhar(surface, camera_x, camera_y)

    def get_inimigos_vivos(self):
        return list(self.inimigos)

    def limpar_inimigos(self):
        self.inimigos.clear()
        self.projeteis_inimigos.clear()
        print("DEBUG(GerenciadorDeInimigos): Todos os inimigos e projéteis limpos.")

