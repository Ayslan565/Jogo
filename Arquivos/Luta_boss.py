# Luta_boss.py
import pygame
import time 
import os 
import random 
import sys 
import inspect 

# --- Configurações ---
# Define as dimensões padrão para a arena de batalha do chefe.
DIMENSOES_ARENA_CHEFE = (800, 600) 
# Lista para armazenar os caminhos das músicas de chefe. Será preenchida por 'configurar_musicas_chefe'.
MUSICA_CHEFE_DEFAULT = []

# --- Variáveis de Estado do Módulo ---
# Essas variáveis controlam o estado global da luta contra o chefe no jogo.
_luta_ativa = False  # Flag booleana que indica se uma luta contra chefe está em andamento.
_arena_rect = None  # Objeto pygame.Rect que define os limites da arena da luta.
_chefe_atual = None  # Mantém a instância do objeto do chefe ativo.
_musica_normal_anterior_pos = None  # Armazena a posição (em ms) da música de fundo normal antes da luta.
_musica_normal_anterior_path = None # Armazena o caminho do arquivo da música de fundo normal.

# --- Funções de Gerenciamento da Luta ---

def configurar_musicas_chefe(lista_musicas_chefe_projeto):
    """
    Configura a lista de músicas que podem ser tocadas durante as lutas contra chefes.
    Esta função deve ser chamada uma vez no início do jogo.

    Args:
        lista_musicas_chefe_projeto (list): Uma lista de strings, onde cada string é o caminho para um arquivo de música.
    """
    global MUSICA_CHEFE_DEFAULT
    MUSICA_CHEFE_DEFAULT = lista_musicas_chefe_projeto
    # print(f"DEBUG (Luta_boss.py): Músicas do chefe configuradas: {MUSICA_CHEFE_DEFAULT}")

def iniciar_luta_chefe(jogador, indice_estacao, gerenciador_inimigos, estacoes_obj, tela_largura, tela_altura, musica_atual_path=None, musica_atual_pos_ms=None):
    """
    Inicia a sequência de luta contra o chefe.
    Esta função é o coração do módulo, responsável por:
    - Limpar inimigos normais.
    - Definir a arena de batalha.
    - Spawna o chefe específico da estação.
    - Pausar a música normal e tocar a música do chefe.
    - Pausar o spawn de inimigos normais.

    Args:
        jogador (Player): A instância do jogador.
        indice_estacao (int): O índice da estação atual, para determinar qual chefe spawnar.
        gerenciador_inimigos (GerenciadorDeInimigos): A instância do gerenciador de inimigos.
        estacoes_obj (Estacoes): A instância do gerenciador de estações.
        tela_largura (int): Largura atual da tela.
        tela_altura (int): Altura atual da tela.
        musica_atual_path (str, optional): Caminho da música que estava tocando.
        musica_atual_pos_ms (int, optional): Posição em milissegundos da música que estava tocando.

    Returns:
        bool: True se a luta foi iniciada com sucesso, False caso contrário.
    """
    global _luta_ativa, _arena_rect, _chefe_atual, _musica_normal_anterior_pos, _musica_normal_anterior_path
    
    # Validação inicial dos objetos necessários
    if not jogador or not hasattr(jogador, 'rect'):
        print("ERRO (Luta_boss.py): Jogador inválido para iniciar luta contra chefe.")
        return False
    if not hasattr(jogador, 'x') or not hasattr(jogador, 'y'):
        print("ERRO (Luta_boss.py): Jogador não possui atributos 'x' ou 'y' para definir a arena.")
        if hasattr(jogador, 'rect') and jogador.rect:
            print("AVISO (Luta_boss.py): Usando jogador.rect.center para arena devido à ausência de jogador.x/y.")
            jogador_pos_x_mundo = float(jogador.rect.centerx)
            jogador_pos_y_mundo = float(jogador.rect.centery)
        else:
            _luta_ativa = False 
            return False
    else:
        jogador_pos_x_mundo = float(jogador.x)
        jogador_pos_y_mundo = float(jogador.y)

    print(f"DEBUG (Luta_boss.py): Tentando iniciar luta contra chefe para estação índice {indice_estacao}.")
    _luta_ativa = True # Assume que vai dar certo inicialmente, reverte em caso de erro

    # Limpa os inimigos normais existentes do mapa
    if hasattr(gerenciador_inimigos, 'limpar_todos_inimigos_normais'):
        gerenciador_inimigos.limpar_todos_inimigos_normais()
    else:
        print("AVISO (Luta_boss.py): gerenciador_inimigos não possui 'limpar_todos_inimigos_normais'.")

    # Cria a arena de batalha centralizada no jogador
    try:
        arena_x = jogador_pos_x_mundo - DIMENSOES_ARENA_CHEFE[0] // 2
        arena_y = jogador_pos_y_mundo - DIMENSOES_ARENA_CHEFE[1] // 2
        _arena_rect = pygame.Rect(arena_x, arena_y, DIMENSOES_ARENA_CHEFE[0], DIMENSOES_ARENA_CHEFE[1])
        # print(f"DEBUG (Luta_boss.py): Arena definida em {_arena_rect}")
    except Exception as e:
        print(f"ERRO (Luta_boss.py): Erro ao definir arena: {e}")
        _luta_ativa = False
        return False

    # Spawna o chefe
    if hasattr(gerenciador_inimigos, 'spawn_chefe_estacao'):
        posicao_spawn_chefe = _arena_rect.center
        print(f"DEBUG (Luta_boss.py): Chamando gerenciador_inimigos.spawn_chefe_estacao({indice_estacao}, {posicao_spawn_chefe})")
        chefe_spawnado = gerenciador_inimigos.spawn_chefe_estacao(indice_estacao, posicao_spawn_chefe)
        
        if not chefe_spawnado:
            # A mensagem de erro será impressa pelo código que chama esta função se ela retornar False.
            _luta_ativa = False; _arena_rect = None
            return False # Retorna False explicitamente se o chefe não for spawnado
        
        set_chefe_atual_para_monitoramento(chefe_spawnado)
        print(f"DEBUG (Luta_boss.py): Chefe '{type(_chefe_atual).__name__}' spawnado e definido para monitoramento.")
    else:
        print("ERRO (Luta_boss.py): gerenciador_inimigos não possui 'spawn_chefe_estacao'.")
        _luta_ativa = False; _arena_rect = None
        return False

    # Gerenciamento da música: salva a música atual e toca a do chefe
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        _musica_normal_anterior_pos = musica_atual_pos_ms if musica_atual_pos_ms is not None else pygame.mixer.music.get_pos()
        _musica_normal_anterior_path = musica_atual_path
        pygame.mixer.music.fadeout(1000)
        # print(f"DEBUG (Luta_boss.py): Música normal pausada.")

    if MUSICA_CHEFE_DEFAULT and isinstance(MUSICA_CHEFE_DEFAULT, list) and len(MUSICA_CHEFE_DEFAULT) > 0 and pygame.mixer.get_init():
        valid_tracks = [p for p in MUSICA_CHEFE_DEFAULT if isinstance(p, str) and os.path.exists(p)]
        if valid_tracks:
            selected_track = random.choice(valid_tracks)
            try:
                pygame.mixer.music.load(selected_track)
                pygame.mixer.music.play(-1, fade_ms=1000)
                # print(f"DEBUG (Luta_boss.py): Tocando música do chefe: {selected_track}")
            except pygame.error as e:
                print(f"ERRO (Luta_boss.py): ao carregar/tocar música do chefe '{selected_track}': {e}")
        else:
            print("AVISO (Luta_boss.py): Nenhuma faixa de música de chefe VÁLIDA encontrada.")
    
    # Pausa o spawn de inimigos normais
    if hasattr(gerenciador_inimigos, 'pausar_spawn_normal'):
        gerenciador_inimigos.pausar_spawn_normal(True)
    
    print(f"DEBUG (Luta_boss.py): Luta contra chefe iniciada com sucesso para estação {indice_estacao}.")
    return True


def finalizar_luta_chefe(jogador, estacoes_obj, gerenciador_inimigos):
    """
    Finaliza a luta contra o chefe.
    Esta função é chamada quando o chefe é derrotado. Responsável por:
    - Restaurar a música normal.
    - Conceder XP ao jogador.
    - Limpar as variáveis de estado da luta.
    - Sinalizar ao gerenciador de estações para avançar.
    - Reativar o spawn de inimigos normais.

    Args:
        jogador (Player): A instância do jogador.
        estacoes_obj (Estacoes): A instância do gerenciador de estações.
        gerenciador_inimigos (GerenciadorDeInimigos): A instância do gerenciador de inimigos.
    """
    global _luta_ativa, _arena_rect, _chefe_atual, _musica_normal_anterior_pos, _musica_normal_anterior_path
    # print("DEBUG (Luta_boss.py): Finalizando luta contra chefe.")
    _luta_ativa = False
    _arena_rect = None
    
    # Para a música do chefe e restaura a música anterior
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(1000)
    if _musica_normal_anterior_path and pygame.mixer.get_init() and os.path.exists(_musica_normal_anterior_path):
        try:
            pygame.mixer.music.load(_musica_normal_anterior_path)
            start_pos_sec = _musica_normal_anterior_pos / 1000.0 if _musica_normal_anterior_pos is not None else 0
            pygame.mixer.music.play(-1, start=start_pos_sec, fade_ms=1000)
        except pygame.error as e:
            print(f"ERRO (Luta_boss.py): ao restaurar música normal: {e}")
        except Exception as e_restore:
            print(f"ERRO (Luta_boss.py): inesperado ao restaurar música: {e_restore}")
    
    # Limpa as variáveis de música
    _musica_normal_anterior_path = None
    _musica_normal_anterior_pos = None

    # Concede XP de chefe ao jogador
    if _chefe_atual and hasattr(jogador, 'ganhar_xp_chefe') and hasattr(_chefe_atual, 'xp_value_boss'):
        xp_do_chefe = getattr(_chefe_atual, 'xp_value_boss', 100)
        if hasattr(jogador, 'ganhar_xp_chefe') and callable(jogador.ganhar_xp_chefe):
            jogador.ganhar_xp_chefe(xp_do_chefe)
    
    _chefe_atual = None 
    
    # Permite que o jogo prossiga para a próxima estação
    if hasattr(estacoes_obj, 'confirmar_derrota_chefe_primavera_e_avancar'): 
        estacoes_obj.confirmar_derrota_chefe_primavera_e_avancar() 
    elif hasattr(estacoes_obj, 'confirmar_mudanca_estacao'): 
        estacoes_obj.confirmar_mudanca_estacao()

    # Reativa o spawn de inimigos e reseta os temporizadores
    if hasattr(gerenciador_inimigos, 'pausar_spawn_normal'):
        gerenciador_inimigos.pausar_spawn_normal(False)
    if hasattr(gerenciador_inimigos, 'resetar_temporizador_spawn_estacao'):
        gerenciador_inimigos.resetar_temporizador_spawn_estacao()
    if hasattr(gerenciador_inimigos, 'spawn_inimigos_iniciais') and jogador:
        gerenciador_inimigos.spawn_inimigos_iniciais(jogador)


def atualizar_luta(jogador, estacoes_obj, gerenciador_inimigos):
    """
    Deve ser chamada a cada frame do loop do jogo enquanto a luta estiver ativa.
    Monitora a condição de derrota do chefe.

    Args:
        jogador (Player): A instância do jogador.
        estacoes_obj (Estacoes): A instância do gerenciador de estações.
        gerenciador_inimigos (GerenciadorDeInimigos): A instância do gerenciador de inimigos.

    Returns:
        bool: True se o chefe foi derrotado neste frame, False caso contrário.
    """
    global _chefe_atual 
    if not _luta_ativa:
        return False 

    chefe_derrotado_agora = False
    if _chefe_atual:
        # Verifica se a instância do chefe ainda existe no gerenciador de inimigos
        # ou se sua própria flag de vida indica que foi derrotado.
        chefe_ainda_existe_no_gerenciador = True
        if hasattr(gerenciador_inimigos, 'grupo_chefe_ativo') and hasattr(_chefe_atual, 'alive'):
            # Para sprites do Pygame, 'alive()' é um bom indicador.
            if not _chefe_atual.alive() or _chefe_atual not in gerenciador_inimigos.grupo_chefe_ativo:
                chefe_ainda_existe_no_gerenciador = False
        elif hasattr(_chefe_atual, 'alive') and not _chefe_atual.alive(): 
            chefe_ainda_existe_no_gerenciador = False
        
        # Condição de derrota: ou o método 'esta_vivo' retorna False, ou o sprite foi removido.
        if (hasattr(_chefe_atual, 'esta_vivo') and not _chefe_atual.esta_vivo()) or \
           not chefe_ainda_existe_no_gerenciador:
            # print(f"DEBUG (Luta_boss.py): Chefe '{type(_chefe_atual).__name__}' detectado como derrotado.")
            finalizar_luta_chefe(jogador, estacoes_obj, gerenciador_inimigos)
            chefe_derrotado_agora = True 
    elif _luta_ativa: 
        # Caso de segurança: se a luta está ativa, mas a referência ao chefe foi perdida.
        print("AVISO CRÍTICO (Luta_boss.py): Luta ativa mas _chefe_atual é None. Finalizando luta.")
        finalizar_luta_chefe(jogador, estacoes_obj, gerenciador_inimigos)
        chefe_derrotado_agora = True 

    return chefe_derrotado_agora

# --- Funções de Acesso (Getters/Setters) ---

def esta_luta_ativa():
    """Retorna o estado atual da luta contra o chefe."""
    return _luta_ativa

def get_arena_rect():
    """Retorna o retângulo da arena de batalha."""
    return _arena_rect

def get_chefe_atual():
    """Retorna a instância do chefe atual."""
    return _chefe_atual

def set_chefe_atual_para_monitoramento(instancia_chefe):
    """Define a instância do chefe a ser monitorada. Usado internamente."""
    global _chefe_atual
    _chefe_atual = instancia_chefe

# --- Bloco Principal para Teste (if __name__ == "__main__":) ---
# Este bloco permite executar o arquivo Luta_boss.py diretamente para testar
# sua funcionalidade de forma isolada, usando classes "Mock" (simuladas)
# para representar o jogador, gerenciadores, etc.
if __name__ == "__main__":
    pygame.init() 

    try:
        display_info = pygame.display.Info()
        LARGURA_TELA_TESTE = display_info.current_w - 50 
        ALTURA_TELA_TESTE = display_info.current_h - 100 
        if LARGURA_TELA_TESTE < 800: LARGURA_TELA_TESTE = 800 
        if ALTURA_TELA_TESTE < 600: ALTURA_TELA_TESTE = 600
    except pygame.error:
        LARGURA_TELA_TESTE, ALTURA_TELA_TESTE = 1000, 700
    
    tela_teste = pygame.display.set_mode((LARGURA_TELA_TESTE, ALTURA_TELA_TESTE), pygame.RESIZABLE)
    pygame.display.set_caption("Teste Luta_boss.py - Depuração")

    current_dir_test = os.path.dirname(os.path.abspath(__file__))
    project_root_dir_guess_test = os.path.dirname(current_dir_test) 
    if project_root_dir_guess_test not in sys.path:
        sys.path.insert(0, project_root_dir_guess_test)
    if current_dir_test not in sys.path: 
        sys.path.insert(0, current_dir_test)

    CAMINHO_IMAGEM_CHAO_TESTE_ABS = os.path.join(project_root_dir_guess_test, "Sprites", "Chao", "A1.png")
    primeira_imagem_chefe_fallback_relativa = os.path.join("Sprites", "Inimigos", "Arvore Maldita", "Arvore Maldita1.png")
    CAMINHO_PRIMEIRA_IMAGEM_CHEFE_FALLBACK_ABS = os.path.join(project_root_dir_guess_test, primeira_imagem_chefe_fallback_relativa)

    musicas_chefe_teste_abs = [
        os.path.join(project_root_dir_guess_test, "Musica", "Boss Fight", "Faixa1.mp3"),
        os.path.join(project_root_dir_guess_test, "Musica", "Boss Fight", "Faixa2.mp3")
    ]
    configurar_musicas_chefe(musicas_chefe_teste_abs)

    Player_classe = None
    print("DEBUG (Luta_boss.py Teste): Tentando importar Player original...")
    try:
        from player import Player as PlayerOriginal 
        Player_classe = PlayerOriginal
        print(f"DEBUG (Luta_boss.py Teste): Player original importado: {Player_classe}")
    except Exception as e: print(f"AVISO (Luta_boss.py Teste): Falha ao importar Player original: {e}")

    ArvoreMaldita_classe = None
    print("DEBUG (Luta_boss.py Teste): Tentando importar ArvoreMaldita...")
    try:
        from Inimigos.Arvore_Maldita import ArvoreMaldita 
        ArvoreMaldita_classe = ArvoreMaldita
        print(f"DEBUG (Luta_boss.py Teste): ArvoreMaldita importada: {ArvoreMaldita_classe}")
        if ArvoreMaldita_classe and hasattr(ArvoreMaldita_classe, 'carregar_recursos_arvore_maldita'): 
            print("DEBUG (Luta_boss.py Teste): Tentando carregar recursos da ArvoreMaldita...")
            try:
                ArvoreMaldita_classe.carregar_recursos_arvore_maldita()
                print("DEBUG (Luta_boss.py Teste): Recursos da ArvoreMaldita carregados.")
            except Exception as e_am_recursos:
                print(f"ERRO (Luta_boss.py Teste): Falha ao carregar recursos da ArvoreMaldita: {e_am_recursos}")
                ArvoreMaldita_classe = None # Define como None se recursos falharem
    except ImportError as e_import_am: 
        print(f"AVISO (Luta_boss.py Teste): Falha ao importar ArvoreMaldita (ImportError): {e_import_am}. Chefe da Primavera será Mock.")
        ArvoreMaldita_classe = None # Garante que é None se a importação falhar
    except Exception as e_geral_am:
        print(f"ERRO (Luta_boss.py Teste): Erro inesperado ao lidar com ArvoreMaldita: {e_geral_am}. Chefe da Primavera será Mock.")
        ArvoreMaldita_classe = None # Garante que é None em outros erros

    
    if not pygame.mixer.get_init(): 
        try: pygame.mixer.init()
        except pygame.error as e: print(f"AVISO (Luta_boss.py Teste): Falha ao inicializar mixer: {e}")

    clock = pygame.time.Clock()
    imagem_chao_teste_surf = None
    if os.path.exists(CAMINHO_IMAGEM_CHAO_TESTE_ABS):
        try: imagem_chao_teste_surf = pygame.image.load(CAMINHO_IMAGEM_CHAO_TESTE_ABS).convert()
        except Exception as e: print(f"ERRO (Luta_boss.py Teste): Ao carregar imagem do chão: {e}")

    jogador_teste_obj = None
    if Player_classe:
        try:
            jogador_teste_obj = Player_classe(velocidade=3, vida_maxima=200)
            jogador_teste_obj.x = float(LARGURA_TELA_TESTE // 2)
            jogador_teste_obj.y = float(ALTURA_TELA_TESTE // 2)
            jogador_teste_obj.rect.center = (int(jogador_teste_obj.x), int(jogador_teste_obj.y))
            if not hasattr(jogador_teste_obj, 'rect_colisao'): jogador_teste_obj.rect_colisao = jogador_teste_obj.rect.copy()
            if not hasattr(jogador_teste_obj, 'ganhar_xp_chefe'):
                def _temp_ganhar_xp_chefe_test(self, xp): print(f"Player REAL (teste): Ganhou {xp} XP!")
                Player_classe.ganhar_xp_chefe = _temp_ganhar_xp_chefe_test
            print("DEBUG (Luta_boss.py Teste): Usando Player REAL para teste.")
        except Exception as e: 
            print(f"ERRO (Luta_boss.py Teste): Ao instanciar Player real: {e}. Usando Mock.")
            Player_classe = None 

    if not Player_classe: 
        class MockJogadorTeste(pygame.sprite.Sprite):
            def __init__(self, x, y):
                super().__init__()
                self.image = pygame.Surface((40, 60), pygame.SRCALPHA); self.image.fill((0,150,0,180))
                self.rect = self.image.get_rect(center=(x,y)); self.x = float(x); self.y = float(y)
                self.rect_colisao = self.rect.inflate(-5, -5); self.velocidade = 3
                self.pode_levar_dano = True
            def ganhar_xp_chefe(self, xp): print(f"MockJogadorTeste: Ganhou {xp} XP!")
            def mover(self, teclas, obstaculos):
                dx, dy = 0,0
                if teclas[pygame.K_LEFT]: dx = -self.velocidade
                if teclas[pygame.K_RIGHT]: dx = self.velocidade
                if teclas[pygame.K_UP]: dy = -self.velocidade
                if teclas[pygame.K_DOWN]: dy = self.velocidade
                self.x += dx; self.y += dy
                self.rect.center = (int(self.x), int(self.y))
                self.rect_colisao.center = self.rect.center
            def update(self, *args): pass 
            def receber_dano(self, dano, _origem_dano=None): print(f"MockJogadorTeste: Recebeu {dano} de dano.")
        jogador_teste_obj = MockJogadorTeste(LARGURA_TELA_TESTE // 2, ALTURA_TELA_TESTE // 2)
        print("DEBUG (Luta_boss.py Teste): Usando MockJogadorTeste.")


    class MockChefeFallbackTeste(pygame.sprite.Sprite):
        def __init__(self, x, y, image_path=None):
            super().__init__()
            self.size = (100, 120)
            if image_path and os.path.exists(image_path):
                try:
                    self.original_image = pygame.image.load(image_path).convert_alpha()
                    self.image = pygame.transform.scale(self.original_image, self.size)
                except Exception:
                    self.image = pygame.Surface(self.size, pygame.SRCALPHA); self.image.fill((150,0,0,200))
            else:
                self.image = pygame.Surface(self.size, pygame.SRCALPHA); self.image.fill((150,0,0,200))
            self.rect = self.image.get_rect(center=(x,y)); self.x = float(x); self.y = float(y)
            self.hp = 200; self.max_hp = 200; self.xp_value_boss = 500; self.nome_unico = "ChefeDeTesteFallback"
            self.contact_damage = 15
        def esta_vivo(self): return self.hp > 0
        def receber_dano(self, dano):
            self.hp -= dano; 
            if self.hp <= 0: self.hp = 0; print(f"{self.nome_unico}: Derrotado!"); self.kill()
        def update(self, jogador, dt_ms=0): 
            if self.esta_vivo() and jogador:
                dx = jogador.rect.centerx - self.rect.centerx; dy = jogador.rect.centery - self.rect.centery
                dist = (dx**2 + dy**2)**0.5
                if dist > 5 and dist !=0: self.rect.x += dx/dist * 1; self.rect.y += dy/dist * 1
                self.x = float(self.rect.centerx); self.y = float(self.rect.centery)

    class MockGerenciadorInimigosTeste:
        def __init__(self): self.grupo_chefe_ativo = pygame.sprite.GroupSingle(); self.inimigos = []
        def limpar_todos_inimigos_normais(self): self.inimigos.clear(); self.grupo_chefe_ativo.empty()
        
        def spawn_chefe_estacao(self, indice_estacao, posicao):
            chefe = None
            print(f"DEBUG (MockGerenciadorInimigosTeste): Tentando spawnar chefe para estação {indice_estacao}.")
            if indice_estacao == 0: # Primavera
                if ArvoreMaldita_classe: # Verifica se a classe foi importada e não definida como None
                    print(f"DEBUG (MockGerenciadorInimigosTeste): ArvoreMaldita_classe ({ArvoreMaldita_classe}) encontrada. Tentando instanciar...")
                    try:
                        chefe = ArvoreMaldita_classe(x=posicao[0], y=posicao[1], velocidade=0.3)
                        print(f"DEBUG (MockGerenciadorInimigosTeste): ArvoreMaldita instanciada: {chefe}")
                    except Exception as e_am_spawn: 
                        print(f"ERRO (MockGerenciadorInimigosTeste): Falha ao instanciar ArvoreMaldita real: {e_am_spawn}")
                        chefe = None 
                else:
                    print(f"DEBUG (MockGerenciadorInimigosTeste): ArvoreMaldita_classe é None ou não foi importada para estação 0.")
            
            if not chefe: 
                print(f"DEBUG (MockGerenciadorInimigosTeste): Usando MockChefeFallbackTeste para estação {indice_estacao}.")
                try:
                    chefe = MockChefeFallbackTeste(posicao[0], posicao[1], CAMINHO_PRIMEIRA_IMAGEM_CHEFE_FALLBACK_ABS)
                    print(f"DEBUG (MockGerenciadorInimigosTeste): MockChefeFallbackTeste instanciado: {chefe}")
                except Exception as e_mock_spawn:
                    print(f"ERRO CRÍTICO (MockGerenciadorInimigosTeste): Falha ao instanciar MockChefeFallbackTeste: {e_mock_spawn}")
                    pass 
            
            if chefe: 
                self.grupo_chefe_ativo.add(chefe)
                self.inimigos = [chefe] 
                print(f"DEBUG (MockGerenciadorInimigosTeste): Chefe {type(chefe).__name__} adicionado ao grupo.")
            else:
                print(f"ERRO (MockGerenciadorInimigosTeste): Nenhum chefe (nem real nem fallback) foi instanciado para estação {indice_estacao}.")
            return chefe

        def pausar_spawn_normal(self, pausar): pass
        def resetar_temporizador_spawn_estacao(self): pass
        def spawn_inimigos_iniciais(self, jogador, *args): pass 
        def update_inimigos(self, jogador, dt_ms): 
            if self.grupo_chefe_ativo.sprite and hasattr(self.grupo_chefe_ativo.sprite, 'update'):
                    self.grupo_chefe_ativo.sprite.update(jogador, dt_ms) 
        def update_chefe(self, jogador_ref, dt_ms_ref): 
            chefe_a_atualizar = self.grupo_chefe_ativo.sprite
            if chefe_a_atualizar and hasattr(chefe_a_atualizar, 'update'):
                chefe_a_atualizar.update(jogador_ref, dt_ms_ref)


    class MockEstacoesTeste:
        def __init__(self): self.i = 0; self.nomes_estacoes = ["PrimaveraTeste", "VeraoTeste"]; self.tempo_troca = 15; self.ultimo_tempo_troca = time.time()
        def atualizar(self): 
            if time.time() - self.ultimo_tempo_troca > self.tempo_troca:
                if not esta_luta_ativa(): return "PENDENTE_CHEFE_ESTACAO" 
            return None
        def confirmar_mudanca_estacao(self): self.i = (self.i + 1) % len(self.nomes_estacoes); self.ultimo_tempo_troca = time.time(); print(f"MockEstacoes: Estação mudou para {self.nome_estacao()}")
        def confirmar_derrota_chefe_primavera_e_avancar(self): self.confirmar_mudanca_estacao(); return True 
        def nome_estacao(self): return self.nomes_estacoes[self.i]
        def get_indice_estacao_atual(self): return self.i

    gerenciador_inimigos_teste_obj = MockGerenciadorInimigosTeste()
    estacoes_teste_obj = MockEstacoesTeste()
    grupo_sprites_teste_render = pygame.sprite.Group() 
    if jogador_teste_obj: grupo_sprites_teste_render.add(jogador_teste_obj)

    rodando_teste_loop = True; fonte_debug_teste = pygame.font.Font(None, 28)
    camera_x_teste_mundo, camera_y_teste_mundo = 0,0 

    print("-" * 20 + " INICIANDO TESTE Luta_boss.py " + "-" * 20)
    print("Pressione 'B' para iniciar luta, 'H' para danificar chefe, ESC para sair do TESTE.")

    while rodando_teste_loop:
        dt_ms_teste = clock.tick(60) 
        for event_teste in pygame.event.get():
            if event_teste.type == pygame.QUIT: rodando_teste_loop = False
            if event_teste.type == pygame.KEYDOWN:
                if event_teste.key == pygame.K_ESCAPE: rodando_teste_loop = False
                elif event_teste.key == pygame.K_b and not esta_luta_ativa() and jogador_teste_obj:
                    print("DEBUG (Luta_boss.py Teste): Tecla 'B' pressionada. Tentando iniciar luta...")
                    if iniciar_luta_chefe(jogador_teste_obj, estacoes_teste_obj.get_indice_estacao_atual(), 
                                        gerenciador_inimigos_teste_obj, estacoes_teste_obj, 
                                        LARGURA_TELA_TESTE, ALTURA_TELA_TESTE):
                        print("DEBUG (Luta_boss.py Teste): iniciar_luta_chefe retornou True.")
                        chefe_inst = get_chefe_atual() 
                        if chefe_inst and chefe_inst not in grupo_sprites_teste_render: 
                            grupo_sprites_teste_render.add(chefe_inst) 
                    else:
                        print("ERRO (Luta_boss.py Teste): iniciar_luta_chefe retornou False.")

                elif event_teste.key == pygame.K_h and esta_luta_ativa():
                    chefe_inst_dano = get_chefe_atual()
                    if chefe_inst_dano and hasattr(chefe_inst_dano, 'receber_dano'): 
                        chefe_inst_dano.receber_dano(30) 
            if event_teste.type == pygame.VIDEORESIZE: 
                LARGURA_TELA_TESTE = event_teste.w
                ALTURA_TELA_TESTE = event_teste.h
                tela_teste = pygame.display.set_mode((LARGURA_TELA_TESTE, ALTURA_TELA_TESTE), pygame.RESIZABLE)

        teclas_teste = pygame.key.get_pressed()
        if jogador_teste_obj and hasattr(jogador_teste_obj, 'mover'): 
            jogador_teste_obj.mover(teclas_teste, []) 
        if jogador_teste_obj and hasattr(jogador_teste_obj, 'update'): 
            try:
                sig = inspect.signature(jogador_teste_obj.update)
                params = sig.parameters
                if len(params) == 0: jogador_teste_obj.update()
                elif len(params) == 1 and list(params.keys())[0] != 'self': jogador_teste_obj.update(dt_ms_teste)
                elif len(params) >= 2: jogador_teste_obj.update(dt_ms_teste, teclas_teste)
            except Exception: 
                try: jogador_teste_obj.update() 
                except: pass

        if jogador_teste_obj:
            camera_x_teste_mundo = jogador_teste_obj.x - LARGURA_TELA_TESTE // 2
            camera_y_teste_mundo = jogador_teste_obj.y - ALTURA_TELA_TESTE // 2

        if not esta_luta_ativa(): 
            sinal_est_teste = estacoes_teste_obj.atualizar()
            if sinal_est_teste == "PENDENTE_CHEFE_ESTACAO": 
                if iniciar_luta_chefe(jogador_teste_obj, estacoes_teste_obj.get_indice_estacao_atual(), 
                                      gerenciador_inimigos_teste_obj, estacoes_teste_obj, 
                                      LARGURA_TELA_TESTE, ALTURA_TELA_TESTE):
                    chefe_inst_auto = get_chefe_atual()
                    if chefe_inst_auto and chefe_inst_auto not in grupo_sprites_teste_render:
                        grupo_sprites_teste_render.add(chefe_inst_auto)
        else: 
            chefe_foi_derrotado_frame_atual = atualizar_luta(jogador_teste_obj, estacoes_teste_obj, gerenciador_inimigos_teste_obj)
            arena_teste = get_arena_rect()
            if arena_teste and jogador_teste_obj:
                jogador_teste_obj.rect.clamp_ip(arena_teste)
                jogador_teste_obj.x = float(jogador_teste_obj.rect.centerx) 
                jogador_teste_obj.y = float(jogador_teste_obj.rect.centery)

        if esta_luta_ativa() and gerenciador_inimigos_teste_obj.grupo_chefe_ativo.sprite:
                gerenciador_inimigos_teste_obj.update_chefe(jogador_teste_obj, dt_ms_teste)


        tela_teste.fill((30,30,50)) 
        if imagem_chao_teste_surf: 
            chao_w, chao_h = imagem_chao_teste_surf.get_size()
            if chao_w > 0 and chao_h > 0: 
                for i in range(int(camera_x_teste_mundo // chao_w) -1, int((camera_x_teste_mundo + LARGURA_TELA_TESTE) // chao_w) + 2):
                    for j in range(int(camera_y_teste_mundo // chao_h) -1, int((camera_y_teste_mundo + ALTURA_TELA_TESTE) // chao_h) + 2):
                        tela_teste.blit(imagem_chao_teste_surf, (i * chao_w - camera_x_teste_mundo, j * chao_h - camera_y_teste_mundo))

        if esta_luta_ativa():
            arena_des_teste = get_arena_rect()
            if arena_des_teste: 
                pygame.draw.rect(tela_teste, (200,0,0), arena_des_teste.move(-camera_x_teste_mundo, -camera_y_teste_mundo), 3)

        chefe_render = get_chefe_atual()
        if chefe_render and esta_luta_ativa() and hasattr(chefe_render, 'alive') and chefe_render.alive() and chefe_render not in grupo_sprites_teste_render:
            grupo_sprites_teste_render.add(chefe_render)
        elif chefe_render and hasattr(chefe_render, 'alive') and not chefe_render.alive() and chefe_render in grupo_sprites_teste_render:
            grupo_sprites_teste_render.remove(chefe_render) 
        elif not esta_luta_ativa() and chefe_render in grupo_sprites_teste_render: 
            grupo_sprites_teste_render.remove(chefe_render)

        for sprite in grupo_sprites_teste_render:
            if hasattr(sprite, 'rect') and hasattr(sprite, 'image') and sprite.image:
                    tela_teste.blit(sprite.image, sprite.rect.move(-camera_x_teste_mundo, -camera_y_teste_mundo))
        
        chefe_ativo_teste_ui = get_chefe_atual()
        if chefe_ativo_teste_ui and hasattr(chefe_ativo_teste_ui, 'hp') and hasattr(chefe_ativo_teste_ui, 'max_hp') and esta_luta_ativa(): 
            hp_t = f"Chefe HP: {int(chefe_ativo_teste_ui.hp)}/{int(chefe_ativo_teste_ui.max_hp)}"
            img_hp = fonte_debug_teste.render(hp_t, True, (255,255,255)); tela_teste.blit(img_hp, (10,10))
        
        s_l_t = f"Luta Ativa: {esta_luta_ativa()}"; img_s_l = fonte_debug_teste.render(s_l_t, True, (255,255,255)); tela_teste.blit(img_s_l, (10,40))
        e_a_t = f"Estacao: {estacoes_teste_obj.nome_estacao()}"; img_e_a = fonte_debug_teste.render(e_a_t, True, (255,255,255)); tela_teste.blit(img_e_a, (10,70))
        if jogador_teste_obj:
            p_j_t = f"Jogador:({int(jogador_teste_obj.x)},{int(jogador_teste_obj.y)})"
            img_p_j = fonte_debug_teste.render(p_j_t, True, (255,255,255)); tela_teste.blit(img_p_j, (10,100))

        pygame.display.flip() 
    pygame.quit() 
    print("Luta_boss.py (Teste): Teste finalizado.")
