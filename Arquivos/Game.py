# Game.py (ou o ficheiro que contém a função inicializar_jogo)
import pygame
import random
import time
import sys
import os # Importa os para ajudar a verificar caminhos

# Importa as classes necessárias
from player import Player
from Estacoes import Estacoes
from GerenciadorDeInimigos import GerenciadorDeInimigos
from arvores import Arvore
from grama import Grama
from vida import Vida
from Menu import Menu # Importa a classe Menu
from gerador_plantas import gerar_plantas_ao_redor_do_jogador
from timer1 import Timer
# Assumindo que você tem uma classe Camera em Camera.py
# from Camera import Camera # Certifique-se de que o nome do arquivo e da classe estão corretos


# >>> LISTA DE ARQUIVOS DE MÚSICA PARA O JOGO PRINCIPAL <<<
MUSICAS_JOGO = [
    "Musica\Gameplay\Faixa 1.mp3",
    "Musica\Gameplay\Faixa 2.mp3",
    "Musica\Gameplay\Faixa 3.mp3",
]

# Inicialização do jogo e variáveis
def inicializar_jogo(largura_tela, altura_tela):
    """Inicializa as variáveis e objetos do jogo."""
    print("DEBUG(Game): Inicializando componentes do jogo...")
    tempo_inicio = pygame.time.get_ticks()

    # Inicializa o jogador
    jogador = Player()
    # Assumindo que a classe Player tem um atributo rect ou rect_colisao

    # Inicializa as estações
    estacoes = Estacoes() # <<< Cria a instância de Estacoes aqui

    # Inicializa a vida do jogador
    vida = Vida(vida_maxima=100, vida_atual=100)
    # Assumindo que a classe Vida tem um método esta_vivo() e receber_dano()

    # Listas para elementos do mapa
    gramas = []
    arvores = []
    blocos_gerados = set() # Para controlar a geração de terreno

    # Inicializa o gerenciador de inimigos com parâmetros
    # >>> CORREÇÃO: Passa a instância de Estacoes para o GerenciadorDeInimigos <<<
    gerenciador_inimigos = GerenciadorDeInimigos(estacoes_obj=estacoes, intervalo_spawn=5.0, spawns_iniciais=3, limite_inimigos=150)
    print("DEBUG(Game): Gerenciador de Inimigos inicializado.")

    # Inicializa a câmera (exemplo - ajuste conforme sua implementação)
    # Se a sua classe Camera precisa de argumentos, ajuste aqui
    # camera = Camera(jogador, largura_tela, altura_tela) # Exemplo

    # >>> Spawna inimigos iniciais para a estação atual (obtida do objeto Estacoes) <<<
    # A lógica de spawn agora usa o objeto Estacoes interno do GerenciadorDeInimigos
    # Verifica se o jogador tem o atributo rect antes de passar para spawn_inimigos
    if hasattr(jogador, 'rect'):
        gerenciador_inimigos.spawn_inimigos(jogador) # <<< Não precisa passar a estação aqui
        print(f"DEBUG(Game): Spawns iniciais acionados.") # Debug
    else:
        print("DEBUG(Game): Aviso: Jogador não tem atributo 'rect'. Não foi possível acionar spawns iniciais.")


    # Cria uma instância do Timer.
    # Calcula a posição X para centralizar o fundo do timer.
    # A posição Y pode ser um valor fixo no topo.
    timer_pos_y = 30 # Posição Y fixa no topo
    # Para centralizar o timer, precisamos saber a largura do texto. Como a largura
    # do texto varia (MM:SS), é melhor calcular a posição X de desenho dentro
    # do método desenhar da classe Timer, mas podemos dar uma posição inicial aqui.
    # Uma estimativa simples para centralizar a área do timer:
    fonte_estimativa = pygame.font.Font(None, 36)
    largura_estimada_texto = fonte_estimativa.size("00:00")[0] # Largura estimada para "00:00"
    largura_estimada_fundo = largura_estimada_texto + 10 # Largura estimada do fundo
    # Usa a largura da tela dinâmica para centralizar
    timer_pos_x = largura_tela // 2 - largura_estimada_fundo // 2
    timer_obj = Timer(timer_pos_x, timer_pos_y)


    # Retorna todos os objetos e estados iniciais
    # Se estiver usando a classe Camera, retorne-a também:
    # return jogador, estacoes, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, False, tempo_inicio, camera, timer_obj
    return jogador, estacoes, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, False, tempo_inicio, timer_obj


def tocar_musica_jogo():
    """Carrega e toca uma música aleatória da lista de músicas do jogo em loop."""
    if not MUSICAS_JOGO:
        print("Jogo: Nenhuma música configurada para o jogo principal.")
        return

    musica_path = random.choice(MUSICAS_JOGO) # Seleciona uma música aleatória

    # Adicionado print para depuração
    print(f"Jogo: Tentando carregar música: {os.path.abspath(musica_path)}")

    try:
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play(-1) # O -1 faz a música tocar em loop infinito
        print(f"Jogo: Tocando música: {musica_path}")
    except pygame.error as e:
        print(f"Jogo: Erro ao carregar ou tocar a música '{musica_path}': {e}")
        # Se houver um erro, pode-se tentar tocar outra música ou apenas registrar o erro.
        # Por enquanto, apenas registramos o erro.


# Verifica colisões entre jogador e inimigos
def verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador, vida):
    """
    Verifica colisões entre o jogador e todos os inimigos e aplica dano.
    Usa colliderect() para detecção de colisão.
    """
    # Adiciona verificação para garantir que o jogador tem o atributo rect ou rect_colisao
    if not hasattr(jogador, 'rect') and not hasattr(jogador, 'rect_colisao'):
        # print("DEBUG(Game): Jogador não tem atributo 'rect' ou 'rect_colisao'. Não é possível verificar colisões com inimigos.")
        return # Sai da função se o jogador não tiver um retângulo de colisão

    # Usa rect_colisao se existir, caso contrário usa rect
    jogador_rect_colisao = getattr(jogador, 'rect_colisao', getattr(jogador, 'rect', None))

    if jogador_rect_colisao is None:
         # print("DEBUG(Game): Não foi possível obter o retângulo de colisão do jogador.")
         return # Sai da função se não foi possível obter o retângulo

    # Cria uma cópia da lista para iterar, pois inimigos podem ser removidos (se tiver lógica de remoção por dano)
    # Verifica se gerenciador_inimigos existe e tem a lista inimigos
    if not hasattr(gerenciador_inimigos, 'inimigos'):
         # print("DEBUG(Game): Gerenciador de inimigos não tem lista 'inimigos'. Não foi possível verificar colisões.")
         return

    for inimigo in list(gerenciador_inimigos.inimigos):
        # Verifica se o inimigo tem um método verificar_colisao ou usa colliderect diretamente
        # E se o inimigo tem um atributo rect
        if hasattr(inimigo, 'rect'):
            if hasattr(inimigo, 'verificar_colisao'):
                 if inimigo.verificar_colisao(jogador):
                     # Verifica se o jogador tem o método receber_dano e está vivo
                     if hasattr(vida, 'esta_vivo') and vida.esta_vivo() and hasattr(vida, 'receber_dano'):
                          vida.receber_dano(getattr(inimigo, 'contact_damage', 10)) # Aplica dano de contato do inimigo ou 10 por padrão
                          # print(f"DEBUG(Game): Colisão detectada com {type(inimigo).__name__}. Dano aplicado.") # Debug
                     # Opcional: Lógica de empurrar pode ser aqui ou no método atacar do inimigo
            elif inimigo.rect.colliderect(jogador_rect_colisao): # Usa o retângulo de colisão do jogador
                 # Verifica se o jogador tem o método receber_dano e está vivo
                 if hasattr(vida, 'esta_vivo') and vida.esta_vivo() and hasattr(vida, 'receber_dano'):
                      vida.receber_dano(getattr(inimigo, 'contact_damage', 10)) # Aplica dano de contato do inimigo ou 10 por padrão
                      # print(f"DEBUG(Game): Colisão detectada com {type(inimigo).__name__}. Dano aplicado.") # Debug
        # else:
            # print(f"DEBUG(Game): Inimigo do tipo {type(inimigo).__name__} não tem atributo 'rect'. Não é possível verificar colisão.") # Debug


# Desenha toda a cena (terreno, jogador, timer, vida)
# Agora recebe o objeto timer como argumento
# Adiciona camera_x e camera_y como argumentos para desenhar com offset
def atualizar_cena(est, gramas, arvores, jogador, janela, camera_x, camera_y, vida, tempo_decorrido, timer_obj):
    """
    Desenha todos os elementos da cena, incluindo terreno, plantas, jogador, vida e timer.
    Agora utiliza um objeto Timer para desenhar o timer.

    Args:
        est (Estacoes): Objeto da estação atual.
        gramas (list): Lista de objetos Grama.
        arvores (list): Lista de objetos Arvore.
        jogador (Player): Objeto do jogador.
        janela (pygame.Surface): A superfície onde desenhar.
        camera_x (int): O offset x da câmera.
        camera_y (int): O offset y da câmera.
        vida (Vida): Objeto de vida do jogador.
        tempo_decorrido (int): Tempo decorrido em segundos.
        timer_obj (Timer): Objeto Timer para desenhar.
    """
    # Desenha o plano de fundo da estação (se o objeto est existir e tiver método desenhar)
    if hasattr(est, 'desenhar'):
        est.desenhar(janela)
    # else:
        # print("DEBUG(Game): Objeto estacoes não tem método 'desenhar'. Não foi possível desenhar o fundo.")


    # Desenha gramas com offset da câmera
    for gr in gramas:
        if hasattr(gr, 'desenhar'):
             gr.desenhar(janela, camera_x, camera_y)
        # else:
             # print("DEBUG(Game): Objeto grama não tem método 'desenhar'.")


    # Separa árvores para desenhar atrás e na frente do jogador para ordem de desenho correta
    # Adiciona verificação se jogador tem rect antes de comparar
    if hasattr(jogador, 'rect'):
        arvores_tras = [a for a in arvores if hasattr(a, 'rect') and a.rect.bottom < jogador.rect.bottom]
        arvores_frente = [a for a in arvores if hasattr(a, 'rect') and a.rect.bottom >= jogador.rect.bottom]
    else:
        # Se o jogador não tem rect, desenha todas as árvores na ordem que estão na lista
        arvores_tras = arvores
        arvores_frente = [] # Nenhuma árvore na frente se não há jogador para comparar

    # Desenha árvores atrás do jogador
    for a in arvores_tras:
        if hasattr(a, 'desenhar'):
             a.desenhar(janela, camera_x, camera_y)
        # else:
             # print("DEBUG(Game): Objeto árvore (trás) não tem método 'desenhar'.")


    # Desenha o jogador centralizado na tela (se o jogador existir e tiver imagem e rect)
    if hasattr(jogador, 'image') and hasattr(jogador, 'rect'):
        janela.blit(jogador.image, (
            janela.get_width() // 2 - jogador.rect.width // 2,
            janela.get_height() // 2 - jogador.rect.height // 2
        ))
    # else:
        # print("DEBUG(Game): Jogador não tem imagem ou rect. Não foi possível desenhar o jogador.")


    # Desenha árvores na frente do jogador
    for a in arvores_frente:
        if hasattr(a, 'desenhar'):
             a.desenhar(janela, camera_x, camera_y)
        # else:
             # print("DEBUG(Game): Objeto árvore (frente) não tem método 'desenhar'.")


    # Desenha a mensagem da estação atual (se o objeto est existir e tiver método desenhar_mensagem_estacao)
    if hasattr(est, 'desenhar_mensagem_estacao'):
        est.desenhar_mensagem_estacao(janela)
    # else:
        # print("DEBUG(Game): Objeto estacoes não tem método 'desenhar_mensagem_estacao'. Não foi possível desenhar a mensagem da estação.")


    # Desenha a barra de vida (se o objeto vida existir e tiver método desenhar)
    if hasattr(vida, 'desenhar'):
        vida.desenhar(janela, 20, 20) # Desenha a barra de vida
    # else:
        # print("DEBUG(Game): Objeto vida não tem método 'desenhar'. Não foi possível desenhar a barra de vida.")


    # Desenha o timer usando o objeto Timer (se o objeto timer_obj existir e tiver método desenhar)
    if hasattr(timer_obj, 'desenhar'):
        timer_obj.desenhar(janela, tempo_decorrido)
    # else:
        # print("DEBUG(Game): Objeto timer_obj não tem método 'desenhar'. Não foi possível desenhar o timer.")


# Tela de morte e opções de reinício ou saída
def tela_de_morte(janela):
    """Exibe a tela de morte e aguarda a entrada do usuário para reiniciar ou sair."""
    fonte = pygame.font.Font(None, 45)
    texto = fonte.render("Você morreu! Pressione R para reiniciar ou ESC para sair.", True, (255, 0, 0))

    # Para a música do jogo antes de exibir a tela de morte
    pygame.mixer.music.stop()
    print("Jogo: Música do jogo parada.")


    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # Use sys.exit() para garantir que o programa feche completamente
                return # Sai da função tela_de_morte
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                 pygame.quit()
                 sys.exit()
                 return
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                 # Reinicia o jogo chamando main() novamente
                 main()
                 return # Sai da tela de morte para evitar loop infinito

        janela.fill((0, 0, 0)) # Preenche a tela com preto
        pos_x = janela.get_width() // 2 - texto.get_width() // 2
        pos_y = janela.get_height() // 2 - texto.get_height() // 2
        janela.blit(texto, (pos_x, pos_y)) # Desenha o texto de morte
        pygame.display.update() # Atualiza a tela
        pygame.time.Clock().tick(60) # Limita o FPS

# Função principal
def main():
    """Função principal que executa o loop do jogo, incluindo o menu."""
    # Inicializa todos os módulos do Pygame, incluindo o mixer de áudio
    pygame.init()
    try:
        pygame.mixer.init()
        print("Pygame: Mixer de audio inicializado com sucesso.")
    except pygame.error as e:
        print(f"Pygame: Erro ao inicializar o mixer de audio: {e}")
        # O jogo pode continuar sem áudio se o mixer falhar

    # >>> Obtém as dimensões do monitor atual <<<
    info = pygame.display.Info()
    largura_tela = info.current_w
    altura_tela = info.current_h
    print(f"Resolução do monitor detectada: {largura_tela}x{altura_tela}")


    # Cria a janela do jogo em tela cheia
    # Adiciona o flag pygame.FULLSCREEN para tela cheia
    janela = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN)
    pygame.display.set_caption("Lenda de Asrahel") # Define o título da janela
    clock = pygame.time.Clock() # Cria um objeto Clock para controlar o FPS

    # Cria uma instância do menu, passando as novas dimensões da tela
    menu = Menu(largura_tela, altura_tela)
    acao_menu = None # Variável para armazenar a ação selecionada no menu

    # >>> LOOP DO MENU <<<
    while acao_menu is None:
        mouse_pos = pygame.mouse.get_pos() # Obtém a posição do mouse para o efeito hover
        menu.desenhar(janela, mouse_pos) # Desenha o menu

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                menu.parar_musica() # Para a música do menu ao sair
                pygame.quit()
                sys.exit() # Sai do programa
            if evento.type == pygame.MOUSEBUTTONDOWN:
                acao_menu = menu.verificar_click(*evento.pos) # Verifica se uma opção foi clicada
                # Se a ação for sair, sai imediatamente do loop do menu
                if acao_menu == "sair":
                    break # Sai do loop for para ir para o if/elif/else abaixo

        pygame.display.update() # Atualiza a tela para mostrar o menu
        clock.tick(60) # Limita o FPS do menu

    # >>> FIM DO LOOP DO MENU <<<

    # Lógica após sair do loop do menu
    if acao_menu == "jogar":
        if hasattr(menu, 'parar_musica'):
             menu.parar_musica() # Para a música do menu APÓS sair do loop
        # else:
             # print("DEBUG(Game): Objeto menu não tem método 'parar_musica'.")
        print("Menu 'Jogar' selecionado. Inicializando jogo...") # Print para depuração

        # Inicializa todos os componentes do jogo
        # Passa as dimensões da tela para inicializar_jogo
        # Se estiver usando a classe Camera, inicialize-a dentro de inicializar_jogo
        jogador, est, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, jogador_morreu, tempo_inicio, timer_obj = inicializar_jogo(largura_tela, altura_tela)

        # >>> TOCA A MÚSICA DO JOGO PRINCIPAL AGORA <<<
        print("Iniciando música do jogo...") # Print para depuração
        tocar_musica_jogo()

        # Loop principal do jogo
        while not jogador_morreu:
            dt = clock.tick(60) # Controla o FPS e obtém o tempo desde o último frame

            # Lida com eventos do Pygame
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.mixer.music.stop() # Para a música ao sair
                    pygame.quit() # Sai do Pygame
                    sys.exit() # Sai da função main
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                     pygame.mixer.music.stop() # Para a música ao sair
                     pygame.quit()
                     sys.exit() # Sai da função main

                # Lida com input do jogador (se a classe Player tiver handle_input)
                if hasattr(jogador, 'handle_input'):
                     jogador.handle_input(evento)
                # else:
                     # print("DEBUG(Game): Jogador não tem método 'handle_input'.")


            # Obtém o estado das teclas pressionadas e move o jogador
            teclas = pygame.key.get_pressed()
            # Verifica se o jogador tem o método mover antes de chamar
            if hasattr(jogador, 'mover'):
                 jogador.mover(teclas, arvores) # Passa as árvores para colisão
            # else:
                 # print("DEBUG(Game): Jogador não tem método 'mover'.")


            # Atualiza o estado do jogador (animação, etc.) - ESSENCIAL PARA MOVIMENTO E ANIMAÇÃO
            # Verifica se o jogador tem o método update antes de chamar
            if hasattr(jogador, 'update'):
                 jogador.update() # <--- CHAMADA DO UPDATE DO JOGADOR
            # else:
                 # print("DEBUG(Game): Jogador não tem método 'update'.")


            # Gera plantas ao redor do jogador conforme ele se move
            # Verifica se o jogador tem o atributo rect antes de chamar
            if hasattr(jogador, 'rect'):
                 gerar_plantas_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados)
            # else:
                 # print("DEBUG(Game): Jogador não tem atributo 'rect'. Não foi possível gerar plantas.")


            # Detecta mudança de estação e atualiza árvores e spawna inimigos imediatamente
            # Verifica se o objeto est existe e tem o atributo i e método atualizar
            if hasattr(est, 'i') and hasattr(est, 'atualizar'):
                 est_ant = est.i
                 est.atualizar() # Atualiza a estação
                 if est.i != est_ant:
                     print(f"DEBUG(Game): Mudança de estação detectada: {est.nome_estacao()}") # Debug mudança de estação
                     # Atualiza os sprites das árvores para a nova estação
                     for arv in arvores:
                         if hasattr(arv, 'atualizar_sprite'):
                              arv.atualizar_sprite(est.i)
                         # else:
                              # print(f"DEBUG(Game): Árvore não tem método 'atualizar_sprite'.")

                     # Spawna inimigos imediatamente ao mudar de estação
                     # A lógica de spawn agora usa o objeto Estacoes interno do GerenciadorDeInimigos
                     # Verifica se o gerenciador_inimigos existe e tem o método spawn_inimigos
                     if hasattr(gerenciador_inimigos, 'spawn_inimigos') and hasattr(jogador, 'rect'):
                          gerenciador_inimigos.spawn_inimigos(jogador) # <<< Não precisa passar a estação aqui
                          print(f"DEBUG(Game): Spawns imediatos acionados para a nova estação.") # Debug
                     # else:
                          # print("DEBUG(Game): Gerenciador de inimigos ou jogador.rect ausente. Não foi possível spawnar inimigos na mudança de estação.")
            # else:
                 # print("DEBUG(Game): Objeto estacoes não tem atributos/métodos necessários para atualização de estação.")


            # Tenta spawnar inimigos periodicamente
            # Verifica se o gerenciador_inimigos existe e tem o método tentar_spawnar
            if hasattr(gerenciador_inimigos, 'tentar_spawnar') and hasattr(jogador, 'rect'):
                 gerenciador_inimigos.tentar_spawnar(jogador) # <<< Não precisa passar a estação aqui
            # else:
                 # print("DEBUG(Game): Gerenciador de inimigos ou jogador.rect ausente. Não foi possível tentar spawn periódico.")


            # Atualiza inimigos (movimento e ataque) - ESSENCIAL PARA O MOVIMENTO DO ESPANTALHO
            # Verifica se o gerenciador_inimigos existe e tem o método update_inimigos
            # Usa rect_colisao para o update dos inimigos se existir, caso contrário usa rect
            jogador_para_update_inimigos = jogador
            if not hasattr(jogador, 'rect_colisao') and hasattr(jogador, 'rect'):
                 jogador_para_update_inimigos = jogador # Usa o objeto jogador original se não tiver rect_colisao mas tiver rect
            elif not hasattr(jogador, 'rect_colisao') and not hasattr(jogador, 'rect'):
                 jogador_para_update_inimigos = None # Não passa o jogador se não tiver nem rect nem rect_colisao
                 # print("DEBUG(Game): Jogador não tem atributo 'rect_colisao' nem 'rect'. Não foi possível passar jogador para update de inimigos.")


            if hasattr(gerenciador_inimigos, 'update_inimigos') and jogador_para_update_inimigos is not None:
                 gerenciador_inimigos.update_inimigos(jogador_para_update_inimigos) # <--- CHAMADA DO UPDATE DOS INIMIGOS (que chama o update individual)
            elif hasattr(gerenciador_inimigos, 'update_inimigos') and jogador_para_update_inimigos is None:
                 # print("DEBUG(Game): Jogador ausente ou sem retângulos de colisão. Não foi possível atualizar inimigos.")
                 pass # Não chama o update se não há jogador válido
            # else:
                 # print("DEBUG(Game): Gerenciador de inimigos não tem método 'update_inimigos'.")


            # Câmera centralizada no jogador
            # Se estiver usando uma classe Camera, atualize-a aqui
            # camera.update() # Exemplo

            # Calcula o offset da câmera manualmente se não estiver usando uma classe Camera
            camera_x = 0
            camera_y = 0
            if hasattr(jogador, 'rect'):
                 camera_x = jogador.rect.centerx - janela.get_width() // 2
                 camera_y = jogador.rect.centery - janela.get_height() // 2
            # else:
                 # print("DEBUG(Game): Jogador não tem atributo 'rect'. Offset da câmera não calculado.")


            janela.fill((0, 0, 0)) # Preenche o fundo da janela

            # Desenha a cena com offset da câmera
            # Passa o objeto timer para a função atualizar_cena
            tempo_decorrido_segundos = (pygame.time.get_ticks() - tempo_inicio) // 1000
            # Verifica se todos os objetos necessários para atualizar_cena existem
            # Remove a verificação de hasattr(jogador, 'image') e hasattr(jogador, 'rect') aqui
            # porque a função atualizar_cena já faz essa verificação internamente para desenhar o jogador
            if hasattr(est, 'desenhar') and hasattr(vida, 'desenhar') and hasattr(timer_obj, 'desenhar'):
                 atualizar_cena(est, gramas, arvores, jogador, janela, camera_x, camera_y, vida, tempo_decorrido_segundos, timer_obj)
            # else:
                 # print("DEBUG(Game): Objetos necessários para atualizar_cena ausentes (exceto jogador image/rect). Não foi possível desenhar a cena.")


            # Desenha inimigos após a cena, com offset da câmera
            # Verifica se o gerenciador_inimigos existe e tem o método desenhar_inimigos
            if hasattr(gerenciador_inimigos, 'desenhar_inimigos'):
                 gerenciador_inimigos.desenhar_inimigos(janela, camera_x, camera_y)
            # else:
                 # print("DEBUG(Game): Gerenciador de inimigos não tem método 'desenhar_inimigos'.")


            # Verifica colisões entre jogador e inimigos e aplica dano
            # Verifica se todos os objetos necessários para verificar_colisoes_com_inimigos existem
            # Usa rect_colisao ou rect do jogador na verificação interna da função
            if hasattr(gerenciador_inimigos, 'inimigos') and (hasattr(jogador, 'rect') or hasattr(jogador, 'rect_colisao')) and hasattr(vida, 'receber_dano'):
                 verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador, vida)
            # else:
                 # print("DEBUG(Game): Objetos necessários para verificar_colisoes_com_inimigos ausentes.")


            # Verifica se o jogador morreu APÓS verificar colisões e aplicar dano
            # Verifica se o objeto vida existe e tem o método esta_vivo
            if hasattr(vida, 'esta_vivo'):
                 if not vida.esta_vivo():
                     jogador_morreu = True # Define a flag para sair do loop principal
            # else:
                 # print("DEBUG(Game): Objeto vida não tem método 'esta_vivo'. Não foi possível verificar a morte do jogador.")


            pygame.display.update() # Atualiza a tela para mostrar as mudanças

        # Se o loop principal terminou (jogador morreu), chama a tela de morte
        # Verifica se a janela existe antes de chamar tela_de_morte
        if 'janela' in locals() and janela is not None:
             tela_de_morte(janela)
        # else:
             # print("DEBUG(Game): Objeto janela ausente. Não foi possível exibir a tela de morte.")


    elif acao_menu == "sair":
        # Se a ação selecionada for "sair", fecha o Pygame
        if hasattr(menu, 'parar_musica'):
             menu.parar_musica() # Para a música do menu
        # else:
             # print("DEBUG(Game): Objeto menu não tem método 'parar_musica'.")
        pygame.quit()
        sys.exit()

    # Adicione lógica para outras opções do menu aqui (carregar, opções, creditos)
    # Por enquanto, elas apenas sairão do menu sem iniciar o jogo.
    else:
        if hasattr(menu, 'parar_musica'):
             menu.parar_musica() # Para a música do menu
        # else:
             # print("DEBUG(Game): Objeto menu não tem método 'parar_musica'.")
        pygame.quit()
        sys.exit()


# Executa a função main si o script for o ponto de entrada principal
if __name__ == "__main__":
    main()
