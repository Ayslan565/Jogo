# Armas/MachadoBarbaro.py
from .MachadoBase import MachadoBase # Importa a nova classe base para machados

class MachadoBarbaro(MachadoBase):
    """
    Representa o Machado Bárbaro Cravejado, uma arma com níveis de evolução.
    """
    def __init__(self):
        super().__init__(
            name="Machado Bárbaro Cravejado", # Nome completo para exibição no jogo
            damage=55.0,
            attack_range=85.0,
            cooldown=2.2
        )
        self.level = 1.0

        self._stats_by_level = {
            1.0: {"damage": 15.0, "range": 85.0, "cooldown": 2.2},
            1.5: {"damage": 20.0, "range": 90.0, "cooldown": 2.1},
            2.0: {"damage": 25.0, "range": 100.0, "cooldown": 1.9},
            2.5: {"damage": 30.0, "range": 105.0, "cooldown": 1.8},
            3.0: {"damage": 35.0, "range": 120.0, "cooldown": 1.6},
        }
        self._apply_level_stats()
        print(f"DEBUG(MachadoBarbaro): Machado '{self.name}' criada no Nível {self.level}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(MachadoBarbaro): {self.name} evoluiu para o Nível {self.level}!")
        else:
            print(f"DEBUG(MachadoBarbaro): Nível de evolução {target_level} inválido para {self.name}.")

    def _apply_level_stats(self):
        stats = self._stats_by_level.get(self.level)
        if stats:
            self.damage = stats["damage"]
            self.attack_range = stats["range"]
            self.cooldown = stats["cooldown"]
        else:
            print(f"DEBUG(MachadoBarbaro): Aviso: Estatísticas não encontradas para o nível {self.level}. Mantendo as atuais.")