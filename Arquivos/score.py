class ScoreManager:
    def __init__(self):
        self.score = 0

    def adicionar_xp(self, xp):
        self.score += xp

    def get_score(self):
        return self.score

    def reset(self):
        self.score = 0