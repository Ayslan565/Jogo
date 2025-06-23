import pygame
import os
import random
import time

TIPO_CURA = "cura"
TIPO_LENTIDAO = "lentidao"
TIPO_RAPIDEZ = "rapidez"

DURACAO_EFEITO_COGUMELO_S = 10 

class Cogumelo(pygame.sprite.Sprite):
    """
    Representa um cogumelo coletável no jogo, com um tipo de efeito específico.
    """
    def __init__(self, x, y, tipo_cogumelo=TIPO_CURA):
        super().__init__()
        self.x = x
        self.y = y
        self.largura = 60 # Tamanho do sprite do cogumelo
        self.altura = 60 # Tamanho do sprite do cogumelo
        self.coletado = False
        self.tipo_cogumelo = tipo_cogumelo # Define o tipo de cogumelo (cura, lentidao, rapidez)

        # --- CORRIGIDO: Nomes dos arquivos de sprite atualizados para corresponder à imagem. ---
        sprite_paths_disponiveis = [
            os.path.join("Sprites", "Cogumelos", "Cogumelo 1.png"),
            os.path.join("Sprites", "Cogumelos", "Cogumelo 2.png"),
            os.path.join("Sprites", "Cogumelos", "Cogumelo 3.png"),
        ]
        
        # Escolhe um sprite aleatoriamente para este cogumelo
        self.sprite_path = random.choice(sprite_paths_disponiveis)

        self.image = self._carregar_sprite(self.sprite_path, (self.largura, self.altura))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def _carregar_sprite(self, path, tamanho):
        """Carrega e escala um sprite, com um fallback para placeholder."""
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        project_root_dir = os.path.dirname(base_dir) 
        
        full_path = os.path.join(project_root_dir, path.replace("\\", "/"))

        if not os.path.exists(full_path): 
            #print(f"ALERTA(Cogumelo): Sprite não encontrado: {full_path}. Usando placeholder.") 
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            
            # Cores de placeholder baseadas no tipo para depuração
            if self.tipo_cogumelo == TIPO_CURA:
                img.fill((0, 150, 0, 150)) # Verde para Cura
            elif self.tipo_cogumelo == TIPO_LENTIDAO:
                img.fill((0, 0, 150, 150)) # Azul para Lentidão
            elif self.tipo_cogumelo == TIPO_RAPIDEZ:
                img.fill((150, 150, 0, 150)) # Amarelo para Rapidez
            else:
                img.fill((150, 0, 150, 150)) # Magenta padrão

            pygame.draw.circle(img, (200, 50, 200), (tamanho[0]//2, tamanho[1]//2), tamanho[0]//2 - 5) 
            return img 
        try:
            img = pygame.image.load(full_path).convert_alpha() 
            img = pygame.transform.scale(img, tamanho) 
            return img 
        except pygame.error as e:
            #print(f"ERRO(Cogumelo): Erro ao carregar sprite '{full_path}' para o tipo {self.tipo_cogumelo}: {e}. Usando placeholder.") 
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            
            if self.tipo_cogumelo == TIPO_CURA:
                img.fill((0, 150, 0, 150))
            elif self.tipo_cogumelo == TIPO_LENTIDAO:
                img.fill((0, 0, 150, 150))
            elif self.tipo_cogumelo == TIPO_RAPIDEZ:
                img.fill((150, 150, 0, 150))
            else:
                img.fill((150, 0, 150, 150))

            pygame.draw.circle(img, (200, 50, 200), (tamanho[0]//2, tamanho[1]//2), tamanho[0]//2 - 5) 
            return img 

    def aplicar_efeito(self, jogador):
        """Aplica o efeito específico do cogumelo ao jogador."""
        if not self.coletado: 
            #print(f"DEBUG(Cogumelo): Cogumelo de {self.tipo_cogumelo} coletado!") 
            if self.tipo_cogumelo == TIPO_CURA:
                self._efeito_cura_vida(jogador)
            elif self.tipo_cogumelo == TIPO_LENTIDAO:
                self._efeito_lentidao(jogador)
            elif self.tipo_cogumelo == TIPO_RAPIDEZ:
                self._efeito_rapidez(jogador)
            
            self.coletado = True 
            self.kill() # Remove o sprite do grupo 

    def _efeito_cura_vida(self, jogador):
        """Função de efeito: Cura a vida do jogador."""
        # Verificando se o objeto 'vida' existe E tem os atributos 'hp' e 'max_hp' para evitar AttributeError
        if hasattr(jogador, 'vida') and jogador.vida is not None and \
           hasattr(jogador.vida, 'curar') and \
           hasattr(jogador.vida, 'hp') and hasattr(jogador.vida, 'max_hp'):
            jogador.vida.curar(30) # Cura 30 de vida
            #print(f"DEBUG(Efeito Cura): Vida do jogador curada! Vida atual: {jogador.vida.hp}/{jogador.vida.max_hp}")
    

    def _efeito_lentidao(self, jogador):
        """Função de efeito: Aplica lentidão ao jogador."""
        if hasattr(jogador, 'velocidade') and hasattr(jogador, 'velocidade_original'):
            jogador.velocidade = jogador.velocidade_original * 0.5 # Reduz velocidade para 50%
            jogador.tempo_fim_efeito_lentidao = time.time() + DURACAO_EFEITO_COGUMELO_S # Duração de 10 segundos
            #print(f"DEBUG(Efeito Lentidão): Jogador ficou lento por {DURACAO_EFEITO_COGUMELO_S}s. Velocidade atual: {jogador.velocidade}")
    

    def _efeito_rapidez(self, jogador):
        """Função de efeito: Aplica rapidez ao jogador."""
        if hasattr(jogador, 'velocidade') and hasattr(jogador, 'velocidade_original'):
            jogador.velocidade = jogador.velocidade_original * 1.5 # Aumenta velocidade para 150%
            jogador.tempo_fim_efeito_rapidez = time.time() + DURACAO_EFEITO_COGUMELO_S # Duração de 10 segundos
            #print(f"DEBUG(Efeito Rapidez): Jogador ficou rápido por {DURACAO_EFEITO_COGUMELO_S}s. Velocidade atual: {jogador.velocidade}")
    

    def desenhar(self, janela, camera_x, camera_y):
        """Desenha o cogumelo na tela."""
        if not self.coletado: 
            screen_x = self.rect.x - camera_x 
            screen_y = self.rect.y - camera_y 
            janela.blit(self.image, (screen_x, screen_y))
