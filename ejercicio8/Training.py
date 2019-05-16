from Juego import *
from Jugadores import *
import Graficar
import sys
import os
import numpy as np
import RedNeuronal

uso = """
Invocar como python3 Training.py [nombre directorio] [pesos red] [oponente] [numero de partidas] donde:
-'pesos red' es el archivo con los pesos de la red neuronal.
-'oponente' puede ser una ruta a un archivo con pesos o "Aleatorio".
-'nombre directorio' es el nombre del directorio en donde se guardan los resultados.
Los pesos deben estar escritos en una sola línea y separados por espacios.
"""

'''
Jugar a modo de entrenamiento el número de partidas indicas por parámetro.
Imprime en consola el número de partidas ganadas por el jugador que usa la red neuronal.
'''

if __name__ == '__main__':
    #Chequear número y valores de los argumentos
    if not(len(sys.argv) == 3):
        print("***Número incorrecto de parámetros***")
        print(uso)
        exit()

    directorio = sys.argv[1]
    pesos_red = sys.argv[2]
    oponente = sys.argv[3]
    num_partidas = int(sys.argv[4])

    print("[*] Creando jugadores")
    print('[*] Cargando los pesos de la red neuronal')
    red_neuronal = RedNeuronal.cargar_red(pesos_red)
    jugador1 = Red(Color.Blancas, red_neuronal, True, directorio)
    if oponente != "Aleatorio":
        jugador2 = AI(Color.Negras, "AI", None, False, 0)
        print("[*] Cargando pesos de la AI oponente")
        jugador2.cargar_pesos(oponente)
        jugador2.alternar_pesos()
    # Solo el primero es AI
    elif oponente == "Aleatorio":
        jugador2 = Aleatorio(Color.Negras, "Aleatorio")
    else:
        print("***Valores de oponente incorrectos. Debe ser un archivo de pesos de AI o 'Aleatorio'.***")
        print(uso)
        exit()

    victorias = 0
    empates = 0

    # Crear un directorio para guardar los datos de entrenamiento
    os.mkdir(directorio)
    print("[*] Se crea el directorio {dir}".format(dir=directorio))

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

    print("[*] Comenzando la serie de partidas")
    for i in range(num_partidas):
        print("[-] Comenzando partida {num}".format(num=i+1))
        juego = Juego(jugador2, jugador1)
        ganador = juego.jugar(color_que_empieza)
        color_que_empieza = Color.Blancas if (color_que_empieza == Color.Negras) else Color.Negras

        print("[-] Partida {partida} => Ganó {ganador}.".format(partida=i+1, ganador=ganador))
        if ganador is None:
            empates += 1
        elif ganador == 'Red Neuronal':
            victorias += 1

        print("[-] Victorias = {victorias}".format(victorias=victorias))
        print("[-] Empates = {empates}".format(empates=empates))

    print("[*] La AI ganó el {porcentaje}% de las veces".format(porcentaje=victorias/num_partidas*100))
    print("[*] La AI empató el {porcentaje}% de las veces".format(porcentaje=empates/num_partidas*100))
