import random
from grama import Grama
from arvores import Arvore
from Estacoes import Estacoes
from vida import Vida
from player import Player

# Armazena regiões já geradas (dividido em "blocos")
blocos_gerados = set()
Asrahel = Player()

def gerar_plantas_ao_redor_do_jogador(Asrahel, gramas, arvores, est, blocos_gerados):
    jogador = Asrahel
    distancia_geracao = 1920  # distância do centro do jogador
    bloco_tamanho = 1080  # tamanho do bloco usado para evitar gerar novamente

    jogador_bloco_x = jogador.rect.x // bloco_tamanho
    jogador_bloco_y = jogador.rect.y // bloco_tamanho

    # Explora ao redor do jogador (9 blocos)
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            bloco_coord = (jogador_bloco_x + dx, jogador_bloco_y + dy)
            if bloco_coord not in blocos_gerados:
                blocos_gerados.add(bloco_coord)
                base_x = (jogador_bloco_x + dx) * bloco_tamanho
                base_y = (jogador_bloco_y + dy) * bloco_tamanho

                # Gerar gramas nas bordas
                for _ in range(random.randint(15, 25)):
                    tipo_planta = 'grama'
                    # Gerar no limite do bloco (bordas)
                    x = base_x + random.randint(0, bloco_tamanho)
                    y = base_y + random.randint(0, bloco_tamanho)
                    gramas.append(Grama(x, y, 50, 50))

                # Gerar árvores na área central
                for _ in range(random.randint(1, 15)):  # Menos árvores do que gramas
                    tipo_planta = 'arvore'
                    # Gerar no centro do bloco
                    x = base_x + random.randint(bloco_tamanho // 4, 3 * bloco_tamanho // 4)
                    y = base_y + random.randint(bloco_tamanho // 4, 3 * bloco_tamanho // 4)
                    arvores.append(Arvore(x, y, 180, 180, est.i))
