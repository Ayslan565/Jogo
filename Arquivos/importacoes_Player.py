# Arquivo: importacoes.py
# Este arquivo centraliza as importações comuns para o jogo.

import pygame
import random
import math
import os
import time 
import threading # Adicionado para threading.Event em Roda_Armas
import tkinter as tk # Adicionado para tk.TclError em Roda_Armas
from vida import Vida 
from Armas.weapon import Weapon 

# Tentativas de importação para todas as armas listadas na loja
try: from Arquivos.Armas.AdagaFogo import AdagaFogo
except ImportError: AdagaFogo = None
try: from Armas.EspadaFogoAzul import EspadaFogoAzul # Para "Espada de Fogo azul Sacra Cerulea"
except ImportError: EspadaFogoAzul = None
try: from Armas.EspadaPenitencia import EspadaPenitencia # Para "Espada do Olhar Da Penitencia"
except ImportError: EspadaPenitencia = None
try: from Armas.EspadaCaida import EspadaCaida # Para "Espada Sacra Caida"
except ImportError: EspadaCaida = None
try: from Armas.EspadaLua import EspadaLua # Para "Espada Sacra do Lua"
except ImportError: EspadaLua = None
try: from Armas.LaminaCeuCinti import LaminaDoCeuCentilhante # Para "Lâmina do Ceu Centilhante"
except ImportError: LaminaDoCeuCentilhante = None

try: from Armas.MachadoBarbaro import MachadoBarbaro # Para "Machado Bárbaro Cravejado"
except ImportError: MachadoBarbaro = None
try: from Armas.MachadoCeruleo import MachadoCeruleo # Para "Machado Cerúleo da Estrela Cadente"
except ImportError: MachadoCeruleo = None
try: from Armas.Machado_Santa import MachadoDaDescidaSanta # Para "Machado da Descida Santa"
except ImportError: MachadoDaDescidaSanta = None
try: from Armas.MachadoAbrasa import MachadoDoFogoAbrasador # Para "Machado do Fogo Abrasador"
except ImportError: MachadoDoFogoAbrasador = None
try: from Armas.MachadoMarfim import MachadoMarfim # Para "Machado do Marfim Resplendor"
except ImportError: MachadoMarfim = None
try: from Armas.MachadoMacabro import MachadoMacabro # Para "Machado Macabro da Gula Infinita"
except ImportError: MachadoMacabro = None

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
try: from Arquivos.Armas.AdagaFogo import AdagaFogo
except ImportError: AdagaFogo = None
try: from Armas.EspadaFogoAzul import EspadaFogoAzul
except ImportError: EspadaFogoAzul = None
try: from Armas.EspadaLua import EspadaLua
except ImportError: EspadaLua = None
try: from Armas.EspadaCaida import EspadaCaida
except ImportError: EspadaCaida = None
try: from Armas.EspadaPenitencia import EspadaPenitencia
except ImportError: EspadaPenitencia = None
# Adicione aqui outras classes de armas que seu jogo possa ter

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

try:
    from GerenciadorDeInimigos import GerenciadorDeInimigos
    # As importações de inimigos específicos são feitas dentro de GerenciadorDeInimigos.py
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
    from timer1 import Timer # Se o nome do seu arquivo for timer1.py
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'timer1.py' ou classe 'Timer' não encontrado.")
    Timer = None

try:
    import shop_elements # Se for um módulo com funções/classes globais
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'shop_elements.py' não encontrado.")
    shop_elements = None

try:
    from death_screen import run_death_screen
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'death_screen.py' ou função 'run_death_screen' não encontrado.")
    run_death_screen = None
import inventario_barra
try:
    from Spawn_Loja import run_shop_scene # Anteriormente era loja.py, ajustado para loja_core.py como no seu último Game.py
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'loja_core.py' ou função 'run_shop_scene' não encontrado.")
    run_shop_scene = None # Nome da função, não um módulo

# --- NOVO: Importação da Barra de Inventário ---
try:
    from inventario_barra import BarraInventario, ItemInventario
except ImportError:
    print("DEBUG(importacoes): Aviso: Módulo 'inventario_barra.py' ou suas classes não encontrados.")
    BarraInventario = None
    ItemInventario = None

print("DEBUG(importacoes): Módulo importacoes.py carregado e atualizado.")

