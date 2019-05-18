#momentum
#Rprop
#Regularización

import numpy as np
import ejercicio8.Utils as Utils
import os

class RedNeuronal(object):
	def __init__(self, neuronas, activation_function='tanh', batch_size=1, learning_rate_number=0.01, momentum=0.5):
		# Inicializar capas y neuronas de la red
		print('[-] Inicializando neuronas de la red con valores aleatorios')
		self.capas = []
		for i in range(len(neuronas)-1):
			neuronas_capa_acutal = neuronas[i] + 1  # Considerar la neurona de sesgo
			neuronas_capa_siguiente = neuronas[i + 1]
			capa = np.random.randn(neuronas_capa_siguiente, neuronas_capa_acutal)
			# Inicialización de Xavier/He
			capa = capa * np.sqrt(2 / (neuronas_capa_acutal + neuronas_capa_siguiente))
			self.capas.append(capa)
		print('[-] Red neuronal inicializada')

		self.activation_function = activation_function

	# Recibe una instancia y devuelve una valoración del tablero.
	def forwardpropagation(self, input):
		x = np.array(input)
		if x.ndim == 1:
			x = x.reshape(len(input), 1)
		elif x.ndim == 2:
			x = x.T
		else:
			raise Exception('RedNeuronal.py: invalid array dimension in forwardpropagation')
		# Aplicar la función de acivación seleccionada en cada capa intermedia
		for i in range(len(self.capas)-1):
			capa = self.capas[i]
			if x.ndim == 1:
				x = np.vstack([1, x])
			elif x.ndim == 2:
				x = np.vstack([np.ones(x.shape[1]), x])
			else:
				raise Exception('RedNeuronal.py: invalid array dimension in forwardpropagation')
			if self.activation_function == 'sigmoid':
				x = Utils.sigmoid(capa.dot(x))
			elif self.activation_function == 'tanh':
				x = Utils.tanh(capa.dot(x))
		# Aplicar siempre tanh a la última capa, para obtener un resultado en [-1,1]
		ultima_capa = self.capas[-1]
		if x.ndim == 1:
			x = np.vstack([1, x])
		elif x.ndim == 2:
			x = np.vstack([np.ones(x.shape[1]), x])
		else:
			raise Exception('RedNeuronal.py: invalid array dimension in forwardpropagation')
		x = Utils.tanh(ultima_capa.dot(x))
		return x

	# Recibe una instancia y devuelve una lista con los valores z de cada capa.
	def forwardpropagation_z(self, input):
		z = []
		x = np.array(input)
		if x.ndim == 1:
			x = x.reshape(len(input), 1)
		elif x.ndim == 2:
			x = x.T
		else:
			raise Exception('RedNeuronal.py: invalid array dimension in forwardpropagation')
		# Aplicar la función de acivación seleccionada en cada capa intermedia
		for i in range(len(self.capas) - 1):
			capa = self.capas[i]
			if x.ndim == 1:
				x = np.vstack([1, x])
			elif x.ndim == 2:
				x = np.vstack([np.ones(x.shape[1]), x])
			else:
				raise Exception('RedNeuronal.py: invalid array dimension in forwardpropagation_z')
			z_actual = capa.dot(x)
			z.append(z_actual)
			if self.activation_function == 'sigmoid':
				x = Utils.sigmoid(z_actual)
			elif self.activation_function == 'tanh':
				x = Utils.tanh(z_actual)
		ultima_capa = self.capas[-1]
		if x.ndim == 1:
			x = np.vstack([1, x])
		elif x.ndim == 2:
			x = np.vstack([np.ones(x.shape[1]), x])
		else:
			raise Exception('RedNeuronal.py: invalid array dimension in forwardpropagation_z')
		z_actual = ultima_capa.dot(x)
		z.append(z_actual)
		return z

	# Guardar la partida actual (tableros + movimientos realizados) en el archivo
	def guardar_partida(self, partida, archivo_instancias):
		np.savez(archivo_instancias, np.array(partida[:-1]))
		os.rename(archivo_instancias, archivo_instancias + partida[-1])

	# Cargar la partida del archivo seleccionado.
	# Retorna una tupla:
	# -la primera componente contiene las instancias en un arreglo numpy (a su vez, cada instancia es otro arreglo numpy).
	# -la segunda componente contiene el valor final de la partida: -1 (perdió), 0 (empate) o +1 (ganó).
	def cargar_partida(self, archivo_instancias):
		if archivo_instancias[-2:] == '-1':
			resultado = -1
		else:
			resultado = int(archivo_instancias[-1])
		instancias = np.load(archivo_instancias)

		return resultado, instancias

	# Aplicar el algoritmo de backpropagation sobre el archivo de instancias seleccionado
	def backpropagation(self, archivo_instancias):
		resultado, instancias = self.cargar_partida(archivo_instancias)
		z = self.forwardpropagation_z()
		# Ajustar el error en la capa de salida
		capa_salida = self.capas[-1]
		capa_salida.dot(Utils.d_tanh())
		# Ajustar el error en las capas intermedias
		for i in range(len(self.capas)-1):
			pass

def guardar_red(archivo_pesos):
	print('[-] Guardando la red neuronal en "{file}"'.format(file=archivo_pesos))
	pass

def cargar_red(archivo_pesos):
	print('[-] Cargandp la red neuronal del archivo "{file}"'.format(file=archivo_pesos))
	pass

if __name__ == '__main__':
	# Test forwardpropagation
	# x = [[1, 2, 3], [0, 0, 0]]
	# red1 = RedNeuronal([3, 3, 1])
	# print(red1.forwardpropagation(x))
	# red2 = RedNeuronal([3, 1])
	# print(red2.forwardpropagation(x))
	# red3 = RedNeuronal([3, 7, 9, 8, 5, 2])
	# print(red3.forwardpropagation(x))

	# Test guardar_partida y cargar_partida
	# red = RedNeuronal([3, 3, 1])
	# red.guardar_partida([[1, 2, 3, 4], [5, 6, 7, 8], '-1'], 'test.npz')
	# resultado, instancias = red.cargar_partida('test.npz-1')
	# print(resultado)
	# print(list(instancias.values()))

	# Test fordwardpropagation_z
	# x = [[1, 2, 3], [0, 0, 0]]
	# red1 = RedNeuronal([3, 3, 1])
	# print(red1.forwardpropagation_z(x))
	# red2 = RedNeuronal([3, 1])
	# print(red2.forwardpropagation_z(x))
	# red3 = RedNeuronal([3, 7, 9, 8, 5, 2])
	# print(red3.forwardpropagation_z(x))
	pass
