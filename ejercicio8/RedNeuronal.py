#neuronas de entrada
#lista con neuronas en cada capa interna
#neuronas de salida
#tamaño de batch
#batch size
#learning rate
#learning rate number
#momentum

import numpy as np
import Utils

class RedNeuronal(object):
	def __init__(self, neuronas, activation_function='tanh', batch_size=1, learning_rate=None,
				 learning_rate_number=0.01, momentum=0.5):
		# Inicializar capas y neuronas de la red
		print('[-] Inicializando neuronas de la red con valores aleatorios')
		self.capas = []
		for i in range(len(neuronas)-1):
			neuronas_capa_acutal = neuronas[i] + 1  # Considerar la neurona de sesgo
			neuronas_capa_siguiente = neuronas[i + 1]
			self.capas.append(np.random.rand(neuronas_capa_siguiente, neuronas_capa_acutal))
		print('[-] Red neuronal inicializada')

		self.activation_function = activation_function

	# Recibe una instancia y devuelve una valoración del tablero.
	def forwardpropagation(self, input):
		x = np.array(input).reshape(len(input), 1)
		for capa in self.capas:
			x = np.vstack([1, x])
			if self.activation_function == 'sigmoid':
				x = Utils.sigmoid(capa.dot(x))
			elif self.activation_function == 'tanh':
				x = Utils.tanh(capa.dot(x))
		return x

	# Guardar la instancia actual (tablero + movimiento realizado) en el archivo
	def guardar_instancia(self, instancia, archivo_instancias):
		pass

	# Aplicar el algoritmo de backpropagation sobre el archivo de instancias seleccionado
	def backpropagation(self, archivo_instancias):
		pass

def guardar_red(archivo_pesos):
	print('[-] Guardando la red neuronal en "{file}"'.format(file=archivo_pesos))
	pass

def cargar_red(archivo_pesos):
	print('[-] Cargandp la red neuronal del archivo "{file}"'.format(file=archivo_pesos))
	pass

if __name__ == '__main__':
	x = [1, 2, 3]
	red1 = RedNeuronal([3, 3, 1])
	print(red1.forwardpropagation(x))
	red2 = RedNeuronal([3, 1])
	print(red2.forwardpropagation(x))
	red3 = RedNeuronal([3, 7, 9, 8, 5, 2])
	print(red3.forwardpropagation(x))
