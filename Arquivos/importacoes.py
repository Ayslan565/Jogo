
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
    Vida = None

try:
    from player import Player
except ImportError:
    Player = None

try:
    # Se inventario_barra.py está na mesma pasta que importacoes.py (Arquivos)
    from inventario_barra import *
    if BarraInventario is None: # Checagem adicional pós-importação bem-sucedida (sintaticamente)
        BarraInventario = None
        ItemInventario = None
except ImportError:
    BarraInventario = None
    ItemInventario = None


try:
    from Pause import PauseMenuManager
except ImportError:
    PauseMenuManager = None

try:
    from xp_manager import XPManager
except ImportError:
    XPManager = None

try:
    from Menu import Menu
except ImportError:
    Menu = None

try:
    from GerenciadorDeInimigos import GerenciadorDeInimigos
except ImportError:
    GerenciadorDeInimigos = None

try:
    from Estacoes import Estacoes
except ImportError:
    Estacoes = None

try:
    from grama import Grama
except ImportError:
    Grama = None

try:
    from arvores import Arvore
except ImportError:
    Arvore = None

try:
    from timer1 import Timer
except ImportError:
    Timer = None

try:
    import shop_elements
except ImportError:
    shop_elements = None

try:
    from death_screen import run_death_screen
except ImportError:
    run_death_screen = None

try:
    import loja as loja_core # Para a UI da loja
except ImportError:
    loja_core = None

try:
    import Luta_boss # Módulo para lutas contra chefes
except ImportError:
    Luta_boss = None

try:
    from .gerenciador_moedas import GerenciadorMoedas
except ImportError:
    try:
        from gerenciador_moedas import GerenciadorMoedas
    except ImportError:
        GerenciadorMoedas = None


# --- Classes Base de Armas ---
try:
    from .Armas.weapon import Weapon
except ImportError:
    try:
        from Armas.weapon import Weapon # Tentativa de importação se a estrutura for Jogo/Armas
    except ImportError:
        Weapon = None


# --- Classes de Armas Específicas ---
try: from .Armas.AdagaFogo import AdagaFogo
except ImportError: AdagaFogo = None
try: from .Armas.EspadaBrasas import EspadaBrasas
except ImportError: EspadaBrasas = None
try: from .Armas.EspadaCaida import EspadaCaida
except ImportError: EspadaCaida = None
try: from .Armas.EspadaFogoAzul import EspadaFogoAzul
except ImportError: EspadaFogoAzul = None
try: from .Armas.EspadaLua import EspadaLua
except ImportError: EspadaLua = None
try: from .Armas.EspadaPenitencia import EspadaPenitencia
except ImportError: EspadaPenitencia = None
try: from .Armas.EspadaSacraDasBrasas import EspadaSacraDasBrasas
except ImportError: EspadaSacraDasBrasas = None
try: from .Armas.EspadaSacraCerulea import EspadaSacraCerulea
except ImportError: EspadaSacraCerulea = None

try: from .Armas.LaminaCeuCinti import LaminaDoCeuCintilante
except ImportError: LaminaDoCeuCintilante = None

try: from .Armas.MachadoBase import MachadoBase
except ImportError: MachadoBase = None
try: from .Armas.MachadoBarbaro import MachadoBarbaro
except ImportError: MachadoBarbaro = None
try: from .Armas.MachadoCeruleo import MachadoCeruleo
except ImportError: MachadoCeruleo = None
try: from .Armas.Machado_Santa import MachadoDaDescidaSanta
except ImportError: MachadoDaDescidaSanta = None
try: from .Armas.MachadoAbrasa import MachadoDoFogoAbrasador
except ImportError: MachadoDoFogoAbrasador = None
try: from .Armas.MachadoMarfim import MachadoMarfim
except ImportError: MachadoMarfim = None
try: from .Armas.MachadoMacabro import MachadoMacabro
except ImportError: MachadoMacabro = None

