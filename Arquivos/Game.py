import pygame
import random
import sys
import os
# import tkinter as tk # Não é mais necessário

# --- Configuração do sys.path ---
# Garante que os módulos locais e do projeto possam ser importados corretamente.
current_dir = os.path.dirname(os.path.abspath(__file__))
arquivos_dir = current_dir # Assume que 'main.py' está na pasta 'Arquivos'
if arquivos_dir not in sys.path:
    sys.path.append(arquivos_dir)

project_root_dir = os.path.dirname(current_dir) # Assume que 'Arquivos' é uma subpasta do projeto
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir) 
    print(f"DEBUG(Game Path): Adicionado ao sys.path (raiz do projeto): {project_root_dir}")

# --- Pré-definição de Nomes Globais como Fallback ---
# Inicializa nomes de classes/módulos como None. Serão preenchidos pelas importações.
Player, PauseMenuManager, XPManager, Menu, GerenciadorDeInimigos, Estacoes, Grama, Arvore, Timer, shop_elements, run_death_screen, loja_core, Vida, BarraInventario, ItemInventario = (None,) * 15
AdagaFogo, EspadaBrasas, MachadoCeruleo, MachadoMacabro, MachadoMarfim, MachadoBarbaro, EspadaFogoAzul, EspadaLua, EspadaCaida, EspadaPenitencia, MachadoBase = (None,) * 11
WeaponWheelUI = None 

# --- Importações Centralizadas ---
# Tenta importar todos os módulos necessários de 'importacoes.py'
try:
    from importacoes import * 
except ImportError as e_imp:
    print(f"ALERTA(Game Imports): Falha ao carregar módulos de 'importacoes.py': {e_imp}. Tentando fallbacks.")
except Exception as e_gen_imp:
    print(f"ERRO(Game Imports): Erro inesperado ao importar de 'importacoes.py': {e_gen_imp}")


# Fallback para Player se a importação centralizada falhar em defini-lo
try:
    if Player is None: # Só tenta importar localmente se Player ainda for None
        from player import Player as PlayerLocal # Tenta importar Player de player.py
        Player = PlayerLocal # Atribui a classe local à variável global Player
        print("DEBUG(Game Imports): Classe Player carregada diretamente de player.py (fallback).")
except ImportError as e_player_local:
    print(f"ALERTA(Game Imports): Falha ao importar 'Player' de player.py (fallback): {e_player_local}")
    # Player permanece None se ambas as tentativas de importação falharem.

# --- Constantes e Configurações Globais do Jogo ---
MUSICAS_JOGO = [
    "Musica/Gameplay/Faixa 1.mp3",
    "Musica/Gameplay/Faixa 2.mp3",
    "Musica/Gameplay/Faixa 3.mp3",
]
DEATH_SCREEN_BACKGROUND_IMAGE = "Sprites/Backgrounds/death_background.png"

game_music_volume = 0.5 # Volume padrão da música
game_sfx_volume = 0.5   # Volume padrão dos efeitos sonoros

# Variáveis globais de estado do jogo (serão inicializadas em inicializar_jogo)
jogador = None 
pause_manager = None
xp_manager = None 
barra_inventario = None 
gerenciador_inimigos = None 
game_is_running_flag = True     # Flag para threads externas (se houver)
jogo_pausado_para_inventario = False # Controla se o jogo está pausado devido ao inventário aberto


def inicializar_jogo(largura_tela, altura_tela):
    """
    Inicializa todos os componentes principais do jogo (jogador, inimigos, UI, etc.).
    Retorna uma tupla com os objetos inicializados e o estado do jogo.
    """
    global jogador, game_music_volume, pause_manager, xp_manager, barra_inventario, gerenciador_inimigos
    print("DEBUG(Game): Iniciando inicializar_jogo()...")
    tempo_inicio_func = pygame.time.get_ticks() # Para medir o tempo de inicialização, se necessário

    if Player is None:
        print("ERRO CRÍTICO(Game): Classe Player não está disponível. Impossível iniciar o jogo.")
        # Retorna valores que indicam falha na inicialização
        return None, None, None, [], [], set(), None, True, tempo_inicio_func, None, None 

    # Cria a instância do jogador
    jogador = Player(velocidade=5, vida_maxima=150) 
    print(f"DEBUG(Game): Instância do jogador criada: {jogador}") 
    
    # Garante que o jogador tenha um rect_colisao (essencial para movimento e interações)
    if not hasattr(jogador, 'rect_colisao') and hasattr(jogador, 'rect'): 
        print("DEBUG(Game): Jogador não possui rect_colisao, criando um a partir do rect principal.")
        jogador.rect_colisao = jogador.rect.inflate(-10,-10) # Cria um rect de colisão um pouco menor
    elif not hasattr(jogador, 'rect'):
        print("ERRO CRÍTICO(Game): Jogador não possui atributo 'rect' após inicialização.")
        return None, None, None, [], [], set(), None, True, tempo_inicio_func, None, None

    # Inicializa o gerenciador de XP
    if XPManager is not None:
        xp_manager = XPManager(player_ref=jogador, largura_tela=largura_tela, altura_tela=altura_tela)
        if hasattr(jogador, 'xp_manager'): jogador.xp_manager = xp_manager # Atribui ao jogador
        print("DEBUG(Game): XPManager inicializado.")
    else: 
        xp_manager = None
        print("ALERTA(Game): XPManager não disponível.")
    
    # --- MODIFICADO: Arma Inicial ---
    # Adiciona e equipa AdagaFogo como a ÚNICA arma inicial.
    if AdagaFogo is not None and hasattr(jogador, 'add_owned_weapon'):
        initial_weapon_instance = AdagaFogo()
        # O método add_owned_weapon já equipa a arma se for a primeira.
        if jogador.add_owned_weapon(initial_weapon_instance):
            print(f"DEBUG(Game): Arma inicial '{initial_weapon_instance.name}' adicionada e equipada.")
        else:
            print(f"ALERTA(Game): Falha ao adicionar arma inicial '{initial_weapon_instance.name}'.")
    else:
        print("ALERTA(Game): AdagaFogo ou método add_owned_weapon não disponível no jogador.")

    # O bloco que adicionava EspadaBrasas foi REMOVIDO para garantir que o jogador comece apenas com a Adaga.

    # Inicializa o sistema de estações do ano
    estacoes = Estacoes() if Estacoes is not None else None
    if estacoes: print("DEBUG(Game): Estacoes inicializadas.")
    else: print("ALERTA(Game): Estacoes não disponíveis.")

    gramas, arvores, blocos_gerados = [], [], set() # Elementos do cenário
    
    # Inicializa o gerenciador de inimigos
    if GerenciadorDeInimigos is not None and estacoes is not None:
        gerenciador_inimigos = GerenciadorDeInimigos(estacoes_obj=estacoes, tela_largura=largura_tela, altura_tela=altura_tela)
        if jogador and hasattr(jogador, 'rect'): 
            # Tenta fazer o spawn inicial de inimigos
            if hasattr(gerenciador_inimigos, 'spawn_inimigos_iniciais'):
                gerenciador_inimigos.spawn_inimigos_iniciais(jogador) 
            elif hasattr(gerenciador_inimigos, 'spawn_inimigos'): # Fallback para método genérico
                gerenciador_inimigos.spawn_inimigos(jogador)
            print("DEBUG(Game): GerenciadorDeInimigos inicializado e spawn inicial tentado.")
    else:
        gerenciador_inimigos = None
        print("ALERTA(Game): GerenciadorDeInimigos não pôde ser inicializado (dependências ausentes).")

    # Inicializa o timer do jogo (se disponível)
    timer_obj = None
    if Timer is not None and pygame.font.get_init(): 
        try:
            # Estima a largura do texto do timer para centralizá-lo
            fonte_estimativa_timer = pygame.font.Font(None, 36)
            largura_texto_timer = fonte_estimativa_timer.size("00:00")[0]
            largura_fundo_timer = largura_texto_timer + 20 # Adiciona padding
            timer_pos_x = largura_tela // 2 - largura_fundo_timer // 2
            timer_obj = Timer(timer_pos_x, 25) # Posição Y ajustada
            print("DEBUG(Game): Timer inicializado.")
        except pygame.error as e_timer_font: 
            print(f"ALERTA(Game): Erro ao criar fonte para Timer: {e_timer_font}")
        except Exception as e_timer_gen:
            print(f"ALERTA(Game): Erro inesperado ao inicializar Timer: {e_timer_gen}")


    # Reseta o spawn da loja (se o módulo existir)
    if shop_elements and hasattr(shop_elements, 'reset_shop_spawn'):
        shop_elements.reset_shop_spawn()
        print("DEBUG(Game): Spawn da loja resetado.")

    # Inicializa o gerenciador do menu de pausa
    if PauseMenuManager is not None:
        # main é passado como callback para retornar ao menu principal ou reiniciar o jogo
        pause_manager = PauseMenuManager(pygame.display.get_surface(), 
                                         largura_tela, altura_tela, 
                                         main, main, # Assumindo que main pode reiniciar o jogo ou ir para o menu
                                         game_music_volume, game_sfx_volume)
        print("DEBUG(Game): PauseMenuManager inicializado.")
    else: 
        pause_manager = None
        print("ALERTA(Game): PauseMenuManager não disponível.")
    
    # Inicializa a barra de inventário de armas
    if BarraInventario and jogador and hasattr(jogador, 'owned_weapons'):
        margem_borda_x_inv = 25
        margem_borda_y_inv = 25
        slot_tamanho_barra_inv = 50 # Tamanho dos slots na barra
        
        # Posiciona a barra de inventário no canto inferior esquerdo
        barra_inv_x = margem_borda_x_inv
        barra_inv_y = altura_tela - slot_tamanho_barra_inv - margem_borda_y_inv
        
        barra_inventario = BarraInventario(barra_inv_x, barra_inv_y, largura_tela, altura_tela, 
                                           num_slots_hud=4, # Número de slots na barra rápida
                                           slot_tamanho=(slot_tamanho_barra_inv, slot_tamanho_barra_inv),
                                           espacamento=7)
        print("DEBUG(Game): Barra de Inventário (Armas) inicializada.")

        # Adiciona as armas iniciais do jogador à interface da barra de inventário
        # (Esta parte foi simplificada pois o jogador agora só começa com uma arma)
        if hasattr(barra_inventario, 'handle_input'): # Verifica se o método esperado existe
            # A barra de inventário deve ser capaz de ler jogador.owned_weapons em seu método desenhar.
            # Não é mais necessário popular manualmente aqui se a barra lê dinamicamente.
            # Se a barra precisa que itens sejam "adicionados" a ela, isso seria feito aqui.
            # Exemplo:
            # for i, arma_no_inv_jogador in enumerate(jogador.owned_weapons):
            #     if arma_no_inv_jogador and i < barra_inventario.num_slots_hud:
            #         # Supondo que barra_inventario.adicionar_arma_ao_slot(arma, slot_idx) exista
            #         pass 
            pass # A lógica de popular a barra foi simplificada/movida para a própria classe BarraInventario ou seu desenhar.
            
    else:
        barra_inventario = None
        print("ALERTA(Game): BarraInventario não disponível ou jogador/inventário ausente.")

    # Referência à vida do jogador para a UI
    vida_jogador_ref = None
    if hasattr(jogador, 'vida') and jogador.vida is not None:
        vida_jogador_ref = jogador.vida
    elif Vida is not None: # Se o jogador não tem 'vida' mas a classe Vida existe
        print("ALERTA(Game): jogador.vida é None. Criando instância de Vida separada para UI.")
        vida_max_fallback = getattr(jogador, 'vida_maxima', 150) 
        vida_jogador_ref = Vida(vida_maxima=vida_max_fallback)
        if hasattr(jogador, 'vida'): # Tenta atribuir de volta ao jogador
            jogador.vida = vida_jogador_ref
    
    if vida_jogador_ref: print("DEBUG(Game): Referência à vida do jogador obtida para UI.")
    else: print("ALERTA(Game): Não foi possível obter referência à vida do jogador para UI.")

    print("DEBUG(Game): Saindo de inicializar_jogo().") 
    return jogador, estacoes, vida_jogador_ref, gramas, arvores, blocos_gerados, gerenciador_inimigos, False, tempo_inicio_func, timer_obj, barra_inventario


def gerar_elementos_ao_redor_do_jogador(jogador_obj, gramas_lista, arvores_lista, estacoes_obj, blocos_ja_gerados_set):
    """Gera dinamicamente elementos do cenário (grama, árvores) em blocos ao redor do jogador."""
    if jogador_obj is None or not hasattr(jogador_obj, 'rect') or estacoes_obj is None:
        # print("DEBUG(Game Gen): Abortando geração de elementos (jogador/estacoes ausente).")
        return

    bloco_tamanho_geracao = 1080 # Tamanho da área (bloco) para geração de novos elementos
    
    # Determina o bloco atual do jogador
    jogador_bloco_x = int(jogador_obj.rect.centerx // bloco_tamanho_geracao)
    jogador_bloco_y = int(jogador_obj.rect.centery // bloco_tamanho_geracao)

    # Verifica os blocos adjacentes (incluindo o atual)
    for dx_bloco in range(-1, 2): # De -1 a 1 (bloco anterior, atual, próximo)
        for dy_bloco in range(-1, 2):
            bloco_coord_atual = (jogador_bloco_x + dx_bloco, jogador_bloco_y + dy_bloco)
            
            if bloco_coord_atual not in blocos_ja_gerados_set: # Se este bloco ainda não foi gerado
                blocos_ja_gerados_set.add(bloco_coord_atual)
                # print(f"DEBUG(Game Gen): Gerando elementos para o novo bloco: {bloco_coord_atual}")
                
                # Calcula as coordenadas base do bloco
                base_x_bloco = (jogador_bloco_x + dx_bloco) * bloco_tamanho_geracao
                base_y_bloco = (jogador_bloco_y + dy_bloco) * bloco_tamanho_geracao
                
                # Gera grama (se a classe Grama estiver disponível)
                if Grama is not None:
                    for _ in range(random.randint(15, 25)): # Número aleatório de gramas por bloco
                        gramas_lista.append(Grama(base_x_bloco + random.randint(0, bloco_tamanho_geracao), 
                                                  base_y_bloco + random.randint(0, bloco_tamanho_geracao), 
                                                  50, 50)) # Tamanho da grama
                
                # Gera árvores (se a classe Arvore e o índice da estação estiverem disponíveis)
                if Arvore is not None and hasattr(estacoes_obj, 'i'):
                    for _ in range(random.randint(1, 3)): # Número aleatório de árvores por bloco
                        # Posiciona árvores mais centralizadas no bloco para evitar bordas abruptas
                        arvores_lista.append(Arvore(base_x_bloco + random.randint(bloco_tamanho_geracao // 4, 3 * bloco_tamanho_geracao // 4), 
                                                    base_y_bloco + random.randint(bloco_tamanho_geracao // 4, 3 * bloco_tamanho_geracao // 4), 
                                                    180, 180, estacoes_obj.i)) # Tamanho da árvore e estação atual
                
                # Tenta gerar a loja (se o módulo e função existirem)
                if shop_elements and hasattr(shop_elements, 'spawn_shop_if_possible'):
                    shop_elements.spawn_shop_if_possible(jogador_obj, estacoes_obj, blocos_ja_gerados_set)

def tocar_musica_jogo():
    """Seleciona aleatoriamente e toca uma música de fundo para o jogo."""
    global game_music_volume
    if not MUSICAS_JOGO: 
        print("ALERTA(Game Audio): Nenhuma música definida em MUSICAS_JOGO.")
        return
        
    musica_path_escolhida = random.choice(MUSICAS_JOGO)
    try:
        if pygame.mixer.get_init(): # Verifica se o mixer está inicializado
            pygame.mixer.music.load(musica_path_escolhida)
            pygame.mixer.music.set_volume(game_music_volume) # Usa o volume global
            pygame.mixer.music.play(-1) # -1 para tocar em loop infinito
            print(f"DEBUG(Game Audio): Tocando música: {musica_path_escolhida}")
    except pygame.error as e_audio: 
        print(f"ERRO(Game Audio): Erro ao carregar/tocar música '{musica_path_escolhida}': {e_audio}")
    except Exception as e_gen_audio:
        print(f"ERRO(Game Audio): Erro inesperado com áudio: {e_gen_audio}")


def verificar_colisoes_com_inimigos(gerenciador_inimigos_obj, jogador_obj):
    """Verifica e aplica dano ao jogador por colisão com inimigos."""
    if jogador_obj is None or not hasattr(jogador_obj, 'vida') or jogador_obj.vida is None or \
       not hasattr(jogador_obj.vida, 'esta_vivo') or not jogador_obj.vida.esta_vivo():
        return # Jogador inválido ou já morto
    
    jogador_col_rect = getattr(jogador_obj, 'rect_colisao', getattr(jogador_obj, 'rect', None))
    if jogador_col_rect is None or gerenciador_inimigos_obj is None or not hasattr(gerenciador_inimigos_obj, 'inimigos'):
        return # Sem rect de colisão do jogador ou gerenciador/lista de inimigos inválido

    for inimigo_atual in list(gerenciador_inimigos_obj.inimigos): # Itera sobre uma cópia para permitir remoção
        if inimigo_atual and hasattr(inimigo_atual, 'rect'):
            dano_contato_inimigo = getattr(inimigo_atual, 'contact_damage', 10) # Dano padrão se não especificado
            inimigo_col_rect_atual = getattr(inimigo_atual, 'rect_colisao', inimigo_atual.rect) # Usa rect_colisao se existir

            if inimigo_col_rect_atual and jogador_col_rect.colliderect(inimigo_col_rect_atual):
                if hasattr(jogador_obj, 'receber_dano') and jogador_obj.pode_levar_dano: # Verifica se pode levar dano (I-Frames)
                    # print(f"DEBUG(Game Colisão): Jogador colidiu com {getattr(inimigo_atual, 'nome', 'Inimigo')}. Dano: {dano_contato_inimigo}")
                    try: 
                        # Tenta passar o rect do inimigo para empurrar, se o método aceitar
                        jogador_obj.receber_dano(dano_contato_inimigo, inimigo_col_rect_atual) 
                    except TypeError: # Se receber_dano não aceitar o segundo argumento
                        jogador_obj.receber_dano(dano_contato_inimigo)


def desenhar_cena(janela_surf, estacoes_obj, gramas_lista, arvores_lista, jogador_obj, 
                  gerenciador_inimigos_obj, vida_ui_obj, barra_inventario_ui_obj, 
                  cam_x, cam_y, tempo_decorrido_seg, timer_ui_obj, delta_time_ms): 
    """Desenha todos os elementos visíveis do jogo na tela."""
    global xp_manager # Acessa o xp_manager global
    
    janela_surf.fill((0, 0, 0)) # Limpa a tela (fundo preto)
    
    # Desenha a estação (fundo)
    if estacoes_obj and hasattr(estacoes_obj, 'desenhar'): 
        estacoes_obj.desenhar(janela_surf)
    
    # Desenha gramas
    for grama_item in gramas_lista: 
        if grama_item and hasattr(grama_item, 'desenhar'): 
            grama_item.desenhar(janela_surf, cam_x, cam_y)
    
    # Desenha inimigos e seus projéteis
    if gerenciador_inimigos_obj:
        if hasattr(gerenciador_inimigos_obj, 'desenhar_inimigos'): 
            gerenciador_inimigos_obj.desenhar_inimigos(janela_surf, cam_x, cam_y)
        if hasattr(gerenciador_inimigos_obj, 'desenhar_projeteis_inimigos'): 
            gerenciador_inimigos_obj.desenhar_projeteis_inimigos(janela_surf, cam_x, cam_y)
    
    # Desenha o jogador
    if jogador_obj and hasattr(jogador_obj, 'desenhar'): 
        jogador_obj.desenhar(janela_surf, cam_x, cam_y)
    
    # Desenha árvores (após o jogador, para sobreposição correta)
    for arvore_item in arvores_lista: 
        if arvore_item and hasattr(arvore_item, 'desenhar'): 
            arvore_item.desenhar(janela_surf, cam_x, cam_y)
            
    # Desenha elementos da loja (se houver)
    if shop_elements and hasattr(shop_elements, 'draw_shop_elements'): 
        shop_elements.draw_shop_elements(janela_surf, cam_x, cam_y, delta_time_ms) 
        
    # Mensagem da estação (ex: "Verão")
    if estacoes_obj and hasattr(estacoes_obj, 'desenhar_mensagem_estacao'): 
        estacoes_obj.desenhar_mensagem_estacao(janela_surf)
    
    # UI: Barra de vida
    if vida_ui_obj and hasattr(vida_ui_obj, 'desenhar'): 
        vida_ui_obj.desenhar(janela_surf, 20, 20) # Posição fixa no canto superior esquerdo
        
    # UI: Timer do jogo
    if timer_ui_obj and hasattr(timer_ui_obj, 'desenhar'): 
        timer_ui_obj.desenhar(janela_surf, tempo_decorrido_seg)
        
    # UI: Barra de XP
    if xp_manager and hasattr(xp_manager, 'draw'): 
        xp_manager.draw(janela_surf)

    # UI: Barra de Inventário (Armas)
    if barra_inventario_ui_obj and hasattr(barra_inventario_ui_obj, 'desenhar') and jogador_obj:
        barra_inventario_ui_obj.desenhar(janela_surf, jogador_obj) # Passa a referência do jogador


def main():
    """Função principal que executa o menu e o loop do jogo."""
    global jogador, game_music_volume, game_sfx_volume, pause_manager, game_is_running_flag, \
           xp_manager, barra_inventario, jogo_pausado_para_inventario, gerenciador_inimigos

    print("DEBUG(Game): Iniciando main()...") 
    pygame.init() # Inicializa todos os módulos Pygame
    if not pygame.font.get_init(): # Garante que o módulo de fontes está pronto
        pygame.font.init()
        print("DEBUG(Game): Módulo Pygame Font inicializado em main.")
    try:
        pygame.mixer.init() # Inicializa o mixer de áudio
        print("DEBUG(Game): Módulo Pygame Mixer inicializado.")
    except pygame.error as e_mixer: 
        print(f"ALERTA(Game): Erro ao inicializar Pygame Mixer: {e_mixer}")

    # Configura a tela para fullscreen com base na resolução do monitor
    info_display = pygame.display.Info()
    largura_tela_jogo = info_display.current_w
    altura_tela_jogo = info_display.current_h
    janela_principal = pygame.display.set_mode((largura_tela_jogo, altura_tela_jogo), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Lenda de Asrahel")
    clock = pygame.time.Clock() # Relógio para controlar o FPS

    # --- Loop do Menu Principal ---
    if Menu is None: 
        print("ALERTA(Game): Classe Menu não disponível. Pulando diretamente para o jogo.")
        acao_menu_principal = "jogar" # Se não houver menu, assume que quer jogar
    else:
        menu_principal_obj = Menu(largura_tela_jogo, altura_tela_jogo)
        acao_menu_principal = None # Ação a ser retornada pelo menu
        print("DEBUG(Game): Entrando no loop do menu principal...") 
        while acao_menu_principal is None: 
            mouse_pos_menu = pygame.mouse.get_pos()
            menu_principal_obj.desenhar(janela_principal, mouse_pos_menu)
            
            for evento_menu in pygame.event.get(): 
                if evento_menu.type == pygame.QUIT:
                    if hasattr(menu_principal_obj, 'parar_musica'): menu_principal_obj.parar_musica()
                    pygame.quit()
                    sys.exit()
                if evento_menu.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(menu_principal_obj, 'verificar_click'):
                        acao_menu_principal = menu_principal_obj.verificar_click(*evento_menu.pos)
                        if acao_menu_principal == "sair": break # Sai do loop do menu se "sair" for clicado
            
            if acao_menu_principal == "sair": break 
            pygame.display.update() # Atualiza a tela do menu
            clock.tick(60) # Limita o FPS do menu
        print(f"DEBUG(Game): Saindo do loop do menu principal. Ação: {acao_menu_principal}") 

    # --- Início do Jogo ---
    if acao_menu_principal == "jogar":
        if Menu is not None and 'menu_principal_obj' in locals() and hasattr(menu_principal_obj, 'parar_musica'):
            menu_principal_obj.parar_musica() # Para a música do menu
        
        print("DEBUG(Game): Ação 'jogar' selecionada. Chamando inicializar_jogo()...") 
        
        # Inicializa todos os componentes do jogo
        jogador, est, vida_jogador_ref, gramas, arvores, blocos_gerados, \
        gerenciador_inimigos, jogador_morreu, tempo_inicio_jogo, timer_obj, \
        barra_inventario = inicializar_jogo(largura_tela_jogo, altura_tela_jogo)
        
        print(f"DEBUG(Game): Retorno de inicializar_jogo(): Jogador: {'OK' if jogador else 'FALHA'}, Vida UI: {'OK' if vida_jogador_ref else 'FALHA'}, BarraInv UI: {'OK' if barra_inventario else 'FALHA'}") 
        
        if jogador is None: # Verificação crítica
            print("ERRO CRÍTICO(Game): Falha ao inicializar o jogador em inicializar_jogo(). Encerrando.")
            pygame.quit()
            sys.exit()

        tocar_musica_jogo() # Inicia a música de fundo do jogo
        game_state = "playing"  # Estado atual do jogo (pode ser "paused", "inventory", etc.)
        game_is_running_flag = True # Flag para o loop principal

        running_game_loop = True
        print("DEBUG(Game): Entrando no loop principal do jogo (while running_game_loop)...") 
        while running_game_loop:
            delta_time_ms = clock.get_rawtime() # Tempo desde o último frame, para movimentos baseados em tempo

            # --- Processamento de Eventos ---
            for evento_jogo in pygame.event.get():
                if evento_jogo.type == pygame.QUIT: 
                    running_game_loop = False # Encerra o loop do jogo
                
                if evento_jogo.type == pygame.KEYDOWN:
                    # print(f"DEBUG(Game Loop) KEYDOWN: {pygame.key.name(evento_jogo.key)}") # Log de teclas (pode ser verboso)
                    
                    if evento_jogo.key == pygame.K_ESCAPE:
                        if jogo_pausado_para_inventario and barra_inventario: 
                            # print("DEBUG(Game Loop): ESC com inventário aberto. Fechando inventário.")
                            barra_inventario.toggle_visao_inventario(jogador)
                            jogo_pausado_para_inventario = False 
                            if pygame.mixer.get_init() and pygame.mixer.music.get_busy(): # Se a música estava tocando
                                pygame.mixer.music.unpause()
                            # print("DEBUG(Game Loop): Inventário fechado com ESC, jogo retomado.")
                        elif game_state == "playing" and pause_manager: 
                            # print("DEBUG(Game Loop): ESC pressionado. Abrindo menu de pausa.")
                            # Pausa a música antes de mostrar o menu
                            if pygame.mixer.get_init() and pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                            
                            action_pause, new_music_vol_pause, new_sfx_vol_pause = pause_manager.show_menu()
                            game_music_volume, game_sfx_volume = new_music_vol_pause, new_sfx_vol_pause # Atualiza volumes globais
                            
                            # Retoma a música se o jogador continuar
                            if action_pause == "resume_game" and pygame.mixer.get_init():
                                if not pygame.mixer.music.get_busy(): tocar_musica_jogo() # Se não estava tocando, reinicia
                                else: pygame.mixer.music.unpause()
                            elif action_pause == "main_menu": 
                                running_game_loop = False; acao_menu_principal = "main_menu_from_pause"; break 
                            elif action_pause == "quit": 
                                running_game_loop = False; break
                    
                    elif evento_jogo.key == pygame.K_TAB and game_state == "playing": 
                        # print(f"DEBUG(Game Loop): TAB pressionado.")
                        if barra_inventario and jogador: 
                            # print(f"DEBUG(Game Loop): Chamando toggle_visao_inventario. Estado atual: {barra_inventario.visao_inventario_aberta}")
                            barra_inventario.toggle_visao_inventario(jogador)
                            jogo_pausado_para_inventario = barra_inventario.visao_inventario_aberta
                            # print(f"DEBUG(Game Loop): Novo estado visao_inventario: {barra_inventario.visao_inventario_aberta}, jogo_pausado: {jogo_pausado_para_inventario}")
                            if jogo_pausado_para_inventario:
                                if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                                    pygame.mixer.music.pause()
                                # print("DEBUG(Game Loop): Inventário aberto com TAB, jogo pausado.")
                            else: # Fechou inventário
                                if pygame.mixer.get_init(): 
                                    if not pygame.mixer.music.get_busy(): tocar_musica_jogo() # Se não estava tocando, reinicia
                                    else: pygame.mixer.music.unpause()
                                # print("DEBUG(Game Loop): Inventário fechado com TAB, jogo retomado.")
                    
                    # Passa inputs para a barra de inventário (1-4 para equipar, cliques se aberta)
                    # A barra de inventário lida com as teclas numéricas para troca rápida.
                    if barra_inventario and game_state == "playing" and jogador: 
                        # O handle_input da barra de inventário já verifica se está aberta para cliques.
                        # Para teclas (1-4), funciona mesmo se fechada (HUD).
                        barra_inventario.handle_input(evento_jogo, jogador)
            
            if not running_game_loop: break # Sai do loop de eventos se o jogo terminou
            
            # --- Lógica de Atualização do Jogo (se não pausado) ---
            teclas_pressionadas = pygame.key.get_pressed() 
            
            if game_state == "playing" and not jogo_pausado_para_inventario: 
                if jogador:
                    if hasattr(jogador, 'mover'):
                        jogador.mover(teclas_pressionadas, arvores) # Passa árvores para colisão de movimento
                    if hasattr(jogador, 'update'): 
                        jogador.update() # Atualiza animações, timers internos do jogador
                
                if gerenciador_inimigos: 
                    if hasattr(gerenciador_inimigos, 'process_spawn_requests') and jogador:
                        gerenciador_inimigos.process_spawn_requests(jogador)
                    if hasattr(gerenciador_inimigos, 'update_inimigos') and jogador:
                        gerenciador_inimigos.update_inimigos(jogador) # Movimento, IA, ataques de inimigos
                    if hasattr(gerenciador_inimigos, 'update_projeteis_inimigos') and jogador:
                        gerenciador_inimigos.update_projeteis_inimigos(jogador) # Atualiza projéteis

                # Gera novos elementos do cenário dinamicamente
                gerar_elementos_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados)

                # Atualiza a estação do ano
                if est and hasattr(est, 'atualizar'):
                    estacao_anterior = est.i
                    est.atualizar()
                    if est.i != estacao_anterior: # Se a estação mudou
                        print(f"DEBUG(Game Loop): Mudança de estação para {est.nome_estacao()}")
                        if arvores: # Atualiza a aparência das árvores
                            for arvore_obj in arvores:
                                if arvore_obj and hasattr(arvore_obj, 'atualizar_sprite'): 
                                    arvore_obj.atualizar_sprite(est.i)
                        if gerenciador_inimigos: # Reseta spawns ou muda tipos de inimigos
                            if hasattr(gerenciador_inimigos, 'resetar_temporizador_spawn_estacao'):
                                gerenciador_inimigos.resetar_temporizador_spawn_estacao()
                            if jogador and hasattr(jogador, 'rect'): # Tenta novo spawn inicial para a estação
                                if hasattr(gerenciador_inimigos, 'spawn_inimigos_iniciais'): 
                                    gerenciador_inimigos.spawn_inimigos_iniciais(jogador) 
                                elif hasattr(gerenciador_inimigos, 'spawn_inimigos'):
                                    gerenciador_inimigos.spawn_inimigos(jogador)

                # Ataque do jogador
                if jogador and gerenciador_inimigos and hasattr(gerenciador_inimigos, 'inimigos'):
                    if hasattr(jogador, 'atacar'):
                        jogador.atacar(gerenciador_inimigos.inimigos) # Passa a lista de inimigos para o ataque
                
                # Colisões jogador-inimigo
                if jogador and hasattr(jogador, 'vida') and jogador.vida: 
                    verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador)
                    if not jogador.vida.esta_vivo(): # Verifica se o jogador morreu
                        jogador_morreu = True
                        running_game_loop = False # Encerra o loop do jogo

                # Interação com a Loja
                current_shop_rect_map = shop_elements.get_current_shop_rect() if shop_elements else None
                if current_shop_rect_map and jogador and hasattr(jogador, 'rect_colisao') and \
                   jogador.rect_colisao.colliderect(current_shop_rect_map) and teclas_pressionadas[pygame.K_e]: 
                    
                    if loja_core and hasattr(loja_core, 'run_shop_scene'):
                        if pygame.mixer.get_init() and pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                        
                        # Executa a cena da loja
                        continuar_jogo_apos_loja = loja_core.run_shop_scene(janela_principal, jogador, largura_tela_jogo, altura_tela_jogo)
                        
                        # Retoma a música do jogo
                        if pygame.mixer.get_init():
                            if pygame.mixer.music.get_busy(): pygame.mixer.music.unpause()
                            else: tocar_musica_jogo() # Se a música parou por algum motivo
                        
                        if not continuar_jogo_apos_loja: running_game_loop = False # Se a loja indicar para sair
                        
                        # Reseta o spawn da loja para que ela possa aparecer novamente
                        if shop_elements and hasattr(shop_elements, 'reset_shop_spawn'):
                            shop_elements.reset_shop_spawn()

            # --- Desenho da Cena ---
            cam_x_calc = jogador.rect.centerx - largura_tela_jogo // 2 if jogador and hasattr(jogador, 'rect') else 0
            cam_y_calc = jogador.rect.centery - altura_tela_jogo // 2 if jogador and hasattr(jogador, 'rect') else 0
            tempo_decorrido_total_seg = (pygame.time.get_ticks() - tempo_inicio_jogo) // 1000 if tempo_inicio_jogo else 0
            
            desenhar_cena(janela_principal, est, gramas, arvores, jogador, gerenciador_inimigos, 
                          vida_jogador_ref, barra_inventario, 
                          cam_x_calc, cam_y_calc, tempo_decorrido_total_seg, timer_obj, delta_time_ms)

            pygame.display.flip() # Atualiza a tela inteira
            clock.tick(60) # Mantém o FPS em 60

        # --- Fim do Loop Principal do Jogo ---
        game_is_running_flag = False # Sinaliza para threads externas pararem (se houver)
        
        # Para threads do gerenciador de inimigos, se existirem
        if gerenciador_inimigos and hasattr(gerenciador_inimigos, 'stop_threads'): 
            print("DEBUG(Game): Parando threads do GerenciadorDeInimigos...")
            gerenciador_inimigos.stop_threads()

        # Tela de Morte (se o jogador morreu)
        if jogador_morreu and run_death_screen:
            print("DEBUG(Game): Jogador morreu. Exibindo tela de morte...")
            # Garante que janelas Tkinter do menu de pausa sejam fechadas (se existirem)
            if pause_manager: 
                if hasattr(pause_manager, 'toplevel_window') and pause_manager.toplevel_window and \
                   hasattr(pause_manager.toplevel_window, 'winfo_exists') and pause_manager.toplevel_window.winfo_exists():
                    pause_manager.toplevel_window.destroy()
                if hasattr(pause_manager, 'tk_root') and pause_manager.tk_root and \
                   hasattr(pause_manager.tk_root, 'winfo_exists') and pause_manager.tk_root.winfo_exists():
                    pause_manager.tk_root.destroy()
            run_death_screen(janela_principal, main, main, DEATH_SCREEN_BACKGROUND_IMAGE) # Passa main para reiniciar/menu
        
        # Se saiu do jogo pelo menu de pausa para voltar ao menu principal
        if acao_menu_principal == "main_menu_from_pause": 
            print("DEBUG(Game): Retornando ao menu principal a partir do jogo...")
            main() # Chama main recursivamente para reiniciar o processo do menu
            return # Evita executar o código de quit abaixo

    elif acao_menu_principal == "sair":
        if Menu is not None and 'menu_principal_obj' in locals() and hasattr(menu_principal_obj, 'parar_musica'):
            menu_principal_obj.parar_musica()
        print("DEBUG(Game): Ação 'sair' selecionada no menu principal.")
    
    # --- Finalização do Jogo ---
    game_is_running_flag = False 
    
    if 'gerenciador_inimigos' in locals() and gerenciador_inimigos and hasattr(gerenciador_inimigos, 'stop_threads'): 
        print("DEBUG(Game): Parando threads do GerenciadorDeInimigos na finalização...")
        gerenciador_inimigos.stop_threads()

    if pygame.mixer.get_init(): pygame.mixer.quit() # Desinicializa o mixer
    pygame.quit() # Desinicializa todos os módulos Pygame
    print("DEBUG(Game): Pygame finalizado. Saindo do programa.")
    sys.exit()

if __name__ == "__main__":
    # Este bloco é executado quando o script é rodado diretamente.
    # Adiciona um try-except para capturar exceções não tratadas na função main,
    # o que pode ajudar a manter a janela aberta para ver o erro no console.
    try:
        main()
    except Exception as e_main_fatal:
        print(f"ERRO FATAL em main(): {e_main_fatal}")
        import traceback
        traceback.print_exc() # Imprime o stack trace completo do erro
        pygame.quit() # Tenta fechar o Pygame de forma limpa
        input("Pressione Enter para sair após o erro fatal...") # Pausa para ver o erro
        sys.exit(1) # Sai com código de erro
