from database.DB_connect import DBConnect
from model.hub import Hub
from model.tratta import Tratta
class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def get_nodi():
        conn = DBConnect.get_connection()
        set_hub = set()
        query = """ Select id, nome
                    from Hub
                    """

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query)

            for row in cursor:
                hub = Hub(row["id"], row["nome"])
                set_hub.add(hub)

        except Exception as e:
            print(f"Errore durante la query get_attrazioni: {e}")
        finally:
            cursor.close()
            conn.close()

        return set_hub

    @staticmethod
    def get_dizionario_tratte():
        conn = DBConnect.get_connection()
        dizionario_tratte = {}
        query = """ Select id_hub_origine, id_hub_destinazione, valore_merce
                    from spedizione
                    """

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query)

            for row in cursor:
                #ciclo su tutte le tratte che ho:
                primo_hub = max(int(row["id_hub_origine"]), int(row["id_hub_destinazione"]))
                secondo_hub = min(int(row["id_hub_origine"]), int(row["id_hub_destinazione"]))
                #creo un oggetto Tratta:
                tratta = Tratta(primo_hub, secondo_hub, row["valore_merce"], contatore = 1)

                chiave = (int(primo_hub), int(secondo_hub))

                if chiave in dizionario_tratte.keys() :
                    oggetto_tratta = dizionario_tratte[chiave]
                    oggetto_tratta.valore_merce += row["valore_merce"]
                    oggetto_tratta.contatore += 1
                    dizionario_tratte[chiave] = oggetto_tratta
                else:
                    dizionario_tratte[chiave] = tratta
        except Exception as e:
            print(f"Errore durante la query get_attrazioni: {e}")
            dizionario_tratte = None
        finally:
            cursor.close()
            conn.close()

        return dizionario_tratte

