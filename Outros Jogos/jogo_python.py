import os
import pygame
import random

# Inicia, configura e cria a tela, relógio 
os.system("cls")
pygame.init()

# Configurações da tela
pygame.display.set_caption("Jogo da python")
largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Cores
preto = (0, 0, 0)
branco = (255, 255, 255)    
verde = (35, 142, 35)
rosa = (204, 50, 153)
azul = (0, 0, 255)
cinza = (150, 150, 150)

tamanho_quadrado = 20
velocidade_atualizacao = 10

# Inicializa o mixer do pygame e carrega a música
pygame.mixer.init()
pygame.mixer.music.load(r"C:\Users\aysla\Documents\Projetos\Projetos em Python\musica.mp3")  # Use raw string (r) para evitar problemas com barras
pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop

# Comida Gerada Aleatoriamente
def comida_aleatoria():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / tamanho_quadrado) * tamanho_quadrado
    return comida_x, comida_y

# Desenho comida
def desenho_comida(comida_x, comida_y):
    pygame.draw.rect(tela, rosa, [comida_x, comida_y, tamanho_quadrado, tamanho_quadrado])

# Desenho python
def desenho_python(tamanho_quadrado, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, preto, [pixel[0], pixel[1], tamanho_quadrado, tamanho_quadrado])

# Texto
def desenho_pontuação(pontos):
    fonte = pygame.font.SysFont('arial', 35)
    texto = fonte.render(f"Pontos: {pontos}", True, branco)
    tela.blit(texto, [25, 25])

# Velocidade
def selecionar_velocidade(tecla):
    
    if tecla == pygame.K_DOWN:
        velocidade_x = 0
        velocidade_y = tamanho_quadrado

    elif tecla == pygame.K_UP:
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado

    elif tecla == pygame.K_RIGHT:
        velocidade_x = tamanho_quadrado
        velocidade_y = 0

    elif tecla == pygame.K_LEFT:
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0

    else:
        velocidade_x = 0
        velocidade_y = 0


    return velocidade_x, velocidade_y

# Jogo
def rodar_jogo():
    finalizado = False
    x = largura / 2
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0
    
    tamanho_python = 1
    pixels = []

    comida_x, comida_y = comida_aleatoria()

    while not finalizado:
        tela.fill(verde)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                finalizado = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)

        # Atualiza a posição da cobra
        x += velocidade_x
        y += velocidade_y

        # Verifica colisão com as bordas
        if x >= largura or x < 0 or y >= altura or y < 0:
            finalizado = True

        # Desenho comida
        desenho_comida(comida_x, comida_y)

        # Desenho python (Movimento)
        pixels.append([x, y])  # Adiciona a nova posição da cabeça da cobra

        # Se a cobra não comeu a comida, remove o último pixel
        if len(pixels) > tamanho_python:
            del pixels[0]

        # Se ela bater em si mesma
        for pixel in pixels[:-1]: 
            if pixel == [x, y]:
                finalizado = True

        desenho_python(tamanho_quadrado, pixels)
        desenho_pontuação(tamanho_python - 1)
        
        pygame.display.update()

        # Cria uma nova comida
        if x == comida_x and y == comida_y:
            tamanho_python += 1  # Aumenta o tamanho da cobra
            comida_x, comida_y = comida_aleatoria()  # Gera uma nova comida

        relogio.tick(velocidade_atualizacao)

    # Para a música quando o jogo terminar
    pygame.mixer.music.stop()

rodar_jogo()
pygame.quit()