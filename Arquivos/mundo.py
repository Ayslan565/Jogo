# mundo.py
# Responsável pela geração e gerenciamento de elementos do mundo (grama, árvores)

import pygame
import random
import math # Importa math para cálculos de distância
import os # Importa os para verificar a existência de arquivos

# Importa classes de elementos do mundo e configurações
try:
    from grama import Grama
except ImportError:
    print("AVISO(Mundo): Módulo 'grama.py' ou classe 'Grama' não encontrado.")
    Grama = None # Define como None para evitar NameError

try:
    from arvores import Arvore
except ImportError:
    print("AVISO(Mundo): Módulo 'arvores.py' ou classe 'Arvore' não encontrado.")
    Arvore = None # Define como None para evitar NameError

try:
    from Estacoes import Estacoes
except ImportError:
    print("AVISO(Mundo): Módulo 'Estacoes.py' ou classe 'Estacoes' não encontrado.")
    Estacoes = None # Define como None para evitar NameError

try:
    import config # Importa o arquivo de configuração
except ImportError:
    print("AVISO(Mundo): Módulo 'config.py' não encontrado.")
    config = None # Define como None para evitar NameError


# Armazena regiões já geradas (dividido em "blocos")
# Usado para evitar regenerar a mesma área várias vezes
blocos_gerados = set()

def gerar_plantas_ao_redor_do_jogador(jogador, gramas, arvores, est):
    """
    Gera grama e árvores em blocos ao redor do jogador para criar um mundo dinâmico.
    Evita regenerar blocos já gerados.

    Args:
        jogador (Player): O objeto jogador para determinar a posição central.
        gramas (list): Lista onde os objetos Grama serão adicionados.
        arvores (list): Lista onde os objetos Arvore serão adicionados.
        est (Estacoes): O objeto Estacoes para determinar a estação atual para as árvores.
    """
    # Verifica se os objetos necessários e seus atributos existem
    if jogador is None or not hasattr(jogador, 'rect') or est is None or not hasattr(est, 'i') or config is None:
        # print("DEBUG(Mundo): Aviso: Objetos necessários ou atributos ausentes para geração de plantas.") # Debug removido
        return # Sai da função se os objetos necessários não estiverem disponíveis

    # Obtém o tamanho do bloco do arquivo de configuração
    bloco_tamanho = config.BLOCK_SIZE

    # Calcula o bloco atual onde o jogador se encontra
    jogador_bloco_x = int(jogador.rect.centerx // bloco_tamanho)
    jogador_bloco_y = int(jogador.rect.centery // bloco_tamanho)

    # Explora ao redor do jogador (um grid de 3x3 blocos centrado no jogador)
    # Ajuste o range si quiser gerar uma área maior ou menor
    for dx in range(-1, 2): # Itera de -1 a 1 (total de 3 colunas)
        for dy in range(-1, 2): # Itera de -1 a 1 (total de 3 linhas)
            bloco_coord = (jogador_bloco_x + dx, jogador_bloco_y + dy)
            # Verifica si o bloco ainda não foi gerado
            if bloco_coord not in blocos_gerados:
                blocos_gerados.add(bloco_coord) # Marca o bloco como gerado
                # Calcula a posição inicial (canto superior esquerdo) do bloco
                base_x = (jogador_bloco_x + dx) * bloco_tamanho
                base_y = (jogador_bloco_y + dy) * bloco_tamanho

                # Gera um número aleatório de plantas dentro deste bloco
                # Ajuste a quantidade de plantas geradas por bloco aqui
                num_plantas = random.randint(5, 15) # Exemplo: entre 5 e 15 plantas por bloco

                for _ in range(num_plantas):
                    # Escolhe aleatoriamente si será grama ou árvore
                    # Ajuste as probabilidades si desejar mais de um tipo de planta
                    tipo_planta = random.choice(['grama', 'arvore']) # Exemplo: 50/50 chance

                    # Posição aleatória dentro do bloco atual
                    # Garante que a planta seja gerada dentro dos limites do bloco
                    x = base_x + random.randint(0, bloco_tamanho)
                    y = base_y + random.randint(0, bloco_tamanho)

                    # Cria a instância da planta correta, verificando si a classe foi importada
                    if tipo_planta == 'grama' and Grama is not None:
                         # Cria uma instância de Grama na posição calculada
                         gramas.append(Grama(x, y, 50, 50)) # Ajuste tamanho si necessário
                    elif tipo_planta == 'arvore' and Arvore is not None:
                         # Cria uma instância de Arvore na posição calculada, passando a estação atual
                         # Assume que a classe Arvore tem um __init__(x, y, largura, altura, estacao)
                         arvores.append(Arvore(x, y, 180, 180, est.i)) # Ajuste tamanho si necessário
                    # else:
                         # print(f"DEBUG(Mundo): Aviso: Tipo de planta desconhecido '{tipo_planta}' ou classe não importada.") # Debug removido

# Funções adicionais para gerenciar o mundo podem ser adicionadas aqui, como:
# - Remover plantas distantes do jogador para otimização
# - Gerenciar diferentes tipos de terrenos ou obstáculos
# - Salvar/carregar o estado do mundo
