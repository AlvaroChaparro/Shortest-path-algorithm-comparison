from GenerateGPX import GenerateGPX
from Frontera import *
from Problema import *
import math


class Busqueda:

    def Busqueda(self, Prob, estrategia, Prof_Max, Inc_Prof = None):

        prof_Actual = Inc_Prof
        solucion = None
        self.EspEstados = Prob.get_espacioDeEstados
        self.listaIni = Prob.get_estadoinicial.listaNodos

        while solucion is None and prof_Actual <= Prof_Max:
            solucion = self.Busqueda_Acotada(Prob, estrategia, prof_Actual)
            prof_Actual = prof_Actual + Inc_Prof

        if solucion == None:
            print("No se encontró una solución")
            return None
        else:
            return solucion

    def Busqueda_Acotada(self, Prob, estrategia, Prof_Max):
        # Estrategias: 0-Anchura 1-Profundidad 2-Coste-Uniforme 3-A* 4-Voraz
        if estrategia not in [0, 1, 2, 3, 4]:
            estrategia = 0
        else:
            estrategia = estrategia

        frontera = Frontera()
        estadoinicial = Prob.get_estadoinicial()
        n_inicial = Nodo(None, estadoinicial, 0, None, 0, 0)

        frontera.Insertar(n_inicial)
        solucion = False
        n_actual = None
        nodos = []
        nodosvisitados = []
        totalnodosgenerados = 0
        exitW = None

        while not solucion and not frontera.EsVacia():
            exitW = 0
            n_actual = frontera.Elimina()
            while n_actual.p > Prof_Max:
                n_actual = frontera.Elimina()
                if frontera.EsVacia() and n_actual > Prof_Max:
                    break

            nodos = list.copy(n_actual.estado.listaNodos)
            numeronodoactual = n_actual.get_id()

            # Recorremos los nodos visitados y si encontramos uno con el mismo estado
            # y menor costo descartamos el nodo actual
            for nodoid in nodosvisitados:
                if nodoid.estado.ID == n_actual.estado.ID and nodoid.costo < n_actual.costo:
                    exitW = 1
                    break
            #Condicion de cambio de iteracion del bucle
            if exitW == 1:
                continue

            totalnodosgenerados += 1
            nodosvisitados.append(n_actual)

            if numeronodoactual in nodos:
                nodos.remove(numeronodoactual)

            estado = Estado(numeronodoactual, nodos)  # Para crear el nuevo estado actual
            if Prob.esObjetivo(estado):  # Si el nuevo estado es objetivo
                solucion = True  # Ya tenemos una solucion
                break
            else:
                listaSucesores = list.copy(self.EspEstados.sucesores(estado))
                listaNodos = list.copy(self.CreaListaNodosArbol(listaSucesores, n_actual, Prof_Max, estrategia))
                for nodosrestantes in listaNodos:
                    frontera.Insertar(nodosrestantes)

        if solucion:
            return self.creaSolucion(n_actual, estrategia, totalnodosgenerados)
        else:
            return None

    def CreaListaNodosArbol(self, listaSucesores, n_actual, Prof_Max, estrategia):
        listaNodos = []
        #Si los nodos van a sobrepasar el limite no se generan
        if n_actual.get_p() + 1 > Prof_Max or listaNodos is None:
            return listaNodos
        for sucesor in listaSucesores:
            nodo = Nodo(n_actual, sucesor[1], (n_actual.costo+sucesor[2]), sucesor[0],
                        n_actual.get_p() + 1, 0)
            nodo.set_f(self.calcularF(estrategia, nodo))
            listaNodos.append(nodo)
        return listaNodos

    def calcularF(self, estrategia, nodo):
        #Switch de  estrategias
        listaEstrategias = {0: self.anchura,
                            1: self.profundidad,
                            2: self.coste,
                            3: self.estrategiaA,
                            4: self.voraz}
        f = listaEstrategias[estrategia](nodo)
        return f

    def anchura(self, nodo):  # Metodo de calculo de f en Anchura
        return nodo.p

    def profundidad(self, nodo):  # Metodo de calculo de f en Profundidad
        return -nodo.p

    def coste(self, nodo):  # Metodo de calculo de f en Coste Uniforme
        return float(nodo.get_costo())

    # Metodo para calcular la distancia
    # idNodo = Posicion del nodo (nodo.estado.posicionActual)
    def distance(self, nodo, i):
        idNode1 = nodo.estado.posicionActual
        idNode2 = nodo.estado.listaNodos[i]

        (lng1, lat1) = self.EspEstados.graph.posicionnodo(idNode1)
        (lng2, lat2) = self.EspEstados.graph.posicionnodo(idNode2)
        earth_radius = 6371009

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        d_phi = phi2 - phi1

        theta1 = math.radians(lng1)
        theta2 = math.radians(lng2)
        d_theta = theta2 - theta1

        h = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_theta / 2) ** 2
        h = min(1.0, h)  # protect against floating point errors

        arc = 2 * math.asin(math.sqrt(h))
        # return distance in units of earth_radius
        dist = arc * earth_radius
        return dist

    #Calculo de h con la distancia al nodo mas cercano de la lista de pendientes
    def calcularH(self, nodo):
        h = 0
        length = len(nodo.estado.listaNodos)
        for i in range(0, length-1):
            actual = self.distance(nodo, i)
            if actual < h or i == 0 or h == 0:
                h = actual
        return h

    # Calculamos f de la estrategia A con la suma de h y el costo
    def estrategiaA(self, nodo):
        return self.calcularH(nodo) + float(nodo.get_costo())

    #Calculamos f de la estrategia Voraz con el calculo de h
    def voraz(self, nodo):
        return self.calcularH(nodo)

    def creaSolucion(self, n_actual, estrategia, totalnodosgenerados):
        #Lista de nodos o acciones recorridos hasta la solucion
        nodos = []
        while not n_actual.get_padre() == None:
            nodos.append(n_actual)
            n_actual = n_actual.get_padre()

        #Creamos el string con la solucion
        solucion = "La solucion es: \n"
        for i in reversed(range(0, len(nodos))):
            if (str(nodos[i].get_id()) in self.listaIni):
                solucion += ("\n" + str(nodos[i].get_padre().get_id()) + " -> " + str(nodos[i].get_id()) + " " +
                             str(nodos[i].get_accion()) + " " + str(round(nodos[i].get_costo(), 1)) + " "
                             + str(nodos[i].get_p()) + " " + str(round(nodos[i].get_f(), 1)))
                solucion += ("\nEstoy en " + str(nodos[i].get_id()) + " y tengo que visitar [ ")
                for j in range(0, len(nodos[i - 1].get_estado().get_listaNodos)):
                    if (i == 0):
                        solucion += ("")
                    else:
                        solucion += ("'" + str(nodos[i - 1].get_estado().get_listaNodos[j]) + "', ")
                solucion += ("]\n")


        print(solucion)

        ultimonodo = nodos[0]
        costoTotal = nodos[0].costo
        nodos.append(n_actual)

        #Escribimos la solucion en el archivo de texto
        file = open("solucion.txt", "w")
        file.truncate()
        file.write(solucion)

        #Cogemos la lista de posiciones recorridas por la solucion
        listaPuntos = [None] * len(nodos)
        for i in reversed(range(0, len(nodos))):
            listaPuntos[i] = self.EspEstados.graph.posicionnodo(nodos[i].estado.posicionActual)

        #Generamos el archivo gpx y lo enseñamos en el navegador
        a = GenerateGPX(listaPuntos)
        a.crearVista()

        print("Estrategia:")
        if estrategia == 0:
            print("\tAnchura")
        if estrategia == 1:
            print("\tProfundidad")
        if estrategia == 2:
            print("\tCoste-Uniforme")
        if estrategia == 3:
            print("\tA*")
        if estrategia == 4:
            print("\tVoraz")

        print("Total nodos generados: "+ str(totalnodosgenerados))
        print("Profundidad: "+ str(ultimonodo.get_p() + 1))
        print("Costo: "+ str(round(costoTotal, 1)))

        return nodos
