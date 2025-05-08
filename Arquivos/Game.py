import pygame
import random
from player import Player
from Estacoes import Estacoes
from GerenciadorDeInimigos import GerenciadorDeInimigos
from fantasma import Fantasma
from boneco_de_neve import BonecoDeNeve
from arvores import Arvore
from grama import Grama
from vida import Vida
from gerador_plantas import gerar_plantas_ao_redor_do_jogador

def main():
    pygame.init()
    janela = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Lenda de Asrahel")
    clock = pygame.time.Clock()

    # Inicializa o jogo
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

        # Spawn de inimigos baseado no tempo
        tempo_spawn += dt
        if tempo_spawn >= tempo_geracao_inimigos:
            tempo_spawn = 0
            quantidade_inimigos *= 2  # crescimento exponencial

            if est.i == "inverno":
                for _ in range(quantidade_inimigos):
                    tipo_inimigo = random.choice([Fantasma, BonecoDeNeve])
                    inimigo = tipo_inimigo()
                    gerenciador_inimigos.adicionar_inimigo(inimigo)

        gerenciador_inimigos.update_inimigos(Asrahel.rect)
        gerenciador_inimigos.desenhar_inimigos(janela, 0, 0)

        # Verifica colisões com inimigos
        for inimigo in gerenciador_inimigos.inimigos:
            if inimigo.verificar_colisao(Asrahel):
                vida.receber_dano(10)

        if vida.vida_atual <= 0:
            jogador_morreu = True
            break

        # Câmera
        camera_x = Asrahel.rect.centerx - janela.get_width() // 2
        camera_y = Asrahel.rect.centery - janela.get_height() // 2

        # Desenho da cena
        est.desenhar(janela)

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

        vida.desenhar(janela, 20, 20)

        pygame.display.update()

    # Tela de morte
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
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
