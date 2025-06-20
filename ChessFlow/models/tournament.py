from models.player import Player
from models.round import Round

class Tournament:
    def __init__(self, name, place, date, description, players=None, rounds=None):
        self.name = name
        self.place = place
        self.date = date
        self.description = description
        self.players = players or []
        self.rounds = rounds or []

    def to_dict(self):
        return {
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "description": self.description,
            "players": [p.to_dict() for p in self.players],
            "rounds": [r.to_dict() for r in self.rounds],
        }

    @staticmethod
    def from_dict(data):
        return Tournament(
            data["name"],
            data["place"],
            data["date"],
            data["description"],
            [Player.from_dict(p) for p in data["players"]],
            [Round.from_dict(r) for r in data.get("rounds", [])]
        )

    def __str__(self):
        return f"{self.name} - {self.place} - {self.date}"

# --- views/view.py ---
class View:
    def main_menu(self):
        print("\n--- Menu Principal ---")
        print("1. Créer un tournoi")
        print("2. Voir les tournois")
        print("3. Quitter")
        return input("Votre choix : ")

    def get_tournament_info(self):
        print("\n--- Création d'un tournoi ---")
        name = input("Nom du tournoi : ")
        place = input("Lieu : ")
        date = input("Date : ")
        description = input("Description : ")
        return name, place, date, description

    def get_player_info(self, i):
        print(f"\n--- Joueur {i} ---")
        last = input("Nom : ")
        first = input("Prénom : ")
        birth = input("Date de naissance : ")
        rank = input("Classement : ")
        return last, first, birth, rank

    def display(self, msg):
        print("\n" + msg)
