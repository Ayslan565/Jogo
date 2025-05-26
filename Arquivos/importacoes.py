# Arquivo: importacoes.py
# Este arquivo centraliza as importações comuns para o jogo.
# DEBUG: Confirmando que importacoes.py está sendo carregado
print("DEBUG(importacoes): Módulo importacoes.py carregado.")

import pygame
import random
import math
import os
import time 
import threading # Usado por GerenciadorDeInimigos e potencialmente outras UIs
# import tkinter as tk # Não é mais necessário se Roda_Armas (Tkinter) foi removida

# --- Classes Base e Utilitários ---
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

# --- Classes de Armas Específicas ---
# Adicione todas as suas classes de armas aqui
try: from Armas.AdagaFogo import AdagaFogo
except ImportError: AdagaFogo = None; print("DEBUG(importacoes): AdagaFogo não encontrada.")
try: from Armas.EspadaBrasas import EspadaBrasas
except ImportError: EspadaBrasas = None; print("DEBUG(importacoes): EspadaBrasas não encontrada.")
try: from Armas.EspadaCaida import EspadaCaida
except ImportError: EspadaCaida = None; print("DEBUG(importacoes): EspadaCaida não encontrada.")
try: from Armas.EspadaFogoAzul import EspadaFogoAzul
except ImportError: EspadaFogoAzul = None; print("DEBUG(importacoes): EspadaFogoAzul não encontrada.")
try: from Armas.EspadaLua import EspadaLua
except ImportError: EspadaLua = None; print("DEBUG(importacoes): EspadaLua não encontrada.")
try: from Armas.EspadaPenitencia import EspadaPenitencia
except ImportError: EspadaPenitencia = None; print("DEBUG(importacoes): EspadaPenitencia não encontrada.")
# Exemplo: from Armas.EspadaSacraDasBrasas import EspadaSacraDasBrasas
try: from Armas.MachadoBarbaro import MachadoBarbaro
except ImportError: MachadoBarbaro = None; print("DEBUG(importacoes): MachadoBarbaro não encontrado.")
try: from Armas.MachadoCeruleo import MachadoCeruleo
except ImportError: MachadoCeruleo = None; print("DEBUG(importacoes): MachadoCeruleo não encontrado.")
try: from Armas.MachadoMacabro import MachadoMacabro
except ImportError: MachadoMacabro = None; print("DEBUG(importacoes): MachadoMacabro não encontrado.")
try: from Armas.MachadoMarfim import MachadoMarfim
except ImportError: MachadoMarfim = None; print("DEBUG(importacoes): MachadoMarfim não encontrado.")
# Exemplo: from Armas.MachadoCeruleoDaEstrelaCadente import MachadoCeruleoDaEstrelaCadente

# --- Módulos de UI e Jogo ---
try:
    from player import Player 
except ImportError:
    print("DEBUG(importacoes): ERRO CRÍTICO: Módulo 'player.py' ou classe 'Player' não encontrado.")
    Player = None

# REMOVIDO: WeaponWheelUI (Tkinter)
# try:
#     from Roda_Armas import WeaponWheelUI
# except ImportError:
#     print("DEBUG(importacoes): Aviso: Módulo 'Roda_Armas.py' ou classe 'WeaponWheelUI' não encontrado.")
#     WeaponWheelUI = None

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

try:
    from GerenciadorDeInimigos import GerenciadorDeInimigos
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'GerenciadorDeInimigos.py' ou classe 'GerenciadorDeInimigos' não encontrado.")
    GerenciadorDeInimigos = None

try:
    from Estacoes import Estacoes
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'Estacoes.py' ou classe 'Estacoes' não encontrado.")
    Estacoes = None

try:
    from grama import Grama
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'grama.py' ou classe 'Grama' não encontrado.")
    Grama = None

try:
    from arvores import Arvore
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'arvores.py' ou classe 'Arvore' não encontrado.")
    Arvore = None

try:
    from timer1 import Timer # Assumindo que o nome do arquivo é timer1.py
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'timer1.py' ou classe 'Timer' não encontrado.")
    Timer = None

try:
    import shop_elements 
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'shop_elements.py' não encontrado.")
    shop_elements = None

try:
    from death_screen import run_death_screen
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'death_screen.py' ou função 'run_death_screen' não encontrado.")
    run_death_screen = None

# --- MODIFICADO: Importação da UI da Loja ---
try:
    import loja as loja_core # Importa o módulo loja.py (que você disse conter a UI da loja)
                            # e o apelida de loja_core, para ser usado em Game.py
except ImportError:
    print("DEBUG(importacoes): ERRO CRÍTICO: Módulo 'loja.py' (para loja_core) não encontrado.")
    loja_core = None

# A importação anterior de run_shop_scene de Spawn_Loja.py foi removida,
# assumindo que Spawn_Loja.py é para constantes de spawn e não para a UI completa.
# Se Spawn_Loja.py realmente tiver a função run_shop_scene da UI, esta lógica precisará ser ajustada.

# --- ADICIONADO: Importação da Barra de Inventário ---
try:
    from inventario_barra import BarraInventario # ItemInventario não parece ser usado diretamente pelo Game.py
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'inventario_barra.py' ou classe 'BarraInventario' não encontrado.")
    BarraInventario = None
    # ItemInventario = None # Se ItemInventario fosse necessário externamente, manteria.

# --- Classes de Inimigos Específicos (movidas para GerenciadorDeInimigos.py, mas podem ser listadas aqui se necessário em outros lugares) ---
# Geralmente, é melhor que o GerenciadorDeInimigos lide com suas próprias importações de tipos de inimigos.
# try: from Fantasma import Fantasma
# except ImportError: Fantasma = None; print("DEBUG(importacoes): Fantasma não encontrado.")
# ... e assim por diante para outros inimigos ...

print("DEBUG(importacoes): Fim do carregamento do módulo importacoes.py.")
