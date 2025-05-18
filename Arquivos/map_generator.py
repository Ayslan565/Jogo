# map_generator.py
import pygame
import random
import time
import math
import os

# Importa as classes e constantes necessárias do Game.py e outros módulos
# Certifique-se de que os caminhos de importação estão corretos
try:
    from player import Player
except ImportError:
    print("DEBUG(MapGenerator): Aviso: Módulo 'player.py' ou classe 'Player' não encontrado.")
    Player = None

try:
    from Estacoes import Estacoes
except ImportError:
    print("DEBUG(MapGenerator): Aviso: Módulo 'Estacoes.py' ou classe 'Estacoes' não encontrado.")
    Estacoes = None

try:
    from arvores import Arvore
except ImportError:
    print("DEBUG(MapGenerator): Aviso: Módulo 'arvores.py' ou classe 'Arvore' não encontrado.")
    Arvore = None

try:
    from grama import Grama
except ImportError:
    print("DEBUG(MapGenerator): Aviso: Módulo 'grama.py' ou classe 'Grama' não encontrado.")
    Grama = None

try:
    from loja import run_shop_scene # Necessário para verificar se a função da loja existe
except ImportError:
    print("DEBUG(MapGenerator): Aviso: Módulo 'loja.py' ou função 'run_shop_scene' não encontrado.")
    run_shop_scene = None

try:
    from Spawn_Loja import PROBABILIDADE_SPAWN_LOJA, INTERVALO_MINIMO_SPAWN_LOJA # Importa as constantes de spawn da loja
except ImportError:
    print("DEBUG(MapGenerator): Aviso: Módulo 'Spawn_Loja.py' ou variáveis 'PROBABILIDADE_SPAWN_LOJA', 'INTERVALO_MINIMO_SPAWN_LOJA' não encontrados.")
    PROBABILIDADE_SPAWN_LOJA = 0.0
    INTERVALO_MINIMO_SPAWN_LOJA = 0


# Variáveis globais relacionadas à loja (definidas em Game.py, acessadas aqui)
# Estas variáveis precisam ser globais em Game.py e acessadas aqui para serem modificadas
current_shop_rect = None
shop_sprite_image = None
last_shop_spawn_time = 0 # Tempo do último spawn bem-sucedido da loja

# Caminho para o sprite da loja no mapa (constante definida em Game.py, acessada aqui)
SHOP_SPRITE_PATH = None # Será definido em Game.py e acessado globalmente
# Tamanho do placeholder da loja se a imagem não carregar (constante definida em Game.py, acessada aqui)
SHOP_PLACEHOLDER_SIZE = (150, 150) # Será definido em Game.py e acessado globalmente

# Variáveis globais para o pop-up e seta da loja (definidas em Game.py, acessadas aqui)
shop_spawn_popup_message = ""
shop_popup_display_time = 0 # Tempo restante para exibir o pop-up (em milissegundos)
shop_arrow_visible = False
shop_arrow_display_time = 0 # Tempo restante para exibir a seta (em milissegundos)
shop_arrow_target_pos = (0, 0) # Posição do alvo da seta (centro da loja)


def gerar_elementos_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados):
    """
    Gera plantas (grama e árvores) e potencialmente a loja especial
    ao redor do jogador em blocos de mapa não gerados.
    Esta função agora acessa e modifica variáveis globais definidas em Game.py
    para gerenciar o spawn da loja.
    """
    # Acessa as variáveis globais definidas em Game.py
    global current_shop_rect, shop_sprite_image, last_shop_spawn_time
    global shop_spawn_popup_message, shop_popup_display_time, shop_arrow_visible, shop_arrow_display_time, shop_arrow_target_pos
    global SHOP_SPRITE_PATH, SHOP_PLACEHOLDER_SIZE, PROBABILIDADE_SPAWN_LOJA, INTERVALO_MINIMO_SPAWN_LOJA

    # Verifica se as constantes SHOP_SPRITE_PATH e SHOP_PLACEHOLDER_SIZE foram definidas em Game.py
    if SHOP_SPRITE_PATH is None:
        print("DEBUG(MapGenerator): Erro: SHOP_SPRITE_PATH não definido em Game.py. Não foi possível gerar a loja.")
        # Define um valor padrão ou placeholder para evitar erros
        SHOP_SPRITE_PATH = "Sprites/Loja/Placeholder.png" # Use um caminho que não deve existir
        SHOP_PLACEHOLDER_SIZE = (150, 150) # Use o tamanho padrão

    jogador = jogador # Renomeado para clareza, mas ainda é o mesmo objeto
    distancia_geracao = 1920  # distância do centro do jogador (usado implicitamente pelos blocos ao redor)
    bloco_tamanho = 1080  # tamanho do bloco usado para evitar gerar novamente

    # Verifica si o jogador e o objeto Estacoes existem antes de calcular o bloco
    if jogador is None or not hasattr(jogador, 'rect') or est is None:
        print("DEBUG(MapGenerator): Aviso: Jogador ou Estacoes ausente. Não foi possível gerar elementos.")
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

                print(f"DEBUG(MapGenerator): Gerando elementos para novo bloco: {bloco_coord}") # Debug geração de bloco

                # Gerar gramas nas bordas
                if Grama is not None:
                    for _ in range(random.randint(15, 25)):
                        x = base_x + random.randint(0, bloco_tamanho)
                        y = base_y + random.randint(0, bloco_tamanho)
                        gramas.append(Grama(x, y, 50, 50))
                else:
                    print("DEBUG(MapGenerator): Aviso: Classe Grama não disponível. Não foi possível gerar grama.")


                # Gerar árvores na área central
                if Arvore is not None and hasattr(est, 'i'):
                    for _ in range(random.randint(1, 3)):  # Menos árvores do que gramas
                        x = base_x + random.randint(bloco_tamanho // 4, 3 * bloco_tamanho // 4)
                        y = base_y + random.randint(bloco_tamanho // 4, 3 * bloco_tamanho // 4)
                        arvores.append(Arvore(x, y, 180, 180, est.i)) # Passa o índice da estação
                elif Arvore is None:
                    print("DEBUG(MapGenerator): Aviso: Classe Arvore não disponível. Não foi possível gerar árvores.")
                elif not hasattr(est, 'i'):
                     print("DEBUG(MapGenerator): Aviso: Objeto Estacoes não tem atributo 'i'. Não foi possível gerar árvores com estação correta.")


                # --- Lógica para spawnar a loja ---
                # Verifica si a loja ainda não existe no mundo
                # Verifica si a probabilidade de spawn é maior que 0 e a função run_shop_scene existe
                # E verifica si o intervalo mínimo desde o último spawn passou
                if current_shop_rect is None and PROBABILIDADE_SPAWN_LOJA > 0 and run_shop_scene is not None and \
                   (current_time - last_shop_spawn_time) >= INTERVALO_MINIMO_SPAWN_LOJA:

                    # Rola a "sorte" para spawnar a loja neste bloco
                    if random.random() < PROBABILIDADE_SPAWN_LOJA:
                        print(f"DEBUG(MapGenerator): Probabilidade de spawn da loja ({PROBABILIDADE_SPAWN_LOJA*100:.1f}%) bem-sucedida no bloco {bloco_coord} e intervalo mínimo passado!") # Debug spawn bem-sucedido

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
                                print(f"DEBUG(MapGenerator): Imagem da loja carregada para spawn: {SHOP_SPRITE_PATH}")
                            else:
                                print(f"DEBUG(MapGenerator): Aviso: Imagem da loja não encontrada para spawn: {SHOP_SPRITE_PATH}. Usando placeholder.")
                                # Cria um placeholder se a imagem não for encontrada
                                shop_sprite_image = pygame.Surface(SHOP_PLACEHOLDER_SIZE, pygame.SRCALPHA)
                                pygame.draw.rect(shop_sprite_image, (100, 50, 0), (0, 0, SHOP_PLACEHOLDER_SIZE[0], SHOP_PLACEHOLDER_SIZE[1])) # Placeholder marrom

                        except pygame.error as e:
                            print(f"DEBUG(MapGenerator): Erro ao carregar imagem da loja para spawn: {e}. Usando placeholder.")
                            # Cria um placeholder em caso de erro de carregamento
                            shop_sprite_image = pygame.Surface(SHOP_PLACEHOLDER_SIZE, pygame.SRCALPHA)
                            pygame.draw.rect(shop_sprite_image, (100, 50, 0), (0, 0, SHOP_PLACEHOLDER_SIZE[0], SHOP_PLACEHOLDER_SIZE[1])) # Placeholder marrom

                        # Cria o retângulo de colisão para a loja na posição calculada
                        if shop_sprite_image is not None:
                             current_shop_rect = shop_sprite_image.get_rect(topleft=shop_world_pos)
                             print(f"DEBUG(MapGenerator): Loja spawnada em ({shop_world_pos[0]}, {shop_world_pos[1]}).") # Debug posição spawn
                             last_shop_spawn_time = current_time # Atualiza o tempo do último spawn bem-sucedido

                             # --- Ativa o pop-up e a seta ---
                             shop_spawn_popup_message = "Uma loja apareceu!"
                             shop_popup_display_time = 3000 # Exibir pop-up por 3 segundos (em milissegundos)
                             shop_arrow_visible = True
                             shop_arrow_display_time = 10000 # Exibir seta por 10 segundos (em milissegundos)
                             # A seta aponta para o centro do retângulo da loja
                             shop_arrow_target_pos = current_shop_rect.center
                             print("DEBUG(MapGenerator): Pop-up e seta da loja ativados.") # Debug ativação visual

                        else:
                             print("DEBUG(MapGenerator): Aviso: Sprite da loja não disponível após carregamento. Não foi possível criar o retângulo de colisão.")

                # else:
                    # print(f"DEBUG(MapGenerator): Probabilidade de spawn da loja ({PROBABILIDADE_SPAWN_LOJA*100:.1f}%) falhou no bloco {bloco_coord}.") # Debug spawn falhou (opcional)

                # else:
                    # print(f"DEBUG(MapGenerator): Intervalo mínimo de spawn da loja ({INTERVALO_MINIMO_SPAWN_LOJA}s) ainda não passou.") # Debug intervalo não passou (opcional)

