from ejercicio8.Juego import *
from ejercicio8.Jugadores import *
import sys
import os

uso = """
Invocar como python3 Corpus.py [archivo conf] donde
'archivo_conf' es un archivo de configuración. A modo de ejemplo, ver Corpus.conf.
"""

if __name__ == '__main__':
    directorio, jugador1_str, jugador2_str, num_partidas = Utils.parsear_conf(sys.argv[1])
    num_partidas = int(num_partidas)

    jugadores = []
    print("[*] Creando jugadores")
    # Ambos son AIs.
    if jugador1_str != "Aleatorio" and jugador2_str != "Aleatorio":
        jugadores = ["AI1", "AI2"]
        jugador1 = AI(Color.Blancas, "AI1", None, True, factor_aprendizaje, directorio)
        print("[*] Leyendo pesos del jugador 1")
        jugador1.cargar_pesos(jugador1_str)
        jugador2 = AI(Color.Negras, "AI2", None, False, factor_aprendizaje)
        print("[*] Leyendo pesos del jugador 2")
        jugador2.cargar_pesos(jugador2_str)
        jugador2.alternar_pesos()

    # Solo el primero es AI
    elif jugador1_str != "Aleatorio" and jugador2_str == "Aleatorio":
        jugadores = ["AI", "Aleatorio"]
        jugador1 = AI(Color.Blancas, "AI", None, True, factor_aprendizaje, directorio)
        print("[*] Leyendo pesos del jugador 1")
        jugador1.cargar_pesos(jugador1_str)
        jugador2 = Aleatorio(Color.Negras, "Aleatorio")
    # Solo el segundo es AI
    elif jugador1_str == "Aleatorio" and jugador2_str != "Aleatorio":
        jugadores = ["Aleatorio", "AI"]
        jugador1 = AI(Color.Blancas, "AI", None, True, factor_aprendizaje, directorio)
        jugador2 = Aleatorio(Color.Negras, "Aleatorio")
        print("[*] Leyendo pesos del jugador 2")
        jugador1.cargar_pesos(jugador2_str)
    # Ninguno es AI
    else:
        print("***Valores de jugadores incorrectos. Al menos uno debe ser una AI.***")
        print(uso)
        exit()

    victorias = 0
    empates = 0

    # Crear un directorio para guardar los datos de entrenamiento
    os.mkdir(directorio)
    print("[*] Se crea el directorio {dir}".format(dir=directorio))

    color_que_empieza = Color.Blancas

    print("[*] Comenzando la serie de partidas")
    for i in range(num_partidas):
        print("[-] Comenzando partida {num}".format(num=i+1))
        juego = Juego(jugador2, jugador1)
        ganador = juego.jugar(color_que_empieza)
        color_que_empieza = Color.Blancas if (color_que_empieza == Color.Negras) else Color.Negras
        #Para debugging
        print("Partida {partida} => Ganó {ganador}.".format(partida=i+1, ganador=ganador))
        # Chequear que el ganador sea la AI o la AI más reciente (AI1)
        if ganador is not None and "AI" in ganador:
            if ganador != "AI2":
                victorias += 1
        elif ganador is None:
            empates += 1
        print("Victorias = {victorias}".format(victorias=victorias))
        print("Empates = {empates}".format(empates=empates))

    string_evol_vict_formateado = "La AI ganó el {porcentaje}% de las veces".format(porcentaje=victorias/num_partidas*100)
    string_evol_emp_formateado = "La AI empató el {porcentaje}% de las veces".format(porcentaje=empates/num_partidas*100)
    print(string_evol_vict_formateado)
    print(string_evol_emp_formateado)
    string_evol_vict_formateado += "\n"
    string_evol_emp_formateado += "\n"
