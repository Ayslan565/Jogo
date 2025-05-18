# GerenciadorDeInimigos.py
import pygame
import random
import time
import math # Importa math para a função hypot e exp
import os # Importa os para verificar a existência de arquivos

# Importa a classe base Inimigo do ficheiro Inimigos.py
# Certifique-se de que o ficheiro Inimigos.py está na mesma pasta ou num caminho acessível
try:
    from Inimigos import Inimigo
    print("DEBUG(GerenciadorDeInimigos): Classe base Inimigo importada com sucesso.")
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): ERRO: Módulo 'Inimigos.py' ou classe 'Inimigo' NÃO encontrado. O jogo pode não funcionar corretamente sem a classe base Inimigo.")
    # Não define um placeholder aqui, pois a intenção é remover o placeholder.
    # O código dependerá da importação bem-sucedida de Inimigos.py.
    Inimigo = None # Define como None para que as verificações 'is not None' funcionem.


# Importa as classes necessárias (mantido try-except para robustez)
try:
    from Estacoes import Estacoes
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Estacoes.py' ou classe 'Estacoes' não encontrado.")
    Estacoes = None

try:
    from Fantasma import Fantasma
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Fantasma.py' ou classe 'Fantasma' não encontrado.")
    Fantasma = None

try:
    from BonecoDeNeve import BonecoDeNeve
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'BonecoDeNeve.py' ou classe 'BonecoDeNeve' não encontrado.")
    BonecoDeNeve = None

try:
    from Planta_Carnivora import Planta_Carnivora
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Planta_Carnivora.py' ou classe 'Planta_Carnivora' não encontrado.")
    Planta_Carnivora = None

try:
    from Espantalho import Espantalho
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Espantalho.py' ou classe 'Espantalho' não encontrado.")
    Espantalho = None

try:
    from Fenix import Fenix
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Fenix.py' ou classe 'Fenix' não encontrado.")
    Fenix = None

# Importa a classe de inimigo da Primavera: Mãe Natureza
try:
    from Mae_Natureza import Mae_Natureza
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Mae_Natureza.py' ou classe 'Mae_Natureza' não encontrado.")
    Mae_Natureza = None # Define como None se a importação falhar

# NOVO: Importa a classe de inimigo da Primavera: Espirito_Das_Flores
try:
    from Espirito_Das_Flores import Espirito_Das_Flores
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Espirito_Das_Flores.py' ou classe 'Espirito_Das_Flores' não encontrado.")
    Espirito_Das_Flores = None # Define como None se a importação falhar


# Importa a classe de projétil (necessária para gerenciar projéteis)
try:
    from Projetil_BolaNeve import ProjetilNeve
except ImportError:
    print("DEBUG(GerenciadorDeInimigos): Aviso: Módulo 'Projetil_BolaNeve.py' ou classe 'ProjetilNeve' não encontrado.")
    ProjetilNeve = None


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

        print("DEBUG(GerenciadorDeInimigos): Gerenciador de Inimigos inicializado com objeto Estacoes, spawn exponencial e gerenciamento de projéteis.") # Debug inicialização
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
            tipo_inimigo (str): O tipo de inimigo a criar ('fantasma', 'bonecodeneve', 'planta_carnivora', 'espantalho', 'fenix', 'maenatureza', 'espiritodasflores'). # Adicionado espiritodasflores
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
        elif tipo_inimigo.lower() == 'fenix' and Fenix is not None:
             novo_inimigo = Fenix(x, y, velocidade=velocidade)
             # print(f"DEBUG(GerenciadorDeInimigos): Criado nova Fenix em ({int(x)}, {int(y)}).") # Debug criação
        # Adiciona a criação da Mãe Natureza
        elif tipo_inimigo.lower() == 'maenatureza' and Mae_Natureza is not None:
             novo_inimigo = Mae_Natureza(x, y, velocidade=velocidade)
             print(f"DEBUG(GerenciadorDeInimigos): Criado nova Mãe Natureza em ({int(x)}, {int(y)}).") # Debug criação
        # NOVO: Adiciona a criação do Espirito_Das_Flores
        elif tipo_inimigo.lower() == 'espiritodasflores' and Espirito_Das_Flores is not None:
             novo_inimigo = Espirito_Das_Flores(x, y, velocidade=velocidade)
             print(f"DEBUG(GerenciadorDeInimigos): Criado novo Espirito das Flores em ({int(x)}, {int(y)}).") # Debug criação
        else:
            # print(f"DEBUG(GerenciadorDeInimigos): Tipo de inimigo desconhecido ou classe não importada: {tipo_inimigo}") # Debug erro
            pass # Não faz nada si o tipo for desconhecido ou a classe não foi importada

        if novo_inimigo:
            self.adicionar_inimigo(novo_inimigo) # Adiciona o inimigo criado à lista
        return novo_inimigo

    # Não recebe mais 'estacao' como argumento, usa self.estacoes
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

        # ADICIONADO: Print para depuração
        print(f"DEBUG(GerenciadorDeInimigos): spawn_inimigos chamado para estação: {est_nome}")

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
            # Adiciona Mãe Natureza à lista de spawns da primavera
            if Mae_Natureza is not None:
                 tipos_disponiveis.append('maenatureza')
                 print("DEBUG(GerenciadorDeInimigos): 'maenatureza' adicionado aos tipos disponíveis para spawn inicial (Primavera).") # Debug específico da primavera
            # NOVO: Adiciona Espirito_Das_Flores à lista de spawns da primavera
            if Espirito_Das_Flores is not None:
                 tipos_disponiveis.append('espiritodasflores')
                 print("DEBUG(GerenciadorDeInimigos): 'espiritodasflores' adicionado aos tipos disponíveis para spawn inicial (Primavera).") # Debug específico da primavera


        # Lógica para o Outono (Espantalho)
        elif est_nome == "outono": # Verifica si o nome da estação (em minúsculas) é 'outono'
            if Espantalho is not None: # Verifica si a classe Espantalho foi importada
                 tipos_disponiveis.append('espantalho')
            # Adicione outros inimigos de outono aqui
        # Lógica para o Verão (Fênix)
        elif est_nome == "verão":
            if Fenix is not None:
                 tipos_disponiveis.append('fenix')
                 print("DEBUG(GerenciadorDeInimigos): 'fenix' adicionado aos tipos disponíveis para spawn inicial (Verão).") # Debug específico do verão


        # Spawna inimigos apenas si houver tipos disponíveis E si não atingiu o limite
        if tipos_disponiveis and len(self.inimigos) < self.limite_inimigos:
             # Spawna a quantidade definida para spawns iniciais (ou menos, si o limite for próximo)
             num_to_spawn = min(self.spawns_iniciais, self.limite_inimigos - len(self.inimigos))

             print(f"DEBUG(GerenciadorDeInimigos): Tentando spawnar {num_to_spawn} inimigos para a estação '{est_nome}'. Tipos disponíveis: {tipos_disponiveis}") # Debug spawn inicial

             for _ in range(num_to_spawn):
                # Escolhe um tipo de inimigo aleatoriamente entre os disponíveis para esta estação
                tipo = random.choice(tipos_disponiveis)
                print(f"DEBUG(GerenciadorDeInimigos): Tipo de inimigo escolhido para spawn inicial: {tipo}") # Debug tipo escolhido

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
             print(f"DEBUG(GerenciadorDeInimigos): Aviso: Nenhum tipo de inimigo disponível para spawn inicial na estação '{est_nome}'.") # Opcional: para depuração
             pass # Não faz nada si não houver inimigos para spawnar nesta estação
        else:
             print(f"DEBUG(GerenciadorDeInimigos): Limite de inimigos ({self.limite_inimigos}) atingido ({len(self.inimigos)}). Não foi possível spawnar mais inimigos.") # Debug limite atingido


    # Implementa lógica de spawn exponencial
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
                 # CHAMADA CORRETA DO MÉTODO INTERNO
                 # ADICIONADO: Print para depuração
                 print(f"DEBUG(GerenciadorDeInimigos): tentar_spawnar acionado para estação: {self.estacoes.nome_estacao().lower()}")
                 self.spawn_inimigo_periodico(self.estacoes.nome_estacao(), jogador) # Passa o nome da estação
                 self.ultimo_spawn = agora # Atualiza o tempo do último spawn
            else:
                 print("DEBUG(GerenciadorDeInimigos): Aviso: Objeto Estacoes não disponível ou não tem nome_estacao(). Não foi possível tentar spawn periódico.")

        # elif len(self.inimigos) >= self.limite_inimigos:
             # print(f"DEBUG(GerenciadorDeInimigos): Limite de inimigos ({self.limite_inimigos}) atingido. Não foi possível tentar spawn periódico.") # Debug limite atingido
             # pass # Não imprime a cada frame si o limite for atingido, para evitar poluir a consola


    # MÉTODO spawn_inimigo_periodico DEFINIDO AQUI
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
                 # Adiciona Mãe Natureza à lista de spawns periódicos da primavera
                 if Mae_Natureza is not None:
                      tipos_disponiveis.append('maenatureza')
                      print("DEBUG(GerenciadorDeInimigos): 'maenatureza' adicionado aos tipos disponíveis para spawn periódico (Primavera).") # Debug específico da primavera
                 # NOVO: Adiciona Espirito_Das_Flores à lista de spawns periódicos da primavera
                 if Espirito_Das_Flores is not None:
                      tipos_disponiveis.append('espiritodasflores')
                      print("DEBUG(GerenciadorDeInimigos): 'espiritodasflores' adicionado aos tipos disponíveis para spawn periódico (Primavera).") # Debug específico da primavera


             # Spawna 1 inimigo si houver tipos disponíveis e não atingiu o limite
             if tipos_disponiveis and len(self.inimigos) < self.limite_inimigos:
                  tipo = random.choice(tipos_disponiveis)
                  print(f"DEBUG(GerenciadorDeInimigos): Tipo de inimigo escolhido para spawn periódico: {tipo}") # Debug tipo escolhido

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
                  print(f"DEBUG(GerenciadorDeInimigos): Aviso: Nenhum tipo de inimigo disponível para spawn periódico na estação '{est_nome}'.") # Opcional: para depuração
                  pass # Não faz nada si não houver inimigos para spawnar nesta estação
             else:
                  print(f"DEBUG(GerenciadorDeInimigos): Limite de inimigos ({self.limite_inimigos}) atingido ({len(self.inimigos)}). Não foi possível tentar spawn periódico.") # Debug limite atingido


    def update_inimigos(self, jogador):
        """
        Atualiza o estado de todos os inimigos ativos (movimento, ataque, vida).
        Passa a lista de projéteis e as dimensões da tela para o update dos inimigos.

        Args:
            jogador (Player): O objeto jogador para que os inimigos possam segui-lo e atacá-lo.
        """
        # print("DEBUG(GerenciadorDeInimigos): Método update_inimigos chamado.") # Debug update geral
        inimigos_vivos = [] # Lista temporária para os inimigos que sobreviveram à atualização

        # Itera sobre uma cópia da lista de inimigos para evitar problemas si um inimigo for removido durante a iteração
        for inimigo in list(self.inimigos): # Usa list() para criar uma cópia e permitir remoção segura
            # print(f"DEBUG(GerenciadorDeInimigos): Atualizando inimigo: {type(inimigo).__name__}") # Debug por inimigo
            # Verifica si o inimigo está vivo antes de atualizá-lo
            if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo():
                # Chama o método update do inimigo, passando o objeto jogador E os novos argumentos
                # Adiciona verificação para garantir que o inimigo tem o método update
                if hasattr(inimigo, 'update'):
                    # Passa os argumentos adicionais (lista de projéteis, largura e altura da tela)
                    # O BonecoDeNeve espera estes argumentos no seu método update.
                    # Outros inimigos podem precisar de argumentos diferentes ou nenhum.
                    # Adapte as chamadas de update aqui para cada tipo de inimigo si necessário.
                    if isinstance(inimigo, BonecoDeNeve):
                        inimigo.update(jogador, self.projeteis_inimigos, self.tela_largura, self.altura_tela)
                    # Chama o update para Mãe Natureza (assumindo que ele só precisa do jogador)
                    elif isinstance(inimigo, Mae_Natureza):
                         inimigo.update(jogador) # Adapte os argumentos se o update da Mãe Natureza precisar de mais coisas
                    # Chama o update para Planta Carnívora (assumindo que ele só precisa do jogador)
                    elif isinstance(inimigo, Planta_Carnivora):
                         inimigo.update(jogador) # Adapte os argumentos se o update da Planta Carnívora precisar de mais coisas
                    # NOVO: Chama o update para Espirito_Das_Flores (assumindo que ele só precisa do jogador)
                    elif isinstance(inimigo, Espirito_Das_Flores):
                         inimigo.update(jogador) # Adapte os argumentos se o update do Espirito_Das_Flores precisar de mais coisas
                    else:
                        # Para outros tipos de inimigos, chame o update com os argumentos que eles esperam
                        # O padrão é apenas o jogador
                        inimigo.update(jogador)


                    inimigos_vivos.append(inimigo) # Adiciona o inimigo vivo à lista temporária
                else:
                    print(f"DEBUG(GerenciadorDeInimigos): Aviso: Inimigo do tipo {type(inimigo).__name__} não tem método 'update'.") # Debug aviso
            elif hasattr(inimigo, 'hp') and inimigo.hp <= 0:
                 # Si o inimigo tem HP e morreu (HP <= 0)
                 # print(f"DEBUG(GerenciadorDeInimigos): Removendo inimigo morto (HP <= 0): {type(inimigo).__name__}") # Debug remoção de morto
                 # Não adicionamos à lista inimigos_vivos, efetivamente removendo-o
                 pass # Não imprime a cada frame si o limite for atingido, para evitar poluir a consola
            elif not hasattr(inimigo, 'esta_vivo') and not hasattr(inimigo, 'hp'):
                 # Si o inimigo não tem método esta_vivo nem atributo hp, não podemos verificar si está vivo/morto
                 print(f"DEBUG(GerenciadorDeInimigos): Aviso: Inimigo do tipo {type(inimigo).__name__} não tem método 'esta_vivo' nem atributo 'hp'. Não é possível verificar si está vivo.") # Debug aviso
                 # Mantém na lista de vivos por padrão, mas pode causar problemas si não tiver lógica de remoção
                 inimigos_vivos.append(inimigo)


        # Substitui a lista de inimigos pela lista de inimigos vivos
        self.inimigos = inimigos_vivos
        # print(f"DEBUG(GerenciadorDeInimigos): Fim do update_inimigos. Total de inimigos vivos: {len(self.inimigos)}") # Debug final do update

    def update_projeteis_inimigos(self, jogador):
        """
        Atualiza todos os projéteis lançados pelos inimigos.
        """
        # Use uma cópia da lista para iterar, permitindo remoção segura durante a iteração
        for projetil in list(self.projeteis_inimigos):
            # Verifica se o objeto é um projétil válido e tem o método update
            if hasattr(projetil, 'update'):
                 # O método update do ProjetilNeve espera: player, tela_largura, altura_tela
                 # Adapte os argumentos se você tiver outros tipos de projéteis com updates diferentes
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

            else:
                 # Se o objeto na lista não for um projétil válido ou não tiver update, remova-o
                 if projetil in self.projeteis_inimigos:
                      self.projeteis_inimigos.remove(projetil)
                      print("DEBUG(GerenciadorDeInimigos): Aviso: Objeto inválido encontrado na lista de projéteis. Removido.")


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
             # else:
                  # print("DEBUG(GerenciadorDeInimigos): Aviso: Objeto na lista de projéteis não tem método 'desenhar'.") # Debug aviso


    def get_inimigos_vivos(self):
        """Retorna a lista de inimigos vivos."""
        return [inimigo for inimigo in self.inimigos if hasattr(inimigo, 'esta_vivo') and inimigo.esta_vivo()]

    def limpar_inimigos(self):
        """Remove todos os inimigos ativos da lista."""
        # print("DEBUG(GerenciadorDeInimigos): Limpando lista de inimigos.") # Debug
        self.inimigos.clear()
        self.projeteis_inimigos.clear() # Limpa também a lista de projéteis


# No seu loop principal do jogo, você chamaria algo assim:
# gerenciador_inimigos = GerenciadorDeInimigos(estacoes_obj, TELA_LARGURA, altura_tela, ...) # Passe as dimensões da tela aqui
# ...
# gerenciador_inimigos.update_inimigos(jogador)
# gerenciador_inimigos.update_projeteis_inimigos(jogador) # Chame o update dos projéteis
# ...
# gerenciador_inimigos.desenhar_inimigos(janela, camera_x, camera_y)
# gerenciador_inimigos.desenhar_projeteis_inimigos(janela, camera_x, camera_y) # Desenhe os projéteis
