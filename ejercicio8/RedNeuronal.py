#neuronas de entrada
#lista con neuronas en cada capa interna
#neuronas de salida
#tamaño de batch
#batch size
#learning rate
#learning rate number
#momentum

import numpy as np

class RedNeuronal(object):
	def __init__(self, neuronas_entrada, capas_intermedias, neuronas_salida, batch_size, learning_rate,
				 learning_rate_number, momentum):
		pass

	# Recibe una instancia y devuelve una valoración del tablero.
	def evaluar(self, input):
		return 0

	# Guardar la instancia actual (tablero + movimiento realizado) en el archivo
	def guardar_instancia(self, instancia, archivo_instancias):
		pass

	# Aplicar el algoritmo de backpropagation sobre el archivo de instancias seleccionado
	def backpropagation(self, archivo_instancias):
		pass

def cargar_red(archivo_pesos):
	pass
