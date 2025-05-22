# EspadaSacraDasBrasas.py
from .weapon import Weapon # Importa a nova classe base para machados

class EspadaSacraDasBrasas(Weapon):
    """
    Representa a Espada Sacra das Brasas, uma arma específica.
    """
    def __init__(self):
        # Chama o construtor da classe base (Weapon) com as estatísticas da espada
        super().__init__(
            name="Espada Sacra das Brasas",
            damage=30.0,  # Dano base da espada
            attack_range=100.0, # Alcance de ataque da espada (pixels)
            cooldown=1.5  # Cooldown entre ataques (em segundos)
        )
        print(f"DEBUG(EspadaSacraDasBrasas): Espada '{self.name}' criada.")

