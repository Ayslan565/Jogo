# Game.py
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

# --- Pré-definição de Nomes Globais como Fallback ---
# Inicializa variáveis globais como None.
# CORRIGIDO: O número de Nones agora corresponde ao número de variáveis (15).
Player, PauseMenuManager, XPManager, Menu, GerenciadorDeInimigos, Estacoes, Grama, Arvore, Timer, shop_elements, run_death_screen, loja_core, Vida, ItemInventario, GerenciadorMoedas = (None,) * 15
AdagaFogo, EspadaBrasas, MachadoCeruleo, MachadoMacabro, MachadoMarfim, MachadoBarbaro, EspadaFogoAzul, EspadaLua, EspadaCaida, EspadaPenitencia, MachadoBase = (None,) * 11
LaminaDoCeuCentilhante, MachadoDaDescidaSanta, MachadoDoFogoAbrasador = (None,) * 3
WeaponWheelUI = None
Luta_boss = None

# --- NOVA IMPORTAÇÃO DIRETA PARA BarraInventario ---
# Como Game.py e inventario_barra.py estão em Jogo/Arquivos/,
# tentamos uma importação direta.
BarraInventario = None # Inicializa como None para o caso de falha na importação abaixo
try:
    from inventario_barra import BarraInventario
    if BarraInventario is None: # Checagem adicional se a importação ocorreu mas resultou em None
         print("AVISO (Game.py): 'inventario_barra.BarraInventario' foi importado como None. Verifique o arquivo 'inventario_barra.py' por definições ou erros internos.")
except ImportError as e_barra_inv:
    print(f"ERRO CRÍTICO (Game.py): Falha ao importar 'BarraInventario' diretamente de 'inventario_barra.py': {e_barra_inv}")
    import traceback
    traceback.print_exc()
except Exception as e_geral_barra_inv:
    print(f"ERRO CRÍTICO (Game.py): Exceção geral ao importar 'BarraInventario': {e_geral_barra_inv}")
    import traceback
    traceback.print_exc()


# --- Importações Centralizadas (todas as outras, via importacoes.py) ---
try:
    from importacoes import * # Esta linha DEVE trazer GerenciadorMoedas e outras dependências
                              # mas BarraInventario agora é importada diretamente acima.
    if Luta_boss is None: # Se Luta_boss não foi importado por 'importacoes'
        try:
            import Luta_boss as LutaBossModule # Tenta importar Luta_boss diretamente
            Luta_boss = LutaBossModule
        except ImportError: pass # Ignora se a importação direta também falhar
except ImportError: # Se 'importacoes.py' falhar completamente
    try:
        if Luta_boss is None: # Mesmo assim, tenta importar Luta_boss
            import Luta_boss as LutaBossModule
            Luta_boss = LutaBossModule
    except ImportError: pass
except Exception: pass # Captura outras exceções genéricas durante a importação

try:
    if Player is None: # Se Player não foi importado por 'importacoes'
        from player import Player as PlayerLocal # Tenta importar Player diretamente
        Player = PlayerLocal
except ImportError: pass

# --- Constantes e Configurações Globais do Jogo ---
MUSICAS_JOGO = [
    os.path.join(project_root_dir, "Musica", "Gameplay", "Faixa 1.mp3"),
    os.path.join(project_root_dir, "Musica", "Gameplay", "Faixa 2.mp3"),
    os.path.join(project_root_dir, "Musica", "Gameplay", "Faixa 3.mp3"),
]
MUSICAS_CHEFE_PARA_MODULO = [
    os.path.join(project_root_dir, "Musica", "Boss Fight", "Faixa1.mp3"),
    os.path.join(project_root_dir, "Musica", "Boss Fight", "Faixa2.mp3"),
]
DEATH_SCREEN_BACKGROUND_IMAGE = os.path.join(project_root_dir, "Sprites", "Backgrounds", "death_background.png")
game_music_volume = 0.3
game_sfx_volume = 0.5

# Variáveis globais
jogador = None
pause_manager = None
xp_manager = None
# barra_inventario será inicializado em inicializar_jogo usando a classe BarraInventario importada diretamente
barra_inventario = None # Será instanciada em inicializar_jogo
gerenciador_inimigos = None
gerenciador_de_moedas = None
game_is_running_flag = True
jogo_pausado_para_inventario = False
musica_gameplay_atual_path = None
musica_gameplay_atual_pos_ms = 0

def inicializar_jogo(largura_tela, altura_tela):
    global jogador, game_music_volume, pause_manager, xp_manager, barra_inventario, gerenciador_inimigos, \
           musica_gameplay_atual_path, musica_gameplay_atual_pos_ms, gerenciador_de_moedas
    tempo_inicio_func = pygame.time.get_ticks()

    if Luta_boss and hasattr(Luta_boss, 'configurar_musicas_chefe'):
        Luta_boss.configurar_musicas_chefe(MUSICAS_CHEFE_PARA_MODULO)

    if Player is None:
        print("ERRO CRÍTICO (Game.py - inicializar_jogo): Classe Player não carregada.")
        return None, None, None, [], [], set(), None, True, tempo_inicio_func, None, None

    jogador = Player(velocidade=5, vida_maxima=150)
    jogador.x = float(largura_tela // 2)
    jogador.y = float(altura_tela // 2)
    if hasattr(jogador, 'rect'): jogador.rect.center = (int(jogador.x), int(jogador.y))

    if not hasattr(jogador, 'rect_colisao') and hasattr(jogador, 'rect'):
        jogador.rect_colisao = jogador.rect.inflate(-10,-10)
    elif not hasattr(jogador, 'rect'):
        print("ERRO CRÍTICO (Game.py - inicializar_jogo): Instância do Jogador não possui 'rect'.")
        return None, None, None, [], [], set(), None, True, tempo_inicio_func, None, None

    if GerenciadorMoedas is not None and Player is not None and hasattr(jogador, 'dinheiro'):
        gerenciador_de_moedas = GerenciadorMoedas(jogador_ref=jogador, fonte_path=None)
    else:
        gerenciador_de_moedas = None
        if GerenciadorMoedas is None: print("AVISO (Game.py - inicializar_jogo): Classe GerenciadorMoedas não disponível.")
        elif Player is None or not hasattr(jogador, 'dinheiro'): print("AVISO (Game.py - inicializar_jogo): Jogador ou atributo 'dinheiro' não definido para GerenciadorMoedas.")

    if XPManager is not None:
        xp_manager = XPManager(player_ref=jogador, largura_tela=largura_tela, altura_tela=altura_tela)
        if hasattr(jogador, 'xp_manager'): jogador.xp_manager = xp_manager
    else: xp_manager = None

    if AdagaFogo is not None and hasattr(jogador, 'add_owned_weapon') and callable(jogador.add_owned_weapon):
        try:
            jogador.add_owned_weapon(AdagaFogo())
        except Exception as e: print(f"AVISO (Game.py - inicializar_jogo): Falha ao adicionar AdagaFogo: {e}")

    estacoes = Estacoes() if Estacoes is not None else None
    gramas, arvores, blocos_gerados = [], [], set()

    if GerenciadorDeInimigos is not None and estacoes is not None:
        gerenciador_inimigos = GerenciadorDeInimigos(estacoes_obj=estacoes,
                                                     tela_largura=largura_tela,
                                                     altura_tela=altura_tela,
                                                     gerenciador_moedas_ref=gerenciador_de_moedas)
        if jogador and hasattr(jogador, 'rect') and hasattr(gerenciador_inimigos, 'spawn_inimigos_iniciais'):
            gerenciador_inimigos.spawn_inimigos_iniciais(jogador)
    else: gerenciador_inimigos = None

    timer_obj = None
    if Timer is not None and pygame.font.get_init():
        try:
            fonte_timer = pygame.font.Font(None, 36)
            largura_fundo_timer = fonte_timer.size("00:00")[0] + 20
            timer_pos_x = largura_tela // 2 - largura_fundo_timer // 2
            timer_obj = Timer(timer_pos_x, 25)
        except Exception as e: print(f"AVISO (Game.py - inicializar_jogo): Falha ao inicializar Timer: {e}")

    if shop_elements and hasattr(shop_elements, 'reset_shop_spawn'):
        shop_elements.reset_shop_spawn()

    if PauseMenuManager is not None:
        pause_manager = PauseMenuManager(pygame.display.get_surface(), largura_tela, altura_tela,
                                         main, main, game_music_volume, game_sfx_volume)
    else: pause_manager = None

    # Inicialização da barra_inventario usando a classe BarraInventario importada diretamente
    # A variável global `barra_inventario` será definida aqui.
    if BarraInventario and jogador and hasattr(jogador, 'owned_weapons'): # Verifica se BarraInventario foi importada com sucesso
        barra_inv_x, barra_inv_y = 25, altura_tela - 50 - 25
        # A variável global `barra_inventario` é atualizada aqui
        barra_inventario = BarraInventario(barra_inv_x, barra_inv_y, largura_tela, altura_tela, num_slots_hud=4)
        print(f"DEBUG (Game.py - inicializar_jogo): BarraInventario INICIALIZADA com sucesso. Objeto: {barra_inventario}")
    else:
        # barra_inventario já é None por padrão (global), apenas loga o motivo
        print("DEBUG (Game.py - inicializar_jogo): Falha ao inicializar BarraInventario (variável global permanece None). Condições:")
        if not BarraInventario: print("  - Classe BarraInventario é None (importação falhou no topo do Game.py).")
        if not jogador: print("  - Objeto jogador é None.")
        elif not hasattr(jogador, 'owned_weapons'): print("  - Jogador não possui 'owned_weapons'.")

    vida_jogador_ref = getattr(jogador, 'vida', None)
    if vida_jogador_ref is None and Vida is not None:
        vida_jogador_ref = Vida(getattr(jogador, 'vida_maxima', 150))
        if hasattr(jogador, 'vida'): jogador.vida = vida_jogador_ref

    musica_gameplay_atual_path = None; musica_gameplay_atual_pos_ms = 0
    # Retorna a instância de barra_inventario criada (ou None)
    return jogador, estacoes, vida_jogador_ref, gramas, arvores, blocos_gerados, gerenciador_inimigos, False, tempo_inicio_func, timer_obj, barra_inventario


def gerar_elementos_ao_redor_do_jogador(jogador_obj, gramas_lista, arvores_lista, estacoes_obj, blocos_ja_gerados_set):
    if not (jogador_obj and hasattr(jogador_obj, 'rect') and estacoes_obj and Grama and Arvore):
        return
    bloco_tamanho_geracao = 1080
    jogador_bloco_x = int(jogador_obj.rect.centerx // bloco_tamanho_geracao)
    jogador_bloco_y = int(jogador_obj.rect.centery // bloco_tamanho_geracao)
    for dx_bloco in range(-1, 2):
        for dy_bloco in range(-1, 2):
            bloco_coord_atual = (jogador_bloco_x + dx_bloco, jogador_bloco_y + dy_bloco)
            if bloco_coord_atual not in blocos_ja_gerados_set:
                blocos_ja_gerados_set.add(bloco_coord_atual)
                base_x_bloco = bloco_coord_atual[0] * bloco_tamanho_geracao
                base_y_bloco = bloco_coord_atual[1] * bloco_tamanho_geracao
                for _ in range(random.randint(15, 25)):
                    try:
                        gramas_lista.append(Grama(base_x_bloco + random.randint(0, bloco_tamanho_geracao),
                                                  base_y_bloco + random.randint(0, bloco_tamanho_geracao),
                                                  50, 50))
                    except Exception as e: print(f"AVISO (Game.py): Erro ao gerar grama: {e}")
                if hasattr(estacoes_obj, 'indice_estacao_atual'):
                    for _ in range(random.randint(1, 3)):
                        try:
                            arvores_lista.append(Arvore(base_x_bloco + random.randint(bloco_tamanho_geracao // 4, 3 * bloco_tamanho_geracao // 4),
                                                        base_y_bloco + random.randint(bloco_tamanho_geracao // 4, 3 * bloco_tamanho_geracao // 4),
                                                        180, 180, estacoes_obj.indice_estacao_atual))
                        except Exception as e: print(f"AVISO (Game.py): Erro ao gerar arvore: {e}")
                if shop_elements and hasattr(shop_elements, 'spawn_shop_if_possible'):
                    shop_elements.spawn_shop_if_possible(jogador_obj, estacoes_obj, blocos_ja_gerados_set)

def tocar_musica_jogo():
    global game_music_volume, musica_gameplay_atual_path, musica_gameplay_atual_pos_ms
    if not MUSICAS_JOGO: return
    if not pygame.mixer.get_init(): return
    if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()
    musica_path_escolhida = random.choice(MUSICAS_JOGO)
    try:
        pygame.mixer.music.load(musica_path_escolhida)
        pygame.mixer.music.set_volume(game_music_volume)
        pygame.mixer.music.play(-1)
        musica_gameplay_atual_path = musica_path_escolhida
        musica_gameplay_atual_pos_ms = 0
    except Exception as e:
        print(f"ERRO (Game.py) ao tocar música '{musica_path_escolhida}': {e}")
        musica_gameplay_atual_path = None

def verificar_colisoes_com_inimigos(gerenciador_inimigos_obj, jogador_obj):
    if not (jogador_obj and hasattr(jogador_obj, 'vida') and jogador_obj.vida and \
            hasattr(jogador_obj.vida, 'esta_vivo') and jogador_obj.vida.esta_vivo() and \
            hasattr(jogador_obj, 'receber_dano') and callable(jogador_obj.receber_dano) and \
            getattr(jogador_obj, 'pode_levar_dano', True)):
        return
    jogador_col_rect = getattr(jogador_obj, 'rect_colisao', getattr(jogador_obj, 'rect', None))
    if not (jogador_col_rect and gerenciador_inimigos_obj and hasattr(gerenciador_inimigos_obj, 'inimigos')):
        return
    for inimigo_atual in list(gerenciador_inimigos_obj.inimigos):
        if inimigo_atual and hasattr(inimigo_atual, 'rect') and hasattr(inimigo_atual, 'esta_vivo') and inimigo_atual.esta_vivo():
            dano_contato_inimigo = getattr(inimigo_atual, 'contact_damage', 0)
            if dano_contato_inimigo <= 0: continue
            inimigo_col_rect_atual = getattr(inimigo_atual, 'rect_colisao', inimigo_atual.rect)
            if inimigo_col_rect_atual and jogador_col_rect.colliderect(inimigo_col_rect_atual):
                try:
                    jogador_obj.receber_dano(dano_contato_inimigo, inimigo_col_rect_atual)
                except TypeError:
                    jogador_obj.receber_dano(dano_contato_inimigo)

def desenhar_cena(janela_surf, estacoes_obj, gramas_lista, arvores_lista, jogador_obj,
                  gerenciador_inimigos_obj, vida_ui_obj, barra_inventario_ui_arg, # Renomeado para evitar conflito com global
                  cam_x, cam_y, tempo_decorrido_seg, timer_ui_obj, delta_time_ms,
                  luta_boss_ativa_status):
    global xp_manager, Luta_boss, gerenciador_de_moedas

    janela_surf.fill((20, 20, 30))
    if estacoes_obj and hasattr(estacoes_obj, 'desenhar'): estacoes_obj.desenhar(janela_surf)

    if not luta_boss_ativa_status:
        elementos_cenario = gramas_lista + arvores_lista
        for elemento in elementos_cenario:
            if elemento and hasattr(elemento, 'desenhar'): elemento.desenhar(janela_surf, cam_x, cam_y)
        if shop_elements and hasattr(shop_elements, 'draw_shop_elements'):
            shop_elements.draw_shop_elements(janela_surf, cam_x, cam_y, delta_time_ms)

    if gerenciador_inimigos_obj:
        if hasattr(gerenciador_inimigos_obj, 'desenhar_inimigos') and not luta_boss_ativa_status:
            gerenciador_inimigos_obj.desenhar_inimigos(janela_surf, cam_x, cam_y)
        if hasattr(gerenciador_inimigos_obj, 'desenhar_chefe') and luta_boss_ativa_status:
            gerenciador_inimigos_obj.desenhar_chefe(janela_surf, cam_x, cam_y)
        if hasattr(gerenciador_inimigos_obj, 'desenhar_projeteis_inimigos'):
            gerenciador_inimigos_obj.desenhar_projeteis_inimigos(janela_surf, cam_x, cam_y)

    if jogador_obj and hasattr(jogador_obj, 'desenhar'): jogador_obj.desenhar(janela_surf, cam_x, cam_y)

    if luta_boss_ativa_status:
        arena_atual_local = Luta_boss.get_arena_rect() if Luta_boss else None
        if arena_atual_local:
            rect_arena_na_tela = arena_atual_local.move(-cam_x, -cam_y)
            s = pygame.Surface((rect_arena_na_tela.width, rect_arena_na_tela.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (150, 0, 0, 90), s.get_rect(), 7, border_radius=10)
            janela_surf.blit(s, rect_arena_na_tela.topleft)

        chefe_para_ui = Luta_boss.get_chefe_atual() if Luta_boss else None
        if chefe_para_ui and hasattr(chefe_para_ui, 'hp') and hasattr(chefe_para_ui, 'max_hp') and hasattr(chefe_para_ui, 'esta_vivo') and chefe_para_ui.esta_vivo():
            largura_barra_vida_chefe = janela_surf.get_width() * 0.6
            altura_barra_vida_chefe = 20
            x_barra_vida_chefe = (janela_surf.get_width() - largura_barra_vida_chefe) / 2
            y_barra_vida_chefe = 30
            percentual_vida_chefe = max(0, chefe_para_ui.hp / chefe_para_ui.max_hp)
            pygame.draw.rect(janela_surf, (100,0,0), (x_barra_vida_chefe, y_barra_vida_chefe, largura_barra_vida_chefe, altura_barra_vida_chefe))
            pygame.draw.rect(janela_surf, (255,0,0), (x_barra_vida_chefe, y_barra_vida_chefe, largura_barra_vida_chefe * percentual_vida_chefe, altura_barra_vida_chefe))
            pygame.draw.rect(janela_surf, (255,255,255), (x_barra_vida_chefe, y_barra_vida_chefe, largura_barra_vida_chefe, altura_barra_vida_chefe), 2)

    if vida_ui_obj and hasattr(vida_ui_obj, 'desenhar') and callable(vida_ui_obj.desenhar):
        vida_ui_obj.desenhar(janela_surf, 20, 20)

    if not luta_boss_ativa_status:
        if estacoes_obj and hasattr(estacoes_obj, 'desenhar_mensagem_estacao'):
            estacoes_obj.desenhar_mensagem_estacao(janela_surf)
        if timer_ui_obj and hasattr(timer_ui_obj, 'desenhar') and callable(timer_ui_obj.desenhar):
            timer_ui_obj.desenhar(janela_surf, tempo_decorrido_seg)
        if xp_manager and hasattr(xp_manager, 'draw') and callable(xp_manager.draw):
            xp_manager.draw(janela_surf)
        # Usa barra_inventario_ui_arg que é passado como argumento
        if barra_inventario_ui_arg and hasattr(barra_inventario_ui_arg, 'desenhar') and callable(barra_inventario_ui_arg.desenhar) and jogador_obj:
            barra_inventario_ui_arg.desenhar(janela_surf, jogador_obj)
        if gerenciador_de_moedas and hasattr(gerenciador_de_moedas, 'desenhar_hud_moedas'):
            largura_tela_atual = janela_surf.get_width()
            pos_x_moedas_hud = largura_tela_atual - 220
            pos_y_moedas_hud = 20
            gerenciador_de_moedas.desenhar_hud_moedas(janela_surf, pos_x_moedas_hud, pos_y_moedas_hud)


def main():
    global jogador, game_music_volume, game_sfx_volume, pause_manager, game_is_running_flag, \
           xp_manager, barra_inventario, jogo_pausado_para_inventario, gerenciador_inimigos, \
           musica_gameplay_atual_path, musica_gameplay_atual_pos_ms, Luta_boss, gerenciador_de_moedas

    pygame.init()
    if not pygame.font.get_init(): pygame.font.init()

    mixer_initialized_successfully = False
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(32)
        mixer_initialized_successfully = True
    except pygame.error as e: print(f"AVISO (main.py): Falha ao inicializar pygame.mixer: {e}")

    try:
        info_display = pygame.display.Info()
        largura_tela_jogo, altura_tela_jogo = info_display.current_w, info_display.current_h
        janela_principal = pygame.display.set_mode((largura_tela_jogo, altura_tela_jogo), pygame.FULLSCREEN | pygame.SCALED)
    except Exception:
        largura_tela_jogo, altura_tela_jogo = 1280, 720
        janela_principal = pygame.display.set_mode((largura_tela_jogo, altura_tela_jogo), pygame.RESIZABLE)
    pygame.display.set_caption("Lenda de Asrahel")
    clock = pygame.time.Clock()

    acao_menu_principal = "jogar"
    if Menu is not None:
        menu_principal_obj = Menu(largura_tela_jogo, altura_tela_jogo)
        acao_menu_principal = None
        while acao_menu_principal is None:
            mouse_pos_menu = pygame.mouse.get_pos()
            menu_principal_obj.desenhar(janela_principal, mouse_pos_menu)
            for evento_menu in pygame.event.get():
                if evento_menu.type == pygame.QUIT: pygame.quit(); sys.exit()
                if evento_menu.type == pygame.MOUSEBUTTONDOWN and evento_menu.button == 1:
                    if hasattr(menu_principal_obj, 'verificar_click'):
                        acao_menu_principal = menu_principal_obj.verificar_click(*evento_menu.pos)
                        if acao_menu_principal == "sair": break
            if acao_menu_principal == "sair": break
            pygame.display.update()
            clock.tick(30)

    if acao_menu_principal == "jogar":
        if Menu is not None and 'menu_principal_obj' in locals() and hasattr(menu_principal_obj, 'parar_musica'):
            menu_principal_obj.parar_musica()

        # A variável global `barra_inventario` será definida dentro de `inicializar_jogo`
        jogador, est, vida_jogador_ref, gramas, arvores, blocos_gerados, \
        gerenciador_inimigos, jogador_morreu, tempo_inicio_jogo, timer_obj, \
        _ = inicializar_jogo(largura_tela_jogo, altura_tela_jogo) # O último valor retornado é a instância de barra_inventario


        if jogador is None: pygame.quit(); sys.exit()
        if mixer_initialized_successfully and Luta_boss and not Luta_boss.esta_luta_ativa():
            tocar_musica_jogo()

        game_state = "playing"
        running_game_loop = True

        while running_game_loop:
            delta_time_ms = clock.tick(60)
            luta_boss_ativa_main = Luta_boss and Luta_boss.esta_luta_ativa()

            if mixer_initialized_successfully and pygame.mixer.music.get_busy() and not luta_boss_ativa_main:
                musica_gameplay_atual_pos_ms = pygame.mixer.music.get_pos()

            for evento_jogo in pygame.event.get():
                if evento_jogo.type == pygame.QUIT: running_game_loop = False; game_is_running_flag = False

                if evento_jogo.type == pygame.KEYDOWN:
                    if evento_jogo.key == pygame.K_ESCAPE:
                        if jogo_pausado_para_inventario and barra_inventario and not luta_boss_ativa_main:
                            barra_inventario.toggle_visao_inventario(jogador)
                            jogo_pausado_para_inventario = False
                            if mixer_initialized_successfully and musica_gameplay_atual_path and not pygame.mixer.music.get_busy():
                                pygame.mixer.music.unpause()
                            elif mixer_initialized_successfully and not pygame.mixer.music.get_busy():
                                tocar_musica_jogo()
                        elif game_state == "playing" and pause_manager and not luta_boss_ativa_main:
                            if mixer_initialized_successfully and pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                            action_pause, new_music_vol, new_sfx_vol = pause_manager.show_menu()
                            game_music_volume, game_sfx_volume = new_music_vol, new_sfx_vol
                            if mixer_initialized_successfully: pygame.mixer.music.set_volume(game_music_volume)
                            if action_pause == "resume_game" and mixer_initialized_successfully:
                                if musica_gameplay_atual_path and not pygame.mixer.music.get_busy(): pygame.mixer.music.unpause()
                                elif not pygame.mixer.music.get_busy(): tocar_musica_jogo()
                            elif action_pause == "main_menu": running_game_loop = False; acao_menu_principal = "main_menu_from_pause"; break
                            elif action_pause == "quit": running_game_loop = False; game_is_running_flag = False; break

                    elif evento_jogo.key == pygame.K_TAB and game_state == "playing" and not luta_boss_ativa_main:
                        if barra_inventario and jogador: # Usa a variável global barra_inventario
                            barra_inventario.toggle_visao_inventario(jogador)
                            jogo_pausado_para_inventario = barra_inventario.visao_inventario_aberta
                            if jogo_pausado_para_inventario:
                                if mixer_initialized_successfully and pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                            else:
                                if mixer_initialized_successfully:
                                    if musica_gameplay_atual_path and not pygame.mixer.music.get_busy(): pygame.mixer.music.unpause()
                                    elif not pygame.mixer.music.get_busy(): tocar_musica_jogo()

                    elif evento_jogo.key == pygame.K_F10 and Luta_boss and not luta_boss_ativa_main and \
                         jogador and est and gerenciador_inimigos and game_state == "playing":
                        if Luta_boss.iniciar_luta_chefe(jogador, 0, gerenciador_inimigos, est,
                                                      largura_tela_jogo, altura_tela_jogo,
                                                      musica_gameplay_atual_path, musica_gameplay_atual_pos_ms):
                            pass
                        else:
                            print("ERRO (main.py): Falha ao iniciar luta contra chefe via F10.")
                            if mixer_initialized_successfully and not pygame.mixer.music.get_busy() and musica_gameplay_atual_path:
                                tocar_musica_jogo()
                # Usa a variável global barra_inventario
                if barra_inventario and game_state == "playing" and jogador and not luta_boss_ativa_main:
                    barra_inventario.handle_input(evento_jogo, jogador)

            if not running_game_loop: break

            if game_state == "playing" and not (jogo_pausado_para_inventario and not luta_boss_ativa_main):
                teclas_pressionadas = pygame.key.get_pressed()
                if jogador:
                    if hasattr(jogador, 'mover'): jogador.mover(teclas_pressionadas, arvores)
                    if hasattr(jogador, 'update'): jogador.update(delta_time_ms, teclas_pressionadas)

                if luta_boss_ativa_main:
                    arena_atual = Luta_boss.get_arena_rect()
                    if arena_atual and jogador and hasattr(jogador, 'rect'):
                        jogador.rect.clamp_ip(arena_atual)
                        if hasattr(jogador, 'x') and hasattr(jogador, 'y'):
                            jogador.x = float(jogador.rect.centerx); jogador.y = float(jogador.rect.centery)

                    if Luta_boss: Luta_boss.atualizar_luta(jogador, est, gerenciador_inimigos)

                    if Luta_boss and Luta_boss.esta_luta_ativa():
                        chefe_obj = Luta_boss.get_chefe_atual()
                        if chefe_obj and hasattr(chefe_obj, 'esta_vivo') and chefe_obj.esta_vivo():
                            if gerenciador_inimigos and hasattr(gerenciador_inimigos, 'update_chefe'):
                                gerenciador_inimigos.update_chefe(jogador, delta_time_ms)

                    if jogador and gerenciador_inimigos and hasattr(jogador, 'atacar'):
                        alvos_chefe = []
                        chefe_para_atacar = Luta_boss.get_chefe_atual() if Luta_boss else None
                        if chefe_para_atacar and hasattr(chefe_para_atacar, 'esta_vivo') and chefe_para_atacar.esta_vivo():
                            alvos_chefe.append(chefe_para_atacar)
                        try: jogador.atacar(alvos_chefe, delta_time_ms)
                        except TypeError: jogador.atacar(alvos_chefe)

                    if jogador and hasattr(jogador, 'vida') and jogador.vida:
                        chefe_para_colisao = Luta_boss.get_chefe_atual() if Luta_boss else None
                        if chefe_para_colisao and hasattr(chefe_para_colisao, 'rect') and \
                           hasattr(jogador, 'rect_colisao') and hasattr(chefe_para_colisao, 'esta_vivo') and \
                           chefe_para_colisao.esta_vivo() and getattr(jogador, 'pode_levar_dano', True):
                            dano_contato_chefe = getattr(chefe_para_colisao, 'contact_damage', 0)
                            if dano_contato_chefe > 0:
                                rect_colisao_chefe = getattr(chefe_para_colisao, 'rect_colisao', chefe_para_colisao.rect)
                                if jogador.rect_colisao.colliderect(rect_colisao_chefe):
                                    try: jogador.receber_dano(dano_contato_chefe, rect_colisao_chefe)
                                    except TypeError: jogador.receber_dano(dano_contato_chefe)

                        if not jogador.vida.esta_vivo():
                            jogador_morreu = True; running_game_loop = False
                            if Luta_boss: Luta_boss.finalizar_luta_chefe(jogador, est, gerenciador_inimigos)
                else:
                    if est and hasattr(est, 'atualizar_ciclo_estacoes'):
                        sinal_estacao = est.atualizar_ciclo_estacoes()
                        if sinal_estacao == "PENDENTE_CHEFE_PRIMAVERA":
                            if Luta_boss and jogador and gerenciador_inimigos:
                                if Luta_boss.iniciar_luta_chefe(jogador, 0, gerenciador_inimigos, est,
                                                              largura_tela_jogo, altura_tela_jogo,
                                                              musica_gameplay_atual_path, musica_gameplay_atual_pos_ms):
                                    pass
                                else:
                                    print("ERRO (main.py): Falha ao iniciar luta contra chefe da Primavera.")
                                    if hasattr(est, 'chefe_primavera_pendente'): est.chefe_primavera_pendente = False
                                    if mixer_initialized_successfully and not pygame.mixer.music.get_busy() and musica_gameplay_atual_path:
                                        tocar_musica_jogo()
                        elif sinal_estacao is True:
                            for arvore_obj in arvores:
                                if arvore_obj and hasattr(arvore_obj, 'atualizar_sprite') and hasattr(est, 'indice_estacao_atual'):
                                    arvore_obj.atualizar_sprite(est.indice_estacao_atual)
                            if gerenciador_inimigos:
                                if hasattr(gerenciador_inimigos, 'resetar_temporizador_spawn_estacao'):
                                    gerenciador_inimigos.resetar_temporizador_spawn_estacao()
                                if jogador and hasattr(jogador, 'rect') and hasattr(gerenciador_inimigos, 'spawn_inimigos_iniciais'):
                                    gerenciador_inimigos.spawn_inimigos_iniciais(jogador, delta_time_ms)

                    if gerenciador_inimigos:
                        if hasattr(gerenciador_inimigos, 'process_spawn_requests'): gerenciador_inimigos.process_spawn_requests(jogador, delta_time_ms)
                        if hasattr(gerenciador_inimigos, 'update_inimigos'): gerenciador_inimigos.update_inimigos(jogador, delta_time_ms)
                        if hasattr(gerenciador_inimigos, 'update_projeteis_inimigos'): gerenciador_inimigos.update_projeteis_inimigos(jogador, delta_time_ms)
                    gerar_elementos_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados)

                    if jogador and gerenciador_inimigos and hasattr(jogador, 'atacar'):
                        alvos_normais = list(gerenciador_inimigos.inimigos)
                        try: jogador.atacar(alvos_normais, delta_time_ms)
                        except TypeError: jogador.atacar(alvos_normais)

                    if jogador and hasattr(jogador, 'vida') and jogador.vida:
                        verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador)
                        if not jogador.vida.esta_vivo():
                            jogador_morreu = True; running_game_loop = False

                    if shop_elements and loja_core and not (Luta_boss and Luta_boss.esta_luta_ativa()):
                        shop_rect = shop_elements.get_current_shop_rect() if hasattr(shop_elements, 'get_current_shop_rect') else None
                        if shop_rect and jogador and hasattr(jogador, 'rect_colisao') and \
                           jogador.rect_colisao.colliderect(shop_rect) and teclas_pressionadas[pygame.K_e]:
                            if mixer_initialized_successfully and pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                            continuar = loja_core.run_shop_scene(janela_principal, jogador, largura_tela_jogo, altura_tela_jogo)
                            if mixer_initialized_successfully:
                                if musica_gameplay_atual_path and not pygame.mixer.music.get_busy(): pygame.mixer.music.unpause()
                                elif not pygame.mixer.music.get_busy(): tocar_musica_jogo()
                            if not continuar: running_game_loop = False; game_is_running_flag = False
                            if hasattr(shop_elements, 'reset_shop_spawn'): shop_elements.reset_shop_spawn()

            cam_x = jogador.rect.centerx - largura_tela_jogo // 2 if jogador and hasattr(jogador, 'rect') else 0
            cam_y = jogador.rect.centery - altura_tela_jogo // 2 if jogador and hasattr(jogador, 'rect') else 0
            tempo_total_seg = (pygame.time.get_ticks() - tempo_inicio_jogo) // 1000 if tempo_inicio_jogo is not None else 0

            # Passa a instância global 'barra_inventario' para desenhar_cena
            desenhar_cena(janela_principal, est, gramas, arvores, jogador, gerenciador_inimigos,
                          vida_jogador_ref, barra_inventario, 
                          cam_x, cam_y, tempo_total_seg, timer_obj, delta_time_ms,
                          luta_boss_ativa_main)

            if jogo_pausado_para_inventario and barra_inventario and \
               hasattr(barra_inventario, 'desenhar_inventario_completo') and not luta_boss_ativa_main:
                barra_inventario.desenhar_inventario_completo(janela_principal, jogador)

            pygame.display.flip()

        if gerenciador_inimigos and hasattr(gerenciador_inimigos, 'stop_threads'):
            gerenciador_inimigos.stop_threads()

        if jogador_morreu and run_death_screen:
            if pause_manager and hasattr(pause_manager, 'destroy_tkinter_window'):
                pass
            run_death_screen(janela_principal, main, main, DEATH_SCREEN_BACKGROUND_IMAGE)
            return

        if acao_menu_principal == "main_menu_from_pause": main(); return

    if 'gerenciador_inimigos' in locals() and gerenciador_inimigos and hasattr(gerenciador_inimigos, 'stop_threads'):
        gerenciador_inimigos.stop_threads()
    if mixer_initialized_successfully: pygame.mixer.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e_main_fatal:
        import traceback
        traceback.print_exc()
        if pygame.get_init():
            if 'gerenciador_inimigos' in locals() and gerenciador_inimigos and hasattr(gerenciador_inimigos, 'stop_threads'):
                gerenciador_inimigos.stop_threads()
            pygame.quit()
        input("Pressione Enter para sair após o erro fatal...")
        sys.exit(1)

