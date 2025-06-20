class Round:
    def __init__(self, name, matches=None):
        self.name = name
        self.matches = matches or []

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [m.to_dict() for m in self.matches],
        }

    @staticmethod
    def from_dict(data):
        return Round(
            data["name"],
            [Match.from_dict(m) for m in data["matches"]]
        )
