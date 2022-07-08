import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Antecedente
antiguedad = ctrl.Antecedent(np.arange(0, 15, 0.1), 'antiguedad') # Antiguedad en años
habilidad = ctrl.Antecedent(np.arange(0, 10, 0.1), 'habilidad') # Escala del 1 al 10
tiempo = ctrl.Antecedent(np.arange(0, 10, 0.1), 'tiempo') # Horas semanales disponibles
# Consecuente
genero = ctrl.Consequent(np.arange(0, 1, 0.01), 'genero') 

#Establecer funciones de pertenencia
#Etiqueta
etiquetas_antiguedad = ['Moderno','No tan antiguo','Antiguo']
# Auto genera funciones de membresia
antiguedad.automf(names = etiquetas_antiguedad)
#Antiguedad
#antiguedad['Moderno'] = fuzz.sigmf(antiguedad.universe,6.0,-1.5)
#antiguedad['No tan antiguo'] = fuzz.gaussmf(antiguedad.universe,7.5,2.0)
#antiguedad['Antiguo'] = fuzz.sigmf(antiguedad.universe,7.5,1.5)
#Habilidad
etiquetas_habilidad = ['Muy habil','Algo habil', 'Poco habil']
habilidad.automf(names = etiquetas_habilidad)
#Tiempo
etiquetas_tiempo = ['Poco tiempo', 'Algo de tiempo', 'Mucho tiempo']
tiempo.automf(names = etiquetas_tiempo)
#Genero
etiquetas_genero = ['Plataforma','Puzzle','Metroidvania','Sandbox']
#genero['Plataforma'] = fuzz.trapmf(genero.universe,[0,0,0.25,0.25])
#genero['Puzzle'] = fuzz.trapmf(genero.universe,[0.25,0.25,0.50,0.50])
#genero['Metroidvania'] = fuzz.trapmf(genero.universe,[0.50,0.50,0.75,0.75])
#genero['Sandbox'] = fuzz.trapmf(genero.universe,[0.75,0.75,1.0,1.0])
genero.automf(names = etiquetas_genero)

# Reglas para el modelo de logica difusa
regla1 = ctrl.Rule(antiguedad['Antiguo'] & habilidad['Algo habil'] & tiempo['Poco tiempo'], genero['Plataforma'])
regla2 = ctrl.Rule(tiempo['Algo de tiempo'] | habilidad['Muy habil'] & antiguedad['Antiguo'], genero['Metroidvania'])
regla3 = ctrl.Rule(tiempo['Poco tiempo'] | habilidad['Poco habil'] & antiguedad['Antiguo'], genero['Puzzle'])
regla4 = ctrl.Rule(antiguedad['Moderno'] & tiempo['Mucho tiempo'] & habilidad['Algo habil'], genero['Sandbox'])
regla5 = ctrl.Rule(habilidad['Muy habil'] & tiempo['Algo de tiempo'], genero['Sandbox'])
regla6 = ctrl.Rule(antiguedad['No tan antiguo'] & habilidad['Algo habil'], genero['Sandbox'])
regla7 = ctrl.Rule(tiempo['Mucho tiempo'] & habilidad['Algo habil'] & antiguedad['Antiguo'], genero['Metroidvania'])

# Se crea el sistema de control
reglas = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7])
# Creacion de simulador
simulador = ctrl.ControlSystemSimulation(reglas)

# Se hace una simulacion
simulador.input['antiguedad'] = 10
simulador.input['habilidad'] = 5
simulador.input['tiempo'] = 10
simulador.compute() # Mamdani
print(simulador.output['genero'])
genero.view(sim = simulador)

#generar graficos
antiguedad.view()
genero.view()
habilidad.view()
tiempo.view()
plt.show()