#Rprop
#Learning rate adaptativo
#Gradient checking

import numpy as np
import ejercicio8.Utils as Utils
import os

class RedNeuronal(object):
    def __init__(self, neuronas, activation_function='tanh', factor_descuento=0.9, batch_size=10,
                 learning_rate=0.01, regularization=0.5, momentum=0.9, epsilon=1e-6):
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
        self.epsilon = epsilon
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
        # a = [Utils.extend_array(x)]
        # Aplicar la función de acivación seleccionada en cada capa intermedia
        for i in range(len(self.capas) - 1):
            capa = self.capas[i]
            x = Utils.extend_array(x)
            x = Utils.activation_function(self.activation_function, capa.dot(x))
            a.append(x)
        # a.append(Utils.extend_array(x))
        # Aplicar siempre tanh a la última capa, para obtener un resultado en [-1,1]
        ultima_capa = self.capas[-1]
        x = Utils.extend_array(x)
        x = Utils.tanh(ultima_capa.dot(x))
        a.append(x)
        return a

    # Guardar la partida actual (tableros + movimientos realizados) en el archivo
    def guardar_partida(self, partida, archivo_instancias):
        np.savez(archivo_instancias, np.array(partida))

    def guardar_evaluaciones(self, evals, archivo_evals):
        with open(archivo_evals, 'w') as archivo:
            for q in evals:
                archivo.write(str(q)+'\n')

    # Cargar la partida del archivo seleccionado.
    # Retorna las instancias en un arreglo numpy (a su vez, cada instancia es otro arreglo numpy).
    def cargar_partida(self, archivo_instancias):
        return np.load(archivo_instancias)['arr_0']

    def cargar_evaluaciones(self, archivo_evals):
        with open(archivo_evals, 'r') as archivo:
            evals = archivo.readlines()
        for i in range(len(evals)):
            evals[i] = float(evals[i])
        return evals

    # Aplicar el algoritmo de backpropagation sobre el archivo de instancias seleccionado.
    # Devuelve el error total y promedio que se cometió en la evaluación, junto con el error total y promedio
    # de las capas de la red.
    def backpropagation(self, archivo_instancias, archivo_evals, check_gradient=False):
        print('[-] Comenzando backpropagation')
        instancias = self.cargar_partida(archivo_instancias)
        evaluaciones = self.cargar_evaluaciones(archivo_evals)
        numero_instancias = instancias.shape[0]
        # Aplicar Descenso por Gradiente según el tamaño de batch y el tope de iteraciones indicado
        evals = np.array(evaluaciones).reshape(1, len(evaluaciones))
        total_delta = 0
        total_loss = 0
        total_gradient = []
        for iter in range(numero_instancias, 0, -1):
            # Calcular el (mini) batch para la instancia número 'iter'
            if iter - self.batch_size < 0:
                batch = instancias[0:iter, :]
                y = y[:, -iter:]
            else:
                batch = instancias[iter - self.batch_size:iter, :]
                y = evals[:, (iter-self.batch_size):iter]

            # Ajustar el error en la capa de salida
            a = self.forwardpropagation_a(instancias[iter-1])
            y1 = self.forwardpropagation(batch)
            total_loss += np.average(y1 - y)
            delta_salida = np.average(y1 - y) * Utils.d_tanh(a[-1])  # Producto componente a componente
            delta_salida = np.average(delta_salida)
            total_delta += delta_salida

            # Ajustar los pesos de cada capa
            delta_l_anterior = np.array(delta_salida)
            for l in range(len(self.capas) - 1, -1, -1):
                # Calcular el gradiente sobre los pesos de la capa actual
                capa_l = self.capas[l]
                gradiente = delta_l_anterior * Utils.extend_array(a[l]).T
                if check_gradient and iter == numero_instancias:
                    total_gradient.append(gradiente)
                # Ajustar pesos de la capa actual
                self.descenso_gradiente(capa_l, gradiente)
                # Calcular delta de la capa actual
                delta_l_actual = capa_l.T.dot(delta_l_anterior)
                delta_l_actual *= Utils.d_activation_function(self.activation_function, Utils.extend_array(a[l]))
                total_delta += np.sum(delta_l_actual)
                if delta_l_actual.ndim == 2:
                    delta_l_anterior = delta_l_actual[1:, :]
                else:
                    delta_l_anterior = delta_l_actual

            if check_gradient and iter == numero_instancias:
                self.gradient_checking(instancias[iter-1], total_gradient)
                total_gradient = []

        print('    Total loss: {err}'.format(err=total_loss))
        print('    Avg. loss: {err}'.format(err=total_loss / numero_instancias))
        print('    Total delta: {err}'.format(err=total_delta))
        print('    Avg. delta: {err}'.format(err=total_delta / (self.numero_neuronas + numero_instancias)))
        return delta_salida, total_loss, total_loss / self.numero_neuronas

    def gradient_checking(self, input, gradient):
        error = 0
        for i in range(len(gradient)):
            j = len(gradient) - 1 - i
            print(gradient[j].shape)
            print(self.capas[i].shape)
            for x, y in np.ndindex(gradient[j].shape):
                self.capas[i][x, y] += self.epsilon
                a_mas_epsilon = self.forwardpropagation(input)
                self.capas[i][x, y] -= 2 * self.epsilon
                a_menos_epsilon = self.forwardpropagation(input)
                self.capas[i][x, y] += self.epsilon
                aproximate_derivative = ((a_mas_epsilon - a_menos_epsilon) / (2 * self.epsilon))
                error += (gradient[j][x, y] - aproximate_derivative) ** 2
                print((gradient[j][x, y] - aproximate_derivative) ** 2)
        error = np.sqrt(error)[0, 0]
        print('    Gradient Cheking error: {err}'.format(err=error))

    def descenso_gradiente(self, pesos, gradiente):
        if self.momentum == 0:
            pesos -= self.learning_rate * gradiente
        else:
            pesos -= self.learning_rate * (self.momentum*pesos + (1 - self.momentum)*gradiente)
        if self.regularization != 0:
            pesos -= self.regularization * self.learning_rate * pesos


def guardar_red(archivo_pesos):
    print('[-] Guardando la red neuronal en "{file}"'.format(file=archivo_pesos))
    pass


def cargar_red(archivo_pesos):
    print('[-] Cargandp la red neuronal del archivo "{file}"'.format(file=archivo_pesos))
    pass


if __name__ == '__main__':
    # Test backpropagation
    red = RedNeuronal([85, 8, 8, 1], 'sigmoid', 0.9, 10, 0.01, 0.5, 0.9)
    # red.backpropagation('partida1.npz-1', False)
    red.backpropagation('partida1.npz', 'eval1.txt', True)
