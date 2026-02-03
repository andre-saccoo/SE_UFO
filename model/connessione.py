from dataclasses import dataclass

@dataclass
class Connessione:
    state1: str
    state2: str

    def __hash__(self):
        return hash((self.state1, self.state2))
    def __eq__(self, other):
        return self.state1 == other.state1 and self.state2 == other.state2

