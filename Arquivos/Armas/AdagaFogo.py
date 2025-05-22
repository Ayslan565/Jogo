# AdagaFogo.py
from .weapon import Weapon

class AdagaFogo(Weapon):
    """
    Representa a Adaga do Fogo Contudente, uma arma com níveis de evolução.
    Adagas geralmente têm dano menor, mas cooldown muito rápido e alcance curto.
    """
    def __init__(self):
        super().__init__(
            name="Adaga do Fogo Contudente", # Nome completo para exibição no jogo
            damage=150,
            attack_range=10.0,
            cooldown=0.2 # Muito rápido
        )
        self.level = 1.0

        self._stats_by_level = {
            1.0: {"damage": 25.0, "range": 25.0, "cooldown": 0.4},
            1.5: {"damage": 20.0, "range": 50.0, "cooldown": 0.55},
            2.0: {"damage": 25.0, "range": 60.0, "cooldown": 0.5},
            2.5: {"damage": 30.0, "range": 60.0, "cooldown": 0.45},
            3.0: {"damage": 35.0, "range": 70.0, "cooldown": 0.4},
        }
        self._apply_level_stats()
        print(f"DEBUG(AdagaFogo): Adaga '{self.name}' criada no Nível {self.level}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(AdagaFogo): {self.name} evoluiu para o Nível {self.level}!")
        else:
            print(f"DEBUG(AdagaFogo): Nível de evolução {target_level} inválido para {self.name}.")

    def _apply_level_stats(self):
        stats = self._stats_by_level.get(self.level)
        if stats:
            self.damage = stats["damage"]
            self.attack_range = stats["range"]
            self.cooldown = stats["cooldown"]
        else:
            print(f"DEBUG(AdagaFogo): Aviso: Estatísticas não encontradas para o nível {self.level}. Mantendo as atuais.")

