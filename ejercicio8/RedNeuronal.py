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
		if not isinstance(neuronas, str):
			print('[-] Inicializando neuronas de la red con valores aleatorios')
			self.capas = []
			for i in range(len(neuronas)-1):
				neuronas_capa_acutal = neuronas[i] + 1  # Considerar la neurona de sesgo
				neuronas_capa_siguiente = neuronas[i + 1]
				capa = np.random.randn(neuronas_capa_siguiente, neuronas_capa_acutal)
				# Inicialización de Xavier/He
				capa = capa * np.sqrt(2 / (neuronas_capa_acutal + neuronas_capa_siguiente))
				self.capas.append(capa)
		else:
			print('[-] Inicializando neuronas de la red con valores del archivo {file}'.format(file=neuronas))
			self.capas = cargar_red(neuronas)
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
			x = Utils.activation_function(self.activation_function, capa.dot(x))
		# Aplicar siempre tanh a la última capa, para obtener un resultado en [-1,1]
		ultima_capa = self.capas[-1]
		x = Utils.extend_array(x)
		x = Utils.tanh(ultima_capa.dot(x))
		return x

	# Recibe una instancia y devuelve una lista con los valores de activación de cada capa.
	def forwardpropagation_a(self, input):
		x = np.array(input)
		x = Utils.reshape_array(x)
		a = [x]
		# Aplicar la función de acivación seleccionada en cada capa intermedia
		for i in range(len(self.capas) - 1):
			capa = self.capas[i]
			x = Utils.extend_array(x)
			x = Utils.activation_function(self.activation_function, capa.dot(x))
			a.append(x)
		# Aplicar siempre tanh a la última capa, para obtener un resultado en [-1,1]
		ultima_capa = self.capas[-1]
		x = Utils.extend_array(x)
		x = Utils.tanh(ultima_capa.dot(x))
		a.append(x)
		return a

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
	# Devuelve el error total y promedio que se cometió en la evaluación, junto con el error total y promedio
	# de las capas de la red.
	def backpropagation(self, archivo_instancias):
		print('[-] Comenzando backpropagation')
		resultado, instancias = self.cargar_partida(archivo_instancias)
		numero_instancias = instancias.shape[0]
		# Aplicar Descenso por Gradiente según el tamaño de batch y el tope de iteraciones indicado
		y = [(resultado*self.factor_descuento)**(self.batch_size-i) for i in range(self.batch_size-1)]
		y.append(resultado)
		y = np.array(y).reshape(1, len(y))
		total_delta = 0
		total_loss = 0
		for iter in range(numero_instancias, 0, -1):
			# Calcular el (mini) batch para la instancia número 'iter'
			if iter - self.batch_size < 0:
				batch = instancias[0:iter, :]
				y = y[:, -iter:]
			else:
				batch = instancias[iter - self.batch_size:iter, :]

			# Ajustar el error en la capa de salida
			a = self.forwardpropagation_a(instancias[iter-1])
			y1 = self.forwardpropagation(batch)
			total_loss += np.average(y1 - y)
			delta_salida = np.average(y1 - y) * Utils.d_tanh(a[-1])  # Producto componente a componente
			delta_salida = np.average(delta_salida)
			total_delta += delta_salida

			# Ajustar los pesos de cada capa
			delta_l_anterior = delta_salida
			for l in range(len(self.capas) - 1, -1, -1):
				# Calcular delta de la capa actual
				capa_l = self.capas[l][:, 1:]
				delta_l_actual = capa_l.T.dot(delta_l_anterior)
				delta_l_actual *= Utils.d_activation_function(self.activation_function, a[l])
				total_delta += np.sum(delta_l_actual)
				# Calcular el gradiente sobre los pesos de la capa actual
				gradiente = delta_l_actual * a[l]
				# Ajustar pesos de la capa actual
				self.descenso_gradiente(capa_l, gradiente.T)
				delta_l_anterior = delta_l_actual
			y *= self.factor_descuento

		print('    Total loss: {err}'.format(err=total_loss))
		print('    Avg. loss: {err}'.format(err=total_loss / numero_instancias))
		print('    Total delta: {err}'.format(err=total_delta))
		print('    Avg. delta: {err}'.format(err=total_delta / (self.numero_neuronas + numero_instancias)))
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
	# Test backpropagation
	red = RedNeuronal([85, 20, 10, 1], 'tanh', 0.9, 2, 0.01, 0.5, 0.9)
	print(len(red.capas))
	print(red.capas[0].shape)
	print(red.capas[1].shape)
	print(red.capas[2].shape)
	red.backpropagation('partida1.npz0')
