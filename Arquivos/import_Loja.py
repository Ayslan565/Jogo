# Arquivo: importacoes_armas.py
# Este arquivo centraliza todas as importações de classes de armas para o jogo.

print("DEBUG: Iniciando importação de todas as classes de armas...")

# --- CLASSES BASE ---
try:
    from Armas.weapon import Weapon
    print("  (+) Classe base 'Weapon' importada.")
except ImportError:
    Weapon = None
    print("  (-) AVISO: Classe base 'Weapon' não encontrada em Armas/weapon.py.")

try:
    from Armas.MachadoBase import MachadoBase
    print("  (+) Classe base 'MachadoBase' importada.")
except ImportError:
    MachadoBase = None
    print("  (-) AVISO: Classe base 'MachadoBase' não encontrada em Armas/MachadoBase.py.")

# --- ESPADAS ---
print("\n--- Importando Espadas ---")
try:
    from Armas.AdagaFogo import AdagaFogo
    print("  (+) AdagaFogo importada.")
except ImportError:
    AdagaFogo = None
    print("  (-) AVISO: AdagaFogo não encontrada.")
except ImportError:
    AdagaFogo = None
    print("  (-) AVISO: AdagaFogo não encontrada.")

try:
    from Armas.EspadaBrasas import EspadaBrasas
    print("  (+) EspadaBrasas importada.")
except ImportError:
    EspadaBrasas = None
    print("  (-) AVISO: EspadaBrasas não encontrada.")
    
try:
    from Armas.EspadaPenitencia import EspadaPenitencia
    print("  (+) EspadaPenitencia importada.")
except ImportError:
    EspadaPenitencia = None
    print("  (-) AVISO: EspadaPenitencia não encontrada.")

try:
    from Armas.EspadaCaida import EspadaCaida
    print("  (+) EspadaCaida importada.")
except ImportError:
    EspadaCaida = None
    print("  (-) AVISO: EspadaCaida não encontrada.")

try:
    from Armas.EspadaFogoAzul import EspadaFogoAzul
    print("  (+) EspadaFogoAzul importada.")
except ImportError:
    EspadaFogoAzul = None
    print("  (-) AVISO: EspadaFogoAzul não encontrada.")

try:
    from Armas.EspadaLua import EspadaLua
    print("  (+) EspadaLua importada.")
except ImportError:
    EspadaLua = None
    print("  (-) AVISO: EspadaLua não encontrada.")

try:
    from Armas.EspadaSacraCerulea import EspadaSacraCerulea
    print("  (+) EspadaSacraCerulea importada.")
except ImportError:
    EspadaSacraCerulea = None
    print("  (-) AVISO: EspadaSacraCerulea não encontrada.")

try:
    from Armas.EspadaSacraDasBrasas import EspadaSacraDasBrasas
    print("  (+) EspadaSacraDasBrasas importada.")
except ImportError:
    EspadaSacraDasBrasas = None
    print("  (-) AVISO: EspadaSacraDasBrasas não encontrada.")

try:
    from Armas.LaminaCeuCinti import LaminaDoCeuCintilante
    print("  (+) LaminaDoCeuCentilhante importada.")
except ImportError:
    LaminaDoCeuCentilhante = None
    print("  (-) AVISO: LaminaDoCeuCentilhante não encontrada.")


# --- MACHADOS ---
print("\n--- Importando Machados ---")
try:
    from Armas.MachadoBarbaro import MachadoBarbaro
    print("  (+) MachadoBarbaro importado.")
except ImportError:
    MachadoBarbaro = None
    print("  (-) AVISO: MachadoBarbaro não encontrado.")

try:
    from Armas.MachadoCeruleo import MachadoCeruleo
    print("  (+) MachadoCeruleo importado.")
except ImportError:
    MachadoCeruleo = None
    print("  (-) AVISO: MachadoCeruleo não encontrado.")

try:
    from Armas.Machado_Santa import MachadoDaDescidaSanta
    print("  (+) MachadoDaDescidaSanta importado.")
except ImportError:
    MachadoDaDescidaSanta = None
    print("  (-) AVISO: MachadoDaDescidaSanta não encontrado.")

try:
    from Armas.MachadoAbrasa import MachadoDoFogoAbrasador
    print("  (+) MachadoDoFogoAbrasador importado.")
except ImportError:
    MachadoDoFogoAbrasador = None
    print("  (-) AVISO: MachadoDoFogoAbrasador não encontrado.")

try:
    from Armas.MachadoMarfim import MachadoMarfim
    print("  (+) MachadoMarfim importado.")
except ImportError:
    MachadoMarfim = None
    print("  (-) AVISO: MachadoMarfim não encontrado.")

try:
    from Armas.MachadoMacabro import MachadoMacabro
    print("  (+) MachadoMacabro importado.")
except ImportError:
    MachadoMacabro = None
    print("  (-) AVISO: MachadoMacabro não encontrado.")

# --- CAJADOS ---
# Adicione mais importações de cajados conforme necessário
print("\n--- Importando Cajados ---")
try:
    from Armas.Cajado import Cajado # Supondo que exista um Cajado.py com uma classe base ou específica
    print("  (+) Cajado importado.")
except ImportError:
    Cajado = None
    print("  (-) AVISO: Cajado não encontrado.")

print("\nDEBUG: Importação de armas concluída.")
