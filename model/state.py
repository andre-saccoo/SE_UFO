from dataclasses import dataclass

@dataclass
class State:
    name: str
    id: str
    num_avvistamenti: int
    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return self.id == other.id
    def __repr__(self):
        return f"{self.name} codice: {self.id} avvistamenti: {self.num_avvistamenti} "