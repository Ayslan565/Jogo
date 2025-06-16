import pygame
import random
import sys
import os

# --- Configuração do sys.path ---
# Adiciona o diretório do projeto ao sys.path para facilitar importações relativas
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
project_root_dir = os.path.dirname(current_dir)
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

# --- Importações Essenciais ---
# Importa a função de créditos
try:
    from Creditos import exibir_creditos
except ImportError:
    print("AVISO (Game.py): Não foi possível importar 'exibir_creditos' do arquivo 'creditos.py'. A opção não funcionará.")
    def exibir_creditos(tela, clock): # Função placeholder para evitar erros
        
        print("ERRO: A função de créditos não pôde ser carregada.")
        pass

# Importa os módulos principais do jogo
try:
    from importacoes import *
    from inventario_barra import BarraInventario
except ImportError as e:
    print(f"ERRO CRÍTICO (Game.py): Falha ao importar módulos essenciais: {e}")
    # Define fallbacks para evitar crashes imediatos
    Player, PauseMenuManager, XPManager, Menu, GerenciadorDeInimigos, Estacoes, Grama, Arvore, Timer, shop_elements, run_death_screen, loja_core, Vida, ItemInventario, GerenciadorMoedas = (None,) * 15
    AdagaFogo = None
    BarraInventario = None

# --- Importação do ScoreManager ---
try:
    from Arquivos.Inimigos.score import ScoreManager
    score_manager = ScoreManager()
except ImportError:
    print("AVISO: Não foi possível importar ScoreManager.")
    score_manager = None

# --- Constantes e Configurações Globais do Jogo ---
MUSICAS_JOGO = [
    os.path.join(project_root_dir, "Musica", "Gameplay", "Faixa 1.mp3"),
    os.path.join(project_root_dir, "Musica", "Gameplay", "Faixa 2.mp3"),
    os.path.join(project_root_dir, "Musica", "Gameplay", "Faixa 3.mp3"),
]
DEATH_SCREEN_BACKGROUND_IMAGE = os.path.join(project_root_dir, "Sprites", "Backgrounds", "death_background.png")
game_music_volume = 0.3
game_sfx_volume = 0.5

# --- Variáveis Globais ---
jogador = None
pause_manager = None
xp_manager = None
barra_inventario = None
gerenciador_inimigos = None
gerenciador_de_moedas = None
game_is_running_flag = True
jogo_pausado_para_inventario = False
musica_gameplay_atual_path = None
musica_gameplay_atual_pos_ms = 0

def inicializar_jogo(largura_tela, altura_tela):
    """Prepara todos os objetos e variáveis para uma nova sessão de jogo."""
    global jogador, game_music_volume, pause_manager, xp_manager, barra_inventario, gerenciador_inimigos, \
           musica_gameplay_atual_path, musica_gameplay_atual_pos_ms, gerenciador_de_moedas
    
    tempo_inicio_func = pygame.time.get_ticks()

    if Player is None:
        print("ERRO CRÍTICO (Game.py): Classe Player não carregada.")
        return None, None, None, [], [], set(), None, True, tempo_inicio_func, None, None

    jogador = Player(velocidade=5, vida_maxima=150)
    jogador.x = float(largura_tela // 2)
    jogador.y = float(altura_tela // 2)
    if hasattr(jogador, 'rect'):
        jogador.rect.center = (int(jogador.x), int(jogador.y))
        jogador.rect_colisao = jogador.rect.inflate(-10, -10)

    if GerenciadorMoedas and hasattr(jogador, 'dinheiro'):
        gerenciador_de_moedas = GerenciadorMoedas(jogador_ref=jogador, fonte_path=None)
    
    if XPManager:
        xp_manager = XPManager(player_ref=jogador, largura_tela=largura_tela, altura_tela=altura_tela)
        if hasattr(jogador, 'xp_manager'):
            jogador.xp_manager = xp_manager

    if AdagaFogo and hasattr(jogador, 'add_owned_weapon'):
        jogador.add_owned_weapon(AdagaFogo())

    estacoes = Estacoes(largura_tela, altura_tela) if Estacoes else None
    
    gramas, arvores, blocos_gerados = [], [], set()

    if GerenciadorDeInimigos and estacoes:
        gerenciador_inimigos = GerenciadorDeInimigos(
            estacoes_obj=estacoes,
            tela_largura=largura_tela,
            altura_tela=altura_tela,
            gerenciador_moedas_ref=gerenciador_de_moedas
        )
        if jogador and hasattr(jogador, 'rect'):
            gerenciador_inimigos.spawn_inimigos_iniciais(jogador)
    
    timer_obj = None
    if Timer and pygame.font.get_init():
        try:
            fonte_timer = pygame.font.Font(None, 36)
            largura_fundo_timer = fonte_timer.size("00:00")[0] + 20
            timer_pos_x = largura_tela // 2 - largura_fundo_timer // 2
            timer_obj = Timer(timer_pos_x, 25)
        except Exception as e:
            print(f"AVISO (Game.py): Falha ao inicializar Timer: {e}")

    if shop_elements:
        shop_elements.reset_shop_spawn()

    if PauseMenuManager:
        pause_manager = PauseMenuManager(pygame.display.get_surface(), largura_tela, altura_tela,
                                         main, main, game_music_volume, game_sfx_volume)

    if BarraInventario and jogador and hasattr(jogador, 'owned_weapons'):
        barra_inv_x, barra_inv_y = 25, altura_tela - 75
        barra_inventario = BarraInventario(barra_inv_x, barra_inv_y, largura_tela, altura_tela, num_slots_hud=4)
    else:
        barra_inventario = None

    vida_jogador_ref = getattr(jogador, 'vida', None)
    if vida_jogador_ref is None and Vida:
        jogador.vida = Vida(getattr(jogador, 'vida_maxima', 150))
        vida_jogador_ref = jogador.vida
    
    musica_gameplay_atual_path = None
    musica_gameplay_atual_pos_ms = 0
    return jogador, estacoes, vida_jogador_ref, gramas, arvores, blocos_gerados, gerenciador_inimigos, False, tempo_inicio_func, timer_obj, barra_inventario

def gerar_elementos_ao_redor_do_jogador(jogador_obj, gramas_lista, arvores_lista, estacoes_obj, blocos_ja_gerados_set):
    if not all([jogador_obj, hasattr(jogador_obj, 'rect'), estacoes_obj, Grama, Arvore]):
        return
    
    bloco_tamanho_geracao = 1080
    jogador_bloco_x = int(jogador_obj.rect.centerx // bloco_tamanho_geracao)
    jogador_bloco_y = int(jogador_obj.rect.centery // bloco_tamanho_geracao)

    for dx_bloco in range(-1, 2):
        for dy_bloco in range(-1, 2):
            bloco_coord_atual = (jogador_bloco_x + dx_bloco, jogador_bloco_y + dy_bloco)
            if bloco_coord_atual not in blocos_ja_gerados_set:
                blocos_ja_gerados_set.add(bloco_coord_atual)
                base_x = bloco_coord_atual[0] * bloco_tamanho_geracao
                base_y = bloco_coord_atual[1] * bloco_tamanho_geracao
                
                for _ in range(random.randint(15, 25)):
                    gramas_lista.append(Grama(base_x + random.randint(0, bloco_tamanho_geracao),
                                              base_y + random.randint(0, bloco_tamanho_geracao), 50, 50))
                
                if hasattr(estacoes_obj, 'indice_estacao_atual'):
                    for _ in range(random.randint(1, 3)):
                        arvores_lista.append(Arvore(base_x + random.randint(270, 810),
                                                    base_y + random.randint(270, 810),
                                                    180, 180, estacoes_obj.indice_estacao_atual))
                
                if shop_elements:
                    shop_elements.spawn_shop_if_possible(jogador_obj, estacoes_obj, blocos_ja_gerados_set)

def tocar_musica_jogo():
    global game_music_volume, musica_gameplay_atual_path, musica_gameplay_atual_pos_ms
    if not MUSICAS_JOGO or not pygame.mixer.get_init():
        return
    
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        
    musica_path_escolhida = random.choice(MUSICAS_JOGO)
    try:
        pygame.mixer.music.load(musica_path_escolhida)
        pygame.mixer.music.set_volume(game_music_volume)
        pygame.mixer.music.play(-1)
        musica_gameplay_atual_path = musica_path_escolhida
        musica_gameplay_atual_pos_ms = 0
    except Exception as e:
        print(f"ERRO (Game.py): Ao tocar música '{musica_path_escolhida}': {e}")
        musica_gameplay_atual_path = None

def verificar_colisoes_com_inimigos(gerenciador_obj, jogador_obj):
    if not (jogador_obj and getattr(jogador_obj, 'vida', None) and jogador_obj.vida.esta_vivo() and getattr(jogador_obj, 'pode_levar_dano', True)):
        return
    
    jogador_col_rect = getattr(jogador_obj, 'rect_colisao', None)
    if not (jogador_col_rect and gerenciador_obj and hasattr(gerenciador_obj, 'inimigos')):
        return

    for inimigo in list(gerenciador_obj.inimigos):
        if inimigo and inimigo.esta_vivo():
            dano_contato = getattr(inimigo, 'contact_damage', 0)
            if dano_contato > 0:
                inimigo_col_rect = getattr(inimigo, 'rect_colisao', inimigo.rect)
                if inimigo_col_rect and jogador_col_rect.colliderect(inimigo_col_rect):
                    try:
                        jogador_obj.receber_dano(dano_contato, inimigo_col_rect)
                    except TypeError:
                        jogador_obj.receber_dano(dano_contato)

def desenhar_cena(janela_surf, estacoes_obj, gramas_lista, arvores_lista, jogador_obj,
                  gerenciador_inimigos_obj, vida_ui_obj, barra_inventario_ui,
                  cam_x, cam_y, tempo_decorrido_seg, timer_ui_obj, delta_time_ms, jogo_pausado_inv):
    global xp_manager, gerenciador_de_moedas

    janela_surf.fill((20, 20, 30))
    # --- MUDANÇA PRINCIPAL ---
    # Agora passamos as coordenadas da câmera para o método desenhar das estações.
    if estacoes_obj:
        estacoes_obj.desenhar(janela_surf, cam_x, cam_y)

    elementos_cenario = gramas_lista + arvores_lista
    for elemento in elementos_cenario:
        elemento.desenhar(janela_surf, cam_x, cam_y)
    
    if shop_elements:
        shop_elements.draw_shop_elements(janela_surf, cam_x, cam_y, delta_time_ms)

    if gerenciador_inimigos_obj:
        gerenciador_inimigos_obj.desenhar_inimigos(janela_surf, cam_x, cam_y)
        gerenciador_inimigos_obj.desenhar_projeteis_inimigos(janela_surf, cam_x, cam_y)

    if jogador_obj:
        # Assumindo que o método de desenhar do jogador também aceita a câmera
        jogador_obj.desenhar(janela_surf, cam_x, cam_y) 

    # --- ELEMENTOS DE UI (NÃO USAM CÂMERA) ---
    if vida_ui_obj:
        vida_ui_obj.desenhar(janela_surf, 20, 20)
    if estacoes_obj:
        estacoes_obj.desenhar_mensagem_estacao(janela_surf)
    if timer_ui_obj:
        timer_ui_obj.desenhar(janela_surf, tempo_decorrido_seg)
    if xp_manager:
        xp_manager.draw(janela_surf)
    
    # Só desenha o HUD da barra se o inventário completo não estiver aberto
    if not jogo_pausado_inv and barra_inventario_ui and jogador_obj:
        barra_inventario_ui.desenhar(janela_surf, jogador_obj)

    # --- EXIBE O SCORE NO LUGAR DAS MOEDAS ---
    if score_manager:
        largura_tela_atual = janela_surf.get_width()
        fonte_score = pygame.font.Font(None, 48)
        score_text = fonte_score.render(f"Score: {score_manager.get_score()}", True, (255, 215, 0))
        janela_surf.blit(score_text, (largura_tela_atual - 220, 20))
    # Se quiser remover moedas, não desenhe o HUD de moedas:
    # if gerenciador_de_moedas:
    #     largura_tela_atual = janela_surf.get_width()
    #     gerenciador_de_moedas.desenhar_hud_moedas(janela_surf, largura_tela_atual - 220, 20)

def main():
    global jogador, game_music_volume, game_sfx_volume, pause_manager, game_is_running_flag, \
           xp_manager, barra_inventario, jogo_pausado_para_inventario, gerenciador_inimigos, \
           musica_gameplay_atual_path, musica_gameplay_atual_pos_ms, gerenciador_de_moedas

    pygame.init()
    if not pygame.font.get_init(): pygame.font.init()

    mixer_initialized_successfully = False
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(32)
        mixer_initialized_successfully = True
    except pygame.error as e:
        print(f"AVISO (main): Falha ao inicializar pygame.mixer: {e}")

    try:
        info_display = pygame.display.Info()
        largura_tela_jogo, altura_tela_jogo = info_display.current_w, info_display.current_h
        janela_principal = pygame.display.set_mode((largura_tela_jogo, altura_tela_jogo), pygame.FULLSCREEN | pygame.SCALED)
    except Exception:
        largura_tela_jogo, altura_tela_jogo = 1280, 720
        janela_principal = pygame.display.set_mode((largura_tela_jogo, altura_tela_jogo), pygame.RESIZABLE)
    
    pygame.display.set_caption("Lenda de Asrahel")
    clock = pygame.time.Clock()

    while True: # Loop principal que controla o menu e o jogo
        menu_principal_obj = Menu(largura_tela_jogo, altura_tela_jogo) if Menu else None
        if not menu_principal_obj:
            print("ERRO CRÍTICO: Não foi possível criar o objeto do Menu. Saindo.")
            break

        acao_menu_principal = None
        while acao_menu_principal not in ["jogar", "sair"]:
            mouse_pos_menu = pygame.mouse.get_pos()
            menu_principal_obj.desenhar(janela_principal, mouse_pos_menu)
            
            for evento_menu in pygame.event.get():
                if evento_menu.type == pygame.QUIT:
                    acao_menu_principal = "sair"
                    break
                if evento_menu.type == pygame.MOUSEBUTTONDOWN and evento_menu.button == 1:
                    acao_clicada = menu_principal_obj.verificar_click(*evento_menu.pos)
                    if acao_clicada == "creditos":
                        exibir_creditos(janela_principal, clock)
                        menu_principal_obj.tocar_proxima_musica()
                    elif acao_clicada is not None:
                        acao_menu_principal = acao_clicada
                        break
            
            pygame.display.update()
            clock.tick(30)

        if acao_menu_principal == "sair":
            break # Sai do loop principal do programa

        # --- Início do Loop do Jogo ---
        if acao_menu_principal == "jogar":
            if menu_principal_obj:
                menu_principal_obj.parar_musica()

            jogador, est, vida_jogador_ref, gramas, arvores, blocos_gerados, \
            gerenciador_inimigos, jogador_morreu, tempo_inicio_jogo, timer_obj, \
            barra_inventario = inicializar_jogo(largura_tela_jogo, altura_tela_jogo)
            
            if jogador is None: break # Falha na inicialização

            if mixer_initialized_successfully:
                tocar_musica_jogo()

            game_state = "playing"
            running_game_loop = True

            while running_game_loop:
                delta_time_ms = clock.tick(60)
                
                if mixer_initialized_successfully and pygame.mixer.music.get_busy():
                    musica_gameplay_atual_pos_ms = pygame.mixer.music.get_pos()

                for evento_jogo in pygame.event.get():
                    if evento_jogo.type == pygame.QUIT:
                        running_game_loop = False
                        game_is_running_flag = False

                    if evento_jogo.type == pygame.KEYDOWN:
                        if evento_jogo.key == pygame.K_ESCAPE:
                            if jogo_pausado_para_inventario and barra_inventario:
                                barra_inventario.toggle_visao_inventario(jogador)
                                jogo_pausado_para_inventario = False
                                if mixer_initialized_successfully and musica_gameplay_atual_path:
                                    pygame.mixer.music.unpause()
                            elif game_state == "playing" and pause_manager:
                                if mixer_initialized_successfully: pygame.mixer.music.pause()
                                action_pause, new_music_vol, new_sfx_vol = pause_manager.show_menu()
                                game_music_volume, game_sfx_volume = new_music_vol, new_sfx_vol
                                if mixer_initialized_successfully:
                                    pygame.mixer.music.set_volume(game_music_volume)
                                    if action_pause == "resume_game":
                                        pygame.mixer.music.unpause()
                                if action_pause == "main_menu":
                                    running_game_loop = False 
                                    break
                                elif action_pause == "quit":
                                    running_game_loop = False
                                    game_is_running_flag = False
                                    break
                        
                        elif evento_jogo.key == pygame.K_TAB and game_state == "playing":
                            if barra_inventario and jogador:
                                barra_inventario.toggle_visao_inventario(jogador)
                                jogo_pausado_para_inventario = barra_inventario.visao_inventario_aberta
                                if jogo_pausado_para_inventario and mixer_initialized_successfully:
                                    pygame.mixer.music.pause()
                                elif not jogo_pausado_para_inventario and mixer_initialized_successfully:
                                    pygame.mixer.music.unpause()

                    if barra_inventario and game_state == "playing" and jogador:
                        barra_inventario.handle_input(evento_jogo, jogador)
                
                if not running_game_loop: break

                if game_state == "playing" and not jogo_pausado_para_inventario:
                    teclas_pressionadas = pygame.key.get_pressed()
                    if jogador:
                        jogador.mover(teclas_pressionadas, arvores)
                        jogador.update(delta_time_ms, teclas_pressionadas)
                    
                    if est:
                        if est.atualizar_ciclo_estacoes():
                            for arvore_obj in arvores:
                                arvore_obj.atualizar_sprite(est.indice_estacao_atual)
                            if gerenciador_inimigos:
                                gerenciador_inimigos.resetar_temporizador_spawn_estacao()
                                gerenciador_inimigos.spawn_inimigos_iniciais(jogador, delta_time_ms)
                    
                    if gerenciador_inimigos:
                        gerenciador_inimigos.process_spawn_requests(jogador, delta_time_ms)
                        gerenciador_inimigos.update_inimigos(jogador, delta_time_ms)
                        gerenciador_inimigos.update_projeteis_inimigos(jogador, delta_time_ms)

                    gerar_elementos_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados)
                    
                    if jogador and gerenciador_inimigos:
                        jogador.atacar(list(gerenciador_inimigos.inimigos), delta_time_ms)

                    if jogador and vida_jogador_ref:
                        verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador)
                        if not vida_jogador_ref.esta_vivo():
                            jogador_morreu = True
                            running_game_loop = False

                    if shop_elements and loja_core and jogador:
                        shop_rect = shop_elements.get_current_shop_rect()
                        if shop_rect and jogador.rect_colisao.colliderect(shop_rect) and teclas_pressionadas[pygame.K_e]:
                            if mixer_initialized_successfully: pygame.mixer.music.pause()
                            loja_core.run_shop_scene(janela_principal, jogador, largura_tela_jogo, altura_tela_jogo)
                            if mixer_initialized_successfully: pygame.mixer.music.unpause()
                            shop_elements.reset_shop_spawn()

                cam_x = jogador.rect.centerx - largura_tela_jogo // 2 if jogador else 0
                cam_y = jogador.rect.centery - altura_tela_jogo // 2 if jogador else 0
                tempo_total_seg = (pygame.time.get_ticks() - tempo_inicio_jogo) // 1000

                desenhar_cena(janela_principal, est, gramas, arvores, jogador, gerenciador_inimigos,
                              vida_jogador_ref, barra_inventario, 
                              cam_x, cam_y, tempo_total_seg, timer_obj, delta_time_ms, jogo_pausado_para_inventario)

                if jogo_pausado_para_inventario and barra_inventario:
                    barra_inventario.desenhar(janela_principal, jogador)

                pygame.display.flip()

            if jogador_morreu and run_death_screen:
                run_death_screen(janela_principal, main, main, DEATH_SCREEN_BACKGROUND_IMAGE)
                return 

    if 'gerenciador_inimigos' in locals() and gerenciador_inimigos:
        gerenciador_inimigos.stop_threads()
    if mixer_initialized_successfully:
        pygame.mixer.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e_main_fatal:
        import traceback
        traceback.print_exc()
        if pygame.get_init():
            if 'gerenciador_inimigos' in locals() and gerenciador_inimigos:
                gerenciador_inimigos.stop_threads()
            pygame.quit()
        input("Pressione Enter para sair após o erro fatal...")
        sys.exit(1)