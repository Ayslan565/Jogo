import time
import random
import pygame
# Importe as classes de inimigos. Certifique-se de que os caminhos de importação estão corretos
# com base na estrutura do seu projeto (ex: from Arquivos.Fantasma import fantasma)
from Fantasma import fantasma
from BonecoDeNeve import BonecoDeNeve
import math # Importe math se for usado em alguma lógica interna (não parece ser o caso aqui, mas mantido por segurança)

class GerenciadorDeInimigos:
    """
    Gerencia a criação, atualização e desenho dos inimigos no jogo.
    """
    def __init__(self, intervalo_spawn: float = 3.0, spawns_iniciais: int = 5):
        """
        Inicializa o gerenciador de inimigos.

        Args:
            intervalo_spawn (float): Tempo em segundos entre os spawns periódicos.
            spawns_iniciais (int): Número de inimigos a spawnar imediatamente em certas condições.
        """
        self.inimigos = [] # Lista para armazenar os objetos inimigos ativos
        self.ultimo_spawn = time.time() # Tempo do último spawn para controle do intervalo
        self.intervalo_spawn = intervalo_spawn # Intervalo entre spawns periódicos
        self.spawns_iniciais = spawns_iniciais # Quantidade de spawns iniciais

    def spawn_inimigos(self, estacao, jogador):
        """
        Spawna inimigos com base na estação atual.
        Esta função é chamada para spawns imediatos (ex: mudança de estação)
        e periodicamente pela função tentar_spawnar.

        Args:
            estacao (int ou str): A estação atual (0-3 ou nome).
            jogador (Player): O objeto jogador para determinar a área de spawn.
        """
        nomes = {0: 'primavera', 1: 'verao', 2: 'outono', 3: 'inverno'}
        # Converte o índice da estação para o nome, se necessário
        est_nome = estacao if isinstance(estacao, str) else nomes.get(estacao, '')

        # Exemplo: Spawna inimigos específicos no inverno
        if est_nome == "inverno":
            # Lista de tipos de inimigos disponíveis para spawn nesta estação
            tipos_disponiveis = []
            # Adiciona classes de inimigos à lista APENAS se elas foram importadas com sucesso
            if 'fantasma' in globals() and isinstance(fantasma, type):
                 tipos_disponiveis.append(fantasma)
            if 'BonecoDeNeve' in globals() and isinstance(BonecoDeNeve, type):
                 tipos_disponiveis.append(BonecoDeNeve)

            # Spawna inimigos apenas se houver tipos disponíveis
            if tipos_disponiveis:
                 for _ in range(self.spawns_iniciais):
                    # Escolhe um tipo de inimigo aleatoriamente entre os disponíveis
                    tipo = random.choice(tipos_disponiveis)
                    # Calcula uma posição de spawn aleatória ao redor do jogador
                    x = jogador.rect.centerx + random.choice([-1, 1]) * random.randint(100, 300)
                    y = jogador.rect.centery + random.choice([-1, 1]) * random.randint(100, 300)
                    # Cria uma instância do inimigo escolhido
                    inimigo = tipo(x, y)
                    # Adiciona o novo inimigo à lista de inimigos ativos
                    self.inimigos.append(inimigo)
            else:
                 print("Aviso: Nenhum tipo de inimigo disponível para spawn no inverno.")


    def tentar_spawnar(self, estacao, jogador):
        """
        Verifica se é hora de spawnar novos inimigos periodicamente e os spawna.

        Args:
            estacao (int ou str): A estação atual.
            jogador (Player): O objeto jogador.
        """
        agora = time.time()
        # Verifica se o intervalo de spawn passou desde o último spawn
        if agora - self.ultimo_spawn >= self.intervalo_spawn:
            self.spawn_inimigos(estacao, jogador) # Chama a função de spawn
            self.ultimo_spawn = agora # Atualiza o tempo do último spawn

    def update_inimigos(self, jogador):
        """
        Atualiza o estado de todos os inimigos ativos (movimento, ataque, vida).

        Args:
            jogador (Player): O objeto jogador para que os inimigos possam segui-lo e atacá-lo.
        """
        # Cria uma cópia da lista para permitir a remoção segura durante a iteração
        for inimigo in list(self.inimigos):
            inimigo.update(jogador.rect) # Atualiza o inimigo (movimento, animação, etc.)
            # Verifica se o inimigo tem um método 'atacar' e o chama
            if hasattr(inimigo, 'atacar'):
                inimigo.atacar(jogador)
            # Verifica se o inimigo tem HP e se ele chegou a zero ou menos
            if hasattr(inimigo, 'hp') and inimigo.hp <= 0:
                self.inimigos.remove(inimigo) # Remove o inimigo da lista se ele morreu

    def desenhar_inimigos(self, janela, camera_x: int, camera_y: int):
        """
        Desenha todos os inimigos ativos na janela, aplicando o offset da câmera.

        Args:
            janela (pygame.Surface): A superfície onde desenhar.
            camera_x (int): O offset x da câmera.
            camera_y (int): O offset y da câmera.
        """
        for inimigo in self.inimigos:
            inimigo.desenhar(janela, camera_x, camera_y) # Chama o método desenhar do inimigo

    def limpar_inimigos(self):
        """Remove todos os inimigos ativos da lista."""
        self.inimigos.clear()
