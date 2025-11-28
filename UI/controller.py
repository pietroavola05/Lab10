import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia (minima)
        """
        #Verifico che il valore inserito sia un valore numerico:

        self._view.lista_visualizzazione.controls.clear()
        self._view.update()

        valore_inserito_utente = self._view.guadagno_medio_minimo.value

        try:
            # Validazione input e conversione a float
            soglia_inserita = float(valore_inserito_utente)
            if soglia_inserita < 0:
                self._view.show_alert("Inserisci un valore numerico non negativo.")
                return

            lista_tratte_valide = self._model.creo_lista_delle_tratte_valide(soglia_inserita)
            # Costruisce il grafo con la soglia corrente
            self._model.costruisci_grafo(soglia_inserita)

            # Ottiene le statistiche
            num_nodi = self._model.get_num_nodes()
            num_archi = self._model.get_num_edges()

            # Visualizzazione delle statistiche
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f"Numero di Hub (Nodi) totali: {num_nodi}" ))
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f"Numero di Tratte (Archi) valide {num_archi}",))

            #lista delle tratte (ordino per chiarezza visiva)
            lista_tratte_valide.sort(key=lambda tratta: tratta.guadagno_medio, reverse=True)

            indice= 0 #per avere il numerino vicino alla visualizzazione
            for elemento in lista_tratte_valide:
                self._view.lista_visualizzazione.controls.append(ft.Text(f"{indice}) "+ str(elemento)))
                indice+=1

        except ValueError:
            self._view.show_alert("Inserisci un valore numerico valido per il guadagno minimo.")
        except Exception as e:
            #errori generici
            self._view.show_alert(f"Si è verificato un errore inaspettato: {e}")

        self._view.update()