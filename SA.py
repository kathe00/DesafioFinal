"""
Implementación de Simulated Annealing

Integrantes:
- Esteban González
- Priscilla Riffo
- Carlos Núñez
- Katherine Sepúlveda

"""

# librerías
import math
import random
import matplotlib.pyplot as plt
from instancia import Instancia

instancia = Instancia()

#--------------------------- Funciones para SA --------------------------------#

# Solución Inicial por medio de Selección Aleatoria Uniforme
def solucionInicial(instancia):
    # Selección Aleatoria Uniforme
    # 1. Tomar el orden incial:
    lista = list(range(1,instancia.tam+1)) # se crea una lista con los nros del 1 al tamaño
    solucion = [] # y una lista vacia para la solución

    # 2. Aplicar el algoritmo:
    while lista:
      # tomar una posición aleatoria (de 0 al largo de la lista)
      rand = random.randint(0, len(lista) - 1)
      
      # agregar el elemento a la solucion
      solucion.append(lista[rand])
      
      # quitar el elemento
      lista.pop(rand)

    # 3. Retornar la solución
    return solucion

# Criterio de término: temperatura mínima
def criterioTermino(temp_actual, temp_min):
  # mientras la temperatura sea mayor al minimo, continuar
  if (temp_actual >= temp_min):
    return True
  return False

# Siguiente vecino: SWAP
def siguienteVecino(solucion):
  sol = solucion.copy()
  
  # SWAP
  # 1. Elegir 2 posiciones randoms de la solución
  pos1 = random.randint(0, len(sol) - 1)
  pos2 = random.randint(0, len(sol) - 1)

  # verificar que no sean iguales
  while pos1 == pos2:
    pos2 = random.randint(0, len(sol) - 1)

  # 2. Hacemos el intercambio con ayuda de un auxiliar
  # guardamos el valor ubicado en la posición 1
  aux = sol[pos1]
  # cambiamos el valor de la posición 1 por la 2
  sol[pos1] = sol[pos2]
  # cambiamos el valor de la posicion 2 por el que estaba en la 1
  sol[pos2] = aux

  # 3. Retornamos la solución encontrada
  return sol

# Criterio de aceptación: Criterio de Metrópolis
def criterioAceptacion(actual, siguiente, temperatura):
  # Se aplica Criterio de Metrópolis
  delta = siguiente - actual
  #print(f"delta = {delta}")

  if delta < 0:
    # si el delta es negativo, la solución siguiente es mejor y se acepta automáticamente.
    return True 

  # probabilidad de aceptación si la solucion siguiente es peor
  div = (delta * -1) / temperatura
  prob = math.exp(div)
  nro = random.random()

  # se acepta según la probabilidad
  if ( nro < prob):
    return True
  
  return False

# Función Objetivo para QAP
def funcionObjetivo(solucion, instancia):
  # La función objetivo calcula el costo total de asignar un valor en una posición

  # Cálculo de la Función Objetivo
  # 1. Por cada sumatoria se realiza un ciclo for
  # el costo comienza en 0
  costo = 0
  for i in range(0, len(solucion)-1):
    for j in range (i+1, len(solucion)):

      # 2. Se calcula la distancia entre los elementos i y j
      # para esto, sumamos las distancias que hay de i a i+1, de i+1 a i+2
      # y así, hasta llegar a j
      distancia = 0
      for k in range(i,j):
        distancia += instancia.distancias[solucion[k]-1][solucion[k+1]-1]

      # 3. Ahora calculamos el flujo entre i y j
      flujo = instancia.flujos[solucion[i]-1][solucion[j]-1]

      # 3. Se multiplican y se suman al costo total
      costo += distancia * flujo
  
  # 4. Y retornamos el esfuerzo total calculado
  return costo

# ------------------------ Implementación del Algoritmo --------------------------#

# Definimos los parámetros
temp_inicial = 100000
temp_min = 0.02
alpha = 0.98

# 1. Primero, creamos la solución inicial, la establecemos como la mejor
# e inicializamos la temperatura 
solucion = solucionInicial(instancia)
mejor_solucion = solucion.copy()
temperatura = temp_inicial

iteraciones = 0 #contador de iteraciones
y = [funcionObjetivo(solucion, instancia)] #arreglo para guardar las soluciones encontradas

print("Solución inicial:")
print(solucion)
print(f"Función Objetivo: {funcionObjetivo(solucion, instancia)}\n")

# 2. Comenzamos la iteración. 
# Mientras se cumpla el criterio de término, se sigue iterando
while criterioTermino(temperatura, temp_min):
  iteraciones += 1
  # 3. Tomamos un vecino de la actual solucion
  solucion_sig = siguienteVecino(solucion)

  # 4. Calculamos las funciones objetivo de la solucion actual y la siguiente
  fObj = funcionObjetivo(solucion, instancia)
  fObj_sig = funcionObjetivo(solucion_sig, instancia)

  # 5. Evaluamos con el criterio de aceptación si será aceptada
  if criterioAceptacion(fObj, fObj_sig, temperatura):
    solucion = solucion_sig.copy()
    y.append(fObj_sig)
    
  # 6. Si la solución encontrada es mejor que la actual mejor solución, se cambia
  if funcionObjetivo(solucion, instancia) < funcionObjetivo(mejor_solucion, instancia):
    print(f"Nueva mejor solución encontrada: {fObj_sig}")
    mejor_solucion = solucion.copy()

  # 7. Enfriamos la temperatura
  temperatura = alpha * temperatura

# ----------------- Solución Final -------------------#
# Terminadas las iteraciones, obtenemos los resultados
print("***")
print(f"Mejor Solución: {mejor_solucion}")
print(f"Costo: {funcionObjetivo(mejor_solucion, instancia)}")
print(f"Iteraciones: {iteraciones}")

fig, ax = plt.subplots()
x = list(range(0,len(y)))
ax.plot(x,y)
plt.show()