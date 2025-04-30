import pygame
import random
from player import Player
from Estacoes import Estacoes
from Inimigos import Fantasma
from arvores import Arvore
from grama import Grama
from vida import Vida  # Importando a classe Vida

def main():
    pygame.init()
    janela = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Lenda de Asrahel")

    # Instâncias principais
    Asrahel = Player()
    fantasminha = Fantasma(velocidade=1.5)
    est = Estacoes()
    vida = Vida(vida_maxima=100, vida_atual=100)

    # Gramas
    gramas = [Grama(random.randint(0, janela.get_width()),
                    random.randint(0, janela.get_height()), 50, 50)
              for _ in range(random.randint(80, 350))]

    # Árvores
    arvores = pygame.sprite.Group()
    x_ant = 0
    for _ in range(random.randint(0, 20)):
        x = x_ant + random.randint(80, 150)
        if x + 180 > janela.get_width():
            x = janela.get_width() - 180
        y = random.randint(10, janela.get_height() - 180)
        arv = Arvore(x, y, 180, 180)
        arvores.add(arv)
        x_ant = x

    camera_x = camera_y = 0
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(20)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return

        # Atualizações
        teclas = pygame.key.get_pressed()
        Asrahel.mover(teclas, arvores)
        Asrahel.update()
        est.atualizar()
        fantasminha.update(Asrahel.rect)

        if fantasminha.verificar_colisao(Asrahel):
            print("O fantasma bateu no jogador!")
            vida.receber_dano(10)

        if vida.vida_atual <= 0:
            print("Você morreu!")
            janela.fill((0, 0, 0))
            fonte = pygame.font.SysFont(None, 75)
            texto = fonte.render("Você morreu! Pressione R para reiniciar ou ESC para sair.", True, (255, 0, 0))
            janela.blit(texto, (janela.get_width() // 2 - texto.get_width() // 2, janela.get_height() // 2))
            pygame.display.update()

            esperando_input = True
            while esperando_input:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                        pygame.quit()
                        return
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                        main()
                        esperando_input = False

        # Desenho
        est.desenhar(janela)
        for gr in gramas:
            gr.desenhar(janela)

        vida.desenhar(janela, 20, 20)

        # Separar árvores
        arvores_tras = [arv for arv in arvores if arv.rect.bottom < Asrahel.rect.bottom]
        arvores_frente = [arv for arv in arvores if arv.rect.bottom >= Asrahel.rect.bottom]

        # Desenha árvores atrás do jogador
        for arv in arvores_tras:
            arv.desenhar(janela)

        # Desenha o jogador
        janela.blit(Asrahel.image, Asrahel.rect)

        # Desenha árvores na frente do jogador
        for arv in arvores_frente:
            arv.desenhar(janela)

        # Desenha o fantasma
        fantasminha.desenhar(janela, camera_x, camera_y)

        pygame.display.update()

if __name__ == "__main__":
    main()
