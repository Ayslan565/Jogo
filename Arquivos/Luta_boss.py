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
try:
    from importacoes import Player, GerenciadorDeInimigos, Estacoes
except ImportError as e:
    print(f"AVISO (Luta_boss.py): Falha ao importar anotações de tipo: {e}")
    class Player: pass
    class GerenciadorDeInimigos: pass
    class Estacoes: pass


# --- Configurações do Módulo Luta_boss ---
# =====================================================================================
# --- NOVAS CONFIGURAÇÕES (EDITÁVEL PELO USUÁRIO) ---
# =====================================================================================
CAMINHOS_TEXTURA_ARENA = [
    "Sprites\\Chao\\A1.png", # Primavera
    "Sprites\\Chao\\A2.png", # Verão
    "Sprites\\Chao\\A3.png", # Outono
    "Sprites\\Chao\\A4.png"  # Inverno
]
MUSICAS_CHEFE_OPCOES = [
    "Musica\Boss Fight\Faixa1.mp3", "Musica\\Boss Fight\\Faixa2.mp3",

]
# =====================================================================================


# --- Variáveis de Estado do Módulo Luta_boss ---
_luta_ativa = False
_arena_centro = (0, 0)
_arena_raio = 0
_chefe_atual = None
_jogador_em_luta = None
_velocidade_original_jogador = None # <<< NOVO: Para guardar a velocidade normal
_musica_normal_anterior_pos = None
_musica_normal_anterior_path = None
_arena_chao_textura = None
_cor_fallback_chao = (40, 35, 50)

_project_root_for_music = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSICA_CHEFE_DEFAULT = [
    os.path.join(_project_root_for_music, path.replace("\\", os.sep))
    for path in MUSICAS_CHEFE_OPCOES
    if os.path.exists(os.path.join(_project_root_for_music, path.replace("\\", os.sep)))
]
if not MUSICA_CHEFE_DEFAULT:
    print("AVISO (Luta_boss.py): Nenhuma música de chefe válida foi encontrada.")


# --- Funções de Gerenciamento da Luta ---

def iniciar_luta_chefe(jogador, indice_estacao, gerenciador_inimigos, estacoes_obj, largura_tela, altura_tela, musica_atual_path=None, musica_atual_pos_ms=None):
    """
    Inicia a luta contra o chefe com uma arena circular e bônus de velocidade para o jogador.
    """
    global _luta_ativa, _arena_centro, _arena_raio, _chefe_atual, _musica_normal_anterior_pos, _musica_normal_anterior_path, _arena_chao_textura, _jogador_em_luta, _velocidade_original_jogador
    
    if not (jogador and hasattr(jogador, 'rect')):
        print("ERRO (Luta_boss.py): Objeto do jogador inválido.")
        return False

    _luta_ativa = True
    _jogador_em_luta = jogador
    gerenciador_inimigos.limpar_todos_inimigos_normais()

    # --- NOVO: Aumenta a velocidade do jogador ---
    if hasattr(jogador, 'velocidade'):
        _velocidade_original_jogador = jogador.velocidade
        # >>> EDITE O VALOR 1.25 PARA MUDAR O BÔNUS (1.5 = 50% mais rápido) <<<
        jogador.velocidade *= 1.25 
        print(f"DEBUG(Luta_boss): Velocidade do jogador aumentada para {jogador.velocidade}")

    # --- LÓGICA DA ARENA CIRCULAR ---
    _arena_raio = min(largura_tela, altura_tela) * 0.45  # Diâmetro da arena = 90% da tela
    _arena_centro = (jogador.x, jogador.y)
    
    try:
        if 0 <= indice_estacao < len(CAMINHOS_TEXTURA_ARENA):
            caminho_textura = CAMINHOS_TEXTURA_ARENA[indice_estacao]
            textura_original = pygame.image.load(caminho_textura).convert()
            tamanho_textura = (_arena_raio * 2, _arena_raio * 2)
            _arena_chao_textura = pygame.transform.scale(textura_original, tamanho_textura)
        else:
            raise IndexError(f"Índice da estação ({indice_estacao}) inválido.")
    except Exception as e:
        print(f"AVISO(Luta_boss.py): Falha ao carregar textura da arena: {e}.")
        _arena_chao_textura = None

    # --- LÓGICA DE SPAWN DO CHEFE ---
    angulo_spawn = random.uniform(0, 2 * math.pi)
    distancia_spawn = _arena_raio * 0.75 
    spawn_x = _arena_centro[0] + distancia_spawn * math.cos(angulo_spawn)
    spawn_y = _arena_centro[1] + distancia_spawn * math.sin(angulo_spawn)
    
    dist_jogador = math.hypot(spawn_x - jogador.rect.centerx, spawn_y - jogador.rect.centery)
    if dist_jogador < 200:
        spawn_x = _arena_centro[0] - (spawn_x - _arena_centro[0])
        spawn_y = _arena_centro[1] - (spawn_y - _arena_centro[1])
        
    chefe_spawnado = gerenciador_inimigos.spawn_chefe_estacao(indice_estacao, (spawn_x, spawn_y))
    
    if not chefe_spawnado:
        print(f"ERRO CRÍTICO (Luta_boss.py): Falha ao spawnar o chefe.")
        _luta_ativa = False
        return False
    
    set_chefe_atual_para_monitoramento(chefe_spawnado)

    # Gerenciamento da música
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        _musica_normal_anterior_pos = musica_atual_pos_ms if musica_atual_pos_ms is not None else pygame.mixer.music.get_pos()
        _musica_normal_anterior_path = musica_atual_path
        pygame.mixer.music.fadeout(1000)
        time.sleep(1)

    if MUSICA_CHEFE_DEFAULT:
        try:
            selected_track = random.choice(MUSICA_CHEFE_DEFAULT)
            pygame.mixer.music.load(selected_track)
            pygame.mixer.music.play(-1, fade_ms=1000)
        except pygame.error as e:
            print(f"ERRO (Luta_boss.py): ao tocar música do chefe: {e}")
    
    gerenciador_inimigos.pausar_spawn_normal(True)
    print(f"Luta contra o chefe '{type(_chefe_atual).__name__}' iniciada!")
    return True


def finalizar_luta_chefe(jogador, estacoes_obj, gerenciador_inimigos):
    global _luta_ativa, _arena_centro, _arena_raio, _chefe_atual, _musica_normal_anterior_pos, _musica_normal_anterior_path, _arena_chao_textura, _jogador_em_luta, _velocidade_original_jogador

    # --- NOVO: Restaura a velocidade original do jogador ---
    if hasattr(jogador, 'velocidade') and _velocidade_original_jogador is not None:
        jogador.velocidade = _velocidade_original_jogador
        print(f"DEBUG(Luta_boss): Velocidade do jogador restaurada para {jogador.velocidade}")
        _velocidade_original_jogador = None

    _luta_ativa = False
    _jogador_em_luta = None
    _arena_centro = (0,0)
    _arena_raio = 0
    _arena_chao_textura = None 
    
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
        print("AVISO (Luta_boss.py): Objeto de estações não possui 'avancar_estacao_apos_chefe'.")

    gerenciador_inimigos.pausar_spawn_normal(False)
    gerenciador_inimigos.resetar_temporizador_spawn_estacao()
    gerenciador_inimigos.spawn_inimigos_iniciais(jogador)


def atualizar_luta(jogador, estacoes_obj, gerenciador_inimigos):
    global _chefe_atual 
    if not _luta_ativa:
        return False 

    for combatente in [_jogador_em_luta, _chefe_atual]:
        if combatente and hasattr(combatente, 'rect'):
            dist = math.hypot(combatente.rect.centerx - _arena_centro[0], combatente.rect.centery - _arena_centro[1])
            if dist > _arena_raio:
                angulo = math.atan2(combatente.rect.centery - _arena_centro[1], combatente.rect.centerx - _arena_centro[0])
                combatente.rect.centerx = _arena_centro[0] + _arena_raio * math.cos(angulo)
                combatente.rect.centery = _arena_centro[1] + _arena_raio * math.sin(angulo)
                if hasattr(combatente, 'x'):
                    combatente.x = float(combatente.rect.centerx)
                    combatente.y = float(combatente.rect.centery)

    if _chefe_atual:
        if hasattr(_chefe_atual, 'esta_vivo') and not _chefe_atual.esta_vivo():
            finalizar_luta_chefe(jogador, estacoes_obj, gerenciador_inimigos)
            return True
    elif _luta_ativa: 
        print("AVISO CRÍTICO (Luta_boss.py): Luta ativa mas _chefe_atual é None.")
        finalizar_luta_chefe(jogador, estacoes_obj, gerenciador_inimigos)
        return True

    return False

def desenhar_efeitos_arena(surface, camera_x, camera_y):
    global _jogador_em_luta, _chefe_atual

    if not _luta_ativa:
        return

    surface.fill((0, 0, 0))

    arena_surf = pygame.Surface((_arena_raio * 2, _arena_raio * 2), pygame.SRCALPHA)
    if _arena_chao_textura:
        pygame.draw.circle(arena_surf, (255, 255, 255), (_arena_raio, _arena_raio), _arena_raio)
        arena_surf.blit(_arena_chao_textura, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    else:
        pygame.draw.circle(arena_surf, _cor_fallback_chao, (_arena_raio, _arena_raio), _arena_raio)

    pos_chao_x = _arena_centro[0] - _arena_raio - camera_x
    pos_chao_y = _arena_centro[1] - _arena_raio - camera_y
    surface.blit(arena_surf, (pos_chao_x, pos_chao_y))
    
    sprites_na_arena = []
    if _jogador_em_luta: sprites_na_arena.append(_jogador_em_luta)
    if _chefe_atual: sprites_na_arena.append(_chefe_atual)
    
    sprites_na_arena.sort(key=lambda sprite: sprite.rect.bottom)

    for sprite in sprites_na_arena:
        if hasattr(sprite, 'desenhar'):
            sprite.desenhar(surface, camera_x, camera_y)


# --- Funções de Acesso (Getters/Setters) ---
def esta_luta_ativa():
    return _luta_ativa

def get_arena_raio_e_centro():
    return (_arena_raio, _arena_centro)

def get_chefe_atual():
    return _chefe_atual

def set_chefe_atual_para_monitoramento(instancia_chefe):
    global _chefe_atual
    _chefe_atual = instancia_chefe


def resetar_estado_luta_boss():
    global _luta_ativa, _arena_centro, _arena_raio, _chefe_atual, _musica_normal_anterior_pos, _musica_normal_anterior_path, _arena_chao_textura, _jogador_em_luta, _velocidade_original_jogador
    
    print("DEBUG(Luta_boss.py): Resetando estado da luta de chefe.")
    _luta_ativa = False
    _arena_centro = (0, 0)
    _arena_raio = 0
    _chefe_atual = None
    _jogador_em_luta = None
    _velocidade_original_jogador = None # <<< NOVO: Garante o reset
    _musica_normal_anterior_pos = None
    _musica_normal_anterior_path = None
    _arena_chao_textura = None
