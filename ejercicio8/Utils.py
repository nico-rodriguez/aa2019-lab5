import numpy as np
import re

"""
Aplicar la función Sigmoide a cada elemento de un arreglo numpy.
"""
def sigmoid(arr):
	return 1 / (1 + np.exp(-arr))


"""
Aplicar la función tangente hiperbolica a cada elemento de un arreglo numpy.
"""
def tanh(arr):
	return np.tanh(arr)


"""
Aplicar la función de activación seleccionada.
"""
def activation_function(fun, arr):
	if fun == 'sigmoid':
		x = sigmoid(arr)
	elif fun == 'tanh':
		x = tanh(arr)
	else:
		raise Exception('Utils.py: invalid activation function in activation_function')
	return x


"""
Aplicar la derivada de la función de activación seleccionada. Los valores del arreglo arr son los valores de
activación (resultado de aplicar la función de activación). Se aprovecha que las derivadas de tanh y sigmoid
se pueden expresar en función de esos valores, para reducir la cantidad de cálculos.
"""
def d_activation_function(fun, arr):
	if fun == 'sigmoid':
		x = d_sigmoid(arr)
	elif fun == 'tanh':
		x = d_tanh(arr)
	else:
		raise Exception('Utils.py: invalid activation function in activation_function')
	return x


"""
Aplicar la derivada de la función Sigmoide a cada elemento de un arreglo numpy.
"""
def d_sigmoid(arr):
	return arr * (1 - arr)


"""
Aplicar la derivada de la función tangente hiperbolica a cada elemento de un arreglo numpy.
"""
def d_tanh(arr):
	return 1 - (arr ** 2)


"""
Agregar un 1 en la primera posición del arreglo (o si es una matriz, en la primera fila).
"""
def extend_array(arr):
	if arr.ndim == 1:
		arr = np.vstack([1, arr])
	elif arr.ndim == 2:
		arr = np.vstack([np.ones(arr.shape[1]), arr])
	else:
		raise Exception('Utils.py: invalid array dimension in extend_array')
	return arr


"""
Redimensionar el arreglo n-dimensional. Si es un vector, convertirlo en un arreglo n-dimensional de una columna;
si es un arreglo de dos dimentiones, trasponerlo.
"""
def reshape_array(arr):
	if arr.ndim == 1:
		arr = arr.reshape(len(arr), 1)
	elif arr.ndim == 2:
		arr = arr.T
	else:
		raise Exception('Utils.py: invalid array dimension in reshape_array')
	return arr


"""
Parsear un archivo de configuración en donde los argumentos para el programa se encuentran uno en cada línea, antes
de un conjunto de tabulaciones.
"""
def parsear_conf(archivo_conf):
	with open(archivo_conf, 'r') as conf:
		conf_lines = conf.readlines()
	params = []
	for line in conf_lines:
		params.append(re.match(r'^(.+)\s+#', line)[1].strip())
	return params


# Guardar la partida actual (tableros + movimientos realizados) en el archivo
def guardar_partida(partida, archivo_instancias):
	np.savez(archivo_instancias, np.array(partida))


def guardar_evaluaciones(evals, archivo_evals):
	with open(archivo_evals, 'w') as archivo:
		for q in evals:
			archivo.write(str(q) + '\n')


if __name__ == '__main__':
	print(parsear_conf('Training.conf'))
