# Arquivo: importacoes.py
# Este arquivo centraliza as importações comuns para o jogo.

import pygame
import random
import math
import os
import time
import threading # Adicionado para threading.Event em Roda_Armas
import tkinter as tk # Adicionado para tk.TclError em Roda_Armas

# --- Módulos do Jogo (no diretório Jogo/) ---
try:
    from vida import Vida
except ImportError:
    print("DEBUG(importacoes): 'vida.py' ou classe 'Vida' não encontrada.")
    Vida = None

try:
    # inventario_barra.py is in Jogo/ according to the image
    # The original "from inventario_barra import *" should make these available.
    # If this specific named import fails, check inventario_barra.py for internal errors
    # or ensure the classes BarraInventario and ItemInventario are correctly defined there.
    from inventario_barra import BarraInventario, ItemInventario
except ImportError:
    print("DEBUG(importacoes): Falha ao importar BarraInventario, ItemInventario de 'inventario_barra.py'.")
    BarraInventario = None
    ItemInventario = None

# --- Classes Base de Armas ---
try:
    from Armas.weapon import Weapon # weapon.py is in Jogo/Armas/
except ImportError:
    print("DEBUG(importacoes): 'Armas/weapon.py' ou classe 'Weapon' não encontrada.")
    Weapon = None

# --- Classes de Armas Específicas (TODAS DEVEM VIR DE Armas.) ---
# Removidas todas as referências a 'Arquivos.Armas.'

# Adaga
try:
    from .Armas.AdagaFogo import AdagaFogo
except ImportError:
    print("DEBUG(importacoes): Armas.AdagaFogo não encontrada.")
    AdagaFogo = None

# Espadas
try:
    from Armas.EspadaFogoAzul import EspadaFogoAzul
except ImportError: EspadaFogoAzul = None; print("DEBUG(importacoes): Armas.EspadaFogoAzul não encontrada.")
try:
    from Armas.EspadaPenitencia import EspadaPenitencia
except ImportError: EspadaPenitencia = None; print("DEBUG(importacoes): Armas.EspadaPenitencia não encontrada.")
try:
    from Armas.EspadaCaida import EspadaCaida
except ImportError: EspadaCaida = None; print("DEBUG(importacoes): Armas.EspadaCaida não encontrada.")
try:
    from Armas.EspadaLua import EspadaLua
except ImportError: EspadaLua = None; print("DEBUG(importacoes): Armas.EspadaLua não encontrada.")
try:
    from Armas.EspadaBrasas import EspadaBrasas # Previously under a different block
except ImportError: EspadaBrasas = None; print("DEBUG(importacoes): Armas.EspadaBrasas não encontrada.")

# Lâminas (Verifique o nome real do arquivo python para LaminaDoCeuCentilhante)
try:
    # Supondo que o arquivo seja LaminaDoCeuCentilhante.py ou LaminaCeuCinti.py
    from Armas.LaminaCeuCinti import LaminaDoCeuCentilhante # Ou from Armas.LaminaDoCeuCentilhante import ...
except ImportError: LaminaDoCeuCentilhante = None; print("DEBUG(importacoes): Armas.LaminaCeuCinti (ou similar) não encontrada.")

# Machados (Verifique os nomes reais dos arquivos python)
try:
    from Armas.MachadoBarbaro import MachadoBarbaro
except ImportError: MachadoBarbaro = None; print("DEBUG(importacoes): Armas.MachadoBarbaro não encontrada.")
try:
    from Armas.MachadoCeruleo import MachadoCeruleo
except ImportError: MachadoCeruleo = None; print("DEBUG(importacoes): Armas.MachadoCeruleo não encontrada.")
try:
    # Supondo que o arquivo seja Machado_Santa.py ou MachadoDaDescidaSanta.py
    from Armas.Machado_Santa import MachadoDaDescidaSanta # Ou from Armas.MachadoDaDescidaSanta import ...
except ImportError: MachadoDaDescidaSanta = None; print("DEBUG(importacoes): Armas.Machado_Santa (ou similar) não encontrada.")
try:
    # Supondo que o arquivo seja MachadoAbrasa.py ou MachadoDoFogoAbrasador.py
    from Armas.MachadoAbrasa import MachadoDoFogoAbrasador # Ou from Armas.MachadoDoFogoAbrasador import ...
except ImportError: MachadoDoFogoAbrasador = None; print("DEBUG(importacoes): Armas.MachadoAbrasa (ou similar) não encontrada.")
try:
    from Armas.MachadoMarfim import MachadoMarfim
except ImportError: MachadoMarfim = None; print("DEBUG(importacoes): Armas.MachadoMarfim não encontrada.")
try:
    from Armas.MachadoMacabro import MachadoMacabro
except ImportError: MachadoMacabro = None; print("DEBUG(importacoes): Armas.MachadoMacabro não encontrada.")

# --- Outros Módulos do Jogo (no diretório Jogo/) ---

try:
    from Pause import PauseMenuManager
except ImportError:
    print("DEBUG(importacoes): 'Pause.py' ou classe 'PauseMenuManager' não encontrada.")
    PauseMenuManager = None
try:
    from xp_manager import XPManager
except ImportError:
    print("DEBUG(importacoes): 'xp_manager.py' ou classe 'XPManager' não encontrada.")
    XPManager = None
try:
    from Menu import Menu
except ImportError:
    print("DEBUG(importacoes): 'Menu.py' ou classe 'Menu' não encontrada.")
    Menu = None
try:
    from GerenciadorDeInimigos import GerenciadorDeInimigos
except ImportError:
    print("DEBUG(importacoes): 'GerenciadorDeInimigos.py' não encontrado.")
    GerenciadorDeInimigos = None
try:
    from Estacoes import Estacoes
except ImportError:
    print("DEBUG(importacoes): 'Estacoes.py' não encontrado.")
    Estacoes = None
try:
    from grama import Grama
except ImportError:
    print("DEBUG(importacoes): 'grama.py' não encontrado.")
    Grama = None
try:
    from arvores import Arvore
except ImportError:
    print("DEBUG(importacoes): 'arvores.py' não encontrado.")
    Arvore = None
try:
    from timer1 import Timer
except ImportError:
    print("DEBUG(importacoes): 'timer1.py' não encontrado.")
    Timer = None
try:
    import shop_elements # Se for um módulo com funções/classes globais
except ImportError:
    print("DEBUG(importacoes): 'shop_elements.py' não encontrado.")
    shop_elements = None
try:
    from death_screen import run_death_screen
except ImportError:
    print("DEBUG(importacoes): 'death_screen.py' ou 'run_death_screen' não encontrado.")
    run_death_screen = None
try:
    # Se loja.py contém run_shop_scene
    from loja import run_shop_scene
except ImportError:
    print("DEBUG(importacoes): 'loja.py' ou função 'run_shop_scene' não encontrada.")
    run_shop_scene = None

print("DEBUG(importacoes): Módulo importacoes.py carregado e atualizado (baseado na estrutura da imagem).")