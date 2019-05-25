from ejercicio8.Juego import *
from ejercicio8.Jugadores import *
import os
import sys
import ejercicio8.RedNeuronal as RedNeuronal
import ejercicio8.Utils as Utils
import ast

uso = """
Invocar como python3 Training.py [config file]. El módulo recibe los parámetros de entrada desde el archivo de configuración.
En ese archivo, cada argumento se define en una línea a parte.
El formato del archivo es el siguiente:
[nombre directorio]     #nombre del directorio en donde se guardan los resultados
[oponente]              #ruta a un archivo con pesos o "Aleatorio"
[corpus]                #directorio del corpus inicial
[tamaño corpus]         #tamaño del corpus inicial
[número de partidas]    #cantidad de partidas de entrenamiento
[pesos red]             #archivo con los pesos de la red neuronal o una tupla con la cantidad de neuronas de cada capa
                        #interna (sin incluir las neuronas de sesgo).
[función de activación] #'tanh' o 'sigmoid'
[factor de descuento]   #factor de descuento de la función Q
[batch size]            #tamaño del batch para el aprendizaje
[iter_num]              #número máximo de iteraciones durante el aprendizaje
[learning rate]         #taza de aprendizaje (factor del tamaño del paso en el descenso por gradiente)
[regularization]        #factor de regularización de los pesos de la red (0 para deshabilitar)
[momentum]              #factor de momentum (0 para deshabilitar)
"""

'''
Jugar a modo de entrenamiento el número de partidas indicas por parámetro.
Imprime en consola el número de partidas ganadas por el jugador que usa la red neuronal.
'''

if __name__ == '__main__':
    directorio, oponente, directorio_corpus, num_corpus, num_partidas, red, activation_function, discount_rate,\
    batch_size, iter_num, learning_rate, regularization, momentum = Utils.parsear_conf(sys.argv[1])

    if oponente != 'Aleatorio' and not os.path.isfile(oponente):
        print("***Valor incorrecto para el oponente. Debe ser 'Aleatorio' o un archivo con los pesos de una AI***")
        print(uso)
        exit()
    elif oponente == 'Aleatorio':
        print('[*] Oponente aleatorio seleccionado')
    else:
        print('[*] Oponente AI seleccionado')

    if not os.path.isdir(directorio_corpus):
        print("***Valor incorrecto para el directorio del corpus.***")
        print(uso)
        exit()
    else:
        print('[*] Directorio de corpus inicial establecido en {dir}'.format(dir=directorio_corpus))

    num_corpus = int(num_corpus)
    if num_corpus <= 0:
        print("***Valor incorrecto para el número de partidas del corpus inicial. Debe ser un entero positivo***")
        print(uso)
        exit()
    else:
        print('[*] Partidas del corpus inicial establecidas en {num}'.format(num=num_corpus))

    num_partidas = int(num_partidas)
    if num_partidas <= 0:
        print("***Valor incorrecto para el número de partidas. Debe ser un entero positivo***")
        print(uso)
        exit()
    else:
        print('[*] Se jugarán {num} partidas de entrenamiento'.format(num=num_partidas))

    if not os.path.isfile(red):
        red = ast.literal_eval(red)
        if isinstance(red, str):
            print("***Valor incorrecto para la red neuronal. Debe ser una lista con la cantidad de neuronas en cada" +
                  " capa (sin contar neuronas de sesgo) o un archivo con los valores de cada peso***")
            print(uso)
            exit()
        else:
            print('[*] Se creará una red neuronal con capas {capas}'.format(capas=red))
    else:
        print('[*] Se cargará una red neuronal desde el archivo {file}'.format(file=red))

    if activation_function != 'tanh' and activation_function != 'sigmoid':
        print('***Valor incorrecto de función de activación. Debe ser "tanh" o "sigmoid"***')
        print(uso)
        exit()
    else:
        print('[*] Función de activación {fun} seleccionada'.format(fun=activation_function))

    discount_rate = float(discount_rate)
    if discount_rate < 0 or discount_rate >= 1:
        print('***Valor incorrecto de tasa de descuento. Debe ser un valor entre 0 y 1 (inclusive 1)***')
        print(uso)
        exit()
    else:
        print('[*] Tasa de descuento establecida en {tasa}'.format(tasa=discount_rate))

    batch_size = int(batch_size)
    if batch_size <= 0:
        print('***Valor incorrecto de tamaño de batch. Debe ser positivo***')
        print(uso)
        exit()
    else:
        print('[*] Tamaño de batch establecida en {batch}'.format(batch=batch_size))

    iter_num = int(iter_num)
    if iter_num <= 0:
        print('***Valor incorrecto de número de iteraciones. Debe ser positivo***')
        print(uso)
        exit()
    else:
        print('[*] Número de iteraciones máximo para el aprendizaje establecido en {iter}'.format(iter=iter_num))

    learning_rate = float(learning_rate)
    if learning_rate < 0 or learning_rate > 1:
        print('***Valor inapropiado de tasa de aprendizaje. Se recomienda un valor entre 0 y 1***')
        print(uso)
        exit()
    else:
        print('[*] Tasa de aprendizaje establecida en {tasa}'.format(tasa=learning_rate))

    regularization = float(regularization)
    if regularization < 0:
        print('***Valor incorrecto de tasa de regularización. Debe ser un valor positivo (o cero para deshabilitar esta funcionalidad)***')
        print(uso)
        exit()
    elif regularization == 0:
        print('[*] Tasa de regularización establecida en cero. No se utilizará regularización durante el aprendizaje!')
    else:
        print('[*] Tasa de regularización establecida en {tasa}'.format(tasa=regularization))

    momentum = float(momentum)
    if momentum < 0:
        print('***Valor incorrecto de tasa de momentum. Debe ser un valor positivo (o cero para deshabilitar esta funcionalidad)***')
        print(uso)
        exit()
    elif regularization == 0:
        print('[*] Tasa de momentum establecida en cero. No se utilizará momentum durante el aprendizaje!')
    else:
        print('[*] Tasa de momentum establecida en {tasa}'.format(tasa=momentum))

    input_key = input("Si algún valor de la configuración es incorrecto, presione 'q' para salir; presione ENTER para continuar...\n")
    if len(input_key) > 0 and input_key[0] == 'q':
        exit()

    print("[*] Creando jugadores")
    print('[*] Cargando los pesos de la red neuronal')
    red_neuronal = RedNeuronal.RedNeuronal(neuronas=red, activation_function=activation_function, factor_descuento=discount_rate,
                                           num_iters=iter_num, batch_size=batch_size, learning_rate=learning_rate,
                                           regularization=regularization, momentum=momentum)
    jugador1 = Red(Color.Blancas, red_neuronal, True, directorio)
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

    print(jugador1.red_neuronal.mlp)

    print('[*] Entrenando la red neuronal con el corpus inicial')
    for i in range(1, num_corpus+1):
        jugador1.red_neuronal.backpropagation(directorio_corpus + '/partida{num_partida}.npz'.format(num_partida=i),
                                              directorio_corpus + '/eval{num_partida}.txt'.format(num_partida=i))
    print('[*] Entrenamiento inicial finalizado')

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
    print("[*] Guardando la red neuronal entrenada en {file}".format(file=jugador1.directorio_instancias + '/red.sav'))
    RedNeuronal.guardar_red(jugador1.red_neuronal.mlp, jugador1.directorio_instancias + '/red.sav')
