# MachadoMarfim.py
from .MachadoBase import MachadoBase # Importa a nova classe base para machados

class MachadoMarfim(MachadoBase):
    """
    Representa o Machado do Marfim Resplendor, uma arma com níveis de evolução.
    """
    def __init__(self):
        super().__init__(
            name="Machado do Marfim Resplendor", # Nome completo para exibição no jogo
            damage=48.0,
            attack_range=95.0,
            cooldown=1.8
        )
        self.level = 1.0

        self._stats_by_level = {
            1.0: {"damage": 48.0, "range": 95.0, "cooldown": 1.8},
            1.5: {"damage": 53.0, "range": 100.0, "cooldown": 1.7},
            2.0: {"damage": 65.0, "range": 110.0, "cooldown": 1.5},
            2.5: {"damage": 70.0, "range": 115.0, "cooldown": 1.4},
            3.0: {"damage": 85.0, "range": 130.0, "cooldown": 1.2},
        }
        self._apply_level_stats()
        print(f"DEBUG(MachadoMarfim): Machado '{self.name}' criado no Nível {self.level}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(MachadoMarfim): {self.name} evoluiu para o Nível {self.level}!")
        else:
            print(f"DEBUG(MachadoMarfim): Nível de evolução {target_level} inválido para {self.name}.")

    def _apply_level_stats(self):
        stats = self._stats_by_level.get(self.level)
        if stats:
            self.damage = stats["damage"]
            self.attack_range = stats["range"]
            self.cooldown = stats["cooldown"]
        else:
            print(f"DEBUG(MachadoMarfim): Aviso: Estatísticas não encontradas para o nível {self.level}. Mantendo as atuais.")

