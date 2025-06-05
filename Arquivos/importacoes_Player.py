# Arquivo: importacoes_Player.py
# Destinado a centralizar as importações necessárias para a classe Player.
# Principalmente Vida, a classe base Weapon, e todas as classes de armas específicas.

import pygame # Pygame pode ser útil para tipos ou inicializações, embora não diretamente para imports.
import os # Para manipulação de caminhos, se necessário em contextos mais complexos.

# --- Importação da Classe Vida ---
try:
    # Assumindo que vida.py está na mesma pasta (Arquivos) que importacoes_Player.py
    from .vida import Vida
except ImportError:
    print("ALERTA(importacoes_Player): Módulo 'vida.py' ou classe 'Vida' não encontrado.")
    Vida = None

# --- Importação da Classe Base Weapon ---
# Assumindo que importacoes_Player.py está em Jogo/Arquivos/
# e weapon.py está em Jogo/Arquivos/Armas/
try:
    from .Armas.weapon import Weapon
except ImportError as e:
    print(f"ALERTA(importacoes_Player): Falha ao importar 'Weapon' de '.Armas.weapon': {e}. Verifique o caminho.")
    # Fallback tentando um caminho diferente se a estrutura for Jogo/Armas/
    try:
        from .Armas.weapon import Weapon # Se Armas está um nível acima de Arquivos
        print("INFO(importacoes_Player): 'Weapon' importada de '..Armas.weapon' como fallback.")
    except ImportError:
        print("ERRO CRÍTICO(importacoes_Player): Classe 'Weapon' não encontrada. Funcionalidade de armas comprometida.")
        Weapon = None

# --- Importação das Classes de Armas Específicas ---
# Todas devem estar na pasta Armas, que é uma subpasta de Arquivos,
# ou em Jogo/Armas/ se o fallback acima para Weapon foi usado.

# Adagas
try:
    from .Armas.AdagaFogo import AdagaFogo
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.AdagaFogo' não encontrada.")
    AdagaFogo = None

# Espadas
try:
    from .Armas.EspadaBrasas import EspadaBrasas
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.EspadaBrasas' não encontrada.")
    EspadaBrasas = None
try:
    from .Armas.EspadaCaida import EspadaCaida
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.EspadaCaida' não encontrada.")
    EspadaCaida = None
try:
    from .Armas.EspadaFogoAzul import EspadaFogoAzul
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.EspadaFogoAzul' não encontrada.")
    EspadaFogoAzul = None
try:
    from .Armas.EspadaLua import EspadaLua
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.EspadaLua' não encontrada.")
    EspadaLua = None
try:
    from .Armas.EspadaPenitencia import EspadaPenitencia
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.EspadaPenitencia' não encontrada.")
    EspadaPenitencia = None
try:
    from .Armas.EspadaSacraDasBrasas import EspadaSacraDasBrasas
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.EspadaSacraDasBrasas' não encontrada.")
    EspadaSacraDasBrasas = None
try:
    from .Armas.EspadaSacraCerulea import EspadaSacraCerulea
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.EspadaSacraCerulea' não encontrada.")
    EspadaSacraCerulea = None


# Lâminas
try:
    # Assumindo que o nome da classe é LaminaDoCeuCentilhante e o arquivo LaminaCeuCinti.py
    from .Armas.LaminaCeuCinti import LaminaDoCeuCentilhante
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.LaminaCeuCinti' ou classe 'LaminaDoCeuCentilhante' não encontrada.")
    LaminaDoCeuCentilhante = None

# Machados
try:
    from .Armas.MachadoBase import MachadoBase
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.MachadoBase' não encontrado.")
    MachadoBase = None
try:
    from .Armas.MachadoBarbaro import MachadoBarbaro
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.MachadoBarbaro' não encontrado.")
    MachadoBarbaro = None
try:
    from .Armas.MachadoCeruleo import MachadoCeruleo
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.MachadoCeruleo' não encontrado.")
    MachadoCeruleo = None
try:
    # Assumindo que o nome da classe é MachadoDaDescidaSanta e o arquivo Machado_Santa.py
    from .Armas.Machado_Santa import MachadoDaDescidaSanta
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.Machado_Santa' ou classe 'MachadoDaDescidaSanta' não encontrada.")
    MachadoDaDescidaSanta = None
try:
    # Assumindo que o nome da classe é MachadoDoFogoAbrasador e o arquivo MachadoAbrasa.py
    from .Armas.MachadoAbrasa import MachadoDoFogoAbrasador
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.MachadoAbrasa' ou classe 'MachadoDoFogoAbrasador' não encontrada.")
    MachadoDoFogoAbrasador = None
try:
    from .Armas.MachadoMarfim import MachadoMarfim
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.MachadoMarfim' não encontrado.")
    MachadoMarfim = None
try:
    from .Armas.MachadoMacabro import MachadoMacabro
except ImportError:
    # print("ALERTA(importacoes_Player): '.Armas.MachadoMacabro' não encontrado.")
    MachadoMacabro = None

# Adicione aqui outras classes de armas que você possa ter, seguindo o mesmo padrão.
# Exemplo para Cajados (se existirem e forem armas):
# try:
#     from .Armas.CajadoDaFixacaoAmetista import CajadoDaFixacaoAmetista
# except ImportError:
#     # print("ALERTA(importacoes_Player): '.Armas.CajadoDaFixacaoAmetista' não encontrado.")
#     CajadoDaFixacaoAmetista = None

# print("INFO(importacoes_Player): Módulo importacoes_Player.py carregado.")
