# Armas/EspadaLua.py
from .weapon import Weapon

class EspadaLua(Weapon):
    """
    Representa a Espada Sacra da Lua (Azul com Roxo), uma arma com níveis de evolução.
    """
    def __init__(self):
        super().__init__(
            name="Espada Sacra da Lua (Azul com Roxo)", # Nome completo para exibição no jogo
            damage=45.0,
            attack_range=115.0,
            cooldown=1.2
        )
        self.level = 1.0

        self._stats_by_level = {
            1.0: {"damage": 45.0, "range": 115.0, "cooldown": 1.2},
            1.5: {"damage": 50.0, "range": 120.0, "cooldown": 1.15},
            2.0: {"damage": 62.0, "range": 130.0, "cooldown": 1.0},
            2.5: {"damage": 68.0, "range": 135.0, "cooldown": 0.95},
            3.0: {"damage": 85.0, "range": 150.0, "cooldown": 0.8},
        }
        self._apply_level_stats()
        print(f"DEBUG(EspadaLua): Espada '{self.name}' criada no Nível {self.level}.")

    def evolve(self, target_level: float):
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(EspadaLua): {self.name} evoluiu para o Nível {self.level}!")
        else:
            print(f"DEBUG(EspadaLua): Nível de evolução {target_level} inválido para {self.name}.")

    def _apply_level_stats(self):
        stats = self._stats_by_level.get(self.level)
        if stats:
            self.damage = stats["damage"]
            self.attack_range = stats["range"]
            self.cooldown = stats["cooldown"]
        else:
            print(f"DEBUG(EspadaLua): Aviso: Estatísticas não encontradas para o nível {self.level}. Mantendo as atuais.")