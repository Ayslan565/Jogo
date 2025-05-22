# Armas/EspadaPenitencia.py
from .weapon import Weapon

class EspadaPenitencia(Weapon):
    """
    Representa a Espada do Olhar da Penitência, uma arma com níveis de evolução.
    """
    def __init__(self):
        super().__init__(
            name="Espada do Olhar da Penitência", # Nome completo para exibição no jogo
            damage=58.0,
            attack_range=130.0,
            cooldown=1.5
        )
        self.level = 1.0

        self._stats_by_level = {
            1.0: {"damage": 58.0, "range": 130.0, "cooldown": 1.5},
            1.5: {"damage": 65.0, "range": 135.0, "cooldown": 1.4},
            2.0: {"damage": 80.0, "range": 145.0, "cooldown": 1.2},
            2.5: {"damage": 88.0, "range": 150.0, "cooldown": 1.1},
            3.0: {"damage": 100.0, "range": 165.0, "cooldown": 1.0},
        }
        self._apply_level_stats()
        print(f"DEBUG(EspadaPenitencia): Espada '{self.name}' criada no Nível {self.level}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(EspadaPenitencia): {self.name} evoluiu para o Nível {self.level}!")
        else:
            print(f"DEBUG(EspadaPenitencia): Nível de evolução {target_level} inválido para {self.name}.")

    def _apply_level_stats(self):
        stats = self._stats_by_level.get(self.level)
        if stats:
            self.damage = stats["damage"]
            self.attack_range = stats["range"]
            self.cooldown = stats["cooldown"]
        else:
            print(f"DEBUG(EspadaPenitencia): Aviso: Estatísticas não encontradas para o nível {self.level}. Mantendo as atuais.")