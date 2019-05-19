#Rprop
#Learning rate adaptativo
#Gradient checking

import numpy as np
import ejercicio8.Utils as Utils
import os

class RedNeuronal(object):
	def __init__(self, neuronas, activation_function='tanh', factor_descuento=0.9, batch_size=10,
				 learning_rate=0.01, regularization=0.5, momentum=0.9):
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
		self.factor_descuento = factor_descuento
		self.batch_size = batch_size
		self.learning_rate = learning_rate
		self.regularization = regularization
		self.momentum = momentum
		self.numero_neuronas = sum(neuronas)

	# Recibe una instancia y devuelve una valoración del tablero.
	def forwardpropagation(self, input):
		x = np.array(input)
		x = Utils.reshape_array(x)
		# Aplicar la función de acivación seleccionada en cada capa intermedia
		for i in range(len(self.capas)-1):
			capa = self.capas[i]
			x = Utils.extend_array(x)
			if self.activation_function == 'sigmoid':
				x = Utils.sigmoid(capa.dot(x))
			elif self.activation_function == 'tanh':
				x = Utils.tanh(capa.dot(x))
		# Aplicar siempre tanh a la última capa, para obtener un resultado en [-1,1]
		ultima_capa = self.capas[-1]
		x = Utils.extend_array(x)
		x = Utils.tanh(ultima_capa.dot(x))
		return x

	# Recibe una instancia y devuelve una lista con los valores z de cada capa.
	def forwardpropagation_z(self, input):
		x = np.array(input)
		x = Utils.reshape_array(x)
		z = [x]
		# Aplicar la función de acivación seleccionada en cada capa intermedia
		for i in range(len(self.capas) - 1):
			capa = self.capas[i]
			x = Utils.extend_array(x)
			z_actual = capa.dot(x)
			z.append(z_actual)
			if self.activation_function == 'sigmoid':
				x = Utils.sigmoid(z_actual)
			elif self.activation_function == 'tanh':
				x = Utils.tanh(z_actual)
		ultima_capa = self.capas[-1]
		x = Utils.extend_array(x)
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
		instancias = np.load(archivo_instancias)['arr_0']

		return resultado, instancias

	# Aplicar el algoritmo de backpropagation sobre el archivo de instancias seleccionado.
	# Devuelve el error que se cometió en la capa de salida, el error total de la red y el error promedio.
	def backpropagation(self, archivo_instancias):
		print('[-] Comenzando backpropagation')
		resultado, instancias = self.cargar_partida(archivo_instancias)
		numero_instancias = instancias.shape[0]
		# Aplicar Descenso por Gradiente según el tamaño de batch y el tope de iteraciones indicado
		y = [(resultado*self.factor_descuento)**(self.batch_size-i) for i in range(self.batch_size-1)]
		y.append(resultado)
		y = np.array(y).reshape(1, len(y))
		for iter in range(numero_instancias, 0, -1):
			total_loss = 0
			# Calcular el (mini) batch para la instancia número 'iter'
			y *= self.factor_descuento
			if iter - self.batch_size < 0:
				batch = instancias[0:iter, :]
				y = y[-iter:]
			else:
				batch = instancias[iter - self.batch_size:iter, :]

			y1 = self.forwardpropagation(batch)
			z = self.forwardpropagation_z(instancias[iter-1])
			print(batch)
			# Ajustar el error en la capa de salida
			capa_salida = self.capas[-1]
			delta_salida = (y1 - y) * Utils.d_tanh(z[-1])  # Producto componente a componente
			delta_salida = np.average(delta_salida)

			# Ajustar pesos de la capa de salida
			gradiente = delta_salida
			print(gradiente)
			if self.activation_function == 'sigmoid':
				gradiente *= Utils.sigmoid(z[-1])
			elif self.activation_function == 'tanh':
				gradiente *= Utils.tanh(z[-1])
			else:
				raise Exception('RedNeuronal.py: invalid activation function in backpropagation')
			self.descenso_gradiente(capa_salida, gradiente)

			print('    Output loss: {err}'.format(err=delta_salida))
			total_loss += delta_salida
			# Ajustar el error en las capas intermedias
			delta_l_anterior = delta_salida
			for l in range(len(self.capas) - 2, 0, -1):
				# Calcular delta de la capa actual
				capa_l = self.capas[l]
				delta_l_actual = capa_l.T.dot(delta_l_anterior)
				if self.activation_function == 'sigmoid':
					delta_l_actual *= Utils.d_sigmoid(z[l])
				elif self.activation_function == 'tanh':
					delta_l_actual *= Utils.d_tanh(z[l])
				else:
					raise Exception('RedNeuronal.py: invalid activation function in backpropagation')
				# Calcular el gradiente sobre los pesos de la capa actual
				if self.activation_function == 'sigmoid':
					gradiente = delta_l_actual * Utils.sigmoid(z[l-1])
				elif self.activation_function == 'tanh':
					gradiente = gradiente * Utils.tanh(z[l-1])
				else:
					raise Exception('RedNeuronal.py: invalid activation function in backpropagation')
				# Ajustar pesos de la capa actual
				self.descenso_gradiente(capa_l, gradiente)

			print('    Total loss: {err}'.format(err=total_loss))
			print('    Avg. loss: {err}'.format(err=total_loss / self.numero_neuronas))
		return delta_salida, total_loss, total_loss / self.numero_neuronas

	def descenso_gradiente(self, pesos, gradiente):
		if self.momentum is None:
			pesos -= self.learning_rate * gradiente
		else:
			pesos -= self.learning_rate * (self.momentum*pesos + (1 - self.momentum)*gradiente)
		if self.regularization is not None:
			pesos -= self.regularization * self.learning_rate * pesos

def guardar_red(archivo_pesos):
	print('[-] Guardando la red neuronal en "{file}"'.format(file=archivo_pesos))
	pass

def cargar_red(archivo_pesos):
	print('[-] Cargandp la red neuronal del archivo "{file}"'.format(file=archivo_pesos))
	pass

if __name__ == '__main__':
	# Test forwardpropagation
	x = [[1, 2, 3], [0, 0, 0]]
	red1 = RedNeuronal([3, 3, 1])
	print(red1.forwardpropagation(x))
	red2 = RedNeuronal([3, 1])
	print(red2.forwardpropagation(x))
	red3 = RedNeuronal([3, 7, 9, 8, 5, 2])
	print(red3.forwardpropagation(x))

	# Test guardar_partida y cargar_partida
	# red = RedNeuronal([4, 3, 1])
	# red.guardar_partida([[1, 2, 3, 4], [5, 6, 7, 8], [1, 3, 5, 7], [2, 4, 6, 8], '-1'], 'test.npz')
	# resultado, instancias = red.cargar_partida('test.npz-1')
	# print(resultado)
	# print(instancias)

	# Test fordwardpropagation_z
	x = [[1, 2, 3], [0, 0, 0]]
	red1 = RedNeuronal([3, 3, 1])
	print(red1.forwardpropagation_z(x))
	red2 = RedNeuronal([3, 1])
	z = red2.forwardpropagation_z(x)
	print(z[-1])
	print(z[-1].shape)
	red3 = RedNeuronal([3, 7, 9, 8, 5, 2])
	z = red3.forwardpropagation_z(x)
	print(z[-1])
	print(z[-1].shape)

	# Test backpropagation
	red = RedNeuronal([4, 3, 1], 'tanh', 0.9, 2, 0.01, 0.5, 0.9)
	red.backpropagation('test.npz-1')
