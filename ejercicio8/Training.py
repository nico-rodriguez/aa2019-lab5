from ejercicio8.Juego import *
from ejercicio8.Jugadores import *
import sys
import os
import ejercicio8.RedNeuronal as RedNeuronal
import ejercicio8.Utils as Utils
import ast

uso = """
Invocar como python3 Training.py [config file]. El módulo recibe los parámetros de entrada desde el archivo de configuración.
En ese archivo, cada argumento se define en una línea a parte.
El formato del archivo es el siguiente:
[nombre directorio]     #nombre del directorio en donde se guardan los resultados
[oponente]              #ruta a un archivo con pesos o "Aleatorio"
[número de partidas]    #cantidad de partidas de entrenamiento
[pesos red]             #archivo con los pesos de la red neuronal o una lista con la cantidad de neuronas de cada capa
                        #(sin incluir las neuronas de sesgo).
[función de activación] #'tanh' o 'sigmoid'
[factor de descuento]   #factor de descuento de la función Q
[batch size]            #tamaño del batch para el aprendizaje
[learning rate]         #taza de aprendizaje (factor del tamaño del paso en el descenso por gradiente)
[regularization]        #factor de regularización de los pesos de la red
[momentum]              #factor de momentum para la actualización de los pesos en el descenso por gradiente
"""

'''
Jugar a modo de entrenamiento el número de partidas indicas por parámetro.
Imprime en consola el número de partidas ganadas por el jugador que usa la red neuronal.
'''

if __name__ == '__main__':
    directorio, oponente, num_partidas, red, activation_function, discount_rate,\
    batch_size, learning_rate, regularization, momentum = Utils.parsear_conf('Training.conf')

    if oponente != 'Aleatorio' and not os.path.isfile(oponente):
        print("***Valor incorrecto para el oponente. Debe ser 'Aleatorio' o un archivo con los pesos de una AI***")
        print(uso)
        exit()

    num_partidas = int(num_partidas)
    if num_partidas <= 0:
        print("***Valor incorrecto para el número de partidas. Debe ser un entero positivo***")
        print(uso)
        exit()
    if not os.path.isfile(red):
        red = ast.literal_eval(red)
        if isinstance(red, str):
            print("***Valor incorrecto para la red neuronal. Debe ser una lista con la cantidad de neuronas en cada" +
                  " capa (sin contar neuronas de sesgo) o un archivo con los valores de cada peso***")
            print(uso)
            exit()

    if activation_function != 'tanh' and activation_function != 'sigmoid':
        print('***Valor incorrecto de función de activación. Debe ser "tanh" o "sigmoid"***')
        print(uso)
        exit()

    discount_rate = float(discount_rate)
    if discount_rate < 0 or discount_rate > 1:
        print('***Valor incorrecto de tasa de descuento. Debe ser un valor entre 0 y 1***')
        print(uso)
        exit()

    batch_size = int(batch_size)
    if batch_size <= 0:
        print('***Valor incorrecto de tamaño de batch. Debe ser positivo***')
        print(uso)
        exit()

    learning_rate = float(learning_rate)
    if learning_rate < 0 or learning_rate > 1:
        print('***Valor incorrecto de tasa de aprendizaje. Debe ser un valor entre 0 y 1***')
        print(uso)
        exit()

    regularization = float(regularization)
    if regularization < 0:
        print('***Valor incorrecto de tasa de regularización. Debe ser un valor positivo***')
        print(uso)
        exit()

    momentum = float(momentum)
    if momentum < 0 or momentum > 1:
        print('***Valor incorrecto de tasa de momentum. Debe ser un valor entre 0 y 1***')
        print(uso)
        exit()


    print("[*] Creando jugadores")
    print('[*] Cargando los pesos de la red neuronal')
    red_neuronal = RedNeuronal.RedNeuronal(red, activation_function, discount_rate, batch_size, learning_rate, regularization, momentum)
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
    if not os.path.isdir(directorio):
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

    print("[*] La Red Neuronal ganó el {porcentaje}% de las veces".format(porcentaje=victorias/num_partidas*100))
    print("[*] La Red Neuronal empató el {porcentaje}% de las veces".format(porcentaje=empates/num_partidas*100))
