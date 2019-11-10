
class Frontera:

    def __init__(self):
        self.frontera = []

    def Insertar(self, nodoArbol):
        self.frontera.append(nodoArbol)
        self.frontera.sort(key=lambda x: x.f)   #Ordenacion de nodos por el parametro f

    def Elimina(self):
        primerNodo = self.frontera[0]
        self.frontera.remove(self.frontera[0])
        return primerNodo

    def EsVacia(self):
        if len(self.frontera) == 0:
            return True
        else:
            return False
