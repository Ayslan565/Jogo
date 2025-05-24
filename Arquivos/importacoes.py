# Arquivo: importacoes.py
# Este arquivo centraliza as importações comuns para o jogo.

# Bibliotecas padrão e Pygame
import pygame
import random
import time
import sys
import os
import threading
import math

# --- Módulos e Classes do Jogo ---

# Classes base e utilidades
try:
    from vida import Vida
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'vida.py' ou classe 'Vida' não encontrado.")
    Vida = None

try:
    from Armas.weapon import Weapon
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'Armas/weapon.py' ou classe 'Weapon' não encontrado.")
    Weapon = None

# Classes de Armas Específicas
# Adicione todas as suas classes de armas aqui
try: from Armas.EspadaBrasas import EspadaBrasas
except ImportError: EspadaBrasas = None
try: from Armas.MachadoCeruleo import MachadoCeruleo
except ImportError: MachadoCeruleo = None
try: from Armas.MachadoMacabro import MachadoMacabro
except ImportError: MachadoMacabro = None
try: from Armas.MachadoMarfim import MachadoMarfim
except ImportError: MachadoMarfim = None
try: from Armas.MachadoBarbaro import MachadoBarbaro
except ImportError: MachadoBarbaro = None
try: from Armas.AdagaFogo import AdagaFogo
except ImportError: AdagaFogo = None
try: from Armas.EspadaFogoAzul import EspadaFogoAzul
except ImportError: EspadaFogoAzul = None
try: from Armas.EspadaLua import EspadaLua
except ImportError: EspadaLua = None
try: from Armas.EspadaCaida import EspadaCaida
except ImportError: EspadaCaida = None
try: from Armas.EspadaPenitencia import EspadaPenitencia
except ImportError: EspadaPenitencia = None
# Exemplo para futuras armas:
# try: from Armas.NomeDaSuaArma import NomeDaSuaArma
# except ImportError: NomeDaSuaArma = None

# Componentes de UI e Gerenciamento de Jogo
try:
    from Roda_Armas import WeaponWheelUI
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'Roda_Armas.py' ou classe 'WeaponWheelUI' não encontrado.")
    WeaponWheelUI = None

try:
    from Pause import PauseMenuManager
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'Pause.py' ou classe 'PauseMenuManager' não encontrado.")
    PauseMenuManager = None

try:
    from xp_manager import XPManager
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'xp_manager.py' ou classe 'XPManager' não encontrado.")
    XPManager = None

try:
    from Menu import Menu
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'Menu.py' ou classe 'Menu' não encontrado.")
    Menu = None

# Elementos do Mundo do Jogo e Gerenciadores de Entidades
try:
    from GerenciadorDeInimigos import GerenciadorDeInimigos
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'GerenciadorDeInimigos.py' não encontrado.")
    GerenciadorDeInimigos = None

try:
    from Estacoes import Estacoes
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'Estacoes.py' não encontrado.")
    Estacoes = None

try:
    from grama import Grama
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'grama.py' não encontrado.")
    Grama = None

try:
    from arvores import Arvore
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'arvores.py' não encontrado.")
    Arvore = None

try:
    from timer1 import Timer # Assumindo que timer1.py contém a classe Timer
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'timer1.py' ou classe 'Timer' não encontrado.")
    Timer = None

# Módulos da Loja e Telas Especiais
try:
    import shop_elements # Importa o módulo inteiro para acesso às suas funções e variáveis globais
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'shop_elements.py' não encontrado.")
    shop_elements = None

try:
    from death_screen import run_death_screen # Importa a função específica
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'death_screen.py' ou função 'run_death_screen' não encontrado.")
    run_death_screen = None

try:
    import loja as loja_core # Importa o módulo da loja (loja_core.py) como um alias
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'loja.py' (loja_core) não encontrado.")
    loja_core = None

# NOTA IMPORTANTE SOBRE Player:
# A classe 'Player' não é importada aqui para evitar dependências circulares.
# Se 'player.py' também for usar este arquivo 'importacoes.py', importar 'Player' aqui
# criaria um problema.
# O seu arquivo principal (ex: Game.py) deve continuar importando 'Player' diretamente:
# from player import Player
