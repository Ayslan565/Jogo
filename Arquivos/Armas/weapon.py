class Weapon:
    """
    Classe base para todas as armas no jogo.
    Define atributos comuns como nome, dano, alcance e cooldown.
    """
    def __init__(self, name: str, damage: float, attack_range: float, cooldown: float):
        self.name = name
        self.damage = damage
        self.attack_range = attack_range
        self.cooldown = cooldown

    def __str__(self):
        return f"{self.name} (Dano: {self.damage}, Alcance: {self.attack_range}, Cooldown: {self.cooldown}s)"

# weapon.py

class Weapon:
    """
    Classe base para todas as armas no jogo.
    Define atributos comuns como nome, dano, alcance e cooldown.
    """
    def __init__(self, name: str, damage: float, attack_range: float, cooldown: float):
        self.name = name
        self.damage = damage
        self.attack_range = attack_range
        self.cooldown = cooldown

    def __str__(self):
        return f"{self.name} (Dano: {self.damage}, Alcance: {self.attack_range}, Cooldown: {self.cooldown}s)"

