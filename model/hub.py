from dataclasses import dataclass

@dataclass
class Hub:
    id: int
    nome: str
    #gli altri non mi servono per questo programma
    """codice: str 
    citta: str
    stato: str
    latitudine: float
    longitudine: float"""

    def __eq__(self, other):
        return isinstance(other, Hub) and self.id == other.id

    def __str__(self):
        return f"{self.nome}"

    def __repr__(self):
        return f"{self.nome}"

    def __hash__(self):
        return hash(self.id)
