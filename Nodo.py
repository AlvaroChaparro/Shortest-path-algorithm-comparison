
class Nodo:

    def __init__(self, padre, estado, costo, accion, p, f=None):
        self.padre = padre
        self.estado = estado
        self.costo = costo
        self.accion = accion
        self.p = p
        self.f = f

    def get_id(self):
        return self.estado.get_posicionActual

    def get_padre(self):
        return self.padre

    def get_estado(self):
        return self.estado

    def get_p(self):
        return self.p

    def get_f(self):
        return self.f

    def get_accion(self):
        return self.accion

    def get_costo(self):
        return self.costo

    def set_f(self, f):
        self.f = f
