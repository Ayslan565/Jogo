import pygame
import math
import os

class ProjetilMaga(pygame.sprite.Sprite):
    sprites_carregados = None
    tamanho_sprite_definido = (30, 30) # Tamanho do projétil

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", "..", ".."))

    @staticmethod
    def carregar_recursos_projetil_maga():
        if ProjetilMaga.sprites_carregados is None:
            caminhos_sprites = ["Sprites/Inimigos/Maga/Projetil_1.png", # Exemplo de sprite de projétil
                                "Sprites/Inimigos/Maga/Projetil_2.png"]
            ProjetilMaga.sprites_carregados = []
            pasta_raiz = ProjetilMaga._obter_pasta_raiz_jogo()
            for path_relativo in caminhos_sprites:
                caminho_completo = os.path.join(pasta_raiz, path_relativo.replace("/", os.sep))
                try:
                    if os.path.exists(caminho_completo):
                        sprite = pygame.image.load(caminho_completo).convert_alpha()
                        sprite = pygame.transform.scale(sprite, ProjetilMaga.tamanho_sprite_definido)
                        ProjetilMaga.sprites_carregados.append(sprite)
                    else:
                        print(f"AVISO: Sprite de projétil '{caminho_completo}' não encontrado. Usando placeholder.")
                        placeholder = pygame.Surface(ProjetilMaga.tamanho_sprite_definido, pygame.SRCALPHA)
                        placeholder.fill((255, 100, 0, 200)) # Cor laranja/roxa para o projétil
                        ProjetilMaga.sprites_carregados.append(placeholder)
                except pygame.error as e:
                    print(f"ERRO ao carregar sprite de projétil '{caminho_completo}': {e}. Usando placeholder.")
                    placeholder = pygame.Surface(ProjetilMaga.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder.fill((255, 100, 0, 200))
                    ProjetilMaga.sprites_carregados.append(placeholder)
            if not ProjetilMaga.sprites_carregados:
                placeholder = pygame.Surface(ProjetilMaga.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder.fill((200, 50, 0, 255))
                ProjetilMaga.sprites_carregados.append(placeholder)

    def __init__(self, x, y, direcao_x, direcao_y, dano, velocidade, sprite_inicial=None):
        super().__init__()
        ProjetilMaga.carregar_recursos_projetil_maga()

        self.x = float(x)
        self.y = float(y)
        self.direcao_x = direcao_x
        self.direcao_y = direcao_y
        self.dano = dano
        self.velocidade = velocidade # Pixels por frame ou por segundo (depende de como dt_ms é usado)
        self.sprites = ProjetilMaga.sprites_carregados
        self.sprite_index = 0
        self.intervalo_animacao = 100 # Animação do projétil
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()

        if self.sprites:
            self.image = self.sprites[self.sprite_index]
        else:
            self.image = pygame.Surface(ProjetilMaga.tamanho_sprite_definido, pygame.SRCALPHA)
            self.image.fill((255, 100, 0, 200)) # Fallback para cor se não houver sprite
        
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.esta_ativo_flag = True
        self.duracao_maxima_ms = 5000 # Tempo máximo de vida do projétil em ms
        self.tempo_criacao = pygame.time.get_ticks()

    def update(self, dt_ms):
        if not self.esta_ativo_flag:
            return

        agora = pygame.time.get_ticks()
        if agora - self.tempo_criacao > self.duracao_maxima_ms:
            self.kill() # Remove o projétil se ele durar muito tempo
            self.esta_ativo_flag = False
            return

        # Movimento do projétil
        movimento_x = self.direcao_x * self.velocidade * (dt_ms / 1000.0) # Ajuste para dt_ms
        movimento_y = self.direcao_y * self.velocidade * (dt_ms / 1000.0)

        self.x += movimento_x
        self.y += movimento_y
        self.rect.center = (int(self.x), int(self.y))

        # Atualizar animação
        if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            self.image = self.sprites[self.sprite_index]
            self.tempo_ultimo_update_animacao = agora

    def desenhar(self, janela, camera_x, camera_y):
        if self.esta_ativo_flag:
            janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

    def esta_ativo(self):
        return self.esta_ativo_flag

    def kill(self):
        self.esta_ativo_flag = False
        super().kill()