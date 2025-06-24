# main.py ou game.py (Nome do seu arquivo principal)
import pygame
import time
import sys # Importa sys para sair corretamente

# Inicializa todos os módulos do Pygame
# É uma boa prática inicializar apenas uma vez no início do script principal
pygame.init()

# Define o tamanho da tela
largura, altura = 1920, 1080
screen = pygame.display.set_mode((largura, altura))

# Define o título da janela
pygame.display.set_caption("Seu Jogo") # Altere para o nome do seu jogo

# Define a cor de fundo padrão (pode ser usada se a imagem de fundo não carregar)
PRETO = (0, 0, 0)

def main():
    """
    Função principal do jogo, incluindo a tela de splash.
    """
    # --- Tela de Splash ---
    splash_image_path = r"C:\Users\aysla\Documents\Jogo_Asrahel\Jogo\Sprites\Asrahel\Asrahel2.png" # Use raw string para evitar problemas com backslashes

    try:
        # Carrega a imagem da tela de splash
        splash = pygame.image.load(splash_image_path).convert() # Use convert() para otimizar
        # Redimensiona a imagem para o tamanho da tela
        splash = pygame.transform.scale(splash, (largura, altura))

        # Desenha a imagem na tela
        screen.blit(splash, (0, 0))
        # Atualiza a tela para mostrar a imagem
        pygame.display.flip()

        # Espera por 3 segundos (ajuste conforme necessário)
        time.sleep(3)

    except pygame.error as e:
        print(f"Erro ao carregar a imagem da tela de splash: {splash_image_path}")
        print(f"Detalhes do erro: {e}")
        # Se a imagem não carregar, preenche a tela com preto e exibe uma mensagem de erro
        screen.fill(PRETO)
        fonte_erro = pygame.font.Font(None, 50)
        texto_erro = fonte_erro.render("Erro ao carregar tela de splash", True, (255, 0, 0)) # Texto vermelho para erro
        screen.blit(texto_erro, (largura // 2 - texto_erro.get_width() // 2, altura // 2 - texto_erro.get_height() // 2))
        pygame.display.flip()
        time.sleep(3) # Espera um pouco antes de continuar


    # --- Após a Tela de Splash (Exemplo: Loop básico para manter a janela aberta) ---
    # Aqui você normalmente chamaria sua função de menu principal ou iniciaria o loop do jogo
    print("Tela de splash exibida. Continuando para o menu/jogo...")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Adicione outros eventos aqui (por exemplo, cliques do mouse para o menu)

        # Exemplo: Desenhar algo simples após a splash (opcional)
        # screen.fill(PRETO) # Limpa a tela (se não quiser o fundo da splash)
        # pygame.display.flip()

        # Não há necessidade de controlar o FPS neste loop simples, mas seria necessário em um jogo real
        # clock.tick(60) # Se você tivesse um objeto clock definido

    # --- Fim do Jogo ---
    pygame.quit() # Finaliza o Pygame
    sys.exit() # Sai do script

# Executa a função principal se o script for executado diretamente
if __name__ == "__main__":
    main()
