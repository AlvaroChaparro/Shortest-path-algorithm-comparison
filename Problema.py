import networkx as nx
import json
from Estado import *
from EspacioEstados import *

class Problema:

    def __init__(self, file):
        with open(file) as f:  # Leemos el archivo json
            data = json.load(f)
        graphmlfile = data["graphlmfile"] + '.xml'  # Cogemos el nombre del fichero para construir el grafo y
                    # arreglamos el nombre añadiendo al final ".xml" que es como de verdad se llaman los ficheros

        nodoini = data['IntSt']['node']  # Capturamos el nodo inicial
        nodosproblem = data['IntSt']['listNodes']  # Capturamos los nodos que quedan por recorrer
        ide = data['IntSt']['id']
        self.estadoinicial = Estado(nodoini, nodosproblem, ide)  # Guardamos el estado inicial del problema
        self.espacioDeEstados = EspacioEstados(graphmlfile)

    def esObjetivo(self, estado):
        if len(estado.listaNodos) == 0:
            return True
        else:
            return False

    @property
    def get_estadoinicial(self):
        return self.estadoinicial

    @property
    def set_estadoinicial(self, estadoinicial):
        self.estadoinicial = estadoinicial

    @property
    def get_espacioDeEstados(self):
        return self.espacioDeEstados

    @property
    def set_espacioDeEstados(self, espacioDeEstados):
        self.espacioDeEstados = espacioDeEstados