from ejercicio8.Juego import *
from ejercicio8.Jugadores import *
import os
import sys
import ejercicio8.RedNeuronal as RedNeuronal
import ejercicio8.Utils as Utils

uso = """
Invocar como python3 Evaluador.py [config file]. El módulo recibe los parámetros de entrada desde el archivo de configuración.
En ese archivo, cada argumento se define en una línea a parte.
El formato del archivo es el siguiente:
[nombre directorio]     #nombre del directorio en donde se guardan los resultados
[oponente]              #ruta a un archivo con pesos o "Aleatorio"
[número de partidas]    #cantidad de partidas de evaluación
[pesos red]             #archivo con los pesos de la red neuronal, guardado luego de correr el módulo Training.py
"""

'''
Jugar a modo de entrenamiento el número de partidas indicas por parámetro.
Imprime en consola el número de partidas ganadas por el jugador que usa la red neuronal.
'''

if __name__ == '__main__':
    directorio, oponente, num_partidas, red = Utils.parsear_conf(sys.argv[1])

    if oponente != 'Aleatorio' and not os.path.isfile(oponente):
        print("***Valor incorrecto para el oponente. Debe ser 'Aleatorio' o un archivo con los pesos de una AI***")
        print(uso)
        exit()
    elif oponente == 'Aleatorio':
        print('[*] Oponente aleatorio seleccionado')
    else:
        print('[*] Oponente AI seleccionado')

    num_partidas = int(num_partidas)
    if num_partidas <= 0:
        print("***Valor incorrecto para el número de partidas. Debe ser un entero positivo***")
        print(uso)
        exit()
    else:
        print('[*] Se jugarán {num} partidas de entrenamiento'.format(num=num_partidas))

    if not os.path.isfile(red):
        print("***Valor incorrecto para la red neuronal. Debe ser una lista con la cantidad de neuronas en cada" +
              " capa (sin contar neuronas de sesgo) o un archivo con los valores de cada peso***")
        print(uso)
        exit()
    else:
        print('[*] Se cargará una red neuronal desde el archivo {file}'.format(file=red))

    input_key = input("Si algún valor de la configuración es incorrecto, presione 'q' para salir; presione ENTER para continuar...\n")
    if len(input_key) > 0 and input_key[0] == 'q':
        exit()

    print("[*] Creando jugadores")
    print('[*] Cargando los pesos de la red neuronal')
    red_neuronal = RedNeuronal.RedNeuronal(neuronas=red)
    print('[*] Red neuronal cargada con éxito')
    jugador1 = Red(Color.Blancas, red_neuronal, False, directorio)
    if oponente != "Aleatorio":
        jugador2 = AI(Color.Negras, "AI", None, False, 0)
        print("[*] Cargando pesos de la AI oponente")
        jugador2.cargar_pesos(oponente)
        jugador2.alternar_pesos()
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

    print("[*] Comenzando la serie de partidas")
    color_que_empieza = Color.Blancas
    for i in range(num_partidas):
        print("[-] Comenzando partida {num}".format(num=i+1))
        resultado = ''
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

        jugador1.red_neuronal.backpropagation(jugador1.directorio_instancias +
                                              '/partida{num_partida}.npz'.format(
                                                  num_partida=jugador1.contador_partidas-1),
                                              jugador1.directorio_instancias +
                                              '/eval{num_partida}.txt'.format(
                                                  num_partida=jugador1.contador_partidas - 1))

    print("[*] La Red Neuronal ganó el {porcentaje}% de las veces".format(porcentaje=victorias/num_partidas*100))
    print("[*] La Red Neuronal empató el {porcentaje}% de las veces".format(porcentaje=empates/num_partidas*100))
