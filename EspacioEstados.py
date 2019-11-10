from Estado import *
from Grafo import *
import networkx as nx


class EspacioEstados:
    def __init__(self, file):
        self.graph = Grafo(file)  # Creamos el grafo a partir del fichero graphlm

    def sucesores(self, state):
        actual = state.get_posicionActual  # Obtenemos la posicion actual y la marcamos como el origen
        sucesores = []  # Creamos una lista vacia de sucesores
        listadenodos = self.graph.adyacentesnodo(actual)

        #Ver cuando listadenodos es NoneType
        if listadenodos is None:
            return sucesores

        for sucesor in listadenodos:  # Para cada nodo:
            destino = sucesor[1]  # marcamos el sucesor como destino
            #accM = 'Ir por ' + self.graph.get_nombrecalle(actual, destino)
            accM = '(' + self.graph.get_nombrecalle(actual, destino) + ')'
            costAcci = float(sucesor[3])
            #costAcci = self.graph.get_coste(actual, destino)  # buscamos el coste en el grafo entre esos dos nodos
            try:
                listadenodos.remove(actual)
            except ValueError:
                pass
            estadoNuevoM = Estado(destino, list.copy(state.listaNodos))  # Creamos el nuevo estado desde el nodo destino
            actual = destino  # Cambiamos la posicion actual
            sucesores.append([accM, estadoNuevoM, costAcci])  # Añadimos el sucesor a la lista en el formato pedido
        return sucesores

    def esta(self, state):  # Nos dice si state está en el espacio de estados
        for nodososm in self.graph.listanodos():
            if state.get_posicionActual() == nodososm[0]:
                return True
        return False