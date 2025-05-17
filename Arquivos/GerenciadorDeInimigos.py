# GerenciadorDeInimigos.py
import pygame
import random
import time
import math # Importa math para a função hypot e exp
import os # Importa os para verificar a existência de arquivos

# Importa a classe Estacoes
try:
    from Estacoes import Estacoes
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Estacoes.py' ou classe 'Estacoes' não encontrado.")
    Estacoes = None # Define como None para evitar NameError

# Importa as classes de inimigos
# Certifique-se de que os nomes dos arquivos correspondem
try:
    from Fantasma import Fantasma # Assumindo que a classe se chama Fantasma e o arquivo Fantasma.py
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Fantasma.py' ou classe 'Fantasma' não encontrado.")
    Fantasma = None # Define como None para evitar NameError

try:
    from BonecoDeNeve import BonecoDeNeve # Assumindo que a classe se chama BonecoDeNeve e o arquivo BonecoDeNeve.py
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'BonecoDeNeve.py' ou classe 'BonecoDeNeve' não encontrado.")
    BonecoDeNeve = None # Define como None para evitar NameError

try:
    from Planta_Carnivora import Planta_Carnivora # Assumindo que a classe se chama Planta_Carnivora e o arquivo Planta_Carnivora.py
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Planta_Carnivora.py' ou classe 'Planta_Carnivora' não encontrado.")
    Planta_Carnivora = None # Define como None para evitar NameError

try:
    from Espantalho import Espantalho # Assumindo que a classe se chama Espantalho e o arquivo Espantalho.py
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Espantalho.py' ou classe 'Espantalho' não encontrado.")
    Espantalho = None # Define como None para evitar NameError

try:
    from Fenix import Fenix # Assumindo que a classe se chama Fenix e o arquivo Fenix.py
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Fenix.py' ou classe 'Fenix' não encontrado.")
    Fenix = None # Define como None para evitar NameError


class GerenciadorDeInimigos:
    """
    Classe responsável por gerenciar todos os inimigos no jogo.
    Lida com a criação, atualização e remoção de inimigos.
    """
    # Modificado: Recebe uma instância de Estacoes e adiciona parâmetros para spawn exponencial
    def __init__(self, estacoes_obj, intervalo_spawn_inicial: float = 3.0, spawns_iniciais: int = 5, limite_inimigos: int = 150, fator_exponencial_spawn: float = 0.02, intervalo_spawn_minimo: float = 0.5):
        """
        Inicializa o gerenciador de inimigos com spawn exponencial.

        Args:
            estacoes_obj (Estacoes): Uma instância da classe Estacoes.
            intervalo_spawn_inicial (float): Tempo inicial em segundos entre os spawns periódicos.
            spawns_iniciais (int): Número de inimigos a spawnar imediatamente em certas condições.
            limite_inimigos (int): O número máximo de inimigos permitidos na tela.
            fator_exponencial_spawn (float): Controla a rapidez com que o intervalo de spawn diminui. Um valor maior significa spawn mais rápido.
            intervalo_spawn_minimo (float): O menor intervalo de spawn permitido.
        """
        self.estacoes = estacoes_obj # Armazena a instância de Estacoes
        self.inimigos = [] # Lista para armazenar todas as instâncias de inimigos
        self.ultimo_spawn = time.time() # Tempo do último spawn para controle do intervalo
        self.intervalo_spawn_inicial = intervalo_spawn_inicial # Intervalo inicial entre spawns periódicos
        self.spawns_iniciais = spawns_iniciais # Quantidade de spawns iniciais
        self.limite_inimigos = limite_inimigos # Novo: Limite máximo de inimigos

        # Adicionados para spawn exponencial
        self.tempo_inicial_jogo = time.time() # Registra o tempo de início do jogo
        self.fator_exponencial_spawn = fator_exponencial_spawn # Fator para o crescimento exponencial
        self.intervalo_spawn_minimo = intervalo_spawn_minimo # Intervalo mínimo para evitar spawns instantâneos

        print("DEBUG(GerenciadorDeInimigos): Gerenciador de Inimigos inicializado com objeto Estacoes e spawn exponencial.") # Debug inicialização
        print(f"DEBUG(GerenciadorDeInimigos): Configurações: Intervalo Spawn Inicial={self.intervalo_spawn_inicial}s, Spawns Iniciais={self.spawns_iniciais}, Limite={self.limite_inimigos}, Fator Exponencial={self.fator_exponencial_spawn}, Intervalo Mínimo={self.intervalo_spawn_minimo}s") # Debug configurações


    def adicionar_inimigo(self, inimigo):
        """
        Adiciona uma instância de inimigo à lista de inimigos gerenciados.

        Args:
            inimigo (Inimigo): A instância do inimigo a ser adicionada.
        """
        self.inimigos.append(inimigo)
        # print(f"DEBUG(GerenciadorDeInimigos): Inimigo adicionado à lista. Total: {len(self.inimigos)}") # Debug adição

    def remover_inimigo(self, inimigo):
        """
        Remove uma instância de inimigo da lista de inimigos gerenciados.

        Args:
            inimigo (Inimigo): A instância do inimigo a ser removida.
        """
        if inimigo in self.inimigos:
            self.inimigos.remove(inimigo)
            # print(f"DEBUG(GerenciadorDeInimigos): Inimigo removido da lista. Total: {len(self.inimigos)}") # Debug remoção

    def criar_inimigo_aleatorio(self, tipo_inimigo, x, y, velocidade=1.0):
        """
        Cria uma nova instância de um tipo de inimigo especificado em uma posição.

        Args:
            tipo_inimigo (str): O tipo de inimigo a criar ('fantasma', 'bonecodeneve', 'planta_carnivora', 'espantalho', 'fenix').
            x (int): A posição x onde o inimigo será criado.
            y (int): A posição y onde o inimigo será criado.
            velocidade (float): A velocidade do inimigo (opcional, padrão 1.0).

        Returns:
            Inimigo or None: A instância do inimigo criado, ou None si o tipo for inválido.
        """
        novo_inimigo = None
        if tipo_inimigo.lower() == 'fantasma' and Fantasma is not None:
            novo_inimigo = Fantasma(x, y, velocidade=velocidade)
            # print(f"DEBUG(GerenciadorDeInimigos): Criado novo Fantasma em ({int(x)}, {int(y)}).") # Debug criação
        elif tipo_inimigo.lower() == 'bonecodeneve' and BonecoDeNeve is not None:
            novo_inimigo = BonecoDeNeve(x, y, velocidade=velocidade)
            # print(f"DEBUG(GerenciadorDeInimigos): Criado novo Boneco de Neve em ({int(x)}, {int(y)}).") # Debug criação
        elif tipo_inimigo.lower() == 'planta_carnivora' and Planta_Carnivora is not None:
             novo_inimigo = Planta_Carnivora(x, y, velocidade=velocidade) # Passando velocidade para Planta_Carnivora também
             # print(f"DEBUG(GerenciadorDeInimigos): Criado nova Planta Carnivora em ({int(x)}, {int(y)}).") # Debug criação
        elif tipo_inimigo.lower() == 'espantalho' and Espantalho is not None:
             novo_inimigo = Espantalho(x, y, velocidade=velocidade) # Passando velocidade para Espantalho
             # print(f"DEBUG(GerenciadorDeInimigos): Criado novo Espantalho em ({int(x)}, {int(y)}).") # Debug criação
        elif tipo_inimigo.lower() == 'fenix' and Fenix is not None: # Adicionado check para Fenix
             novo_inimigo = Fenix(x, y, velocidade=velocidade)
             # print(f"DEBUG(GerenciadorDeInimigos): Criado nova Fenix em ({int(x)}, {int(y)}).") # Debug criação
        else:
            # print(f"DEBUG(GerenciadorDeInimigos): Tipo de inimigo desconhecido ou classe não importada: {tipo_inimigo}") # Debug erro
            pass # Não faz nada si o tipo for desconhecido ou a classe não foi importada

        if novo_inimigo:
            self.adicionar_inimigo(novo_inimigo) # Adiciona o inimigo criado à lista
        return novo_inimigo

    # Modificado: Não recebe mais 'estacao' como argumento, usa self.estacoes
    def spawn_inimigos(self, jogador):
        """
        Spawna inimigos com base na estação atual (obtida de self.estacoes).
        Esta função é chamada para spawns imediatos (ex: mudança de estação).

        Args:
            jogador (Player): O objeto jogador para determinar a área de spawn.
        """
        # Obtém o nome da estação diretamente do objeto Estacoes
        # Verifica si self.estacoes existe e tem o método nome_estacao
        if self.estacoes is None or not hasattr(self.estacoes, 'nome_estacao'):
             print("DEBUG(GerenciadorDeInimigos): Aviso: Objeto Estacoes não disponível ou não tem nome_estacao(). Não foi possível spawnar inimigos.")
             return # Sai da função si o objeto Estacoes não estiver configurado

        est_nome = self.estacoes.nome_estacao().lower() # Obtém o nome e converte para minúsculas

        # Lista de tipos de inimigos disponíveis para spawn nesta estação
        tipos_disponiveis = []

        # Adiciona tipos de inimigos com base na estação (usando nomes em minúsculas)
        if est_nome == "inverno":
            # Adiciona classes de inimigos à lista APENAS si elas foram importadas com sucesso
            if Fantasma is not None:
                 tipos_disponiveis.append('fantasma')
            if BonecoDeNeve is not None:
                 tipos_disponiveis.append('bonecodeneve')
        # Lógica para a Primavera
        elif est_nome == "primavera":
            if Planta_Carnivora is not None:
                 tipos_disponiveis.append('planta_carnivora')
            # Você pode adicionar outros inimigos que spawnem na primavera aqui
        # Lógica para o Outono (Espantalho)
        elif est_nome == "outono": # Verifica si o nome da estação (em minúsculas) é 'outono'
            if Espantalho is not None: # Verifica si a classe Espantalho foi importada
                  tipos_disponiveis.append('espantalho')
            # Adicione outros inimigos de outono aqui
        # Lógica para o Verão (Fênix) - ADICIONADO
        elif est_nome == "verao":
            if Fenix is not None: # Verifica si a classe Fenix foi importada
                  tipos_disponiveis.append('fenix') # Adiciona 'fenix' à lista


        # Spawna inimigos apenas si houver tipos disponíveis E si não atingiu o limite
        if tipos_disponiveis and len(self.inimigos) < self.limite_inimigos:
             # Spawna a quantidade definida para spawns iniciais (ou menos, si o limite for próximo)
             num_to_spawn = min(self.spawns_iniciais, self.limite_inimigos - len(self.inimigos))

             print(f"DEBUG(GerenciadorDeInimigos): Tentando spawnar {num_to_spawn} inimigos para a estação '{est_nome}'. Tipos disponíveis: {tipos_disponiveis}") # Debug spawn inicial

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
                else:
                     print("DEBUG(GerenciadorDeInimigos): Aviso: Jogador não tem atributo 'rect'. Não foi possível determinar posição de spawn.")


        elif not tipos_disponiveis:
             # print(f"DEBUG(GerenciadorDeInimigos): Aviso: Nenhum tipo de inimigo disponível para spawn inicial na estação '{est_nome}'.") # Opcional: para depuração
             pass # Não faz nada si não houver inimigos para spawnar nesta estação
        else:
             print(f"DEBUG(GerenciadorDeInimigos): Limite de inimigos ({self.limite_inimigos}) atingido. Não foi possível spawnar mais inimigos.") # Debug limite atingido


    # Modificado: Implementa lógica de spawn exponencial
    def tentar_spawnar(self, jogador):
        """
        Verifica si é hora de spawnar novos inimigos periodicamente e os spawna.
        O intervalo de spawn diminui exponencialmente com o tempo de jogo.

        Args:
            jogador (Player): O objeto jogador.
        """
        agora = time.time()
        tempo_decorrido = agora - self.tempo_inicial_jogo # Tempo desde o início do jogo

        # Calcula o intervalo de spawn atual usando uma função exponencial decrescente
        # O intervalo diminui com o tempo, mas não vai abaixo de intervalo_spawn_minimo
        intervalo_atual = max(self.intervalo_spawn_minimo, self.intervalo_spawn_inicial * math.exp(-self.fator_exponencial_spawn * tempo_decorrido))

        # print(f"DEBUG(GerenciadorDeInimigos): Tempo decorrido: {tempo_decorrido:.2f}s, Intervalo de spawn atual: {intervalo_atual:.2f}s") # Debug do intervalo

        # Verifica si o intervalo de spawn atual passou desde o último spawn E si não atingiu o limite
        if agora - self.ultimo_spawn >= intervalo_atual and len(self.inimigos) < self.limite_inimigos:
            # Chama a função de spawn periódico (que já tem a verificação interna do limite)
            # Passa a estação obtida de self.estacoes
            # Verifica si self.estacoes existe e tem o método nome_estacao
            if self.estacoes is not None and hasattr(self.estacoes, 'nome_estacao'):
                 # >>> CHAMADA CORRETA DO MÉTODO INTERNO <<<
                 self.spawn_inimigo_periodico(self.estacoes.nome_estacao(), jogador) # Passa o nome da estação
                 self.ultimo_spawn = agora # Atualiza o tempo do último spawn
            else:
                 print("DEBUG(GerenciadorDeInimigos): Aviso: Objeto Estacoes não disponível ou não tem nome_estacao(). Não foi possível tentar spawn periódico.")

        elif len(self.inimigos) >= self.limite_inimigos:
             # print(f"DEBUG(GerenciadorDeInimigos): Limite de inimigos ({self.limite_inimigos}) atingido. Não foi possível tentar spawn periódico.") # Debug limite atingido
             pass # Não imprime a cada frame si o limite for atingido, para evitar poluir a consola

    # >>> MÉTODO spawn_inimigo_periodico DEFINIDO AQUI <<<
    def spawn_inimigo_periodico(self, estacao_nome, jogador):
            """
            Spawna um único inimigo periodicamente.
            Recebe o nome da estação como string.
            """
            # print(f"DEBUG(GerenciadorDeInimigos): Chamado spawn_inimigo_periodico para estação: {estacao_nome}") # Debug: Confirma si a função é chamada

            est_nome = estacao_nome.lower() # Converte o nome da estação para minúsculas

            tipos_disponiveis = []

            # Adiciona tipos de inimigos com base na estação para spawn periódico (usando nomes em minúsculas)
            if est_nome == "inverno":
                if Fantasma is not None:
                     tipos_disponiveis.append('fantasma')
                if BonecoDeNeve is not None:
                     tipos_disponiveis.append('bonecodeneve')
            # Lógica para a Primavera (spawn periódico)
            elif est_nome == "primavera":
                if Planta_Carnivora is not None:
                     tipos_disponiveis.append('planta_carnivora')
                # Adicione outros inimigos de primavera para spawn periódico aqui
            # Lógica para o Outono (Espantalho) - Spawn Periódico
            elif est_nome == "outono":
                if Espantalho is not None:
                     tipos_disponiveis.append('espantalho')
                # Adicione outros inimigos de outono para spawn periódico aqui
            # Lógica para o Verão (Fênix) - ADICIONADO
            elif est_nome == "verao":
                if Fenix is not None: # Verifica si a classe Fenix foi importada
                     tipos_disponiveis.append('fenix') # Adiciona 'fenix' à lista


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
                     # print(f"DEBUG(GerenciadorDeInimigos): Spawned periodic {tipo} at ({int(x)}, {int(y)})") # Debug spawn periódico
                 else:
                     print("DEBUG(GerenciadorDeInimigos): Aviso: Jogador não tem atributo 'rect'. Não foi possível determinar posição de spawn para spawn periódico.")

            elif not tipos_disponiveis:
                 # print(f"DEBUG(GerenciadorDeInimigos): Aviso: Nenhum tipo de inimigo disponível para spawn periódico na estação '{est_nome}'.") # Opcional: para depuração
                 pass # Não faz nada si não houver inimigos para spawnar nesta estação


    def update_inimigos(self, jogador):
        """
        Atualiza o estado de todos os inimigos ativos (movimento, ataque, vida).

        Args:
            jogador (Player): O objeto jogador para que os inimigos possam segui-lo e atacá-lo.
        """
        # print("DEBUG(GerenciadorDeInimigos): Método update_inimigos chamado.") # Debug update geral
        inimigos_vivos = [] # Lista temporária para os inimigos que sobreviveram à atualização

        # Itera sobre a lista de inimigos
        for inimigo in list(self.inimigos): # Usa list() para criar uma cópia e permitir remoção segura
            # print(f"DEBUG(GerenciadorDeInimigos): Atualizando inimigo: {type(inimigo).__name__}") # Debug por inimigo
            # Verifica si o inimigo está vivo antes de atualizá-lo
            if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo():
                # Chama o método update do inimigo, passando o objeto jogador
                # Adiciona verificação para garantir que o inimigo tem o método update
                if hasattr(inimigo, 'update'):
                    inimigo.update(jogador)
                    inimigos_vivos.append(inimigo) # Adiciona o inimigo vivo à lista temporária
                else:
                    print(f"DEBUG(GerenciadorDeInimigos): Aviso: Inimigo do tipo {type(inimigo).__name__} não tem método 'update'.") # Debug aviso
            elif hasattr(inimigo, 'hp') and inimigo.hp <= 0:
                 # Si o inimigo tem HP e morreu (HP <= 0)
                 # print(f"DEBUG(GerenciadorDeInimigos): Removendo inimigo morto (HP <= 0): {type(inimigo).__name__}") # Debug remoção de morto
                 # Não adicionamos à lista inimigos_vivos, efetivamente removendo-o
                 pass # Não imprime a cada remoção para evitar poluir a consola
            elif not hasattr(inimigo, 'esta_vivo') and not hasattr(inimigo, 'hp'):
                 # Si o inimigo não tem método esta_vivo nem atributo hp, não podemos verificar si está vivo/morto
                 print(f"DEBUG(GerenciadorDeInimigos): Aviso: Inimigo do tipo {type(inimigo).__name__} não tem método 'esta_vivo' nem atributo 'hp'. Não é possível verificar si está vivo.") # Debug aviso
                 # Mantém na lista de vivos por padrão, mas pode causar problemas si não tiver lógica de remoção
                 inimigos_vivos.append(inimigo)


        # Substitui a lista de inimigos pela lista de inimigos vivos
        self.inimigos = inimigos_vivos
        # print(f"DEBUG(GerenciadorDeInimigos): Fim do update_inimigos. Total de inimigos vivos: {len(self.inimigos)}") # Debug final do update

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
                else:
                    print(f"DEBUG(GerenciadorDeInimigos): Aviso: Inimigo do tipo {type(inimigo).__name__} não tem método 'desenhar'.") # Debug aviso
            # Si o inimigo não tem esta_vivo, tentamos desenhar assim mesmo (pode ser um placeholder)
            elif not hasattr(inimigo, 'esta_vivo') and hasattr(inimigo, 'desenhar'):
                 print(f"DEBUG(GerenciadorDeInimigos): Aviso: Inimigo do tipo {type(inimigo).__name__} não tem método 'esta_vivo', mas tem 'desenhar'. Tentando desenhar.") # Debug aviso
                 inimigo.desenhar(janela, camera_x, camera_y)


    def get_inimigos_vivos(self):
        """Retorna a lista de inimigos vivos."""
        return [inimigo for inimigo in self.inimigos if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo()]

    def limpar_inimigos(self):
        """Remove todos os inimigos ativos da lista."""
        # print("DEBUG(GerenciadorDeInimigos): Limpando lista de inimigos.") # Debug
        self.inimigos.clear()
