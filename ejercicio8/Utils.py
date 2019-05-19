import numpy as np

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
Aplicar la derivada de la función Sigmoide a cada elemento de un arreglo numpy.
"""
def d_sigmoid(arr):
	s = sigmoid(arr)
	return s * (1 - s)


"""
Aplicar la derivada de la función tangente hiperbolica a cada elemento de un arreglo numpy.
"""
def d_tanh(arr):
	return 1 - (np.tanh(arr) ** 2)


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
