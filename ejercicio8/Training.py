from ejercicio8.Juego import *
from ejercicio8.Jugadores import *
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
[regularization]        #factor de regularización de los pesos de la red (0 para deshabilitar)
[momentum]              #factor de momentum para la actualización de los pesos en el descenso por gradiente (0 para deshabilitar)
[epsilon]               #valor de epsilon para el gradient checking (0 para deshabilitar). El gradien checking se hace cada 50 jugadas
"""

'''
Jugar a modo de entrenamiento el número de partidas indicas por parámetro.
Imprime en consola el número de partidas ganadas por el jugador que usa la red neuronal.
'''

if __name__ == '__main__':
    directorio, oponente, num_partidas, red, activation_function, discount_rate,\
    batch_size, learning_rate, regularization, momentum, epsilon = Utils.parsear_conf('Training.conf')

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
    if momentum <= 0 or momentum > 1:
        print('***Valor incorrecto de tasa de momentum. Debe ser un valor entre 0 y 1 (o cero para deshabilitar esta funcionalidad)***')
        print(uso)
        exit()
    elif momentum == 0:
        print('[*] Valor de momentum establecido en cero. No se utilizará momentum durante el aprendizaje!')
    else:
        print('[*] Valor de momentum establecido en {tasa}'.format(tasa=momentum))

    epsilon = float(epsilon)
    if momentum < 1e-8 or momentum > 1:
        print('***Valor inapropiado para el epsilon del Gradient Checking. Se recomienda un valor entre 1e-8 y 1 (o cero para deshabilitar esta funcionalidad)***')
        print(uso)
        exit()
    elif epsilon == 0:
        print('[*] Valor de epsilon para el gradient checking establecido en cero. No se utilizará gradient checking momentum durante el aprendizaje!')
    else:
        print('[*] Valor de epsilon para el gradient checking establecido en {epsilon}'.format(epsilon=epsilon))

    input_key = input("Si algún valor de la configuración es incorrecto, presione 'q' para salir; presione ENTER para continuar...\n")
    if len(input_key) > 0 and input_key[0] == 'q':
        exit()

    print("[*] Creando jugadores")
    print('[*] Cargando los pesos de la red neuronal')
    red_neuronal = RedNeuronal.RedNeuronal(red, activation_function, discount_rate, batch_size, learning_rate, regularization, momentum, epsilon)
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
            resultado = '0'
        elif ganador == 'Red Neuronal':
            victorias += 1
            resultado = '1'
        else:
            resultado = '-1'

        print("[-] Victorias = {victorias}".format(victorias=victorias))
        print("[-] Empates = {empates}".format(empates=empates))

        jugador1.red_neuronal.backpropagation(jugador1.directorio_instancias +
                                              '/partida{num_partida}.npz{res}'.format(num_partida=jugador1.contador_partidas-1, res=resultado), (i+1) % 10 == 0)

    print("[*] La Red Neuronal ganó el {porcentaje}% de las veces".format(porcentaje=victorias/num_partidas*100))
    print("[*] La Red Neuronal empató el {porcentaje}% de las veces".format(porcentaje=empates/num_partidas*100))
