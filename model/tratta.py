# tratta.py (CORRETTO)
from dataclasses import dataclass

@dataclass
class Tratta:
    id_origine: int
    id_destinazione: int
    valore_merce: float
    contatore: int

    @property
    def guadagno_medio(self):
        return self.valore_merce / self.contatore

    def __str__(self):
        return f"Tratta Hub {self.id_origine} <-> Hub {self.id_destinazione}: €{self.guadagno_medio:.2f}"