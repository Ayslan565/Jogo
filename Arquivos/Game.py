import pygame
import random
import time
from player import Player
from Estacoes import Estacoes
from GerenciadorDeInimigos import GerenciadorDeInimigos
from arvores import Arvore
from grama import Grama
from vida import Vida
from Menu import Menu # Se você estiver usando uma classe Menu
from gerador_plantas import gerar_plantas_ao_redor_do_jogador
from timer1 import Timer


# Inicialização do jogo e variáveis
def inicializar_jogo():
    """Inicializa as variáveis e objetos do jogo."""
    tempo_inicio = pygame.time.get_ticks()
    jogador = Player()
    estacoes = Estacoes()
    vida = Vida(vida_maxima=100, vida_atual=100)
    gramas = []
    arvores = []
    blocos_gerados = set()
    # Inicializa o gerenciador de inimigos, talvez com parâmetros ajustados
    gerenciador_inimigos = GerenciadorDeInimigos(intervalo_spawn=5.0, spawns_iniciais=3)

    # Retorna todos os objetos e estados iniciais
    return jogador, estacoes, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, False, tempo_inicio

# Verifica colisões entre jogador e inimigos
def verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador, vida):
    """
    Verifica colisões entre o jogador e todos os inimigos e aplica dano.
    Usa colliderect() para detecção de colisão.
    """
    for inimigo in list(gerenciador_inimigos.inimigos):
        if inimigo.rect.colliderect(jogador.rect):
            vida.receber_dano(10)
            # Opcional: Adicionar lógica para empurrar o inimigo ou jogador após a colisão.
            # Isso pode ser feito aqui ou no método atacar do inimigo.


# Desenha toda a cena (terreno, jogador, timer, vida)
# Agora recebe o objeto timer como argumento
def atualizar_cena(est, gramas, arvores, jogador, janela, camera_x, camera_y, vida, tempo_decorrido, timer_obj):
    """
    Desenha todos os elementos da cena, incluindo terreno, plantas, jogador, vida e timer.
    Agora utiliza um objeto Timer para desenhar o timer.

    Args:
        est (Estacoes): Objeto da estação atual.
        gramas (list): Lista de objetos Grama.
        arvores (list): Lista de objetos Arvore.
        jogador (Player): Objeto do jogador.
        janela (pygame.Surface): A superfície onde desenhar.
        camera_x (int): O offset x da câmera.
        camera_y (int): O offset y da câmera.
        vida (Vida): Objeto de vida do jogador.
        tempo_decorrido (int): Tempo decorrido em segundos.
        timer_obj (Timer): Objeto Timer para desenhar.
    """
    est.desenhar(janela) # Desenha o plano de fundo da estação

    # Desenha gramas com offset da câmera
    for gr in gramas:
        gr.desenhar(janela, camera_x, camera_y)

    # Separa árvores para desenhar atrás e na frente do jogador para ordem de desenho correta
    arvores_tras = [a for a in arvores if a.rect.bottom < jogador.rect.bottom]
    arvores_frente = [a for a in arvores if a.rect.bottom >= jogador.rect.bottom]

    # Desenha árvores atrás do jogador
    for a in arvores_tras:
        a.desenhar(janela, camera_x, camera_y)

    # Desenha o jogador centralizado na tela
    janela.blit(jogador.image, (
        janela.get_width() // 2 - jogador.rect.width // 2,
        janela.get_height() // 2 - jogador.rect.height // 2
    ))

    # Desenha árvores na frente do jogador
    for a in arvores_frente:
        a.desenhar(janela, camera_x, camera_y)

    est.desenhar_mensagem_estacao(janela) # Desenha a mensagem da estação atual
    vida.desenhar(janela, 20, 20) # Desenha a barra de vida

    # Desenha o timer usando o objeto Timer
    timer_obj.desenhar(janela, tempo_decorrido)


# Tela de morte e opções de reinício ou saída
def tela_de_morte(janela):
    """Exibe a tela de morte e aguarda a entrada do usuário para reiniciar ou sair."""
    fonte = pygame.font.Font(None, 45)
    texto = fonte.render("Você morreu! Pressione R para reiniciar ou ESC para sair.", True, (255, 0, 0))

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                main() # Reinicia o jogo chamando main() novamente
                return # Sai da tela de morte para evitar loop infinito

        janela.fill((0, 0, 0)) # Preenche a tela com preto
        pos_x = janela.get_width() // 2 - texto.get_width() // 2
        pos_y = janela.get_height() // 2 - texto.get_height() // 2
        janela.blit(texto, (pos_x, pos_y)) # Desenha o texto de morte
        pygame.display.update() # Atualiza a tela
        pygame.time.Clock().tick(60) # Limita o FPS

# Função principal
def main():
    """Função principal que executa o loop do jogo."""
    pygame.init() # Inicializa o Pygame
    largura_tela, altura_tela = 1920, 1080
    janela = pygame.display.set_mode((largura_tela, altura_tela)) # Cria a janela do jogo
    pygame.display.set_caption("Lenda de Asrahel") # Define o título da janela
    clock = pygame.time.Clock() # Cria um objeto Clock para controlar o FPS

    # Inicializa todos os componentes do jogo
    jogador, est, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, jogador_morreu, tempo_inicio = inicializar_jogo()

    # Cria uma instância do Timer.
    # Calcula a posição X para centralizar o fundo do timer.
    # A posição Y pode ser um valor fixo no topo.
    timer_pos_y = 30 # Posição Y fixa no topo
    # Para centralizar o timer, precisamos saber a largura do texto. Como a largura
    # do texto varia (MM:SS), é melhor calcular a posição X de desenho dentro
    # do método desenhar da classe Timer, mas podemos dar uma posição inicial aqui.
    # Uma estimativa simples para centralizar a área do timer:
    fonte_estimativa = pygame.font.Font(None, 36)
    largura_estimada_texto = fonte_estimativa.size("00:00")[0] # Largura estimada para "00:00"
    largura_estimada_fundo = largura_estimada_texto + 10 # Largura estimada do fundo
    timer_pos_x = janela.get_width() // 2 - largura_estimada_fundo // 2

    timer_obj = Timer(timer_pos_x, timer_pos_y)


    # Loop principal do jogo
    while not jogador_morreu:
        dt = clock.tick(60) # Controla o FPS e obtém o tempo desde o último frame

        # Lida com eventos do Pygame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit() # Sai do Pygame
                return # Sai da função main

        # Obtém o estado das teclas pressionadas e move o jogador
        teclas = pygame.key.get_pressed()
        jogador.mover(teclas, arvores)
        jogador.update() # Atualiza o estado do jogador (animação, etc.)

        # Gera plantas ao redor do jogador conforme ele se move
        gerar_plantas_ao_redor_do_jogador(jogador, gramas, arvores, est, blocos_gerados)

        # Detecta mudança de estação e atualiza árvores e spawna inimigos imediatamente
        est_ant = est.i
        est.atualizar() # Atualiza a estação
        if est.i != est_ant:
            # Atualiza os sprites das árvores para a nova estação
            for arv in arvores:
                arv.atualizar_sprite(est.i)
            # Spawna inimigos imediatamente ao mudar de estação
            gerenciador_inimigos.spawn_inimigos(est.i, jogador)

        # Tenta spawnar inimigos periodicamente
        gerenciador_inimigos.tentar_spawnar(est.i, jogador)


        # Atualiza inimigos (movimento e ataque)
        gerenciador_inimigos.update_inimigos(jogador)

        # Câmera centralizada no jogador
        camera_x = jogador.rect.centerx - largura_tela // 2
        camera_y = jogador.rect.centery - altura_tela // 2

        janela.fill((0, 0, 0)) # Preenche o fundo da janela

        # Desenha a cena com offset da câmera
        # Passa o objeto timer para a função atualizar_cena
        tempo_decorrido_segundos = (pygame.time.get_ticks() - tempo_inicio) // 1000
        atualizar_cena(est, gramas, arvores, jogador, janela, camera_x, camera_y, vida, tempo_decorrido_segundos, timer_obj)

        # Desenha inimigos após a cena, com offset da câmera
        gerenciador_inimigos.desenhar_inimigos(janela, camera_x, camera_y)

        # Verifica colisões entre jogador e inimigos e aplica dano
        verificar_colisoes_com_inimigos(gerenciador_inimigos, jogador, vida)

        # Verifica se o jogador morreu APÓS verificar colisões e aplicar dano
        if not vida.esta_vivo():
            jogador_morreu = True # Define a flag para sair do loop principal

        pygame.display.update() # Atualiza a tela para mostrar as mudanças

    # Se o loop principal terminou (jogador morreu), chama a tela de morte
    tela_de_morte(janela)

# Executa a função main se o script for o ponto de entrada principal
if __name__ == "__main__":
    main()
