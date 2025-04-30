import pygame
import random
import math

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, velocidade=1.5, sprite_paths=None):
        super().__init__()

        # Carrega os sprites fornecidos
        self.sprites = [
            pygame.transform.scale(pygame.image.load(sprite_path), (80, 80))
            for sprite_path in sprite_paths
        ]
        self.sprite_index = 0
        self.image = self.sprites[self.sprite_index]

        # Posição inicial aleatória
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, 700)
        self.rect.y = random.randint(100, 500)

        # Reduz a área de colisão em 20px na largura e altura
        self.rect.inflate_ip(-20, -20)

        self.velocidade = velocidade
        self.hp = 100  # Pontos de vida do Inimigo

    def mover_em_direcao(self, alvo_x, alvo_y):
        dx = alvo_x - self.rect.centerx
        dy = alvo_y - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia
            self.rect.x += dx * self.velocidade
            self.rect.y += dy * self.velocidade

    def atualizar_animacao(self):
        self.sprite_index += 0.1
        if self.sprite_index >= len(self.sprites):
            self.sprite_index = 0
        self.image = self.sprites[int(self.sprite_index)]

    def update(self, alvo_rect):
        self.mover_em_direcao(alvo_rect.centerx, alvo_rect.centery)
        self.atualizar_animacao()

    def desenhar(self, tela, camera_x, camera_y):
        tela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

    def verificar_colisao(self, player):
        return self.rect.colliderect(player.rect)

    def receber_dano(self, dano):
        self.hp -= dano
        if self.hp <= 0:
            self.morrer()

    def morrer(self):
        print(f"{self.__class__.__name__} morreu!")
        self.kill()  # Remove o inimigo do grupo de sprites


class Fantasma(Inimigo):
    def __init__(self, velocidade=1.5):
        sprite_paths = [
            "Sprites/Fantasma/Fantasma1.png", "Sprites/Fantasma/Fantasma2.png", 
            "Sprites/Fantasma/Fantasma3.png", "Sprites/Fantasma/Fantasma4.png", 
            "Sprites/Fantasma/Fantasma5.png", "Sprites/Fantasma/Fantasma6.png", 
            "Sprites/Fantasma/Fantasma8.png", "Sprites/Fantasma/Fantasma9.png"
        ]
        super().__init__(velocidade, sprite_paths)
        self.hp = 100  # Pontos de vida do Fantasma

    def mover_em_direcao(self, alvo_x, alvo_y):
        dx = alvo_x - self.rect.centerx
        dy = alvo_y - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia
            self.rect.x += dx * self.velocidade
            self.rect.y += dy * self.velocidade - 0.5  # Pequena variação para dar mais fluidez ao movimento

    def verificar_colisao(self, player):
        """Verifica colisão com o jogador."""
        return self.rect.colliderect(player.rect)

    def update(self, player_rect):
        """Atualiza o inimigo com base no movimento do jogador."""
        self.mover_em_direcao(player_rect.centerx, player_rect.centery)
        self.atualizar_animacao()

    def atacar(self, player):
        """Quando o fantasma colide com o jogador, ele causa dano e empurra o jogador."""
        if self.rect.colliderect(player.rect):
            dano = 10  # Definindo um valor de dano
            print("Fantasma atacou o jogador!")

            # Causando dano no jogador
            player.receber_dano(dano)

            # Empurrando o jogador para longe do fantasma
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distancia = math.hypot(dx, dy)

            if distancia > 0:
                dx /= distancia
                dy /= distancia
                empurrar_forca = 15  # Intensidade do empurrão
                player.rect.x += dx * empurrar_forca
                player.rect.y += dy * empurrar_forca


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Definindo a imagem do jogador
        self.image = pygame.Surface((50, 50))  # Exemplo de tamanho
        self.image.fill((0, 0, 255))  # Cor do jogador (azul)
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.hp = 100  # Pontos de vida do jogador

    def receber_dano(self, dano):
        self.hp -= dano
        if self.hp <= 0:
            print("Jogador morreu!")

    def update(self, teclas):
        """Movimenta o jogador com as teclas WASD."""
        if teclas[pygame.K_a]:
            self.rect.x -= 5
        if teclas[pygame.K_d]:
            self.rect.x += 5
        if teclas[pygame.K_w]:
            self.rect.y -= 5
        if teclas[pygame.K_s]:
            self.rect.y += 5
