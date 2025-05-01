import pygame
import random
from player import Player
from Estacoes import Estacoes
from Inimigos import Fantasma
from arvores import Arvore
from grama import Grama
from vida import Vida

# Armazena regiões já geradas (dividido em "blocos")
blocos_gerados = set()

def gerar_plantas_ao_redor_do_jogador(jogador, gramas, arvores, est):
    distancia_geracao = 1920  # distância do centro do jogador
    bloco_tamanho = 1080  # tamanho do bloco usado para evitar gerar novamente

    jogador_bloco_x = jogador.rect.x // bloco_tamanho
    jogador_bloco_y = jogador.rect.y // bloco_tamanho

    # Explora ao redor do jogador (9 blocos)
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            bloco_coord = (jogador_bloco_x + dx, jogador_bloco_y + dy)
            if bloco_coord not in blocos_gerados:
                blocos_gerados.add(bloco_coord)
                base_x = (jogador_bloco_x + dx) * bloco_tamanho
                base_y = (jogador_bloco_y + dy) * bloco_tamanho

                for _ in range(random.randint(5, 10)):
                    tipo_planta = random.choice(['grama', 'arvore'])
                    x = base_x + random.randint(0, bloco_tamanho)
                    y = base_y + random.randint(0, bloco_tamanho)

                    if tipo_planta == 'grama':
                        gramas.append(Grama(x, y, 50, 50))
                    else:
                        arvores.append(Arvore(x, y, 180, 180, est.i))

def main():
    pygame.init()
    janela = pygame.display.set_mode()
    pygame.display.set_caption("Lenda de Asrahel")

    Asrahel = Player()
    fantasminha = Fantasma(velocidade=1.5)
    est = Estacoes()
    vida = Vida(vida_maxima=100, vida_atual=100)

    gramas = []
    arvores = []

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return

        teclas = pygame.key.get_pressed()
        Asrahel.mover(teclas, arvores)
        Asrahel.update()
        fantasminha.update(Asrahel.rect)

        gerar_plantas_ao_redor_do_jogador(Asrahel, gramas, arvores, est)

        # Atualiza estação e árvores
        tempo_anterior = est.i
        est.atualizar()
        if est.i != tempo_anterior:
            for arv in arvores:
                arv.atualizar_sprite(est.i)

        if fantasminha.verificar_colisao(Asrahel):
            vida.receber_dano(10)

        if vida.vida_atual <= 0:
            fonte = pygame.font.SysFont(None, 75)
            texto = fonte.render("Você morreu! Pressione R para reiniciar ou ESC para sair.", True, (255, 0, 0))
            janela.fill((0, 0, 0))
            janela.blit(texto, (janela.get_width() // 2 - texto.get_width() // 2,
                                janela.get_height() // 2))
            pygame.display.update()
            esperando_input = True
            while esperando_input:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                        pygame.quit()
                        return
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                        main()
                        return

        # Câmera centralizada
        camera_x = Asrahel.rect.centerx - janela.get_width() // 2
        camera_y = Asrahel.rect.centery - janela.get_height() // 2

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

        fantasminha.desenhar(janela, camera_x, camera_y)
        vida.desenhar(janela, 20, 20)

        pygame.display.update()

if __name__ == "__main__":
    main()
