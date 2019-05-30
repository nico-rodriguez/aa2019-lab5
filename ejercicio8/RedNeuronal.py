import numpy as np
from sklearn.neural_network import MLPRegressor
import joblib


class RedNeuronal(object):
    def __init__(self, neuronas, activation_function='tanh', factor_descuento=0.9, num_iters=200, batch_size=32,
                 learning_rate=0.0001, regularization=0.5, momentum=0.9):
        # Inicializar capas y neuronas de la red
        if not isinstance(neuronas, str):
            print('[-] Inicializando neuronas de la red con valores aleatorios')
            self.mlp = MLPRegressor(hidden_layer_sizes=neuronas, activation=activation_function, solver='adam',
                                    alpha=regularization, batch_size=batch_size, learning_rate='adaptive',
                                    learning_rate_init=learning_rate, max_iter=num_iters, momentum=momentum)
        else:
            print('[-] Inicializando neuronas de la red con valores del archivo {file}'.format(file=neuronas))
            self.mlp = cargar_red(neuronas)

        self.factor_descuento = factor_descuento
        print('[-] Red neuronal inicializada')

    # Recibe una instancia y devuelve una valoración del tablero.
    def forwardpropagation(self, input):
        return self.mlp.predict(np.array(input).reshape(1, -1))

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
    def backpropagation(self, archivo_instancias, archivo_evals):
        # print('[-] Comenzando backpropagation')
        instancias = self.cargar_partida(archivo_instancias)
        evaluaciones = self.cargar_evaluaciones(archivo_evals)
        self.mlp = self.mlp.partial_fit(instancias, evaluaciones)


def guardar_red(red, archivo_red):
    print('[-] Guardando la red neuronal en "{file}"'.format(file=archivo_red))
    joblib.dump(red, archivo_red)


def cargar_red(archivo_red):
    print('[-] Cargandp la red neuronal del archivo "{file}"'.format(file=archivo_red))
    return joblib.load(archivo_red)


if __name__ == '__main__':
    # Test backpropagation
    red = RedNeuronal((8,), 'tanh', 0.9, 100, 10, 0.01, 0.5, 0.9)
    red.backpropagation('partida1.npz', 'eval1.txt')
    print(red.mlp.predict(np.zeros(85).reshape(1, -1)))
