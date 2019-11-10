from Busqueda import *

graphlmfile="Ciudad Real/data/Manzanares.graphml.xml"
graph = Grafo(graphlmfile)
EspEstados = EspacioEstados(graphlmfile)

nodo = "2140711440"
nodos = ["960815541", "325794463"]
estado = Estado(nodo, nodos)

lista = EspEstados.sucesores(estado)
for item in lista:
    print("Estoy en "+str(item[1].posicionActual)+" y tengo que visitar "+str(item[1].listaNodos)+" y el coste hasta ahora es "+str(item[2]))

print("¿Cual es la estrategia? (0-Anchura 1-Profundidad 2-Coste-Uniforme 3-A* 4-Voraz)")
estrategia = int(input())

#prob = Problema("problema.json")
#prob = Problema("Almagro.json")
#prob = Problema("Arenales de San Gregorio.json")
prob = Problema("examen.json")

b = Busqueda()
b.Busqueda(prob, estrategia, 901, 900)
