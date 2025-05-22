# Game.py
import pygame
import random
import time
import sys
import os
import threading # Importa a biblioteca threading

# --- ADICIONAR ESTAS LINHAS NO INÍCIO DE GAME.PY
# Isso garante que o diretório 'Arquivos' seja o ponto de partida para as importações
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
# FIM DAS LINHAS ADICIONADAS

# --- Importações da Roda de Armas Tkinter ---
from Roda_Armas import WeaponWheelUI
# --- Fim das Importações da Roda de Armas Tkinter ---

# --- Importação do Menu de Pausa ---
from Pause import PauseMenuManager 
# --- Fim da Importação do Menu de Pausa ---

# --- Importação do XPManager ---
from xp_manager import XPManager
# --- Fim da Importação do XPManager ---

# Importa player.py 
try:
    from player import Player
except ImportError as e:
    print(f"DEBUG(Game): Warning: Módulo 'player.py' ou classe 'Player' não encontrado. Erro: {e}")
    Player = None

# Importa as classes de armas
try:
    from Armas.weapon import Weapon
except ImportError as e:
    print(f"DEBUG(Game): Warning: Módulo 'Armas/weapon.py' não encontrado. Erro: {e}")
    Weapon = None
try:
    from Armas.MachadoBase import MachadoBase 
except ImportError as e:
    print(f"DEBUG(Game): Warning: Módulo 'Armas/MachadoBase.py' não encontrado. Erro: {e}")
    MachadoBase = None
try:
    from Armas.AdagaFogo import AdagaFogo
except ImportError as e:
    print(f"DEBUG(Game): Error: Módulo 'Armas/AdagaFogo.py' não encontrado. Erro: {e}")
    AdagaFogo = None
try:
    from Armas.EspadaBrasas import EspadaBrasas
except ImportError as e:
    print(f"DEBUG(Game): Error: Módulo 'Armas/EspadaBrasas.py' não encontrado. Erro: {e}")
    EspadaBrasas = None
try:
    from Armas.EspadaCaida import EspadaCaida
except ImportError as e:
    print(f"DEBUG(Game): Error: Módulo 'Armas/EspadaCaida.py' não encontrado. Erro: {e}")
    EspadaCaida = None
try:
    from Armas.EspadaFogoAzul import EspadaFogoAzul
except ImportError as e:
    print(f"DEBUG(Game): Error: Módulo 'Armas/EspadaFogoAzul.py' não encontrado. Erro: {e}")
    EspadaFogoAzul = None
try:
    from Armas.EspadaLua import EspadaLua
except ImportError as e:
    print(f"DEBUG(Game): Error: Módulo 'Armas/EspadaLua.py' não encontrado. Erro: {e}")
    EspadaLua = None
try:
    from Armas.EspadaPenitencia import EspadaPenitencia
except ImportError as e:
    print(f"DEBUG(Game): Error: Módulo 'Armas/EspadaPenitencia.py' não encontrado. Erro: {e}")
    EspadaPenitencia = None
try:
    from Armas.MachadoBarbaro import MachadoBarbaro
except ImportError as e:
    print(f"DEBUG(Game): Error: Módulo 'Armas/MachadoBarbaro.py' not found. Erro: {e}")
    MachadoBarbaro = None
try:
    from Armas.MachadoCeruleo import MachadoCeruleo
except ImportError as e:
    print(f"DEBUG(Game): Error: Módulo 'Armas/MachadoCeruleo.py' not found. Erro: {e}")
    MachadoCeruleo = None
try:
    from Armas.MachadoMacabro import MachadoMacabro
except ImportError as e:
    print(f"DEBUG(Game): Error: Módulo 'Armas/MachadoMacabro.py' not found. Erro: {e}")
    MachadoMacabro = None
try:
    from Armas.MachadoMarfim import MachadoMarfim
except ImportError as e:
    print(f"DEBUG(Game): Error: Módulo 'Armas/MachadoMarfim.py' not found. Erro: {e}")
    MachadoMarfim = None

# Outros imports
try:
    from Menu import Menu
except ImportError as e:
    print(f"DEBUG(Game): Aviso: Módulo 'Menu.py' ou classe 'Menu' não encontrado. Erro: {e}")
    Menu = None
try:
    from GerenciadorDeInimigos import GerenciadorDeInimigos
except ImportError as e:
    print(f"DEBUG(Game): Aviso: Módulo 'GerenciadorDeInimigos.py' ou classe 'GerenciadorDeInimigos' não encontrado. Erro: {e}")
    GerenciadorDeInimigos = None
try:
    from Estacoes import Estacoes
except ImportError as e:
    print(f"DEBUG(Game): Aviso: Módulo 'Estacoes.py' ou classe 'Estacoes' não encontrado. Erro: {e}")
    Estacoes = None
try:
    from grama import Grama
except ImportError as e:
    print(f"DEBUG(Game): Aviso: Módulo 'grama.py' ou classe 'Grama' não encontrado. Erro: {e}")
    Grama = None
try:
    from arvores import Arvore
except ImportError as e:
    print(f"DEBUG(Game): Aviso: Módulo 'arvores.py' ou classe 'Arvore' não encontrado. Erro: {e}")
    Arvore = None
try:
    from timer1 import Timer
except ImportError as e:
    print(f"DEBUG(Game): Aviso: Módulo 'timer1.py' ou classe 'Timer' não encontrado. Erro: {e}")
    Timer = None
try:
    import shop_elements
except ImportError as e:
    print(f"DEBUG(Game): Aviso: Módulo 'shop_elements.py' não encontrado. Erro: {e}")
    shop_elements = None
try:
    from death_screen import run_death_screen 
except ImportError as e:
    print(f"DEBUG(Game): Aviso: Módulo 'death_screen.py' ou função 'run_death_screen' não encontrado. Erro: {e}")
    run_death_screen = None
try:
    from loja import run_shop_scene 
except ImportError as e:
    print(f"DEBUG(Game): Aviso: Módulo 'loja.py' ou função 'run_shop_scene' não encontrado. Erro: {e}")
    run_shop_scene = None
try:
    from vida import Vida
except ImportError as e:
    print(f"DEBUG(Game): Aviso: Módulo 'vida.py' ou classe 'Vida' não encontrado. Erro: {e}")
    Vida = None


MUSICAS_JOGO = [
    "Musica/Gameplay/Faixa 1.mp3",
    "Musica/Gameplay/Faixa 2.mp3",
    "Musica/Gameplay/Faixa 3.mp3",
]
DEATH_SCREEN_BACKGROUND_IMAGE = "Sprites/Backgrounds/death_background.png"

game_music_volume = 0.5 
game_sfx_volume = 0.5  

# Variáveis globais para controle do thread da roda de armas
weapon_wheel_ui = None
weapon_wheel_thread = None # Thread para a UI da roda de armas
weapon_wheel_active_event = threading.Event() # Evento para sinalizar que a roda deve ser mostrada/escondida

game_paused_for_wheel = False
jogador = None
pause_manager = None
xp_manager = None
game_is_running_flag = True # Flag para controlar o loop de threads


def on_weapon_selected_from_wheel(selected_weapon):
    global jogador, game_paused_for_wheel, weapon_wheel_active_event
    if jogador and hasattr(jogador, 'owned_weapons'):
        if any(w.name == selected_weapon.name for w in jogador.owned_weapons):
            jogador.equip_weapon(selected_weapon)
            print(f"Game: Jogador equipou {selected_weapon.name} via roda de armas.")
        else:
            print(f"Game: Erro - Jogador não possui a arma {selected_weapon.name}. Não pode equipar.")
    else:
        print("Game: Erro - Jogador não disponível ou sem inventário para equipar arma da roda.")
    
    game_paused_for_wheel = False
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy(): # Verifica se o mixer está inicializado
        pygame.mixer.music.unpause()
    weapon_wheel_active_event.clear() # Sinaliza que a roda não está mais ativa

def run_weapon_wheel_thread_target():
    """
    Função alvo para o thread da roda de armas.
    Assume que weapon_wheel_ui.show_wheel() agora gerencia seu próprio loop de eventos Tkinter
    e só retorna quando a roda é fechada.
    """
    global weapon_wheel_ui, game_paused_for_wheel, weapon_wheel_active_event
    
    # Este loop externo permite que o thread seja reutilizado (embora um novo thread seja criado a cada TAB atualmente)
    # Para uma implementação mais robusta, a própria WeaponWheelUI gerenciaria seu thread e loop.
    print("DEBUG(Game): Thread da roda de armas iniciado.")
    if weapon_wheel_ui:
        try:
            # weapon_wheel_ui.show_wheel() # Esta chamada agora deve ser bloqueante (ex: conter tk_root.mainloop())
            # E deve ser projetada para ser chamada desta forma.
            # A lógica de fechar a janela Tkinter (via callback ou hide_wheel) deve fazer este método retornar.
            
            # Simulação simplificada:
            # A UI Tkinter precisa de um root.mainloop() para rodar.
            # A WeaponWheelUI.show_wheel() deveria idealmente configurar e iniciar isso.
            # E WeaponWheelUI.hide_wheel() deveria parar o mainloop e destruir a janela.
            if hasattr(weapon_wheel_ui, 'tk_root') and weapon_wheel_ui.tk_root:
                # Esta é uma suposição de como a UI pode ser executada.
                # A Roda_Armas.py precisaria ser adaptada para este modelo de thread.
                print("DEBUG(Game): Chamando show_wheel() e entrando no loop da UI da roda (simulado).")
                weapon_wheel_ui.show_wheel() # Mostra a janela
                
                # Um loop para manter o thread vivo enquanto a roda está "ativa"
                # Este loop é uma simplificação. Idealmente, o mainloop do Tkinter estaria aqui.
                while weapon_wheel_active_event.is_set() and game_is_running_flag:
                    if hasattr(weapon_wheel_ui, 'tk_root') and weapon_wheel_ui.tk_root.winfo_exists():
                        weapon_wheel_ui.tk_root.update() # Processa eventos Tkinter
                        weapon_wheel_ui.tk_root.update_idletasks()
                    else: # Janela foi destruída
                        weapon_wheel_active_event.clear()
                        break
                    time.sleep(0.01) # Evita consumo excessivo de CPU

                print("DEBUG(Game): Saindo do loop da UI da roda.")
                if hasattr(weapon_wheel_ui, 'hide_wheel'): # Tenta esconder/destruir se ainda não foi
                    weapon_wheel_ui.hide_wheel()

        except Exception as e:
            print(f"DEBUG(Game): Erro no thread da roda de armas: {e}")
        finally:
            print("DEBUG(Game): Thread da roda de armas finalizando.")
            # Garante que o estado de pausa seja resetado se o thread terminar inesperadamente
            if game_paused_for_wheel:
                game_paused_for_wheel = False
                if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpause()
            weapon_wheel_active_event.clear()


def inicializar_jogo(largura_tela, altura_tela):
    global jogador, game_music_volume, pause_manager, xp_manager, weapon_wheel_ui
    print("DEBUG(Game): Initializing game components...")
    tempo_inicio = pygame.time.get_ticks()

    jogador = Player() if Player is not None else None
    if jogador is None:
        print("DEBUG(Game): Error: Player class not available. Could not initialize player.")
    else:
        xp_manager = XPManager(player_ref=jogador, largura_tela=largura_tela, altura_tela=altura_tela)
        jogador.xp_manager = xp_manager
        initial_weapon_instance = AdagaFogo() if AdagaFogo is not None else None
        if initial_weapon_instance:
            jogador.add_owned_weapon(initial_weapon_instance)
            jogador.equip_weapon(initial_weapon_instance)
            print(f"DEBUG(Game): Arma inicial: {jogador.current_weapon.name} (Nível {jogador.current_weapon.level})")
        else:
            print("DEBUG(Game): Aviso: Nenhuma arma inicial configurada.")

    estacoes = Estacoes() if Estacoes is not None else None
    vida = Vida(vida_maxima=100, vida_atual=100) if Vida is not None else None
    gramas = []
    arvores = []
    blocos_gerados = set()
    gerenciador_inimigos = GerenciadorDeInimigos(estacoes_obj=estacoes, tela_largura=largura_tela, altura_tela=altura_tela) if GerenciadorDeInimigos is not None and estacoes is not None else None
    
    if gerenciador_inimigos and jogador and hasattr(jogador, 'rect'):
        gerenciador_inimigos.spawn_inimigos(jogador)

    timer_obj = None
    if Timer is not None:
        fonte_estimativa = pygame.font.Font(None, 36)
        largura_estimada_texto = fonte_estimativa.size("00:00")[0]
        largura_estimada_fundo = largura_estimada_texto + 10
        timer_pos_x = largura_tela // 2 - largura_estimada_fundo // 2
        timer_obj = Timer(timer_pos_x, 30)

    if shop_elements and hasattr(shop_elements, 'reset_shop_spawn'):
        shop_elements.reset_shop_spawn()

    pause_manager = PauseMenuManager(pygame.display.get_surface(), 
                                     largura_tela, altura_tela, 
                                     main, main, # Passando a função main como callback
                                     game_music_volume, game_sfx_volume)
    
    # Inicializa a UI da roda de armas aqui, mas não inicia o thread ainda
    if WeaponWheelUI is not None and jogador:
        weapon_wheel_ui = WeaponWheelUI(parent_game_instance=None, 
                                        on_weapon_selected_callback=on_weapon_selected_from_wheel,
                                        player_owned_weapons_ref=jogador.owned_weapons)
    else:
        print("DEBUG(Game): Aviso: WeaponWheelUI ou Jogador não disponível. Roda de armas não funcionará.")
        weapon_wheel_ui = None


    return jogador, estacoes, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, False, tempo_inicio, timer_obj


def gerar_elementos_ao_redor_do_jogador(Asrahel, gramas, arvores, est, blocos_gerados):
    jogador_obj = Asrahel # Renomeado para clareza
    bloco_tamanho = 1080
    if jogador_obj is None or not hasattr(jogador_obj, 'rect') or est is None:
        return
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
    if not MUSICAS_JOGO:
        print("Game: Nenhuma música configurada para o jogo principal.")
        return
    musica_path = random.choice(MUSICAS_JOGO)
    try:
        if pygame.mixer.get_init(): # Verifica se o mixer foi inicializado
            pygame.mixer.music.load(musica_path)
            pygame.mixer.music.set_volume(game_music_volume)
            pygame.mixer.music.play(-1)
        else:
            print("DEBUG(Game): Mixer de áudio não inicializado. Não é possível tocar música.")
    except pygame.error as e:
        print(f"Game: Erro ao carregar ou tocar música '{musica_path}': {e}")

def verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador_obj, vida_obj):
    if jogador_obj is None or vida_obj is None or not hasattr(vida_obj, 'esta_vivo') or not hasattr(vida_obj, 'receber_dano'):
        return
    jogador_rect_colisao = getattr(jogador_obj, 'rect_colisao', getattr(jogador_obj, 'rect', None))
    if jogador_rect_colisao is None or gerenciador_inimigos is None or not hasattr(gerenciador_inimigos, 'inimigos'):
        return
    for inimigo in list(gerenciador_inimigos.inimigos):
        if inimigo and hasattr(inimigo, 'rect'):
            dano_a_aplicar = getattr(inimigo, 'contact_damage', 10) # Dano padrão de 10 se não especificado
            colidiu = False
            if hasattr(inimigo, 'verificar_colisao') and callable(getattr(inimigo, 'verificar_colisao')):
                if inimigo.verificar_colisao(jogador_obj):
                    colidiu = True
            elif inimigo.rect.colliderect(jogador_rect_colisao):
                colidiu = True
            
            if colidiu and vida_obj.esta_vivo():
                vida_obj.receber_dano(dano_a_aplicar)


def desenhar_cena(janela, est, gramas, arvores, jogador_obj, gerenciador_inimigos, vida_obj, camera_x, camera_y, tempo_decorrido, timer_obj, dt_ms):
    global xp_manager
    janela.fill((0, 0, 0))
    if est and hasattr(est, 'desenhar'): est.desenhar(janela)
    if gramas:
        for gr in gramas:
            if gr and hasattr(gr, 'desenhar'): gr.desenhar(janela, camera_x, camera_y)
    if gerenciador_inimigos:
        if hasattr(gerenciador_inimigos, 'desenhar_inimigos'): gerenciador_inimigos.desenhar_inimigos(janela, camera_x, camera_y)
        if hasattr(gerenciador_inimigos, 'desenhar_projeteis_inimigos'): gerenciador_inimigos.desenhar_projeteis_inimigos(janela, camera_x, camera_y)
    if jogador_obj and hasattr(jogador_obj, 'desenhar'): jogador_obj.desenhar(janela, camera_x, camera_y)
    if arvores:
        for a in arvores:
            if a and hasattr(a, 'desenhar'): a.desenhar(janela, camera_x, camera_y)
    if shop_elements and hasattr(shop_elements, 'draw_shop_elements'): shop_elements.draw_shop_elements(janela, camera_x, camera_y, dt_ms)
    if est and hasattr(est, 'desenhar_mensagem_estacao'): est.desenhar_mensagem_estacao(janela)
    if vida_obj and hasattr(vida_obj, 'desenhar'): vida_obj.desenhar(janela, 20, 20)
    if timer_obj and hasattr(timer_obj, 'desenhar'): timer_obj.desenhar(janela, tempo_decorrido)
    if xp_manager and hasattr(xp_manager, 'draw'): xp_manager.draw(janela)


def main():
    global jogador, game_paused_for_wheel, weapon_wheel_ui, weapon_wheel_thread, weapon_wheel_active_event
    global game_music_volume, game_sfx_volume, pause_manager, game_is_running_flag

    pygame.init()
    try:
        pygame.mixer.init()
        print("Pygame: Audio mixer initialized successfully.")
    except pygame.error as e:
        print(f"Pygame: Error initializing audio mixer: {e}")

    info = pygame.display.Info()
    largura_tela = info.current_w
    altura_tela = info.current_h
    janela = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Lenda de Asrahel")
    clock = pygame.time.Clock()

    menu = Menu(largura_tela, altura_tela) if Menu is not None else None
    acao_menu = None

    if menu is not None:
        while acao_menu is None: # Corrigido para 'is None'
            mouse_pos = pygame.mouse.get_pos()
            menu.desenhar(janela, mouse_pos)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    if hasattr(menu, 'parar_musica'): menu.parar_musica()
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(menu, 'verificar_click'):
                        acao_menu = menu.verificar_click(*evento.pos)
                        if acao_menu == "sair": break 
            if acao_menu == "sair": break # Sai do while também
            pygame.display.update()
            clock.tick(60)

    if acao_menu == "jogar":
        if menu and hasattr(menu, 'parar_musica'): menu.parar_musica()
        print("Menu 'Play' selected. Initializing game...")
        
        jogador, est, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, jogador_morreu, tempo_inicio, timer_obj = inicializar_jogo(largura_tela, altura_tela)
        
        tocar_musica_jogo()
        game_state = "playing"
        game_is_running_flag = True # Define a flag para o loop de jogo e threads

        running = True
        while running:
            dt = clock.tick(60)
            dt_ms = clock.get_rawtime() # Usado por shop_elements

            # Não processa mais weapon_wheel_ui.process_events() aqui, pois o thread cuidará disso (supostamente)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    running = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        if game_paused_for_wheel:
                            if weapon_wheel_ui and hasattr(weapon_wheel_ui, 'hide_wheel'):
                                weapon_wheel_ui.hide_wheel() # Sinaliza para o thread da UI fechar
                            weapon_wheel_active_event.clear() # Garante que o evento seja limpo
                            game_paused_for_wheel = False
                            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                                pygame.mixer.music.unpause()
                        elif pause_manager: # Se não é a roda, é o menu de pausa normal
                            action, new_music_vol, new_sfx_vol = pause_manager.show_menu()
                            game_music_volume = new_music_vol
                            game_sfx_volume = new_sfx_vol
                            if action == "main_menu":
                                running = False # Para o loop do jogo para voltar ao menu
                                acao_menu = "main_menu_from_pause" # Sinaliza para reiniciar no menu
                                break 
                            elif action == "quit":
                                running = False
                                break
                            # "resume" já é tratado por show_menu despausando a música
                    
                    if evento.key == pygame.K_TAB and not game_paused_for_wheel and game_state == "playing":
                        if weapon_wheel_ui:
                            print("DEBUG(Game): TAB pressionado. Tentando mostrar roda de armas.")
                            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                                pygame.mixer.music.pause()
                            
                            game_paused_for_wheel = True
                            weapon_wheel_active_event.set() # Sinaliza para o thread da roda mostrar a UI

                            # Inicia o thread da roda de armas se não estiver rodando ou se o anterior terminou
                            if weapon_wheel_thread is None or not weapon_wheel_thread.is_alive():
                                weapon_wheel_thread = threading.Thread(target=run_weapon_wheel_thread_target, daemon=True)
                                weapon_wheel_thread.start()
                            # Se o thread já existe e está vivo, o evento 'set' deve ser suficiente
                            # para que ele mostre a roda novamente (depende da implementação em Roda_Armas.py)
                        else:
                            print("DEBUG(Game): Roda de armas (weapon_wheel_ui) não está disponível.")
                
                if game_state == "playing" and not game_paused_for_wheel:
                    if jogador and hasattr(jogador, 'handle_input'):
                        jogador.handle_input(evento)
            
            if not running: break # Sai do loop principal se running for False

            if game_state == "playing" and not game_paused_for_wheel:
                teclas = pygame.key.get_pressed()
                if jogador and hasattr(jogador, 'mover'): jogador.mover(teclas, arvores)
                if jogador and hasattr(jogador, 'update'): jogador.update()
                
                gerar_elementos_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados)

                if est and hasattr(est, 'atualizar'):
                    est_ant = est.i
                    est.atualizar()
                    if est.i != est_ant:
                        if arvores:
                            for arv in arvores:
                                if arv and hasattr(arv, 'atualizar_sprite'): arv.atualizar_sprite(est.i)
                        if gerenciador_inimigos and jogador and hasattr(jogador, 'rect'):
                            gerenciador_inimigos.spawn_inimigos(jogador)
                
                if gerenciador_inimigos and jogador and hasattr(jogador, 'rect'):
                    if hasattr(gerenciador_inimigos, 'tentar_spawnar'): gerenciador_inimigos.tentar_spawnar(jogador)
                    if hasattr(gerenciador_inimigos, 'update_inimigos'): gerenciador_inimigos.update_inimigos(jogador)
                    if hasattr(gerenciador_inimigos, 'update_projeteis_inimigos'): gerenciador_inimigos.update_projeteis_inimigos(jogador)

                if jogador and gerenciador_inimigos and hasattr(gerenciador_inimigos, 'inimigos'):
                    jogador.atacar(gerenciador_inimigos.inimigos)
                
                if vida and gerenciador_inimigos and jogador:
                    verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador, vida)
                    if not vida.esta_vivo():
                        jogador_morreu = True
                        running = False # Termina o loop do jogo

                keys = pygame.key.get_pressed()
                current_shop_rect = shop_elements.get_current_shop_rect() if shop_elements else None
                if current_shop_rect and jogador and hasattr(jogador, 'rect') and jogador.rect.colliderect(current_shop_rect) and keys[pygame.K_e]:
                    if run_shop_scene:
                        print("DEBUG(Game): Entrando na loja.")
                        if pygame.mixer.get_init(): pygame.mixer.music.pause()
                        game_state = "shop"
                    else:
                        print("DEBUG(Game): Função da loja não disponível.")
            
            elif game_state == "shop":
                if run_shop_scene:
                    continue_game, _ = run_shop_scene(janela, jogador, largura_tela, altura_tela, weapon_wheel_ui)
                    if continue_game:
                        game_state = "playing"
                        print("DEBUG(Game): Saindo da loja, retornando ao jogo.")
                        if pygame.mixer.get_init() and pygame.mixer.music.get_busy(): # Verifica se o mixer e a música estão ativos
                           pygame.mixer.music.unpause()
                    else:
                        running = False # Sai do jogo se a loja retornar para não continuar
                        print("DEBUG(Game): Saindo da loja, fechando o jogo.")
                else: # Fallback se run_shop_scene não estiver disponível
                    game_state = "playing"


            camera_x = jogador.rect.centerx - largura_tela // 2 if jogador and hasattr(jogador, 'rect') else 0
            camera_y = jogador.rect.centery - altura_tela // 2 if jogador and hasattr(jogador, 'rect') else 0
            
            if game_state == "playing": # Só desenha a cena do jogo se estiver jogando
                tempo_decorrido_segundos = (pygame.time.get_ticks() - tempo_inicio) // 1000 if tempo_inicio else 0
                desenhar_cena(janela, est, gramas, arvores, jogador, gerenciador_inimigos, vida, camera_x, camera_y, tempo_decorrido_segundos, timer_obj, dt_ms)

            pygame.display.flip()

        game_is_running_flag = False # Sinaliza para threads terminarem
        if weapon_wheel_thread and weapon_wheel_thread.is_alive():
            print("DEBUG(Game): Esperando thread da roda de armas terminar...")
            weapon_wheel_active_event.set() # Garante que o loop interno do thread possa verificar a flag e sair
            weapon_wheel_thread.join(timeout=1.0) # Espera pelo thread com timeout
            if weapon_wheel_thread.is_alive():
                print("DEBUG(Game): Thread da roda de armas não terminou a tempo.")
        if weapon_wheel_ui: # Tenta destruir a UI do Tkinter de forma segura
            if hasattr(weapon_wheel_ui, 'tk_root') and weapon_wheel_ui.tk_root:
                try:
                    weapon_wheel_ui.tk_root.quit() # Pede para o mainloop do Tkinter sair
                    weapon_wheel_ui.tk_root.destroy()
                except Exception as e:
                    print(f"DEBUG(Game): Erro ao tentar fechar tk_root da roda de armas: {e}")
            weapon_wheel_ui = None


        if jogador_morreu:
            if run_death_screen:
                # Garante que o pause_manager (se usar Tkinter) seja destruído
                if pause_manager and hasattr(pause_manager, 'toplevel_window') and pause_manager.toplevel_window and pause_manager.toplevel_window.winfo_exists():
                    pause_manager.toplevel_window.destroy()
                if pause_manager and hasattr(pause_manager, 'tk_root') and pause_manager.tk_root and pause_manager.tk_root.winfo_exists():
                    pause_manager.tk_root.destroy()
                run_death_screen(janela, main, main, DEATH_SCREEN_BACKGROUND_IMAGE)
            else:
                print("DEBUG(Game): Tela de morte não disponível.")
        
        # Se saiu do loop do jogo para ir ao menu principal (pelo menu de pausa)
        if acao_menu == "main_menu_from_pause":
            main() # Reinicia o jogo a partir do menu principal
            return # Evita que o código abaixo seja executado nesta chamada recursiva

    elif acao_menu == "sair":
        if menu and hasattr(menu, 'parar_musica'): menu.parar_musica()
    
    game_is_running_flag = False # Garante que a flag seja False ao sair
    if weapon_wheel_thread and weapon_wheel_thread.is_alive():
        weapon_wheel_active_event.set() 
        weapon_wheel_thread.join(timeout=0.5)
    
    pygame.mixer.quit() # Desinicializa o mixer
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
