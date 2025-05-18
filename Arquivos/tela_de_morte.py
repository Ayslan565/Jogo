import pygame
import sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_r
import Game

def tela_de_morte(janela):
    """Exibe a tela de morte e espera pela interação do jogador."""
    fonte = pygame.font.Font(None, 45)
    texto = fonte.render("Você morreu! Pressione R para reiniciar ou ESC para sair.", True, (255, 0, 0))

    # Para a música do jogo ao entrar na tela de morte
    pygame.mixer.music.stop()
    print("Jogo: Música do jogo parada.")

    # Loop da tela de morte
    while True:
        for evento in pygame.event.get():
            # Si o evento for fechar a janela, sai do jogo
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Si a tecla ESC for pressionada, sai do jogo
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # Si a tecla R for pressionada, reinicia o jogo chamando main()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                Game.main()
                return # Sai da função tela_de_morte para voltar ao loop principal do jogo (reiniciado)

        # Preenche a tela com preto
        janela.fill((0, 0, 0))
        # Calcula a posição para centralizar o texto
        pos_x = janela.get_width() // 2 - texto.get_width() // 2
        pos_y = janela.get_height() // 2 - texto.get_height() // 2
        # Desenha o texto na janela
        janela.blit(texto, (pos_x, pos_y))
        # Atualiza a tela para mostrar as mudanças
        pygame.display.update()
        # Limita o framerate
        pygame.time.Clock().tick(60)