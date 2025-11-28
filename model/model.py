from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = set()
        self._edges = []
        self._grafo = nx.Graph()
        self._dict_tratte = {}
        self._soglia_minima = 0.0
        self._id_to_hub: dict = {} #(keys = id_hub -> Hub (oggetto))

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """

        # Il grafo deve avere:
        # - tutti i nodi
        # - solo gli archi che soddisfano la condizione > soglia

        # Pulizia del grafico (good pratice)
        self._grafo.clear()
        self._edges.clear()

        self._soglia_minima = threshold

        if not self._dict_tratte:  # previene ricaricamento se è già stato fatto da creo_lista_delle_tratte_valide
            self._dict_tratte = self.creo_dizionario_delle_tratte()

        # self nodes è un set di oggetti Hub
        self._nodes = DAO.get_nodi()
        for node in self._nodes:
            self._grafo.add_node(node)

        self._id_to_hub = {hub.id: hub for hub in self._nodes}
        for (hub1_id, hub2_id), tratta in self._dict_tratte.items():  # coppia (chiave-valore)
            if tratta.guadagno_medio >= self._soglia_minima:

                # Ottiene gli oggetti Hub dal mapping
                hub1_obj = self._id_to_hub.get(hub1_id)
                hub2_obj = self._id_to_hub.get(hub2_id)

                if hub1_obj and hub2_obj:
                    # Aggiunge l'arco con il peso = guadagno medio
                    weight = tratta.guadagno_medio
                    self._grafo.add_edge(hub1_obj, hub2_obj, weight=weight)
                    self._edges.append(((hub1_obj, hub2_obj), weight)) # self._edges è una lista





    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        return self._grafo.number_of_edges()

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        return self._grafo.number_of_nodes()

    def creo_dizionario_delle_tratte(self):
        dizionario = DAO.get_dizionario_tratte()
        return dizionario
        # print(self._dict_tratte)
        # ho un dizionario che ha come chiavi le tuple (hub1, hub2) e come valore il valore della merce

    def creo_lista_delle_tratte_valide(self, soglia_minima):
        self._dict_tratte = self.creo_dizionario_delle_tratte()
        self._soglia_minima = soglia_minima

        # ora devo filtrare e devo restituire una lista che abbia solo le
        # tratte con valore/soglia sueriore a quella minimi

        lista_tratte_valide = []
        for tratta in self._dict_tratte.values():
            if tratta.guadagno_medio >= soglia_minima:
                lista_tratte_valide.append(tratta)

        return lista_tratte_valide