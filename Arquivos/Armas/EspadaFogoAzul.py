# EspadaFogoAzul.py
from .weapon import Weapon

class EspadaFogoAzul(Weapon):
    """
    Representa a Espada de Fogo Azul Sacra Cerúlea, uma arma com níveis de evolução.
    """
    def __init__(self):
        super().__init__(
            name="Espada de Fogo Azul Sacra Cerúlea", # Nome completo para exibição no jogo
            damage=42.0,
            attack_range=110.0,
            cooldown=1.3
        )
        self.level = 1.0

        self._stats_by_level = {
            1.0: {"damage": 42.0, "range": 110.0, "cooldown": 1.3},
            1.5: {"damage": 48.0, "range": 115.0, "cooldown": 1.25},
            2.0: {"damage": 60.0, "range": 125.0, "cooldown": 1.1},
            2.5: {"damage": 65.0, "range": 130.0, "cooldown": 1.05},
            3.0: {"damage": 80.0, "range": 145.0, "cooldown": 0.9},
        }
        self._apply_level_stats()
        print(f"DEBUG(EspadaFogoAzul): Espada '{self.name}' criada no Nível {self.level}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(EspadaFogoAzul): {self.name} evoluiu para o Nível {self.level}!")
        else:
            print(f"DEBUG(EspadaFogoAzul): Nível de evolução {target_level} inválido para {self.name}.")

    def _apply_level_stats(self):
        stats = self._stats_by_level.get(self.level)
        if stats:
            self.damage = stats["damage"]
            self.attack_range = stats["range"]
            self.cooldown = stats["cooldown"]
        else:
            print(f"DEBUG(EspadaFogoAzul): Aviso: Estatísticas não encontradas para o nível {self.level}. Mantendo as atuais.")

