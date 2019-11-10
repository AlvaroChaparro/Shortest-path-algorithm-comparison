#import networkx as nx
from Grafo import *
import hashlib

class Estado:

    def __init__(self, actual, listanodo=None, ide=None):
        self.posicionActual = actual
        if listanodo == None:
            self.listaNodos = []  # Ordenacion de nodos por id nodo final de cada arista
        else:
            self.listaNodos = listanodo
        # Guardamos los nodos adyacentes a la posicion actual
        if ide == None: #Si no pasan un id lo calculamos
            temphash = hashlib.md5()  # Llamamos al md5
            temphash.update(self.posicionActual.encode('utf-8'))  # Le metemos la posicion actual
            temphash.update(repr(self.listaNodos).encode('utf-8')) # Y la lista de nodos adyacentes
            self.ID = temphash.digest()  # Y calculamos el hash
        else:
            self.ID = ide #Si nos pasan un id se lo asignamos

    def __call__(self):
        return self

    @property
    def get_posicionActual(self):
        return self.posicionActual
    @property
    def get_listaNodos(self):
        #return [self.listaNodos]
        return self.listaNodos

    @property
    def get_ID(self):
        return self.ID


