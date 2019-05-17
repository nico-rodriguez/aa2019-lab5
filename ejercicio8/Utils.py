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
	e_menos_x = np.exp(-arr)
	e_mas_x = np.exp(arr)
	return (e_mas_x + e_menos_x) / (e_mas_x - e_menos_x)
