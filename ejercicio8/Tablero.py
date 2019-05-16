from Constantes import *
from enum import Enum
from math import sqrt
import numpy as np

'''
La clase tablero contiene las posiciones del tablero, las posiciones de las
fichas de los dos jugadores y algunas cantidades de interés como el número
de fichas de cada jugador que llegó a la punta opuesta de la estrella, 
el número de fichas que no salieron aún de la propia punta de la estrella, 
la distancia vertical de las fichas a la punta opuesta de la estrella y 
la cantidad de fichas adyacentes que son de un mismo jugador o de cualquier jugador.
Además, la clase provee métodos para calcular posibles movimientos.
Por fuera de la clase se provee de un método para generar nuevos tableros a partir de 
una lista de posibles movimientos.
'''

class Color(Enum):
	Blancas = "blancas"
	Negras = "negras"

class Tablero:
	def __init__(self):

		# Inicializar las piezas de ambos jugadores (blancas y negras)
		# Las negras comienzan en la punta superior de la estrella y las blancas en la punta inferior
		self.negras = punta_negra.copy()
		self.blancas = punta_blanca.copy()
		self.largo_tablero = 8

		# Tupla del tablero
		self.tupla = {
			"distancia_blancas" : self.distancia(Color.Blancas),
			"distancia_negras" : self.distancia(Color.Negras),
			"fichas_blancas_en_punta_opuesta" : self.fichas_en_punta_opuesta(Color.Blancas),
			"fichas_negras_en_punta_opuesta" : self.fichas_en_punta_opuesta(Color.Negras),
			"posiciones_disminuyen_distancia_blancas" : self.posiciones_disminuyen_distancia_jugador(Color.Blancas),
			"posiciones_disminuyen_distancia_negras" : self.posiciones_disminuyen_distancia_jugador(Color.Negras),
			"distancia_ultima_ficha_a_primer_espacio_libre_blancas" : self.distancia_ultima_ficha_a_primer_espacio_libre(Color.Blancas),
			"distancia_ultima_ficha_a_primer_espacio_libre_negras" : self.distancia_ultima_ficha_a_primer_espacio_libre(Color.Negras),
		}
        
	# Retorna una copia (deep copy) del tablero actual
	def copy(self):
		tablero = Tablero()
		tablero.blancas = self.blancas.copy()
		tablero.negras = self.negras.copy()
		tablero.tupla = self.tupla.copy()
		return tablero

    # Devuelve los elementos que representan el tablero como una tupla.
    # El orden es el que espera la función de valoración del jugador AI.
    # El orden es:
    #("distancia_blancas", "distancia_negras",
    # "fichas_blancas_en_punta_opuesta", "fichas_negras_en_punta_opuesta",
    # "posiciones_disminuyen_distancia_blancas", "posiciones_disminuyen_distancia_negras",
    # "posibles_movimientos_blancas", "posibles_movimientos_negras")
	def obtener_tupla(self):
		return [self.tupla["distancia_blancas"], self.tupla["distancia_negras"],
                self.tupla["fichas_blancas_en_punta_opuesta"], self.tupla["fichas_negras_en_punta_opuesta"],
                self.tupla["posiciones_disminuyen_distancia_blancas"], self.tupla["posiciones_disminuyen_distancia_negras"],
                self.tupla["distancia_ultima_ficha_a_primer_espacio_libre_blancas"], self.tupla["distancia_ultima_ficha_a_primer_espacio_libre_negras"]]
    
	# tablero_actual es una instancia de Tablero
	# ficha es una tupla con la posición de la ficha a mover
	# movimiento es una tupla con la nueva posición de la ficha
	def actualizar_tablero(self, ficha, movimiento, color):
		lista = self.negras if color == Color.Negras else self.blancas
		lista.remove(ficha)
		lista.append(movimiento)
		self.actualizar_tupla(color, ficha, movimiento)

	def actualizar_tupla(self, color, ficha, movimiento):
		if color == Color.Blancas:
			self.tupla["distancia_blancas"] = self.distancia(Color.Blancas)
			if not(ficha in punta_negra) and movimiento in punta_negra:
				self.tupla["fichas_blancas_en_punta_opuesta"] += 1
			elif ficha in punta_negra and not(movimiento in punta_negra):
				self.tupla["fichas_blancas_en_punta_opuesta"] -= 1
			self.tupla["posiciones_disminuyen_distancia_blancas"] = self.posiciones_disminuyen_distancia_jugador(Color.Blancas)
			self.tupla["distancia_ultima_ficha_a_primer_espacio_libre_blancas"] = self.distancia_ultima_ficha_a_primer_espacio_libre(Color.Blancas)
		else:
			self.tupla["distancia_negras"] = self.distancia(Color.Negras)
			if not(ficha in punta_blanca) and movimiento in punta_blanca:
				self.tupla["fichas_negras_en_punta_opuesta"] += 1
			elif ficha in punta_blanca and not(movimiento in punta_blanca):
				self.tupla["fichas_negras_en_punta_opuesta"] -= 1
			self.tupla["posiciones_disminuyen_distancia_negras"] = self.posiciones_disminuyen_distancia_jugador(Color.Negras)
			self.tupla["distancia_ultima_ficha_a_primer_espacio_libre_negras"] = self.distancia_ultima_ficha_a_primer_espacio_libre(Color.Negras)

	#Retorna la suma de las distancias de las fichas de color "color" hacia la fila libre mas lejana de la punta opuesta
	def distancia(self, color):
		contador = 0
		ultima_fila = -self.largo_tablero if color == Color.Negras else self.largo_tablero
		lista = self.negras if color == Color.Negras else self.blancas
		for pos_x, _ in lista:
			contador += abs(ultima_fila - pos_x)
		return contador

	#Retorna la cantidad de fichas en la punta opuesta del tablero para el color "color"
	def fichas_en_punta_opuesta(self, color):
		contador = 0
		lista = self.negras if color == Color.Negras else self.blancas
		punta_opuesta = punta_blanca if color == Color.Negras else punta_negra
		for pos in lista:
				if pos in punta_opuesta:
					contador += 1
		return contador

	# Dadas las coordenadas cartesianas de una posición (en una tupla) devuelve True sii la posición pertenece al tablero
	def pertenece_al_tablero(self, pos):

		pos_x,_ = pos
		if pos_x <= 8 and pos_x > 4:
			return pos in punta_negra
		elif pos_x <= 4 and pos_x > 0:
			return pos in parte_media_superior
		elif pos_x == 0:
			return pos in parte_media_central
		elif pos_x < 0 and pos_x >= -4:
			return pos in parte_media_inferior
		else:
			return pos in punta_blanca

	# Dadas las coordenadas cartesianas de una posición (en una tupla) devuelve True sii la posición está ocupada por una ficha
	# No chequea si la posición es factible (si pertence al tablero)
	def posicion_ocupada(self, pos):

		return pos in self.negras or pos in self.blancas

	# Dadas las coordenadas cartesianas de una posición (en una tupla) devuelve una tupla con dos listas:
	# la primera contiene las posiciones adyacentes libres; la segunda, las posiciones adyacentes ocupadas
	def posiciones_adyacentes(self, pos):

		adyacentes_libres = []
		adyacentes_ocupadas = []

		for dir_x,dir_y in direcciones:
			# chequear si la dirección es factible (cae dentro del tablero)
			pos_x, pos_y = pos
			nueva_pos = (pos_x+dir_x, pos_y+dir_y)
			if self.pertenece_al_tablero(nueva_pos):
				if not self.posicion_ocupada(nueva_pos):
					adyacentes_libres.append(nueva_pos)
				else:
					adyacentes_ocupadas.append(nueva_pos)

		return (adyacentes_libres, adyacentes_ocupadas)

	# Dada la posición de una ficha, devuelve una lista con posibles nuevas posiciones para la misma
	# de acuerdo con las reglas del juego
	def posibles_movimientos(self, pos):

		posibles_movimientos = set()	# conjunto con los posibles movimientos (posiciones libres)
		posibles_saltos = set()			# conjunto que contiene posiciones libres (salvo la posición inicial, que tiene la ficha que se va a mover) desde las que se podría saltar
	
		adyacentes_libres, adyacentes_ocupadas = self.posiciones_adyacentes(pos)
		posibles_movimientos.update(adyacentes_libres)
		posibles_saltos.add(pos)

		while posibles_saltos:
			actual_pos = posibles_saltos.pop()
			actual_pos_x,actual_pos_y = actual_pos
			for dir_x,dir_y in direcciones:
				ady_pos = (actual_pos_x+dir_x, actual_pos_y+dir_y)
				if self.pertenece_al_tablero(ady_pos):
					# posible salto
					if self.posicion_ocupada(ady_pos):
						ady_pos_x,ady_pos_y = ady_pos
						nueva_pos = (ady_pos_x+dir_x, ady_pos_y+dir_y)
						if self.pertenece_al_tablero(nueva_pos) and not self.posicion_ocupada(nueva_pos) and not(nueva_pos in posibles_movimientos):
							# el salto es posible
							posibles_movimientos.add(nueva_pos)
							posibles_saltos.add(nueva_pos)

		return list(posibles_movimientos)

	#Retorna las cantidad de movimientos posibles para el jugador con color "color", que lo acercan a la punta opuesta
	def posiciones_disminuyen_distancia_jugador(self, color):
		contador = 0
		lista = self.negras if color == Color.Negras else self.blancas
		for pos_x,pos_y in lista:
			posibles_movimientos = self.posibles_movimientos((pos_x,pos_y))
			contador += len(posibles_movimientos)
			for movimiento_x,_ in posibles_movimientos:
				if (color == Color.Blancas and movimiento_x <= pos_x) or (color == Color.Negras and movimiento_x >= pos_x):
					contador -= 1
		return contador
  
	#Retorna la distancia entre la ultima ficha a la posicion libre mas lejana.
	def distancia_ultima_ficha_a_primer_espacio_libre(self, color):
		# encotnrar la ultima ficha
		fichas = self.negras if color == Color.Negras else self.blancas
		ficha_ultima = max(fichas) if color == Color.Negras else min(fichas)

		# encontrar la posicion libre mas lejana
		posiciones_meta = punta_blanca if color == Color.Negras else punta_negra
		posiciones_meta_aux = posiciones_meta.copy()
		for posicion in posiciones_meta:
			if self.posicion_ocupada(posicion):
				posiciones_meta_aux.remove(posicion)

		if posiciones_meta_aux:
			posicion_libre_mas_lejana = min(posiciones_meta_aux) if color == Color.Negras else max(posiciones_meta_aux)
		else:
			posicion_libre_mas_lejana = min(punta_blanca) if color == Color.Negras else max(punta_negra)
		return sqrt(sum([(a - b) **2 for a, b in zip(ficha_ultima, posicion_libre_mas_lejana)]))
    #Retorna true si hay un ganador para el tablero actual
	def hay_ganador(self):
		return self.tupla["fichas_blancas_en_punta_opuesta"] == 10 or self.tupla["fichas_negras_en_punta_opuesta"] == 10
    
    #Retorna el ganador solo en caso que haya (hay_ganador == true) sino retorna None
	def ganador(self):
		if self.tupla["fichas_blancas_en_punta_opuesta"] == 10:
			return Color.Blancas
		elif self.tupla["fichas_negras_en_punta_opuesta"] == 10:
			return Color.Negras
		else:
			return None

	# Para debugging
	def imprimir_tablero(self):

		ancho = round(25/2)
		altura = round(17/2)
		casillas_en_rectangulo = 0

		for i in range(altura, -altura-1, -1):
			for j in range(ancho, -ancho-1, -1):
				if self.pertenece_al_tablero((i,j)):
					print("0", end="")
					casillas_en_rectangulo += 1
				else:
					print("*", end="")
			print()

		print("Casillas dentro del rectángulo: {casillas_en_rectangulo}".format(casillas_en_rectangulo=casillas_en_rectangulo))
		print("Casillas en instancia de Tablero: {len(punta_negra) + len(punta_blanca) + len(parte_media_superior) + len(parte_media_inferior) + len(parte_media_central)}")
		print("Fichas blancas: {len(tablero.blancas)}")
		print("Fichas negras: {len(tablero.negras)}")

	def imprimir_tablero_con_fichas(self):

		ancho = round(25/2)
		altura = round(17/2)

		for i in range(altura, -altura-1, -1):
			for j in range(ancho, -ancho-1, -1):
				if self.pertenece_al_tablero((i,j)):
					if (i,j) in self.blancas:
						print("b", end="")
					elif (i,j) in self.negras:
						print("n", end="")
					else:
						print("0", end="")
				else:
					print(" ", end="")
			print()

	def tablero2lista(self):
		tablero_lista = []
		lista_posiciones_tablero = [punta_negra, parte_media_superior, parte_media_inferior, parte_media_central, punta_blanca]
		for lista_posiciones in lista_posiciones_tablero:
			for pos in lista_posiciones:
				if pos in self.blancas:
					tablero_lista.append(1)
				elif pos in self.negras:
					tablero_lista.append(-1)
				else:
					tablero_lista.append(0)
		return tablero_lista

# Para debuggeing
if __name__ == '__main__':
	tablero = Tablero()
	tablero.imprimir_tablero()

	arr = tablero.tablero2lista()
	print(arr)
	print(len(arr))
