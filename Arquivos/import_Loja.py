try:
    from Armas.weapon import Weapon
except ImportError:
    Weapon = None
    print("DEBUG(import_Loja): Weapon não encontrado em Armas.weapon.")

try:
    from Armas.AdagaFogo import AdagaFogo
except ImportError:
    AdagaFogo = None
    print("DEBUG(import_Loja): AdagaFogo não encontrado em Armas.AdagaFogo.")

try:
    from Armas.EspadaBrasas import EspadaBrasas
except ImportError:
    EspadaBrasas = None
    print("DEBUG(import_Loja): EspadaBrasas não encontrado em Armas.EspadaBrasas.")

try:
    from Armas.EspadaCaida import EspadaCaida
except ImportError:
    EspadaCaida = None
    print("DEBUG(import_Loja): EspadaCaida não encontrado em Armas.EspadaCaida.")

try:
    from Armas.EspadaFogoAzul import EspadaFogoAzul
except ImportError:
    EspadaFogoAzul = None
    print("DEBUG(import_Loja): EspadaFogoAzul não encontrado em Armas.EspadaFogoAzul.")

try:
    from Armas.EspadaLua import EspadaLua
except ImportError:
    EspadaLua = None
    print("DEBUG(import_Loja): EspadaLua não encontrado em Armas.EspadaLua.")

try:
    from Armas.EspadaSacraCerulea import EspadaSacraCerulea
except ImportError:
    EspadaSacraCerulea = None
    print("DEBUG(import_Loja): EspadaSacraCerulea não encontrado em Armas.EspadaSacraCerulea.")

try:
    from Armas.EspadaSacraDasBrasas import EspadaSacraDasBrasas
except ImportError:
    EspadaSacraDasBrasas = None
    print("DEBUG(import_Loja): EspadaSacraDasBrasas não encontrado em Armas.EspadaSacraDasBrasas.")
