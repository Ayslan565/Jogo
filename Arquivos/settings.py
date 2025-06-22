import os

# --- Configurações de Tela e Janela ---
TITULO_JOGO = "Lenda de Asrahel"
LARGURA_TELA = 1280  # Largura padrão se o modo tela cheia falhar
ALTURA_TELA = 720   # Altura padrão se o modo tela cheia falhar
FPS = 60            # Frames Por Segundo

# --- Configurações de Áudio ---
DEFAULT_MUSIC_VOLUME = 0.3
DEFAULT_SFX_VOLUME = 0.5

# --- Caminhos de Arquivos (Assets) ---
# Encontra o caminho raiz do projeto para garantir que os assets sempre sejam encontrados
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho para a imagem de tela de morte
DEATH_SCREEN_BACKGROUND_IMAGE = os.path.join(PROJECT_ROOT, "Sprites", "Backgrounds", "death_background.png")

# Lista de músicas para a jogabilidade
MUSICAS_JOGO = [
    os.path.join(PROJECT_ROOT, "Musica", "Gameplay", "Faixa 1.mp3"),
    os.path.join(PROJECT_ROOT, "Musica", "Gameplay", "Faixa 2.mp3"),
    os.path.join(PROJECT_ROOT, "Musica", "Gameplay", "Faixa 3.mp3"),
    os.path.join(PROJECT_ROOT, "Musica", "Gameplay", "Faixa 4.mp3"),
    os.path.join(PROJECT_ROOT, "Musica", "Gameplay", "Faixa 5.mp3"),
]

# --- Configurações de Gameplay (Exemplos) ---
# Você pode mover outras constantes para cá no futuro
# PLAYER_SPEED = 5
# PLAYER_INITIAL_HEALTH = 150