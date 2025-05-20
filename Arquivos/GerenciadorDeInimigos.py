# GerenciadorDeInimigos.py
import pygame
import random
import time
import math # Importa math para a função hypot e exp
import os # Importa os para verificar a existência de arquivos

# Importa a classe base Inimigo do ficheiro Inimigos.py
# Certifique-se de que o ficheiro Inimigos.py está na mesma pasta ou num caminho acessível
from Inimigos import Inimigo


# Importa as classes necessárias
from Estacoes import Estacoes
from Fantasma import Fantasma
from BonecoDeNeve import BonecoDeNeve
from Planta_Carnivora import Planta_Carnivora
from Espantalho import Espantalho
from Fenix import Fenix

# Importa a classe de inimigo da Primavera: Mãe Natureza
from Mae_Natureza import Mae_Natureza

# NOVO: Importa a classe de inimigo da Primavera: Espirito_Das_Flores
from Espirito_Das_Flores import Espirito_Das_Flores


# Importa a classe de projétil (necessária para gerenciar projéteis)
from Projetil_BolaNeve import ProjetilNeve


class GerenciadorDeInimigos:
    """
    Classe responsável por gerenciar todos os inimigos no jogo.
    Lida com a criação, atualização e remoção de inimigos e seus projéteis.
    """
    # Modificado: Recebe uma instância de Estacoes e adiciona parâmetros para spawn exponencial
    # Adicionado parâmetros para largura e altura da tela
    def __init__(self, estacoes_obj, tela_largura: int, altura_tela: int, intervalo_spawn_inicial: float = 3.0, spawns_iniciais: int = 5, limite_inimigos: int = 150, fator_exponencial_spawn: float = 0.02, intervalo_spawn_minimo: float = 0.5):
        """
        Inicializa o gerenciador de inimigos com spawn exponencial e gerenciamento de projéteis.

        Args:
            estacoes_obj (Estacoes): Uma instância da classe Estacoes.
            tela_largura (int): A largura da tela do jogo.
            altura_tela (int): A altura da tela do jogo.
            intervalo_spawn_inicial (float): Tempo inicial em segundos entre os spawns periódicos.
            spawns_iniciais (int): Número de inimigos a spawnar imediatamente em certas condições.
            limite_inimigos (int): O número máximo de inimigos permitidos na tela.
            fator_exponencial_spawn (float): Controla a rapidez com que o intervalo de spawn diminui. Um valor maior significa spawn mais rápido.
            intervalo_spawn_minimo (float): O menor intervalo de spawn permitido.
        """
        self.estacoes = estacoes_obj # Armazena a instância de Estacoes
        self.inimigos = [] # Lista para armazenar todas as instâncias de inimigos
        self.projeteis_inimigos = [] # Lista para armazenar projéteis lançados pelos inimigos
        self.ultimo_spawn = time.time() # Tempo do último spawn para controle do intervalo
        self.intervalo_spawn_inicial = intervalo_spawn_inicial # Intervalo inicial entre spawns periódicos
        self.spawns_iniciais = spawns_iniciais # Quantidade de spawns iniciais
        self.limite_inimigos = limite_inimigos # Novo: Limite máximo de inimigos

        # Adicionados para spawn exponencial
        self.tempo_inicial_jogo = time.time() # Registra o tempo de início do jogo
        self.fator_exponencial_spawn = fator_exponencial_spawn # Fator para o crescimento exponencial
        self.intervalo_spawn_minimo = intervalo_spawn_minimo # Intervalo mínimo para evitar spawns instantâneos

        # Dimensões da tela (necessárias para o update dos projéteis)
        self.tela_largura = tela_largura
        self.altura_tela = altura_tela


    def adicionar_inimigo(self, inimigo):
        """
        Adiciona uma instância de inimigo à lista de inimigos gerenciados.

        Args:
            inimigo (Inimigo): A instância do inimigo a ser adicionada.
        """
        self.inimigos.append(inimigo)

    def remover_inimigo(self, inimigo):
        """
        Remove uma instância de inimigo da lista de inimigos gerenciados.

        Args:
            inimigo (Inimigo): A instância do inimigo a ser removida.
        """
        if inimigo in self.inimigos:
            self.inimigos.remove(inimigo)

    def criar_inimigo_aleatorio(self, tipo_inimigo, x, y, velocidade=1.0):
        """
        Cria uma nova instância de um tipo de inimigo especificado em uma posição.

        Args:
            tipo_inimigo (str): O tipo de inimigo a criar ('fantasma', 'bonecodeneve', 'planta_carnivora', 'espantalho', 'fenix', 'maenatureza', 'espiritodasflores'). # Adicionado espiritodasflores
            x (int): A posição x onde o inimigo será criado.
            y (int): A posição y onde o inimigo será criado.
            velocidade (float): A velocidade de movimento do inimigo (opcional, padrão 1.0).

        Returns:
            Inimigo or None: A instância do inimigo criado, ou None si o tipo for inválido.
        """
        novo_inimigo = None
        if tipo_inimigo.lower() == 'fantasma':
            novo_inimigo = Fantasma(x, y, velocidade=velocidade)
        elif tipo_inimigo.lower() == 'bonecodeneve':
            novo_inimigo = BonecoDeNeve(x, y, velocidade=velocidade)
        elif tipo_inimigo.lower() == 'planta_carnivora':
             novo_inimigo = Planta_Carnivora(x, y, velocidade=velocidade) # Passando velocidade para Planta_Carnivora também
        elif tipo_inimigo.lower() == 'espantalho':
             novo_inimigo = Espantalho(x, y, velocidade=velocidade) # Passando velocidade para Espantalho
        elif tipo_inimigo.lower() == 'fenix':
             novo_inimigo = Fenix(x, y, velocidade=velocidade)
        # Adiciona a criação da Mãe Natureza
        elif tipo_inimigo.lower() == 'maenatureza':
             novo_inimigo = Mae_Natureza(x, y, velocidade=velocidade)
        # NOVO: Adiciona a criação do Espirito_Das_Flores
        elif tipo_inimigo.lower() == 'espiritodasflores':
             novo_inimigo = Espirito_Das_Flores(x, y, velocidade=velocidade)
        else:
            pass # Não faz nada si o tipo for desconhecido

        if novo_inimigo:
            self.adicionar_inimigo(novo_inimigo) # Adiciona o inimigo criado à lista
        return novo_inimigo

    # CORRIGIDO: Agora aceita 'estacao' e 'jogador' como argumentos
    def spawn_inimigos(self, estacao, jogador):
        """
        Spawna inimigos com base na estação (para spawns imediatos, ex: mudança de estação).

        Args:
            estacao (int ou str): A estação atual (0-3 ou nome).
            jogador (Player): O objeto jogador para determinar a área de spawn.
        """
        # Obtém o nome da estação a partir do argumento 'estacao'
        # Verifica si self.estacoes existe e tem o método nome_estacao para converter o índice, se necessário
        if isinstance(estacao, int) and self.estacoes is not None and hasattr(self.estacoes, 'nome_estacao'):
             est_nome = self.estacoes.nome_estacao().lower()
        elif isinstance(estacao, str):
             est_nome = estacao.lower()
        else:
             return # Sai da função si a estação não puder ser determinada


        # Lista de tipos de inimigos disponíveis para spawn nesta estação
        tipos_disponiveis = []

        # Adiciona tipos de inimigos com base na estação (usando nomes em minúsculas)
        if est_nome == "inverno":
            # Adiciona classes de inimigos à lista
            tipos_disponiveis.append('fantasma')
            tipos_disponiveis.append('bonecodeneve')
        # Lógica para a Primavera
        elif est_nome == "primavera":
            tipos_disponiveis.append('planta_carnivora')
            # Adiciona Mãe Natureza à lista de spawns da primavera
            tipos_disponiveis.append('maenatureza')
            # NOVO: Adiciona Espirito_Das_Flores à lista de spawns da primavera
            tipos_disponiveis.append('espiritodasflores')


        # Lógica para o Outono (Espantalho)
        elif est_nome == "outono": # Verifica si o nome da estação (em minúsculas) é 'outono'
            tipos_disponiveis.append('espantalho')
            # Adicione outros inimigos de outono aqui
        # Lógica para o Verão (Fênix)
        elif est_nome == "verão":
            tipos_disponiveis.append('fenix')


        # Spawna inimigos apenas si houver tipos disponíveis E si não atingiu o limite
        if tipos_disponiveis and len(self.inimigos) < self.limite_inimigos:
             # Spawna a quantidade definida para spawns iniciais (ou menos, si o limite for próximo)
             num_to_spawn = min(self.spawns_iniciais, self.limite_inimigos - len(self.inimigos))


             for _ in range(num_to_spawn):
                # Escolhe um tipo de inimigo aleatoriamente entre os disponíveis para esta estação
                tipo = random.choice(tipos_disponiveis)

                # Calcula uma posição de spawn aleatória ao redor do jogador
                # Garante que o spawn aconteça fora da área visível imediata
                spawn_distance = random.randint(300, 600) # Distância mínima e máxima do jogador
                angle = random.uniform(0, 2 * math.pi) # Ângulo aleatório em radianos

                # Adiciona verificação para garantir que o jogador tem o atributo rect
                if hasattr(jogador, 'rect'):
                     x = jogador.rect.centerx + spawn_distance * math.cos(angle)
                     y = jogador.rect.centery + spawn_distance * math.sin(angle)
                     # Cria o inimigo usando o método criar_inimigo_aleatorio
                     self.criar_inimigo_aleatorio(tipo, x, y) # O método já adiciona à lista


    # Implementa lógica de spawn exponencial
    def tentar_spawnar(self, estacao, jogador): # CORRIGIDO: Agora aceita 'estacao' como argumento
        """
        Verifica si é hora de spawnar novos inimigos periodicamente e os spawna.
        O intervalo de spawn diminui exponencialmente com o tempo de jogo.

        Args:
            estacao (int ou str): A estação atual.
            jogador (Player): O objeto jogador.
        """
        agora = time.time()
        tempo_decorrido = agora - self.tempo_inicial_jogo # Tempo desde o início do jogo

        # Calcula o intervalo de spawn atual usando uma função exponencial decrescente
        # O intervalo diminui com o tempo, mas não vai abaixo de intervalo_spawn_minimo
        intervalo_atual = max(self.intervalo_spawn_minimo, self.intervalo_spawn_inicial * math.exp(-self.fator_exponencial_spawn * tempo_decorrido))


        # Verifica si o intervalo de spawn atual passou desde o último spawn E si não atingiu o limite
        if agora - self.ultimo_spawn >= intervalo_atual and len(self.inimigos) < self.limite_inimigos:
            # Chama a função de spawn periódico (que já tem a verificação interna do limite)
            # Passa a estação obtida de self.estacoes
            # Verifica si self.estacoes existe e tem o método nome_estacao
            if self.estacoes is not None and hasattr(self.estacoes, 'nome_estacao'):
                 # CHAMADA CORRETA DO MÉTODO INTERNO
                 self.spawn_inimigo_periodico(self.estacoes.nome_estacao(), jogador) # Passa o nome da estação
                 self.ultimo_spawn = agora # Atualiza o tempo do último spawn


    # MÉTODO spawn_inimigo_periodico DEFINIDO AQUI
    def spawn_inimigo_periodico(self, estacao_nome, jogador):
             """
             Spawna um único inimigo periodicamente.
             Recebe o nome da estação como string.
             """

             est_nome = estacao_nome.lower() # Converte o nome da estação para minúsculas

             tipos_disponiveis = []

             # Adiciona tipos de inimigos com base na estação para spawn periódico (usando nomes em minúsculas)
             if est_nome == "inverno":
                 tipos_disponiveis.append('fantasma')
                 tipos_disponiveis.append('bonecodeneve')
             # Lógica para a Primavera (spawn periódico)
             elif est_nome == "primavera":
                 tipos_disponiveis.append('planta_carnivora')
                 # Adiciona Mãe Natureza à lista de spawns periódicos da primavera
                 tipos_disponiveis.append('maenatureza')
                 # NOVO: Adiciona Espirito_Das_Flores à lista de spawns periódicos da primavera
                 tipos_disponiveis.append('espiritodasflores')


             # Spawna 1 inimigo si houver tipos disponíveis e não atingiu o limite
             if tipos_disponiveis and len(self.inimigos) < self.limite_inimigos:
                  tipo = random.choice(tipos_disponiveis)

                  spawn_distance = random.randint(300, 600) # Distância mínima e máxima do jogador
                  angle = random.uniform(0, 2 * math.pi) # Ângulo aleatório em radianos

                  # Adiciona verificação para garantir que o jogador tem o atributo rect
                  if hasattr(jogador, 'rect'):
                       x = jogador.rect.centerx + spawn_distance * math.cos(angle)
                       y = jogador.rect.centery + spawn_distance * math.sin(angle)
                       # Cria o inimigo usando o método criar_inimigo_aleatorio
                       self.criar_inimigo_aleatorio(tipo, x, y) # O método já adiciona à lista


    # Modificado: Agora aceita a lista de árvores como argumento
    def update_inimigos(self, jogador, arvores):
        """
        Atualiza o estado de todos os inimigos ativos (movimento, ataque, vida).
        Passa a lista de projéteis e as dimensões da tela para o update dos inimigos.

        Args:
            jogador (Player): O objeto jogador para que os inimigos possam segui-lo e atacá-lo.
            arvores (list): Uma lista de objetos Arvore para colisão.
        """
        inimigos_vivos = [] # Lista temporária para os inimigos que sobreviveram à atualização

        # Itera sobre uma cópia da lista de inimigos para evitar problemas si um inimigo for removido durante a iteração
        for inimigo in list(self.inimigos): # Usa list() para criar uma cópia e permitir remoção segura
            # Verifica si o inimigo está vivo antes de atualizá-lo
            if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo():
                # Chama o método update do inimigo, passando o objeto jogador E os novos argumentos
                # Adiciona verificação para garantir que o inimigo tem o método update
                if hasattr(inimigo, 'update'):
                    # Passa os argumentos adicionais (lista de projéteis, largura e altura da tela, E ARVORES)
                    # Adapte as chamadas de update aqui para cada tipo de inimigo si necessário,
                    # garantindo que 'arvores' seja passado se o método update do inimigo o espera.
                    # O método update na classe base Inimigo AGORA espera 'player' e 'arvores'.
                    # As classes derivadas devem sobrescrever update e chamar super().update(player, arvores)
                    # ou passar 'arvores' para self.mover_em_direcao diretamente.

                    # Exemplo para BonecoDeNeve que pode precisar de mais argumentos:
                    if isinstance(inimigo, BonecoDeNeve):
                         # Se o update do BonecoDeNeve precisa de projéteis e dimensões da tela:
                         inimigo.update(jogador, arvores, self.projeteis_inimigos, self.tela_largura, self.altura_tela)
                    # Exemplo para outros inimigos que usam o update base ou um update que espera 'player' e 'arvores':
                    elif hasattr(inimigo, 'update'): # Verifica novamente para garantir que o método existe após os isinstance checks
                         # Chama o update passando player e arvores
                         inimigo.update(jogador, arvores)


                    inimigos_vivos.append(inimigo) # Adiciona o inimigo vivo à lista temporária
            elif hasattr(inimigo, 'hp') and inimigo.hp <= 0:
                 # Si o inimigo tem HP e morreu (HP <= 0)
                 # Não adicionamos à lista inimigos_vivos, efetivamente removendo-o
                 pass # Não imprime a cada frame si o limite for atingido, para evitar poluir a consola
            elif not hasattr(inimigo, 'esta_vivo') and not hasattr(inimigo, 'hp'):
                 # Si o inimigo não tem método esta_vivo nem atributo hp, não podemos verificar si está vivo/morto
                 # Mantém na lista de vivos por padrão, mas pode causar problemas si não tiver lógica de remoção
                 inimigos_vivos.append(inimigo)


        # Substitui a lista de inimigos pela lista de inimigos vivos
        self.inimigos = inimigos_vivos

    def update_projeteis_inimigos(self, jogador):
        """
        Atualiza todos os projéteis lançados pelos inimigos.
        """
        # Use uma cópia da lista para iterar, permitindo remoção segura durante a iteração
        for projetil in list(self.projeteis_inimigos):
            # Verifica si o objeto é um projétil válido e tem o método update
            if hasattr(projetil, 'update'):
                 # O método update do ProjetilNeve espera: player, tela_largura, altura_tela
                 # Adapte os argumentos si você tiver outros tipos de projéteis com updates diferentes
                 if isinstance(projetil, ProjetilNeve): # Verifica se é um ProjetilNeve
                      projetil.update(jogador, self.tela_largura, self.altura_tela)
                      # A lógica de remoção (projetil.kill() ou verificação de self.atingiu/vida útil)
                      # deve estar dentro do método update do ProjetilNeve.
                      # Se estiver usando grupos, o kill() já remove. Se for só lista,
                      # a iteração sobre a cópia e a remoção da lista original é necessária.
                      # Verificamos se o sprite ainda "existe" após o update (se não foi kill()ed)
                      if not projetil.alive(): # Exemplo se estiver usando grupos e kill()
                           if projetil in self.projeteis_inimigos: # Verifica se ainda está na lista antes de tentar remover
                                self.projeteis_inimigos.remove(projetil)
                 else:
                      # Para outros tipos de projéteis, chame o update com os argumentos que eles esperam
                      # Exemplo: projetil.update(jogador)
                      pass # Adicione lógica para outros tipos de projéteis aqui


    def desenhar_inimigos(self, janela, camera_x: int, camera_y: int):
        """
        Desenha todos os inimigos ativos na janela, aplicando o offset da câmera.

        Args:
            janela (pygame.Surface): A superfície onde desenhar.
            camera_x (int): O offset x da câmera.
            camera_y (int): O offset y da câmera.
        """
        for inimigo in self.inimigos:
            # Desenha o inimigo apenas si ele estiver vivo
            if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo():
                # Adiciona verificação para garantir que o inimigo tem o método desenhar
                if hasattr(inimigo, 'desenhar'):
                    inimigo.desenhar(janela, camera_x, camera_y)
            # Si o inimigo não tem esta_vivo, tentamos desenhar assim mesmo (pode ser um placeholder)
            elif not hasattr(inimigo, 'esta_vivo') and hasattr(inimigo, 'desenhar'):
                 inimigo.desenhar(janela, camera_x, camera_y)

    def desenhar_projeteis_inimigos(self, surface, camera_x, camera_y):
        """
        Desenha todos os projéteis ativos dos inimigos na superfície, aplicando o offset da câmera.

        Args:
            surface (pygame.Surface): A superfície onde desenhar.
            camera_x (int): O offset x da câmera.
            camera_y (int): O offset y da câmera.
        """
        # Use uma cópia da lista para iterar e desenhar
        for projetil in list(self.projeteis_inimigos): # Use list() para iterar sobre uma cópia
             # Verifica se o objeto é um projétil válido e tem o método desenhar
             if hasattr(projetil, 'desenhar'):
                  projetil.desenhar(surface, camera_x, camera_y)


    def get_inimigos_vivos(self):
        """Retorna a lista de inimigos vivos."""
        return [inimigo for inimigo in self.inimigos if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo()]

    def limpar_inimigos(self):
        """Remove todos os inimigos ativos da lista."""
        self.inimigos.clear()
        self.projeteis_inimigos.clear() # Limpa também a lista de projéteis

