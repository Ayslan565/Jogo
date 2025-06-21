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

# =====================================================================================
# --- NOVAS CONFIGURAÇÕES (EDITÁVEL PELO USUÁRIO) ---
# =====================================================================================
# >>> CAMINHOS PARA AS TEXTURAS DO CHÃO DA ARENA (UM PARA CADA ESTAÇÃO) <<<
# A ordem deve corresponder à ordem das estações: Primavera, Verão, Outono, Inverno.
CAMINHOS_TEXTURA_ARENA = [
    "Sprites\\Chao\\A1.png", # Primavera
    "Sprites\\Chao\\A2.png", # Verão
    "Sprites\\Chao\\A3.png", # Outono
    "Sprites\\Chao\\A4.png"  # Inverno
]

# >>> CAMINHOS PARA AS MÚSICAS DOS CHEFES <<<
# Adicione os caminhos das músicas que podem tocar durante as lutas.
MUSICAS_CHEFE_OPCOES = [
    "Musica\\Boss Fight\\Faixa1.mp3",
    "Musica\\Boss Fight\\Faixa2.mp3"
]
# =====================================================================================


# --- Variáveis de Estado do Módulo Luta_boss ---
_luta_ativa = False
_arena_rect = None
_chefe_atual = None
_musica_normal_anterior_pos = None
_musica_normal_anterior_path = None
_arena_chao_textura = None # Armazena a superfície da textura do chão
_cor_fallback_chao = (40, 35, 50) # Cor de fallback caso a textura não carregue
MUSICA_CHEFE_DEFAULT = [] # Será populada pela função de configuração


# --- Funções de Gerenciamento da Luta ---

def configurar_musicas_chefe(lista_musicas_chefe_projeto):
    """
    Configura a lista de músicas que podem ser tocadas durante as lutas contra chefes.
    Esta função deve ser chamada uma vez no início do jogo.

    Args:
        lista_musicas_chefe_projeto (list): Uma lista de caminhos para arquivos de música.
    """
    global MUSICA_CHEFE_DEFAULT
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
    global _luta_ativa, _arena_rect, _chefe_atual, _musica_normal_anterior_pos, _musica_normal_anterior_path, _arena_chao_textura
    
    if not (jogador and hasattr(jogador, 'rect') and hasattr(jogador, 'x') and hasattr(jogador, 'y')):
        print("ERRO (Luta_boss.py): Objeto do jogador inválido para iniciar a luta.")
        return False

    _luta_ativa = True
    gerenciador_inimigos.limpar_todos_inimigos_normais()

    # Cria a arena de batalha e carrega seus recursos visuais
    arena_x = jogador.x - DIMENSOES_ARENA_CHEFE[0] // 2
    arena_y = jogador.y - DIMENSOES_ARENA_CHEFE[1] // 2
    _arena_rect = pygame.Rect(arena_x, arena_y, DIMENSOES_ARENA_CHEFE[0], DIMENSOES_ARENA_CHEFE[1])
    
    # --- LÓGICA CORRIGIDA PARA SELECIONAR TEXTURA DA ARENA ---
    try:
        # Seleciona o caminho da textura com base no índice da estação
        if 0 <= indice_estacao < len(CAMINHOS_TEXTURA_ARENA):
            caminho_textura_selecionada = CAMINHOS_TEXTURA_ARENA[indice_estacao]
            textura_original = pygame.image.load(caminho_textura_selecionada).convert()
            _arena_chao_textura = pygame.transform.scale(textura_original, DIMENSOES_ARENA_CHEFE)
            print(f"DEBUG(Luta_boss.py): Textura da arena '{caminho_textura_selecionada}' carregada com sucesso.")
        else:
            raise IndexError(f"Índice da estação ({indice_estacao}) está fora do alcance da lista de texturas.")
    except Exception as e:
        print(f"AVISO(Luta_boss.py): Falha ao carregar a textura da arena: {e}. Usando cor sólida de fallback.")
        _arena_chao_textura = None

    # Spawna o chefe
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
        time.sleep(1) # Pausa para a transição musical

    if MUSICA_CHEFE_DEFAULT:
        selected_track = random.choice(MUSICA_CHEFE_DEFAULT)
        try:
            pygame.mixer.music.load(selected_track)
            pygame.mixer.music.play(-1, fade_ms=1000)
        except pygame.error as e:
            print(f"ERRO (Luta_boss.py): ao carregar/tocar música do chefe '{selected_track}': {e}")
    
    gerenciador_inimigos.pausar_spawn_normal(True)
    print(f"Luta contra o chefe '{type(_chefe_atual).__name__}' iniciada!")
    return True


def finalizar_luta_chefe(jogador, estacoes_obj, gerenciador_inimigos):
    """
    Finaliza a luta contra o chefe, restaura a música normal, concede XP,
    e sinaliza para o jogo avançar para a próxima estação.
    """
    global _luta_ativa, _arena_rect, _chefe_atual, _musica_normal_anterior_pos, _musica_normal_anterior_path, _arena_chao_textura

    print(f"DEBUG(Luta_boss.py): Finalizando luta contra o chefe '{type(_chefe_atual).__name__ if _chefe_atual else 'Desconhecido'}'.")
    _luta_ativa = False
    _arena_rect = None
    _arena_chao_textura = None # Libera a textura da memória
    
    if _chefe_atual and hasattr(jogador, 'xp_manager') and hasattr(_chefe_atual, 'xp_value_boss'):
        xp_do_chefe = getattr(_chefe_atual, 'xp_value_boss', 100)
        if hasattr(jogador.xp_manager, 'gain_xp'):
            jogador.xp_manager.gain_xp(xp_do_chefe)
            print(f"Jogador ganhou {xp_do_chefe} XP pela vitória contra o chefe!")
    
    _chefe_atual = None 
    
    if pygame.mixer.get_init():
        pygame.mixer.music.fadeout(1500)
        if _musica_normal_anterior_path and os.path.exists(_musica_normal_anterior_path):
            try:
                time.sleep(1.5)
                pygame.mixer.music.load(_musica_normal_anterior_path)
                start_pos_sec = _musica_normal_anterior_pos / 1000.0 if _musica_normal_anterior_pos else 0
                pygame.mixer.music.play(-1, start=start_pos_sec, fade_ms=1000)
            except pygame.error as e:
                print(f"ERRO (Luta_boss.py): ao restaurar música normal: {e}")

    _musica_normal_anterior_path = None
    _musica_normal_anterior_pos = None

    if hasattr(estacoes_obj, 'avancar_estacao_apos_chefe'): 
        estacoes_obj.avancar_estacao_apos_chefe()
    else:
        print("AVISO (Luta_boss.py): Objeto de estações não possui o método 'avancar_estacao_apos_chefe'.")

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
        if jogador.rect.left < _arena_rect.left: jogador.rect.left = _arena_rect.left
        if jogador.rect.right > _arena_rect.right: jogador.rect.right = _arena_rect.right
        if jogador.rect.top < _arena_rect.top: jogador.rect.top = _arena_rect.top
        if jogador.rect.bottom > _arena_rect.bottom: jogador.rect.bottom = _arena_rect.bottom
        if hasattr(jogador, 'x') and hasattr(jogador, 'y'):
            jogador.x = float(jogador.rect.centerx)
            jogador.y = float(jogador.rect.centery)

    # Verifica se o chefe foi derrotado
    if _chefe_atual:
        if hasattr(_chefe_atual, 'esta_vivo') and not _chefe_atual.esta_vivo():
            finalizar_luta_chefe(jogador, estacoes_obj, gerenciador_inimigos)
            return True # Retorna True indicando que a luta acabou de terminar
    elif _luta_ativa: 
        print("AVISO CRÍTICO (Luta_boss.py): Luta ativa mas _chefe_atual é None. Finalizando luta.")
        finalizar_luta_chefe(jogador, estacoes_obj, gerenciador_inimigos)
        return True

    return False

# --- NOVA FUNÇÃO DE DESENHO ---
def desenhar_efeitos_arena(surface, camera_x, camera_y):
    """
    Desenha o chão da arena e o efeito de "blackout" ao redor.
    Esta função deve ser chamada no loop de desenho principal (Game.py) ANTES de desenhar
    os sprites do mundo, mas DEPOIS do fundo normal das estações.
    """
    if not _luta_ativa or not _arena_rect:
        return

    tela_largura, tela_altura = surface.get_size()
    arena_pos_tela_x = _arena_rect.x - camera_x
    arena_pos_tela_y = _arena_rect.y - camera_y

    # 1. Desenha o chão da arena por cima do chão normal do jogo
    if _arena_chao_textura:
        surface.blit(_arena_chao_textura, (arena_pos_tela_x, arena_pos_tela_y))
    else:
        pygame.draw.rect(surface, _cor_fallback_chao, (arena_pos_tela_x, arena_pos_tela_y, _arena_rect.width, _arena_rect.height))

    # 2. Desenha o "blackout" ao redor da arena
    cor_preta = (0, 0, 0)
    # Retângulo acima da arena
    pygame.draw.rect(surface, cor_preta, (0, 0, tela_largura, arena_pos_tela_y))
    # Retângulo abaixo da arena
    pygame.draw.rect(surface, cor_preta, (0, arena_pos_tela_y + _arena_rect.height, tela_largura, tela_altura - (arena_pos_tela_y + _arena_rect.height)))
    # Retângulo à esquerda da arena
    pygame.draw.rect(surface, cor_preta, (0, arena_pos_tela_y, arena_pos_tela_x, _arena_rect.height))
    # Retângulo à direita da arena
    pygame.draw.rect(surface, cor_preta, (arena_pos_tela_x + _arena_rect.width, arena_pos_tela_y, tela_largura - (arena_pos_tela_x + _arena_rect.width), _arena_rect.height))


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
