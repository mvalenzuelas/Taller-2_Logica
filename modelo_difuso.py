import skfuzzy as fuzz 
import numpy as np 
import matplotlib.pyplot as plt

def conseguirAntiguedad(pertenenciaModerno, pertenenciaNoTanAntiguo, pertenenciaAntiguo):
    # Se obtiene el maximo de las pertenencias
    pertenenciaMayor = max([pertenenciaModerno,pertenenciaNoTanAntiguo,pertenenciaAntiguo])
    #Se retorna una string que representa la antiguedad escogida:
    if pertenenciaMayor == pertenenciaModerno:
        return "moderno"
    if pertenenciaMayor == pertenenciaNoTanAntiguo:
        return "noTanAntiguo"
    return "antiguo"

def conseguirHabilidad(pertenenciaPocoHabil, pertenenciaAlgoHabil, pertenenciaMuyHabil):
    # Se obtiene el maximo de las pertenencias
    pertenenciaMayor = max([pertenenciaPocoHabil,pertenenciaAlgoHabil,pertenenciaMuyHabil])
    #Se retorna una string que representa la habilidad escogida:
    if pertenenciaMayor == pertenenciaPocoHabil:
        return "pocoHabil"
    if pertenenciaMayor == pertenenciaAlgoHabil:
        return "algoHabil"
    return "muyHabil"

def conseguirTiempo(pertenenciaPocoTiempo, pertenenciaAlgoDeTiempo, pertenenciaMuchoTiempo):
    # Se obtiene el maximo de las pertenencias
    pertenenciaMayor = max([pertenenciaPocoTiempo,pertenenciaAlgoDeTiempo,pertenenciaMuchoTiempo])
    #Se retorna una string que representa el tiempo libre escogido:
    if pertenenciaMayor == pertenenciaPocoTiempo:
        return "pocoTiempo"
    if pertenenciaMayor == pertenenciaAlgoDeTiempo:
        return "algoDeTiempo"
    return "muchoTiempo"

def entregarCategoria(grado_plataforma, grado_puzzle, grado_metroidvania, grado_sandox):
    mayorValor = max([grado_plataforma,grado_puzzle,grado_metroidvania,grado_sandox])
    if mayorValor == grado_plataforma:
        return 0, "Plataforma"
    if mayorValor == grado_puzzle:
        return 1, "Puzzle"
    if mayorValor == grado_metroidvania:
        return 2, "Metroidvania"
    if mayorValor == grado_sandox:
        return 3, "Sandbox"

class modeloDifuso:
    def __init__(self):
        # Creacion de escalas de rangos de valores a tomar
        self.rango_antiguedad = np.arange(0, 15, 0.1) # Antiguedad en años
        self.rango_habilidad = np.arange(0, 10, 0.1)# Escala del 1 al 10
        self.rango_tiempo = np.arange(0, 10, 0.1)# Horas semanales disponibles
        self.rango_genero = np.arange(0, 10, 0.1)

        # Fuzzificación de las variables de pertenencia
        ##Antiguedad##
        self.antiguedad_moderno = fuzz.sigmf(self.rango_antiguedad,6.0,-1.5) 
        self.antiguedad_noTanAntiguo = fuzz.gaussmf(self.rango_antiguedad,7.5,2.0)
        self.antiguedad_antiguo = fuzz.sigmf(self.rango_antiguedad,7.5,1.5)

        ##Habilidad##
        self.habilidad_pocoHabil = fuzz.trapmf(self.rango_habilidad,[0,0,2,4]) 
        self.habilidad_algoHabil = fuzz.gaussmf(self.rango_habilidad,5,1)
        self.habilidad_muyHabil = fuzz.trapmf(self.rango_habilidad,[6,7,10,10])

        ##Tiempo##
        self.tiempo_pocoTiempo = fuzz.trapmf(self.rango_tiempo,[0,0,2,4])
        self.tiempo_algoDeTiempo = fuzz.gaussmf(self.rango_tiempo,5,1)
        self.tiempo_muchoTiempo = fuzz.trapmf(self.rango_tiempo,[6,7,10,10])

        ##Genero##
        self.genero_plataforma = fuzz.trapmf(self.rango_genero, [0,0,2,3])
        self.genero_puzzle = fuzz.trimf(self.rango_genero, [2,4,5.5])
        self.genero_metroidvania = fuzz.trimf(self.rango_genero, [4.5, 6.5, 8.5])
        self.genero_sandbox = fuzz.trapmf(self.rango_genero, [7.5, 8, 10, 10])

        ## Base de datos de juegos:
        self.juegos_plataforma = [
            ["Mario Bros","antiguo","algoHabil","algoDeTiempo"],
            ["Megaman X","antiguo","muyHabil","pocoTiempo"],
            ["Cuphead","moderno","muyHabil","muchoTiempo"],
            ["Inside","noTanAntiguo","pocoHabil","pocoTiempo"]]

        self.juegos_puzzle = [
            ["Portal","antiguo","pocoHabil","algoDeTiempo"],
            ["It Takes Two","moderno","algoHabil","muchoTiempo"],
            ["Human: Fall Flat","noTanAntiguo","muyHabil","pocoTiempo"]]

        self.juegos_metroidvania = [
            ["Hollow Knight","noTanAntiguo","muyHabil","algoDeTiempo"],
            ["Ori and the Will of the Wisps","moderno","pocoHabil","muchoTiempo"],
            ["Super Metroid","antiguo","algoHabil","pocoTiempo"]]

        self.juegos_sandbox = [
            ["Minecraft","antiguo","muyHabil","muchoTiempo"],
            ["Hitman","noTanAntiguo","algoHabil","algoDeTiempo"],
            ["Genshin Impact","moderno","pocoHabil","pocoTiempo"]]

    def predecir(self,input_antiguedad, input_habilidad, input_tiempo, opcion_graficar):
        # Se consigue el grado de pertenencia para los inputs ingresados

        ## Grado de pertenencia para antiguedad ##
        grado_antiguedad_moderno = fuzz.interp_membership(self.rango_antiguedad, self.antiguedad_moderno, input_antiguedad)
        grado_antiguedad_noTanAntiguo = fuzz.interp_membership(self.rango_antiguedad, self.antiguedad_noTanAntiguo, input_antiguedad)
        grado_antiguedad_antiguo = fuzz.interp_membership(self.rango_antiguedad, self.antiguedad_antiguo, input_antiguedad)

        ## Grado de pertenencia para Habilidad ##
        grado_habilidad_pocoHabil = fuzz.interp_membership(self.rango_habilidad, self.habilidad_pocoHabil, input_habilidad)
        grado_habilidad_algoHabil = fuzz.interp_membership(self.rango_habilidad, self.habilidad_algoHabil, input_habilidad)
        grado_habilidad_muyHabil = fuzz.interp_membership(self.rango_habilidad, self.habilidad_muyHabil, input_habilidad)

        ## Grado de pertenencia para Tiempo ##
        grado_tiempo_pocoTiempo = fuzz.interp_membership(self.rango_tiempo, self.tiempo_pocoTiempo, input_tiempo)
        grado_tiempo_algoDeTiempo = fuzz.interp_membership(self.rango_tiempo, self.tiempo_algoDeTiempo, input_tiempo)
        grado_tiempo_muchoTiempo = fuzz.interp_membership(self.rango_tiempo, self.tiempo_muchoTiempo, input_tiempo)

        ## Implementación de inferencia de mamdani (Minimo-Maximo) a partir de reglas
        # OR = max | AND = min

        # Regla 1:
        # Si la Antiguedad es antiguo y la habilidad es algo habil y el tiempo es poco tiempo, entonces el genero es plataforma
        regla1 = np.fmin(np.fmin(grado_antiguedad_antiguo, grado_habilidad_algoHabil), grado_tiempo_pocoTiempo)

        # Regla 2:
        # Si la Antiguedad es antiguo y la habilidad es muy habil o el tiempo es algo de tiempo, entonces el genero es puzzle
        regla2 = np.fmax(np.fmin(grado_antiguedad_antiguo, grado_habilidad_muyHabil), grado_tiempo_algoDeTiempo)

        # Regla 3:
        # Si la antiguedad es antiguo y la habilidad es poco habil o el tiempo es poco tiempo, entonces el genero es plataforma
        regla3 = np.fmax(np.fmin(grado_antiguedad_antiguo, grado_habilidad_pocoHabil), grado_tiempo_pocoTiempo)

        # Regla 4:
        # Si la antiguedad es moderno y la habilidad es algo habil y el tiempo es mucho tiempo, entonces el genero es sandbox
        regla4 = np.fmin(np.fmin(grado_antiguedad_moderno, grado_habilidad_algoHabil), grado_tiempo_muchoTiempo)

        # Regla 5:
        # Si la antiguedad es moderno y la habilidad es muy habil y el tiempo es poco tiempo, entonces el genero es sandbox
        regla5 = np.fmin(np.fmin(grado_antiguedad_moderno, grado_habilidad_muyHabil), grado_tiempo_pocoTiempo)

        # Regla 6:
        # Si la antiguedad es no tan antiguo y la habilidad es muy habil y el tiempo es poco tiempo, entonces el genero es plataforma
        regla6 = np.fmin(np.fmin(grado_antiguedad_noTanAntiguo, grado_habilidad_muyHabil), grado_tiempo_pocoTiempo)

        # Regla 7:
        # Si la antiguedad es antiguo y la habilidad es poco habil y el tiempo es mucho tiempo, entonces el genero es Metroidvania
        regla7 = np.fmin(np.fmin(grado_antiguedad_antiguo, grado_habilidad_pocoHabil), grado_tiempo_muchoTiempo)

        # Se genera a continuacion la activación de cada regla vinculandola a su respuesta
        # recordar que en Mamdani al final se toma el minimo de cada recta
        activacion_regla1 = np.fmin(regla1, self.genero_plataforma)
        activacion_regla2 = np.fmin(regla2, self.genero_puzzle)
        activacion_regla3 = np.fmin(regla3, self.genero_plataforma)
        activacion_regla4 = np.fmin(regla4, self.genero_sandbox)
        activacion_regla5 = np.fmin(regla5, self.genero_sandbox)
        activacion_regla6 = np.fmin(regla6, self.genero_plataforma)
        activacion_regla7 = np.fmin(regla7, self.genero_metroidvania)

        # Finalmente mamdani ocupa agregación(calculando el maximo), para generar la union entre todas las areas/graficas conseguidas
        # y posteriormente a esta aplicarle un método de desfuzzificación

        agregacion = np.fmax(activacion_regla1,
                np.fmax(activacion_regla2,
                np.fmax(activacion_regla3,
                np.fmax(activacion_regla4,
                np.fmax(activacion_regla5,
                np.fmax(activacion_regla6,activacion_regla7))))))

        # Aplicar desfuzzificacion de centro de area (COA)
        desfuzzificacion = fuzz.defuzz(self.rango_genero, agregacion, 'centroid')

       #print(desfuzzificacion)

        # Para evaluar el resultado de la desfuzzificación se evalua su pertenencia dentro de las variables de genero
        grado_plataforma = fuzz.interp_membership(self.rango_genero, self.genero_plataforma, desfuzzificacion)
        grado_puzzle = fuzz.interp_membership(self.rango_genero, self.genero_puzzle, desfuzzificacion)
        grado_metroidvania = fuzz.interp_membership(self.rango_genero, self.genero_metroidvania, desfuzzificacion)
        grado_sandbox = fuzz.interp_membership(self.rango_genero, self.genero_sandbox, desfuzzificacion)

        #print(grado_plataforma)
        #print(grado_puzzle)
        #print(grado_metroidvania)
        #print(grado_sandbox)

        numCategoria, textoOutput = entregarCategoria(grado_plataforma, grado_puzzle, grado_metroidvania, grado_sandbox)

        # Ademas se retornaran los juegos que mejor se ajusten a las caracteristicas ingresadas, para esto
        # se conseguira que caracteristicas tienen el mayor grado de pertenencia para las entradas ingresadas

        antiguedad_seleccionada = conseguirAntiguedad(grado_antiguedad_moderno, grado_antiguedad_noTanAntiguo, grado_antiguedad_antiguo)
        habilidad_seleccionada = conseguirHabilidad(grado_habilidad_pocoHabil, grado_habilidad_algoHabil, grado_habilidad_muyHabil)
        tiempo_seleccionado = conseguirTiempo(grado_tiempo_pocoTiempo, grado_tiempo_algoDeTiempo, grado_tiempo_muchoTiempo)

        # Se consiguen los juegos que mejor se ajustan a las preferencias ingresadas
        juegosSeleccionados, juegosAlternativos = self.retornarListaJuegosPreferidos(numCategoria, antiguedad_seleccionada, habilidad_seleccionada, tiempo_seleccionado)
        # En caso el usuario haya solicitado mostrar el gráfico de resultado final con la desfusificación
        if opcion_graficar == "Si":
            self.graficarResultadoCoa(agregacion,desfuzzificacion)

        return textoOutput, juegosSeleccionados, juegosAlternativos

    def graficarFuncionesDePertenenciaDifusas(self):
        # Grafica de resumen generada
        plt.figure()
        filas = 2
        columnas = 2
        plt.subplot(filas,columnas,1)
        plt.title("Antiguedad")
        plt.plot(self.rango_antiguedad,self.antiguedad_moderno, label="Moderno", marker=".")
        plt.plot(self.rango_antiguedad,self.antiguedad_noTanAntiguo, label="No tan antiguo", marker=".")
        plt.plot(self.rango_antiguedad,self.antiguedad_antiguo, label="Antiguo", marker=".")
        plt.legend(loc="upper left")

        plt.subplot(filas,columnas,2)
        plt.title("Habilidad")
        plt.plot(self.rango_habilidad,self.habilidad_pocoHabil, label="Poco habil", marker=".")
        plt.plot(self.rango_habilidad,self.habilidad_algoHabil, label="Algo habil", marker=".")
        plt.plot(self.rango_habilidad,self.habilidad_muyHabil, label="Muy habil", marker=".")
        plt.legend(loc="upper left")

        plt.subplot(filas,columnas,3)
        plt.title("Tiempo")
        plt.plot(self.rango_habilidad,self.habilidad_pocoHabil, label="Poco tiempo", marker=".")
        plt.plot(self.rango_habilidad,self.habilidad_algoHabil, label="Algo de tiempo", marker=".")
        plt.plot(self.rango_habilidad,self.habilidad_muyHabil, label="Mucho tiempo", marker=".")
        plt.legend(loc="upper left")

        plt.subplot(filas,columnas,4)
        plt.title("Genero")
        plt.plot(self.rango_genero,self.genero_plataforma, label="Plataforma", marker=".")
        plt.plot(self.rango_genero,self.genero_puzzle, label="Puzzle", marker=".")
        plt.plot(self.rango_genero,self.genero_metroidvania, label="Metroidvania", marker=".")
        plt.plot(self.rango_genero,self.genero_sandbox, label="Sandbox", marker=".")
        plt.legend(loc="upper left")
        plt.show()

    def graficarResultadoCoa(self,agregacion,desfuzzificacion):
        ejeCero = np.zeros_like(self.rango_genero) # Auxiliar para graficar
        tip_activation = fuzz.interp_membership(self.rango_genero, agregacion, desfuzzificacion)
        fig, grafica = plt.subplots(figsize=(8, 3))
        # Se grafica el resultado conseguido con el centro de area y la figura conseguida
        grafica.plot(self.rango_genero, self.genero_plataforma, 'b', label="Plataforma", linewidth=0.5, linestyle='--', )
        grafica.plot(self.rango_genero, self.genero_puzzle, 'g', label="Puzzle", linewidth=0.5, linestyle='--')
        grafica.plot(self.rango_genero, self.genero_metroidvania, 'r', label="Metroivania", linewidth=0.5, linestyle='--')
        grafica.plot(self.rango_genero, self.genero_sandbox, 'purple', label="Sandbox", linewidth=0.5, linestyle='--')
        grafica.fill_between(self.rango_genero, ejeCero, agregacion, facecolor='Orange', alpha=0.7)
        grafica.plot([desfuzzificacion, desfuzzificacion], [0, tip_activation], 'k', linewidth=1.5, alpha=0.9)
        grafica.set_title('Funciones de pertenencias agregadas y resultado de COA (Línea negra)')
        grafica.legend()

        # Modificar ejes de la grafica
        for eje in (grafica,):
            eje.spines['top'].set_visible(False)
            eje.spines['right'].set_visible(False)
            eje.get_xaxis().tick_bottom()
            eje.get_yaxis().tick_left()

        plt.tight_layout()
        plt.show()

    def retornarListaJuegosPreferidos(self, numCategoria, antiguedad, habilidad, tiempo):
        juegosSeleccionados = []
        juegosAlternativos = []

        # Si la categoria escogida fue plataforma
        if(numCategoria == 0):
            arregloBusqueda = self.juegos_plataforma
        # Si la categoria escogida fue puzzle
        if(numCategoria == 1):
            arregloBusqueda = self.juegos_puzzle
        # Si la categoria escogida fue Metroidvania
        if(numCategoria == 2):
            arregloBusqueda = self.juegos_metroidvania
        # Si la categoria escogida fue Sandbox
        if(numCategoria == 3):
            arregloBusqueda = self.juegos_sandbox

        # Se busca el o los juegos que concuerden con las preferencias
        for juego in arregloBusqueda:
            if(juego[1] == antiguedad and juego[2] == habilidad and juego[3] == tiempo):
                juegosSeleccionados.append(juego)
        # Si ningún juego cumplio las caracteristicas por completo, se efectua una segunda busqueda
        if(len(juegosSeleccionados) == 0):
            for juego in arregloBusqueda:
                #Se agrega cualquier juego que cumpla con las caracteristicas, dejando una fuera
                if(juego[1] == antiguedad and juego[2] == habilidad):
                    juegosSeleccionados.append(juego)
        # Si ningún juego cumplio las caracteristicas por completo, se efectua una tercera busqueda, solo buscando una caracteristica
        if(len(juegosSeleccionados) == 0):
            for juego in arregloBusqueda:
                #Se agrega cualquier juego que cumpla con las caracteristicas, dejando una fuera
                if(juego[1] == antiguedad):
                    juegosSeleccionados.append(juego)
        # Si ningún juego cumplio con las caracteristicas, se muestran los juegos de la categoria correspondiente
        if(len(juegosSeleccionados) == 0):
            for juego in arregloBusqueda:
                juegosSeleccionados.append(juego)
            
        # Se agregan los juegos que no fueron seleccionados de la categoría
        for juego in arregloBusqueda:
            if juego not in juegosSeleccionados:
                juegosAlternativos.append(juego)
        
        return juegosSeleccionados, juegosAlternativos