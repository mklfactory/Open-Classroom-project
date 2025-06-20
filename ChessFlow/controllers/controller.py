import json
from models.tournament import Tournament
from models.player import Player
from views.view import View

class TournamentController:
    def __init__(self):
        self.view = View()
        self.tournaments = self.load_data()

    def run(self):
        while True:
            choice = self.view.main_menu()
            if choice == "1":
                self.create_tournament()
            elif choice == "2":
                self.list_tournaments()
            elif choice == "3":
                self.save_data()
                self.view.display("Au revoir !")
                break

    def create_tournament(self):
        tournament_data = self.view.get_tournament_info()
        players = [Player(*self.view.get_player_info(i+1)) for i in range(8)]
        tournament = Tournament(*tournament_data, players=players)
        self.tournaments.append(tournament)
        self.view.display("Tournoi créé avec succès.")

    def list_tournaments(self):
        for t in self.tournaments:
            self.view.display(str(t))

    def save_data(self):
        with open("data/tournaments.json", "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tournaments], f, indent=4)

    def load_data(self):
        try:
            with open("data/tournaments.json", "r", encoding="utf-8") as f:
                return [Tournament.from_dict(d) for d in json.load(f)]
        except FileNotFoundError:
            return []