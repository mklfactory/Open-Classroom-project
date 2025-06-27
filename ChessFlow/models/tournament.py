from models.player import Player
from models.round import Round

class Tournament:
    def __init__(self, name, place, start_date, end_date, description, players=None, rounds=None, number_of_rounds=4):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.current_round = 0
        self.players = players or []
        self.rounds = rounds or []

    def to_dict(self):
        return {
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "players": [p.to_dict() for p in self.players],
            "rounds": [r.to_dict() for r in self.rounds]
        }

    @staticmethod
    def from_dict(data):
        return Tournament(
            data["name"],
            data["place"],
            data["start_date"],
            data["end_date"],
            data["description"],
            [Player.from_dict(p) for p in data["players"]],
            [Round.from_dict(r) for r in data.get("rounds", [])],
            data.get("number_of_rounds", 4)
        )

    def __str__(self):
        return f"{self.name} - {self.place} ({self.start_date} au {self.end_date})"