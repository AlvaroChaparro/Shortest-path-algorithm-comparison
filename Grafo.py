import networkx as nx
from Nodo import *


class Grafo:

    def __init__(self, files):  # Constructor de la clase Grafo
        self.graph = nx.Graph()
        try:
            self.graph = nx.read_graphml(files)
        except SyntaxError:
            print("El archivo no es valido")

    def pertenecenodo(self, ide):   # Devuelve si el nodo pertenece o no al grafo
        return self.graph.has_node(ide)

    def posicionnodo(self, ide):    # Devuelve longitud y latitud del nodo (como str) o error si no está en el grafo
        if self.pertenecenodo(ide):
            long = float(self.graph.node[ide]['y'])
            lat = float(self.graph.node[ide]['x'])
            return (long, lat)
            #lista = [self.graph.node[ide]['y'], self.graph.node[ide]['x']]
            #return lista
        else:
            print("Error. Ese nodo no está en el grafo.")
            return None

    def adyacentesnodo(self, ide):   # Devuelve la lista de aristas que salen de ide, en el formato pedido
        vecinos = self.graph.edges(ide, data=True)  # Devuelve una lista con las aristas que salen del nodo ide
        numerovecinos = 0   # Variable para contar el número de aristas que salen de ide
        aristas = []    # Aquí iremos guardando cada arista en el formato pedido
        for neighbor in vecinos:
            try:
                nombre = neighbor[2]['name']
            except KeyError:
                nombre = 'SinNombre'
            edge = [neighbor[0], neighbor[1], nombre, neighbor[2]['length']]
            aristas.append(edge)
            numerovecinos += 1
        if numerovecinos == 0:
            #print("No tiene nodos adyacentes.")
            return None
        else:
            return aristas

    @property
    def get_grafo(self):
        return self.graph

    def listanodos(self):
        return self.graph.nodes()

    def get_nombrecalle(self, destino, origen):
        nodos = self.graph.edges.data('name', origen)
        for nodo in nodos:
            if nodo[1] == destino:
                if nodo[2] is not None:
                    return nodo[2]
                else:
                    return 'SinNombre'
