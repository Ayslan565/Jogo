# Armas/EspadaBrasas.py
from .weapon import Weapon

class EspadaBrasas(Weapon):
    """
    Representa a Espada Sacra das Brasas, uma arma específica com níveis de evolução.
    """
    def __init__(self):
        # Inicializa com as estatísticas base do Nível 1
        super().__init__(
            name="Espada Sacra das Brasas", # Nome completo para exibição no jogo
            damage=30.0,
            attack_range=100.0,
            cooldown=1.5
        )
        self.level = 1.0 # Começa no Nível 1.0 (float para permitir 1.5, 2.5)

        # Dicionário para mapear estatísticas por nível de evolução
        # Você pode ajustar esses valores conforme o balanceamento do seu jogo
        self._stats_by_level = {
            1.0: {"damage": 30.0, "range": 100.0, "cooldown": 1.5},
            1.5: {"damage": 35.0, "range": 105.0, "cooldown": 1.4}, # Nível intermediário, sem novo sprite
            2.0: {"damage": 45.0, "range": 115.0, "cooldown": 1.2},
            2.5: {"damage": 50.0, "range": 120.0, "cooldown": 1.1}, # Nível intermediário, sem novo sprite
            3.0: {"damage": 65.0, "range": 130.0, "cooldown": 0.9},
        }
        
        self._apply_level_stats() # Aplica as estatísticas iniciais baseadas no level

        print(f"DEBUG(EspadaBrasas): Espada '{self.name}' criada no Nível {self.level}.")

    def evolve(self, target_level: float):
        """
        Evolui a espada para um nível específico, atualizando suas estatísticas.
        Args:
            target_level (float): O nível desejado para a evolução (ex: 1.5, 2.0, 3.0).
        """
        if target_level in self._stats_by_level:
            self.level = target_level
            self._apply_level_stats()
            print(f"DEBUG(EspadaBrasas): {self.name} evoluiu para o Nível {self.level}!")
        else:
            print(f"DEBUG(EspadaBrasas): Nível de evolução {target_level} inválido para {self.name}.")

    def _apply_level_stats(self):
        """
        Aplica as estatísticas de dano, alcance e cooldown correspondentes ao nível atual da espada.
        """
        stats = self._stats_by_level.get(self.level)
        if stats:
            self.damage = stats["damage"]
            self.attack_range = stats["range"]
            self.cooldown = stats["cooldown"]
        else:
            print(f"DEBUG(EspadaBrasas): Aviso: Estatísticas não encontradas para o nível {self.level}. Mantendo as atuais.")