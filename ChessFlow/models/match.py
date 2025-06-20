class Match:
    def __init__(self, player1, player2, score1=0, score2=0):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def to_dict(self):
        return {
            "player1": self.player1.to_dict(),
            "player2": self.player2.to_dict(),
            "score1": self.score1,
            "score2": self.score2,
        }

    @staticmethod
    def from_dict(data):
        return Match(
            Player.from_dict(data["player1"]),
            Player.from_dict(data["player2"]),
            data["score1"],
            data["score2"]
        )
