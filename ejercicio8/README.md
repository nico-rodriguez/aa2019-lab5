# Laboratorio 1 del curso Aprendizaje Automático 2019.
Se implementa un algoritmo de aprendizaje Q utilizando redes neuronales y los jugadores de la tarea 1.

## Jugadores
Se agrega un jugador que utiliza una red neuronal a los de la tarea 1 (Aleatorio y AI con regresión lineal).

## Dependencias
* python3 >= 3.5.2
* python3-matplotlib <= 2.1.1

## Modos de invocación

### Generación de corpus de entrenamiento

Invocar como python3 Corpus.py [archivo conf] donde
'archivo_conf' es un archivo de configuración. A modo de ejemplo, ver Corpus.conf.

ejemplo de confuguración:

corpus                     #nombre del directorio en donde se guardan los resultados
pesos.txt                  #jugador 1 (Aleatorio o ruta a pesos de regresión lineal)
Aleatorio                  #jugador 2 (Aleatorio)
500                         #cantidad de partidos

### Entrenamiento del jugador que utiliza la red neuronal

Invocar como python3 Training.py [config file]. El módulo recibe los parámetros de entrada desde el archivo de configuración.
En ese archivo, cada argumento se define en una línea a parte, ver Training.conf.

El formato del archivo es el siguiente:
[nombre directorio]     #nombre del directorio en donde se guardan los resultados
[oponente]              #ruta a un archivo con pesos o "Aleatorio"
[corpus]                #directorio del corpus inicial
[tamaño corpus]         #tamaño del corpus inicial
[número de partidas]    #cantidad de partidas de entrenamiento
[pesos red]             #archivo con los pesos de la red neuronal (archivo.sav) o una tupla con la cantidad de neuronas de cada capa
                        #interna (sin incluir las neuronas de sesgo).
[función de activación] #'tanh', 'logistic' o 'relu'
[factor de descuento]   #factor de descuento de la función Q
[batch size]            #tamaño del batch para el aprendizaje
[iter_num]              #número máximo de iteraciones durante el aprendizaje
[learning rate]         #taza de aprendizaje (factor del tamaño del paso en el descenso por gradiente)
[regularization]        #factor de regularización de los pesos de la red (0 para deshabilitar)
[momentum]              #factor de momentum (0 para deshabilitar)