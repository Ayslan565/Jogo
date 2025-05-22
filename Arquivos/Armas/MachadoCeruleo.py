# Armas/MachadoCeruleo.py
from .MachadoBase import MachadoBase # Importa a nova classe base para machados

class MachadoCeruleo(MachadoBase):
    """
    Representa o Machado Cerúleo, uma arma com níveis de evolução.
    """
    def __init__(self):
        super().__init__(
            name="Machado Cerúleo da Estrela Cadente", # Nome completo para exibição no jogo
            damage=35.0,
            attack_range=90.0,
            cooldown=1.6
        )
        self.level = 1.0

        self._stats_by_level = {
            1.0: {"damage": 35.0, "range": 90.0, "cooldown": 1.6},
            1.5: {"damage": 40.0, "range": 95.0, "cooldown": 1.5},
            2.0: {"damage": 50.0, "range": 105.0, "cooldown": 1.3},
            2.5: {"damage": 55.0, "range": 110.0, "cooldown": 1.2},
            3.0: {"damage": 70.0, "range": 125.0, "cooldown": 1.0},
        }
        self._apply_level_stats()
        print(f"DEBUG(MachadoCeruleo): Machado '{self.name}' criada no Nível {self.level}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(MachadoCeruleo): {self.name} evoluiu para o Nível {self.level}!")
        else:
            print(f"DEBUG(MachadoCeruleo): Nível de evolução {target_level} inválido para {self.name}.")

    def _apply_level_stats(self):
        stats = self._stats_by_level.get(self.level)
        if stats:
            self.damage = stats["damage"]
            self.attack_range = stats["range"]
            self.cooldown = stats["cooldown"]
        else:
            print(f"DEBUG(MachadoCeruleo): Aviso: Estatísticas não encontradas para o nível {self.level}. Mantendo as atuais.")