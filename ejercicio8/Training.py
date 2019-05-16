from Juego import *
from Jugadores import *
import Graficar
import sys
import os

uso = """
Invocar como python3 Training.py [nombre directorio] [jugador1] [jugador2] [numero de partidas] [diferencia]
donde jugador1 y jugador2 pueden ser una ruta a un archivo con pesos o "Aleatorio".
"nombre directorio" es el nombre del directorio en donde se guardan los resultados.
Los pesos deben estar escritos en una sola línea y separados por espacios.
En el caso en que ambos sean AIs, los pesos de la AI más reciente deben pasarse
en jugador1. La AI que entrena siempre es la que se pasa en jugador 1. 
Al menos uno de los jugadores debe ser una AI.
El parámetro "diferencia" solo es obligatorio cuando ambos jugadores son AI.
Indica el número de partidas de distancia entre el AI y su versión previa.
Debe ser un valor entero y positivo.
"""

'''
Jugar a modo de entrenamiento el número de partidas indicas por parámetro.
Imprime en consola el número de partidas ganadas por la AI en caso que juege una.
'''

if __name__ == '__main__':
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))
    #Chequear número y valores de los argumentos
    if not(len(sys.argv) == 5 or len(sys.argv) == 6):
        print("***Número incorrecto de parámetros***")
        print(uso)
        exit()

    directorio = sys.argv[1]
    jugador1_str = sys.argv[2]
    jugador2_str = sys.argv[3]
    num_partidas = int(sys.argv[4])

    jugadores = []
    diferencia_partidas = None      # Indica las partidas de distancia entre la AI y su versión previa. También indica que juegan dos AIs si no es None.
    print("Creando jugadores")
    # Ambos son AIs. Solo el jugador1 entrena. Le pasa sus pesos a jugador2 cada "diferencia_partidas"
    if jugador1_str != "Aleatorio" and jugador2_str != "Aleatorio":
        lista_pesos_previos = []      # para pasarselos a la "versión previa" de la AI
        jugadores = ["AI1", "AI2"]
        jugador1 = AI(Color.Blancas, "AI1", None, True, factor_aprendizaje)
        print("Leyendo pesos del jugador 1")
        jugador1.cargar_pesos(jugador1_str)
        jugador2 = AI(Color.Negras, "AI2", None, False, factor_aprendizaje)
        print("Leyendo pesos del jugador 2")
        jugador2.cargar_pesos(jugador2_str)
        jugador2.alternar_pesos()
        if len(sys.argv) == 6:
            diferencia_partidas = int(sys.argv[5])
            if diferencia_partidas <= 0:
                print("***Valor incorrecto en la diferencia de partidas. Debe ser positivo.***")
                print(uso)
                exit()
    # Solo el primero es AI
    elif jugador1_str != "Aleatorio" and jugador2_str == "Aleatorio":
        jugadores = ["AI", "Aleatorio"]
        jugador1 = AI(Color.Blancas, "AI", None, True, factor_aprendizaje)
        print("Leyendo pesos del jugador 1")
        jugador1.cargar_pesos(jugador1_str)
        jugador2 = Aleatorio(Color.Negras, "Aleatorio")
    # Solo el segundo es AI
    elif jugador1_str == "Aleatorio" and jugador2_str != "Aleatorio":
        jugadores = ["Aleatorio", "AI"]
        jugador1 = AI(Color.Blancas, "AI", None, True, factor_aprendizaje)
        jugador2 = Aleatorio(Color.Negras, "Aleatorio")
        print("Leyendo pesos del jugador 2")
        jugador1.cargar_pesos(jugador2_str)
    # Ninguno es AI
    else:
        print("***Valores de jugadores incorrectos. Al menos uno debe ser una AI.***")
        print(uso)
        exit()

    victorias = 0
    empates = 0

    # Crear un directorio para guardar los datos de entrenamiento
    os.mkdir(directorio)
    print("Se crea el directorio {dir}".format(dir=directorio))

    # Almacena la cantidad de victorias cada 10, 20, 30 ... partidas
    evolucion_victorias = []
    # Almacena la cantidad de empates cada 10, 20, 30 ... partidas
    evolucion_empates = []
    evolucion_victorias_formateado = []
    evolucion_empates_formateado = []
    victorias_aux = None
    empates_aux = None
    partidos_desde_ultimo_ajuste = 0
    color_que_empieza = Color.Blancas

    print("Comenzando la serie de partidas")
    for i in range(num_partidas):
        print("Comenzando partida {num}".format(num=i+1))
        # Crear archivo vacio para los valores de entrenamiento
        try:
            # Se agrega un timestamp al nombre del archivo para que queden ordenados
            ruta_archivo_entrenamiento = directorio + "/" + "partida{num}".format(num=i) + ".txt"
            ruta_archivo_pesos = directorio + "/" + "peso"
            open(ruta_archivo_entrenamiento, "w").close()
            # Avisar a jugador cual es el archivo sobre el cual escribira las tuplas
            jugador1.set_archivo_entrenamiento(ruta_archivo_entrenamiento)
            jugador1.set_archivo_pesos(ruta_archivo_pesos)
        except Exception as e:
            print("Training.py: Error creando el archivo de entrenamiento")
            raise e
        juego = Juego(jugador2, jugador1)
        ganador = juego.jugar(color_que_empieza)
        color_que_empieza = Color.Blancas if (color_que_empieza == Color.Negras) else Color.Negras
        #Para debugging
        print("Partida {partida} => Ganó {ganador}.".format(partida=i+1, ganador=ganador))
        # Chequear que el ganador sea la AI o la AI más reciente (AI1)
        if ganador is not None and "AI" in ganador:
            if ganador != "AI2":
                victorias += 1
        elif ganador is None:
            empates += 1
        print("Victorias = {victorias}".format(victorias=victorias))
        print("Empates = {empates}".format(empates=empates))
        # Llamar ajuste de minimos cuadrados de Jugadores.py
        jugador1.ajuste_minimos_cuadrados()
        # Decidir y actualizar los pesos de la version previa del AI2
        if not(diferencia_partidas is None):
            # Registrar los pesos para pasarselos a la "versión previa" de la AI
            lista_pesos_previos = jugador1.pesos.copy()
            # Comenzar a pasarle los pesos previos de la AI
            if partidos_desde_ultimo_ajuste >= diferencia_partidas:
                # Ajustar el signo de los pesos que le pasamos a la otra AI
                jugador2.pesos = lista_pesos_previos
                jugador2.alternar_pesos()
                partidos_desde_ultimo_ajuste = 0
            else:
                partidos_desde_ultimo_ajuste += 1

        # Actualizar evolución de victorias y empates de la AI (si num_partidas es al menos 30)
        # cada 10 partidas
        if victorias_aux is None:
            victorias_aux = 0
        if empates_aux is None:
            empates_aux = 0
        
        if num_partidas >= 30 and diferencia_partidas is not None:
            if (i+1) % diferencia_partidas == 0:
                # Registrar rango de victorias
                victorias_rango = victorias - victorias_aux 
                evolucion_victorias.append(victorias_rango)
                victorias_aux = victorias
                # Registrar rango de empates
                empates_rango = empates - empates_aux
                evolucion_empates.append(empates_rango)
                empates_aux = empates
        elif diferencia_partidas is None:
            if (i+1) % 10 == 0:
                # Registrar rango de victorias
                victorias_rango = victorias - victorias_aux 
                evolucion_victorias.append(victorias_rango)
                victorias_aux = victorias
                # Registrar rango de empates
                empates_rango = empates - empates_aux
                evolucion_empates.append(empates_rango)
                empates_aux = empates

    # Imprimr los resultados de la evolución de victorias de la AI
    print("Evolución de victorias de la AI")
    for i in range(len(evolucion_victorias)):
        if diferencia_partidas is not None:
            string_evol_vict_formateado = "AI: {ganadas} / {dif_p} => {porcentaje}%".format(ganadas=evolucion_victorias[i], dif_p = diferencia_partidas, porcentaje=evolucion_victorias[i]/diferencia_partidas*100)            
        else:
            string_evol_vict_formateado = "AI: {ganadas} / 10 => {porcentaje}%".format(ganadas=evolucion_victorias[i], porcentaje=evolucion_victorias[i]/10*100)
        print(string_evol_vict_formateado)
        string_evol_vict_formateado += "\n"
        evolucion_victorias_formateado.append(string_evol_vict_formateado)
    # Imprimr los resultados de la evolución de victorias de la AI
    print("Evolución de empates")
    for i in range(len(evolucion_empates)):
        if diferencia_partidas is not None:
            string_evol_emp_formateado = "AI: {empatadas} / {dif_p} => {porcentaje}%".format(empatadas=evolucion_empates[i], dif_p = diferencia_partidas, porcentaje=evolucion_empates[i]/diferencia_partidas*100)        
        else:
            string_evol_emp_formateado = "AI: {empatadas} / 10 => {porcentaje}%".format(empatadas=evolucion_empates[i], porcentaje=evolucion_empates[i]/10*100)
        print(string_evol_emp_formateado)
        string_evol_emp_formateado += "\n"
        evolucion_empates_formateado.append(string_evol_emp_formateado)

    string_evol_vict_formateado = "La AI ganó el {porcentaje}% de las veces".format(porcentaje=victorias/num_partidas*100)
    string_evol_emp_formateado = "La AI empató el {porcentaje}% de las veces".format(porcentaje=empates/num_partidas*100)
    print(string_evol_vict_formateado)
    print(string_evol_emp_formateado)
    string_evol_vict_formateado += "\n"
    string_evol_emp_formateado += "\n"
    evolucion_victorias_formateado.append(string_evol_vict_formateado)
    evolucion_empates_formateado.append(string_evol_emp_formateado)
    jugador1.grabar_datos_en_disco(evolucion_victorias_formateado, directorio + "/" + "resumen_winrate.txt")
    jugador1.grabar_datos_en_disco(evolucion_empates_formateado, directorio + "/" + "resumen_tierate.txt")           
    # Escribe en el archivo de pesos finales un separador
    jugador1.guardar_pesos()

    # Realizar las gráficas de los pesos y guardarlas como png's
    # El 9 es el número de pesos
    for i in range(9):
        Graficar.graficar_peso(directorio, directorio + "/peso{num}.txt".format(num=i), i)

    # Realizar las gráficas del winrate
    Graficar.graficar_winrate(directorio, evolucion_victorias)