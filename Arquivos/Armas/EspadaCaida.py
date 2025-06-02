# Armas/EspadaCaida.py
from weapon import Weapon

class EspadaCaida(Weapon):
    """
    Representa a Espada Sacra Caída (Roxo), uma arma com níveis de evolução.
    """
    def __init__(self):
        super().__init__(
            name="Espada Sacra Caída (Roxo)", # Nome completo para exibição no jogo
            damage=50.0,
            attack_range=120.0,
            cooldown=1.4
        )
        self.level = 1.0

        self._stats_by_level = {
            1.0: {"damage": 50.0, "range": 120.0, "cooldown": 1.4},
            1.5: {"damage": 55.0, "range": 125.0, "cooldown": 1.3},
            2.0: {"damage": 68.0, "range": 135.0, "cooldown": 1.15},
            2.5: {"damage": 75.0, "range": 140.0, "cooldown": 1.0},
            3.0: {"damage": 90.0, "range": 155.0, "cooldown": 0.9},
        }
        self._apply_level_stats()
        print(f"DEBUG(EspadaCaida): Espada '{self.name}' criada no Nível {self.level}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(EspadaCaida): {self.name} evoluiu para o Nível {self.level}!")
        else:
            print(f"DEBUG(EspadaCaida): Nível de evolução {target_level} inválido para {self.name}.")

    def _apply_level_stats(self):
        stats = self._stats_by_level.get(self.level)
        if stats:
            self.damage = stats["damage"]
            self.attack_range = stats["range"]
            self.cooldown = stats["cooldown"]
        else:
            print(f"DEBUG(EspadaCaida): Aviso: Estatísticas não encontradas para o nível {self.level}. Mantendo as atuais.")