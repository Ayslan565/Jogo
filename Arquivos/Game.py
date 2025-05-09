import pygame
import random
from player import Player
from Estacoes import Estacoes
from GerenciadorDeInimigos import GerenciadorDeInimigos
from Fantasma import fantasma
from BonecoDeNeve import BonecoDeNeve
from arvores import Arvore
from grama import Grama
from vida import Vida
from Menu import Menu
from gerador_plantas import gerar_plantas_ao_redor_do_jogador

def inicializar_jogo():
    tempo_inicio = pygame.time.get_ticks()
    Asrahel = Player()
    est = Estacoes()
    vida = Vida(vida_maxima=100, vida_atual=100)
    gramas = []
    arvores = []
    blocos_gerados = set()
    gerenciador_inimigos = GerenciadorDeInimigos()
    jogador_morreu = False

    tempo_spawn = 0
    taxa_spawn = 1
    tempo_geracao_inimigos = 5000
    quantidade_inimigos = 1

    return Asrahel, est, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, jogador_morreu, tempo_spawn, taxa_spawn, tempo_geracao_inimigos, quantidade_inimigos, tempo_inicio

def spawn_inimigos(estacao, tempo_spawn, tempo_geracao_inimigos, quantidade_inimigos, gerenciador_inimigos):
    if tempo_spawn >= tempo_geracao_inimigos:
        tempo_spawn = 0
        quantidade_inimigos *= 2  # crescimento exponencial

        if estacao == "inverno":
            for _ in range(quantidade_inimigos):
                tipo_inimigo = random.choice([fantasma, BonecoDeNeve])
                inimigo = tipo_inimigo()
                gerenciador_inimigos.adicionar_inimigo(inimigo)
    return tempo_spawn, quantidade_inimigos

def verificar_colisoes_com_inimigos(gerenciador_inimigos, Asrahel, vida):
    for inimigo in gerenciador_inimigos.inimigos:
        if inimigo.verificar_colisao(Asrahel):
            vida.receber_dano(10)

def atualizar_cena(est, gramas, arvores, Asrahel, janela, camera_x, camera_y, vida, tempo_decorrido):
    est.desenhar(janela)
    est.desenhar_mensagem_estacao(janela)

    for gr in gramas:
        gr.desenhar(janela, camera_x, camera_y)

    arvores_tras = [a for a in arvores if a.rect.bottom < Asrahel.rect.bottom]
    arvores_frente = [a for a in arvores if a.rect.bottom >= Asrahel.rect.bottom]

    for a in arvores_tras:
        a.desenhar(janela, camera_x, camera_y)

    janela.blit(Asrahel.image,
                (janela.get_width() // 2 - Asrahel.rect.width // 2,
                 janela.get_height() // 2 - Asrahel.rect.height // 2))

    for a in arvores_frente:
        a.desenhar(janela, camera_x, camera_y)

    est.desenhar_mensagem_estacao(janela)
    vida.desenhar(janela, 20, 20)
    
    # Desenha o timer
    fonte_timer = pygame.font.Font(pygame.font.get_default_font(), 36)
    texto_timer = fonte_timer.render(f" {tempo_decorrido}", True, (255, 255, 255))
    timer_pos_x = janela.get_width() // 2 - texto_timer.get_width() // 2
    timer_pos_y = 30  # um pouco abaixo do topo

    borda_arredondada = pygame.Surface((texto_timer.get_width() + 10, texto_timer.get_height() + 10), pygame.SRCALPHA)
    borda_arredondada.set_alpha(128)  # 50% de transparência
    borda_arredondada.fill((0, 0, 0, 0))
    pygame.draw.rect(borda_arredondada, (0, 0, 0), (0, 0, texto_timer.get_width() + 10, texto_timer.get_height() + 10), border_radius=10)
    pygame.draw.rect(borda_arredondada, (255, 255, 255), (0, 0, texto_timer.get_width() + 10, texto_timer.get_height() + 10), 2, border_radius=10)
    janela.blit(borda_arredondada, (timer_pos_x - 5, timer_pos_y - 5))

    janela.blit(texto_timer, (timer_pos_x, timer_pos_y))

def tela_de_morte(janela):
    fonte = pygame.font.Font(pygame.font.get_default_font(), 45)
    texto = fonte.render("Você morreu! Pressione R para reiniciar ou ESC para sair.", True, (255, 0, 0))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                main()  # Reinicia o jogo

        janela.fill((0, 0, 0))
        texto_pos_x = janela.get_width() // 2 - texto.get_width() // 2
        texto_pos_y = janela.get_height() // 2 - texto.get_height() // 2
        janela.blit(texto, (texto_pos_x, texto_pos_y))
        pygame.display.update()
        pygame.time.Clock().tick(60)

def main():
    pygame.init()
    janela = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Lenda de Asrahel")
    clock = pygame.time.Clock()

    Asrahel, est, vida, gramas, arvores, blocos_gerados, gerenciador_inimigos, jogador_morreu, tempo_spawn, taxa_spawn, tempo_geracao_inimigos, quantidade_inimigos, tempo_inicio = inicializar_jogo()

    tempo_decorrido = 0  # Inicializando a variável tempo_decorrido fora do loop

    while not jogador_morreu:
        dt = clock.tick(60)

        # Eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return

        teclas = pygame.key.get_pressed()
        Asrahel.mover(teclas, arvores)
        Asrahel.update()

        gerar_plantas_ao_redor_do_jogador(Asrahel, gramas, arvores, est, blocos_gerados)

        # Atualiza estação e sprites das árvores se mudar
        tempo_anterior = est.i
        est.atualizar()
        if est.i != tempo_anterior:
            for arv in arvores:
                arv.atualizar_sprite(est.i)

        tempo_spawn, quantidade_inimigos = spawn_inimigos(est.i, tempo_spawn, tempo_geracao_inimigos, quantidade_inimigos, gerenciador_inimigos)

        gerenciador_inimigos.update_inimigos(Asrahel.rect)
        gerenciador_inimigos.desenhar_inimigos(janela, 0, 0)
        # Verifica colisões com inimigos
        verificar_colisoes_com_inimigos(gerenciador_inimigos, Asrahel, vida)

        if vida.vida_atual <= 0:
            jogador_morreu = True
            break

        # Câmera
        camera_x = Asrahel.rect.centerx - janela.get_width() // 2
        camera_y = Asrahel.rect.centery - janela.get_height() // 2

        # Atualiza o tempo de jogo
        tempo_decorrido = (pygame.time.get_ticks() - tempo_inicio) // 1000  # Tempo em segundos

        # Desenho da cena
        atualizar_cena(est, gramas, arvores, Asrahel, janela, camera_x, camera_y, vida, tempo_decorrido)

        pygame.display.update()

    # Tela de morte
    tela_de_morte(janela)

if __name__ == "__main__":
    main()
