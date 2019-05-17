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
