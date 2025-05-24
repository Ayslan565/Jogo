import pygame
import random
import time
import sys
import os
import threading 
import tkinter as tk # Necessário para tk.TclError no run_weapon_wheel_thread_target

# --- Configuração do sys.path ---
current_dir = os.path.dirname(os.path.abspath(__file__))
arquivos_dir = current_dir 
if arquivos_dir not in sys.path:
    sys.path.append(arquivos_dir)
project_root_dir = os.path.dirname(current_dir) 
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir) 

# --- Importações Centralizadas ---
try:
    from importacoes import *
except ImportError as e:
    print(f"DEBUG(Game): ERRO CRÍTICO ao importar 'importacoes.py'. Verifique o arquivo e o sys.path. Erro: {e}")
    Player, WeaponWheelUI, PauseMenuManager, XPManager, Menu, GerenciadorDeInimigos, Estacoes, Grama, Arvore, Timer, shop_elements, run_death_screen, loja_core, Vida = (None,) * 14
    AdagaFogo, EspadaBrasas, MachadoCeruleo, MachadoMacabro, MachadoMarfim, MachadoBarbaro, EspadaFogoAzul, EspadaLua, EspadaCaida, EspadaPenitencia, MachadoBase = (None,) * 11

try:
    from player import Player 
except ImportError as e:
    print(f"DEBUG(Game): ERRO CRÍTICO: Módulo 'player.py' ou classe 'Player' não encontrado. Erro: {e}")
    Player = None 


MUSICAS_JOGO = [
    "Musica/Gameplay/Faixa 1.mp3",
    "Musica/Gameplay/Faixa 2.mp3",
    "Musica/Gameplay/Faixa 3.mp3",
]
DEATH_SCREEN_BACKGROUND_IMAGE = "Sprites/Backgrounds/death_background.png"

game_music_volume = 0.5 
game_sfx_volume = 0.5  

weapon_wheel_ui = None
weapon_wheel_thread = None 
weapon_wheel_active_event = threading.Event() 

game_paused_for_wheel = False
jogador = None 
pause_manager = None
xp_manager = None 
game_is_running_flag = True # Flag global para controlar todos os loops de threads


def on_weapon_selected_from_wheel(selected_weapon_instance: Weapon): 
    global jogador, game_paused_for_wheel, weapon_wheel_active_event
    
    if jogador and hasattr(jogador, 'owned_weapons') and hasattr(jogador, 'equip_weapon') and selected_weapon_instance:
        arma_para_equipar = None
        for w_inv in jogador.owned_weapons:
            if w_inv is selected_weapon_instance or (hasattr(w_inv, 'name') and w_inv.name == selected_weapon_instance.name): 
                arma_para_equipar = w_inv
                break
        
        if arma_para_equipar:
            jogador.equip_weapon(arma_para_equipar)
    
    game_paused_for_wheel = False 
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()
    weapon_wheel_active_event.clear() 
    if weapon_wheel_ui and hasattr(weapon_wheel_ui, 'hide_wheel'): 
        weapon_wheel_ui.hide_wheel()


def run_weapon_wheel_thread_target():
    global weapon_wheel_ui, game_paused_for_wheel, weapon_wheel_active_event, game_is_running_flag
    
    # print("DEBUG(Game): Thread da roda de armas iniciado.")
    if weapon_wheel_ui:
        try:
            # Garante que a janela seja criada se não existir e o evento estiver setado
            if weapon_wheel_active_event.is_set():
                if weapon_wheel_ui.toplevel_window is None or not weapon_wheel_ui.toplevel_window.winfo_exists():
                    weapon_wheel_ui.create_wheel_window()
                if weapon_wheel_ui.toplevel_window and weapon_wheel_ui.toplevel_window.winfo_exists(): # Verifica novamente
                    weapon_wheel_ui.show_wheel()

            while game_is_running_flag: # O loop principal do thread agora é controlado por game_is_running_flag
                if weapon_wheel_active_event.is_set(): # Verifica se a roda deve estar ativa
                    if hasattr(weapon_wheel_ui, 'tk_root') and weapon_wheel_ui.tk_root and \
                       hasattr(weapon_wheel_ui, 'toplevel_window') and weapon_wheel_ui.toplevel_window and \
                       weapon_wheel_ui.tk_root.winfo_exists() and weapon_wheel_ui.toplevel_window.winfo_exists():
                        try:
                            # Se a roda foi escondida mas o evento ainda está set (ex: reabertura rápida), mostra-a
                            if not weapon_wheel_ui.toplevel_window.winfo_viewable():
                                weapon_wheel_ui.show_wheel()
                                
                            weapon_wheel_ui.tk_root.update()
                            weapon_wheel_ui.tk_root.update_idletasks()
                        except tk.TclError as e: 
                            print(f"DEBUG(Game): Erro Tcl no loop da roda (ex: janela fechada): {e}")
                            weapon_wheel_active_event.clear() 
                            # Não dá break aqui, deixa game_is_running_flag controlar a saída do thread
                    else: 
                        # Se a janela não existe mais mas o evento está setado, limpa o evento
                        # print("DEBUG(Game): Janela da roda não existe, mas evento estava setado. Limpando evento.")
                        weapon_wheel_active_event.clear()
                
                # Pequena pausa para o thread não consumir 100% CPU e ser responsivo ao game_is_running_flag
                # e ao weapon_wheel_active_event
                # O wait() permite que o thread "durma" até que o evento seja setado ou o timeout ocorra
                # ou até que game_is_running_flag se torne False.
                activated = weapon_wheel_active_event.wait(timeout=0.05) 
                if not game_is_running_flag: # Verifica novamente após o wait
                    break

        except Exception as e:
            print(f"DEBUG(Game): Erro EXCEPCIONAL no thread da roda de armas: {e}")
        finally:
            print("DEBUG(Game): Thread da roda de armas finalizando e limpando recursos Tkinter...")
            if weapon_wheel_ui:
                # Esconde primeiro para liberar grab, se houver
                if hasattr(weapon_wheel_ui, 'hide_wheel'):
                    try:
                        weapon_wheel_ui.hide_wheel() # Isso também deve chamar active_event_ref.clear()
                    except Exception as e_hide:
                        print(f"DEBUG(Game): Erro ao chamar hide_wheel no finally do thread: {e_hide}")

                # Destruição da janela Toplevel
                if hasattr(weapon_wheel_ui, 'toplevel_window') and weapon_wheel_ui.toplevel_window:
                    try:
                        if weapon_wheel_ui.toplevel_window.winfo_exists():
                            weapon_wheel_ui.toplevel_window.destroy()
                        weapon_wheel_ui.toplevel_window = None
                    except Exception as e_tl:
                        print(f"DEBUG(Game): Erro ao destruir toplevel_window no finally do thread: {e_tl}")
                
                # Destruição da raiz Tkinter
                if hasattr(weapon_wheel_ui, 'tk_root') and weapon_wheel_ui.tk_root:
                    try:
                        if weapon_wheel_ui.tk_root.winfo_exists():
                            weapon_wheel_ui.tk_root.quit() 
                            weapon_wheel_ui.tk_root.destroy()
                        weapon_wheel_ui.tk_root = None
                        print("DEBUG(Game): tk_root da roda de armas destruído pelo thread.")
                    except Exception as e_root:
                        print(f"DEBUG(Game): Erro ao destruir tk_root no finally do thread: {e_root}")
            
            # Garante que o estado de pausa do jogo seja resetado
            if game_paused_for_wheel: 
                game_paused_for_wheel = False
                if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpause()
            weapon_wheel_active_event.clear() # Garante que o evento seja limpo
            print("DEBUG(Game): Limpeza final do thread da roda de armas completa.")


def inicializar_jogo(largura_tela, altura_tela):
    global jogador, game_music_volume, pause_manager, xp_manager, weapon_wheel_ui, weapon_wheel_active_event
    print("DEBUG(Game): Initializing game components...")
    tempo_inicio = pygame.time.get_ticks()

    if Player is None:
        print("DEBUG(Game): CRITICAL Error: Player class not available. Aborting initialization.")
        return None, None, None, [], [], set(), None, True, tempo_inicio, None 

    jogador = Player(velocidade=5, vida_maxima=150) 
    
    if not hasattr(jogador, 'rect_colisao') and hasattr(jogador, 'rect'): 
        jogador.rect_colisao = jogador.rect.inflate(-10,-10)
    elif not hasattr(jogador, 'rect'):
         print("DEBUG(Game): CRITICAL Player has no rect attribute after init.")
         return None, None, None, [], [], set(), None, True, tempo_inicio, None

    if XPManager is not None:
        xp_manager = XPManager(player_ref=jogador, largura_tela=largura_tela, altura_tela=altura_tela)
        if hasattr(jogador, 'xp_manager'): jogador.xp_manager = xp_manager
    else: xp_manager = None
    
    if AdagaFogo is not None and hasattr(jogador, 'add_owned_weapon') and hasattr(jogador, 'equip_weapon'):
        initial_weapon_instance = AdagaFogo()
        if jogador.add_owned_weapon(initial_weapon_instance): 
             jogador.equip_weapon(initial_weapon_instance) 

    estacoes = Estacoes() if Estacoes is not None else None
    gramas, arvores, blocos_gerados = [], [], set()
    gerenciador_inimigos = GerenciadorDeInimigos(estacoes_obj=estacoes, tela_largura=largura_tela, altura_tela=altura_tela) if GerenciadorDeInimigos is not None and estacoes is not None else None
    
    if gerenciador_inimigos and jogador and hasattr(jogador, 'rect'): 
        if hasattr(gerenciador_inimigos, 'spawn_inimigos_iniciais'):
             gerenciador_inimigos.spawn_inimigos_iniciais(jogador)
        elif hasattr(gerenciador_inimigos, 'spawn_inimigos'):
             gerenciador_inimigos.spawn_inimigos(jogador)


    timer_obj = None
    if Timer is not None and pygame.font.get_init(): 
        try:
            fonte_estimativa = pygame.font.Font(None, 36)
            largura_estimada_texto = fonte_estimativa.size("00:00")[0]
            largura_estimada_fundo = largura_estimada_texto + 10
            timer_pos_x = largura_tela // 2 - largura_estimada_fundo // 2
            timer_obj = Timer(timer_pos_x, 30)
        except pygame.error as e: print(f"DEBUG(Game): Erro ao criar Timer font: {e}")

    if shop_elements and hasattr(shop_elements, 'reset_shop_spawn'):
        shop_elements.reset_shop_spawn()

    if PauseMenuManager is not None:
        pause_manager = PauseMenuManager(pygame.display.get_surface(), 
                                        largura_tela, altura_tela, 
                                        main, main, 
                                        game_music_volume, game_sfx_volume)
    else: pause_manager = None
    
    if WeaponWheelUI is not None and jogador and hasattr(jogador, 'owned_weapons'):
        weapon_wheel_ui = WeaponWheelUI(
            parent_game_instance=None, 
            on_weapon_selected_callback=on_weapon_selected_from_wheel,
            player_owned_weapons_ref=jogador.owned_weapons,
            active_event_ref=weapon_wheel_active_event 
        )
        print("DEBUG(Game): WeaponWheelUI inicializada.")
    else: 
        weapon_wheel_ui = None
        print("DEBUG(Game): Aviso: WeaponWheelUI ou jogador/inventário não disponível para inicialização.")
    
    vida_jogador_ref = jogador.vida if hasattr(jogador, 'vida') and jogador.vida is not None else None
    if vida_jogador_ref is None and Vida is not None: 
        print("DEBUG(Game): Atenção! jogador.vida é None, criando instância de Vida separada para referência.")
        vida_max_jogador = getattr(jogador, 'vida_maxima', 150) 
        vida_jogador_ref = Vida(vida_maxima=vida_max_jogador)
        if hasattr(jogador, 'vida'): 
            jogador.vida = vida_jogador_ref

    print("DEBUG(Game): Saindo de inicializar_jogo().") 
    return jogador, estacoes, vida_jogador_ref, gramas, arvores, blocos_gerados, gerenciador_inimigos, False, tempo_inicio, timer_obj


def gerar_elementos_ao_redor_do_jogador(Asrahel, gramas, arvores, est, blocos_gerados):
    jogador_obj = Asrahel 
    bloco_tamanho = 1080
    if jogador_obj is None or not hasattr(jogador_obj, 'rect') or est is None: return

    jogador_bloco_x = int(jogador_obj.rect.centerx // bloco_tamanho)
    jogador_bloco_y = int(jogador_obj.rect.centery // bloco_tamanho)
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            bloco_coord = (jogador_bloco_x + dx, jogador_bloco_y + dy)
            if bloco_coord not in blocos_gerados:
                blocos_gerados.add(bloco_coord)
                base_x = (jogador_bloco_x + dx) * bloco_tamanho
                base_y = (jogador_bloco_y + dy) * bloco_tamanho
                if Grama is not None:
                    for _ in range(random.randint(15, 25)):
                        gramas.append(Grama(base_x + random.randint(0, bloco_tamanho), base_y + random.randint(0, bloco_tamanho), 50, 50))
                if Arvore is not None and hasattr(est, 'i'):
                    for _ in range(random.randint(1, 3)):
                        arvores.append(Arvore(base_x + random.randint(bloco_tamanho // 4, 3 * bloco_tamanho // 4), base_y + random.randint(bloco_tamanho // 4, 3 * bloco_tamanho // 4), 180, 180, est.i))
                
                if shop_elements and hasattr(shop_elements, 'spawn_shop_if_possible'):
                    shop_elements.spawn_shop_if_possible(jogador_obj, est, blocos_gerados)

def tocar_musica_jogo():
    global game_music_volume
    if not MUSICAS_JOGO: return
    musica_path = random.choice(MUSICAS_JOGO)
    try:
        if pygame.mixer.get_init(): 
            pygame.mixer.music.load(musica_path)
            pygame.mixer.music.set_volume(game_music_volume)
            pygame.mixer.music.play(-1)
    except pygame.error as e: print(f"Game: Erro ao tocar música '{musica_path}': {e}")

def verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador_obj):
    if jogador_obj is None or not hasattr(jogador_obj, 'vida') or jogador_obj.vida is None or not jogador_obj.vida.esta_vivo():
        return
    
    jogador_rect_colisao = getattr(jogador_obj, 'rect_colisao', getattr(jogador_obj, 'rect', None))
    if jogador_rect_colisao is None or gerenciador_inimigos is None or not hasattr(gerenciador_inimigos, 'inimigos'):
        return

    for inimigo in list(gerenciador_inimigos.inimigos): 
        if inimigo and hasattr(inimigo, 'rect'):
            dano_a_aplicar = getattr(inimigo, 'contact_damage', 10) 
            inimigo_col_rect = getattr(inimigo, 'rect_colisao', inimigo.rect)

            if inimigo_col_rect and jogador_rect_colisao.colliderect(inimigo_col_rect):
                if jogador_obj.vida.esta_vivo(): 
                    if hasattr(jogador_obj, 'receber_dano'):
                        try: jogador_obj.receber_dano(dano_a_aplicar, inimigo_col_rect)
                        except TypeError: jogador_obj.receber_dano(dano_a_aplicar)


def desenhar_cena(janela, est, gramas, arvores, jogador_obj, gerenciador_inimigos, vida_jogador_obj, camera_x, camera_y, tempo_decorrido, timer_obj, dt_ms):
    global xp_manager 
    janela.fill((0, 0, 0))
    if est and hasattr(est, 'desenhar'): est.desenhar(janela)
    for gr in gramas: 
        if gr and hasattr(gr, 'desenhar'): gr.desenhar(janela, camera_x, camera_y)
    if gerenciador_inimigos:
        if hasattr(gerenciador_inimigos, 'desenhar_inimigos'): gerenciador_inimigos.desenhar_inimigos(janela, camera_x, camera_y)
        if hasattr(gerenciador_inimigos, 'desenhar_projeteis_inimigos'): gerenciador_inimigos.desenhar_projeteis_inimigos(janela, camera_x, camera_y)
    
    if jogador_obj and hasattr(jogador_obj, 'desenhar'): jogador_obj.desenhar(janela, camera_x, camera_y)
    
    for a in arvores:
        if a and hasattr(a, 'desenhar'): a.desenhar(janela, camera_x, camera_y)
            
    if shop_elements and hasattr(shop_elements, 'draw_shop_elements'): 
        shop_elements.draw_shop_elements(janela, camera_x, camera_y, dt_ms) 
        
    if est and hasattr(est, 'desenhar_mensagem_estacao'): est.desenhar_mensagem_estacao(janela)
    
    if vida_jogador_obj and hasattr(vida_jogador_obj, 'desenhar'): 
        vida_jogador_obj.desenhar(janela, 20, 20)
        
    if timer_obj and hasattr(timer_obj, 'desenhar'): timer_obj.desenhar(janela, tempo_decorrido)
    if xp_manager and hasattr(xp_manager, 'draw'): xp_manager.draw(janela)


def main():
    global jogador, game_paused_for_wheel, weapon_wheel_ui, weapon_wheel_thread, weapon_wheel_active_event
    global game_music_volume, game_sfx_volume, pause_manager, game_is_running_flag, xp_manager

    print("DEBUG(Game): Iniciando main()...") 
    pygame.init()
    if not pygame.font.get_init(): pygame.font.init(); print("Pygame: Font module initialized in main.")
    try:
        pygame.mixer.init()
    except pygame.error as e: print(f"Pygame: Error initializing audio mixer: {e}")

    info = pygame.display.Info()
    largura_tela = info.current_w
    altura_tela = info.current_h
    janela = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Lenda de Asrahel")
    clock = pygame.time.Clock()

    if Menu is None: 
        print("DEBUG(Game): Classe Menu não disponível. Pulando para o jogo.")
        acao_menu = "jogar"
    else:
        menu = Menu(largura_tela, altura_tela)
        acao_menu = None
        print("DEBUG(Game): Entrando no loop do menu...") 
        while acao_menu is None: 
            mouse_pos = pygame.mouse.get_pos()
            menu.desenhar(janela, mouse_pos)
            for evento in pygame.event.get(): 
                if evento.type == pygame.QUIT:
                    if hasattr(menu, 'parar_musica'): menu.parar_musica(); pygame.quit(); sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(menu, 'verificar_click'):
                        acao_menu = menu.verificar_click(*evento.pos)
                        if acao_menu == "sair": break 
            if acao_menu == "sair": break 
            pygame.display.update()
            clock.tick(60)
        print(f"DEBUG(Game): Saindo do loop do menu. acao_menu = {acao_menu}") 

    if acao_menu == "jogar":
        if Menu is not None and 'menu' in locals() and hasattr(menu, 'parar_musica'): menu.parar_musica()
        print("DEBUG(Game): Ação 'jogar' selecionada. Chamando inicializar_jogo()...") 
        
        jogador, est, vida_jogador_ref, gramas, arvores, blocos_gerados, gerenciador_inimigos, jogador_morreu, tempo_inicio, timer_obj = inicializar_jogo(largura_tela, altura_tela)
        print(f"DEBUG(Game): inicializar_jogo() retornou. Jogador: {jogador}, Vida Ref: {vida_jogador_ref}") 
        
        if jogador is None: 
            print("DEBUG(Game): Falha crítica ao inicializar o jogador. Encerrando.")
            pygame.quit()
            sys.exit()

        tocar_musica_jogo()
        game_state = "playing" 
        game_is_running_flag = True # Define a flag para o loop de jogo e threads

        running = True
        print("DEBUG(Game): Entrando no loop principal do jogo (while running)...") 
        while running:
            dt_ms = clock.get_rawtime() 

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: running = False
                if evento.type == pygame.KEYDOWN:
                    # print(f"DEBUG(Game.py) KEYDOWN Event: {pygame.key.name(evento.key)}") 
                    if evento.key == pygame.K_ESCAPE:
                        if game_paused_for_wheel: 
                            if weapon_wheel_ui and hasattr(weapon_wheel_ui, 'hide_wheel'): weapon_wheel_ui.hide_wheel() 
                            # A lógica de despausar o jogo é agora tratada no hide_wheel ou no callback
                        elif game_state == "playing" and pause_manager: 
                            action, new_music_vol, new_sfx_vol = pause_manager.show_menu()
                            game_music_volume, game_sfx_volume = new_music_vol, new_sfx_vol
                            if action == "main_menu": running = False; acao_menu = "main_menu_from_pause"; break 
                            elif action == "quit": running = False; break
                    
                    if evento.key == pygame.K_TAB and not game_paused_for_wheel and game_state == "playing":
                        if weapon_wheel_ui and jogador and hasattr(jogador, 'owned_weapons'):
                            print("DEBUG(Game): TAB pressionado. Abrindo roda de armas...") 
                            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                                pygame.mixer.music.pause()
                            game_paused_for_wheel = True
                            weapon_wheel_active_event.set() 
                            
                            weapon_wheel_ui.player_weapons_ref = jogador.owned_weapons 
                            
                            if weapon_wheel_thread is None or not weapon_wheel_thread.is_alive():
                                print("DEBUG(Game): Criando e iniciando novo thread para roda de armas.") 
                                weapon_wheel_thread = threading.Thread(target=run_weapon_wheel_thread_target, daemon=True)
                                weapon_wheel_thread.start()
                
            if not running: break 
            
            teclas = pygame.key.get_pressed() 
            
            if game_state == "playing" and not game_paused_for_wheel:
                if jogador:
                    if hasattr(jogador, 'mover'):
                        jogador.mover(teclas, arvores)
                    if hasattr(jogador, 'update'): 
                        jogador.update()
                
                if gerenciador_inimigos: 
                    if hasattr(gerenciador_inimigos, 'process_spawn_requests') and jogador:
                         gerenciador_inimigos.process_spawn_requests(jogador)
                    if hasattr(gerenciador_inimigos, 'update_inimigos') and jogador:
                        gerenciador_inimigos.update_inimigos(jogador)
                    if hasattr(gerenciador_inimigos, 'update_projeteis_inimigos') and jogador:
                        gerenciador_inimigos.update_projeteis_inimigos(jogador)

                gerar_elementos_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados)

                if est and hasattr(est, 'atualizar'):
                    est_ant = est.i; est.atualizar()
                    if est.i != est_ant:
                        if arvores:
                            for arv in arvores:
                                if arv and hasattr(arv, 'atualizar_sprite'): arv.atualizar_sprite(est.i)
                        if gerenciador_inimigos and jogador and hasattr(jogador, 'rect'):
                            if hasattr(gerenciador_inimigos, 'spawn_inimigos_iniciais'): 
                                gerenciador_inimigos.spawn_inimigos_iniciais(jogador) 
                            elif hasattr(gerenciador_inimigos, 'spawn_inimigos'):
                                gerenciador_inimigos.spawn_inimigos(jogador)


                if jogador and gerenciador_inimigos and hasattr(gerenciador_inimigos, 'inimigos'):
                    jogador.atacar(gerenciador_inimigos.inimigos)
                
                if jogador and hasattr(jogador, 'vida') and jogador.vida: 
                    verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador)
                    if not jogador.vida.esta_vivo():
                        jogador_morreu = True; running = False 

                current_shop_rect_on_map = shop_elements.get_current_shop_rect() if shop_elements else None
                if current_shop_rect_on_map and jogador and hasattr(jogador, 'rect_colisao') and \
                   jogador.rect_colisao.colliderect(current_shop_rect_on_map) and teclas[pygame.K_e]: 
                    
                    if loja_core and hasattr(loja_core, 'run_shop_scene'): # loja_core é o módulo loja.py
                        if pygame.mixer.get_init() and pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                        
                        should_continue_main_game = loja_core.run_shop_scene(janela, jogador, largura_tela, altura_tela)
                        
                        if pygame.mixer.get_init():
                            if pygame.mixer.music.get_busy(): pygame.mixer.music.unpause()
                            else: tocar_musica_jogo() 
                        
                        if not should_continue_main_game: running = False 
                        
                        if shop_elements and hasattr(shop_elements, 'reset_shop_spawn'):
                            shop_elements.reset_shop_spawn()

            if game_state == "playing": 
                camera_x = jogador.rect.centerx - largura_tela // 2 if jogador and hasattr(jogador, 'rect') else 0
                camera_y = jogador.rect.centery - altura_tela // 2 if jogador and hasattr(jogador, 'rect') else 0
                tempo_decorrido_segundos = (pygame.time.get_ticks() - tempo_inicio) // 1000 if tempo_inicio else 0
                desenhar_cena(janela, est, gramas, arvores, jogador, gerenciador_inimigos, vida_jogador_ref, camera_x, camera_y, tempo_decorrido_segundos, timer_obj, dt_ms)

            pygame.display.flip()
            clock.tick(60) 

        # --- FIM DO LOOP while running ---
        game_is_running_flag = False # Sinaliza para todos os threads pararem
        
        print("DEBUG(Game): Saindo do loop principal. Esperando threads...")

        if weapon_wheel_thread and weapon_wheel_thread.is_alive():
            print("DEBUG(Game): Sinalizando e esperando thread da roda de armas terminar...")
            weapon_wheel_active_event.set() # Garante que o thread não esteja bloqueado em wait()
            time.sleep(0.05) # Dá uma chance para o thread processar a mudança de game_is_running_flag
            weapon_wheel_active_event.clear() # Agora limpa para que o loop do thread termine se ainda estiver nele
            weapon_wheel_thread.join(timeout=2.0) 
            if weapon_wheel_thread.is_alive():
                print("DEBUG(Game): AVISO: Thread da roda de armas não terminou a tempo.")
            else:
                print("DEBUG(Game): Thread da roda de armas finalizado.")
        
        # A limpeza dos recursos Tkinter da roda de armas agora é feita no finally do run_weapon_wheel_thread_target
        weapon_wheel_ui = None # Limpa a referência

        if gerenciador_inimigos and hasattr(gerenciador_inimigos, 'stop_threads'): 
            gerenciador_inimigos.stop_threads()

        if jogador_morreu and run_death_screen:
            if pause_manager: 
                if hasattr(pause_manager, 'toplevel_window') and pause_manager.toplevel_window and pause_manager.toplevel_window.winfo_exists():
                    pause_manager.toplevel_window.destroy()
                if hasattr(pause_manager, 'tk_root') and pause_manager.tk_root and pause_manager.tk_root.winfo_exists():
                    pause_manager.tk_root.destroy()
            run_death_screen(janela, main, main, DEATH_SCREEN_BACKGROUND_IMAGE)
        
        if acao_menu == "main_menu_from_pause": main(); return 

    elif acao_menu == "sair":
        if Menu is not None and 'menu' in locals() and hasattr(menu, 'parar_musica'): menu.parar_musica()
    
    # Finalização geral do jogo
    game_is_running_flag = False 
    if weapon_wheel_thread and weapon_wheel_thread.is_alive(): # Segunda verificação
        weapon_wheel_active_event.clear()
        weapon_wheel_thread.join(timeout=1.0)
    
    if gerenciador_inimigos and hasattr(gerenciador_inimigos, 'stop_threads'): 
        gerenciador_inimigos.stop_threads()

    if pygame.mixer.get_init(): pygame.mixer.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
