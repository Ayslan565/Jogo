# Jogo/Arquivos/Luta_boss.py

import pygame
import random
import sys
import os
import traceback
import math
import time

# --- Configuração do sys.path ---
# Garante que os módulos do projeto possam ser encontrados
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
project_root_dir = os.path.dirname(current_dir)
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

# --- Importações Essenciais ---
# Importações mínimas para evitar dependência circular e sobrecarga.
# As instâncias necessárias (jogador, gerenciador, etc.) são passadas como argumentos.
try:
    # Apenas para tipos, se necessário. Evitar importações de classes de jogo completas.
    from importacoes import Player, GerenciadorDeInimigos, Estacoes
except ImportError as e:
    print(f"AVISO (Luta_boss.py): Falha ao importar anotações de tipo: {e}")
    # Define classes placeholder para anotação de tipo se a importação falhar
    class Player: pass
    class GerenciadorDeInimigos: pass
    class Estacoes: pass


# --- Configurações do Módulo Luta_boss ---
DIMENSOES_ARENA_CHEFE = (1000, 700) # Arena um pouco maior
MUSICA_CHEFE_DEFAULT = []

# --- Variáveis de Estado do Módulo Luta_boss ---
_luta_ativa = False
_arena_rect = None
_chefe_atual = None
_musica_normal_anterior_pos = None
_musica_normal_anterior_path = None

# --- Funções de Gerenciamento da Luta ---

def configurar_musicas_chefe(lista_musicas_chefe_projeto):
    """
    Configura a lista de músicas que podem ser tocadas durante as lutas contra chefes.
    Esta função deve ser chamada uma vez no início do jogo.

    Args:
        lista_musicas_chefe_projeto (list): Uma lista de caminhos para arquivos de música.
    """
    global MUSICA_CHEFE_DEFAULT
    # Garante que a lista contenha apenas caminhos válidos
    if isinstance(lista_musicas_chefe_projeto, list):
        MUSICA_CHEFE_DEFAULT = [path for path in lista_musicas_chefe_projeto if isinstance(path, str) and os.path.exists(path)]
        if not MUSICA_CHEFE_DEFAULT:
            print("AVISO (Luta_boss.py): Nenhuma música de chefe válida foi encontrada nos caminhos fornecidos.")
    else:
        print("ERRO (Luta_boss.py): 'lista_musicas_chefe_projeto' deve ser uma lista.")
        MUSICA_CHEFE_DEFAULT = []


def iniciar_luta_chefe(jogador, indice_estacao, gerenciador_inimigos, estacoes_obj, musica_atual_path=None, musica_atual_pos_ms=None):
    """
    Inicia a sequência de luta contra o chefe. Limpa inimigos normais, define a arena,
    spawna o chefe, troca a música e pausa o spawn normal.
    """
    global _luta_ativa, _arena_rect, _chefe_atual, _musica_normal_anterior_pos, _musica_normal_anterior_path
    
    if not (jogador and hasattr(jogador, 'rect') and hasattr(jogador, 'x') and hasattr(jogador, 'y')):
        print("ERRO (Luta_boss.py): Objeto do jogador inválido para iniciar a luta.")
        return False

    _luta_ativa = True

    # Limpa os inimigos normais existentes
    gerenciador_inimigos.limpar_todos_inimigos_normais()

    # Cria a arena de batalha centralizada no jogador
    arena_x = jogador.x - DIMENSOES_ARENA_CHEFE[0] // 2
    arena_y = jogador.y - DIMENSOES_ARENA_CHEFE[1] // 2
    _arena_rect = pygame.Rect(arena_x, arena_y, DIMENSOES_ARENA_CHEFE[0], DIMENSOES_ARENA_CHEFE[1])

    # Spawna o chefe específico da estação
    posicao_spawn_chefe = _arena_rect.center
    chefe_spawnado = gerenciador_inimigos.spawn_chefe_estacao(indice_estacao, posicao_spawn_chefe)
    
    if not chefe_spawnado:
        print(f"ERRO CRÍTICO (Luta_boss.py): Falha ao spawnar o chefe para a estação de índice {indice_estacao}.")
        _luta_ativa = False
        _arena_rect = None
        return False
    
    set_chefe_atual_para_monitoramento(chefe_spawnado)

    # Gerenciamento da música
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        _musica_normal_anterior_pos = musica_atual_pos_ms if musica_atual_pos_ms is not None else pygame.mixer.music.get_pos()
        _musica_normal_anterior_path = musica_atual_path
        pygame.mixer.music.fadeout(1000)

    time.sleep(1) # Pequena pausa para a transição musical

    if MUSICA_CHEFE_DEFAULT:
        selected_track = random.choice(MUSICA_CHEFE_DEFAULT)
        try:
            pygame.mixer.music.load(selected_track)
            pygame.mixer.music.play(-1, fade_ms=1000)
        except pygame.error as e:
            print(f"ERRO (Luta_boss.py): ao carregar/tocar música do chefe '{selected_track}': {e}")
    
    # Pausa o spawn de inimigos normais
    gerenciador_inimigos.pausar_spawn_normal(True)
    
    print(f"Luta contra o chefe '{type(_chefe_atual).__name__}' iniciada!")
    return True


def finalizar_luta_chefe(jogador, estacoes_obj, gerenciador_inimigos):
    """
    Finaliza a luta contra o chefe, restaura a música normal, concede XP,
    e sinaliza para o jogo avançar para a próxima estação.
    """
    global _luta_ativa, _arena_rect, _chefe_atual, _musica_normal_anterior_pos, _musica_normal_anterior_path

    print(f"DEBUG(Luta_boss.py): Finalizando luta contra o chefe '{type(_chefe_atual).__name__ if _chefe_atual else 'Desconhecido'}'.")
    _luta_ativa = False
    _arena_rect = None
    
    # Concede XP de chefe ao jogador
    if _chefe_atual and hasattr(jogador, 'xp_manager') and hasattr(_chefe_atual, 'xp_value_boss'):
        xp_do_chefe = getattr(_chefe_atual, 'xp_value_boss', 100) # Valor padrão de 100
        if hasattr(jogador.xp_manager, 'gain_xp'):
            jogador.xp_manager.gain_xp(xp_do_chefe)
            print(f"Jogador ganhou {xp_do_chefe} XP pela vitória contra o chefe!")
    
    _chefe_atual = None 
    
    # Restaura a música de fundo anterior
    if pygame.mixer.get_init():
        pygame.mixer.music.fadeout(1500)
        if _musica_normal_anterior_path and os.path.exists(_musica_normal_anterior_path):
            try:
                # Espera o fadeout terminar antes de carregar a nova música
                time.sleep(1.5)
                pygame.mixer.music.load(_musica_normal_anterior_path)
                start_pos_sec = _musica_normal_anterior_pos / 1000.0 if _musica_normal_anterior_pos else 0
                pygame.mixer.music.play(-1, start=start_pos_sec, fade_ms=1000)
            except pygame.error as e:
                print(f"ERRO (Luta_boss.py): ao restaurar música normal: {e}")

    _musica_normal_anterior_path = None
    _musica_normal_anterior_pos = None

    # Permite que o jogo prossiga para a próxima estação
    if hasattr(estacoes_obj, 'avancar_estacao_apos_chefe'): 
        estacoes_obj.avancar_estacao_apos_chefe()
    else:
        print("AVISO (Luta_boss.py): Objeto de estações não possui o método 'avancar_estacao_apos_chefe'.")

    # Reativa o spawn de inimigos e reseta os temporizadores
    gerenciador_inimigos.pausar_spawn_normal(False)
    gerenciador_inimigos.resetar_temporizador_spawn_estacao()
    gerenciador_inimigos.spawn_inimigos_iniciais(jogador)


def atualizar_luta(jogador, estacoes_obj, gerenciador_inimigos):
    """
    Chamada a cada frame para monitorar a condição de derrota do chefe e prender o jogador na arena.
    """
    global _chefe_atual 
    if not _luta_ativa:
        return False 

    # Mantém o jogador dentro da arena
    if _arena_rect and hasattr(jogador, 'rect'):
        # jogador.rect.clamp_ip(_arena_rect) # clamp_ip modifica o rect original
        
        # Lógica de clamp manual para atualizar as coordenadas x e y do jogador
        if jogador.rect.left < _arena_rect.left:
            jogador.rect.left = _arena_rect.left
        if jogador.rect.right > _arena_rect.right:
            jogador.rect.right = _arena_rect.right
        if jogador.rect.top < _arena_rect.top:
            jogador.rect.top = _arena_rect.top
        if jogador.rect.bottom > _arena_rect.bottom:
            jogador.rect.bottom = _arena_rect.bottom

        # Atualiza as coordenadas float do jogador para corresponder ao rect
        if hasattr(jogador, 'x') and hasattr(jogador, 'y'):
            jogador.x = float(jogador.rect.centerx)
            jogador.y = float(jogador.rect.centery)


    # Verifica se o chefe foi derrotado
    chefe_derrotado_agora = False
    if _chefe_atual:
        # A forma mais confiável é checar o método 'esta_vivo()' do próprio chefe.
        if hasattr(_chefe_atual, 'esta_vivo') and not _chefe_atual.esta_vivo():
            finalizar_luta_chefe(jogador, estacoes_obj, gerenciador_inimigos)
            chefe_derrotado_agora = True 
    elif _luta_ativa: 
        # Caso de segurança: se a luta está ativa, mas a referência ao chefe foi perdida.
        print("AVISO CRÍTICO (Luta_boss.py): Luta ativa mas _chefe_atual é None. Finalizando luta.")
        finalizar_luta_chefe(jogador, estacoes_obj, gerenciador_inimigos)
        chefe_derrotado_agora = True 

    return chefe_derrotado_agora

# --- Funções de Acesso (Getters/Setters) ---

def esta_luta_ativa():
    """Retorna o estado atual da luta contra o chefe."""
    return _luta_ativa

def get_arena_rect():
    """Retorna o retângulo da arena de batalha."""
    return _arena_rect

def get_chefe_atual():
    """Retorna a instância do chefe atual."""
    return _chefe_atual

def set_chefe_atual_para_monitoramento(instancia_chefe):
    """Define a instância do chefe a ser monitorada. Usado internamente."""
    global _chefe_atual
    _chefe_atual = instancia_chefe
