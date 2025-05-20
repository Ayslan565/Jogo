# telas.py
# Responsável por gerenciar telas específicas do jogo, como a tela de morte

import pygame
import sys

# Importa configurações
try:
    import config # Importa o arquivo de configuração
except ImportError:
    print("AVISO(Telas): Módulo 'config.py' não encontrado.")
    config = None # Define como None para evitar NameError


def tela_de_morte(janela):
    """
    Exibe a tela de morte e espera pela ação do jogador (reiniciar ou sair).

    Args:
        janela (pygame.Surface): A superfície onde desenhar a tela de morte.

    Returns:
        str: 'reiniciar' si o jogador pressionar R, 'sair' si pressionar ESC ou fechar a janela.
    """
    if janela is None:
        # print("DEBUG(Telas): Aviso: Objeto janela é None. Não foi possível exibir a tela de morte.") # Debug removido
        return 'sair' # Retorna 'sair' si a janela não for válida

    # Define a fonte para a mensagem de morte
    # Verifica se pygame.font está inicializado antes de usar
    if pygame.font.get_init():
         fonte = pygame.font.SysFont(None, 75) # Ajuste o tamanho da fonte si necessário
    else:
         # print("AVISO(Telas): Pygame.font não inicializado. Não foi possível criar a fonte para a tela de morte.") # Debug removido
         fonte = None # Define como None si a fonte não puder ser criada


    # Renderiza o texto da mensagem de morte
    if fonte: # Verifica si a fonte foi criada com sucesso
        texto = fonte.render("Você morreu! Pressione R para reiniciar ou ESC para sair.", True, (255, 0, 0)) # Cor vermelha (ajuste)
        # Calcula a posição para centralizar o texto
        texto_rect = texto.get_rect(center=(janela.get_width() // 2, janela.get_height() // 2))
    else:
        texto = None # Define como None si o texto não puder ser renderizado
        # print("AVISO(Telas): Texto da tela de morte não pôde ser renderizado.") # Debug removido


    janela.fill((0, 0, 0)) # Preenche a tela com preto (ajuste a cor si desejar)

    # Desenha o texto si ele foi renderizado com sucesso
    if texto:
        janela.blit(texto, texto_rect)

    pygame.display.update() # Atualiza a tela para mostrar a mensagem de morte

    esperando_input = True
    while esperando_input:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 'sair' # Retorna 'sair' si a janela for fechada
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return 'sair' # Retorna 'sair' si ESC for pressionado
                if e.key == pygame.K_r:
                    return 'reiniciar' # Retorna 'reiniciar' si R for pressionado

        # Pequena pausa para não consumir 100% da CPU enquanto espera input
        pygame.time.wait(50) # Espera 50 milissegundos

# Outras funções para telas de menu, opções, etc. podem ser adicionadas aqui.
