# game.py
import pygame
import random
import time
import sys
import os # Importa os para ajudar a verificar caminhos
import math # Importa math para cálculos de ângulo para a seta

# Importa as classes necessárias
# Adicionado try-except para cada importação para robustez
try:
    from player import Player
except ImportError:
    print("ERRO FATAL: Módulo 'player.py' ou classe 'Player' não encontrado. Certifique-se de que player.py existe.")
    sys.exit() # Sai do jogo si a classe Player não for encontrada

try:
    from Estacoes import Estacoes
except ImportError:
    print("ERRO FATAL: Módulo 'Estacoes.py' ou classe 'Estacoes' não encontrado. Certifique-se de que Estacoes.py existe.")
    sys.exit() # Sai do jogo si a classe Estacoes não for encontrada

try:
    from GerenciadorDeInimigos import GerenciadorDeInimigos
except ImportError:
    print("ERRO FATAL: Módulo 'GerenciadorDeInimigos.py' ou classe 'GerenciadorDeInimigos' não encontrado. Certifique-se de que GerenciadorDeInimigos.py existe.")
    sys.exit() # Sai do jogo si a classe GerenciadorDeInimigos não for encontrada

try:
    from arvores import Arvore
except ImportError:
    print("AVISO(Game): Módulo 'arvores.py' ou classe 'Arvore' não encontrado.")
    Arvore = None # Define como None para evitar NameError

try:
    from grama import Grama
except ImportError:
    print("AVISO(Game): Módulo 'grama.py' ou classe 'Grama' não encontrado.")
    Grama = None # Define como None para evitar NameError

try:
    from vida import Vida
except ImportError:
    print("ERRO FATAL: Módulo 'vida.py' ou classe 'Vida' não encontrado. Certifique-se de que vida.py existe.")
    sys.exit() # Sai do jogo si a classe Vida não for encontrada

try:
    from Menu import Menu
except ImportError:
    print("ERRO FATAL: Módulo 'Menu.py' ou classe 'Menu' não encontrado. Certifique-se de que Menu.py existe.")
    sys.exit() # Sai do jogo si a classe Menu não for encontrada

# Mantemos a importação para a função base de geração de plantas, se ela ainda for usada diretamente
# Se toda a lógica de geração de plantas foi movida para 'mundo.py', esta importação pode ser removida.
try:
    from gerador_plantas import gerar_plantas_ao_redor_do_jogador
except ImportError:
    print("AVISO(Game): Módulo 'gerador_plantas.py' ou função 'gerar_plantas_ao_redor_do_jogador' não encontrado.")
    gerar_plantas_ao_redor_do_jogador = None # Define como None para evitar NameError

try:
    from timer1 import Timer
except ImportError:
    print("ERRO FATAL: Módulo 'timer1.py' ou classe 'Timer' não encontrado. Certifique-se de que timer1.py existe.")
    sys.exit() # Sai do jogo si a classe Timer não for encontrada

try:
    from shop_manager import ShopManager
except ImportError:
    print("ERRO FATAL: Módulo 'shop_manager.py' ou classe 'ShopManager' não encontrado. Certifique-se de que shop_manager.py existe.")
    sys.exit() # Sai do jogo si a classe ShopManager não for encontrada

# Importa a probabilidade e o intervalo mínimo de spawn da loja (ainda necessário para o ShopManager)
# Mantido try-except para Spawn_Loja, pois o ShopManager lida com a ausência dessas variáveis
try:
    from Spawn_Loja import PROBABILIDADE_SPAWN_LOJA, INTERVALO_MINIMO_SPAWN_LOJA
except ImportError:
    # Estes serão definidos como 0.0 e 0 no ShopManager se a importação falhar lá.
    pass

# Importa o módulo mundo se a geração de elementos do mundo estiver nele
try:
    import mundo # Importa o módulo do mundo
except ImportError:
    print("AVISO(Game): Módulo 'mundo.py' não encontrado. A geração de plantas pode não funcionar.")
    mundo = None # Define como None para evitar NameError


MUSICAS_JOGO = [
    "Musica/Gameplay/Faixa 1.mp3",
    "Musica/Gameplay/Faixa 2.mp3",
    "Musica/Gameplay/Faixa 3.mp3",
]

# Variáveis globais relacionadas à loja foram movidas para a classe ShopManager


def inicializar_jogo(largura_tela, altura_tela):
    """
    Inicializa os componentes do jogo.

    Args:
        largura_tela (int): Largura da janela.
        altura_tela (int): Altura da janela.

    Returns:
        tuple: Uma tupla contendo os objetos e listas inicializados.
               Retorna None se ocorrer um erro crítico durante a inicialização.
    """
    try:
        # Captura o tempo de início em milissegundos
        tempo_inicio = pygame.time.get_ticks()

        # Inicializa o jogador
        jogador = Player()

        # Inicializa as estações
        estacoes = Estacoes()

        # Inicializa a vida do jogador
        vida = Vida(vida_maxima=100, vida_atual=100)

        # Inicializa listas para gramas e árvores
        gramas = []
        arvores = []
        # Conjunto para rastrear blocos de mapa já gerados
        # Se a geração de plantas estiver no módulo mundo, esta variável deve estar lá.
        # Mantida aqui por compatibilidade com a função gerar_elementos_ao_redor_do_jogador
        # que a utiliza diretamente. Idealmente, mover para o módulo mundo.
        blocos_gerados = set()


        # Inicializa o gerenciador de inimigos
        # Passando os argumentos que o construtor de GerenciadorDeInimigos espera
        # Ajuste os argumentos do GerenciadorDeInimigos se o construtor esperar algo diferente de estacoes, largura, altura
        gerenciador_inimigos = GerenciadorDeInimigos(estacoes, largura_tela, altura_tela)


        # Inicializa a câmera (comentado, si você não estiver usando uma classe Camera separada)
        # camera = Camera(jogador, largura_tela, altura_tela) if Camera is not None and jogador is not None else None


        # Realiza o spawn inicial de inimigos si o gerenciador e o jogador estiverem disponíveis
        # Nota: O método spawn_inimigos no GerenciadorDeInimigos anterior esperava 'estacao' e 'jogador'.
        # Ajustando para passar 'estacoes.i' (se estacoes existir) e 'jogador'.
        # Removida a chamada de spawn inicial aqui. Será feita no loop principal após a criação da janela.
        pass


        # Inicializa o objeto Timer
        timer_obj = Timer(largura_tela // 2 - 45, 30) # Posição centralizada no topo


        # Inicializa o gerenciador da loja
        # CORRIGIDO: Passando largura e altura da tela para o ShopManager
        shop_manager = ShopManager(largura_tela, altura_tela)


        # Retorna os objetos inicializados e o estado inicial do jogo
        # Adicionado blocos_gerados ao retorno
        return jogador, estacoes, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, False, tempo_inicio, timer_obj, shop_manager

    except Exception as e:
        print(f"Erro crítico durante a inicialização do jogo: {e}")
        # Retorna None para indicar que a inicialização falhou
        return None


# --- Função modificada para gerar plantas E chamar o spawn da loja ---
# Se a geração de plantas foi movida para o módulo mundo, esta função pode ser removida
# e a chamada direta para mundo.gerar_plantas_ao_redor_do_jogador deve ser feita no loop principal.
# Mantida por compatibilidade com o código enviado.
def gerar_elementos_ao_redor_do_jogador(Asrahel, gramas, arvores, est, blocos_gerados, shop_manager):
    """
    Gera plantas (grama e árvores) e chama a lógica para potencialmente spawnar a loja
    ao redor do jogador em blocos de mapa não gerados.

    Args:
        Asrahel (Player): O objeto jogador.
        gramas (list): Lista de objetos Grama.
        arvores (list): Lista de objetos Arvore.
        est (Estacoes): O objeto Estacoes para determinar o sprite da árvore.
        blocos_gerados (set): Conjunto de coordenadas de blocos já gerados.
        shop_manager (ShopManager): O gerenciador da loja.
    """
    jogador = Asrahel
    distancia_geracao = 1920  # distância do centro do jogador (usado implicitamente pelos blocos ao redor)
    bloco_tamanho = 1080  # tamanho do bloco usado para evitar gerar novamente

    # Verifica si o jogador e o objeto Estacoes existem antes de calcular o bloco
    if jogador is None or not hasattr(jogador, 'rect') or est is None:
        return

    # Usa centerx/centery para o centro do bloco
    jogador_bloco_x = int(jogador.rect.centerx // bloco_tamanho)
    jogador_bloco_y = int(jogador.rect.centery // bloco_tamanho)

    # Explora ao redor do jogador (9 blocos)
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            bloco_coord = (jogador_bloco_x + dx, jogador_bloco_y + dy)

            # Processa apenas blocos que ainda não foram gerados
            if bloco_coord not in blocos_gerados:
                blocos_gerados.add(bloco_coord)
                base_x = (jogador_bloco_x + dx) * bloco_tamanho
                base_y = (jogador_bloco_y + dy) * bloco_tamanho

                # Gerar gramas nas bordas
                if Grama is not None:
                     for _ in range(random.randint(15, 25)):
                         x = base_x + random.randint(0, bloco_tamanho)
                         y = base_y + random.randint(0, bloco_tamanho)
                         gramas.append(Grama(x, y, 50, 50)) # Ajuste tamanho si necessário

                # Gerar árvores na área central
                if Arvore is not None and hasattr(est, 'i'):
                    for _ in range(random.randint(1, 3)):  # Menos árvores do que gramas
                        x = base_x + random.randint(bloco_tamanho // 4, 3 * bloco_tamanho // 4)
                        y = base_y + random.randint(bloco_tamanho // 4, 3 * bloco_tamanho // 4)
                        arvores.append(Arvore(x, y, 180, 180, est.i)) # Passa o índice da estação


                # --- Chama a lógica para spawnar a loja usando o ShopManager ---
                if shop_manager is not None and hasattr(shop_manager, 'check_and_spawn_shop'):
                     # Passa o bloco_coord, base_x e base_y para o ShopManager
                     shop_manager.check_and_spawn_shop(jogador, bloco_coord, base_x, base_y)


def tocar_musica_jogo():
    """Carrega e toca uma música aleatória do jogo em loop."""
    if not MUSICAS_JOGO:
        print("Jogo: Nenhuma música configurada para o jogo principal.")
        return

    # Seleciona uma música aleatória da lista
    musica_path = random.choice(MUSICAS_JOGO)

    try:
        # Carrega a música
        pygame.mixer.music.load(musica_path)
        # Toca a música em loop infinito (-1)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Jogo: Erro ao carregar ou tocar a música '{musica_path}': {e}")

def verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador, vida):
    """Verifica colisões entre o jogador e os inimigos para aplicar dano ao jogador."""
    # Verifica si os objetos necessários existem antes de proceder
    if jogador is None or vida is None or not hasattr(vida, 'esta_vivo') or not hasattr(vida, 'receber_dano'):
        # print("AVISO(Game - Colisões Inimigos): Objetos necessários para verificar colisões com inimigos ausentes.") # Debug removido
        return

    # Obtém o retângulo de colisão do jogador (preferindo rect_colisao si existir)
    jogador_rect_colisao = getattr(jogador, 'rect_colisao', getattr(jogador, 'rect', None))

    # Si o retângulo de colisão do jogador não existir, retorna
    if jogador_rect_colisao is None:
        # print("AVISO(Game - Colisões Inimigos): Retângulo de colisão do jogador ausente.") # Debug removido
        return

    # Verifica si o gerenciador de inimigos existe e tem uma lista de inimigos
    if gerenciador_inimigos is None or not hasattr(gerenciador_inimigos, 'inimigos'):
        # print("AVISO(Game - Colisões Inimigos): Gerenciador de inimigos ou lista de inimigos ausente.") # Debug removido
        return

    # Itera sobre uma cópia da lista de inimigos para evitar problemas si um inimigo for removido durante a iteração
    for inimigo in list(gerenciador_inimigos.inimigos):
        # Verifica si o inimigo existe e tem um retângulo de colisão (rect)
        if inimigo is not None and hasattr(inimigo, 'rect'):
            # Verifica si o inimigo tem um método de verificação de colisão customizado
            # Se o inimigo tiver uma hitbox de colisão específica para o jogador,
            # a lógica deve estar no método check_player_collision do inimigo.
            # Esta função aqui no Game.py pode ser simplificada para apenas chamar o método do inimigo.

            # Chamamos o método check_player_collision do inimigo para que ele lide com a colisão com o jogador
            if hasattr(inimigo, 'check_player_collision'):
                 inimigo.check_player_collision(jogador)
            # else:
                 # print(f"AVISO(Game - Colisões Inimigos): Inimigo do tipo {type(inimigo).__name__} não tem método 'check_player_collision'.") # Debug aviso

        # else:
             # print(f"AVISO(Game - Colisões Inimigos): Objeto inimigo inválido na lista ou sem atributo 'rect'.") # Debug aviso


def desenhar_cena(janela, est, gramas, arvores, jogador, gerenciador_inimigos, vida, camera_x, camera_y, tempo_decorrido, timer_obj, shop_manager):
    """Desenha todos os elementos da cena na janela, considerando o offset da câmera."""

    # Preenche o fundo da janela
    janela.fill((0, 0, 0)) # Fundo preto

    # 1. Desenha a estação (fundo ou elementos estáticos)
    if est is not None and hasattr(est, 'desenhar'):
        est.desenhar(janela)

    # 2. Desenha a grama (elementos do cenário)
    if gramas is not None:
        for gr in gramas:
            if gr is not None and hasattr(gr, 'desenhar'):
                gr.desenhar(janela, camera_x, camera_y)

    # 3. Desenha o sprite da loja (se estiver no mapa) - Desenha antes dos personagens
    if shop_manager is not None and hasattr(shop_manager, 'current_shop_rect') and shop_manager.current_shop_rect is not None and hasattr(shop_manager, 'shop_sprite_image') and shop_manager.shop_sprite_image is not None:
         # Desenha o sprite da loja com o offset da câmera
         shop_rect_on_screen = pygame.Rect(shop_manager.current_shop_rect.x - camera_x, shop_manager.current_shop_rect.y - camera_y, shop_manager.current_shop_rect.width, shop_manager.current_shop_rect.height)
         janela.blit(shop_manager.shop_sprite_image, shop_rect_on_screen)

    # 4. Desenha os inimigos
    if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'desenhar_inimigos'):
        gerenciador_inimigos.desenhar_inimigos(janela, camera_x, camera_y)

    # 5. Desenha os projéteis dos inimigos
    if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'desenhar_projeteis_inimigos'):
        gerenciador_inimigos.desenhar_projeteis_inimigos(janela, camera_x, camera_y)

    # 6. Desenha o jogador
    if jogador is not None and hasattr(jogador, 'desenhar'):
        jogador.desenhar(janela, camera_x, camera_y)

    # 7. Desenha TODAS as árvores - Desenha APÓS o jogador, inimigos e projéteis para sobrepô-los
    if arvores is not None:
        # Ordena as árvores pela posição Y para desenhar as mais "distantes" primeiro (para profundidade entre as próprias árvores)
        arvores_ordenadas = sorted([a for a in arvores if a is not None and hasattr(a, 'rect') and hasattr(a, 'desenhar')], key=lambda arvore: arvore.rect.bottom)
        for a in arvores_ordenadas:
            if a is not None and hasattr(a, 'desenhar'):
                 a.desenhar(janela, camera_x, camera_y)

    # 8. Desenha os elementos de UI da loja (pop-up e seta) - Desenha APÓS os elementos do mundo
    # Esses elementos devem ser desenhados em posições FIXAS na tela, sem o offset da câmera.
    # É importante que draw_ui_elements use o offset da câmera para posicionar a seta em relação à loja no mundo,
    # mas desenhe o pop-up em uma posição fixa na tela.
    if shop_manager is not None and hasattr(shop_manager, 'draw_ui_elements'):
         shop_manager.draw_ui_elements(janela, camera_x, camera_y, jogador)

    # 9. Desenha a mensagem da estação (si houver) - Desenha sobre os elementos do mundo
    # A mensagem da estação deve ser desenhada em uma posição FIXA na tela, sem o offset da câmera.
    if est is not None and hasattr(est, 'desenhar_mensagem_estacao'):
        est.desenhar_mensagem_estacao(janela)

    # 10. Desenha a barra de vida do jogador - Desenha SEMPRE por cima
    # A barra de vida deve ser desenhada em uma posição FIXA na tela, sem o offset da câmera.
    if vida is not None and hasattr(vida, 'desenhar'):
        vida.desenhar(janela, 20, 20) # Posição fixa na tela


    # 11. Desenha o timer - Desenha SEMPRE por cima
    # O timer deve ser desenhado em uma posição FIXA na tela, sem o offset da câmera.
    if timer_obj is not None and hasattr(timer_obj, 'desenhar'):
        timer_obj.desenhar(janela, tempo_decorrido) # tempo_decorrido é o tempo em segundos


def tela_de_morte(janela):
    """Exibe a tela de morte e espera pela interação do jogador."""
    # Verifica si a janela é válida antes de tentar desenhar
    if janela is None:
        # print("AVISO(Game - Tela Morte): Objeto janela é None. Não foi possível exibir a tela de morte.") # Debug removido
        return # Sai da função si a janela não for válida

    # Verifica si pygame.font está inicializado antes de usar
    if pygame.font.get_init():
         fonte = pygame.font.Font(None, 45) # Ajuste o tamanho da fonte si necessário
    else:
         # print("AVISO(Game - Tela Morte): Pygame.font não inicializado. Não foi possível criar a fonte para a tela de morte.") # Debug removido
         fonte = None # Define como None si a fonte não puder ser criada


    # Renderiza o texto da mensagem de morte
    texto = None
    if fonte: # Verifica si a fonte foi criada com sucesso
        texto = fonte.render("Você morreu! Pressione R para reiniciar ou ESC para sair.", True, (255, 0, 0)) # Cor vermelha (ajuste)
        # Calcula a posição para centralizar o texto
        texto_rect = texto.get_rect(center=(janela.get_width() // 2, janela.get_height() // 2))
    # else:
         # print("AVISO(Game - Tela Morte): Texto da tela de morte não pôde ser renderizado.") # Debug removido


    # Para a música do jogo ao entrar na tela de morte
    pygame.mixer.music.stop()
    print("Jogo: Música do jogo parada.") # Mantido, é uma mensagem informativa do jogo

    # Loop da tela de morte
    while True:
        for evento in pygame.event.get():
            # Si o evento for fechar a janela, sai do jogo
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Si a tecla ESC for pressionada, sai do jogo
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # Si a tecla R for pressionada, reinicia o jogo chamando main()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                    # Antes de reiniciar, limpa o conjunto de blocos gerados para um novo mapa
                    # Verifica si o módulo mundo existe e tem o atributo blocos_gerados
                    if mundo is not None and hasattr(mundo, 'blocos_gerados'):
                         mundo.blocos_gerados.clear()
                    # Se a variável blocos_gerados estiver neste arquivo (Game.py), limpe-a aqui:
                    # global blocos_gerados
                    # blocos_gerados.clear()

                    main() # Chama a função principal para reiniciar o jogo
                    return # Sai da função tela_de_morte para voltar ao loop principal do jogo (reiniciado)

        # Preenche a tela com preto
        janela.fill((0, 0, 0))
        # Desenha o texto si ele foi renderizado com sucesso
        if texto:
            janela.blit(texto, texto_rect)
        # Atualiza a tela para mostrar as mudanças
        pygame.display.update()
        # Limita o framerate
        pygame.time.Clock().tick(60)

def main():
    """Função principal do jogo."""

    # Inicializa o Pygame
    pygame.init()
    try:
        # Inicializa o mixer de audio do Pygame
        pygame.mixer.init()
        print("Pygame: Mixer de audio inicializado com sucesso.") # Mantido, é uma mensagem informativa
    except pygame.error as e:
        print(f"Pygame: Erro ao inicializar o mixer de audio: {e}") # Mantido, é uma mensagem de erro

    # Obtém informações da tela do monitor
    info = pygame.display.Info()
    largura_tela = info.current_w
    altura_tela = info.current_h
    print(f"Resolução do monitor detectada: {largura_tela}x{altura_tela}") # Mantido, é uma mensagem informativa

    # Cria a janela do jogo em tela cheia
    janela = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN)
    # Define o título da janela
    pygame.display.set_caption("Lenda de Asrahel")
    # Cria um objeto Clock para controlar o framerate
    clock = pygame.time.Clock()

    # Inicializa o menu
    menu = Menu(largura_tela, altura_tela)

    # Variável para armazenar a ação selecionada no menu
    acao_menu = None

    # Loop do menu principal
    if menu is not None:
        while acao_menu is None:
            # Obtém a posição do mouse
            mouse_pos = pygame.mouse.get_pos()
            # Desenha o menu
            if hasattr(menu, 'desenhar'):
                 menu.desenhar(janela, mouse_pos)

            # Processa eventos do menu
            for evento in pygame.event.get():
                # Si o evento for fechar a janela, para a música do menu e sai do jogo
                if evento.type == pygame.QUIT:
                    if hasattr(menu, 'parar_musica'):
                         menu.parar_musica()
                    pygame.quit()
                    sys.exit()
                # Si o botão do mouse for pressionado
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    # Verifica qual botão do menu foi clicado
                    if hasattr(menu, 'verificar_click'):
                         acao_menu = menu.verificar_click(*evento.pos)
                         # Si a ação for sair, quebra o loop do menu
                         if acao_menu == "sair":
                             break

            # Atualiza a tela para mostrar o menu
            pygame.display.update()
            # Limita o framerate do menu
            clock.tick(60)

    # Si a ação selecionada for "jogar"
    if acao_menu == "jogar":
        # Para a música do menu si ele existia e tinha o método parar_musica
        if menu is not None and hasattr(menu, 'parar_musica'):
                 menu.parar_musica()
        print("Menu 'Jogar' selecionado. Inicializando jogo...") # Mantido, mensagem informativa

        # Inicializa os componentes do jogo, passando as dimensões da tela.
        # Adicionado shop_manager ao retorno
        inicializacao_resultado = inicializar_jogo(largura_tela, altura_tela)

        # Verifica se a inicialização foi bem-sucedida
        if inicializacao_resultado is not None:
             # Desempacota os resultados da inicialização
             jogador, est, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, jogador_morreu, tempo_inicio, timer_obj, shop_manager = inicializacao_resultado

             # Realiza o spawn inicial de inimigos após a criação da janela
             # Verifica si o gerenciador de inimigos, jogador e estacoes existem antes de tentar spawnar
             if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'spawn_inimigos') and jogador is not None and hasattr(jogador, 'rect') and est is not None and hasattr(est, 'i'):
                  gerenciador_inimigos.spawn_inimigos(est.i, jogador)


             print("Iniciando música do jogo...") # Mantido, mensagem informativa
             # Toca a música do jogo
             tocar_musica_jogo()

             # --- Variável para controlar o estado do jogo ---
             game_state = "playing" # Começa no estado de jogo normal

             # Verifica si o jogador e a vida foram inicializados corretamente
             if jogador is not None and vida is not None:
                 # Loop principal do jogo
                 running = True # Usamos 'running' agora para o loop principal
                 while running:
                     # Obtém o tempo decorrido desde o último frame em milissegundos
                     dt = clock.tick(60) # Limita o framerate a 60 FPS

                     # --- Processamento de Eventos ---
                     for evento in pygame.event.get():
                         # Si o evento for fechar a janela, para a música e sai do jogo
                         if evento.type == pygame.QUIT:
                             pygame.mixer.music.stop()
                             pygame.quit()
                             sys.exit()
                         # Si a tecla ESC for pressionada, para a música e sai do jogo
                         if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                                 # Se estiver na loja, volta para o jogo. Se estiver no jogo, sai.
                                 if shop_manager is not None and shop_manager.is_shop_open: # Verifica si a loja está aberta usando o ShopManager
                                     # Verifica se o shop_manager existe e tem o método para fechar a loja
                                     if hasattr(shop_manager, 'close_shop'):
                                          shop_manager.close_shop() # Chama o método para fechar a loja
                                     game_state = "playing" # Volta para o estado de jogo
                                     pygame.mixer.music.unpause() # Retoma a música do jogo
                                 else: # Não está na loja, então sai do jogo
                                     pygame.mixer.music.stop()
                                     pygame.quit()
                                     sys.exit()

                         # Processa input do jogador (movimento, etc.) - Apenas no estado "playing"
                         # A lógica de movimento contínuo é tratada no update do jogador usando pygame.key.get_pressed()
                         # A lógica de interação (como abrir a loja com 'E') é tratada aqui nos eventos
                         if game_state == "playing":
                              # Lógica de interação com a loja (pressionar 'E')
                              # Verifica se a loja existe, se o jogador está colidindo com ela e pressionou a tecla 'E'
                              keys = pygame.key.get_pressed() # Obtém o estado de todas as teclas
                              # Verifica se shop_manager existe antes de acessar seus atributos
                              if shop_manager is not None and shop_manager.current_shop_rect is not None and jogador is not None and hasattr(jogador, 'rect') and jogador.rect.colliderect(shop_manager.current_shop_rect) and evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
                                   if hasattr(shop_manager, 'run_shop_scene_from_game'):
                                        # Pausa a música do jogo antes de entrar na loja
                                        pygame.mixer.music.pause()
                                        # Chama o método do ShopManager que executa a cena da loja
                                        # Este método deve retornar True para continuar o jogo principal ou False para sair
                                        continue_game = shop_manager.run_shop_scene_from_game(janela, jogador) # Passa janela e jogador
                                        if continue_game:
                                             game_state = "playing" # Volta para o jogo se a loja não foi fechada pelo QUIT
                                             # Retoma a música do jogo ao sair da loja
                                             pygame.mixer.music.unpause()
                                             # Opcional: Remover a loja do mapa após sair? (Se for um spawn único)
                                             # shop_manager.current_shop_rect = None
                                             # shop_manager.shop_sprite_image = None
                                        else:
                                             running = False # Sair do loop principal se a cena da loja retornou False (QUIT)
                              # Outros inputs do jogador (ex: ataque com clique do mouse)
                              # if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1: # Clique esquerdo do mouse
                              #      if hasattr(jogador, 'atacar_com_mouse'): # Se o jogador tiver um método de ataque com mouse
                              #           jogador.atacar_com_mouse(evento.pos, gerenciador_inimigos.inimigos) # Passa a posição do clique e a lista de inimigos


                         # Processa eventos para o ShopManager (cliques nos botões da loja, fechar loja)
                         # Esta parte agora é tratada DENTRO do loop da cena da loja em ShopManager.run_shop_scene_from_game
                         pass # A lógica de interação da loja é tratada dentro do ShopManager.handle_event

                     # --- Lógica de Atualização ---
                     if game_state == "playing":
                         # Obtém o estado das teclas pressionadas (para movimento contínuo)
                         teclas = pygame.key.get_pressed()
                         # Move o jogador com base nas teclas pressionadas
                         # Verifica si o jogador existe e tem o método mover
                         if jogador is not None and hasattr(jogador, 'mover'):
                              jogador.mover(teclas, arvores) # Passa a lista de árvores para verificação de colisão


                         # Atualiza o estado do jogador (animação, etc.)
                         # Verifica si o jogador existe e tem o método update
                         if jogador is not None and hasattr(jogador, 'update'):
                              jogador.update()

                         # --- Chama a função para gerar elementos (incluindo a loja) ---
                         # Passa todos os objetos necessários para a geração, incluindo o shop_manager
                         # Verifica si a função existe (se estiver no módulo mundo, chame mundo.gerar_plantas_ao_redor_do_jogador)
                         if gerar_plantas_ao_redor_do_jogador is not None:
                              gerar_elementos_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados, shop_manager)
                         elif mundo is not None and hasattr(mundo, 'gerar_plantas_ao_redor_do_jogador'):
                              # Se a função foi movida para o módulo mundo
                              mundo.gerar_plantas_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados, shop_manager)


                         # Atualiza a estação e verifica si houve mudança
                         if est is not None and hasattr(est, 'i') and hasattr(est, 'atualizar') and hasattr(est, 'nome_estacao'):
                              est_ant = est.i # Armazena a estação anterior
                              est.atualizar() # Atualiza a estação
                              # Si a estação mudou
                              if est.i != est_ant:
                                 # Atualiza os sprites das árvores para a nova estação (si as árvores e o método existirem)
                                 if arvores is not None:
                                     for arv in arvores:
                                         if arv is not None and hasattr(arv, 'atualizar_sprite'):
                                              arv.atualizar_sprite(est.i)

                                 # Realiza spawns imediatos de inimigos para a nova estação (si o gerenciador e jogador existirem)
                                 if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'spawn_inimigos') and jogador is not None and hasattr(jogador, 'rect') and est is not None and hasattr(est, 'i'):
                                      gerenciador_inimigos.spawn_inimigos(est.i, jogador) # Passa estação e jogador


                         # Tenta spawnar inimigos periodicamente
                         if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'tentar_spawnar') and jogador is not None and hasattr(jogador, 'rect') and est is not None and hasattr(est, 'i'):
                               gerenciador_inimigos.tentar_spawnar(est.i, jogador) # Passa estação e jogador


                         # Atualiza o estado dos inimigos (movimento, etc.)
                         jogador_para_update_inimigos = jogador # Passa o jogador para que os inimigos possam persegui-lo
                         # Passando a lista de árvores para update_inimigos
                         if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'update_inimigos') and jogador_para_update_inimigos is not None and arvores is not None:
                              gerenciador_inimigos.update_inimigos(jogador_para_update_inimigos, arvores) # Passa jogador E arvores


                         # Atualiza o estado dos projéteis dos inimigos
                         if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'update_projeteis_inimigos') and jogador is not None:
                              gerenciador_inimigos.update_projeteis_inimigos(jogador) # Passa o jogador para detecção de colisão

                         # CHAMA O MÉTODO DE ATAQUE AUTOMÁTICO DO JOGADOR
                         # Verifica si o jogador e o gerenciador de inimigos existem
                         if jogador is not None and gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'inimigos') and hasattr(jogador, 'atacar'):
                                 jogador.atacar(gerenciador_inimigos.inimigos)


                         # Verifica colisões entre inimigos e o jogador (para o jogador receber dano)
                         # Verifica si os objetos necessários existem
                         if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'inimigos') and jogador is not None and vida is not None and hasattr(vida, 'receber_dano'):
                              verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador, vida)

                         # Verifica si o jogador morreu
                         # Verifica si o objeto vida existe e tem o método esta_vivo
                         if vida is not None and hasattr(vida, 'esta_vivo'):
                              if not vida.esta_vivo():
                                  jogador_morreu = True # Define a flag para sair do loop principal do jogo
                                  running = False # Sai do loop de jogo principal


                         # --- Atualiza os timers do pop-up e da seta da loja ---
                         # Verifica se o shop_manager existe antes de chamar o método de atualização de timers
                         # Passa o tempo decorrido em milissegundos (dt) para o update
                         if shop_manager is not None and hasattr(shop_manager, 'update_visuals_timers'):
                              shop_manager.update_visuals_timers(clock.get_rawtime()) # Usa o tempo real do frame


                     elif game_state == "shop":
                          # Lógica de atualização específica da loja, se houver (além do handle_event)
                          # A cena da loja é um loop próprio dentro de shop_manager.run_shop_scene_from_game
                          pass


                     # --- Desenho ---
                     # Calcula o offset da câmera para centralizar no jogador (apenas no estado "playing" ou se o jogador existir)
                     camera_x = 0
                     camera_y = 0
                     if jogador is not None and hasattr(jogador, 'rect'):
                            camera_x = jogador.rect.centerx - janela.get_width() // 2
                            camera_y = jogador.rect.centery - janela.get_height() // 2

                     # Desenha a cena apenas no estado "playing"
                     if game_state == "playing":
                          # Calcula o tempo decorrido em segundos desde o início do jogo (apenas no estado "playing")
                          tempo_decorrido_segundos = (pygame.time.get_ticks() - tempo_inicio) // 1000
                          # Passa todos os objetos necessários e o offset da câmera, incluindo o shop_manager
                          desenhar_cena(janela, est, gramas, arvores, jogador, gerenciador_inimigos, vida, camera_x, camera_y, tempo_decorrido_segundos, timer_obj, shop_manager)

                     elif game_state == "shop":
                          # Desenha a cena da loja (ShopManager deve lidar com isso)
                          # A cena da loja é desenhada dentro do loop em shop_manager.run_shop_scene_from_game
                          pass


                     # Atualiza a tela para mostrar as mudanças
                     pygame.display.flip()

                 # Se o loop principal terminou (jogador morreu ou saiu pelo QUIT/ESC), verifica se morreu para exibir a tela de morte
                 if jogador_morreu:
                      # Verifica si a janela existe antes de chamar tela_de_morte
                      if 'janela' in locals() and janela is not None:
                           tela_de_morte(janela)
                      # else:
                           # print("AVISO(Game): Objeto janela ausente. Não foi possível exibir a tela de morte.") # Debug removido
             else:
                  # Se o jogador ou vida não foram inicializados corretamente
                  print("ERRO FATAL: Jogador ou Vida não inicializados corretamente. Saindo.")
                  pygame.quit()
                  sys.exit()
        else:
            # Se a inicialização falhou (inicializacao_resultado é None)
            print("Falha na inicialização do jogo. Saindo.")
            pygame.quit()
            sys.exit()


    # Si a ação selecionada for "sair", fecha o Pygame
    elif acao_menu == "sair":
        if menu is not None and hasattr(menu, 'parar_musica'):
                 menu.parar_musica() # Para a música do menu
        pygame.quit()
        sys.exit()

    # Adicione lógica para outras opções do menu aqui (carregar, opções, creditos)
    # Por enquanto, elas apenas sairão do menu sem iniciar o jogo.
    else:
        if menu is not None and hasattr(menu, 'parar_musica'):
                 menu.parar_musica() # Para a música do menu
        pygame.quit()
        sys.exit()


# Ponto de entrada do programa
if __name__ == "__main__":
    # O jogo continua rodando até que a função main retorne (o que só acontece ao sair completamente)
    main()
