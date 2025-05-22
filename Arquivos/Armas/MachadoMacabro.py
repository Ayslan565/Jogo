# MachadoMacabro.py
from .MachadoBase import MachadoBase # Importa a nova classe base para machados

class MachadoMacabro(MachadoBase):
    """
    Representa o Machado Macabro, uma arma com níveis de evolução.
    """
    def __init__(self):
        super().__init__(
            name="Machado Macabro da Gula Infinita", # Nome completo para exibição no jogo
            damage=40.0,
            attack_range=80.0,
            cooldown=2.0
        )
        self.level = 1.0

        self._stats_by_level = {
            1.0: {"damage": 40.0, "range": 80.0, "cooldown": 2.0},
            1.5: {"damage": 45.0, "range": 85.0, "cooldown": 1.9},
            2.0: {"damage": 55.0, "range": 95.0, "cooldown": 1.7},
            2.5: {"damage": 60.0, "range": 100.0, "cooldown": 1.6},
            3.0: {"damage": 75.0, "range": 115.0, "cooldown": 1.4},
        }
        self._apply_level_stats()
        print(f"DEBUG(MachadoMacabro): Machado '{self.name}' criado no Nível {self.level}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(MachadoMacabro): {self.name} evoluiu para o Nível {self.level}!")
        else:
            print(f"DEBUG(MachadoMacabro): Nível de evolução {target_level} inválido para {self.name}.")

    def _apply_level_stats(self):
        stats = self._stats_by_level.get(self.level)
        if stats:
            self.damage = stats["damage"]
            self.attack_range = stats["range"]
            self.cooldown = stats["cooldown"]
        else:
            print(f"DEBUG(MachadoMacabro): Aviso: Estatísticas não encontradas para o nível {self.level}. Mantendo as atuais.")

