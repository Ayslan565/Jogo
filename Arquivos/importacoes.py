
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
    from inventario_barra import *
    if BarraInventario is None: # Checagem adicional pós-importação bem-sucedida (sintaticamente)
        print("AVISO(importacoes): BarraInventario foi importado como None de 'inventario_barra.py'. Verifique o arquivo 'inventario_barra.py' por erros internos.")
except ImportError as e_ib:
    print(f"AVISO(importacoes): Falha ao importar BarraInventario ou ItemInventario de 'inventario_barra.py'. Erro específico: {e_ib}")
    import traceback
    traceback.print_exc() # Imprime o traceback completo do ImportError
    BarraInventario = None
    ItemInventario = None
except Exception as e_geral_ib: # Captura outros erros que não sejam ImportError
    print(f"ERRO GERAL(importacoes): ao tentar importar de 'inventario_barra.py': {e_geral_ib}")
    import traceback
    traceback.print_exc()
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

try:
    from .gerenciador_moedas import GerenciadorMoedas
except ImportError:
    try:
        from gerenciador_moedas import GerenciadorMoedas
    except ImportError:
        print("AVISO(importacoes): Módulo 'gerenciador_moedas.py' ou classe 'GerenciadorMoedas' não encontrado.")
        GerenciadorMoedas = None


# --- Classes Base de Armas ---
try:
    from .Armas.weapon import Weapon
except ImportError:
    try:
        from Armas.weapon import Weapon # Tentativa de importação se a estrutura for Jogo/Armas
    except ImportError:
        print("AVISO(importacoes): 'Armas/weapon.py' ou classe 'Weapon' não encontrada.")
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
