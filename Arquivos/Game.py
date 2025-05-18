# Game.py
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
    from gerador_plantas import gerar_plantas_ao_redor_do_jogador # Mantemos a importação para a função base
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'gerador_plantas.py' ou função 'gerar_plantas_ao_redor_do_jogador' não encontrado.")
    gerar_plantas_ao_redor_do_jogador = None

try:
    from timer1 import Timer
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'timer1.py' ou classe 'Timer' não encontrado.")
    Timer = None

# Importa a função para rodar a cena da loja
try:
    from loja import run_shop_scene
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'loja.py' ou função 'run_shop_scene' não encontrado.")
    run_shop_scene = None

# Importa a probabilidade e o intervalo mínimo de spawn da loja
try:
    from Spawn_Loja import PROBABILIDADE_SPAWN_LOJA, INTERVALO_MINIMO_SPAWN_LOJA
except ImportError:
    print("DEBUG(Game): Aviso: Módulo 'Spawn_Loja.py' ou variáveis 'PROBABILIDADE_SPAWN_LOJA', 'INTERVALO_MINIMO_SPAWN_LOJA' não encontrados.")
    PROBABILIDADE_SPAWN_LOJA = 0.0 # Define probabilidade zero se o arquivo não for encontrado
    INTERVALO_MINIMO_SPAWN_LOJA = 0 # Define intervalo zero se o arquivo não for encontrado


MUSICAS_JOGO = [
    "Musica/Gameplay/Faixa 1.mp3",
    "Musica/Gameplay/Faixa 2.mp3",
    "Musica/Gameplay/Faixa 3.mp3",
]

# Variáveis globais para gerenciar a loja no mapa
current_shop_rect = None
shop_sprite_image = None
last_shop_spawn_time = 0 # Novo: Tempo do último spawn bem-sucedido da loja

# Caminho para o sprite da loja no mapa
SHOP_SPRITE_PATH = "Sprites\Loja\Loja.png" # 
# Tamanho do placeholder da loja se a imagem não carregar
SHOP_PLACEHOLDER_SIZE = (150, 150)

# Variáveis globais para o pop-up e seta da loja
shop_spawn_popup_message = ""
shop_popup_display_time = 0 # Tempo restante para exibir o pop-up (em milissegundos)
shop_arrow_visible = False
shop_arrow_display_time = 0 # Tempo restante para exibir a seta (em milissegundos)
shop_arrow_target_pos = (0, 0) # Posição do alvo da seta (centro da loja)


def inicializar_jogo(largura_tela, altura_tela):
    """Inicializa os componentes do jogo."""
    global current_shop_rect, shop_sprite_image, last_shop_spawn_time # Declara como global para poder modificar

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
    gerenciador_inimigos = GerenciadorDeInimigos(estacoes_obj=estacoes, tela_largura=largura_tela, altura_tela=altura_tela) if GerenciadorDeInimigos is not None and estacoes is not None else None
    if gerenciador_inimigos is None:
        print("DEBUG(Game): Erro: Classe GerenciadorDeInimigos ou Estacoes não disponível. A gestão de inimigos não funcionará.")
    else:
        print("DEBUG(Game): Gerenciador de Inimigos inicializado.")

    # Inicializa a câmera (comentado, si você não estiver usando uma classe Camera separada)
    # camera = Camera(jogador, largura_tela, altura_tela) if Camera is not None and jogador is not None else None
    # if camera is None and Camera is not None:
    #     print("DEBUG(Game): Erro: Classe Camera disponível, mas jogador ausente. Não foi possível inicializar a câmera.")

    # Realiza o spawn inicial de inimigos si o gerenciador e o jogador estiverem disponíveis
    if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'spawn_inimigos') and jogador is not None and hasattr(jogador, 'rect'):
        gerenciador_inimigos.spawn_inimigos(jogador)
        print(f"DEBUG(Game): Spawns iniciais acionados.")
    elif gerenciador_inimigos is None:
        print("DEBUG(Game): Aviso: Gerenciador de Inimigos ausente. Spawns iniciais não acionados.")
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

    # --- A loja não é mais inicializada aqui, será spawnada dinamicamente ---
    current_shop_rect = None # Garante que a loja não existe no início
    shop_sprite_image = None # Garante que a imagem não existe no início
    last_shop_spawn_time = time.time() # Inicializa o tempo do último spawn da loja com o tempo de início do jogo

    # Retorna os objetos inicializados e o estado inicial do jogo
    # Remove shop_object_rect do retorno, pois ele será gerenciado globalmente
    return jogador, estacoes, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, False, tempo_inicio, timer_obj

# --- Função modificada para gerar plantas E potencialmente a loja ---
def gerar_elementos_ao_redor_do_jogador(Asrahel, gramas, arvores, est, blocos_gerados):
    """
    Gera plantas (grama e árvores) e potencialmente a loja especial
    ao redor do jogador em blocos de mapa não gerados.
    """
    global current_shop_rect, shop_sprite_image, last_shop_spawn_time # Acessa variáveis globais
    global shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time, shop_arrow_target_pos # Acessa variáveis do pop-up/seta
    global SHOP_SPRITE_PATH, SHOP_PLACEHOLDER_SIZE, PROBABILIDADE_SPAWN_LOJA, INTERVALO_MINIMO_SPAWN_LOJA # Acessa constantes

    jogador = Asrahel
    distancia_geracao = 1920  # distância do centro do jogador (usado implicitamente pelos blocos ao redor)
    bloco_tamanho = 1080  # tamanho do bloco usado para evitar gerar novamente

    # Verifica si o jogador e o objeto Estacoes existem antes de calcular o bloco
    if jogador is None or not hasattr(jogador, 'rect') or est is None:
        print("DEBUG(Game): Aviso: Jogador ou Estacoes ausente. Não foi possível gerar elementos.")
        return

    jogador_bloco_x = int(jogador.rect.centerx // bloco_tamanho) # Usa centerx/centery para o centro do bloco
    jogador_bloco_y = int(jogador.rect.centery // bloco_tamanho)

    current_time = time.time() # Tempo atual para verificar o intervalo de spawn

    # Explora ao redor do jogador (9 blocos)
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            bloco_coord = (jogador_bloco_x + dx, jogador_bloco_y + dy)

            # Processa apenas blocos que ainda não foram gerados
            if bloco_coord not in blocos_gerados:
                blocos_gerados.add(bloco_coord)
                base_x = (jogador_bloco_x + dx) * bloco_tamanho
                base_y = (jogador_bloco_y + dy) * bloco_tamanho

                print(f"DEBUG(Game): Gerando elementos para novo bloco: {bloco_coord}") # Debug geração de bloco

                # Gerar gramas nas bordas
                if Grama is not None:
                    for _ in range(random.randint(15, 25)):
                        x = base_x + random.randint(0, bloco_tamanho)
                        y = base_y + random.randint(0, bloco_tamanho)
                        gramas.append(Grama(x, y, 50, 50))
                else:
                    print("DEBUG(Game): Aviso: Classe Grama não disponível. Não foi possível gerar grama.")


                # Gerar árvores na área central
                if Arvore is not None and hasattr(est, 'i'):
                    for _ in range(random.randint(1, 3)):  # Menos árvores do que gramas
                        x = base_x + random.randint(bloco_tamanho // 4, 3 * bloco_tamanho // 4)
                        y = base_y + random.randint(bloco_tamanho // 4, 3 * bloco_tamanho // 4)
                        arvores.append(Arvore(x, y, 180, 180, est.i)) # Passa o índice da estação
                elif Arvore is None:
                    print("DEBUG(Game): Aviso: Classe Arvore não disponível. Não foi possível gerar árvores.")
                elif not hasattr(est, 'i'):
                     print("DEBUG(Game): Aviso: Objeto Estacoes não tem atributo 'i'. Não foi possível gerar árvores com estação correta.")


                # --- Lógica para spawnar a loja ---
                # Verifica si a loja ainda não existe no mundo
                # Verifica si a probabilidade de spawn é maior que 0 e a função run_shop_scene existe
                # E verifica si o intervalo mínimo desde o último spawn passou
                if current_shop_rect is None and PROBABILIDADE_SPAWN_LOJA > 0 and run_shop_scene is not None and \
                   (current_time - last_shop_spawn_time) >= INTERVALO_MINIMO_SPAWN_LOJA:

                    # Rola a "sorte" para spawnar a loja neste bloco
                    if random.random() < PROBABILIDADE_SPAWN_LOJA:
                        print(f"DEBUG(Game): Probabilidade de spawn da loja ({PROBABILIDADE_SPAWN_LOJA*100:.1f}%) bem-sucedida no bloco {bloco_coord} e intervalo mínimo passado!") # Debug spawn bem-sucedido

                        # Calcula uma posição aleatória para a loja dentro deste bloco
                        shop_x = base_x + random.randint(50, bloco_tamanho - SHOP_PLACEHOLDER_SIZE[0] - 50) # Garante margem
                        shop_y = base_y + random.randint(50, bloco_tamanho - SHOP_PLACEHOLDER_SIZE[1] - 50) # Garante margem
                        shop_world_pos = (shop_x, shop_y)

                        # Tenta carregar a imagem da loja
                        try:
                            if os.path.exists(SHOP_SPRITE_PATH):
                                shop_sprite_image = pygame.image.load(SHOP_SPRITE_PATH).convert_alpha()
                                # Opcional: Redimensionar a imagem da loja se necessário
                                # shop_sprite_image = pygame.transform.scale(shop_sprite_image, (200, 200)) # Exemplo de redimensionamento
                                print(f"DEBUG(Game): Imagem da loja carregada para spawn: {SHOP_SPRITE_PATH}")
                            else:
                                print(f"DEBUG(Game): Aviso: Imagem da loja não encontrada para spawn: {SHOP_SPRITE_PATH}. Usando placeholder.")
                                # Cria um placeholder se a imagem não for encontrada
                                shop_sprite_image = pygame.Surface(SHOP_PLACEHOLDER_SIZE, pygame.SRCALPHA)
                                pygame.draw.rect(shop_sprite_image, (100, 50, 0), (0, 0, SHOP_PLACEHOLDER_SIZE[0], SHOP_PLACEHOLDER_SIZE[1])) # Placeholder marrom

                        except pygame.error as e:
                            print(f"DEBUG(Game): Erro ao carregar imagem da loja para spawn: {e}. Usando placeholder.")
                            # Cria um placeholder em caso de erro de carregamento
                            shop_sprite_image = pygame.Surface(SHOP_PLACEHOLDER_SIZE, pygame.SRCALPHA)
                            pygame.draw.rect(shop_sprite_image, (100, 50, 0), (0, 0, SHOP_PLACEHOLDER_SIZE[0], SHOP_PLACEHOLDER_SIZE[1])) # Placeholder marrom

                        # Cria o retângulo de colisão para a loja na posição calculada
                        if shop_sprite_image is not None:
                             current_shop_rect = shop_sprite_image.get_rect(topleft=shop_world_pos)
                             print(f"DEBUG(Game): Loja spawnada em ({shop_world_pos[0]}, {shop_world_pos[1]}).") # Debug posição spawn
                             last_shop_spawn_time = current_time # Atualiza o tempo do último spawn bem-sucedido

                             # --- Ativa o pop-up e a seta ---
                             shop_spawn_popup_message = "Uma loja apareceu!"
                             shop_popup_display_time = 3000 # Exibir pop-up por 3 segundos (em milissegundos)
                             shop_arrow_visible = True
                             shop_arrow_display_time = 10000 # Exibir seta por 10 segundos (em milissegundos)
                             # A seta aponta para o centro do retângulo da loja
                             shop_arrow_target_pos = current_shop_rect.center
                             print("DEBUG(Game): Pop-up e seta da loja ativados.") # Debug ativação visual

                        else:
                             print("DEBUG(Game): Aviso: Sprite da loja não disponível após carregamento. Não foi possível criar o retângulo de colisão.")

                # else:
                    # print(f"DEBUG(Game): Probabilidade de spawn da loja ({PROBABILIDADE_SPAWN_LOJA*100:.1f}%) falhou no bloco {bloco_coord}.") # Debug spawn falhou (opcional)

                # else:
                    # print(f"DEBUG(Game): Intervalo mínimo de spawn da loja ({INTERVALO_MINIMO_SPAWN_LOJA}s) ainda não passou.") # Debug intervalo não passou (opcional)


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
    global shop_sprite_image, current_shop_rect # Acessa a imagem e o retângulo da loja
    global shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time, shop_arrow_target_pos # Acessa variáveis do pop-up/seta

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

    # --- Desenha o sprite da loja no mundo do jogo (se existir) ---
    # Verifica se a imagem da loja e o retângulo existem
    if shop_sprite_image is not None and current_shop_rect is not None:
        # Calcula a posição da imagem na tela com o offset da câmera
        shop_screen_pos = (current_shop_rect.x - camera_x, current_shop_rect.y - camera_y)
        janela.blit(shop_sprite_image, shop_screen_pos)
    # else:
        # print("DEBUG(Game): Aviso: Sprite da loja ou retângulo não disponíveis para desenho.") # Debug (opcional, pode poluir)


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

    # Desenha os projéteis dos inimigos
    if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'desenhar_projeteis_inimigos'):
        gerenciador_inimigos.desenhar_projeteis_inimigos(janela, camera_x, camera_y)
    elif gerenciador_inimigos is None:
        print("DEBUG(Game): Gerenciador de inimigos ausente. Não foi possível desenhar projéteis dos inimigos.")


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

    # --- Desenha o pop-up da loja (se ativo) ---
    if shop_popup_display_time > 0 and shop_spawn_popup_message:
        # Usa uma fonte simples para o pop-up
        try:
            popup_font = pygame.font.Font(None, 40)
            popup_text_surface = popup_font.render(shop_spawn_popup_message, True, (255, 255, 255))
            # Posiciona o pop-up no centro superior da tela
            popup_rect = popup_text_surface.get_rect(center=(janela.get_width() // 2, 80))
            # Desenha um fundo semi-transparente para o pop-up (opcional)
            popup_bg = pygame.Surface((popup_rect.width + 20, popup_rect.height + 10), pygame.SRCALPHA)
            popup_bg.fill((0, 0, 0, 180)) # Fundo preto semi-transparente
            janela.blit(popup_bg, (popup_rect.x - 10, popup_rect.y - 5))
            janela.blit(popup_text_surface, popup_rect)
        except pygame.error as e:
            print(f"DEBUG(Game): Erro ao desenhar pop-up da loja: {e}")


    # --- Desenha a seta apontando para a loja (se ativa) ---
    if shop_arrow_visible and current_shop_rect is not None and jogador is not None and hasattr(jogador, 'rect'):
        # Calcula a posição do centro da tela
        screen_center_x = janela.get_width() // 2
        screen_center_y = janela.get_height() // 2
        screen_center = (screen_center_x, screen_center_y)

        # Calcula a posição da loja na tela (com offset da câmera)
        shop_screen_center_x = current_shop_rect.centerx - camera_x
        shop_screen_center_y = current_shop_rect.centery - camera_y
        shop_screen_center = (shop_screen_center_x, shop_screen_center_y)

        # Calcula o vetor da tela para a loja na tela
        direction_vector = (shop_screen_center_x - screen_center_x, shop_screen_center_y - screen_center_y)

        # Calcula a distância até a loja na tela
        distance_to_shop_on_screen = math.hypot(direction_vector[0], direction_vector[1])

        # Define a posição inicial da seta (um pouco afastada do centro da tela)
        arrow_start_distance = 100 # Distância do centro da tela onde a seta começa
        arrow_length = 30 # Comprimento da seta

        # Desenha a seta apenas se a loja estiver fora da área visível central
        if distance_to_shop_on_screen > arrow_start_distance:
            # Normaliza o vetor de direção
            if distance_to_shop_on_screen > 0:
                direction_norm = (direction_vector[0] / distance_to_shop_on_screen,
                                  direction_vector[1] / distance_to_shop_on_screen)
            else:
                direction_norm = (0, 0) # Evita divisão por zero

            # Calcula a posição inicial da seta na tela
            arrow_start_x = screen_center_x + direction_norm[0] * arrow_start_distance
            arrow_start_y = screen_center_y + direction_norm[1] * arrow_start_distance
            arrow_start_pos = (arrow_start_x, arrow_start_y)

            # Calcula a posição final da seta (ponta)
            arrow_end_x = arrow_start_x + direction_norm[0] * arrow_length
            arrow_end_y = arrow_start_y + direction_norm[1] * arrow_length
            arrow_end_pos = (arrow_end_x, arrow_end_y)

            # Desenha a linha principal da seta
            pygame.draw.line(janela, (255, 255, 0), arrow_start_pos, arrow_end_pos, 3) # Seta amarela

            # Desenha as pontas da seta (triângulo)
            # Calcula o ângulo da seta
            angle = math.atan2(direction_norm[1], direction_norm[0])
            # Calcula os pontos da base do triângulo da ponta
            arrowhead_size = 10
            point1 = (arrow_end_x - arrowhead_size * math.cos(angle - math.pi / 6),
                      arrow_end_y - arrowhead_size * math.sin(angle - math.pi / 6))
            point2 = (arrow_end_x - arrowhead_size * math.cos(angle + math.pi / 6),
                      arrow_end_y - arrowhead_size * math.sin(angle + math.pi / 6))
            # Desenha o triângulo da ponta
            pygame.draw.polygon(janela, (255, 255, 0), [arrow_end_pos, point1, point2]) # Seta amarela

        # else:
             # print("DEBUG(Game): Loja muito perto do centro da tela. Seta não desenhada.") # Debug (opcional)


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
    global shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time # Acessa variáveis do pop-up/seta

    # Inicializa o Pygame
    pygame.init()
    try:
        # Inicializa o mixer de audio do Pygame
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

        # Inicializa os componentes do jogo, passando as dimensões da tela.
        # Remove shop_object_rect do retorno, pois será gerenciado globalmente
        jogador, est, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, jogador_morreu, tempo_inicio, timer_obj = inicializar_jogo(largura_tela, altura_tela)

        print("Iniciando música do jogo...")
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
                            pygame.mixer.music.stop()
                            pygame.quit()
                            sys.exit()

                    # Processa input do jogador (movimento, etc.) - Apenas no estado "playing"
                    if game_state == "playing" and hasattr(jogador, 'handle_input'):
                         jogador.handle_input(evento)

                # --- Lógica de Atualização ---
                if game_state == "playing":
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

                    # --- Chama a função para gerar elementos (incluindo a loja) ---
                    # Passa todos os objetos necessários para a geração
                    gerar_elementos_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados)


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

                    # Atualiza o estado dos projéteis dos inimigos
                    if gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'update_projeteis_inimigos') and jogador is not None:
                            gerenciador_inimigos.update_projeteis_inimigos(jogador) # Passa o jogador para detecção de colisão
                    elif gerenciador_inimigos is None:
                            print("DEBUG(Game): Gerenciador de inimigos ausente. Não foi possível atualizar projéteis dos inimigos.")
                    elif jogador is None:
                            print("DEBUG(Game): Jogador ausente. Não foi possível atualizar projéteis dos inimigos.")

                    # CHAMA O MÉTODO DE ATAQUE AUTOMÁTICO DO JOGADOR
                    # Verifica si o jogador e o gerenciador de inimigos existem
                    if jogador is not None and gerenciador_inimigos is not None and hasattr(gerenciador_inimigos, 'inimigos'):
                            jogador.atacar(gerenciador_inimigos.inimigos)
                    elif jogador is None:
                            print("DEBUG(Game): Jogador ausente. Não foi possível chamar o ataque do jogador.")
                    elif gerenciador_inimigos is None or not hasattr(gerenciador_inimigos, 'inimigos'):
                            print("DEBUG(Game): Gerenciador de inimigos ausente ou sem lista de inimigos. Não foi possível chamar o ataque do jogador.")

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
                                jogador_morreu = True # Define a flag para sair do loop principal do jogo
                                running = False # Sai do loop de jogo principal
                    elif vida is None:
                            print("DEBUG(Game): Objeto vida ausente. Não foi possível verificar a morte do jogador.")
                    elif not hasattr(vida, 'esta_vivo'):
                            print("DEBUG(Game): Objeto vida não tem método 'esta_vivo'. Não foi possível verificar a morte do jogador.")

                    # --- Lógica de Interação com a Loja ---
                    # Verifica se a loja existe, se o jogador está colidindo com ela e pressionou a tecla de interação
                    keys = pygame.key.get_pressed()
                    if current_shop_rect is not None and jogador is not None and hasattr(jogador, 'rect') and jogador.rect.colliderect(current_shop_rect) and keys[pygame.K_e]:
                         if run_shop_scene is not None:
                             print("DEBUG(Game): Colisão com a loja e 'E' pressionado. Entrando na loja.")
                             # Pausa a música do jogo antes de entrar na loja
                             pygame.mixer.music.pause()
                             # Muda o estado do jogo para "shop"
                             game_state = "shop"
                         else:
                              print("DEBUG(Game): Função run_shop_scene não disponível. Não foi possível entrar na loja.")

                    # --- Atualiza os timers do pop-up e da seta da loja ---
                    current_ticks = pygame.time.get_ticks()
                    if shop_popup_display_time > 0:
                         shop_popup_display_time -= clock.get_rawtime() # Usa o tempo real do frame
                         if shop_popup_display_time <= 0:
                              shop_spawn_popup_message = "" # Limpa a mensagem
                              print("DEBUG(Game): Timer do pop-up da loja expirou.") # Debug

                    if shop_arrow_display_time > 0:
                         shop_arrow_display_time -= clock.get_rawtime() # Usa o tempo real do frame
                         if shop_arrow_display_time <= 0:
                              shop_arrow_visible = False # Esconde a seta
                              print("DEBUG(Game): Timer da seta da loja expirou.") # Debug


                elif game_state == "shop":
                    # --- Lógica da Loja ---
                    # A função run_shop_scene gerencia tudo enquanto o estado é "shop"
                    # Ela retorna True para continuar o jogo ou False para sair completamente
                    # Verifica si a função run_shop_scene existe antes de chamá-la
                    if run_shop_scene is not None:
                        continue_game = run_shop_scene(janela, jogador, largura_tela, altura_tela) # Passa janela, jogador, largura, altura
                        if continue_game:
                            game_state = "playing" # Volta para o jogo se a loja não foi fechada pelo QUIT
                            print("DEBUG(Game): Saindo da loja, voltando para o jogo.")
                            # Retoma a música do jogo ao sair da loja
                            pygame.mixer.music.unpause()
                            # Opcional: Remover a loja do mapa após sair? (Se for um spawn único)
                            # current_shop_rect = None
                            # shop_sprite_image = None
                        else:
                            running = False # Sair do loop principal se a cena da loja retornou False (QUIT)
                            print("DEBUG(Game): Saindo da loja, fechando o jogo.")
                    else:
                         print("DEBUG(Game): Função run_shop_scene não disponível. Não foi possível rodar a cena da loja.")
                         game_state = "playing" # Volta para o jogo se a função não existe


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
                     # Passa todos os objetos necessários e o offset da câmera
                     desenhar_cena(janela, est, gramas, arvores, jogador, gerenciador_inimigos, vida, camera_x, camera_y, tempo_decorrido_segundos, timer_obj)

                # Atualiza a tela para mostrar as mudanças
                pygame.display.flip()

            # Se o loop principal terminou (jogador morreu ou saiu pelo QUIT na loja), verifica se morreu para exibir a tela de morte
            if jogador_morreu:
                 # Verifica si a janela existe antes de chamar tela_de_morte
                 if 'janela' in locals() and janela is not None:
                     tela_de_morte(janela)
                 else:
                     print("DEBUG(Game): Objeto janela ausente. Não foi possível exibir a tela de morte.")


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
    main()
