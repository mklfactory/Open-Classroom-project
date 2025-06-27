import datetime
from models.match import Match

class Round:
    def __init__(self, name, matches=None):
        self.name = name
        self.matches = matches or []
        self.start_time = str(datetime.datetime.now())
        self.end_time = None

    def end_round(self):
        self.end_time = str(datetime.datetime.now())

    def to_dict(self):
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "matches": [m.to_dict() for m in self.matches]
        }

    @staticmethod
    def from_dict(data):
        r = Round(
            data["name"],
            [Match.from_dict(m) for m in data["matches"]]
        )
        r.start_time = data.get("start_time")
        r.end_time = data.get("end_time")
        return r