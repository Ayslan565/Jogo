# Game.py
import pygame
import random
import time
import sys
import os # Importa os para ajudar a verificar caminhos

# Importa as classes necessárias
# Adicionado try-except para cada importação para robustez
try:
    from player import Player
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'player.py' ou classe 'Player' não encontrado.")
    Player = None # Define como None para evitar NameError

try:
    from Estacoes import Estacoes
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'Estacoes.py' ou classe 'Estacoes' não encontrado.")
    Estacoes = None # Define como None para evitar NameError

try:
    from GerenciadorDeInimigos import GerenciadorDeInimigos
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'GerenciadorDeInimigos.py' ou classe 'GerenciadorDeInimigos' não encontrado.")
    GerenciadorDeInimigos = None # Define como None para evitar NameError

try:
    from arvores import Arvore
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'arvores.py' ou classe 'Arvore' não encontrado.")
    Arvore = None # Define como None para evitar NameError

try:
    from grama import Grama
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'grama.py' ou classe 'Grama' não encontrado.")
    Grama = None # Define como None para evitar NameError

try:
    from vida import Vida
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'vida.py' ou classe 'Vida' não encontrado.")
    Vida = None # Define como None para evitar NameError

try:
    from Menu import Menu
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'Menu.py' ou classe 'Menu' não encontrado.")
    Menu = None # Define como None para evitar NameError

try:
    from gerador_plantas import gerar_plantas_ao_redor_do_jogador
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'gerador_plantas.py' ou função 'gerar_plantas_ao_redor_do_jogador' não encontrado.")
    gerar_plantas_ao_redor_do_jogador = None

try:
    from timer1 import Timer
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'timer1.py' ou classe 'Timer' não encontrado.")
    Timer = None

# try:
#     from Camera import Camera
# except ImportError:
#     print("DEBUG(Game): Aviso: Módulo 'Camera.py' ou classe 'Camera' não encontrado.")
#     Camera = None


MUSICAS_JOGO = [
    "Musica/Gameplay/Faixa 1.mp3",
    "Musica/Gameplay/Faixa 2.mp3",
    "Musica/Gameplay/Faixa 3.mp3",
]

def inicializar_jogo(largura_tela, altura_tela):
    """Inicializa os componentes do jogo."""
    print("DEBUG(Game): Inicializando componentes do jogo...")
    # Captura o tempo de início em milissegundos
    tempo_inicio = pygame.time.get_ticks()

    # Inicializa o jogador (verifica si a classe Player foi importada)
    jogador = Player() if Player is not None else None
    if jogador is None:
        print("DEBUG(Game): Erro: Classe Player não disponível. Não foi possível inicializar o jogador.")

    # Inicializa as estações (verifica si a classe Estacoes foi importada)
    estacoes = Estacoes() if Estacoes is not None else None
    if estacoes is None:
        print("DEBUG(Game): Erro: Classe Estacoes não disponível. A gestão de estações e spawns pode não funcionar corretamente.")

    # Inicializa a vida do jogador (verifica si a classe Vida foi importada)
    vida = Vida(vida_maxima=100, vida_atual=100) if Vida is not None else None
    if vida is None:
        print("DEBUG(Game): Erro: Classe Vida não disponível. A gestão de vida do jogador pode não funcionar corretamente.")

    # Inicializa listas para gramas e árvores
    gramas = []
    arvores = []
    # Conjunto para rastrear blocos de mapa já gerados
    blocos_gerados = set()

    # Inicializa o gerenciador de inimigos (verifica si as classes foram importadas)
    gerenciador_inimigos = GerenciadorDeInimigos(estacoes_obj=estacoes) if GerenciadorDeInimigos is not None and estacoes is not None else None
    if gerenciador_inimigos is None:
         print("DEBUG(Game): Erro: Classe GerenciadorDeInimigos ou Estacoes não disponível. A gestão de inimigos não funcionará.")
    else:
        print("DEBUG(Game): Gerenciador de Inimigos inicializado.")

    # Inicializa a câmera (comentado, si você não estiver usando uma classe Camera separada)
    # camera = Camera(jogador, largura_tela, altura_tela) if Camera is not None and jogador is not None else None
    # if camera is None and Camera is not None:
    #      print("DEBUG(Game): Erro: Classe Camera disponível, mas jogador ausente. Não foi possível inicializar a câmera.")

    # Realiza o spawn inicial de inimigos si o gerenciador e o jogador estiverem disponíveis
    if gerenciador_inimigos is not None and jogador is not None and hasattr(jogador, 'rect'):
        gerenciador_inimigos.spawn_inimigos(jogador)
        print(f"DEBUG(Game): Spawns iniciais acionados.")
    elif gerenciador_inimigos is None:
         print("DEBUG(Game): Aviso: Gerenciador de Inimigos não disponível. Spawns iniciais não acionados.")
    elif jogador is None or not hasattr(jogador, 'rect'):
         print("DEBUG(Game): Aviso: Jogador ausente ou sem atributo 'rect'. Spawns iniciais não acionados.")

    # Inicializa o objeto Timer (verifica si a classe Timer foi importada)
    timer_obj = None
    if Timer is not None:
        # Calcula a posição do timer na tela
        timer_pos_y = 30
        fonte_estimativa = pygame.font.Font(None, 36) # Fonte para estimar o tamanho
        largura_estimada_texto = fonte_estimativa.size("00:00")[0] # Estima a largura do texto do timer
        largura_estimada_fundo = largura_estimada_texto + 10 # Adiciona um pouco de padding para o fundo
        timer_pos_x = largura_tela // 2 - largura_estimada_fundo // 2 # Centraliza horizontalmente
        timer_obj = Timer(timer_pos_x, timer_pos_y)
    else:
        print("DEBUG(Game): Aviso: Classe Timer não disponível. O timer não funcionará.")

    # Retorna os objetos inicializados e o estado inicial do jogo
    return jogador, estacoes, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, False, tempo_inicio, timer_obj

def tocar_musica_jogo():
    """Carrega e toca uma música aleatória do jogo em loop."""
    if not MUSICAS_JOGO:
        print("Jogo: Nenhuma música configurada para o jogo principal.")
        return

    # Seleciona uma música aleatória da lista
    musica_path = random.choice(MUSICAS_JOGO)

    print(f"Jogo: Tentando carregar música: {os.path.abspath(musica_path)}")

    try:
        # Carrega a música
        pygame.mixer.music.load(musica_path)
        # Toca a música em loop infinito (-1)
        pygame.mixer.music.play(-1)
        print(f"Jogo: Tocando música: {musica_path}")
    except pygame.error as e:
        print(f"Jogo: Erro ao carregar ou tocar a música '{musica_path}': {e}")

def verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador, vida):
    """Verifica colisões entre o jogador e os inimigos para aplicar dano ao jogador."""
    # Verifica si os objetos necessários existem antes de proceder
    if jogador is None or vida is None or not hasattr(vida, 'esta_vivo') or not hasattr(vida, 'receber_dano'):
         return

    # Obtém o retângulo de colisão do jogador (preferindo rect_colisao si existir)
    jogador_rect_colisao = getattr(jogador, 'rect_colisao', getattr(jogador, 'rect', None))

    # Si o retângulo de colisão do jogador não existir, retorna
    if jogador_rect_colisao is None:
         return

    # Verifica si o gerenciador de inimigos existe e tem uma lista de inimigos
    if gerenciador_inimigos is None or not hasattr(gerenciador_inimigos, 'inimigos'):
         return

    # Itera sobre uma cópia da lista de inimigos para evitar problemas si um inimigo for removido durante a iteração
    for inimigo in list(gerenciador_inimigos.inimigos):
        # Verifica si o inimigo existe e tem um retângulo de colisão
        if inimigo is not None and hasattr(inimigo, 'rect'):
             # Verifica si o inimigo tem um método de verificação de colisão customizado
             if hasattr(inimigo, 'verificar_colisao'):
                 if inimigo.verificar_colisao(jogador):
                     # Si o jogador estiver vivo, aplica dano a ele
                     if vida.esta_vivo():
                          # Obtém o dano de contato do inimigo (padrão 10 si não existir)
                          vida.receber_dano(getattr(inimigo, 'contact_damage', 10))
             # Si o inimigo não tem um método customizado, usa a verificação de colisão de retângulos do Pygame
             elif inimigo.rect.colliderect(jogador_rect_colisao):
                 # Si o jogador estiver vivo, aplica dano a ele
                 if vida.esta_vivo():
                      # Obtém o dano de contato do inimigo (padrão 10 si não existir)
                      vida.receber_dano(getattr(inimigo, 'contact_damage', 10))

def desenhar_cena(janela, est, gramas, arvores, jogador, gerenciador_inimigos, vida, camera_x, camera_y, tempo_decorrido, timer_obj):
    """Desenha todos os elementos da cena na janela, considerando o offset da câmera."""
    # Preenche o fundo da janela (pode ser uma cor ou uma imagem de fundo)
    janela.fill((0, 0, 0)) # Fundo preto

    # Desenha a estação (fundo ou elementos estáticos)
    if est is not None and hasattr(est, 'desenhar'):
        est.desenhar(janela)

    # Desenha a grama (elementos do cenário)
    if gramas is not None:
        for gr in gramas:
            if gr is not None and hasattr(gr, 'desenhar'):
                 gr.desenhar(janela, camera_x, camera_y)

    # Desenha as árvores (elementos do cenário)
    if arvores is not None:
        for a in arvores:
            if a is not None and hasattr(a, 'desenhar'):
                 a.desenhar(janela, camera_x, camera_y)

    # Desenha o jogador (usando o método desenhar da classe Player)
    # Este método já considera o offset da câmera e desenha a hitbox de ataque si necessário
    if jogador is not None and hasattr(jogador, 'desenhar'):
        jogador.desenhar(janela, camera_x, camera_y)
    elif jogador is None:
         print("DEBUG(Game): Jogador ausente. Não foi possível desenhar o jogador.")
    elif not hasattr(jogador, 'desenhar'):
         print("DEBUG(Game): Jogador não tem método 'desenhar'. Não foi possível desenhar o jogador.")


    # Desenha os inimigos
    if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'desenhar_inimigos'):
         gerenciador_inimigos.desenhar_inimigos(janela, camera_x, camera_y)
    elif gerenciador_inimigos is None:
         print("DEBUG(Game): Gerenciador de inimigos ausente. Não foi possível desenhar inimigos.")


    # Desenha a mensagem da estação (si houver)
    if est is not None and hasattr(est, 'desenhar_mensagem_estacao'):
        est.desenhar_mensagem_estacao(janela)

    # Desenha a barra de vida do jogador
    if vida is not None and hasattr(vida, 'desenhar'):
        vida.desenhar(janela, 20, 20) # Posição fixa na tela
    elif vida is None:
         print("DEBUG(Game): Objeto vida ausente. Não foi possível desenhar a vida do jogador.")
    elif not hasattr(vida, 'desenhar'):
         print("DEBUG(Game): Objeto vida não tem método 'desenhar'. Não foi possível desenhar a vida do jogador.")


    # Desenha o timer
    if timer_obj is not None and hasattr(timer_obj, 'desenhar'):
        timer_obj.desenhar(janela, tempo_decorrido) # tempo_decorrido é o tempo em segundos
    elif timer_obj is None:
         print("DEBUG(Game): Objeto timer ausente. Não foi possível desenhar o timer.")
    elif not hasattr(timer_obj, 'desenhar'):
         print("DEBUG(Game): Objeto timer não tem método 'desenhar'. Não foi possível desenhar o timer.")


def tela_de_morte(janela):
    """Exibe a tela de morte e espera pela interação do jogador."""
    fonte = pygame.font.Font(None, 45)
    texto = fonte.render("Você morreu! Pressione R para reiniciar ou ESC para sair.", True, (255, 0, 0))

    # Para a música do jogo ao entrar na tela de morte
    pygame.mixer.music.stop()
    print("Jogo: Música do jogo parada.")

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
                 main()
                 return # Sai da função tela_de_morte para voltar ao loop principal do jogo (reiniciado)

        # Preenche a tela com preto
        janela.fill((0, 0, 0))
        # Calcula a posição para centralizar o texto
        pos_x = janela.get_width() // 2 - texto.get_width() // 2
        pos_y = janela.get_height() // 2 - texto.get_height() // 2
        # Desenha o texto na janela
        janela.blit(texto, (pos_x, pos_y))
        # Atualiza a tela para mostrar as mudanças
        pygame.display.update()
        # Limita o framerate
        pygame.time.Clock().tick(60)

def main():
    """Função principal do jogo."""
    # Inicializa o Pygame
    pygame.init()
    try:
        # Inicializa o mixer de áudio do Pygame
        pygame.mixer.init()
        print("Pygame: Mixer de audio inicializado com sucesso.")
    except pygame.error as e:
        print(f"Pygame: Erro ao inicializar o mixer de audio: {e}")

    # Obtém informações da tela do monitor
    info = pygame.display.Info()
    largura_tela = info.current_w
    altura_tela = info.current_h
    print(f"Resolução do monitor detectada: {largura_tela}x{altura_tela}")

    # Cria a janela do jogo em tela cheia
    janela = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN)
    # Define o título da janela
    pygame.display.set_caption("Lenda de Asrahel")
    # Cria um objeto Clock para controlar o framerate
    clock = pygame.time.Clock()

    # Inicializa o menu (verifica si a classe Menu foi importada)
    menu = Menu(largura_tela, altura_tela) if Menu is not None else None
    if menu is None:
        print("DEBUG(Game): Erro: Classe Menu não disponível. O menu não funcionará.")

    # Variável para armazenar a ação selecionada no menu
    acao_menu = None

    # Loop do menu principal
    if menu is not None:
        while acao_menu is None:
            # Obtém a posição do mouse
            mouse_pos = pygame.mouse.get_pos()
            # Desenha o menu
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

    # Si a ação selecionada no menu for "jogar"
    if acao_menu == "jogar":
        # Para a música do menu si ele existia e tinha o método parar_musica
        if menu is not None and hasattr(menu, 'parar_musica'):
             menu.parar_musica()
        print("Menu 'Jogar' selecionado. Inicializando jogo...")

        # Inicializa os componentes do jogo
        jogador, est, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, jogador_morreu, tempo_inicio, timer_obj = inicializar_jogo(largura_tela, altura_tela)

        print("Iniciando música do jogo...")
        # Toca a música do jogo
        tocar_musica_jogo()

        # Verifica si o jogador e a vida foram inicializados corretamente
        if jogador is not None and vida is not None:
            # Loop principal do jogo
            while not jogador_morreu:
                # Obtém o tempo decorrido desde o último frame em milissegundos
                dt = clock.tick(60) # Limita o framerate a 60 FPS

                # Processa eventos do jogo
                for evento in pygame.event.get():
                    # Si o evento for fechar a janela, para a música e sai do jogo
                    if evento.type == pygame.QUIT:
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()
                    # Si a tecla ESC for pressionada, para a música e sai do jogo
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                         pygame.mixer.music.stop()
                         pygame.quit()
                         sys.exit()

                    # Processa input do jogador (movimento, etc.) - O ataque é automático agora
                    # Verifica si o jogador existe e tem o método handle_input (si ainda for necessário para outras ações)
                    if hasattr(jogador, 'handle_input'):
                         jogador.handle_input(evento)

                # Obtém o estado das teclas pressionadas
                teclas = pygame.key.get_pressed()
                # Move o jogador com base nas teclas pressionadas
                # Verifica si o jogador existe e tem o método mover
                if hasattr(jogador, 'mover'):
                     jogador.mover(teclas, arvores) # Passa a lista de árvores para verificação de colisão
                elif jogador is None:
                     print("DEBUG(Game): Jogador ausente. Não foi possível mover o jogador.")
                elif not hasattr(jogador, 'mover'):
                     print("DEBUG(Game): Jogador não tem método 'mover'. Não foi possível mover o jogador.")


                # Atualiza o estado do jogador (animação, etc.)
                # Verifica si o jogador existe e tem o método update
                if hasattr(jogador, 'update'):
                     jogador.update()
                elif jogador is None:
                     print("DEBUG(Game): Jogador ausente. Não foi possível atualizar o jogador.")
                elif not hasattr(jogador, 'update'):
                     print("DEBUG(Game): Jogador não tem método 'update'. Não foi possível atualizar o jogador.")


                # Gera plantas ao redor do jogador si a função e objetos necessários existirem
                if gerar_plantas_ao_redor_do_jogador is not None and jogador is not None and hasattr(jogador, 'rect') and est is not None and blocos_gerados is not None:
                     gerar_plantas_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados)
                elif gerar_plantas_ao_redor_do_jogador is None:
                     print("DEBUG(Game): Função gerar_plantas_ao_redor_do_jogador ausente. Geração de plantas não funcionará.")
                elif jogador is None or not hasattr(jogador, 'rect') or est is None or blocos_gerados is None:
                     print("DEBUG(Game): Objetos necessários para gerar_plantas_ao_redor_do_jogador ausentes. Geração de plantas não funcionará.")


                # Atualiza a estação e verifica si houve mudança
                if est is not None and hasattr(est, 'i') and hasattr(est, 'atualizar') and hasattr(est, 'nome_estacao'):
                     est_ant = est.i # Armazena a estação anterior
                     est.atualizar() # Atualiza a estação
                     # Si a estação mudou
                     if est.i != est_ant:
                         print(f"DEBUG(Game): Mudança de estação detectada: {est.nome_estacao()}")
                         # Atualiza os sprites das árvores para a nova estação (si as árvores e o método existirem)
                         if arvores is not None:
                             for arv in arvores:
                                 if arv is not None and hasattr(arv, 'atualizar_sprite'):
                                      arv.atualizar_sprite(est.i)

                         # Realiza spawns imediatos de inimigos para a nova estação (si o gerenciador e jogador existirem)
                         if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'spawn_inimigos') and jogador is not None and hasattr(jogador, 'rect'):
                              gerenciador_inimigos.spawn_inimigos(jogador)
                              print(f"DEBUG(Game): Spawns imediatos acionados para a nova estação.")
                         elif gerenciador_inimigos is None:
                              print("DEBUG(Game): Gerenciador de inimigos ausente. Não foi possível spawnar inimigos na mudança de estação.")
                         elif jogador is None or not hasattr(jogador, 'rect'):
                              print("DEBUG(Game): Jogador ausente ou sem rect. Não foi possível spawnar inimigos na mudança de estação.")
                elif est is None:
                     print("DEBUG(Game): Objeto estação ausente. Gestão de estações não funcionará.")
                elif not hasattr(est, 'i') or not hasattr(est, 'atualizar') or not hasattr(est, 'nome_estacao'):
                     print("DEBUG(Game): Objeto estação não tem métodos/atributos necessários. Gestão de estações não funcionará.")


                # Tenta spawnar inimigos periodicamente
                if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'tentar_spawnar') and jogador is not None and hasattr(jogador, 'rect'):
                     gerenciador_inimigos.tentar_spawnar(jogador)
                elif gerenciador_inimigos is None:
                     print("DEBUG(Game): Gerenciador de inimigos ausente. Não foi possível tentar spawn periódico.")
                elif jogador is None or not hasattr(jogador, 'rect'):
                     print("DEBUG(Game): Jogador ausente ou sem rect. Não foi possível tentar spawn periódico.")


                # Atualiza o estado dos inimigos (movimento, etc.)
                jogador_para_update_inimigos = jogador # Passa o jogador para que os inimigos possam persegui-lo
                if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'update_inimigos') and jogador_para_update_inimigos is not None:
                     gerenciador_inimigos.update_inimigos(jogador_para_update_inimigos)
                elif gerenciador_inimigos is None:
                     print("DEBUG(Game): Gerenciador de inimigos ausente. Não foi possível atualizar inimigos.")
                elif jogador_para_update_inimigos is None:
                     print("DEBUG(Game): Jogador ausente. Não foi possível atualizar inimigos.")


                # Calcula o offset da câmera para centralizar no jogador
                camera_x = 0
                camera_y = 0
                if jogador is not None and hasattr(jogador, 'rect'):
                     camera_x = jogador.rect.centerx - janela.get_width() // 2
                     camera_y = jogador.rect.centery - janela.get_height() // 2
                elif jogador is None:
                     print("DEBUG(Game): Jogador ausente. Offset da câmera não calculado.")
                elif not hasattr(jogador, 'rect'):
                     print("DEBUG(Game): Jogador não tem atributo 'rect'. Offset da câmera não calculado.")


                # Calcula o tempo decorrido em segundos desde o início do jogo
                # pygame.time.get_ticks() retorna milissegundos
                tempo_decorrido_segundos = (pygame.time.get_ticks() - tempo_inicio) // 1000
                # print(f"DEBUG(Game): tempo_decorrido_segundos: {tempo_decorrido_segundos}") # Print de depuração

                # >>> CHAMA O MÉTODO DE ATAQUE AUTOMÁTICO DO JOGADOR <<<
                # Verifica si o jogador e o gerenciador de inimigos existem
                if jogador is not None and gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'inimigos'):
                    jogador.atacar(gerenciador_inimigos.inimigos)
                elif jogador is None:
                     print("DEBUG(Game): Jogador ausente. Não foi possível chamar o ataque do jogador.")
                elif gerenciador_inimigos is None or not hasattr(gerenciador_inimigos, 'inimigos'):
                     print("DEBUG(Game): Gerenciador de inimigos ausente ou sem lista de inimigos. Não foi possível chamar o ataque do jogador.")


                # Desenha todos os elementos na tela
                # Passa todos os objetos necessários e o offset da câmera
                # A função desenhar_cena foi criada para organizar o desenho
                desenhar_cena(janela, est, gramas, arvores, jogador, gerenciador_inimigos, vida, camera_x, camera_y, tempo_decorrido_segundos, timer_obj)


                # Verifica colisões entre inimigos e o jogador (para o jogador receber dano)
                # Verifica si os objetos necessários existem
                if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'inimigos') and jogador is not None and vida is not None and hasattr(vida, 'receber_dano'):
                     verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador, vida)
                elif gerenciador_inimigos is None or not hasattr(gerenciador_inimigos, 'inimigos'):
                     print("DEBUG(Game): Gerenciador de inimigos ausente ou sem lista de inimigos. Não foi possível verificar colisões (inimigo -> jogador).")
                elif jogador is None or vida is None or not hasattr(vida, 'receber_dano'):
                     print("DEBUG(Game): Jogador, Vida ou método de Vida ausente. Não foi possível verificar colisões (inimigo -> jogador).")


                # Verifica si o jogador morreu
                # Verifica si o objeto vida existe e tem o método esta_vivo
                if vida is not None and hasattr(vida, 'esta_vivo'):
                     if not vida.esta_vivo():
                         jogador_morreu = True # Define a flag para sair do loop principal
                elif vida is None:
                     print("DEBUG(Game): Objeto vida ausente. Não foi possível verificar a morte do jogador.")
                elif not hasattr(vida, 'esta_vivo'):
                     print("DEBUG(Game): Objeto vida não tem método 'esta_vivo'. Não foi possível verificar a morte do jogador.")


                # Atualiza a tela para mostrar as mudanças
                pygame.display.update()

            # Se o loop principal terminou (jogador morreu), chama a tela de morte
            # Verifica si a janela existe antes de chamar tela_de_morte
            if 'janela' in locals() and janela is not None:
                 tela_de_morte(janela)
            else:
                 print("DEBUG(Game): Objeto janela ausente. Não foi possível exibir a tela de morte.")


    # Si a ação selecionada for "sair", fecha o Pygame
    elif acao_menu == "sair":
        if menu is not None and hasattr(menu, 'parar_musica'):
             menu.parar_musica() # Para a música do menu
        # else:
             # print("DEBUG(Game): Objeto menu não disponível ou não tem método 'parar_musica'.")
        pygame.quit()
        sys.exit()

    # Adicione lógica para outras opções do menu aqui (carregar, opções, creditos)
    # Por enquanto, elas apenas sairão do menu sem iniciar o jogo.
    else:
        if menu is not None and hasattr(menu, 'parar_musica'):
             menu.parar_musica() # Para a música do menu
        # else:
             # print("DEBUG(Game): Objeto menu não disponível ou não tem método 'parar_musica'.")
        pygame.quit()
        sys.exit()


# Ponto de entrada do programa
if __name__ == "__main__":
    main()
