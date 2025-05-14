# combate.py

import math
import time # Usaremos time.time() para o cooldown do jogador
import pygame # Importa pygame para usar pygame.Rect

# Não importamos Player ou Inimigo diretamente aqui para manter o módulo mais genérico,
# mas a função espera objetos que tenham os atributos e métodos necessários.

# --- FUNÇÃO PRINCIPAL DE COMBATE AUTOMÁTICO DO JOGADOR ---

def gerenciar_combate_automatico(player, lista_inimigos):
    """
    Gerencia o sistema de combate automático do jogador.
    O jogador ataca automaticamente o inimigo mais próximo dentro do alcance
    se o cooldown permitir.

    Args:
        player: O objeto do jogador. Deve ter os atributos:
                .rect (pygame.Rect) para posição.
                .dano (int/float) para o dano do ataque.
                .alcance_ataque (int/float) para a distância máxima do ataque.
                .cooldown_ataque (int/float) para o tempo de espera entre ataques (em segundos).
                .tempo_ultimo_ataque (float) para o timestamp do último ataque (deve ser atualizado por esta função).

        lista_inimigos: Uma lista ou grupo de objetos inimigos. Cada inimigo deve ter:
                        .rect (pygame.Rect) para posição.
                        .hp (int/float) para os pontos de vida.
                        .receber_dano(dano) (método) para aplicar dano.
                        .kill() (método herdado de pygame.sprite.Sprite para remoção).

    Returns:
        tuple or None: Retorna uma tupla (player_center_x, player_center_y, alcance_ataque)
                       se um ataque ocorreu, caso contrário, retorna None.
                       Isso é usado para desenhar a área de ataque visualmente.
    """

    # Pega o tempo atual
    agora = time.time()

    # Verifica se o cooldown do ataque do jogador já passou
    if agora - player.tempo_ultimo_ataque < player.cooldown_ataque:
        return None # Cooldown ainda ativo, não pode atacar, retorna None

    # Encontrar o inimigo mais próximo dentro do alcance de ataque
    inimigo_mais_proximo = None
    distancia_minima = float('inf') # Inicializa com uma distância infinita

    # Itera sobre a lista de inimigos para encontrar o mais próximo
    # Use uma cópia se a lista puder ser modificada (embora a remoção de mortos
    # geralmente ocorra após chamar esta função no loop principal)
    for inimigo in lista_inimigos:
        # Garante que o inimigo é válido, não é None e tem um rect
        if inimigo and hasattr(inimigo, 'rect'):
            # Calcula a distância entre o centro do jogador e o centro do inimigo
            # Usando math.dist (Python 3.8+) ou math.hypot
            try:
                distancia = math.dist(player.rect.center, inimigo.rect.center)
            except AttributeError: # Fallback para versões anteriores ao Python 3.8
                 distancia = math.hypot(player.rect.centerx - inimigo.rect.centerx, player.rect.centery - inimigo.rect.centery)


            # Verifica se o inimigo está dentro do alcance de ataque do jogador
            if distancia <= player.alcance_ataque:
                # Verifica se este inimigo é o mais próximo encontrado até agora
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    inimigo_mais_proximo = inimigo

    # Se encontrou um inimigo dentro do alcance, ataca
    if inimigo_mais_proximo:
        # Realiza o ataque no inimigo mais próximo
        dano_aplicado = player.dano

        # --- Lógica para aplicar dano ao inimigo ---
        # Assume-se que a classe do inimigo tem um método receber_dano()
        if hasattr(inimigo_mais_proximo, 'receber_dano'):
            inimigo_mais_proximo.receber_dano(dano_aplicado)
            # A lógica de 'derrotado' e 'kill()' está no método receber_dano ou derrotado do inimigo
            # print(f"Jogador atacou inimigo em {inimigo_mais_proximo.rect.center}. Dano: {dano_aplicado}. HP restante do inimigo: {inimigo_mais_proximo.hp if hasattr(inimigo_mais_proximo, 'hp') else 'N/A'}") # Mensagem de debug

            # ----------------------------------------

            # Atualiza o tempo do último ataque do jogador para aplicar o cooldown
            player.tempo_ultimo_ataque = agora

            # --- RETORNA INFORMAÇÕES PARA DESENHAR A ÁREA DE ATAQUE ---
            return (player.rect.centerx, player.rect.centery, player.alcance_ataque)
            # ------------------------------------------------------

        else:
            print(f"Erro: Inimigo {type(inimigo_mais_proximo)} não possui o método 'receber_dano'.")
            return None # Não atacou com sucesso, retorna None

    # Se nenhum inimigo foi encontrado dentro do alcance, não ataca
    return None

