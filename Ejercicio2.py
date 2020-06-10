#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install pulp


# In[5]:


import pulp


# In[10]:


#Creamos el problema de transporte utilizando la variable prob
prob = pulp.LpProblem("Problema_de_distribución_de_cerveza", pulp.LpMinimize)


# In[8]:


# Creamos lista de cervecerías o nodos de oferta
cervecerias = ["Cervecería A", "Cervercería B"]

# diccionario con la capacidad de oferta de cada cerveceria
oferta = {"Cervecería A": 1000,
          "Cervercería B": 4000}

# Creamos la lista de los bares o nodos de demanda
bares = ["Bar 1", "Bar 2", "Bar 3", "Bar 4", "Bar 5"]

# diccionario con la capacidad de demanda de cada bar
demanda = {"Bar 1":500,
           "Bar 2":900,
           "Bar 3":1800,
           "Bar 4":200,
           "Bar 5":700,}

# Lista con los costos de transporte de cada nodo
costos = [   #Bares
         [2,4,5,2,1],#  Cervecerías
         [3,1,3,2,3]
         ]

# Convertimos los costos en un diccionario de PuLP
costos = pulp.makeDict([cervecerias, bares], costos,0)

# Creamos una lista de tuplas que contiene todas las posibles rutas de tranporte.
rutas = [(c,b) for c in cervecerias for b in bares]


# In[9]:


# creamos diccionario x que contendrá la candidad enviada en las rutas
x = pulp.LpVariable.dicts("ruta", (cervecerias, bares), 
                        lowBound = 0,
                        cat = pulp.LpInteger)

# Agregamos la función objetivo al problema
prob += sum([x[c][b]*costos[c][b] for (c,b) in rutas]),             "Suma_de_costos_de_transporte"

# Agregamos la restricción de máxima oferta de cada cervecería al problema.
for c in cervecerias:
    prob += sum([x[c][b] for b in bares]) <= oferta[c],             "Suma_de_Productos_que_salen_de_cervecerias_%s"%c

# Agregamos la restricción de demanda mínima de cada bar
for b in bares:
    prob += sum([x[c][b] for c in cervecerias]) >= demanda[b],     "Sum_of_Products_into_Bar%s"%b
                   
# Los datos del problema son exportado a archivo .lp
prob.writeLP("problemaDeTransporte.lp")

# Resolviendo el problema.
prob.solve()

# Imprimimos el estado del problema.
print("Status: {}".format(pulp.LpStatus[prob.status]))

# Imprimimos cada variable con su solución óptima.
for v in prob.variables():
    print("{0:} = {1:}".format(v.name, v.varValue))

# Imprimimos el valor óptimo de la función objetivo
print("Costo total de transporte = {}".format(prob.objective.value()))


# In[ ]:




