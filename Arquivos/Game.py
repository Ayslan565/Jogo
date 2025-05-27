import pygame
import random
import sys
import os
# import tkinter as tk # Não é mais necessário

# --- Configuração do sys.path ---
current_dir = os.path.dirname(os.path.abspath(__file__))
arquivos_dir = current_dir 
if arquivos_dir not in sys.path:
    sys.path.append(arquivos_dir)
project_root_dir = os.path.dirname(current_dir) 
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir) 
 
# --- Pré-definição de Nomes Globais como Fallback ---
Player, PauseMenuManager, XPManager, Menu, GerenciadorDeInimigos, Estacoes, Grama, Arvore, Timer, shop_elements, run_death_screen, loja_core, Vida, BarraInventario, ItemInventario = (None,) * 15
AdagaFogo, EspadaBrasas, MachadoCeruleo, MachadoMacabro, MachadoMarfim, MachadoBarbaro, EspadaFogoAzul, EspadaLua, EspadaCaida, EspadaPenitencia, MachadoBase = (None,) * 11
WeaponWheelUI = None 

# --- Importações Centralizadas ---
from importacoes import * 

try:
    from player import Player as PlayerLocal
    if Player is None: 
        Player = PlayerLocal
        print("DEBUG(Game): Classe Player carregada de player.py (fallback).")
except ImportError as e:
    print(f"DEBUG(Game): ERRO CRÍTICO ao importar 'player.py' diretamente. Erro: {e}")
    if Player is None: 
        Player = None 


MUSICAS_JOGO = [
    "Musica/Gameplay/Faixa 1.mp3",
    "Musica/Gameplay/Faixa 2.mp3",
    "Musica/Gameplay/Faixa 3.mp3",
]
DEATH_SCREEN_BACKGROUND_IMAGE = "Sprites/Backgrounds/death_background.png"

game_music_volume = 0.5 
game_sfx_volume = 0.5  

jogador = None 
pause_manager = None
xp_manager = None 
barra_inventario = None 
gerenciador_inimigos = None 
game_is_running_flag = True 
jogo_pausado_para_inventario = False


def inicializar_jogo(largura_tela, altura_tela):
    global jogador, game_music_volume, pause_manager, xp_manager, barra_inventario, gerenciador_inimigos
    print("DEBUG(Game): Initializing game components...")
    tempo_inicio = pygame.time.get_ticks()

    if Player is None:
        print("DEBUG(Game): CRITICAL Error: Player class not available. Aborting initialization.")
        return None, None, None, [], [], set(), None, True, tempo_inicio, None, None 

    jogador = Player(velocidade=5, vida_maxima=150) 
    print(f"DEBUG(Game): Objeto jogador criado: {jogador}") 
    
    if not hasattr(jogador, 'rect_colisao') and hasattr(jogador, 'rect'): 
        jogador.rect_colisao = jogador.rect.inflate(-10,-10)
    elif not hasattr(jogador, 'rect'):
         print("DEBUG(Game): CRITICAL Player has no rect attribute after init.")
         return None, None, None, [], [], set(), None, True, tempo_inicio, None, None

    if XPManager is not None:
        xp_manager = XPManager(player_ref=jogador, largura_tela=largura_tela, altura_tela=altura_tela)
        if hasattr(jogador, 'xp_manager'): jogador.xp_manager = xp_manager
    else: xp_manager = None
    
    if AdagaFogo is not None and hasattr(jogador, 'add_owned_weapon') and hasattr(jogador, 'equip_weapon'):
        initial_weapon_instance = AdagaFogo()
        if jogador.add_owned_weapon(initial_weapon_instance): 
             jogador.equip_weapon(initial_weapon_instance) 

    if EspadaBrasas is not None and hasattr(jogador, 'add_owned_weapon'):
        try:
            segunda_arma = EspadaBrasas()
            jogador.add_owned_weapon(segunda_arma)
        except Exception as e:
            print(f"DEBUG(Game): Erro ao adicionar segunda arma para teste: {e}")

    estacoes = Estacoes() if Estacoes is not None else None
    gramas, arvores, blocos_gerados = [], [], set()
    
    if GerenciadorDeInimigos is not None and estacoes is not None:
        gerenciador_inimigos = GerenciadorDeInimigos(estacoes_obj=estacoes, tela_largura=largura_tela, altura_tela=altura_tela)
        if jogador and hasattr(jogador, 'rect'): 
            if hasattr(gerenciador_inimigos, 'spawn_inimigos_iniciais'):
                 gerenciador_inimigos.spawn_inimigos_iniciais(jogador) 
            elif hasattr(gerenciador_inimigos, 'spawn_inimigos'): 
                 gerenciador_inimigos.spawn_inimigos(jogador)
    else:
        gerenciador_inimigos = None
        print("DEBUG(Game): GerenciadorDeInimigos não pôde ser inicializado.")

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
    
    if BarraInventario and jogador and hasattr(jogador, 'owned_weapons'):
        margem_borda_x = 20
        margem_borda_y = 20
        slot_tamanho_barra = 55 
        
        barra_inv_x = margem_borda_x
        barra_inv_y = altura_tela - slot_tamanho_barra - margem_borda_y
        
        barra_inventario = BarraInventario(barra_inv_x, barra_inv_y, largura_tela, altura_tela, num_slots=4, slot_tamanho=(slot_tamanho_barra, slot_tamanho_barra))
        print("DEBUG(Game): Barra de Inventário (Armas) inicializada.")

        if ItemInventario and project_root_dir: 
            for i in range(min(len(jogador.owned_weapons), barra_inventario.num_slots)):
                arma_para_slot = jogador.owned_weapons[i]
                if arma_para_slot: 
                    if hasattr(barra_inventario, 'adicionar_arma'): # Verifica se o método existe
                        barra_inventario.adicionar_arma(arma_para_slot, slot_desejado=i)
                    else: # Fallback se o método for adicionar_item
                        icone_path = getattr(arma_para_slot, 'ui_icon_path', None)
                        if icone_path and not os.path.isabs(icone_path): 
                            icone_path_completo = os.path.join(project_root_dir, icone_path)
                            if not os.path.exists(icone_path_completo):
                                print(f"AVISO(Game): Ícone para {arma_para_slot.name} não encontrado em {icone_path_completo}")
                                icone_path_completo = None 
                        else:
                            icone_path_completo = icone_path 
                        item_para_barra = ItemInventario(arma_para_slot.name, 1, icone_path_completo, item_id=arma_para_slot.name)
                        barra_inventario.adicionar_item(item_para_barra, slot_especifico=i)
            
    else:
        barra_inventario = None
        print("DEBUG(Game): Aviso: Classe BarraInventario não disponível ou jogador sem inventário.")

    vida_jogador_ref = jogador.vida if hasattr(jogador, 'vida') and jogador.vida is not None else None
    if vida_jogador_ref is None and Vida is not None: 
        print("DEBUG(Game): Atenção! jogador.vida é None, criando instância de Vida separada para referência.")
        vida_max_jogador = getattr(jogador, 'vida_maxima', 150) 
        vida_jogador_ref = Vida(vida_maxima=vida_max_jogador)
        if hasattr(jogador, 'vida'): 
            jogador.vida = vida_jogador_ref

    print("DEBUG(Game): Saindo de inicializar_jogo().") 
    return jogador, estacoes, vida_jogador_ref, gramas, arvores, blocos_gerados, gerenciador_inimigos, False, tempo_inicio, timer_obj, barra_inventario


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


def desenhar_cena(janela, est, gramas, arvores, jogador_obj, gerenciador_inimigos, vida_jogador_obj_param, 
                  barra_inventario_obj, camera_x, camera_y, tempo_decorrido, timer_obj, dt_ms): 
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
    
    if vida_jogador_obj_param and hasattr(vida_jogador_obj_param, 'desenhar'): 
        vida_jogador_obj_param.desenhar(janela, 20, 20)
        
    if timer_obj and hasattr(timer_obj, 'desenhar'): timer_obj.desenhar(janela, tempo_decorrido)
    if xp_manager and hasattr(xp_manager, 'draw'): xp_manager.draw(janela)

    if barra_inventario_obj and hasattr(barra_inventario_obj, 'desenhar') and jogador_obj:
        barra_inventario_obj.desenhar(janela, jogador_obj)


def main():
    global jogador, game_music_volume, game_sfx_volume, pause_manager, game_is_running_flag, xp_manager, barra_inventario, jogo_pausado_para_inventario, gerenciador_inimigos

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
        
        jogador, est, vida_jogador_ref, gramas, arvores, blocos_gerados, gerenciador_inimigos, jogador_morreu, tempo_inicio, timer_obj, barra_inventario = inicializar_jogo(largura_tela, altura_tela)
        print(f"DEBUG(Game): inicializar_jogo() retornou. Jogador: {jogador}, Vida Ref: {vida_jogador_ref}, BarraInv: {barra_inventario}") 
        
        if jogador is None: 
            print("DEBUG(Game): Falha crítica ao inicializar o jogador. Encerrando.")
            pygame.quit()
            sys.exit()

        tocar_musica_jogo()
        game_state = "playing" 
        game_is_running_flag = True

        running = True
        print("DEBUG(Game): Entrando no loop principal do jogo (while running)...") 
        while running:
            dt_ms = clock.get_rawtime() 

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: running = False
                if evento.type == pygame.KEYDOWN:
                    print(f"DEBUG(Game.py) KEYDOWN Event: {pygame.key.name(evento.key)}") # DEBUG ATIVO
                    if evento.key == pygame.K_ESCAPE:
                        if jogo_pausado_para_inventario and barra_inventario: 
                            print("DEBUG(Game): ESC pressionado com inventário aberto. Fechando inventário.") # DEBUG
                            barra_inventario.toggle_visao_inventario(jogador)
                            jogo_pausado_para_inventario = False 
                            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                                pygame.mixer.music.unpause()
                            print("DEBUG(Game): Inventário fechado com ESC, jogo retomado.")
                        elif game_state == "playing" and pause_manager: 
                            print("DEBUG(Game): ESC pressionado. Abrindo menu de pausa.") # DEBUG
                            action, new_music_vol, new_sfx_vol = pause_manager.show_menu()
                            game_music_volume, game_sfx_volume = new_music_vol, new_sfx_vol
                            if action == "main_menu": running = False; acao_menu = "main_menu_from_pause"; break 
                            elif action == "quit": running = False; break
                    
                    elif evento.key == pygame.K_TAB and game_state == "playing": 
                        print(f"DEBUG(Game): TAB pressionado. game_state='{game_state}'") # DEBUG
                        if barra_inventario and jogador: 
                            print(f"DEBUG(Game): Chamando toggle_visao_inventario. Estado atual: {barra_inventario.visao_inventario_aberta}") # DEBUG
                            barra_inventario.toggle_visao_inventario(jogador)
                            jogo_pausado_para_inventario = barra_inventario.visao_inventario_aberta
                            print(f"DEBUG(Game): Novo estado visao_inventario_aberta: {barra_inventario.visao_inventario_aberta}, jogo_pausado_para_inventario: {jogo_pausado_para_inventario}") # DEBUG
                            if jogo_pausado_para_inventario:
                                if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                                    pygame.mixer.music.pause()
                                print("DEBUG(Game): Inventário aberto com TAB, jogo pausado.")
                            else:
                                if pygame.mixer.get_init(): 
                                     pygame.mixer.music.unpause()
                                print("DEBUG(Game): Inventário fechado com TAB, jogo retomado.")
                        # else:
                            # print("DEBUG(Game): Barra de inventário ou jogador não disponível para TAB.") # DEBUG
                    
                    if barra_inventario and game_state == "playing" and jogador: 
                        # Passa o input para a barra de inventário APENAS se não for TAB (para evitar processamento duplo)
                        # A barra de inventário já lida com 1-4 para equipar.
                        if evento.key != pygame.K_TAB:
                             barra_inventario.handle_input(evento, jogador)
                
            if not running: break 
            
            teclas = pygame.key.get_pressed() 
            
            if game_state == "playing" and not jogo_pausado_para_inventario: 
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
                        print(f"DEBUG(Game): Mudança de estação para {est.nome_estacao()}")
                        if arvores:
                            for arv in arvores:
                                if arv and hasattr(arv, 'atualizar_sprite'): arv.atualizar_sprite(est.i)
                        if gerenciador_inimigos:
                            if hasattr(gerenciador_inimigos, 'resetar_temporizador_spawn_estacao'):
                                gerenciador_inimigos.resetar_temporizador_spawn_estacao()
                            if jogador and hasattr(jogador, 'rect'):
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
                    
                    if loja_core and hasattr(loja_core, 'run_shop_scene'):
                        if pygame.mixer.get_init() and pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                        
                        should_continue_main_game = loja_core.run_shop_scene(janela, jogador, largura_tela, altura_tela)
                        
                        if pygame.mixer.get_init():
                            if pygame.mixer.music.get_busy(): pygame.mixer.music.unpause()
                            else: tocar_musica_jogo() 
                        
                        if not should_continue_main_game: running = False 
                        
                        if shop_elements and hasattr(shop_elements, 'reset_shop_spawn'):
                            shop_elements.reset_shop_spawn()

            # Desenha a cena principal sempre. A barra de inventário se sobrepõe se estiver aberta.
            camera_x = jogador.rect.centerx - largura_tela // 2 if jogador and hasattr(jogador, 'rect') else 0
            camera_y = jogador.rect.centery - altura_tela // 2 if jogador and hasattr(jogador, 'rect') else 0
            tempo_decorrido_segundos = (pygame.time.get_ticks() - tempo_inicio) // 1000 if tempo_inicio else 0
            desenhar_cena(janela, est, gramas, arvores, jogador, gerenciador_inimigos, vida_jogador_ref, barra_inventario, camera_x, camera_y, tempo_decorrido_segundos, timer_obj, dt_ms)

            pygame.display.flip()
            clock.tick(60) 

        game_is_running_flag = False 
        
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
    
    game_is_running_flag = False 
    
    if gerenciador_inimigos and hasattr(gerenciador_inimigos, 'stop_threads'): 
        gerenciador_inimigos.stop_threads()

    if pygame.mixer.get_init(): pygame.mixer.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
