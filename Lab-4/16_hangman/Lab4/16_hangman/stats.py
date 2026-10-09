class SessionStats:
    def __init__(self):
        self.rounds = 0
        self.wins = 0
        self.best_streak = 0

    def record(self, won, streak):
        self.rounds += 1
        self.wins += int(won)
        self.best_streak = max(self.best_streak, streak)
