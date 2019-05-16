# Laboratorio 1 del curso Aprendizaje Automático 2019.
Se implementa un algoritmo de aprendizaje automático para jugar a las damas chinas (dos jugadores).

## Jugadores
Un jugador aleatorio y un AI. El AI utiliza aprendizaje por refuerzos para mejorar su juego, buscando aumentar su porcentaje de victorias.
Las blancas comienzan abajo, las negras arriba. La versión más entrenada del AI siempre juega con las blancas.

## Función objetivo
Función que dado un tablero devuelve un valor real de valoración, cuanto más grande sea ese valor, más favorable será el tablero para la AI.

## Representación del tablero
*(x<sub>1</sub>,x<sub>2</sub>,x<sub>3</sub>,x<sub>4</sub>,x<sub>5</sub>,x<sub>6</sub>,x<sub>7</sub>,x<sub>8</sub>)*

donde:
1.  *x<sub>1</sub>* es la suma de las distancias verticales de todas las fichas blancas hacia la última fila libre de la punta opuesta
2.  *x<sub>2</sub>* es lo mismo que *x1* pero para las fichas negras
3.  *x<sub>3</sub>* es la cantidad de fichas blancas que llegaron a la punta opuesta del tablero
4.  *x<sub>4</sub>* es lo mismo que *x3* pero para las fichas negras
5.  *x<sub>5</sub>* es la cantidad de movimientos de blancas que disminuyen la distancia a la punta opuesta
6.  *x<sub>6</sub>* es lo mismo que *x5* pero para las fichas negras
7.  *x<sub>7</sub>* es la distancia de la ficha blanca más retrasada hacia la posición libre más lejana
8.  *x<sub>8</sub>* es lo mismo que *x7* pero para las fichas negras

Entonces, la función objetivo (valoración de tablero) se representa como:
*V(x<sub>1</sub>,x<sub>2</sub>,x<sub>3</sub>,x<sub>4</sub>,x<sub>5</sub>,x<sub>6</sub>,x<sub>7</sub>,x<sub>8</sub>) = w<sub>0</sub> + w<sub>1</sub>\*x<sub>1</sub> + ... + w<sub>8</sub>\*x<sub>8</sub>*

## Algoritmo de aproximación
1. Los valores de entrenamiento que se propagan hacia atras son las valoraciones del siguiente tablero en el que le toca jugar a la AI, leyendo los arhcivos de entrenamiento que se generan (ver punto **Archivos generados y su formato**).
2. El ajuste de los pesos *w<sub>i</sub>* se hace con el método de mínimos cuadrados.

La propagación se realiza al final de cada partida de entrenamiento.

## Dependencias
* python3 >= 3.5.2
* python3-matplotlib <= 2.1.1

## Modos de invocación
1.  Modo entrenamiento: en este modo se entrena la AI, ajustando sus pesos como se describió antes. El programa está en Training.py y se invoca como
```
python3 Training.py [directorio] [jugador1] [jugador2] [partidas] [diferencia partidas]
```
donde:
* `directorio` es el nombre del directorio (relativo al directorio actual) en donde se guardan los resultados del entrenamiento: valores de entrenamiento (archivos partidaX.txt), pesos finales, archivos y gráficas de evolución de cada peso y archivos de win-rate y tie-rate para la AI, cuando entrena contra el jugador aleatorio o para `jugador1` cuando ambos son AIs. El archivo con los pesos debe consistir en una única línea con los pesos desde el *w<sub>0</sub>* al *w<sub>8</sub>*, separados por espacios. 
* `jugadorX` puede ser una ruta a un archivo de pesos, en cuyo caso, el jugador es una AI; o puede ser el string "Aleatorio", en cuyo caso, el jugador es el aleatorio. Al menos uno de los jugadores debe ser una AI.
* `partidas` es el número de partidas de entrenamiento.
* `diferencia partidas` solo es requerido por el programa cuando el entrenamiento es entre dos AI. En ese caso, la AI que entrena es la que se pasó en `jugador1` y `diferencia partidas` indica el número de partidas de diferencia con que la AI1 le pasa sus pesos a la AI2.

2.  Modo torneo: en este modo los jugadores solamente juegan partidas (no entrenan). El programa está en Torneo.py y se invoca como
```
python3 Torneo.py [directorio] [jugador1] [jugador2] [partidas]
```
donde los argumentos tienen el mismo significado que para `Training.py`, pero lo que se guarda en `directorio` es solamente los archivos de win-rate y tie-rate.

## Archivos generados y su formato
* win-rate, tie-rate: muestran el porcentaje de victorias y empates cada 10 partidas o cada `diferencia partidas` (solo cuando se psas este parámetro), dentro del número total de partidas.
* archivos de entrenamiento: son los que se leen para hacer la propagación hacia atrás. El formato consiste en líneas de la forma:

*[tupla de tablero]* *[valoración del tablero siguiente]*

Un ejemplo de línea (todos los valores están separados por espacios):

47 42 4 6 8 7 7.0710678118654755 8.0 0.9798266203943695

* pesos_finales.txt: archivo con los pesos luego de finalizado el entrenamiento