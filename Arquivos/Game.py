# Arquivo: Game.py (Finalizado com a Lógica da Boss Fight e Reset)

import os
import sys
import traceback  # Importa o módulo traceback

import pygame

# --- Configuração do sys.path ---
# Garante que os módulos do projeto possam ser encontrados
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
project_root_dir = os.path.dirname(current_dir)
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

# --- Importações Essenciais ---
try:
    from Creditos import exibir_creditos
except ImportError:
    # print("AVISO (Game.py): Não foi possível importar 'exibir_creditos' do arquivo 'creditos.py'. A opção não funcionará.")
    def exibir_creditos(tela, clock): # Função placeholder para evitar erros
        # print("ERRO: A função de créditos não pôde ser carregada.")
        pass

try:
    from importacoes import *
    import loja as loja_core 
    from inventario_barra import BarraInventario
    from cogumelo import Cogumelo
    from gerador_cogumelo import GeradorCogumelos
    from eventos_climaticos import GerenciadorDeEventos
    from Luta_boss import *
    from Luta_boss import resetar_estado_luta_boss
    from XPs_Orb import XPOrb 
    from GeradorXP import GeradorXP 
    import shop_elements
except ImportError as e:
    # print(f"ERRO CRÍTICO (Game.py): Falha ao importar módulos essenciais: {e}")
    # traceback.print_exc() # Imprime o rastreamento completo do erro
    # Define fallbacks para evitar crashes imediatos
    Player, PauseMenuManager, XPManager, Menu, GerenciadorDeInimigos, Estacoes, Grama, Arvore, Timer, shop_elements, run_death_screen, Vida, ItemInventario, GerenciadorMoedas = (None,) * 14
    loja_core = None 
    AdagaFogo = None
    BarraInventario = None
    Cogumelo = None
    GeradorCogumelos = None
    GerenciadorDeEventos = None
    resetar_estado_luta_boss = None
    XPOrb = None 
    GeradorXP = None


# --- Constantes e Configurações Globais ---
MUSICAS_JOGO = [
    os.path.join(project_root_dir, "Musica", "Gameplay", "Faixa 1.mp3"),
    os.path.join(project_root_dir, "Musica", "Gameplay", "Faixa 2.mp3"),
    os.path.join(project_root_dir, "Musica", "Gameplay", "Faixa 3.mp3"),
    os.path.join(project_root_dir, "Musica", "Gameplay", "Faixa 4.mp3"),
    os.path.join(project_root_dir, "Musica", "Gameplay", "Faixa 5.mp3"),
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
jogo_pausado = False # FLAG DE PAUSE UNIFICADA
musica_gameplay_atual_path = None
musica_gameplay_atual_pos_ms = 0
gerador_cogumelos = None
gerador_xp = None
gerenciador_eventos = None

def inicializar_jogo(largura_tela, altura_tela):
    """Prepara todos os objetos e variáveis para uma nova sessão de jogo."""
    global jogador, pause_manager, xp_manager, barra_inventario, gerenciador_inimigos, \
           musica_gameplay_atual_path, musica_gameplay_atual_pos_ms, gerenciador_de_moedas, \
           gerador_cogumelos, gerenciador_eventos, gerador_xp

    if resetar_estado_luta_boss:
        resetar_estado_luta_boss()
    
    tempo_inicio_func = pygame.time.get_ticks()

    if Player is None:
        # print("ERRO CRÍTICO (Game.py): Classe Player não carregada.")
        # Garante que as variáveis de retorno sejam inicializadas para evitar UnboundLocalError
        return None, None, None, [], [], set(), \
               None, False, tempo_inicio_func, None, None, \
               None, None, None

    jogador = Player(velocidade=5, vida_maxima=150)
    jogador.x = float(largura_tela // 2)
    jogador.y = float(altura_tela // 2)

    if GerenciadorMoedas:
        # Passa a referência do jogador, que é necessária
        gerenciador_de_moedas = GerenciadorMoedas(jogador_ref=jogador)
    else:
        gerenciador_de_moedas = None

    if XPManager:
        xp_manager = XPManager(player_ref=jogador, largura_tela=largura_tela, altura_tela=altura_tela)
        if hasattr(jogador, 'xp_manager'):
            jogador.xp_manager = xp_manager
            # Adiciona uma referência ao jogo no xp_manager para acesso futuro
            xp_manager.game_ref = {
                'gerenciador_inimigos': None # Será definido após a criação
            }

    estacoes = Estacoes(largura_tela, altura_tela) if Estacoes else None
    
    if GerenciadorDeEventos and estacoes:
        gerenciador_eventos = GerenciadorDeEventos(largura_tela, altura_tela, estacoes)
    else:
        gerenciador_eventos = None

    # Inicialização garantida de gramas, arvores e blocos_gerados
    gramas, arvores, blocos_gerados = [], [], set()

    if GerenciadorDeInimigos and estacoes:
        gerenciador_inimigos = GerenciadorDeInimigos(
            estacoes_obj=estacoes,
            tela_largura=largura_tela,
            altura_tela=altura_tela,
            gerenciador_moedas_ref=gerenciador_de_moedas
        )
        if jogador:
            gerenciador_inimigos.spawn_inimigos_iniciais(jogador)
        # Atualiza a referência no xp_manager após a criação do gerenciador de inimigos
        if xp_manager:
            xp_manager.game_ref['gerenciador_inimigos'] = gerenciador_inimigos
    
    timer_obj = Timer(largura_tela // 2 - 60, 25) if Timer else None

    if shop_elements:
        shop_elements.reset_shop_spawn()

    if PauseMenuManager:
        pause_manager = PauseMenuManager(pygame.display.get_surface(), largura_tela, altura_tela,
                                         main, main, game_music_volume, game_sfx_volume)

    if BarraInventario and jogador:
        barra_inventario = BarraInventario(25, altura_tela - 75, largura_tela, altura_tela)
    else:
        barra_inventario = None

    vida_jogador_ref = getattr(jogador, 'vida', None)
    
    musica_gameplay_atual_path = None
    musica_gameplay_atual_pos_ms = 0

    if GeradorCogumelos:
        gerador_cogumelos = GeradorCogumelos()
    else:
        gerador_cogumelos = None

    if GeradorXP:
        gerador_xp = GeradorXP()
    else:
        gerador_xp = None

    return jogador, estacoes, vida_jogador_ref, gramas, arvores, blocos_gerados, \
           gerenciador_inimigos, False, tempo_inicio_func, timer_obj, barra_inventario, \
           gerador_cogumelos, gerenciador_eventos, gerador_xp


def gerar_elementos_ao_redor_do_jogador(jogador_obj, gramas_lista, arvores_lista, estacoes_obj, blocos_ja_gerados_set, gerador_cogumelos_obj):
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
                
                if gerador_cogumelos_obj:
                    gerador_cogumelos_obj.tentar_gerar_cogumelo(jogador_obj.rect, blocos_ja_gerados_set)

def tocar_musica_jogo():
    global game_music_volume, musica_gameplay_atual_path, musica_gameplay_atual_pos_ms
    if not MUSICAS_JOGO or not pygame.mixer.get_init(): return
    
    if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()
        
    musica_path_escolhida = random.choice(MUSICAS_JOGO)
    try:
        pygame.mixer.music.load(musica_path_escolhida)
        pygame.mixer.music.set_volume(game_music_volume)
        pygame.mixer.music.play(-1)
        musica_gameplay_atual_path = musica_path_escolhida
        musica_gameplay_atual_pos_ms = 0
    except Exception as e:
        # print(f"ERRO (Game.py): Ao tocar música '{musica_path_escolhida}': {e}")
        musica_gameplay_atual_path = None

def verificar_colisoes_com_inimigos(gerenciador_obj, jogador_obj):
    if not (jogador_obj and getattr(jogador_obj, 'vida') and jogador_obj.esta_vivo() and jogador_obj.pode_levar_dano):
        return
    
    jogador_col_rect = getattr(jogador_obj, 'rect_colisao', jogador_obj.rect)
    if not (gerenciador_obj and hasattr(gerenciador_obj, 'inimigos')): return

    for inimigo in list(gerenciador_obj.inimigos):
        if inimigo and inimigo.esta_vivo():
            dano_contato = getattr(inimigo, 'contact_damage', 0)
            if dano_contato > 0:
                inimigo_col_rect = getattr(inimigo, 'rect_colisao', inimigo.rect)
                if inimigo_col_rect and jogador_col_rect.colliderect(inimigo_col_rect):
                    jogador_obj.receber_dano(dano_contato, inimigo_col_rect)

def verificar_colisao_orbes_xp(jogador_obj, gerador_xp_obj):
    if not all([jogador_obj, gerador_xp_obj, jogador_obj.xp_manager]):
        return
    
    orbes_coletadas = pygame.sprite.spritecollide(jogador_obj, gerador_xp_obj.orbes, True, pygame.sprite.collide_circle_ratio(0.8))
    
    for orbe in orbes_coletadas:
        jogador_obj.xp_manager.gain_xp(orbe.xp_value)

# MODIFICAÇÃO: Função dedicada para atualizar as árvores
def atualizar_todas_as_arvores(lista_de_arvores, nova_estacao_idx):
    """
    Função auxiliar que percorre a lista de árvores e comanda cada uma
    a atualizar seu sprite para a nova estação.
    """
    if not lista_de_arvores:
        return
    # print(f"COMANDO: Atualizando {len(lista_de_arvores)} árvores para o índice de estação {nova_estacao_idx}.")
    for arvore in lista_de_arvores:
        if hasattr(arvore, 'atualizar_sprite'):
            arvore.atualizar_sprite(nova_estacao_idx)
    # print("Atualização das árvores concluída.")


def desenhar_cena(janela_surf, estacoes_obj, gramas_lista, arvores_lista, jogador_obj,
                  gerenciador_inimigos_obj, vida_ui_obj, barra_inventario_ui,
                  cam_x, cam_y, tempo_decorrido_seg, timer_ui_obj, delta_time_ms, jogo_pausado_flag,
                  gerador_cogumelos_obj, gerenciador_eventos_obj, gerador_xp_obj):
    global xp_manager, gerenciador_de_moedas

    if not esta_luta_ativa():
        if estacoes_obj:
            estacoes_obj.desenhar(janela_surf, cam_x, cam_y)

        for grama in gramas_lista:
            grama.desenhar(janela_surf, cam_x, cam_y)

        sprites_do_mundo = []
        if jogador_obj:
            sprites_do_mundo.append(jogador_obj)
        if gerenciador_inimigos_obj:
            sprites_do_mundo.extend(gerenciador_inimigos_obj.inimigos)
        if gerador_cogumelos_obj and hasattr(gerador_cogumelos_obj, 'cogumelos'):
            sprites_do_mundo.extend(gerador_cogumelos_obj.cogumelos)
        
        if gerador_xp_obj and hasattr(gerador_xp_obj, 'orbes'):
            sprites_do_mundo.extend(gerador_xp_obj.orbes)
        
        sprites_do_mundo.extend(arvores_lista)

        sprites_do_mundo.sort(key=lambda sprite: sprite.rect.bottom)

        for sprite in sprites_do_mundo:
            if XPOrb and isinstance(sprite, XPOrb):
                sprite.desenhar(janela_surf, cam_x, cam_y)
            elif hasattr(sprite, 'desenhar'):
                sprite.desenhar(janela_surf, cam_x, cam_y)

        if shop_elements:
            shop_elements.draw_shop_elements(janela_surf, cam_x, cam_y, delta_time_ms)


    if esta_luta_ativa():
        desenhar_efeitos_arena(janela_surf, cam_x, cam_y)
    
    if gerenciador_inimigos_obj:
        gerenciador_inimigos_obj.desenhar_projeteis_inimigos(janela_surf, cam_x, cam_y)
    
    if jogador_obj and hasattr(jogador_obj, 'draw_projectiles'):
        jogador_obj.draw_projectiles(janela_surf, cam_x, cam_y)

    if gerenciador_eventos_obj:
        gerenciador_eventos_obj.desenhar(janela_surf)

    # UI
    if vida_ui_obj:
        vida_ui_obj.desenhar(janela_surf, 20, 20)
    if estacoes_obj:
        estacoes_obj.desenhar_mensagem_estacao(janela_surf)
    if timer_ui_obj:
        timer_ui_obj.desenhar(janela_surf, tempo_decorrido_seg)
    if xp_manager:
        xp_manager.draw(janela_surf)
    
    if not jogo_pausado_flag and barra_inventario_ui and jogador_obj:
        barra_inventario_ui.desenhar(janela_surf, jogador_obj)

def main():
    global jogador, game_music_volume, game_sfx_volume, pause_manager, game_is_running_flag, \
           xp_manager, barra_inventario, jogo_pausado, gerenciador_inimigos, \
           musica_gameplay_atual_path, musica_gameplay_atual_pos_ms, gerenciador_de_moedas, \
           gerador_cogumelos, gerenciador_eventos, gerador_xp

    pygame.init()
    if not pygame.font.get_init(): pygame.font.init()

    mixer_initialized = False
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(32)
        mixer_initialized = True
    except pygame.error as e:
        pass

    try:
        info = pygame.display.Info()
        largura_tela, altura_tela = info.current_w, info.current_h
        janela = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN | pygame.SCALED)
    except Exception:
        largura_tela, altura_tela = 1280, 720
        janela = pygame.display.set_mode((largura_tela, altura_tela), pygame.RESIZABLE)
    
    pygame.display.set_caption("Lenda de Asrahel")
    clock = pygame.time.Clock()

    while True: # Loop do Menu Principal
        menu_obj = Menu(largura_tela, altura_tela) if Menu else None
        if not menu_obj: break

        menu_em_execucao = True
        while menu_em_execucao:
            mouse_pos = pygame.mouse.get_pos()
            menu_obj.desenhar(janela, mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_em_execucao = False
                    game_is_running_flag = False
                
                menu_obj.handle_event(event) # Para sliders de volume

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    acao_clicada = menu_obj.verificar_click(*event.pos)
                    if acao_clicada == "jogar":
                        menu_em_execucao = False
                        game_is_running_flag = True
                    elif acao_clicada == "sair":
                        menu_em_execucao = False
                        game_is_running_flag = False
                    elif acao_clicada == "creditos":
                        exibir_creditos(janela, clock)
                        menu_obj.tocar_proxima_musica()
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and menu_obj.estado == 'opcoes':
                    menu_obj.estado = 'principal'
            
            if not game_is_running_flag:
                break
        
        if not game_is_running_flag:
            break

        # Inicia o jogo
        if menu_obj: menu_obj.parar_musica()

        jogador, est, vida_jogador_ref, gramas, arvores, blocos_gerados, \
        gerenciador_inimigos, jogador_morreu, tempo_inicio, timer_obj, \
        barra_inventario, gerador_cogumelos, gerenciador_eventos, gerador_xp = inicializar_jogo(largura_tela, altura_tela)
        
        if jogador is None: break
        if Luta_boss is None: 
            break

        if mixer_initialized: tocar_musica_jogo()
        
        running_loop = True
        while running_loop:
            dt_ms = clock.tick(60)
            
            cam_x = jogador.rect.centerx - largura_tela // 2
            cam_y = jogador.rect.centery - altura_tela // 2

            # --- LÓGICA DE EVENTOS E PAUSA ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_loop = False
                    game_is_running_flag = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if jogo_pausado and barra_inventario.visao_inventario_aberta:
                            barra_inventario.toggle_visao_inventario(jogador)
                            jogo_pausado = False
                            if mixer_initialized: pygame.mixer.music.unpause()
                        elif not jogo_pausado:
                            if mixer_initialized: pygame.mixer.music.pause()
                            action, music_vol, sfx_vol = pause_manager.show_menu()
                            
                            game_music_volume, game_sfx_volume = music_vol, sfx_vol
                            
                            if action == "main_menu":
                                running_loop = False
                                break 
                            elif action == "quit":
                                running_loop = False
                                game_is_running_flag = False
                                break
                            else:
                                if mixer_initialized:
                                    pygame.mixer.music.set_volume(game_music_volume)
                                    pygame.mixer.music.unpause()
                    
                    elif event.key == pygame.K_TAB and barra_inventario:
                        barra_inventario.toggle_visao_inventario(jogador)
                        jogo_pausado = barra_inventario.visao_inventario_aberta
                        if jogo_pausado and mixer_initialized:
                            pygame.mixer.music.pause()
                        elif not jogo_pausado and mixer_initialized:
                            pygame.mixer.music.unpause()
                
                if barra_inventario and jogador:
                    barra_inventario.handle_input(event, jogador)
            
            if not running_loop: break

            # --- LÓGICA DE ATUALIZAÇÃO DO JOGO (SÓ RODA SE NÃO ESTIVER PAUSADO) ---
            if not jogo_pausado:
                teclas = pygame.key.get_pressed()
                jogador.update(dt_ms, teclas)
                
                if hasattr(jogador, 'update_projectiles'):
                    jogador.update_projectiles()
                
                if gerenciador_inimigos and jogador and hasattr(jogador, 'projeteis_ativos'):
                    for projetil in list(jogador.projeteis_ativos):
                        inimigos_atingidos = pygame.sprite.spritecollide(projetil, gerenciador_inimigos.inimigos, False)
                        if inimigos_atingidos:
                            inimigo = inimigos_atingidos[0]
                            if hasattr(inimigo, 'receber_dano'):
                                dano_do_projetil = getattr(projetil, 'dano', 0)
                                inimigo.receber_dano(dano_do_projetil)
                            projetil.kill()

                sinal_estacoes = est.atualizar_ciclo_estacoes() if est else None
                
                if sinal_estacoes == "INICIAR_LUTA_CHEFE" and not esta_luta_ativa():
                    if gerenciador_eventos: gerenciador_eventos.interromper_evento_climatico()
                    if shop_elements: shop_elements.despawn_loja_imediatamente()
                    iniciar_luta_chefe(
                        jogador=jogador, indice_estacao=est.indice_estacao_atual,
                        gerenciador_inimigos=gerenciador_inimigos, estacoes_obj=est,
                        largura_tela=largura_tela, altura_tela=altura_tela,
                        musica_atual_path=musica_gameplay_atual_path,
                        musica_atual_pos_ms=pygame.mixer.music.get_pos() if mixer_initialized else 0
                    )
                
                if gerenciador_inimigos:
                    gerenciador_inimigos.update_inimigos(jogador, dt_ms)
                    gerenciador_inimigos.update_projeteis_inimigos(jogador, dt_ms)

                if esta_luta_ativa():
                    sinal_luta = atualizar_luta(jogador, est, gerenciador_inimigos)
                    
                    # MODIFICAÇÃO: Lógica refatorada para atualizar as árvores
                    if sinal_luta == "FIM_DA_LUTA":
                        mudou_de_estacao = est.avancar_estacao_apos_chefe()
                        if mudou_de_estacao:
                            # Chama a função auxiliar para atualizar todas as árvores
                            atualizar_todas_as_arvores(arvores, est.indice_estacao_atual)
                        
                        if gerenciador_eventos: 
                            gerenciador_eventos.reativar_eventos_climaticos()

                    jogador.mover(teclas, [])
                    jogador.atacar(list(gerenciador_inimigos.inimigos), dt_ms)
                    verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador)
                else:
                    jogador.mover(teclas, arvores)
                    if gerenciador_eventos:
                        gerenciador_eventos.atualizar_clima()
                        gerenciador_eventos.atualizar_ciclo_dia_noite()
                        gerenciador_eventos.atualizar_particulas()
                    if gerenciador_inimigos:
                        gerenciador_inimigos.process_spawn_requests(jogador, dt_ms)

                    if gerador_cogumelos:
                        gerador_cogumelos.tentar_gerar_cogumelo(jogador.rect, blocos_gerados)
                        gerador_cogumelos.update(jogador, cam_x, cam_y, dt_ms)
                    
                    if gerador_xp:
                        gerador_xp.tentar_gerar_orbe(jogador.rect)
                        gerador_xp.update(dt_ms)
                        verificar_colisao_orbes_xp(jogador, gerador_xp)
                    
                    gerar_elementos_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados, gerador_cogumelos)
                    if gerenciador_inimigos:
                        jogador.atacar(list(gerenciador_inimigos.inimigos), dt_ms)
                    verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador)
                    
                    if shop_elements and loja_core and teclas[pygame.K_e]:
                        shop_rect = shop_elements.get_current_shop_rect()
                        if shop_rect and jogador.rect_colisao.colliderect(shop_rect):
                            jogo_pausado = True
                            if mixer_initialized: pygame.mixer.music.pause()
                            loja_core.run_shop_scene(janela, jogador, largura_tela, altura_tela)
                            if mixer_initialized: pygame.mixer.music.unpause()
                            shop_elements.reset_shop_spawn()
                            jogo_pausado = False

            # --- VERIFICAÇÕES FINAIS E DESENHO (RODAM MESMO SE PAUSADO) ---
            if not jogador.esta_vivo():
                jogador_morreu = True
                running_loop = False
            
            tempo_seg = (pygame.time.get_ticks() - tempo_inicio) // 1000
            desenhar_cena(janela, est, gramas, arvores, jogador, gerenciador_inimigos,
                          vida_jogador_ref, barra_inventario,
                          cam_x, cam_y, tempo_seg, timer_obj, dt_ms, jogo_pausado,
                          gerador_cogumelos, gerenciador_eventos, gerador_xp)

            if jogo_pausado and barra_inventario and barra_inventario.visao_inventario_aberta:
                barra_inventario.desenhar(janela, jogador)

            pygame.display.flip()

        if jogador_morreu and run_death_screen:
            run_death_screen(janela, main, main, DEATH_SCREEN_BACKGROUND_IMAGE)

    # --- FINALIZAÇÃO ---
    if 'gerenciador_inimigos' in locals() and gerenciador_inimigos:
        gerenciador_inimigos.stop_threads()
    if mixer_initialized:
        pygame.mixer.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        exc_text = traceback.format_exc()
        if pygame.get_init():
            if 'gerenciador_inimigos' in locals() and gerenciador_inimigos:
                gerenciador_inimigos.stop_threads()
            pygame.quit()
        with open("crash_log.txt", "w") as f:
            f.write("Um erro fatal ocorreu:\n")
            f.write(exc_text)
        sys.exit()
    # ... (outros métodos em Game.py) ...
    def _atualizar_logica(self):
        
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_clima_update > self.intervalo_clima:
            self.evento_climatico_atual = self.gerador_clima.gerar_evento_aleatorio()
            self.ultimo_clima_update = agora

        if not self.paused:
            dt = self.clock.get_time() / 1000.0  # Delta time em segundos

            self.jogador.update(self.teclas_pressionadas, self.arvores_group, dt)
            self.gerenciador_inimigos.update(self.jogador, self.camera_x, self.camera_y)
            self.jogador.projectiles.update()

            # --- ADICIONE ESTE BLOCO PARA FAZER A ARMA ATACAR ---
            if self.jogador.equipped_weapon:
                self.jogador.equipped_weapon.attack(self.gerenciador_inimigos.inimigos)
            # ----------------------------------------------------

            self.xp_manager.update(self.jogador)
            self.gerenciador_moedas.update(self.jogador)
            self.combate_manager.verificar_colisoes(self.jogador, self.gerenciador_inimigos.inimigos, self.gerenciador_moedas, self.xp_manager)

            self.camera_x = self.jogador.rect.centerx - self.largura // 2
            self.camera_y = self.jogador.rect.centery - self.altura // 2

            if self.evento_climatico_atual:
                self.evento_climatico_atual.update(self.tela)

# ... (resto do código) ...
