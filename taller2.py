import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Antecedente
antiguedad = ctrl.Antecedent(np.arange(0, 15, 0.1), 'antiguedad')  # Antiguedad en años
habilidad = ctrl.Antecedent(np.arange(0, 10, 0.1), 'habilidad')  # Escala del 1 al 10
tiempo = ctrl.Antecedent(np.arange(0, 10, 0.1), 'tiempo')  # Horas semanales disponibles
# Consecuente
genero = ctrl.Consequent(np.arange(0, 8, 0.1), 'genero')

# Establecer funciones de pertenencia
# Antiguedad
etiquetas_antiguedad = ['Moderno', 'No tan antiguo', 'Antiguo']
antiguedad['Moderno'] = fuzz.trapmf(antiguedad.universe, [0, 0, 3, 6])
antiguedad['No tan antiguo'] = fuzz.trimf(antiguedad.universe, [4.5, 7.5, 10.5])
antiguedad['Antiguo'] = fuzz.trapmf(antiguedad.universe, [9, 10, 15, 15])
# Habilidad
etiquetas_habilidad = ['Muy habil', 'Algo habil', 'Poco habil']
habilidad['Poco habil'] = fuzz.trapmf(habilidad.universe, [0, 0, 2, 4])
habilidad['Algo habil'] = fuzz.trimf(habilidad.universe, [3, 5, 7])
habilidad['Muy habil'] = fuzz.trapmf(habilidad.universe, [6, 7, 10, 10])

# Tiempo
etiquetas_tiempo = ['Poco tiempo', 'Algo de tiempo', 'Mucho tiempo']
tiempo.automf(names=etiquetas_tiempo)

# Genero
etiquetas_genero = ['Plataforma', 'Puzzle', 'Metroidvania', 'Sandbox']
genero['Plataforma'] = fuzz.trapmf(genero.universe, [0, 0, 2, 3])
genero['Puzzle'] = fuzz.trimf(genero.universe, [1, 3, 5])
genero['Sandbox'] = fuzz.trimf(genero.universe, [3, 5, 7])
genero['Metroidvania'] = fuzz.trapmf(genero.universe, [5, 6, 8, 8])

# Reglas para el modelo de logica difusa
regla1 = ctrl.Rule(tiempo['Poco tiempo'] & habilidad['Algo habil'] & antiguedad['Antiguo'], genero['Plataforma'])
regla2 = ctrl.Rule(tiempo['Algo de tiempo'] | habilidad['Muy habil'] & antiguedad['Antiguo'], genero['Puzzle'])
regla3 = ctrl.Rule(tiempo['Poco tiempo'] | habilidad['Poco habil'] & antiguedad['Antiguo'], genero['Plataforma'])
regla4 = ctrl.Rule(tiempo['Mucho tiempo'] & habilidad['Algo habil'] & antiguedad['Moderno'], genero['Sandbox'])
regla5 = ctrl.Rule(tiempo['Poco tiempo'] & habilidad['Muy habil'] & antiguedad['Moderno'], genero['Sandbox'])
regla6 = ctrl.Rule(tiempo['Poco tiempo'] & habilidad['Muy habil'] & antiguedad['No tan antiguo'], genero['Plataforma'])
regla7 = ctrl.Rule(tiempo['Mucho tiempo'] & habilidad['Poco habil'] & antiguedad['Antiguo'], genero['Metroidvania'])

# Se crea el sistema de control
reglas = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7])
# Creacion de simulador
simulador = ctrl.ControlSystemSimulation(reglas)

# Se hace una simulacion
simulador.input['tiempo'] = 0
simulador.input['habilidad'] = 5
simulador.input['antiguedad'] = 15

simulador.compute()  # Mamdani
print(simulador.output['genero'])
genero.view(sim=simulador)

# generar graficos
antiguedad.view()
genero.view()
habilidad.view()
tiempo.view()
plt.show()
