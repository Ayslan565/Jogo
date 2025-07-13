import pygame
import sys
import time

# --- Configurações Iniciais ---
pygame.init()

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
BRANCO_OPACO = (255, 255, 255, 255) # Usado para a máscara

# --- Parâmetros de Design ---
FATOR_REDUCAO_IMG2 = 0.5
RAIO_CANTO = 0

# --- Configurações do Texto "APOIO" ---
FONTE_APOIO = pygame.font.Font(None, 60) # None usa a fonte padrão, 48 é o tamanho
COR_APOIO = BRANCO
MARGEM_ACIMA_IMG2 = 20 # Espaço entre o texto e a imagem

# --- Criar a Janela em Modo Tela Cheia ---
try:
    tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Apresentação do Jogo")
except pygame.error as e:
    print(f"Não foi possível iniciar em modo tela cheia: {e}")
    tela = pygame.display.set_mode((800, 600))

# --- Carregar Imagens ---
try:
    img_studio_original = pygame.image.load("Sprites\\inicio\\1.png").convert_alpha()
    img_universidade_original = pygame.image.load("Sprites\\inicio\\2.png").convert_alpha()
except pygame.error as e:
    print(f"Erro ao carregar uma das imagens: {e}")
    print("Verifique se a pasta 'Sprites\\inicio' com os arquivos '1.png' e '2.png' existe.")
    pygame.quit()
    sys.exit()

# --- Funções Auxiliares ---

def arredondar_cantos(imagem, raio):
    """Aplica cantos arredondados a uma superfície/imagem do Pygame."""
    if raio == 0:
        return imagem
    imagem_arredondada = imagem.copy().convert_alpha()
    rect = imagem_arredondada.get_rect()
    mascara_cantos = pygame.Surface(rect.size, pygame.SRCALPHA)
    mascara_cantos.fill((0, 0, 0, 0))
    pygame.draw.rect(mascara_cantos, BRANCO_OPACO, (raio, 0, rect.width - 2 * raio, rect.height))
    pygame.draw.rect(mascara_cantos, BRANCO_OPACO, (0, raio, rect.width, rect.height - 2 * raio))
    pygame.draw.circle(mascara_cantos, BRANCO_OPACO, (raio, raio), raio)
    pygame.draw.circle(mascara_cantos, BRANCO_OPACO, (rect.right - raio, raio), raio)
    pygame.draw.circle(mascara_cantos, BRANCO_OPACO, (raio, rect.bottom - raio), raio)
    pygame.draw.circle(mascara_cantos, BRANCO_OPACO, (rect.right - raio, rect.bottom - raio), raio)
    imagem_arredondada.blit(mascara_cantos, (0, 0), None, pygame.BLEND_RGBA_MIN)
    return imagem_arredondada

def preparar_imagem(imagem_original, tela_surface):
    """Redimensiona a imagem (mantendo proporção) e a centraliza."""
    tela_rect = tela_surface.get_rect()
    img_rect = imagem_original.get_rect()
    if img_rect.width > tela_rect.width or img_rect.height > tela_rect.height:
        ratio = min(tela_rect.width / img_rect.width, tela_rect.height / img_rect.height)
        novo_tamanho = (int(img_rect.width * ratio), int(img_rect.height * ratio))
        imagem_final = pygame.transform.smoothscale(imagem_original, novo_tamanho)
    else:
        imagem_final = imagem_original
    rect_final = imagem_final.get_rect()
    rect_final.center = tela_rect.center
    return imagem_final, rect_final

# Prepara a primeira imagem
img_studio, rect_studio = preparar_imagem(img_studio_original, tela)

# --- Prepara a segunda imagem e o texto ---
largura_original_uni, altura_original_uni = img_universidade_original.get_size()
nova_largura_uni = int(largura_original_uni * FATOR_REDUCAO_IMG2)
nova_altura_uni = int(altura_original_uni * FATOR_REDUCAO_IMG2)
img_universidade_reduzida = pygame.transform.smoothscale(img_universidade_original, (nova_largura_uni, nova_altura_uni))
img_universidade_arredondada = arredondar_cantos(img_universidade_reduzida, RAIO_CANTO)
img_universidade, rect_universidade = preparar_imagem(img_universidade_arredondada, tela)

# Renderiza o texto "APOIO" e posiciona-o
texto_apoio_surface = FONTE_APOIO.render("APOIO", True, COR_APOIO).convert_alpha()
texto_apoio_rect = texto_apoio_surface.get_rect()
texto_apoio_rect.midbottom = rect_universidade.midtop
texto_apoio_rect.y -= MARGEM_ACIMA_IMG2

# --- Funções de Animação Atualizadas ---

def fade_out(imagem, rect, duracao_ms, texto_surface=None, texto_rect=None):
    """Faz uma imagem e um texto opcional desaparecerem gradualmente."""
    clock = pygame.time.Clock()
    velocidade_fade = 255 / (duracao_ms / 1000 * 60)
    for alpha in range(255, -1, -int(velocidade_fade)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        tela.fill(PRETO)
        # Anima a imagem
        imagem.set_alpha(max(alpha, 0))
        tela.blit(imagem, rect)
        
        # Anima o texto, se ele existir
        if texto_surface:
            texto_surface.set_alpha(max(alpha, 0))
            tela.blit(texto_surface, texto_rect)

        pygame.display.flip()
        clock.tick(60)

def fade_in(imagem, rect, duracao_ms, texto_surface=None, texto_rect=None):
    """Faz uma imagem e um texto opcional aparecerem gradualmente."""
    clock = pygame.time.Clock()
    velocidade_fade = 255 / (duracao_ms / 1000 * 60)
    for alpha in range(0, 256, int(velocidade_fade)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        tela.fill(PRETO)
        # Anima a imagem
        imagem.set_alpha(min(alpha, 255))
        tela.blit(imagem, rect)

        # Anima o texto, se ele existir
        if texto_surface:
            texto_surface.set_alpha(min(alpha, 255))
            tela.blit(texto_surface, texto_rect)

        pygame.display.flip()
        clock.tick(60)

# --- Sequência da Apresentação ---
def executar_apresentacao():
    clock = pygame.time.Clock()

    # 1. Fazer a imagem do estúdio aparecer (Fade In)
    fade_in(img_studio, rect_studio, duracao_ms=2000)

    # 2. Manter a imagem do estúdio na tela
    tempo_inicial = time.time()
    while time.time() - tempo_inicial < 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
        clock.tick(30)

    # 3. Esmaecer a imagem do estúdio (Fade Out)
    fade_out(img_studio, rect_studio, duracao_ms=2000)

    # Pausa entre as imagens
    time.sleep(0.5)

    # 4. Fazer a imagem da universidade e o texto "APOIO" aparecerem juntos
    fade_in(img_universidade, rect_universidade, duracao_ms=2000, 
            texto_surface=texto_apoio_surface, texto_rect=texto_apoio_rect)

    # 5. Manter a imagem e o texto na tela
    tempo_inicial = time.time()
    while time.time() - tempo_inicial < 4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
        clock.tick(30)

    # (Opcional) Fade-out final para a segunda cena
    fade_out(img_universidade, rect_universidade, duracao_ms=2000,
             texto_surface=texto_apoio_surface, texto_rect=texto_apoio_rect)


# Executa a apresentação e depois fecha o programa
try:
    executar_apresentacao()
finally:
    pygame.quit()
    sys.exit()