# config.py
# Arquivo para armazenar constantes de configuração do jogo

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Tamanho dos blocos para geração de mundo
BLOCK_SIZE = 1080

# Distância mínima e máxima para spawn de inimigos e plantas a partir do jogador
SPAWN_DISTANCE_MIN = 300
SPAWN_DISTANCE_MAX = 600

# Limite máximo de inimigos na tela
MAX_ENEMIES = 1500

# Configurações de spawn exponencial de inimigos
SPAWN_INTERVAL_INITIAL = 3.0 # Tempo inicial em segundos entre spawns periódicos
EXPONENTIAL_SPAWN_FACTOR = 0.02 # Controla a rapidez com que o intervalo de spawn diminui
MIN_SPAWN_INTERVAL = 0.5 # O menor intervalo de spawn permitido

# Quantidade de inimigos a spawnar inicialmente (ex: ao mudar de estação)
INITIAL_SPAWNS = 5

# Cores (exemplo)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Caminhos para sprites (exemplo - ajuste conforme sua estrutura de pastas)
# SPRITES_PLAYER = "Sprites/Player/"
# SPRITES_FANTASMA = "Sprites/Inimigos/Fantasma/"
# etc.

# Outras constantes podem ser adicionadas aqui conforme necessário
FPS = 60 # Quadros por segundo
