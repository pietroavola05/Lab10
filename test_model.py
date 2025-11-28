
from model.model import Model

model = Model()
dizionario = model.creo_dizionario_delle_tratte()
lista = model.creo_lista_delle_tratte_valide(soglia_minima = 200)
print(lista)

print(dizionario)

