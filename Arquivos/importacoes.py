# Arquivo: importacoes.py
# Este arquivo centraliza as importações comuns para o jogo.
# print("DEBUG(importacoes): Módulo importacoes.py carregado.")

import pygame
import random
import math
import os
import time
import threading
# import tkinter as tk # Removido pois Roda_Armas (Tkinter) não é mais usado

# --- Módulos do Pygame e Utilitários Padrão ---
# Já importados acima

# --- Módulos do Jogo (geralmente na pasta 'Arquivos') ---
try:
    from vida import Vida
except ImportError:
    print("AVISO(importacoes): Módulo 'vida.py' ou classe 'Vida' não encontrado.")
    Vida = None

try:
    from player import Player
except ImportError:
    print("ERRO CRÍTICO(importacoes): Módulo 'player.py' ou classe 'Player' não encontrado.")
    Player = None

try:
    # Se inventario_barra.py está na mesma pasta que importacoes.py (Arquivos)
    from inventario_barra import BarraInventario, ItemInventario
except ImportError:
    print("AVISO(importacoes): Falha ao importar BarraInventario ou ItemInventario de 'inventario_barra.py'.")
    BarraInventario = None
    ItemInventario = None

try:
    from Pause import PauseMenuManager
except ImportError:
    print("AVISO(importacoes): Módulo 'Pause.py' ou classe 'PauseMenuManager' não encontrado.")
    PauseMenuManager = None

try:
    from xp_manager import XPManager
except ImportError:
    print("AVISO(importacoes): Módulo 'xp_manager.py' ou classe 'XPManager' não encontrado.")
    XPManager = None

try:
    from Menu import Menu
except ImportError:
    print("AVISO(importacoes): Módulo 'Menu.py' ou classe 'Menu' não encontrado.")
    Menu = None

try:
    from GerenciadorDeInimigos import GerenciadorDeInimigos
except ImportError:
    print("AVISO(importacoes): Módulo 'GerenciadorDeInimigos.py' ou classe 'GerenciadorDeInimigos' não encontrado.")
    GerenciadorDeInimigos = None

try:
    from Estacoes import Estacoes
except ImportError:
    print("AVISO(importacoes): Módulo 'Estacoes.py' ou classe 'Estacoes' não encontrado.")
    Estacoes = None

try:
    from grama import Grama
except ImportError:
    print("AVISO(importacoes): Módulo 'grama.py' ou classe 'Grama' não encontrado.")
    Grama = None

try:
    from arvores import Arvore
except ImportError:
    print("AVISO(importacoes): Módulo 'arvores.py' ou classe 'Arvore' não encontrado.")
    Arvore = None

try:
    from timer1 import Timer
except ImportError:
    print("AVISO(importacoes): Módulo 'timer1.py' ou classe 'Timer' não encontrado.")
    Timer = None

try:
    import shop_elements
except ImportError:
    print("AVISO(importacoes): Módulo 'shop_elements.py' não encontrado.")
    shop_elements = None

try:
    from death_screen import run_death_screen
except ImportError:
    print("AVISO(importacoes): Módulo 'death_screen.py' ou função 'run_death_screen' não encontrado.")
    run_death_screen = None

try:
    import loja as loja_core # Para a UI da loja
except ImportError:
    print("ERRO CRÍTICO(importacoes): Módulo 'loja.py' (para loja_core) não encontrado.")
    loja_core = None

try:
    import Luta_boss # Módulo para lutas contra chefes
except ImportError:
    print("AVISO(importacoes): Módulo 'Luta_boss.py' não encontrado.")
    Luta_boss = None

# --- Adicionada Importação do GerenciadorMoedas ---
# Assumindo que gerenciador_moedas.py está na mesma pasta que importacoes.py (Jogo/Arquivos/)
try:
    from .gerenciador_moedas import GerenciadorMoedas
except ImportError:
    # Fallback se a importação relativa falhar (ex: executando importacoes.py diretamente)
    try:
        from gerenciador_moedas import GerenciadorMoedas
    except ImportError:
        print("AVISO(importacoes): Módulo 'gerenciador_moedas.py' ou classe 'GerenciadorMoedas' não encontrado.")
        GerenciadorMoedas = None


# --- Classes Base de Armas ---
# Assumindo que importacoes.py está em Jogo/Arquivos/
# e a pasta Armas está em Jogo/Armas/ (um nível acima e depois para Armas)
try:
    from .Armas.weapon import Weapon
except ImportError:
    # Fallback para caso a estrutura seja Jogo/Arquivos/Armas/
    try:
        from .Armas.weapon import Weapon
    except ImportError:
        print("AVISO(importacoes): 'Armas/weapon.py' ou classe 'Weapon' não encontrada.")
        Weapon = None


# --- Classes de Armas Específicas ---
# Assumindo que os arquivos das armas estão em Jogo/Armas/
# Portanto, de Jogo/Arquivos/importacoes.py, o caminho relativo é ..Armas.NomeDoArquivo
try: from .Armas.AdagaFogo import AdagaFogo
except ImportError: AdagaFogo = None; # print("AVISO(importacoes): AdagaFogo não encontrada.")
try: from .Armas.EspadaBrasas import EspadaBrasas
except ImportError: EspadaBrasas = None; # print("AVISO(importacoes): EspadaBrasas não encontrada.")
try: from .Armas.EspadaCaida import EspadaCaida
except ImportError: EspadaCaida = None; # print("AVISO(importacoes): EspadaCaida não encontrada.")
try: from .Armas.EspadaFogoAzul import EspadaFogoAzul
except ImportError: EspadaFogoAzul = None; # print("AVISO(importacoes): EspadaFogoAzul não encontrada.")
try: from .Armas.EspadaLua import EspadaLua
except ImportError: EspadaLua = None; # print("AVISO(importacoes): EspadaLua não encontrada.")
try: from .Armas.EspadaPenitencia import EspadaPenitencia
except ImportError: EspadaPenitencia = None; # print("AVISO(importacoes): EspadaPenitencia não encontrada.")
try: from .Armas.EspadaSacraDasBrasas import EspadaSacraDasBrasas
except ImportError: EspadaSacraDasBrasas = None; # print("AVISO(importacoes): EspadaSacraDasBrasas não encontrada.")
try: from .Armas.EspadaSacraCerulea import EspadaSacraCerulea
except ImportError: EspadaSacraCerulea = None; # print("AVISO(importacoes): EspadaSacraCerulea não encontrada.")

try: from .Armas.LaminaCeuCinti import LaminaDoCeuCentilhante
except ImportError: LaminaDoCeuCentilhante = None; # print("AVISO(importacoes): LaminaDoCeuCentilhante não encontrada.")

try: from .Armas.MachadoBase import MachadoBase
except ImportError: MachadoBase = None; # print("AVISO(importacoes): MachadoBase não encontrado.")
try: from .Armas.MachadoBarbaro import MachadoBarbaro
except ImportError: MachadoBarbaro = None; # print("AVISO(importacoes): MachadoBarbaro não encontrado.")
try: from .Armas.MachadoCeruleo import MachadoCeruleo
except ImportError: MachadoCeruleo = None; # print("AVISO(importacoes): MachadoCeruleo não encontrado.")
try: from .Armas.Machado_Santa import MachadoDaDescidaSanta
except ImportError: MachadoDaDescidaSanta = None; # print("AVISO(importacoes): MachadoDaDescidaSanta não encontrado.")
try: from .Armas.MachadoAbrasa import MachadoDoFogoAbrasador
except ImportError: MachadoDoFogoAbrasador = None; # print("AVISO(importacoes): MachadoDoFogoAbrasador não encontrado.")
try: from .Armas.MachadoMarfim import MachadoMarfim
except ImportError: MachadoMarfim = None; # print("AVISO(importacoes): MachadoMarfim não encontrado.")
try: from .Armas.MachadoMacabro import MachadoMacabro
except ImportError: MachadoMacabro = None; # print("AVISO(importacoes): MachadoMacabro não encontrado.")


# print("AVISO(importacoes): Fim do carregamento do módulo importacoes.py.")
